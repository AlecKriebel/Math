#!/usr/bin/env python3
"""Clean, pinned reproduction; no writes to the supplied upstream clone."""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
PIN='adc7f1241b42e322a6451854ab7e4b4c146bf78a'
MAIN='Universal-optimality-of-the-triangular-lattice-September-23-2026'
ATOMIC='An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,cwd,env=None):
 t=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
 if r.returncode:raise RuntimeError(json.dumps({'command':list(map(str,cmd)),'returncode':r.returncode,'stdout':r.stdout[-4000:],'stderr':r.stderr[-4000:]}))
 return {'command':list(map(str,cmd)),'returncode':r.returncode,'elapsed_seconds':time.monotonic()-t,'stdout_tail':r.stdout[-1000:],'stderr_tail':r.stderr[-1000:]}
def main():
 a=argparse.ArgumentParser();a.add_argument('--upstream',type=Path,required=True);a.add_argument('--run-upstream',action='store_true');a.add_argument('--receipt',type=Path,required=True);a.add_argument('--tectonic',default='tectonic');args=a.parse_args()
 upstream=args.upstream.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip()==PIN,'wrong upstream HEAD'
 manifest=json.loads((ROOT/'sources/UPSTREAM_MANIFEST.json').read_text())
 for row in manifest['files']:
  q=upstream/row['path'];assert q.is_file() and q.stat().st_size==row['bytes'] and digest(q)==row['sha256'],row['path']
 r={'python':sys.version,'platform':platform.platform(),'source_pin':PIN,'upstream_hashes_checked':len(manifest['files']),'commands':[],'full_lean_build':False}
 with tempfile.TemporaryDirectory(prefix='riesz-clean-') as d:
  d=Path(d).resolve();(d/'paper').mkdir();source_bytes=(ROOT/'publication/main.tex').read_bytes();(d/'paper/main.tex').write_bytes(source_bytes)
  env=dict(os.environ,SOURCE_DATE_EPOCH='1791345600')
  r['commands'].append(run([args.tectonic,'--keep-logs','main.tex'],d/'paper',env))
  pdf=d/'paper/main.pdf';assert pdf.read_bytes().startswith(b'%PDF-')
  r['rebuilt_pdf_sha256']=digest(pdf);r['paper_source_sha256']=hashlib.sha256(source_bytes).hexdigest()
  log=(d/'paper/main.log').read_text(errors='replace')
  assert 'Overfull' not in log and 'undefined references' not in log and 'Citation `' not in log
  r['commands'].append(run(['pdfinfo',str(pdf)],d))
  if args.run_upstream:
   import flint
   assert flint.__version__=='0.9.0',flint.__version__
   r['python_flint']=flint.__version__
   for name,short in [(MAIN,'main'),(ATOMIC,'atomic')]:
    shutil.copytree(upstream/'preprints'/name,d/short)
   r['commands'].append(run([sys.executable,'-B','verification/numeric_balls.py','--output-dir',str(d/'main-results')],d/'main'))
   r['commands'].append(run([sys.executable,'-B','verification/arithmetic_bounds.py','--output-dir',str(d/'main-results')],d/'main'))
   for name in ['numeric_balls_results.json','arithmetic_bounds.json']:
    r[name]=json.loads((d/'main-results'/name).read_text())
   r['commands'].append(run([sys.executable,'-I','-B','verification/check_certificate.py'],d/'atomic'))
  r['status']='passed'
 args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'status':r['status'],'upstream_hashes_checked':r['upstream_hashes_checked'],'commands':len(r['commands']),'full_lean_build':False,'receipt':str(args.receipt)}))
if __name__=='__main__':main()
