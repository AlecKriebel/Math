#!/usr/bin/env python3
"""Run saved exact validators in isolated temporary copies, never LP discovery.
The package is not changed. Optionally write a report to --report PATH.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,time
from importlib.metadata import version
ROOT=Path(__file__).resolve().parent
TASKS=[
 ('counterexample',['checks/verify_counterexample.py'],'checks/counterexample_verified.json'),
 ('sparse_discontinuous',['checks/verify_discontinuous_reduction.py','--saved'],None),
 ('fourfold_refinements',['checks/verify_fourfold_refinements.py'],'checks/fourfold_refinement_results.json'),
 ('signed_orbit_pipeline',['checks/verify_orbit_pipeline.py'],'checks/orbit_pipeline_results.json'),
 ('independent_signed_reconstruction',['checks/audit_signed_reconstruction.py'],'checks/audit_signed_reconstruction.json'),
 ('covered_nonextreme',['checks/verify_covered_nonextreme.py'],None),
 ('independent_local_factorization',['fresh_audit/test_local_factorization.py'],'fresh_audit/test_local_factorization.json'),
 ('independent_compressed_decision',['fresh_audit/test_compressed_decision.py'],'fresh_audit/test_compressed_decision.json'),
]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sys.flags.optimize:
  raise SystemExit('Run without Python optimization: the exact validators require active assertions.')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
 results=[]
 with tempfile.TemporaryDirectory(prefix='extremality-replay-') as tmp:
  copy=Path(tmp)/'package';shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  for name,cmd,out in TASKS:
   start=time.monotonic();r=subprocess.run([sys.executable,*cmd],cwd=copy,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   item={'check':name,'command':['python',*cmd],'exit_code':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL','stdout':r.stdout,'stderr':r.stderr}
   if out and r.returncode==0:
    item['frozen_result']=out;item['frozen_sha256']=digest(ROOT/out);item['replayed_sha256']=digest(copy/out)
    item['frozen_byte_match']=item['frozen_sha256']==item['replayed_sha256']
    # A byte mismatch is a failure, even if JSON values happen to agree.
    if not item['frozen_byte_match']:item['status']='FAIL'
   item['elapsed_seconds']=round(time.monotonic()-start,3);results.append(item)
   print(name,item['status'],flush=True)
   if item['status']!='PASS':print(r.stdout,r.stderr,flush=True)
 report={'status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','mode':'saved exact rational replay; no LP discovery','python_version':sys.version.split()[0],'dependencies':{x:version(x) for x in ('sympy','numpy','scipy')},'checks':results,'scope':'Dense finite validators and independent algebra checks, not a compressed AHT implementation or an asymptotic runtime benchmark. The legacy 70-case continuous LP discovery run is not replayed here because its individual rational input values were not stored.'}
 if args.report:
  args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
 print('OVERALL',report['status']);return report['status']!='PASS'
if __name__=='__main__':raise SystemExit(main())
