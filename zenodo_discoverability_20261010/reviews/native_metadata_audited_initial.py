"""Conservative same-record native metadata editor for rich legacy-incompatible records.

Only existing-record edit, metadata PUT and existing-record publish are permitted.
Never reserve a PID, create a record/version, modify files/access, or reuse an
unowned pending draft. Durable original/target snapshots precede every write.
"""
import argparse
import copy
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'zenodo_deposit_tool'))
import zenodo
import metadata_updates as legacy
from baseline import PacedClient, identity

ALLOWED_FIELDS = {'keywords', 'language', 'creators', 'related_identifiers', 'description', 'notes'}

def canonical(value):
    """Ignore only display labels attached to controlled vocabulary IDs."""
    if isinstance(value, list):
        return [canonical(v) for v in value]
    if isinstance(value, dict):
        return {k: canonical(v) for k, v in value.items()
                if not (k == 'title' and 'id' in value and isinstance(value['id'], str))}
    return value

def file_state(record):
    files = record['files']
    return {'enabled': files.get('enabled'), 'default_preview': files.get('default_preview'),
            'order': files.get('order'), 'count': files.get('count'), 'total_bytes': files.get('total_bytes'),
            'entries': {name: {k: entry.get(k) for k in ('id', 'key', 'checksum', 'size', 'access')}
                        for name, entry in files.get('entries', {}).items()}}

def protected(record):
    return {'id': record['id'], 'pids': record['pids'],
            'parent_id': record['parent']['id'], 'parent_pids': record['parent']['pids'],
            'versions': record['versions'], 'access': record['access'],
            'files': file_state(record), 'custom_fields': record['custom_fields']}

def translate(original, patch):
    if not patch or set(patch) - ALLOWED_FIELDS:
        raise RuntimeError('Native patch includes a prohibited or empty field set')
    md = copy.deepcopy(original['metadata'])
    for field, value in patch.items():
        if field == 'keywords':
            if any(set(s) != {'subject'} for s in md.get('subjects', [])):
                raise RuntimeError('Do not replace controlled subjects with free text')
            md['subjects'] = [{'subject': word} for word in value]
        elif field == 'language':
            if md.get('languages'):
                raise RuntimeError('Do not replace existing languages')
            md['languages'] = [{'id': value}]
        elif field == 'creators':
            creators = copy.deepcopy(md['creators'])
            if len(creators) != len(value):
                raise RuntimeError('Cannot alter author count')
            for author, changed in zip(creators, value):
                person = author['person_or_org']
                if changed['name'] != person['name']:
                    raise RuntimeError('Native route only permits adding author ORCID')
                ids = person.setdefault('identifiers', [])
                wanted = {'scheme': 'orcid', 'identifier': changed['orcid']}
                old = [i for i in ids if i['scheme'] == 'orcid']
                if old and old != [wanted]:
                    raise RuntimeError('Cannot overwrite an existing author ORCID')
                if not old:
                    ids.append(wanted)
            md['creators'] = creators
        elif field == 'related_identifiers':
            existing = original['metadata'].get('related_identifiers', [])
            by_key = {(r['identifier'], r['relation_type']['id']): r for r in existing}
            result = []
            for link in value:
                key = (link['identifier'], link['relation'].lower())
                if key in by_key:
                    result.append(copy.deepcopy(by_key[key]))
                else:
                    r = {'identifier': link['identifier'], 'scheme': link['scheme'],
                         'relation_type': {'id': link['relation'].lower()}}
                    if link.get('resource_type'):
                        r['resource_type'] = {'id': link['resource_type']}
                    result.append(r)
            if set(by_key) - {(r['identifier'], r['relation_type']['id']) for r in result}:
                raise RuntimeError('Cannot remove existing related identifiers')
            md[field] = result
        elif field == 'notes':
            descriptions = md.setdefault('additional_descriptions', [])
            retained = [d for d in descriptions if d['type']['id'] != 'notes']
            retained.append({'description': value, 'type': {'id': 'notes'}})
            md['additional_descriptions'] = retained
        else:
            md[field] = value
    return md

