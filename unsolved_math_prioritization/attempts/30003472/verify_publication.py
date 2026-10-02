"""Check preserved evidence bytes, not mathematical truth."""
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;n=0
names=['CHECKPOINT_MANIFEST.json']+[f'TURN_{k}_MANIFEST.json' for k in (2,3,4)]+['FINAL_PACKET_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']
for name in names:
 m=p/name
 for f in json.loads(m.read_text())['files']:
  b=(m.parent/f['path']).read_bytes()
  assert len(b)==f['bytes'],f['path']
  assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
  n+=1
assert hashlib.sha256((p/'FINAL_PACKET_MANIFEST.json').read_bytes()).hexdigest()=='e21ce309aa21fcc8d354c9933893145792c518393304d16757f9723ac2491e43'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='b6c8250dbc46144e9dca05a10bc246987645dbb301ea159169f8a5ed1ea8b4e4'
print(json.dumps({'status':'PASS_PORTABLE_MANIFESTS','file_digest_checks':n,'original_status':'unsolved','turns':5},sort_keys=True))
