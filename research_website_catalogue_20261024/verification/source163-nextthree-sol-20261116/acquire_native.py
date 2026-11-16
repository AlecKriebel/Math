"""Fixed3 published-deposit metadata/assets only; ordinary GETs, no retries or native execution."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import datetime
import hashlib
import json
import shutil
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
RECORDS = [23357329, 23203143, 23153134]


def pin(p):
    b = p.read_bytes()
    return {'path': p.name, 'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def fetch(source, label, url):
    parsed = urlparse(url)
    assert parsed.scheme == 'https' and parsed.hostname == 'zenodo.org' and parsed.username is None and parsed.password is None
    assert not (source / (label + '.transport.json')).exists()
    for ending in ['response.body', 'response.headers', 'curl.stdout.txt', 'curl.stderr.txt']:
        assert not (source / (label + '.' + ending)).exists()
    command = ['curl', '--disable', '--silent', '--show-error', '--request', 'GET', '--proto', '=https', '--connect-timeout', '15', '--max-time', '45', '--max-filesize', '104857600', '--dump-header', str(source / (label + '.response.headers')), '--output', str(source / (label + '.response.body')), '--write-out', '%{json}', url]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, cwd=source, capture_output=True)
    (source / (label + '.curl.stdout.txt')).write_bytes(result.stdout)
    (source / (label + '.curl.stderr.txt')).write_bytes(result.stderr)
    try:
        transport = json.loads(result.stdout)
    except ValueError:
        transport = {}
    receipt = {'UTC_start': start, 'UTC_end': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command': command, 'exit': result.returncode, 'curl_transport': transport, 'automatic_retries': 0, 'redirects_automatically_followed': False, 'stdout': label + '.curl.stdout.txt', 'stderr': label + '.curl.stderr.txt', 'headers': label + '.response.headers', 'body': label + '.response.body'}
    (source / (label + '.transport.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return result.returncode, transport, source / (label + '.response.body')


def logical_get(source, label, url):
    visited = set()
    for hop in range(4):
        assert url not in visited
        visited.add(url)
        name = label if hop == 0 else label + '.redirect-' + str(hop).zfill(2)
        code, transport, body = fetch(source, name, url)
        assert code == 0, 'ordinary transport failure retained: ' + name
        status = transport.get('http_code')
        if status in (301, 302, 303, 307, 308):
            url = transport.get('redirect_url')
            assert url, 'redirect without ordinary Location'
            continue
        assert status == 200, 'ordinary HTTP failure retained: ' + name + '/' + str(status)
        return body, {'label': label, 'response_label': name, 'redirect_hops': hop, 'effective_url': transport.get('url_effective'), 'body': pin(body)}
    raise ValueError('finite ordinary redirect limit reached')


def acquire(record):
    source = P / 'papers' / str(record) / 'sources'
    assert source.is_dir() and not (source / 'ACQUIRED.json').exists()
    original = json.loads((source / 'record.response.body').read_bytes())
    receipt = json.loads((source / 'record.transport.json').read_bytes())
    assert receipt['exit'] == 0 and receipt['curl_transport']['http_code'] == 200 and original['id'] == record
    assert original['status'] == 'published' and original['state'] == 'done'
    events, versions = [], []
    try:
        path, event = logical_get(source, 'files-' + str(record), original['links']['files'])
        events.append(event)
        files = json.loads(path.read_bytes())
        entries = files['entries']
        assert 1 <= len(original['files']) <= 24 and {x['key'] for x in entries} == {x['key'] for x in original['files']}
        by_name = {x['key']: x for x in entries}
        for item in original['files']:
            other = by_name[item['key']]
            assert item['size'] == other['size'] and item['checksum'] == other['checksum']
        path, event = logical_get(source, 'latest', original['links']['latest'])
        events.append(event)
        latest = json.loads(path.read_bytes())
        url = original['links']['versions']
        seen = set()
        for page in range(1, 11):
            assert url not in seen
            seen.add(url)
            path, event = logical_get(source, 'versions-' + str(page).zfill(3), url)
            events.append(event)
            version_page = json.loads(path.read_bytes())
            versions.extend(x['id'] for x in version_page['hits']['hits'])
            url = version_page.get('links', {}).get('next')
            if not url:
                break
        else:
            raise ValueError('finite version-pagination limit reached')
        assert record in versions
        assets = source / 'assets'
        assets.mkdir()
        acquired, folded = [], set()
        for index, item in enumerate(original['files'], 1):
            name = item['key']
            assert name not in ('', '.', '..') and '/' not in name and '\\' not in name and '\0' not in name and ':' not in name
            assert name.casefold() not in folded
            folded.add(name.casefold())
            asset_url = item['links']['self']
            assert urlparse(asset_url).path.startswith('/api/records/' + str(record) + '/files/') and urlparse(asset_url).path.endswith('/content')
            path, event = logical_get(source, 'asset-' + str(record) + '-' + str(index).zfill(3), asset_url)
            events.append(event)
            body = path.read_bytes()
            assert len(body) == item['size'] and item['checksum'].startswith('md5:') and hashlib.md5(body).hexdigest() == item['checksum'][4:], 'native size/MD5 mismatch retained'
            shutil.copyfile(path, assets / name)
            (assets / name).chmod(0o644)
            acquired.append({'native_position': index, 'name': name, 'source_url': asset_url, 'native_MD5': item['checksum'], 'actual_MD5': hashlib.md5(body).hexdigest(), 'asset': {'path': 'assets/' + name, 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}, 'response_label': event['response_label']})
        result = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'NATIVE_METADATA_AND_ASSETS_ACQUIRED_NOT_YET_SOURCE_SEALED', 'record': record, 'title': original['metadata']['title'], 'DOI': original['doi'], 'concept_DOI': original['conceptdoi'], 'metadata_version': original['metadata'].get('version'), 'publication_date': original['metadata']['publication_date'], 'created': original['created'], 'creators': original['metadata']['creators'], 'license': original['metadata']['license'], 'record_files_order': [x['key'] for x in original['files']], 'files_entries_order': [x['key'] for x in entries], 'files_custom_order': files.get('order'), 'default_preview': files.get('default_preview'), 'latest_record_id': latest['id'], 'fixed_record_is_latest': latest['id'] == record, 'version_record_ids': versions, 'assets': acquired, 'transport_events': events, 'automatic_retries': 0, 'native_or_archived_program_execution': False}
        (source / 'ACQUIRED.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        return {'record': record, 'status': result['status'], 'asset_count': len(acquired), 'latest_record': latest['id']}
    except Exception as error:
        failure = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'record': record, 'status': 'ACCESS_OR_IDENTITY_FAILURE_LITERAL_EVIDENCE_PRESERVED_NO_RETRY', 'error': repr(error), 'events_completed': events, 'automatic_retries': 0}
        (source / 'ACQUISITION_FAILURE.json').write_text(json.dumps(failure, indent=2) + '\n')
        return failure


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(acquire, RECORDS):
            print(json.dumps(result, ensure_ascii=False), flush=True)
