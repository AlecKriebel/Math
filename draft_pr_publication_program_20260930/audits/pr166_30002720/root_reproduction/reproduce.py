from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
A=Path(__file__).resolve().parents[1]
O=A/'original_submission/files/unsolved_math_prioritization/attempts/30002720'
D=A/'root_reproduction';D.mkdir(exist_ok=True)
original=(O/'verify.py').read_text();claim=(O/'COUNTEREXAMPLE.md').read_bytes()
if original.count('    assert test, group')!=1:raise RuntimeError('Verifier gate shape differs')
repaired=original.replace('    assert test, group','    if not test: raise RuntimeError(group)')
(D/'verify_raised.py').write_text(repaired)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cases=[('original',original,False),('repaired',repaired,False)]
for name,old,new in [
 ('changed_stationary_source','Q=F(3,4); R=F(1,4)','Q=F(4,5); R=F(1,5)'),
 ('wrong_first_square','isqrt(i)**2==i and i>=4','isqrt(i)**2==i and i>=9'),
 ('charge_singletons','cost=sum(N for N in Ns if N>1)','cost=sum(N for N in Ns if N>=1)')]:
 if repaired.count(old)!=1 or original.count(old)!=1:raise RuntimeError('Mutation target differs '+name)
 cases.append(('original_'+name,original.replace(old,new),True))
 cases.append(('repaired_'+name,repaired.replace(old,new),True))
rows=[]
for name,code,negative in cases:
 for optimized in (False,True):
  f=D/'scratch'/(name+('_optimized' if optimized else '_ordinary'));f.mkdir(parents=True,exist_ok=True)
  (f/'verify.py').write_text(code);(f/'COUNTEREXAMPLE.md').write_bytes(claim)
  cmd=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(f/'verify.py')]
  p=subprocess.run(cmd,cwd=f,capture_output=True,text=True,timeout=90)
  (f/'stdout.txt').write_text(p.stdout);(f/'stderr.txt').write_text(p.stderr)
  receipt=json.loads((f/'verification.json').read_text()) if (f/'verification.json').exists() else None
  row={'name':name,'optimized':optimized,'negative':negative,'exit_code':p.returncode,'receipt':receipt,'input_code':pin(f/'verify.py'),'claim':pin(f/'COUNTEREXAMPLE.md'),'stdout':pin(f/'stdout.txt'),'stderr':pin(f/'stderr.txt')};rows.append(row)
  if not negative and (p.returncode!=0 or receipt is None or receipt['status']!='PASS'):raise RuntimeError('Positive replay failed '+name)
  if negative and name.startswith('repaired_') and (p.returncode==0 or receipt is not None):raise RuntimeError('Repaired mutant false pass '+name)
  print(json.dumps({'name':name,'optimized':optimized,'exit_code':p.returncode,'assertions':receipt['assertions'] if receipt else None}),flush=True)
o={'UTC':datetime.now(timezone.utc).isoformat(),'status':'POSITIVE_REPLAYS_AND_REPAIRED_NEGATIVE_MODES_ACCEPTED','scope':'Finite exact combinatorial controls and verifier-gate fault injection; not a proof or independent certification of universal asymptotic theorem.','original_inputs':[pin(O/'COUNTEREXAMPLE.md'),pin(O/'verify.py')],'repaired_code':pin(D/'verify_raised.py'),'runs':rows,'original_optimized_negative_false_passes':sum(r['negative'] and r['name'].startswith('original_') and r['optimized'] and r['exit_code']==0 for r in rows),'repaired_negative_modes_rejected':sum(r['negative'] and r['name'].startswith('repaired_') and r['exit_code']!=0 for r in rows),'mathematical_clearance':False,'priority_started':False}
out=D/'REPRODUCTION_AND_NEGATIVE_CONTROLS.json';out.write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({'receipt':pin(out),'status':o['status']}))

