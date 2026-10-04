"""Validate the complete actual-merge public manifest, seal and full captures."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(p,r):
 assert not p.is_symlink();b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());expected={r['path'] for r in m['files']}
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() and p.name!='PUBLIC_MANIFEST.json' and not any(x in {'private_runtime','__pycache__'} for x in p.relative_to(D).parts)}
assert actual==expected and len(expected)==len(m['files'])
for r in m['files']:binding(D/r['path'],r)
for r in json.loads((D/'FINAL_SEAL.json').read_bytes())['sealed_artifacts']:binding(D/r['path'],r)
for c in json.loads((D/'receipts/EXECUTIONS.json').read_bytes()):
 assert c['exit_code']==0
 for channel in ['stdout','stderr']:
  r=c[channel];stored=(D/r['path']).read_bytes();assert len(stored)==r['stored_bytes'] and sha(stored)==r['stored_sha256'];raw=gzip.decompress(stored);assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
  if channel=='stderr':assert raw==b''
assert all(c['pass'] is True for c in json.loads((D/'receipts/CHECKS.json').read_bytes()))
print('PASS: actual merge audit entire closed manifest, seal and all complete outputs')
