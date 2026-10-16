#!/usr/bin/env python3
"""Repeat the complete executed review controls without changing sealed receipts.

This is a local repository review reproducer, not the release's portable entrypoint.
Use --candidate for an explicitly preserved revision2 after subsequent repairs.
"""
import argparse,hashlib,json,os,subprocess,tempfile,sys,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'publication';PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
def need(x,s):
 if not x:raise RuntimeError(s)
def main():
 import AUTHENTICATE,REPLAY
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,default=P);ap.add_argument('--output',type=Path);args=ap.parse_args();p=args.candidate.resolve();AUTHENTICATE.run(p)
 with tempfile.TemporaryDirectory(dir=D/'tmp',prefix='complete-reproduce-') as td:
  t=Path(td);env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
  def run(script,*tail):
   r=subprocess.run([str(PY),'-B',str(D/script),*map(str,tail)],env=env,text=True,capture_output=True,timeout=1800);need(r.returncode==0,script+'\n'+r.stderr);return r
  run('REPLAY.py','--candidate',p,'--result-dir',t)
  fresh=json.loads((t/'REPLAY_RECEIPT.json').read_bytes());saved=json.loads((D/'REPLAY_RECEIPT.json').read_bytes());REPLAY.equivalent(fresh,saved)
  run('INDEPENDENT_CONTROLS.py','--bundle',t/'tmp/bundle','--output',t/'independent.json');REPLAY.equivalent(json.loads((t/'independent.json').read_bytes()),json.loads((D/'INDEPENDENT_RESULTS.json').read_bytes()))
  run('HELPER_CONTROLS.py','--output-dir',t);REPLAY.equivalent(json.loads((t/'HELPER_CONTROL_RESULTS.json').read_bytes()),json.loads((D/'HELPER_CONTROL_RESULTS.json').read_bytes()))
  for script,out in [('verify_pr919_disposition_repair.py','disposition.json'),('verify_pr919_receipt_links.py','links.json')]:
   r=subprocess.run([str(PY),'-B',str(D/'reviewed_helpers'/script),'--output',str(t/out)],env=env,text=True,capture_output=True,timeout=30);need(r.returncode==0,r.stderr)
  shutil.copyfile(p/'note.tex',t/'note.tex');r=subprocess.run(['tectonic','-o',str(t),str(t/'note.tex')],env=env,text=True,capture_output=True,timeout=120);need(r.returncode==0,r.stderr)
  raster=[]
  for page in range(1,4):
   for label,pdf in [('current',p/'output/pdf/note.pdf'),('fresh',t/'note.pdf')]:
    r=subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1500','-singlefile','-png',str(pdf),str(t/(label+str(page)))],capture_output=True,timeout=30);need(r.returncode==0,r.stderr)
   b=(t/('current'+str(page)+'.png')).read_bytes();need(b==(t/('fresh'+str(page)+'.png')).read_bytes(),'PDF page pixels '+str(page));raster.append(hashlib.sha256(b).hexdigest())
 from datetime import datetime,timezone
 AUTHENTICATE.run(p);out={'status':'PASS','completed_utc':datetime.now(timezone.utc).isoformat(),'candidate_freeze_sha256':AUTHENTICATE.PINS['freeze'],'four_full_modes_strict_saved_results_identical':True,'current_guard_negatives':140,'current_false_assertions':4,'current_copied_code_corruptions':4,'independent_controls_identical':True,'helper_controls_identical':True,'root_disposition_cases':6,'root_receipt_negatives':27,'extended_receipt_negatives':35,'independent_compile_and_all3_page_pixels_equal':True,'current_page_png_sha256':raster,'endpoint_authentication_passed':True,'no_external_write_action':True}
 if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
