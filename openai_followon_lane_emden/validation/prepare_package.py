#!/usr/bin/env python3
"""Create the explicit, deterministic deposit source archive; no cache/secrets."""
from pathlib import Path
import hashlib,json,zipfile
p=Path(__file__).resolve().parents[1]
items={}
for n in ['main.tex','README.md','LICENSES.md','verify.py']:
    items[n]=p/'publication'/n
for n in ['DEPENDENCY_LEDGER.md','CURRENT_THEOREM.md']:
    items[n]=p/n
for n in ['upstream_mathematical_audit.md','upstream_interval_review.md','upstream_interval_checks.py','transfer_proofs.md','priority_audit.md','priority_modern_check.md','formal_input_audit.md']:
    items['notes/'+n]=p/'notes'/n
for n in ['SOURCE_HASHES.json','370.md','UPSTREAM_LICENSE','UPSTREAM_README.md','priority_source_manifest.json','priority_modern_manifest.json']:
    items['sources/'+n]=p/'sources'/n
for f in (p/'sources/family370').rglob('*'):
    if f.is_file(): items[str(f.relative_to(p))]=f
for n in ['formal_source_hashes.json','formal_source_trust_scan.json','formal_prepare.py','formal_lean_dependency_lock.json','formal_AxiomAudit.lean','formal_model_elaboration_attempt.log','interval_diagnostics.json']:
    items['validation/'+n]=p/'validation'/n
# Latest fresh report remains outside its own reviewed archive to avoid hash self-reference.
for n in ['review01.md','response01.md']:
    f=p/'reviews'/n
    if f.exists(): items['reviews/'+n]=f
with zipfile.ZipFile(p/'publication/source-and-verification.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,f in sorted(items.items()):
        data=f.read_bytes()
        info=zipfile.ZipInfo(name,date_time=(2026,10,6,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644 << 16
        z.writestr(info,data)
identities={name:{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for name,f in sorted(items.items())}
(p/'receipts/package_members.json').write_text(json.dumps(identities,indent=2)+'\n')
print('Prepared',len(items),'explicit members')
