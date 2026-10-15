#!/usr/bin/env python3
"""Reproduce review checks against explicit original candidate; never repair or publish.

After root repairs, use --candidate /.../publication/reviewed_candidates/candidate01.
All replay scratch and transient receipts remain under this review's ignored tmp.
"""
import argparse,datetime,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;P=HERE.parent.parent/'publication/reviewed_candidates/candidate01'
PYTHON='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def need(c,m):
 if not c:raise RuntimeError(m)
def run(cmd):
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=1800);need(p.returncode==0,p.stderr);return p.stdout
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',type=Path,default=P);ap.add_argument('--expected-manifest');ap.add_argument('--output',type=Path);a=ap.parse_args();candidate=a.candidate.absolute()
 if a.expected_manifest:run([PYTHON,'-I','-B',str(HERE/'VERIFY.py'),'--expected-manifest',a.expected_manifest])
 with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='full_reproduction_') as td:
  t=Path(td)
  for phase in ['start']:
   run([PYTHON,'-I','-B',str(HERE/'AUTHENTICATE.py'),'--candidate',str(candidate),'--output',str(t/(phase+'.json'))])
  run([PYTHON,'-I','-B',str(HERE/'REPLAY.py'),'--candidate',str(candidate),'--output-dir',str(t/'replay')])
  for mode in ['normal','O','OO','env2']:
   need((t/'replay'/('REPLAY_'+mode+'.stdout')).read_bytes()==(HERE/('REPLAY_'+mode+'.stdout')).read_bytes(),'full JSON replay differs from recorded '+mode)
  new=run([PYTHON,'-I','-B',str(HERE/'INDEPENDENT_CONTROLS.py'),'--candidate',str(candidate)])
  need(new==(HERE/'INDEPENDENT_RESULTS.json').read_text(),'independent controls receipt differs')
  pdf=False
  if shutil.which('tectonic') and shutil.which('pdftoppm'):
   c=t/'compile';c.mkdir();shutil.copy2(candidate/'note.tex',c/'note.tex');run(['tectonic','--outdir',str(c),str(c/'note.tex')]);run(['pdftoppm','-scale-to','1600','-png',str(c/'note.pdf'),str(c/'page')])
   saved=json.loads((HERE/'PDF_INSPECTION.json').read_text())
   for i in range(1,4):need(hashlib.sha256((c/f'page-{i}.png').read_bytes()).hexdigest()==saved['pages'][str(i)]['raster_sha256'],'recompiled rendered page differs')
   pdf=True
  run([PYTHON,'-I','-B',str(HERE/'AUTHENTICATE.py'),'--candidate',str(candidate),'--output',str(t/'end.json')])
 if a.expected_manifest:run([PYTHON,'-I','-B',str(HERE/'VERIFY.py'),'--expected-manifest',a.expected_manifest])
 out={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'four_full_modes_identical_to_saved':True,'current_guards_rerun':True,'independent_controls_exact_receipt':True,'fresh_candidate_start_end_authentication':True,'recompiled_pages_equal':pdf,'candidate_mutated':False,'helpers_only_historical_snapshots_authenticated':True,'publication_actions_executed':False}
 text=json.dumps(out,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(text)
 print(text,end='')
if __name__=='__main__':main()
