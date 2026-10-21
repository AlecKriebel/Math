#!/usr/bin/env python3
"""Read-only validation of this explicit curated priority-audit allowlist."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
EXPECTED = {
    'README.md', 'FULL_REPORT.md', 'THEOREM_COMPARISON.md',
    'LE_VERSION_AUDIT.md', 'SEARCH_LOG.md', 'SOURCE_MAP.json',
    'INPUT_AUTHENTICATION.json', 'RESULT.json', 'RESEARCH_LOG.md',
    'verify_manifest.py',
}
manifest = json.loads((BASE / 'MANIFEST.json').read_text())
rows = manifest['files']
assert len(rows) == len(EXPECTED)
assert {r['path'] for r in rows} == EXPECTED
for row in rows:
    rel = Path(row['path'])
    assert not rel.is_absolute() and len(rel.parts) == 1
    assert rel.name not in {'private', 'tmp', 'MANIFEST.json'}
    f = BASE / rel
    assert f.is_file() and not f.is_symlink()
    b = f.read_bytes()
    assert len(b) == row['bytes'], str(rel)
    assert hashlib.sha256(b).hexdigest() == row['sha256'], str(rel)
result = json.loads((BASE / 'RESULT.json').read_text())
assert result['problem_id'] == 6000001 and result['pr'] == 946
assert result['new_proof_responses_added'] == 0
assert result['novelty_gate'] == 'NOT_CERTIFIED'
auth = json.loads((BASE / 'INPUT_AUTHENTICATION.json').read_text())
assert auth['proof_copies_equal']
assert auth['proof_git_sha256'] == 'a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2'
assert auth['statement_sha256_utf8'] == '04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd'
print(json.dumps({'curated_files': len(rows), 'bytes_and_sha256': 'PASS',
                  'private_or_raw_allowed': False, 'target_and_budget_controls': 'PASS'}))
