#!/usr/bin/env python3
"""Unmodified isolated mathematical helpers; no historical assessment wrapper."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
import sympy,mpmath
HERE=Path(__file__).resolve().parent
PKG=HERE.parent.parent/'sources/published-source/critical_wave_verification'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_hashes():return {str(p.relative_to(PKG)):sha(p) for p in sorted(PKG.rglob('*')) if p.is_file()}
def main():
 start=datetime.now(timezone.utc).isoformat();before=source_hashes()
 assert before==json.loads((HERE/'initial-source-hashes.json').read_text())
 jobs=[('author3937','verify_algebra.py'),('original_independent1385','independent_check.py'),('source17','controls.py'),('variational215','independent_variational_checks.py'),('addendum21','checks.py')]
 env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONOPTIMIZE',None)
 with tempfile.TemporaryDirectory(prefix='critical-wave-replay-') as tmp:
  work=Path(tmp)
  for name,_ in jobs:shutil.copytree(PKG/'checks'/name,work/name)
  def run(job):
   name,filename=job;script=work/name/filename;begin=datetime.now(timezone.utc).isoformat()
   r=subprocess.run([sys.executable,'-B',str(script)],cwd=script.parent,env=env,capture_output=True,timeout=180)
   (HERE/f'replay-{name}.stdout.txt').write_bytes(r.stdout)
   (HERE/f'replay-{name}.stderr.txt').write_bytes(r.stderr)
   assert r.returncode==0,(name,r.stderr.decode())
   actual=json.loads(r.stdout);expected=json.loads((PKG/'checks'/name/'REFERENCE_EXPECTED.json').read_text())
   # Timestamps are historical/run metadata, not mathematical output.
   excluded=['utc'] if 'utc' in expected else []
   norm=lambda d:{k:v for k,v in d.items() if k not in excluded}
   assert norm(actual)==norm(expected),(name,actual,expected)
   return {'name':name,'script':str(Path('checks')/name/filename),'script_sha256':sha(script),'expected':str(Path('checks')/name/'REFERENCE_EXPECTED.json'),'expected_sha256':sha(PKG/'checks'/name/'REFERENCE_EXPECTED.json'),'exit_code':r.returncode,'assertions':actual.get('assertions',actual.get('exact_assertions')),'exact_json_match_except':excluded,'all_mathematical_fields_exact_match':True,'started_utc':begin,'finished_utc':datetime.now(timezone.utc).isoformat()}
  with ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(run,jobs))
 assert source_hashes()==before
 out={'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'runs':results,'total_submitted_assertions':sum(r['assertions'] for r in results),'all_113_sources_unchanged':True,'source_sha256':before,'full_package_replay_claimed':False,'scope':'Five selected unmodified mathematical controls only, in temporary isolated copies; UTC excluded only where emitted dynamically. No opinion/priority wrapper or PDE simulation.'}
 (HERE/'replay-results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'},indent=2))
if __name__=='__main__':main()
