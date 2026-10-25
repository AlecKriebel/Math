#!/usr/bin/env python3
"""Read-only review custody + own exact-diagnostic checker; no network/source execution."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

E = Path(__file__).resolve().parent


def read(name):
    return json.loads((E / name).read_text())


def digest(path):
    data = Path(path).read_bytes()
    return len(data), sha256(data).hexdigest()


def verify(rows):
    for row in rows:
        actual = digest(row['path'])
        expected = row['bytes'], row['sha256']
        assert actual == expected, (row['path'], expected, actual)
    return len(rows)


baseline = read('source-baseline.json')
source_count = verify(baseline['files'])
early = read('EARLY_SEAL.json')
early_count = verify(early['files'])
assert digest(E / 'EARLY_SEAL.json')[1] == '2f7598194155ce0548c9a467cffef108a1267e1cd6b7d6d091cb7a7163c4ac92'

custody = read('FINAL_CUSTODY.json')
addition_count = verify(custody['observed_source_additions'])
expected_source_paths = {r['path'] for r in baseline['files'] + custody['observed_source_additions']}
actual_source_paths = {str(p) for p in (E.parent.parent / 'sources').rglob('*') if p.is_file()}
assert actual_source_paths == expected_source_paths
assert custody['all_pass'] and source_count == 231 and addition_count == 2

ledger = read('PRIMARY_READ_LEDGER.json')
cache_count = verify(ledger['raw_cache_files'])
assert {r['path'] for r in ledger['raw_cache_files']} == {
    str(p) for p in (E / 'primary-cache').rglob('*') if p.is_file()
}
assert '/primary-cache/' in (E / '.gitignore').read_text().splitlines()
for row in ledger['primary_bodies']:
    assert Path(row['path']).read_bytes().startswith(b'%PDF-')

originals = read('retained-original-hash-receipt.json')
for row in originals['files']:
    assert digest(row['old_raw_path']) == digest(row['own_raw_path']) == (row['bytes'], row['sha256'])

# Only code newly authored for this independent review is evaluated. Setting a
# non-main name bypasses its normal timestamped JSON write; this invocation is read-only.
code_path = E / 'independent_exact_checks.py'
scope = {'__file__': str(code_path), '__name__': 'independent_readonly_reaudit'}
exec(compile(code_path.read_text(), str(code_path), 'exec'), scope)
recorded = read('independent-exact-checks.json')
for key, function in [('coordinate_law', 'coordinate_checks'),
                      ('noncompact_scalar_lift', 'scalar_lift_checks'),
                      ('Schur', 'schur_checks'),
                      ('torsion_boundary', 'torsion_check')]:
    assert scope[function]() == recorded[key], key
assert recorded['all_pass']

manifest_count = None
if (E / 'MANIFEST.json').exists():
    manifest = read('MANIFEST.json')
    manifest_count = verify(manifest['files'])
    expected = {r['path'] for r in manifest['files']}
    actual = {str(p) for p in E.rglob('*') if p.is_file()
              and p.relative_to(E).parts[0] not in {'primary-cache', 'tmp'}
              and p.name not in {'MANIFEST.json', 'SEAL.json'}}
    assert actual == expected, {'extra': sorted(actual - expected), 'missing': sorted(expected - actual)}

seal_count = None
if (E / 'SEAL.json').exists():
    seal = read('SEAL.json')
    seal_count = verify(seal['bindings'])
    assert seal['status'] == 'COMPLETE_SEALED'
    assert seal['manifest_file_count'] == manifest_count

print(json.dumps({
    'utc': datetime.now(timezone.utc).isoformat(),
    'all_pass': True,
    'original_source_bindings_verified': source_count,
    'observed_later_source_custody_additions_verified': addition_count,
    'early_bindings_verified': early_count,
    'raw_primary_cache_files_verified': cache_count,
    'primary_pdf_bodies_verified': len(ledger['primary_bodies']),
    'original_retained_raw_matches_verified': len(originals['files']),
    'own_exact_diagnostics_recomputed_without_writes': True,
    'manifest_files_verified': manifest_count,
    'seal_bindings_verified': seal_count,
    'network_or_source_program_execution': False,
}, indent=2))
