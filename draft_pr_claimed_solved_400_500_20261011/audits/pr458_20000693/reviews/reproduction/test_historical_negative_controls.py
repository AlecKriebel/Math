#!/usr/bin/env python3
"""Run deliberately invalid isolated historical packets in real subprocesses."""
import concurrent.futures, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FROZEN=ROOT.parents[1]/'source_snapshot/unsolved_math_prioritization/attempts/20000693'
PRIVATE=ROOT/'private_cases/negative_controls'
PRIVATE.mkdir(parents=True,exist_ok=True)
AUTHOR=[
 ('author_wrong_deletion_ratio', "assert s.simplify((one/two).subs(x,s.Rational(1,2)))==s.Rational(1,6);checks+=1", "assert s.simplify((one/two).subs(x,s.Rational(1,2)))==s.Rational(1,5);checks+=1"),
 ('author_missing_modulus_lift_restoration', "lifted += [(primitive(n,p),a) for n,q,a in rows if Q%p==0 and q%p!=0]", "lifted += []"),
 ('author_wrong_primitive_aggregation', "assert sum(v*v for v in groups(CASES[0]).values())==4;checks+=1", "assert sum(v*v for v in groups(CASES[0]).values())==2;checks+=1"),
 ('author_conjugate_class_collision', "assert sum(v*v for v in groups(CASES[2]).values())==2;checks+=1", "assert sum(v*v for v in groups(CASES[2]).values())==4;checks+=1"),
]
REVIEWER=[
 ('reviewer_wrong_deletion_ratio', "assert (J1/J2).subs(x,s.Rational(1,2)) == s.Rational(1,6)", "assert (J1/J2).subs(x,s.Rational(1,2)) == s.Rational(1,5)"),
 ('reviewer_wrong_CUE_constant', "mp.mpf(1)/12) < mp.mpf('1e-60')", "mp.mpf(1)/13) < mp.mpf('1e-60')"),
 ('reviewer_separate_local_expectations', "assert closed.subs({u:-1,x:s.Rational(1,3)}) == s.Rational(9,8)", "assert closed.subs({u:-1,x:s.Rational(1,3)}) == s.Rational(9,4)"),
 ('reviewer_missing_modulus_lift_restoration', "restored = common + [(primitive(n,p),a) for n,q,a in rows if Q % p == 0 and q % p != 0]", "restored = common"),
]
PUBLICATION=['publication_same_size_heuristic_corruption','publication_wrong_manifest_byte_count','publication_unlisted_file','publication_rehashed_theorem_claim','publication_rehashed_novelty_claim','publication_rehashed_wrong_queue_status','publication_rehashed_turn_budget','publication_rehashed_frozen_manifest','publication_forbidden_foreign_extraction','publication_expected_frozen_report_mismatch','publication_replay_generated_report_mismatch']
JOBS=[]
for case,old,new in AUTHOR:JOBS.append((case,'author/verify.py',old,new))
for case,old,new in REVIEWER:JOBS.append((case,'review/reviewer_checks.py',old,new))
for case in PUBLICATION:JOBS.append((case,'verify_publication.py',None,None))
def sha(b): return hashlib.sha256(b).hexdigest()
def run(job, optimized):
 case, script, old, new=job
 dest=PRIVATE/(case+('_optimized' if optimized else '_normal'))
 if dest.exists():shutil.rmtree(dest)
 dest.mkdir(parents=True)
 replay=case in ('publication_expected_frozen_report_mismatch','publication_replay_generated_report_mismatch')
 if old is not None:
  code=(FROZEN/script).read_text()
  if code.count(old)!=1:raise RuntimeError('mutation target not unique '+case)
  copied=dest/Path(script).name
  copied.write_text(code.replace(old,new))
 else:
  packet=dest/'packet';shutil.copytree(FROZEN,packet);copied=packet/script
  manifest_path=packet/'PUBLICATION_MANIFEST.json'
  manifest=json.loads(manifest_path.read_text())
  def rehash(name):
   b=(packet/name).read_bytes();manifest['files'][name]={'bytes':len(b),'sha256':sha(b)}
  if case=='publication_same_size_heuristic_corruption':
   f=packet/'author/HEURISTIC.md';b=f.read_bytes();f.write_bytes(bytes([b[0]^1])+b[1:])
  elif case=='publication_wrong_manifest_byte_count':manifest['files']['author/HEURISTIC.md']['bytes']+=1
  elif case=='publication_unlisted_file':(packet/'UNLISTED.txt').write_text('invented sentinel')
  elif case.startswith('publication_rehashed_') and case!='publication_rehashed_frozen_manifest':
   f=packet/'PUBLICATION_STATE.json';s=json.loads(f.read_text())
   if case.endswith('theorem_claim'):s['asymptotic_proved']=True
   elif case.endswith('novelty_claim'):s['novelty_claimed']=True
   elif case.endswith('wrong_queue_status'):s['queue_status']='unsolved'
   elif case.endswith('turn_budget'):s['author_turns_used']=6
   else:raise RuntimeError(case)
   f.write_text(json.dumps(s,indent=2)+'\n');rehash('PUBLICATION_STATE.json')
  elif case=='publication_rehashed_frozen_manifest':
   f=packet/'author/manifest.json';f.write_bytes(f.read_bytes()+b' ');rehash('author/manifest.json')
  elif case=='publication_forbidden_foreign_extraction':
   name='review/topacogullari2019.txt';(packet/name).write_text('invented fixture; no foreign source content');rehash(name)
  elif case=='publication_expected_frozen_report_mismatch':
   name='author/verification.json';f=packet/name;b=f.read_bytes();f.write_bytes(b.replace(b'\"PASS\"',b'\"FAIL\"',1));rehash(name)
  elif replay:
   # Corrupt the actual isolated subprocess-generated report after generation,
   # retaining all author/reviewer input bindings. Rehash this copied wrapper
   # in the public manifest so rejection specifically reaches byte comparison.
   name='verify_publication.py';f=packet/name;code=f.read_text()
   target='            generated = (Path(temp) / output).read_bytes()'
   replacement=("            generated_file = Path(temp) / output\n"
                "            generated_file.write_bytes(generated_file.read_bytes().replace(b'\"PASS\"', b'\"FAIL\"', 1))\n"
                "            generated = generated_file.read_bytes()")
   if code.count(target)!=1:raise RuntimeError('replay mutation not unique')
   f.write_text(code.replace(target,replacement));rehash(name)
  else:raise RuntimeError(case)
  manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 if optimized:env['PYTHONOPTIMIZE']='1'
 result=subprocess.run([sys.executable,str(copied)]+(['--replay'] if replay else []),cwd=dest,env=env,capture_output=True,timeout=240)
 rec={'case':case,'script':script,'mode':'optimized' if optimized else 'normal','inherited_PYTHONOPTIMIZE':env.get('PYTHONOPTIMIZE'),
   'returncode':result.returncode,'rejected':result.returncode!=0,'stdout_sha256':sha(result.stdout),'stdout_bytes':len(result.stdout),
   'stderr':result.stderr.decode(errors='replace'),'mutated_script_sha256':sha(copied.read_bytes())}
 if result.returncode==0:
  report=json.loads(result.stdout);rec['emitted_status']=report.get('status');rec['emitted_asymptotic_proved']=report.get('asymptotic_proved')
  if old is not None:
   expected='author/verification.json' if script.startswith('author') else 'review/REVIEWER_CHECKS.json'
   rec['stdout_exactly_original_pass_report']=result.stdout==(FROZEN/expected).read_bytes()
 else:rec['stdout']=result.stdout.decode(errors='replace')
 return rec
