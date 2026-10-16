#!/usr/bin/env python3
"""Meaningful failure controls for this publication wrapper, in temporary copies."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(ok,message):
 if not ok:raise RuntimeError(message)
def main():
 archive=HERE/'robinson-tangency-source-verification-v1.0.zip'; results=[]
 with tempfile.TemporaryDirectory(prefix='robinson-guard-controls-') as td:
  base=Path(td)/'base';base.mkdir()
  with zipfile.ZipFile(archive) as z:z.extractall(base)
  anchor=hashlib.sha256((base/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest()
  pdf=HERE/'output/pdf/note.pdf'
  cases=['changed_note','missing_checker','unlisted_empty','listed_symlink','unlisted_directory_symlink','FIFO','identity_change','changed_original_proof_rehashed','changed_original_manifest_rehashed','manifest_anchor_change','wrong_PDF']
  for optimized in (False,True):
   p=subprocess.run([sys.executable,*(['-O'] if optimized else []),str(base/'verify_package.py'),'--integrity-only','--expected-manifest',anchor,'--pdf',str(pdf)],capture_output=True,text=True)
   require(p.returncode==0,'Baseline rejected: '+p.stderr)
   for name in cases:
    root=Path(td)/(name+str(optimized));shutil.copytree(base,root);pin=anchor;args=[]
    if name=='changed_note':(root/'note.tex').write_bytes((root/'note.tex').read_bytes()+b'\n')
    elif name=='missing_checker':(root/'reviews/proof_family/check_exact.py').unlink()
    elif name=='unlisted_empty':(root/'.unlisted').touch()
    elif name=='listed_symlink':
     f=root/'note.tex';f.unlink();f.symlink_to(base/'note.tex')
    elif name=='unlisted_directory_symlink':(root/'unlisted_dir').symlink_to(base,target_is_directory=True)
    elif name=='FIFO':os.mkfifo(root/'unlisted_FIFO')
    elif name in ['identity_change','changed_original_proof_rehashed','changed_original_manifest_rehashed']:
     f=root/'PACKAGE_MANIFEST.json';m=json.loads(f.read_text())
     if name=='identity_change':m['problem_id']=30000718
     else:
      target='original_packet/author/PROOF.md' if 'proof' in name else 'original_packet/PUBLIC_MANIFEST.json';q=root/target;q.write_bytes(q.read_bytes()+b'\n');m['files'][target]={'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
     f.write_text(json.dumps(m));pin=hashlib.sha256(f.read_bytes()).hexdigest()
    elif name=='manifest_anchor_change':(root/'PACKAGE_MANIFEST.json').write_bytes((root/'PACKAGE_MANIFEST.json').read_bytes()+b'\n')
    elif name=='wrong_PDF':
     q=Path(td)/'wrong.pdf';q.write_bytes(pdf.read_bytes()+b'\n');args=['--pdf',str(q)]
    p=subprocess.run([sys.executable,*(['-O'] if optimized else []),str(root/'verify_package.py'),'--integrity-only','--expected-manifest',pin,*args],capture_output=True,text=True,timeout=30)
    require(p.returncode!=0,'False PASS: '+name)
    results.append({'case':name,'optimized':optimized,'rejected':True,'diagnostic':p.stderr.strip()})
 out={'status':'PASS','cases':results,'rejected_cases':len(results),'normal_and_optimized_baselines':'PASS','scope':'Outer wrapper integrity, fixed anchors and special-entry guards; not proof truth certification.'}
 (HERE/'PACKAGE_GUARD_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','rejected_cases':len(results)},indent=2))
if __name__=='__main__':main()
