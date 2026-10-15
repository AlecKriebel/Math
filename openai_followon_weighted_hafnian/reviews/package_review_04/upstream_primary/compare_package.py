#!/usr/bin/env python3
"""Compare independently recorded primary hashes to frozen v4 declarations."""
from pathlib import Path
import hashlib,json,datetime
HERE=Path(__file__).resolve().parent
PACKAGE=HERE.parent/'extracted'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((HERE/'PRIMARY_RECEIPTS.json').read_text())
formal=json.loads((PACKAGE/'research/lean_source_inspection/STATIC_AUDIT_RECEIPT.json').read_text())
refs=json.loads((PACKAGE/'DEPENDENCY_REFERENCES.json').read_text())
checks={};mismatches=[]
for name,value in primary['lean_import_closure'].items():
    path=value['path'].removeprefix('lean/')
    expected=formal['hashes'].get(path)
    checks[path]={'independent_sha256':value['sha256'],'package_recorded_sha256':expected}
    if expected!=value['sha256']:mismatches.append(path)
for path,value in primary['source_files'].items():
    expected=refs['manuscript_sha256'].get(path)
    if expected is not None:
        checks[path]={'independent_sha256':value['sha256'],'package_recorded_sha256':expected}
        if expected!=value['sha256']:mismatches.append(path)
reviewed=['main.tex','research/UPSTREAM_PROOF_AUDIT.md','research/FORMAL_SCOPE_AUDIT.md',
          'DEPENDENCY_LEDGER.md','DEPENDENCY_REFERENCES.json',
          'research/lean_source_inspection/STATIC_AUDIT_RECEIPT.json',
          'research/lean_source_inspection/audit_sources.py']
r={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'package':'Frozen extracted v4','package_root':str(PACKAGE),
   'reviewed_files':{name:{'sha256':sha(PACKAGE/name),'bytes':(PACKAGE/name).stat().st_size} for name in reviewed},
   'primary_pin':primary['pinned_commit'],'source_hash_comparisons':checks,
   'hash_mismatches':mismatches,'independent_OAI_modules':len(primary['lean_import_closure']),
   'package_OAI_modules':formal['local_module_count'],
   'independent_OAI_bytes':primary['lean_closure_bytes'],'package_OAI_bytes':formal['local_source_bytes'],
   'independent_kernel_replay':False,'package_claims_kernel_replay':formal['kernel_build_reproduced']}
assert not mismatches,mismatches
assert r['independent_OAI_modules']==r['package_OAI_modules']
assert r['independent_OAI_bytes']==r['package_OAI_bytes']
(HERE/'PACKAGE_COMPARISON_RECEIPTS.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:r[k] for k in ('reviewed_files','hash_mismatches','independent_OAI_modules','independent_OAI_bytes','independent_kernel_replay','package_claims_kernel_replay')},indent=2))
