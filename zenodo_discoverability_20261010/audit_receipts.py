"""Independent, disk-only audit of frozen metadata proposals and public receipts.

Uses only the Python standard library. It neither imports the Zenodo client nor
reads credentials, modifies proposals, calls a network endpoint or runs Git.
Reports are regenerated atomically as additional completed receipts arrive.
"""
import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ALLOWED_PATCH_FIELDS = {
    'keywords', 'language', 'creators', 'related_identifiers', 'description',
    'notes', 'upload_type', 'publication_type',
}
PROTECTED_PATCH_FIELDS = {
    'doi', 'prereserve_doi', 'relations', 'version', 'publication_date', 'title',
    'license', 'access_right',
}
NATIVE_FIELDS = {
    'keywords': 'subjects', 'language': 'languages', 'creators': 'creators',
    'related_identifiers': 'related_identifiers', 'description': 'description',
    'notes': 'additional_descriptions', 'upload_type': 'resource_type',
    'publication_type': 'resource_type',
}
EMPTY_OPTIONAL = {
    'keywords': [], 'references': [], 'locations': [], 'notes': '', 'method': '',
    'language': '', 'custom': {},
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vocab_ids(value):
    """Ignore display titles only within an intentionally changed vocab field."""
    if isinstance(value, list):
        return [vocab_ids(v) for v in value]
    if isinstance(value, dict):
        return {k: vocab_ids(v) for k, v in value.items()
                if not (k == 'title' and isinstance(value.get('id'), str))}
    return value


def diffs(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            p = f'{path}.{key}' if path else key
            if key not in a or key not in b:
                out.append(p)
            else:
                out.extend(diffs(a[key], b[key], p))
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path + '.length']
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(diffs(x, y, f'{path}[{i}]'))
        return out
    return [] if a == b else [path]


def legacy_files(record):
    result = []
    files = record.get('files', [])
    if isinstance(files, dict):
        files = files.values()
    for item in files:
        result.append({'name': item.get('filename', item.get('name')),
                       'md5': str(item.get('checksum', item.get('md5', ''))).lower().removeprefix('md5:'),
                       'size': item.get('filesize', item.get('size'))})
    return sorted(result, key=lambda f: f['name'])


def native_files_projection(files):
    return sorted([{'name': name, 'md5': str(e['checksum']).lower().removeprefix('md5:'),
                    'size': e['size']} for name, e in files['entries'].items()],
                  key=lambda f: f['name'])


def legacy_compare(original, actual, patch):
    expected = {**copy.deepcopy(original), **copy.deepcopy(patch)}
    notes = []
    # Preserve generated public read-only metadata exactly too; it is not dropped
    # merely because the editor's writable target omits it.
    for field, empty in EMPTY_OPTIONAL.items():
        if field in expected and expected[field] == empty and field not in actual:
            expected.pop(field)
            notes.append({'field': field, 'kind': 'empty_optional_legacy_omission'})
    links = expected.get('related_identifiers')
    if isinstance(links, list) and isinstance(actual.get('related_identifiers'), list):
        for old, new in zip(links, actual['related_identifiers']):
            if 'scheme' not in old and 'scheme' in new:
                identifier = old.get('identifier', '')
                scheme = 'doi' if re.fullmatch(r'10\.\d{4,9}/\S+', identifier) else (
                    'url' if identifier.startswith(('https://', 'http://')) else None)
                if scheme and new == {**old, 'scheme': scheme}:
                    old['scheme'] = scheme
                    notes.append({'field': 'related_identifiers', 'kind': 'inferred_identifier_scheme'})
    return expected, notes


def expected_native(original, patch, record_id=None):
    """Independent reconstruction of intended native fields from frozen patch."""
    md = copy.deepcopy(original)
    if 'keywords' in patch:
        if any(set(x) != {'subject'} for x in md.get('subjects', [])):
            raise ValueError('Controlled subject would be replaced by free keywords')
        md['subjects'] = [{'subject': x} for x in patch['keywords']]
    if 'language' in patch:
        if md.get('languages'):
            raise ValueError('Existing native language is being replaced')
        md['languages'] = [{'id': patch['language']}]
    if 'description' in patch:
        md['description'] = patch['description']
    if 'notes' in patch:
        md['additional_descriptions'] = [x for x in md.get('additional_descriptions', [])
                                         if x.get('type', {}).get('id') != 'notes']
        md['additional_descriptions'].append({'description': patch['notes'], 'type': {'id': 'notes'}})
    if 'creators' in patch:
        if len(md['creators']) != len(patch['creators']):
            raise ValueError('Creator count changed')
        for author, addition in zip(md['creators'], patch['creators']):
            person = author['person_or_org']
            if person['name'] != addition['name']:
                # This one frozen, independently source-reviewed correction
                # reverses a wrongly serialized given/family name. Every
                # identifier, affiliation, role and other creator field stays
                # in the original copied structure; no general rename rule.
                if not (record_id == 22770864 and len(md['creators']) == 1
                        and addition == {'name': 'Kriebel, Alec',
                                         'affiliation': 'Independent Researcher',
                                         'orcid': '0009-0001-9320-500X'}
                        and person.get('type') == 'personal'
                        and person['name'] == 'Alec, Kriebel'
                        and person.get('given_name') == 'Kriebel'
                        and person.get('family_name') == 'Alec'):
                    raise ValueError('Creator identity changed')
                person.update(name='Kriebel, Alec', given_name='Alec', family_name='Kriebel')
            old = person.get('identifiers', [])
            wanted = {'scheme': 'orcid', 'identifier': addition['orcid']}
            orcids = [x for x in old if x['scheme'] == 'orcid']
            if orcids and orcids != [wanted]:
                raise ValueError('Existing ORCID changed')
            if not orcids:
                person.setdefault('identifiers', []).append(wanted)
    if 'related_identifiers' in patch:
        old = {(x['identifier'], x['relation_type']['id']): x
               for x in md.get('related_identifiers', [])}
        out = []
        for x in patch['related_identifiers']:
            key = x['identifier'], x['relation'].lower()
            if key in old:
                out.append(copy.deepcopy(old[key]))
            else:
                y = {'identifier': x['identifier'], 'scheme': x['scheme'],
                     'relation_type': {'id': x['relation'].lower()}}
                if x.get('resource_type'):
                    y['resource_type'] = {'id': x['resource_type']}
                out.append(y)
        if set(old) - {(x['identifier'], x['relation_type']['id']) for x in out}:
            raise ValueError('Existing native related identifier removed')
        md['related_identifiers'] = out
    if 'upload_type' in patch or 'publication_type' in patch:
        if patch.get('upload_type') != 'publication' or patch.get('publication_type') != 'preprint':
            raise ValueError('Unrecognized reviewed resource classification change')
        md['resource_type'] = {'id': 'publication-preprint'}
    return md


def audit_preview_repair(rid, dest, before, after, patch_hash, result, check):
    """Bind and independently verify an existing-record preview restoration.

    The only writable file fields must equal the original display settings.
    Raw draft differences are precisely original OAI/generated links omitted,
    and, before restoration only, an original selected preview lost to None.
    """
    paths = {name: dest / (name + '.json') for name in ('preview_repair_pre', 'preview_repair_post')}
    if not any(path.exists() for path in paths.values()):
        return False
    errors_before = len(result['errors'])
    check('preview_repair_both_raw_receipts_present', all(path.exists() for path in paths.values()))
    if not all(path.exists() for path in paths.values()):
        return False
    data = {}
    for name, path in paths.items():
        result['receipt_sha256'][name] = sha(path)
        data[name] = read(path)
        check(name + '_record_and_frozen_patch', data[name].get('id') == rid
              and data[name].get('patch_sha256') == patch_hash)
        check(name + '_no_automatic_mutation_retry', data[name].get('automatic_mutation_retry') is False)
    pre, post = data['preview_repair_pre'], data['preview_repair_post']
    check('preview_repair_phases', pre.get('phase') == 'repair_requested' and post.get('phase') == 'preview_restored')
    session = pre['session']
    writable_original = {k: v for k, v in before['metadata'].items() if k not in {'prereserve_doi', 'relations'}}
    patch = read(HERE / 'patches' / f'{rid}.json')['metadata']
    check('preview_repair_owned_exact_reviewed_session', session.get('id') == rid
          and session.get('environment') == 'production'
          and session.get('phase') in {'update_requested', 'staged'}
          and session.get('original_metadata') == writable_original
          and session.get('target_metadata') == {**writable_original, **patch}
          and session.get('patch_fields') == list(patch)
          and session.get('native_original') == before['native']
          and session.get('files') == before['files'] and session.get('doi') == before['doi'])
    original_files = before['native_files']
    display = {k: copy.deepcopy(original_files[k]) for k in ('enabled', 'default_preview', 'order')}
    check('preview_repair_original_preview_is_existing_file', isinstance(display['default_preview'], str)
          and display['default_preview'] in original_files['entries'])
    payload = pre['payload']
    check('preview_repair_payload_only_original_display_and_reviewed_metadata',
          set(payload) == {'metadata', 'custom_fields', 'files'}
          and payload.get('files') == display
          and payload.get('metadata') == pre['draft']['metadata'] == after['native']['metadata']
          and payload.get('custom_fields') == before['native']['custom_fields'])
    public = pre['public']
    check('preview_repair_pre_public_original_exact', str(public.get('id')) == str(rid)
          and public.get('is_published') is True and public.get('is_draft') is False
          and public['files'] == original_files
          and all(public[k] == before['native'][k] for k in ('metadata', 'pids', 'access', 'custom_fields'))
          and public['parent']['id'] == before['identity']['parent_id']
          and public['parent']['pids'] == before['identity']['parent_pids']
          and public['versions'] == before['identity']['versions'])
    draft_pids = {k: v for k, v in before['native']['pids'].items() if k != 'oai'}
    for label, record in [('pre', pre), ('post', post)]:
        raw = record['draft']
        check('preview_repair_' + label + '_raw_draft_identity_exact', str(raw.get('id')) == str(rid)
              and raw.get('is_draft') is True and raw.get('is_published') is True
              and raw['pids'] == draft_pids
              and raw['parent']['id'] == before['identity']['parent_id']
              and raw['parent']['pids'] == before['identity']['parent_pids']
              and raw['versions'] == before['identity']['versions'])
        check('preview_repair_' + label + '_raw_draft_metadata_access_custom_exact',
              raw['metadata'] == after['native']['metadata']
              and raw['access'] == before['native']['access']
              and raw['custom_fields'] == before['native']['custom_fields'])
        restored = copy.deepcopy(raw['files'])
        for name, file in restored['entries'].items():
            if 'links' not in file and name in original_files['entries']:
                file['links'] = copy.deepcopy(original_files['entries'][name]['links'])
        if label == 'pre':
            check('preview_repair_pre_only_selected_preview_missing', restored.get('default_preview') is None)
            restored['default_preview'] = display['default_preview']
        check('preview_repair_' + label + '_full_files_exact_after_precise_draft_omissions', restored == original_files)
    return len(result['errors']) == errors_before


def audit_one(entry, inventory, catalog, baseline_hashes=None):
    rid = entry['id']
    dest = HERE / 'receipts' / str(rid)
    patch_path = HERE / 'patches' / f'{rid}.json'
    before_path = dest / 'before.json'
    after_path = dest / 'after.json'
    result = {'id': rid, 'title': entry['title'], 'status': 'pending', 'checks': {},
              'errors': [], 'allowed_normalizations': [], 'receipt_sha256': {},
              'patch_sha256': None}

    def check(name, passed, detail=None):
        result['checks'][name] = bool(passed)
        if not passed:
            result['errors'].append({'check': name, 'detail': detail})

    try:
        p = read(patch_path)
        patch = p['metadata']
        result['patch_sha256'] = sha(patch_path)
        check('frozen_patch_hash', result['patch_sha256'] == entry['patch_sha256'])
        check('frozen_patch_fields', list(patch) == entry['patch_fields'])
        check('only_approved_patch_fields', not (set(patch) - ALLOWED_PATCH_FIELDS)
              and not (set(patch) & PROTECTED_PATCH_FIELDS) and set(p) == {'metadata'})
        review = HERE / entry['independent_content_review']
        check('independent_content_review_exists', review.exists())
        if review.exists():
            result['content_review_sha256'] = sha(review)
        check('catalog_is_paper', catalog.get(rid, {}).get('status') == 'paper')
        before = read(before_path)
        result['receipt_sha256']['before'] = sha(before_path)
        if baseline_hashes is not None:
            check('frozen_original_baseline_hash', result['receipt_sha256']['before'] ==
                  baseline_hashes.get(str(rid), {}).get('sha256'))
        check('original_published_state', before['id'] == rid and before['submitted'] is True
              and before['state'] == 'done')
        old_inventory = inventory[rid]
        check('baseline_matches_original_inventory_identity', before['doi'] == old_inventory['doi']
              and str(before['conceptrecid']) == str(old_inventory['conceptrecid'])
              and before['identity']['id'] == str(rid)
              and before['identity']['parent_id'] == str(old_inventory['conceptrecid'])
              and before['identity']['pids']['doi']['identifier'] == old_inventory['doi']
              and before['identity']['parent_pids']['doi']['identifier'] ==
                  '10.5281/zenodo.' + str(old_inventory['conceptrecid']))
        check('baseline_matches_original_inventory_metadata', before['metadata'] == old_inventory['metadata'],
              diffs(old_inventory['metadata'], before['metadata']))
        if rid == 21699069 and not old_inventory.get('files'):
            # This identified pre-existing pending legacy edit projected away
            # public file entries in the initial inventory. Bind to the raw
            # published native snapshot taken before the authorized discard.
            # Do not apply this exception to any other record or shape.
            public_path = dest / 'native_public_before_discard.json'
            public = read(public_path)
            result['receipt_sha256']['native_public_before_discard'] = sha(public_path)
            check('extra_original_public_snapshot_published', public['id'] == str(rid)
                  and public['is_published'] is True and public['is_draft'] is False)
            check('extra_baseline_matches_pre_discard_public_files', before['files'] == native_files_projection(public['files'])
                  and before['native_files'] == public['files'])
            check('extra_baseline_matches_pre_discard_public_native', all(before['native'][k] == public[k]
                  for k in ('metadata','pids','access','custom_fields')))
            check('extra_baseline_matches_pre_discard_public_identity', before['identity']['parent_id'] == public['parent']['id']
                  and before['identity']['parent_pids'] == public['parent']['pids']
                  and before['identity']['versions'] == public['versions'])
            result['allowed_normalizations'].append({'field':'inventory.files',
                'kind':'identified_21699069_pending_legacy_projection_bound_to_original_native_public_snapshot'})
        else:
            check('baseline_matches_original_inventory_files', before['files'] == legacy_files(old_inventory))
        if 'language' in patch:
            check('language_only_when_missing', not before['metadata'].get('language')
                  and not before['native']['metadata'].get('languages') and patch['language'] == 'eng')
        for original_file in before['files']:
            check('valid_file_' + original_file['name'], isinstance(original_file['size'], int)
                  and original_file['size'] >= 0 and bool(re.fullmatch('[0-9a-f]{32}', original_file['md5'])))
        for src in catalog[rid].get('sources', []):
            match = next((x for x in before['files'] if x['name'] == src['filename']), None)
            check('deposited_source_' + src['filename'], match is not None
                  and match['md5'] == src['md5'] and match['size'] == src['size'])
        if not after_path.exists():
            result['status'] = 'fail' if result['errors'] else 'pending'
            return result
        after = read(after_path)
        result['receipt_sha256']['after'] = sha(after_path)
        check('final_published_state', after['id'] == rid and after['submitted'] is True and after['state'] == 'done')
        check('full_identity_exact', before['identity'] == after['identity'], diffs(before['identity'], after['identity']))
        for side, record in [('before', before), ('after', after)]:
            ident = record['identity']
            check(side + '_full_version_list_valid', ident['version_count'] == len(ident['version_ids'])
                  == len(set(ident['version_ids'])) and str(rid) in ident['version_ids']
                  and ident['version_count'] >= 1)
            check(side + '_public_native_identity_consistent', str(record['id']) == ident['id']
                  and record['native']['pids'] == ident['pids']
                  and record['doi'] == ident['pids']['doi']['identifier']
                  and record['metadata']['doi'] == record['doi']
                  and str(record['conceptrecid']) == ident['parent_id'])
            check(side + '_required_public_oai_identity', record['native']['pids'].get('oai') ==
                  {'identifier': f'oai:zenodo.org:{rid}', 'provider': 'oai'})
            check(side + '_native_file_manifest_matches_legacy', native_files_projection(record['native_files']) == record['files'])
            nf = record['native_files']
            check(side + '_native_file_totals_valid', nf['count'] == len(nf['entries'])
                  and nf['total_bytes'] == sum(x['size'] for x in nf['entries'].values()))
            for name, file in nf['entries'].items():
                for link, suffix in [('self',''), ('content','/content')]:
                    url = urlsplit(file.get('links', {}).get(link, ''))
                    check(side + '_public_file_' + link + '_' + name,
                          url.scheme == 'https' and url.hostname == 'zenodo.org'
                          and unquote(url.path) == f'/api/records/{rid}/files/{name}{suffix}'
                          and not url.query and not url.fragment)
        for field in ('doi', 'conceptrecid', 'files', 'native_files'):
            check('preserved_' + field, before[field] == after[field], diffs(before[field], after[field], field))
        for field in ('pids', 'access', 'custom_fields'):
            check('preserved_native_' + field, before['native'][field] == after['native'][field],
                  diffs(before['native'][field], after['native'][field], 'native.' + field))
        for field in PROTECTED_PATCH_FIELDS:
            check('preserved_metadata_' + field, before['metadata'].get(field) == after['metadata'].get(field))
        expected, notes = legacy_compare(before['metadata'], after['metadata'], patch)
        result['allowed_normalizations'].extend(notes)
        check('complete_legacy_metadata_matches_frozen_target', expected == after['metadata'],
              diffs(expected, after['metadata'], 'metadata'))
        bmd, amd = before['native']['metadata'], after['native']['metadata']
        changed = {NATIVE_FIELDS[k] for k in patch}
        unpatched_before = {k: v for k, v in bmd.items() if k not in changed}
        unpatched_after = {k: v for k, v in amd.items() if k not in changed}
        check('all_unpatched_native_metadata_exact', unpatched_before == unpatched_after,
              diffs(unpatched_before, unpatched_after, 'native.metadata'))
        native_expected = expected_native(bmd, patch, rid)
        for field in changed:
            wanted, actual = native_expected.get(field), amd.get(field)
            if field in {'languages', 'resource_type', 'related_identifiers', 'additional_descriptions'}:
                good = vocab_ids(wanted) == vocab_ids(actual)
            else:
                good = wanted == actual
            check('intended_native_' + field, good, diffs(vocab_ids(wanted), vocab_ids(actual), field))
        # Existing relation objects must survive exactly, including controlled
        # attributes and labels, even when a larger relation list is intended.
        for original in bmd.get('related_identifiers', []):
            check('native_existing_relation_' + original['identifier'], original in amd.get('related_identifiers', []))
        if 'notes' in patch:
            old_extra = [x for x in bmd.get('additional_descriptions', []) if x.get('type', {}).get('id') != 'notes']
            new_extra = [x for x in amd.get('additional_descriptions', []) if x.get('type', {}).get('id') != 'notes']
            check('unpatched_additional_descriptions_exact', old_extra == new_extra)
        if 'description' not in patch:
            check('scientific_scope_description_exact', bmd.get('description') == amd.get('description'))
        else:
            check('scientific_scope_description_frozen_reviewed_target', amd.get('description') == patch['description'])
        check('receipt_claim_matches_patch_hash', after.get('verification', {}).get('reviewed_patch_sha256') == entry['patch_sha256'])
        preview_repair_valid = audit_preview_repair(rid, dest, before, after, entry['patch_sha256'], result, check)
        for item in after.get('verification', {}).get('mutation_routes', []):
            base = f'/api/deposit/depositions/{rid}'
            routes = {('POST', base + '/actions/edit'), ('PUT', base), ('POST', base + '/actions/publish')}
            if preview_repair_valid:
                routes.add(('PUT', f'/api/records/{rid}/draft'))
            check('record_bound_mutation_route_' + item['method'] + '_' + item['path'],
                  (item['method'], item['path']) in routes)
        for name in ('stage.json', 'publish.json', 'native_staged.json', 'native_published.json'):
            path = dest / name
            if not path.exists():
                continue
            result['receipt_sha256'][name.removesuffix('.json')] = sha(path)
            rec = read(path)
            check(name + '_same_record', str(rec['id']) == str(rid))
            if name == 'native_published.json':
                check('full_native_public_record_published', rec.get('is_published') is True and rec.get('is_draft') is False)
                check('full_native_public_record_metadata_matches_receipt', rec['metadata'] == amd)
                check('full_native_public_record_files_exact', rec['files'] == before['native_files'])
                check('full_native_public_record_pids_exact', rec['pids'] == before['native']['pids'])
                check('full_native_public_record_access_exact', rec['access'] == before['native']['access'])
                check('full_native_public_record_custom_fields_exact', rec['custom_fields'] == before['native']['custom_fields'])
                check('full_native_public_record_parent_pids_exact', rec['parent']['pids'] == before['identity']['parent_pids'])
                check('full_native_public_record_parent_id_exact', rec['parent']['id'] == before['identity']['parent_id'])
                check('full_native_public_record_versions_exact', rec['versions'] == before['identity']['versions'])
        result['legacy_metadata_changed_fields'] = sorted(k for k in set(before['metadata']) | set(after['metadata'])
                                                         if before['metadata'].get(k) != after['metadata'].get(k))
        result['native_metadata_changed_fields'] = sorted(k for k in set(bmd) | set(amd) if bmd.get(k) != amd.get(k))
        result['doi'] = after['doi']
        result['concept_doi'] = after['identity']['parent_pids'].get('doi', {}).get('identifier')
        result['version_ids'] = after['identity']['version_ids']
        result['version_count'] = after['identity']['version_count']
        result['legacy_compatible'] = before['legacy_compatible']
        result['route'] = ('native-preserving' if before['legacy_compatible'] else 'native-rich') \
            if (dest / 'native_published.json').exists() else ('legacy-with-preview-restoration' if preview_repair_valid else 'legacy')
        result['status'] = 'fail' if result['errors'] else 'pass'
    except Exception as exc:
        result['errors'].append({'check': 'audit_exception', 'detail': f'{type(exc).__name__}: {exc}'})
        result['status'] = 'fail'
    return result


def first_record_check():
    dest = HERE / 'receipts/23271172'
    if not (dest / 'after.json').exists():
        return {'status': 'pending'}
    before, after = read(dest / 'before.json'), read(dest / 'after.json')
    raw = read(dest / 'first_staging_guard_stop.json')
    comp = read(HERE / 'reviews/FILES_DRAFT_REPRESENTATION_COMPARISON.json')
    bpids = before['native']['pids']
    expected_draft = {k: v for k, v in bpids.items() if k != 'oai'}
    restored_files = copy.deepcopy(comp['draft_files'])
    omitted = []
    for name, entry in restored_files['entries'].items():
        if 'links' not in entry:
            entry['links'] = copy.deepcopy(before['native_files']['entries'][name]['links'])
            omitted.append(name)
    checks = {
        'raw_staged_only_original_oai_omitted': raw['native_staged']['pids'] == expected_draft,
        'exact_original_public_oai_restored': after['native']['pids'] == bpids,
        'raw_draft_files_only_generated_links_omitted': restored_files == before['native_files'],
        'original_public_files_match_observed_prepublication_public': comp['public_files'] == before['native_files'],
        'full_original_public_file_settings_entries_links_restored': after['native_files'] == before['native_files'],
        'only_intended_legacy_fields_changed': sorted(k for k in set(before['metadata']) | set(after['metadata'])
                                                     if before['metadata'].get(k) != after['metadata'].get(k)) == ['keywords', 'language'],
    }
    return {'id': 23271172, 'status': 'pass' if all(checks.values()) else 'fail', 'checks': checks,
            'original_public_oai': bpids.get('oai'), 'raw_draft_missing_file_links': omitted,
            'evidence_sha256': {'first_staging_guard_stop': sha(dest / 'first_staging_guard_stop.json'),
                                'draft_file_comparison': sha(HERE / 'reviews/FILES_DRAFT_REPRESENTATION_COMPARISON.json')}}


def write_reports(result):
    dest = HERE / 'reviews'
    json_path = dest / 'FINAL_RECEIPT_AUDIT.json'
    md_path = dest / 'FINAL_RECEIPT_AUDIT.md'
    summary = [
        '# Independent receipt audit', '',
        f"Checkpoint: {result['generated_utc']}. Verified {result['completed_count']}/{result['approved_count']} completed public receipts; "
        f"{len(result['pending_ids'])} pending and {len(result['failed_ids'])} failed. Completion estimate for the final receipt audit: "
        f"{round(100 * result['completed_count'] / max(1,result['approved_count']))}%. Overall audit status: **{result['status']}**.", '',
        'This independent audit reads local receipts, the original inventory/catalog and frozen approved proposal hashes. It uses no Zenodo/client imports, credentials, network operations, Git actions or patch writes. It validates public record/deposition state, full DOI/OAI PIDs, parent concept PIDs, complete version identities/count, full file entry/settings/link dictionaries, checksums/sizes, original inventory/source correspondence, access/custom fields and all unpatched native metadata. Changed native fields are independently reconstructed from the frozen scholarly proposal, while controlled-vocabulary display titles are ignored only inside intentionally changed vocabulary fields. Existing native relation objects and author identifiers, affiliations, roles and other structure remain protected exactly. The sole source-reviewed name-order correction on 22770864 changes only the reversed given/family/name fields; other creator changes only add the reviewed missing ORCID. Description preservation or exact reviewed-description equality binds the scientific scope to the content reviews.', '',
        'Four existing metadata drafts required restoration of an original selected preview that the legacy endpoint omitted. The audit hashes both raw preview-repair receipts and independently checks the exact original public snapshot, owned reviewed session, intended metadata, draft identity, full file dictionaries and payload. Only original writable display options accompany reviewed metadata/custom fields in the exact same-record draft PUT; PIDs, access, file entries/uploads and unreviewed metadata are forbidden. All final public file settings must equal the original exactly.', '',
        'The local snapshots represent the recorded authenticated public read-backs. This audit does not perform a new live query, download file bytes, re-certify the scientific proofs or close manuscript priority/access gaps. Pending receipts never count as completed.', '',
        'The separate original-baseline hash manifest is append-only for newly approved records. It freezes the unchanged recorded public snapshots when this independent audit is installed and prevents later coherent edits to both before/after receipts from escaping detection. Earlier native snapshot authenticity remains grounded in the recorded API provenance and inventory/native cross-checks, rather than a claim that local hashes retroactively authenticate an API response.', '',
        f"Falsification controls: {result.get('falsification_controls', {}).get('count', 0)} controls; "
        f"all passed={result.get('falsification_controls', {}).get('all_passed', False)}; "
        f"bound to current audit-tool bytes={result.get('falsification_controls', {}).get('same_audit_tool', False)}. "
        'Cloned-data mutants test DOI/concept/version/OAI/file-link/file-access/affiliation/scope/tag/language/patch alteration while optimistic receipt booleans remain true, plus unauthorized creator renames, identifier/affiliation/role loss and unsafe or wrong-record preview-restoration evidence.', '',
        '## First-record draft/public representation check', '',
        f"Record 23271172: **{result['first_record_representation']['status']}**. The raw first guard-stop snapshot contains precisely the original DOI PID with the original OAI PID omitted in the draft. The separate raw file comparison contains precisely omitted generated per-file links. The completed public receipt must restore the full original OAI/DOI dictionary and the full original file dictionary, including those links; no public-boundary normalization is allowed. Only keywords/language change.", '',
        '## Completed receipts', '',
        '| Record | Route | Status | Record DOI | Concept DOI | Full version IDs | Changed legacy fields |',
        '|---|---|---|---|---|---|---|',
    ]
    for r in result['records']:
        if r['status'] == 'pending':
            continue
        summary.append(f"| {r['id']} | {r.get('route','—')} | {r['status']} | {r.get('doi','—')} | "
                       f"{r.get('concept_doi','—')} | {', '.join(r.get('version_ids',[]))} | "
                       f"{', '.join(r.get('legacy_metadata_changed_fields',[]))} |")
    summary += ['', '## Pending and failures', '',
                'Pending IDs: ' + ', '.join(map(str, result['pending_ids'])) + '.', '',
                'The JSON companion contains every individual check, exact exception paths, receipt/source-review SHA-256 values, frozen patch hashes and full version counts.']
    for r in result['records']:
        if r['errors']:
            summary += ['', f"Record {r['id']}: `{json.dumps(r['errors'], ensure_ascii=False)}`"]
    for path, value in [(json_path, json.dumps(result, indent=2, ensure_ascii=False) + '\n'),
                        (md_path, '\n'.join(summary) + '\n')]:
        temp = path.with_suffix(path.suffix + '.tmp')
        temp.write_text(value)
        temp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    approved = read(HERE / 'APPROVED_PROPOSALS.json')
    inventory = {x['id']: x for x in read(HERE / 'INVENTORY.json')['records']}
    catalog = {x['id']: x for x in read(HERE / 'SOURCE_CATALOG.json')}
    scope_evidence = HERE / 'reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json'
    if scope_evidence.exists():
        # Keep original inventory entries immutable; augment only records that
        # the independent all_versions=true read discovered were missing.
        scope = read(scope_evidence)
        for original in scope['new_since_inventory_or_previous_versions']:
            inventory.setdefault(original['id'], original)
    baseline_path = HERE / 'reviews/ORIGINAL_BASELINE_HASHES.json'
    baseline_manifest = read(baseline_path) if baseline_path.exists() else {
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'records': {}}
    additions = False
    for entry in approved['records']:
        rid = str(entry['id'])
        path = HERE / 'receipts' / rid / 'before.json'
        if path.exists() and rid not in baseline_manifest['records']:
            baseline_manifest['records'][rid] = {'sha256':sha(path),
                'initial_freeze_utc':datetime.now(timezone.utc).isoformat()}
            additions = True
    if additions:
        temp = baseline_path.with_suffix('.json.tmp')
        temp.write_text(json.dumps(baseline_manifest, indent=2) + '\n')
        temp.replace(baseline_path)
    records = [audit_one(x, inventory, catalog, baseline_manifest['records']) for x in approved['records']]
    first = first_record_check()
    pending = [x['id'] for x in records if x['status'] == 'pending']
    failed = [x['id'] for x in records if x['status'] == 'fail']
    completed = sum(x['status'] == 'pass' for x in records)
    status = 'fail' if failed or first['status'] == 'fail' else ('pending' if pending else 'pass')
    result = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'status': status,
              'approved_count': len(approved['records']), 'completed_count': completed,
              'pending_ids': pending, 'failed_ids': failed,
              'approved_manifest_sha256': sha(HERE / 'APPROVED_PROPOSALS.json'),
              'audit_tool_sha256': sha(Path(__file__)),
              'original_baseline_manifest_sha256': sha(baseline_path),
              'inventory_sha256': sha(HERE / 'INVENTORY.json'),
              'source_catalog_sha256': sha(HERE / 'SOURCE_CATALOG.json'),
              'first_record_representation': first, 'records': records}
    if scope_evidence.exists():
        result['all_versions_scope_evidence_sha256'] = sha(scope_evidence)
    controls_path = HERE / 'reviews/FINAL_RECEIPT_AUDIT_CONTROLS.json'
    if controls_path.exists():
        controls = read(controls_path)
        result['falsification_controls'] = {
            'sha256': sha(controls_path), 'count': len(controls['controls']),
            'all_passed': controls['all_passed'],
            'same_audit_tool': controls.get('audit_tool_sha256') == result['audit_tool_sha256'],
        }
        if controls.get('audit_tool_sha256') == result['audit_tool_sha256'] and not controls['all_passed']:
            result['status'] = 'fail'
            result['audit_errors'] = ['Current falsification controls did not all pass']
        elif controls.get('audit_tool_sha256') != result['audit_tool_sha256'] and result['status'] == 'pass':
            result['status'] = 'pending'
            result['audit_errors'] = ['Falsification controls are not bound to current audit tool; rerun controls']
    elif result['status'] == 'pass':
        result['status'] = 'pending'
        result['audit_errors'] = ['Falsification controls artifact is absent']
    status = result['status']
    write_reports(result)
    print(json.dumps({k: result[k] for k in ('status','approved_count','completed_count','pending_ids','failed_ids')}, indent=2))
    if status == 'fail' or (args.require_complete and status != 'pass'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
