#!/usr/bin/env python3
"""Read-only audit: source, early/final custody, primary identities, own diagnostics."""
from pathlib import Path
from hashlib import sha256, md5
from datetime import datetime, timezone
import json

E = Path(__file__).resolve().parent


def load(name): return json.loads((E / name).read_text())
def digest(path):
    data = Path(path).read_bytes()
    return len(data), sha256(data).hexdigest()
def verify(rows):
    for row in rows:
        assert digest(row['path']) == (row['bytes'], row['sha256']), row['path']
    return len(rows)


baseline = load('source-baseline.json')
source_count = verify(baseline['files'])
assert {r['path'] for r in baseline['files']} == {
    str(p) for p in (E.parent.parent / 'sources').rglob('*') if p.is_file()
}
early = load('EARLY_SEAL.json')
early_count = verify(early['files'])
assert digest(E / 'EARLY_SEAL.json')[1] == 'afa40f12f4b1c13891b404097bdf062a4cfcd8ddc4e8295c13d7ab54db19124c'

ledger = load('PRIMARY_READ_LEDGER.json')
cache_count = verify(ledger['raw_cache_files'])
assert {r['path'] for r in ledger['raw_cache_files']} == {
    str(p) for p in (E / 'primary-cache').rglob('*') if p.is_file()
}
assert '/primary-cache/' in (E / '.gitignore').read_text().splitlines()
for row in ledger['primary_bodies']:
    assert Path(row['path']).read_bytes().startswith(b'%PDF-')

transfer = load('prior-primary-transfer-receipt.json')
for row in transfer['files']:
    assert digest(row['source_path']) == digest(row['path']) == (row['bytes'], row['sha256'])
chronology = load('chronology-receipt.json')
verify([chronology['prior_api'], chronology['reviewed_api']])
prior_api = json.loads(Path(chronology['prior_api']['path']).read_text())
asset = next(f for f in prior_api['files'] if f['key'] == 'OWR-15208-008-paper.pdf')
prior_pdf = (E / 'primary-cache' / 'prior-23062867.pdf').read_bytes()
assert len(prior_pdf) == asset['size']
assert 'md5:' + md5(prior_pdf).hexdigest() == asset['checksum']
assert prior_api['metadata']['publication_date'] == '2026-09-30'
assert chronology['reviewed']['publication_date'] == '2026-10-04'

# The only evaluated code is newly written for this analytic lane. Avoid its
# main block, which normally writes a fresh timestamped diagnostic receipt.
code = E / 'independent_exact_checks.py'
scope = {'__name__': 'independent_readonly_reaudit', '__file__': str(code)}
exec(compile(code.read_text(), str(code), 'exec'), scope)
actual = scope['run_checks']()
recorded = load('independent-exact-checks.json')
for key, value in actual.items(): assert value == recorded[key], key
assert actual['all_pass']
verdict = load('VERDICT.json')
assert verdict['mathematical_verdict'] == 'SUPPORTED_AT_LITERAL_MATHEMATICAL_SCOPE'
assert verdict['original_claim_package_disposition'] == 'DEFER_ATTRIBUTION_CONTRIBUTION_CORRECTION'
assert not verdict['publication_clearance']

manifest_count = None
if (E / 'MANIFEST.json').exists():
    manifest = load('MANIFEST.json')
    manifest_count = verify(manifest['files'])
    expected = {r['path'] for r in manifest['files']}
    actual_paths = {str(p) for p in E.rglob('*') if p.is_file()
                    and p.relative_to(E).parts[0] not in {'primary-cache', 'tmp'}
                    and p.name not in {'MANIFEST.json', 'SEAL.json'}}
    assert expected == actual_paths
seal_count = None
if (E / 'SEAL.json').exists():
    seal = load('SEAL.json')
    seal_count = verify(seal['bindings'])
    assert seal['status'] == 'COMPLETE_SEALED'
    assert seal['manifest_file_count'] == manifest_count

print(json.dumps({
    'utc': datetime.now(timezone.utc).isoformat(), 'all_pass': True,
    'original_source_bindings_verified': source_count,
    'early_bindings_verified': early_count,
    'raw_primary_cache_files_verified': cache_count,
    'primary_pdf_bodies_verified': len(ledger['primary_bodies']),
    'transferred_complete_objects_verified': len(transfer['files']),
    'prior_pdf_api_size_md5_and_chronology_match': True,
    'own_exact_diagnostics_recomputed_without_writes': True,
    'mathematical_and_attribution_verdicts_kept_separate': True,
    'manifest_files_verified': manifest_count, 'seal_bindings_verified': seal_count,
    'network_or_deposited_or_foreign_program_execution': False,
}, indent=2))
