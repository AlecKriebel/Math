"""Read the actual public record and hash both published downloads."""
from pathlib import Path
import datetime, hashlib, json, urllib.parse, urllib.request

A = Path(__file__).resolve().parent
UA = 'Math-PR170-Published-Package-Verification/1.0'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def get(url, limit):
    parts = urllib.parse.urlsplit(url)
    require(parts.scheme == 'https' and parts.hostname == 'zenodo.org', 'Unexpected public download host')
    request = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(limit + 1)
        require(len(data) <= limit, 'Public response exceeded bound')
        require(urllib.parse.urlsplit(response.url).hostname == 'zenodo.org', 'Unexpected response host')
        return data

def main():
    pub = json.loads((A / 'ZENODO_PUBLICATION_READBACK.json').read_text())
    gate = json.loads((A / 'ROOT_PUBLICATION_GATE.json').read_text())
    require(pub['state'] == 'published' and pub['title'] == gate['title'], 'Actual accepted publication required')
    private = A / 'private/published_downloads'
    private.mkdir(parents=True,exist_ok=True)
    raw = get('https://zenodo.org/api/records/' + str(pub['id']), 1500000)
    record = json.loads(raw)
    require(record['id'] == pub['id'] and record['doi'] == pub['doi'] and record['metadata']['title'] == pub['title'], 'Public record identity differs')
    (private / 'PUBLIC_RECORD.json').write_bytes(raw)
    remote_files = {item['key']: item for item in record['files']}
    require(set(remote_files) == set(gate['upload_files']), 'Actual public file inventory differs')
    pins = {}
    for name in gate['upload_files']:
        item = remote_files[name]
        link = item['links'].get('self') or item['links'].get('content')
        require(link, 'Public content link absent')
        data = get(link, gate['files'][name]['bytes'] + 1024)
        require(len(data) == gate['files'][name]['bytes'] and hashlib.sha256(data).hexdigest() == gate['files'][name]['sha256'], 'Actual published bytes differ: ' + name)
        md5 = hashlib.md5(data).hexdigest()
        require(item['checksum'].removeprefix('md5:') == md5, 'Public checksum differs')
        (private / name).write_bytes(data)
        pins[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'md5': md5, 'public_content_url': link}
    receipt = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'PUBLIC_RECORD_AND_BOTH_ACTUAL_DOWNLOAD_BYTES_ACCEPTED', 'PR': 170, 'record_id': pub['id'], 'DOI': pub['doi'], 'title': pub['title'], 'public_record_sha256': hashlib.sha256(raw).hexdigest(), 'files': pins, 'frozen_reviewed_candidate_bytes_match': True, 'metadata_exact_verification': 'Repository kit separately authenticated exact intended metadata with only its narrow declared representation allowances.'}
    (A / 'ZENODO_PUBLIC_DOWNLOAD_ACCEPTANCE.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
