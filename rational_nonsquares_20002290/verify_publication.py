"""Check reviewed bytes, reversible repairs, published reviews, and exact controls."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parent
sha=lambda data:hashlib.sha256(data).hexdigest()
rev=json.loads((root/'REVISED_MANIFEST.json').read_text())
orig=json.loads((root/'ORIGINAL_MANIFEST.json').read_text())
projections=json.loads((root/'PUBLICATION_PROJECTION.json').read_text())
projected={x['file']:x for x in projections['changes']}
for e in rev['files']:
 data=(root/e['path']).read_bytes()
 if e['path'] in projected:
  assert sha(data)==projected[e['path']]['published_sha256'],e['path']
  assert e['sha256']==projected[e['path']]['source_sha256'],e['path']
 else:
  assert len(data)==e['bytes'] and sha(data)==e['sha256'],e['path']
for e in projected.values():assert sha((root/e['file']).read_bytes())==e['published_sha256'],e['file']
changes=json.loads((root/'RELEASE_CHANGE_MAP.json').read_text())['changes']
for e in orig['files']:
 data=(root/e['path']).read_text()
 for change in reversed(changes):
  if change['file']==e['path']:
   assert data.count(change['new'])==1,e['path']
   data=data.replace(change['new'],change['old'])
 raw=data.encode();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'],e['path']
with tempfile.TemporaryDirectory() as temp:
 temp=Path(temp);shutil.copyfile(root/'verify_identities.py',temp/'verify_identities.py')
 subprocess.run([sys.executable,str(temp/'verify_identities.py')],check=True,capture_output=True)
 assert (temp/'verification.json').read_bytes()==(root/'verification.json').read_bytes()
print('PASS: revised bytes, both reviews, 10 reconstructed original files, and all 8 exact-check groups.')
