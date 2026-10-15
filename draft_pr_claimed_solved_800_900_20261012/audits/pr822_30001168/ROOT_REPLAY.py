#!/usr/bin/env python3
"""Reproduce inspected frozen software; it does not prove analytic theorems."""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile,datetime
A=Path(__file__).resolve().parent
S=A/'source'
PROGRAM=A.parents[1]

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def bind():
 d=json.loads((A/'SOURCE_MANIFEST.json').read_bytes());expected={r['path'] for r in d['files']}
 actual={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}
 need(actual==expected,'closed frozen inventory')
 for r in d['files']:
  p=S/r['path'];b=p.read_bytes()
  need(not p.is_symlink() and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'frozen byte binding')
 return len(expected)
def semantic(x):
 if isinstance(x,dict):return {k:semantic(v) for k,v in x.items() if k!='optimized'}
 if isinstance(x,list):return [semantic(v) for v in x]
 return x

def main():
 count=bind();results={}
 with tempfile.TemporaryDirectory(dir=PROGRAM/'local_tools') as td:
  env=dict(os.environ,TMPDIR=str(Path(td).resolve()))
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   q=subprocess.run(['python3','-I','-B',*flags,str(S/'verify_publication.py')],cwd='/',env=env,capture_output=True,text=True,timeout=900)
   need(q.returncode==0 and not q.stderr,'full replay '+mode+': '+q.stderr)
   results[mode]=json.loads(q.stdout)
  q=subprocess.run(['python3','-I','-B',str(S/'package_controls.py')],cwd='/',env=env,capture_output=True,text=True,timeout=900)
  need(q.returncode==0 and not q.stderr,'outercontrols: '+q.stderr);outer=json.loads(q.stdout)
 need(semantic(results['normal'])==semantic(results['optimized']),'optimized semantic outputs differ')
 need(outer['total']==20 and outer['accepted_baselines']==2 and outer['expected_rejections']==18,'outercontrols count')
 need(bind()==count,'final frozen binding')
 out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files_bound_before_after':count,'full_replays':results,'normal_optimized_semantics_identical':True,'outer_controls':outer,'infinite_analytic_result_proven_by_program':False,'meaning':'Strict source/ZIP identity, exact rational arithmetic and negative/integrity controls; smoothness/covariance/minmax/Poisson remain mathematical review obligations.'}
 (A/'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'source_files_bound':count,'normal_optimized_semantics_identical':True,'author_arithmetic_checks':results['normal']['ordinary']['author/verify_bundle.py']['arithmetic_checks'],'audit_controls':results['normal']['audit_controls'],'outer_controls':outer['total'],'second_review_math_controls_each_mode':results['normal']['ordinary']['second_review/verify_review.py']['mathematical_negative_controls_rejected']}))
if __name__=='__main__':main()
