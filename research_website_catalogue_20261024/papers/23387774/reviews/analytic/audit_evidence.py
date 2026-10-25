#!/usr/bin/env python3
"""Read-only custody and own-diagnostic checker; no network/foreign code execution."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

E = Path(__file__).resolve().parent


def load(name): return json.loads((E/name).read_text())
def digest(path):
    data=Path(path).read_bytes()
    return len(data),sha256(data).hexdigest()
def verify(rows):
    for row in rows:
        assert digest(row['path'])==(row['bytes'],row['sha256']),row['path']
    return len(rows)


base=load('source-baseline.json')
source_count=verify(base['files'])
assert {r['path'] for r in base['files']}=={
    str(p) for p in (E.parent.parent/'sources').rglob('*') if p.is_file()
}
early=load('EARLY_SEAL.json')
early_count=verify(early['files'])
assert digest(E/'EARLY_SEAL.json')[1]=='14b670068cf2198143feb9145266eec0f40b89af068b28c65d6e87591c851ff7'
ledger=load('PRIMARY_READ_LEDGER.json')
external_count=verify(ledger['external_primary_bodies'])
cache_count=verify(ledger['own_cache_files'])
assert {r['path'] for r in ledger['own_cache_files']}=={
    str(p) for p in (E/'primary-cache').rglob('*') if p.is_file()
}
assert '/primary-cache/' in (E/'.gitignore').read_text().splitlines()
verify([ledger['external_ignore_binding']])
assert '*' in Path(ledger['external_ignore_binding']['path']).read_text().splitlines()
custody=load('primary-custody-receipt.json')
verify(custody['files'])
verify([custody['source_worker_raw_fetch_receipt_binding']])
for row in custody['files']:
    assert Path(row['path']).read_bytes().startswith(b'%PDF-')
assert load('abt-acquisition-receipt.json')['pdf_magic'] is False
assert load('WEB_PRIMARY_READ_RECEIPT.json')['ABT']['local_raw_pdf_retained'] is False

# Evaluate only newly written own diagnostics. Their normal main-block JSON write
# is bypassed, so the recorded result and all sealed artifacts remain unchanged.
code=E/'independent_exact_checks.py'
scope={'__name__':'independent_readonly_reaudit','__file__':str(code)}
exec(compile(code.read_text(),str(code),'exec'),scope)
actual=scope['run_checks']()
recorded=load('independent-exact-checks.json')
for key,value in actual.items(): assert value==recorded[key],key
assert actual['all_pass']
verdict=load('VERDICT.json')
assert verdict['mathematical_verdict']=='SUPPORTED_AT_LITERAL_SCOPE'
assert not verdict['publication_clearance'] and not verdict['source_correction_required']

manifest_count=None
if (E/'MANIFEST.json').exists():
    manifest=load('MANIFEST.json')
    manifest_count=verify(manifest['files'])
    expected={r['path'] for r in manifest['files']}
    actual_paths={str(p) for p in E.rglob('*') if p.is_file()
                  and p.relative_to(E).parts[0] not in {'primary-cache','tmp'}
                  and p.name not in {'MANIFEST.json','SEAL.json'}}
    assert expected==actual_paths
seal_count=None
if (E/'SEAL.json').exists():
    seal=load('SEAL.json')
    seal_count=verify(seal['bindings'])
    assert seal['status']=='COMPLETE_SEALED'
    assert seal['manifest_file_count']==manifest_count

print(json.dumps({
    'utc':datetime.now(timezone.utc).isoformat(),'all_pass':True,
    'original_source_bindings_verified':source_count,
    'early_bindings_verified':early_count,
    'complete_external_primary_pdf_bodies_verified':external_count,
    'own_ignored_cache_files_verified':cache_count,
    'raw_acquisition_and_ignore_bindings_verified':True,
    'ABT_web_only_local_failure_qualified':True,
    'own_exact_diagnostics_recomputed_without_writes':True,
    'manifest_files_verified':manifest_count,'seal_bindings_verified':seal_count,
    'network_or_deposited_or_foreign_program_execution':False,
},indent=2))
