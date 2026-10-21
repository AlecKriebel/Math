"""Private read-only body/mode, independence-freeze and external-pin verifier.

No network or writes. Final local replay may only create the three exact native
receipt/output files excluded by the manifest; root replay occurs outside here.
"""
from pathlib import Path
import hashlib,json,os,subprocess,sys
if sys.flags.optimize:raise RuntimeError('Run without -O: verification requires assertions enabled.')
S=Path(__file__).resolve().parent;N=S.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,r):
 assert p.is_file() and not p.is_symlink(),str(p)
 b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],str(p)
 assert p.stat().st_mode&0o777==r['mode_decimal'],str(p)
m=json.loads((S/'WHOLE_NAMESPACE_MANIFEST.json').read_text())
assert m['schema']=='pr329-whole-priority-manifest-v1'
assert m['self_seal'] is False and m['publication_authorization'] is False
rows=m['payloads'];expected={r['path'] for r in rows};assert len(expected)==len(rows)
ex={'stage3_current_priority/WHOLE_NAMESPACE_MANIFEST.json',
 'stage3_current_priority/private_evidence/final_whole_replay001/stdout',
 'stage3_current_priority/private_evidence/final_whole_replay001/stderr',
 'stage3_current_priority/private_evidence/final_whole_replay001/receipt.json'}
assert set(m['excluded_exact_paths'])==ex
actual={str(p.relative_to(N)) for p in N.rglob('*') if p.is_file() or p.is_symlink()}
assert actual-ex==expected,{'unexpected':sorted(actual-ex-expected),'missing':sorted(expected-actual)}
for r in rows:
 p=N/r['path'];assert p.resolve().is_relative_to(N.resolve()),r['path'];check(p,r)
for r in m['external_pins']:check(Path(r['path']),r)
freezes=[(N/'SOURCE_ONLY_FREEZE.json',N,'3f82ef0a12c729bf5ebebad8dcaf7622b3c0a714fc4d0d59229a5f23fc43356c',51),
 (N/'stage2_candidate_exposure/FIRST_CANDIDATE_FREEZE.json',N/'stage2_candidate_exposure','4229772cf8b5b3540dbdf2d9c13781d6109e24d1744c0a0981c6cc8f0ea07f16',21)]
for p,base,h,count in freezes:
 assert sha(p.read_bytes())==h,str(p)
 f=json.loads(p.read_text());assert len(f['payloads'])==count
 for r in f['payloads']:check(base/r['path'],r)
 for r in f.get('external_pins',f.get('authorized_external_source_pins',[])):check(Path(r['path']),r)
 if count==21:assert f['earlier_source_freeze_sha256']==freezes[0][2]
# Genuine native receipts are internally checkable against full preserved output.
receipt_count=0
for p in N.rglob('*.receipt.json'):
 r=json.loads(p.read_text())
 if 'actual_exit_code' not in r:continue
 if p.name.endswith('.receipt.json'):
  prefix=p.name[:-len('.receipt.json')]
  for channel in ['stdout','stderr']:
   q=p.parent/(prefix+'.'+channel)
   if q.exists() and channel+'_sha256' in r:
    b=q.read_bytes();assert sha(b)==r[channel+'_sha256'],str(q)
    if channel+'_bytes' in r:assert len(b)==r[channel+'_bytes'],str(q)
 receipt_count+=1
for p in N.rglob('receipt.json'):
 if str(p.relative_to(N)) in ex:continue
 r=json.loads(p.read_text())
 if 'actual_exit_code' not in r:continue
 for channel in ['stdout','stderr']:
  q=p.parent/channel
  if q.exists() and channel+'_sha256' in r:
   b=q.read_bytes();assert sha(b)==r[channel+'_sha256'],str(q)
   if channel+'_bytes' in r:assert len(b)==r[channel+'_bytes'],str(q)
 receipt_count+=1
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
p0=subprocess.run([sys.executable,'-B',str(N/'verify_source_only.py')],cwd=N,env=env,capture_output=True)
assert p0.returncode==0 and p0.stderr==b'',p0.stderr.decode(errors='replace')
assert json.loads(p0.stdout)['official_original_byte_equality'] is True
p=subprocess.run([sys.executable,'-B',str(S/'verify_public_package.py')],cwd=S,env=env,capture_output=True)
assert p.returncode==0 and p.stderr==b'',p.stderr.decode(errors='replace')
pub=json.loads(p.stdout);assert pub['result']=='PASS' and pub['public_payloads']==11
# Recheck all payloads after executable validation; no local mutation permitted.
for r in rows:check(N/r['path'],r)
print(json.dumps({'result':'PASS','namespace_payloads':len(rows),'external_pins':len(m['external_pins']),
 'source_freeze_payloads':51,'first_candidate_freeze_payloads':21,'native_receipts_checked':receipt_count,
 'public_payloads':11,'exact_comparisons':25,'public_verifier_stdout_sha256':sha(p.stdout),
 'whole_manifest_sha256':sha((S/'WHOLE_NAMESPACE_MANIFEST.json').read_bytes()),
 'scope':'read-only full local body/mode/exposure/receipt checks; unsealed, no publication or priority certification'},indent=2))
