"""Additive guard-only repair of author diagnostics, with explicit falsification."""
from pathlib import Path
import subprocess,json,hashlib,os,datetime,ast
A=Path(__file__).resolve().parent;O=A/'original_head_authentication_20261006/original_attempt'
D=A/'repaired_diagnostics_v1';D.mkdir(exist_ok=True)
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def sha(x):return hashlib.sha256(x).hexdigest()
def require(b,label):
 if not b:raise RuntimeError(label)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
require(not (D/'RECEIPT.json').exists(),'Already executed repaired diagnostics')
old=(O/'verify.py').read_text()
require(old.count(' assert x;checks+=1')==1,'Exact single guard expected')
fixed=old.replace(' assert x;checks+=1',' if not x:raise AssertionError("Encoded author check failed")\n checks+=1')
(D/'verify.py').write_text(fixed)
(D/'COUNTEREXAMPLE.md').write_bytes((O/'COUNTEREXAMPLE.md').read_bytes())
(D/'.gitignore').write_text('runs/\n')
runsdir=D/'runs';runsdir.mkdir()
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC'}
events=[]
for tag,source,expect in [('baseline',fixed,0),('candidate_coefficient_mutant',fixed.replace('coeff=[1,p**3-2,1]','coeff=[1,p**3-1,1]'),1)]:
 for opt in [False,True]:
  name=tag+('_optimized' if opt else '_normal')
  wd=runsdir/name;wd.mkdir()
  (wd/'COUNTEREXAMPLE.md').write_bytes((O/'COUNTEREXAMPLE.md').read_bytes())
  f=wd/'verify.py';f.write_text(source)
  args=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(f)]
  ch=subprocess.Popen(args,cwd=wd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
  require((ch.returncode==0)==(expect==0),'Guard/mutant outcome '+name)
  entry={'tag':name,'PID':ch.pid,'argv':args,'exit_code':ch.returncode,'expected_success':expect==0,'stdout_sha256':sha(out),'stderr_sha256':sha(err)}
  (D/(name+'.stdout.txt')).write_bytes(out);(D/(name+'.stderr.txt')).write_bytes(err)
  if expect==0:
   result=json.loads((wd/'verification.json').read_text())
   require((wd/'verification.json').read_bytes()==(O/'verification.json').read_bytes(),'Repaired result differs')
   dump(D/(name+'.json'),result)
   entry['result_reproduces_original_bytes']=True
  events.append(entry)
for tag,source in [('original',old),('repaired',fixed)]:
 tree=ast.parse(source);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='ck')
 guard='checks=0\n'+ast.unparse(node)+'\nck(False)\nprint("FALSE_GUARD_RETURNED")\n'
 for opt in [False,True]:
  args=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+['-c',guard]
  ch=subprocess.Popen(args,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
  expected_failure=tag=='repaired' or not opt
  require((ch.returncode!=0)==expected_failure,'False guard '+tag)
  events.append({'tag':tag+('_optimized' if opt else '_normal')+'_false_guard','PID':ch.pid,'exit_code':ch.returncode,'expected_rejection':expected_failure,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
require(sha((O/'verify.py').read_bytes())=='8072ee3f27e404d7ab8e4f56bfecb574e4be23f7e8e60195f4d3b60117a68a44','Original mutated')
record={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'single_guard_only_repair':True,'old_sha256':sha(old.encode()),'new_sha256':sha(fixed.encode()),'candidate_proof_unchanged':True,'original_files_unchanged':True,'new_central_proof_search_turns':0,'events':events}
dump(D/'RECEIPT.json',record)
print(json.dumps({'UTC':record['UTC'],'PID':os.getpid(),'actual_children':len(events),'baseline_author_checks_each':8967,'both_mutants_rejected':True,'original_optimized_false_guard_returned':True,'repaired_false_guard_rejected_both_modes':True}))

