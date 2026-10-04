"""Read-only complete binding and retained-output validation of the additive audit."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,r):
 assert not p.is_symlink();b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());expected={r['path'] for r in m['files']}
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() and p.name!='PUBLIC_MANIFEST.json'
        and not any(part in {'private_runtime','__pycache__','post_merge'} for part in p.relative_to(D).parts)}
assert actual==expected and len(expected)==len(m['files'])
for r in m['files']:check(D/r['path'],r)
for r in json.loads((D/'FINAL_SEAL.json').read_bytes())['sealed_artifacts']:check(D/r['path'],r)
for capture in json.loads((D/'receipts/EXECUTIONS.json').read_bytes()):
 assert capture['exit_code']==0
 for channel in ('stdout','stderr'):
  r=capture[channel];stored=(D/r['path']).read_bytes()
  assert len(stored)==r['stored_bytes'] and sha(stored)==r['stored_sha256']
  raw=gzip.decompress(stored);assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
  if channel=='stderr':assert raw==b''
for failed in sorted(D.glob('failed_attempt_*')):
 context=json.loads((failed/'FAILED_CONTEXT.json').read_bytes());assert context['status']=='FAILED_NO_ACCEPTANCE_CREDIT'
 for capture in json.loads((failed/'receipts/EXECUTIONS.json').read_bytes()):
  for channel in ('stdout','stderr'):
   r=capture[channel];stored=(failed/r['path']).read_bytes();assert len(stored)==r['stored_bytes'] and sha(stored)==r['stored_sha256']
   raw=gzip.decompress(stored);assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
assert all(c['pass'] is True for c in json.loads((D/'receipts/CHECKS.json').read_bytes()))
print('PASS: complete additive audit, final seal, every binding and all full retained execution outputs')
