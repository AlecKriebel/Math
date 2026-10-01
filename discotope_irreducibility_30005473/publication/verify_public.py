#!/usr/bin/env python3
"""Unauthenticated public-record/file verification against the frozen manifest."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RECORD_ID = 23074543
UA = 'Math-PR-Audit-Public-Verification/1.0'


def fetch(url, limit):
    parsed = urlsplit(url)
    assert parsed.scheme == 'https' and parsed.hostname == 'zenodo.org'
    request = Request(url, headers={'User-Agent': UA})
    # No token, authorization header, or authenticated client is used.
    with urlopen(request, timeout=30) as response:
        assert response.status == 200
        data = response.read(limit + 1)
        assert len(data) <= limit
        return data


def main():
    manifest = json.loads((ROOT / 'zenodo-deposit.json').read_text())
    published = json.loads((ROOT / 'publication/publish.json').read_text())
    assert published['state'] == 'published' and published['id'] == RECORD_ID
    record = json.loads(fetch(f'https://zenodo.org/api/records/{RECORD_ID}', 2_000_000))
    assert record['id'] == RECORD_ID and record['doi'] == published['doi']
    assert record['metadata']['title'] == manifest['metadata']['title']
    files = {entry['key']: entry for entry in record['files']}
    assert len(files) == len(record['files']) == len(manifest['files']) == 2
    assert set(files) == {entry['name'] for entry in manifest['files']}
    evidence = []
    for entry in manifest['files']:
        local = (ROOT / entry['path']).read_bytes()
        remote_entry = files[entry['name']]
        assert remote_entry['size'] == len(local)
        url = remote_entry['links']['self']
        remote = fetch(url, len(local))
        assert remote == local
        evidence.append({'name': entry['name'], 'public_url': url,
                         'size': len(remote),
                         'sha256': hashlib.sha256(remote).hexdigest(),
                         'bytes_equal_frozen_local_file': True})
    receipts = ROOT / 'publication'
    (receipts / 'public_record.json').write_text(json.dumps(record, indent=2) + '\n')
    result = {'checked_utc': datetime.now(timezone.utc).isoformat(),
              'state': 'public_record_and_downloads_verified',
              'record_url': published['record_url'], 'doi_url': published['doi_url'],
              'authentication_used': False, 'files': evidence}
    (receipts / 'public_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
