import os,json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;T=B/'private/tmp/links';T.mkdir(parents=True,exist_ok=True);R='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python';ORIG=B.parents[2]/'original/unsolved_math_prioritization/attempts/6000001';tools={'gate':B/'portable_gate.py','worker':B/'portable_worker.py','comparator':B/'compare_results.py'};pins={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in tools.items()};records=[]
for kind in ['file_link','ancestor_link']:
 for key,source in tools.items():
  if kind=='file_link':path=T/(key+'.link');path.symlink_to(source)
  else:
   parent=T/(key+'_ancestor');parent.symlink_to(B,target_is_directory=True);path=parent/source.name
  use=dict(tools);use[key]=path
  cmd=[R,'-I','-S','-B',str(B/'launch_portable_gate.py'),str(ORIG),'--scratch',str(T)]
  for k in tools:cmd+=['--'+k,str(use[k]),'--'+k+'-sha256',pins[k]]
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
  if not(p.returncode and 'nonblocking executable authentication' in p.stderr):raise RuntimeError('Link accepted')
  records.append(dict(case=kind+'_'+key,command=cmd,returncode=p.returncode,stderr=p.stderr,worker_not_reached=True,timeout_seconds=5,timed_out=False))
(B/'evidence/LINK_TESTS.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',negative_controls=len(records),records=records),indent=2)+'\n')
