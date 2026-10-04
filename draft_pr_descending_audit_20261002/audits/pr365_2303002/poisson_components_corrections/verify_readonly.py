"""Read-only supplement closure and original-namespace restoration check."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
seal=json.loads((R/'FINAL_SEAL.json').read_text())
assert sha((R/'SUPPLEMENT_MANIFEST.json').read_bytes())==seal['manifest_sha256']
m=json.loads((R/'SUPPLEMENT_MANIFEST.json').read_text())
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and 'private' not in p.relative_to(R).parts and '__pycache__' not in p.relative_to(R).parts and p.name not in ('FINAL_SEAL.json','SUPPLEMENT_MANIFEST.json')}
assert actual==set(m['files'])
for p,f in m['files'].items():
    b=(R/p).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
private=json.loads((R/'PRIVATE_INVENTORY.json').read_text())['files']
assert {str(p.relative_to(R)) for p in (R/'private').rglob('*') if p.is_file()}==set(private)
for p,f in private.items():
    b=(R/p).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
O=R.parent/'poisson_components_review'
assert sha((O/'FINAL_SEAL.json').read_bytes())==seal['original_final_seal_sha256']
assert sha((O/'PUBLIC_MANIFEST.json').read_bytes())==seal['original_public_manifest_sha256']
print(json.dumps({'status':'PASS','original_closure_restored':True,'supplement_public_files':len(actual),'private_chronology_files':len(private),'writes':0},indent=2,sort_keys=True))
