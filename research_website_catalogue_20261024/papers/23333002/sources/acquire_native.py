"""Source-only native metadata/assets acquisition; no manuscript/code reading."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from hashlib import sha256, new
import json, runpy

S = Path(__file__).resolve().parent
get = runpy.run_path(str(S / 'fetch_ordinary.py'), run_name='custody_import')['get']


def save(name, obj):
    with (S / name).open('x') as out:
        out.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def request(role, url, name, objects):
    rows, final = get(url, name)
    obj = json.loads(Path(final['body_path']).read_bytes())
    objects.append({'role': role, 'path': final['body_path'], 'bytes': final['body_bytes'],
                    'SHA256': final['body_SHA256']})
    return obj


def main():
    start = json.loads((S / 'START.json').read_bytes())
    rid = start['record_id']
    begun = datetime.now(timezone.utc).isoformat()
    objects = []
    try:
        record = request('record', 'https://zenodo.org/api/records/' + str(rid), 'record.response.body', objects)
        assert record['id'] == rid
        assert record.get('status') == 'published' or record.get('state') == 'done'
        latest = request('latest', record['links']['latest'], 'latest.response.body', objects)
        versions = []
        url = record['links']['versions']
        seen = set()
        for page in range(1, 21):
            assert url not in seen
            seen.add(url)
            obj = request('versions_page%03d' % page, url, 'versions-page%03d.response.body' % page, objects)
            versions.extend(obj['hits']['hits'])
            url = obj.get('links', {}).get('next')
            if not url:
                break
        else:
            raise RuntimeError('bounded version-page limit; no completeness claim')
        files = request('files', record['links']['files'], 'files.response.body', objects)
        entries = files['entries']
        pairs = list(entries.values()) if isinstance(entries, dict) else entries
        assert isinstance(pairs, list)
        assets = []
        for ordinal, item in enumerate(record['files']):
            matches = [x for x in pairs if x['key'] == item['key']]
            assert len(matches) == 1
            entry = matches[0]
            assert entry['size'] == item['size'] and entry['checksum'] == item['checksum']
            key = item['key']
            path = PurePosixPath(key)
            assert not path.is_absolute() and '..' not in path.parts and '\\' not in key and ':' not in key
            name = 'assets/' + key
            rows, final = get(item['links']['self'], name)
            body = Path(final['body_path']).read_bytes()
            algorithm, digest = item['checksum'].split(':', 1)
            assert len(body) == item['size'] and new(algorithm.lower(), body).hexdigest().lower() == digest.lower()
            assets.append({'ordinal_zero_based': ordinal, 'original_api_file_object': item,
                           'whole_original_native_files_entry': entry, 'path': final['body_path'],
                           'bytes': len(body), 'SHA256': sha256(body).hexdigest(),
                           'native_checksum_verified': True, 'acquisition_mechanism': 'ordinary_native_GET',
                           'cached_bytes_reused': False, 'fresh_native_asset_GET_claimed': True})
        save('ACQUIRED_NATIVE.json', {'started_UTC': begun, 'completed_UTC': datetime.now(timezone.utc).isoformat(),
             'record_id': rid, 'whole_native_API_objects': objects, 'all_assets_original_record_order': assets,
             'all_enumerated_version_ids': [x['id'] for x in versions], 'latest_record_id': latest['id'],
             'version_enumeration_exhaustive_no_next_link': True,
             'manuscript_text_preamble_code_results_opinions_read': False})
        print(json.dumps({'record_id': rid, 'status': 'ASSETS_AUTHENTICATED',
                          'title': record['metadata']['title'], 'version': record['metadata'].get('version'),
                          'publication_date': record['metadata']['publication_date'],
                          'created': record['created'], 'latest_record_id': latest['id'],
                          'version_ids': [x['id'] for x in versions], 'assets': assets}, indent=2))
    except Exception as error:
        save('ACQUISITION_STOP.json', {'started_UTC': begun, 'completed_UTC': datetime.now(timezone.utc).isoformat(),
             'record_id': rid, 'status': 'INCOMPLETE', 'exception_type': type(error).__name__,
             'exception': str(error), 'further_network_stopped': True, 'no_retries_or_bypass': True,
             'no_SOURCE_READY_claim': True, 'completed_native_objects_before_stop': objects,
             'source_programmes_executed': [], 'manuscript_or_preamble_read': False})
        print(json.dumps({'record_id': rid, 'status': 'INCOMPLETE', 'reason': str(error)}, indent=2))


if __name__ == '__main__':
    main()
