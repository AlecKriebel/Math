#!/usr/bin/env python3
"""Hash the already identified six sources in memory; never save their bytes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]


def check(source):
    requested = source['url']
    req = urllib.request.Request(requested, headers={'User-Agent': 'Independent-source-hash-verification/1.0'})
    with urllib.request.urlopen(req, timeout=40) as response:
        data = response.read()
        result = {'key': source['key'], 'requested_url': requested, 'resolved_url': response.url, 'http_status': response.status, 'content_type': response.headers.get('Content-Type'), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'expected_bytes': source['bytes'], 'expected_sha256': source['sha256'], 'pdf_magic': data.startswith(b'%PDF-'), 'utc': datetime.now(timezone.utc).isoformat(), 'raw_bytes_written': False}
    result['matches_previous_fresh_review'] = result['bytes'] == source['bytes'] and result['sha256'] == source['sha256'] and result['pdf_magic']
    if not result['matches_previous_fresh_review']:
        raise RuntimeError('Source byte identity changed: ' + source['key'])
    return result


sources = json.loads((AUDIT / 'reviews/full_package_02/evidence/fresh_source_hashes.json').read_text())
with ThreadPoolExecutor(max_workers=6) as pool:
    checks = list(pool.map(check, sources))
result = {'schema_version': 1, 'utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Byte identity refresh of already identified source URLs only; no new mathematical or literature review', 'source_count': len(checks), 'all_source_hashes_unchanged': all(s['matches_previous_fresh_review'] for s in checks), 'source_redistribution': False, 'sources': checks}
(HERE / 'evidence/fresh_source_hashes.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'source_count': len(checks), 'all_hashes_unchanged': result['all_source_hashes_unchanged'], 'raw_bytes_written': False}))
