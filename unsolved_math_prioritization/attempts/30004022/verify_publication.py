"""Portable frozen-evidence integrity checks; not mathematical certification."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
checks=0
names=[f'TURN_{k}_MANIFEST.json' for k in range(1,5)]
names+=['FINAL_AUTHOR_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']
for name in names:
 path=p/name
 for f in json.loads(path.read_text())['files']:
  b=(path.parent/f['path']).read_bytes()
  assert len(b)==f['bytes'],f['path']
  assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
  checks+=1
assert hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='7700308e01180f2771479a42b644247ee20f1b2b0324e95c43832362dbcb9153'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='dc9a7be9ae4f0dc5ce05ef7111035aecdf2f6bb9d8eedb71aca12790a3a493a4'
print(json.dumps({'status':'PASS_PORTABLE_MANIFESTS','file_digest_checks':checks,'original_status':'unsolved','turns':5},sort_keys=True))