def require_state(record, session, changed):
    if protected(record) != session['protected']:
        raise RuntimeError('Native record identity/PIDs/versions/files/access/custom fields changed')
    expected = session['target_metadata'] if changed else session['original']['metadata']
    if canonical(record['metadata']) != canonical(expected):
        raise RuntimeError('Native metadata differs from the reviewed target')

def save(path, session, phase):
    session.update(phase=phase, updated_utc=datetime.now(timezone.utc).isoformat())
    zenodo.save_state(path, session)

def read_native(client, record_id, draft=False):
    return client.native_get(record_id, draft=draft)

def run(record_id, patch_path, publish=False):
    place = zenodo.STATE_DIR / f'native-metadata-{record_id}-production.json'
    receipt_dir = HERE / 'receipts' / str(record_id)
    client = PacedClient('production', zenodo.token_for('production'))
    patch = json.loads(patch_path.read_text())['metadata']
    with legacy.record_lock(record_id, 'production'):
        session = json.loads(place.read_text()) if place.exists() else None
        if publish:
            if not session or session['patch'] != patch or session['phase'] != 'staged':
                raise RuntimeError('Only a fully verified matching staged session can publish')
            current = read_native(client, record_id, draft=True)
            require_state(current, session, changed=True)
            save(place, session, 'publish_requested')
            # No automatic mutation retry. Uncertain outcomes remain inspectable.
            client.request('POST', client.base + f'/api/records/{record_id}/draft/actions/publish',
                           accept='application/vnd.inveniordm.v1+json')
            current = read_native(client, record_id)
            require_state(current, session, changed=True)
            if not current.get('is_published') or current.get('is_draft'):
                raise RuntimeError('Native publication outcome not confirmed')
            save(place, session, 'published')
            (receipt_dir / 'native_published.json').write_text(json.dumps(current, indent=2, ensure_ascii=False)+'\n')
            return {'id': record_id, 'state': 'published', 'doi': current['pids']['doi']['identifier'],
                    'record_url': f'https://zenodo.org/records/{record_id}', 'files_and_identity_unchanged': True}
        if session:
            raise RuntimeError('Existing native session must be inspected before a new stage')
        dep = client.get(record_id)
        if dep.get('state') != 'done' or not dep.get('submitted'):
            raise RuntimeError('Refusing to reuse a pre-existing pending edit')
        original = read_native(client, record_id)
        baseline = json.loads((receipt_dir / 'before.json').read_text())
        versions = client.request('GET', client.base + f'/api/records/{record_id}/versions?size=100',
                                  accept='application/vnd.inveniordm.v1+json')
        if identity(original, versions) != baseline['identity']:
            raise RuntimeError('Native record/concept/version history baseline drift')
        for key in ('metadata', 'pids', 'custom_fields', 'access'):
            if original[key] != baseline['native'][key]:
                raise RuntimeError(f'Native public {key} baseline drift')
        if 'native_files' not in baseline or original['files'] != baseline['native_files']:
            raise RuntimeError('Native public file/preview baseline drift')
        target = translate(original, patch)
        session = {'id': record_id, 'original': original, 'protected': protected(original),
                   'patch': patch, 'target_metadata': target}
        save(place, session, 'edit_requested')
        client.request('POST', client.base + f'/api/records/{record_id}/draft',
                       accept='application/vnd.inveniordm.v1+json')
        draft = read_native(client, record_id, draft=True)
        require_state(draft, session, changed=False)
        save(place, session, 'update_requested')
        client.request('PUT', client.base + f'/api/records/{record_id}/draft',
                       {'metadata': target, 'custom_fields': original['custom_fields']},
                       accept='application/vnd.inveniordm.v1+json')
        draft = read_native(client, record_id, draft=True)
        require_state(draft, session, changed=True)
        save(place, session, 'staged')
        (receipt_dir / 'native_staged.json').write_text(json.dumps(draft, indent=2, ensure_ascii=False)+'\n')
        return {'id': record_id, 'state': 'ready_to_publish_metadata', 'unchanged_doi': original['pids']['doi']['identifier']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('record_id', type=int)
    parser.add_argument('patch', type=Path)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.record_id, args.patch, args.publish), indent=2))
