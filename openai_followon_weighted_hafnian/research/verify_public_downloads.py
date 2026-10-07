"""Verify an already published record and its public payload, without credentials."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def get(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'zenodo.org':
        raise ValueError('Expected a public production Zenodo HTTPS URL')
    return urllib.request.urlopen(urllib.request.Request(
        url, headers={'User-Agent': 'Math-Zenodo-Public-Verification/1.0'}), timeout=60)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record-id', required=True, type=int)
    parser.add_argument('--doi', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'zenodo-deposit.json').read_text())
    identity = json.loads((ROOT / 'publication/CANDIDATE_IDENTITY.json').read_text())
    wanted = manifest['metadata']
    with get(f'https://zenodo.org/api/records/{args.record_id}') as response:
        record = json.load(response)
    assert record['id'] == args.record_id
    assert record['doi'] == args.doi
    metadata = record['metadata']
    assert metadata['title'] == wanted['title']
    assert metadata['publication_date'] == wanted['publication_date']
    assert len(metadata['creators']) == len(wanted['creators'])
    for remote, local in zip(metadata['creators'], wanted['creators']):
        assert remote['name'] == local['name']
        assert remote['orcid'] == local['orcid']
    remote_files = {file['key']: file for file in record['files']}
    local_files = {Path(file['path']).name: file['path'] for file in manifest['files']}
    assert set(remote_files) == set(local_files)
    checked = []
    for name, relative in local_files.items():
        local_bytes = (ROOT / relative).read_bytes()
        local_sha = hashlib.sha256(local_bytes).hexdigest()
        assert local_sha == identity['files'][relative]['sha256']
        remote = remote_files[name]
        assert remote['size'] == len(local_bytes)
        assert remote['checksum'] == 'md5:' + hashlib.md5(local_bytes).hexdigest()
        sha, md5, size = hashlib.sha256(), hashlib.md5(), 0
        download = remote['links']['self']
        with get(download) as response:
            while chunk := response.read(1024 * 1024):
                sha.update(chunk)
                md5.update(chunk)
                size += len(chunk)
        assert size == len(local_bytes)
        assert sha.hexdigest() == local_sha
        assert 'md5:' + md5.hexdigest() == remote['checksum']
        checked.append({'name': name, 'bytes': size, 'sha256': sha.hexdigest(),
                        'md5': md5.hexdigest(), 'download_url': download})
    receipt = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'record_id': args.record_id, 'doi': args.doi,
               'record_url': f'https://zenodo.org/records/{args.record_id}',
               'public_api_url': f'https://zenodo.org/api/records/{args.record_id}',
               'candidate': identity['candidate'], 'public_record_accessible': True,
               'title': metadata['title'], 'creators': metadata['creators'],
               'publication_date': metadata['publication_date'],
               'public_downloads_match_reviewed_bytes': True, 'files': checked,
               'scope': 'Unauthenticated public record and complete downloaded payload verification. Exact full deposition metadata is checked separately by the repository tool.'}
    Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
