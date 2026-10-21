#!/usr/bin/env python3
"""Verify recorded local custody; does not certify historical byte availability."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIVATE = Path('/Users/alec/.cache/pr66_exact_target_priority_20261004')

def digest(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()

def verify(path, size, sha):
    assert digest(path) == (size, sha), str(path)

seal = json.loads((ROOT / 'FIRST_CONCLUSION_SEAL.json').read_text())
verify(Path(seal['path']), seal['bytes'], seal['sha256'])
inputs = json.loads((ROOT / 'INPUT_CUSTODY.json').read_text())
for item in inputs['read_sources']:
    verify(Path(item['path']), item['bytes'], item['sha256'])

counts = {'executed_subprocess': 0, 'web_tool': 0}
failures = []
for path in sorted((ROOT / 'receipts').glob('*.json')):
    item = json.loads(path.read_text())
    counts[item['kind']] += 1
    if item['kind'] == 'executed_subprocess':
        assert item['recorder_pid'] > 0 and item['subprocess_pid'] > 0
        assert datetime.fromisoformat(item['finished_at_utc']) >= datetime.fromisoformat(item['started_at_utc'])
        assert item['cwd'] == str(ROOT)
        for stream in ['stdout', 'stderr']:
            record = item[stream]
            raw = Path(record['path'])
            assert raw.is_relative_to(PRIVATE)
            verify(raw, record['bytes'], record['sha256'])
        assert Path(item['argv'][0]).name != 'git'
        if item['returncode']:
            failures.append({'label': item['label'], 'returncode': item['returncode']})
    elif item['kind'] == 'web_tool':
        assert item['executable_pid'] is None
        raw = Path(item['raw_private_path'])
        assert raw.is_relative_to(PRIVATE)
        verify(raw, item['raw_bytes'], item['raw_sha256'])

expected_failures = {
    'inspect_historical_body_leads': 1,
    'download_inv_published': 56,
    'download_inv_1999_citeseer': 28,
    'wayback_inv_cdx': 56,
}
assert {x['label']: x['returncode'] for x in failures} == expected_failures
public_forbidden = [str(p) for p in ROOT.rglob('*') if p.is_file()
                    and p.suffix.lower() in {'.pdf', '.txt', '.png', '.jpg', '.jpeg', '.html'}]
assert not public_forbidden, public_forbidden
pdf_magic = {}
for path in sorted(PRIVATE.glob('*.pdf')):
    pdf_magic[path.name] = path.read_bytes().startswith(b'%PDF-')
assert {k for k, v in pdf_magic.items() if not v} == {'abe_journal.pdf', 'abe_journal_oldpdf.pdf'}
coverage = json.loads((ROOT / 'SEARCH_COVERAGE.json').read_text())
queries = sum(len(x['request'].get('search_query', [])) for x in coverage['records'])
assert queries == coverage['captured_search_query_count'] == 33
print(json.dumps({
    'check': 'passed',
    'checks': ['FIRST seal unchanged', 'authentic input hashes unchanged',
               'all completed receipt streams match byte counts and SHA256',
               'actual nonzero retrieval/read results remain disclosed',
               'raw source bodies and pixels outside repository',
               'failed Abe journal bodies correctly identified as non-PDF',
               'captured search count matches requests'],
    'previously_completed_receipt_counts': counts,
    'preserved_nonzero_receipts': failures,
    'private_pdf_magic': pdf_magic,
    'historical_byte_availability_certified': False,
    'method_limit': 'Recorded commands only; no claim that every session bootstrap/read command had a subprocess receipt.'
}, indent=2))
