import json,os,subprocess,hashlib,shutil,time
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;ORIG=B.parents[1]/'original/unsolved_math_prioritization/attempts/6000001';TMP=B/'private/tmp/portable';TMP.mkdir(parents=True,exist_ok=True)
R='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
G=B/'portable_gate.py';W=B/'portable_worker.py';C=B/'compare_results.py';pins={q.name:sha(q) for q in [G,W,C]}
records=[]
def run(label,packet,opts=(),extra=(),env2=False,worker=None,comparator=None):
 worker=worker or W;comparator=comparator or C
 cmd=[R,'-I','-S','-B',*opts,str(G),str(packet),'--gate-sha256',pins[G.name],'--worker',str(worker),'--worker-sha256',pins[W.name],'--comparator',str(comparator),'--comparator-sha256',pins[C.name],'--scratch',str(TMP),*extra]
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 if env2:env.update(PYTHONOPTIMIZE='2',PYTHONPATH='/does/not/exist')
 start=datetime.now(timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(cmd,cwd=TMP,env=env,capture_output=True,text=True,timeout=1200)
 (B/'evidence'/('portable_'+label+'.stdout')).write_text(p.stdout);(B/'evidence'/('portable_'+label+'.stderr')).write_text(p.stderr)
 result=json.loads(p.stdout) if p.returncode==0 else None
 records.append(dict(label=label,utc=start,command=cmd,env2=env2,returncode=p.returncode,elapsed_seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stderr=p.stderr,result=result))
 print(label,p.returncode,p.stderr[-120:].strip(),flush=True);return p
for label,opts,env2 in [('normal',(),False),('O',('-O',),False),('OO',('-OO',),False),('env2',(),True)]:
 require(run(label,ORIG,opts,env2=env2).returncode==0,'positive portability failed')
for label,extra in [('postcopy',('--test-corrupt-copy',)),('false_assert',('--test-false-assert',)),('child_O',('--worker-optimize','1')),('child_OO',('--worker-optimize','2'))]:
 p=run(label,ORIG,extra=extra);require(p.returncode!=0,'control accepted')
 if label=='postcopy':require('copied bytes authentication' in p.stderr and 'worker execution' not in p.stderr,'wrong stage')
 if label=='false_assert':require('Intentional worker assertion control' in p.stderr and '"optimize": 0' in p.stderr,'assert disabled')
 if label.startswith('child_'):require('unsafe worker mode' in p.stderr and '"optimize": '+('2' if label=='child_OO' else '1') in p.stderr,'actual child mode missing')
for case in ['missing','extra','empty','fifo','symlink','ancestor_symlink','nan','boolean','int_to_float','worker_tamper','comparator_tamper']:
 packet=TMP/('case_'+case);shutil.copytree(ORIG,packet);worker=W;comparator=C
 if case=='missing':(packet/'public/README.md').unlink()
 elif case=='extra':(packet/'extra.txt').write_text('extra')
 elif case=='empty':(packet/'extra_dir').mkdir()
 elif case=='fifo':os.mkfifo(packet/'fifo')
 elif case=='symlink':
  p=packet/'public/PROOF.md';p.unlink();p.symlink_to(ORIG/'public/PROOF.md')
 elif case=='ancestor_symlink':
  parent=TMP/'linked_ancestor';parent.symlink_to(TMP,target_is_directory=True);packet=parent/packet.name
 elif case in ('nan','boolean','int_to_float'):
  p=packet/'public/VERIFICATION.json';d=json.loads(p.read_text());d['exact_residuals_checked']={'nan':float('nan'),'boolean':True,'int_to_float':26.0}[case];p.write_text(json.dumps(d))
 elif case=='worker_tamper':worker=TMP/'tampered_worker.py';worker.write_bytes(b'raise RuntimeError("must never execute")\n'+W.read_bytes())
 elif case=='comparator_tamper':comparator=TMP/'tampered_comparator.py';comparator.write_bytes(b'raise RuntimeError("must never execute")\n'+C.read_bytes())
 p=run(case,packet,worker=worker,comparator=comparator);require(p.returncode!=0,'bad source accepted');require('worker execution' not in p.stderr,'source control reached execution')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',pins=pins,positive_modes=4,negative_controls=len(records)-4,records=records,limits='Environment2 positive gate uses -I and thus ignores inherited optimization; actual worker flags0 are recorded. Genuinely inherited assertion behavior is separately captured in TRUST_BOUNDARY.json. No OS sandbox or fully adversarial same-user filesystem/runtime guarantee.')
(B/'evidence/PORTABLE_GATE_TESTS.json').write_text(json.dumps(result,indent=2)+'\n')
