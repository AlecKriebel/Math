#!/usr/bin/env python3
"""Repeat R2 ordinary/optimized replay and meaningful false-mechanism tests.

Writes only below this script's directory. Never executes external archives.
"""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,shutil,hashlib,json,sys,time
out=Path(__file__).resolve().parent
package=out.parent/'publication_package_v2'
plan=[('baseline',None,None),
 ('wrong_terminal_parity','verify_exact.py',("terminal='P' if (t+e)%2==0 else 'Q'","terminal='Q' if (t+e)%2==0 else 'P'")),
 ('wrong_intrinsic_reversal','verify_exact.py',('mr=(-m-1 if e==0 else -m)%r','mr=(-m if e==0 else -m-1)%r')),
 ('hex_no_double_first_hit','verify_exact.py',('d=2 if s==2 else 1','d=1')),
 ('affine_scale_squared_wrong','verify_exact.py',('==lam*lam*sum(x*x for x in av)','==lam*sum(x*x for x in av)')),
 ('witness_perturb_B','exact_reversal_counterexample.py',('B=(scalar(5,4),scale(mul(c,c),2))','B=(scalar(6,4),scale(mul(c,c),2))'))]
results=[]
for name,file,mutation in plan:
 for optimized in (False,True):
  dest=out/'replays'/(name+('_optimized' if optimized else '_normal'))
  if dest.exists():shutil.rmtree(dest)
  shutil.copytree(package,dest)
  if file:
   f=dest/'verification'/file;before=f.read_text();old,new=mutation
   if old not in before:raise RuntimeError('Mutation absent '+name)
   f.write_text(before.replace(old,new,1))
  # Retain complete source-layout copy, then remove recorded success outputs.
  # A fresh run must create its own receipt; a failure must create none.
  for receipt in ('verification.json','exact_reversal_counterexample.json'):
   (dest/'verification'/receipt).unlink()
  scripts=('verify_exact.py','exact_reversal_counterexample.py') if name=='baseline' else (file,)
  for script in scripts:
   receipt='verification.json' if script=='verify_exact.py' else 'exact_reversal_counterexample.json'
   cmd=[sys.executable]+(['-O'] if optimized else [])+[str(dest/'verification'/script)]
   t=time.time();r=subprocess.run(cmd,cwd=dest,text=True,capture_output=True)
   (dest/(script+'.stdout.txt')).write_text(r.stdout);(dest/(script+'.stderr.txt')).write_text(r.stderr)
   created=(dest/'verification'/receipt).exists()
   entry={'name':name,'optimized':optimized,'script':script,'returncode':r.returncode,'seconds':time.time()-t,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr':r.stderr[-1200:],'mutation':mutation,'success_receipt_created':created}
   if name=='baseline':
    parsed=json.loads(r.stdout);expected=package/'verification'/receipt
    entry['check_count']=parsed.get('exact_checks',parsed.get('check_count'))
    entry['receipt_bytes_equal_pinned']=created and expected.read_bytes()==(dest/'verification'/receipt).read_bytes()
    if r.returncode or not entry['receipt_bytes_equal_pinned']:raise RuntimeError('Baseline mismatch')
   else:
    entry['detected_false_condition']=r.returncode!=0 and not created
    if not entry['detected_false_condition']:raise RuntimeError('Undetected or stale success '+name)
   results.append(entry)
(out/'REPLAY_RESULTS.json').write_text(json.dumps({'time':datetime.now(timezone.utc).isoformat(),'python':sys.version,'removed_success_receipts_before_each_fresh_layout_run':True,'runs':results},indent=2)+'\n')
print(json.dumps({'fresh_success_runs':sum(x['name']=='baseline' for x in results),'fresh_failure_runs':sum(x['name']!='baseline' for x in results),'all_failures_created_no_success_receipt':all(not x['success_receipt_created'] for x in results if x['name']!='baseline')}))
