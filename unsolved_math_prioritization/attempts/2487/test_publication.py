#!/usr/bin/env python3
"""Relocation and fail-closed controls in temporary directories; no network."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path

def need(v,s):
 if not v:raise ValueError(s)
def run(cmd,ok):
 r=subprocess.run(cmd,capture_output=True);need((r.returncode==0)==ok,'unexpected process result');return r

def main(a):
 root=Path(__file__).resolve().parent;py=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else []);checks=[]
 with tempfile.TemporaryDirectory(prefix='progression-differences-controls-') as t:
  t=Path(t);dst=t/'relocated';shutil.copytree(root,dst);cmd=py+[str(dst/'verify_publication.py')];extra=[];external=[a.catalog,a.problems,a.reports,a.pdf_directory];need(not any(external) or all(external),'all external inputs required')
  if all(external):
   for k,v in zip(('catalog','problems','reports','pdf-directory'),external):extra+=['--'+k,str(Path(v).resolve())]
  run(cmd+extra,True);checks.append('relocated_publication_valid')
  cases=[('archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_SAFE_FREEZE.zip','author_archive_corruption'),('archives/DISTINCT_PROGRESSION_DIFFS_2487_INDEPENDENT_AUDIT_SAFE.zip','audit_archive_corruption'),('archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_EXTERNAL_MANIFEST.json','author_manifest_corruption'),('independent_audit/ACCEPTANCE.json','exact_acceptance_corruption'),('author_original/PROOF.md','loose_proof_corruption'),('PUBLICATION_METADATA.json','publication_scope_corruption')]
  for rel,label in cases:
   f=dst/rel;b=f.read_bytes();c=bytearray(b);c[len(c)//2]^=1;f.write_bytes(c);run(cmd,False);f.write_bytes(b);checks.append(label+'_rejected')
  f=dst/'unexpected.txt';f.write_text('unexpected');run(cmd,False);f.unlink();checks.append('extra_file_rejected')
  if all(external):
   audit=py+[str(dst/'independent_audit/verify_audit.py'),'--author-archive',str(dst/'archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_SAFE_FREEZE.zip'),'--author-manifest',str(dst/'archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_EXTERNAL_MANIFEST.json')]+extra
   for flag,rel in [('--author-archive','archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_SAFE_FREEZE.zip'),('--author-manifest','archives/DISTINCT_PROGRESSION_DIFFS_2487_AUTHOR_EXTERNAL_MANIFEST.json')]:
    f=dst/rel;b=f.read_bytes();f.write_bytes(b+b' ');run(audit,False);f.write_bytes(b);checks.append('frozen_audit_'+flag[2:]+'_corruption_rejected')
   for flag,src in [('--catalog',a.catalog),('--problems',a.problems),('--reports',a.reports)]:
    f=t/'corrupted-input';b=bytearray(Path(src).read_bytes());b[len(b)//2]^=1;f.write_bytes(b);bad=audit[:];bad[bad.index(flag)+1]=str(f);run(bad,False);f.unlink();checks.append('frozen_audit_'+flag[2:]+'_corruption_rejected')
   pdf=t/'pdfs';pdf.mkdir()
   for f in Path(a.pdf_directory).glob('*.pdf'):shutil.copyfile(f,pdf/f.name)
   f=pdf/'lemm.pdf';b=bytearray(f.read_bytes());b[len(b)//2]^=1;f.write_bytes(b);bad=audit[:];bad[bad.index('--pdf-directory')+1]=str(pdf);run(bad,False);checks.append('frozen_audit_source_pdf_corruption_rejected')
  run(cmd+extra,True);checks.append('restored_relocated_publication_valid')
 return dict(status='PASS',optimization_level=sys.flags.optimize,checks=checks,external_corruption_controls_performed=all(external),formal_proof_verification=False)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('catalog','problems','reports','pdf-directory'):p.add_argument('--'+n)
 print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))
