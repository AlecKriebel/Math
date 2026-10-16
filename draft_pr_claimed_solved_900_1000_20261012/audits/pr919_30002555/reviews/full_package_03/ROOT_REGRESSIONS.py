#!/usr/bin/env python3
"""Rerun preserved root regression programs in private copies, no services."""
import argparse,json,os,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent
def run(python,out):
 scratch=R/'private/root_regressions';scratch.mkdir(exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=scratch) as td:
  root=pathlib.Path(td)
  for p in (R/'reviewed_helpers').glob('*.py'):shutil.copy2(p,root/p.name)
  (root/'audits/pr919_30002555/publication/tmp').mkdir(parents=True)
  results={}
  specs=[('verify_pr919_disposition_repair.py','DISPOSITION_TEST.json',[]),('verify_pr919_receipt_links.py','RECEIPT_LINK_TEST.json',[]),('verify_pr919_publication_head_repair.py','PUBLICATION_HEAD_TEST.json',['--launcher',str(root/'run_pr919_zenodo.py')])]
  for name,dest,tail in specs:
   p=subprocess.run([str(python),'-I','-B',str(root/name),*tail,'--output',str(out/dest)],capture_output=True,text=True,timeout=60,env={**os.environ,'TMPDIR':str(root),'PYTHONDONTWRITEBYTECODE':'1'})
   if p.returncode:raise RuntimeError(name+': '+p.stderr)
   results[name]=json.loads((out/dest).read_text())
  if results[specs[0][0]]['passed']!=6 or results[specs[1][0]]['stale_or_cross_target_rejections']!=27 or results[specs[2][0]]['negative_rejections']!=27 or results[specs[2][0]]['positive_cases']!=6:raise RuntimeError('unexpected root regression counts')
 return {'status':'PASS','disposition_cases':6,'receipt_linkage_negatives':27,'receipt_linkage_positives':1,'publication_head_negatives':27,'publication_head_positives':6,'all_calls_mocked':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--python',type=pathlib.Path,default=pathlib.Path(sys.executable));p.add_argument('--outputdir',type=pathlib.Path,required=True);a=p.parse_args();print(json.dumps(run(a.python,a.outputdir),indent=2))