if '--case' in sys.argv:
 selected=sys.argv[sys.argv.index('--case')+1]
 JOBS=[job for job in JOBS if job[0]==selected]
 if len(JOBS)!=1:raise RuntimeError('unknown selected control')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 records=list(pool.map(lambda x:run(*x),[(j,o) for j in JOBS for o in (False,True)]))
report={'reviewer':'/root/pr458_reproduction','pr':458,'problem_id':'20000693','frozen_head':'87a39f7b4e5ef81aacf98464f86586cc95684d7f',
 'cases_per_mode':len(JOBS),'normal_rejected':sum(r['rejected'] for r in records if r['mode']=='normal'),
 'optimized_rejected':sum(r['rejected'] for r in records if r['mode']=='optimized'),
 'optimized_false_acceptance':sum(not r['rejected'] for r in records if r['mode']=='optimized'),
 'optimized_invalid_scripts_byte_identical_pass_reports':sum(r.get('stdout_exactly_original_pass_report',False) for r in records if r['mode']=='optimized'),
 'records':records,'actual_subprocess_execution':True,'frozen_sources_modified':False}
(ROOT/('HISTORICAL_NEGATIVE_CONTROLS_ONE_CASE.json' if '--case' in sys.argv else 'HISTORICAL_NEGATIVE_CONTROLS.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
