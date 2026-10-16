"""Portable finite controls. No network, installs, or package-input writes."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def require(cond,detail):
 if not cond:raise RuntimeError(detail)
def integrity():
 j=json.loads((ROOT/'MANIFEST.json').read_bytes())
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
 require(actual==set(j['files'])|{'MANIFEST.json'},'Unexpected/missing material path')
 for n,x in j['files'].items():
  p=ROOT/n;require(not p.is_symlink(),'Symlink '+n);b=p.read_bytes()
  require({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==x,'Hash mismatch '+n)
 return len(j['files'])
def child(script,args=(),expected_fail=False):
 argv=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(script)]+list(args)
 r=subprocess.run(argv,text=True,capture_output=True,cwd=script.parent)
 if expected_fail:
  require(r.returncode!=0 and 'exact_product' in r.stderr,'False coefficient was not rejected by exact identity')
 else:require(r.returncode==0,'Child failed: '+r.stderr)
 return {'command':[Path(argv[0]).name]+argv[1:],'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--full-physical',action='store_true');ap.add_argument('--legacy-replay',action='store_true');ap.add_argument('--guard-false',action='store_true');args=ap.parse_args()
 require(not args.guard_false,'DELIBERATE FALSE CONDITION')
 n=integrity()
 import sympy,mpmath
 require(sympy.__version__=='1.14.0' and mpmath.__version__=='1.3.0','Use pinned dependency versions')
 reports=[]
 with tempfile.TemporaryDirectory(prefix='pedal-verification-') as tmp:
  d=Path(tmp)
  for name in ['verify_exact_controls.py','physical_audit.py','signed_edge_checks.py']:shutil.copyfile(ROOT/'verification'/name,d/name)
  reports.append(child(d/'verify_exact_controls.py'))
  result=json.loads((d/('CHECK_RESULTS_OPT.json' if sys.flags.optimize else 'CHECK_RESULTS.json')).read_bytes())
  require(result['status']=='PASS' and result['checks']==282,'Exact control count mismatch')
  reports.append(child(d/'physical_audit.py',['--exact-only','--out','exact.json']))
  result=json.loads((d/'exact.json').read_bytes())
  require(sum(result['counts'].values())==7 and not result['cases'],'Exact N4 count mismatch')
  reports.append(child(d/'physical_audit.py',['--exact-only','--mutate-coefficient','--out','false.json'],True))
  require(not (d/'false.json').exists(),'False identity wrote successful output')
  if args.full_physical:
   reports.append(child(d/'physical_audit.py',['--out','full.json']))
   full=json.loads((d/'full.json').read_bytes())
   require(sum(full['counts'].values())==107962 and len(full['cases'])==39,'Physical sweep scope mismatch')
   reports.append(child(d/'signed_edge_checks.py'))
  if args.legacy_replay:
   require(not sys.flags.optimize,'Legacy -O is not validation; see archived enforcement probes')
   old=d/'legacy';shutil.copytree(ROOT/'audit/original_submitted_head',old)
   for rel in ['verification.json','independent_review/independent_receipt.json']:(old/rel).chmod(0o644)
   for script,receipt in [('verify.py','verification.json'),('independent_review/independent_checks.py','independent_review/independent_receipt.json')]:
    reports.append(child(old/script));expected=(ROOT/'audit/original_submitted_head'/receipt).read_bytes()
    require(reports[-1]['stdout'].encode()==expected and (old/receipt).read_bytes()==expected,'Legacy ordinary receipt differs')
 print(json.dumps({'status':'PASS','material_manifest_files':n,'python':sys.version,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'optimization':sys.flags.optimize,'scope':'282 exact geometry controls +7 symbolic N4 controls + actual false-coefficient rejection; optional finite noninterval diagnostics/ordinary legacy replay','reports':reports},indent=2))
if __name__=='__main__':main()
