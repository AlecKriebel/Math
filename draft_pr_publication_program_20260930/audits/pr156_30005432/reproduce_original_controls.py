#!/usr/bin/env python3
"""Reproduce original brace controls and repair their optimization-disabled check harness."""
import datetime,hashlib,json,shutil,subprocess,sys
from pathlib import Path
A=Path(__file__).resolve().parent
O=A/'original_submission/files/unsolved_math_prioritization/attempts/30005432'
F=A/'root_reproduction';F.mkdir(exist_ok=False)
R=A/'repaired_diagnostics_v1';R.mkdir(exist_ok=False)
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
original=(O/'verify.py').read_text()
require('def ck(g,b):assert b,g;C[g]+=1' in original,'Unexpected original checker')
repaired=original.replace('def ck(g,b):assert b,g;C[g]+=1','def ck(g,b):\n if not b:raise RuntimeError(g)\n C[g]+=1')
(R/'verify.py').write_text(repaired)
(R/'COUNTEREXAMPLE.md').write_bytes((O/'COUNTEREXAMPLE.md').read_bytes())
(R/'REPAIR_NOTE.md').write_text('The submitted written proof is retained unchanged. Original verify.py used assert; optimization removes these checks while leaving an apparent PASS count. The repaired checker raises RuntimeError on failed checks in both modes. These controls supplement the universal integer and infinite-coset proof; they do not establish novelty or infer infinite index from finite quotients.\n')
runs=[]
for name,code,optimized,expect in [('original_normal',original,False,'PASS'),('repaired_normal',repaired,False,'PASS'),('repaired_optimized',repaired,True,'PASS'),('original_bad_eps_normal',original.replace('return 1 if c%4 in (0,1) else -1','return 1'),False,'FAIL'),('original_bad_eps_optimized',original.replace('return 1 if c%4 in (0,1) else -1','return 1'),True,'FALSE_PASS_CHECKS_DISABLED'),('repaired_bad_eps_normal',repaired.replace('return 1 if c%4 in (0,1) else -1','return 1'),False,'FAIL'),('repaired_bad_eps_optimized',repaired.replace('return 1 if c%4 in (0,1) else -1','return 1'),True,'FAIL')]:
 d=F/name;d.mkdir()
 (d/'verify.py').write_text(code);(d/'COUNTEREXAMPLE.md').write_bytes((O/'COUNTEREXAMPLE.md').read_bytes())
 args=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(d/'verify.py')]
 p=subprocess.run(args,capture_output=True,text=True,timeout=30)
 (d/'stdout.txt').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 count=None
 if expect in ('PASS','FALSE_PASS_CHECKS_DISABLED'):
  require(p.returncode==0,'Expected successful diagnostic process '+name)
  result=json.loads(p.stdout);count=result['assertions']
  require(count==33512 and result['artifact_sha256']==sha((O/'COUNTEREXAMPLE.md').read_bytes()),'Original control count/artifact differs')
  (d/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 else:
  require(p.returncode!=0 and 'double_right_star' in p.stderr,'Corrupted infinite-factor checker did not fail as expected '+name)
  require('PASS_EXACT_COUNTEREXAMPLE_CONTROLS' not in p.stdout,'Bad checker printed PASS')
 runs.append({'name':name,'optimized':optimized,'exit_code':p.returncode,'expected_outcome':expect,'diagnostic_count':count,'code_sha256':sha(code.encode()),'proof_sha256':sha((O/'COUNTEREXAMPLE.md').read_bytes())})
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rec={'UTC':now,'status':'ORIGINAL_NORMAL_AND_REPAIRED_BOTH_MODES_REPRODUCED_NEGATIVE_CONTROLS_ACCEPTED','original_proof_unchanged':True,'original_checker_normal_controls':33512,'repaired_checker_controls_per_mode':33512,'original_optimized_receipts_are_not_proof_certificates':True,'original_bad_eps_optimized_falsely_passes':True,'repaired_bad_eps_fails_both_modes':True,'repaired_checker_sha256':sha(repaired.encode()),'runs':runs,'mathematical_scope':'Finite-component and exact integer coefficient controls; universal written infinite-coset proof remains essential. Mathematical/priority clearance awaits independent gates.','provider_mutations':False}
(F/'RESULT.json').write_text(json.dumps(rec,indent=2)+'\n')
files=[]
for root in [F,R]:
 for p in sorted(root.rglob('*')):
  if p.is_file():
   b=p.read_bytes();files.append({'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)})
(F/'OUTPUT_MANIFEST.json').write_text(json.dumps({'UTC':now,'files':files},indent=2)+'\n')
print(json.dumps({k:rec[k] for k in ('status','original_checker_normal_controls','repaired_checker_controls_per_mode','original_bad_eps_optimized_falsely_passes','repaired_bad_eps_fails_both_modes')}))

