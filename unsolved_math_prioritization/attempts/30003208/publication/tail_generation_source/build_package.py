# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Rebuild the frozen-PDF source ZIP and upload kit locally. No network/operations."""
from pathlib import Path
import argparse,subprocess,sys,json,zipfile,hashlib
P=Path(__file__).resolve().parent
def zipmake(path,members):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(members):
   info=zipfile.ZipInfo(name,date_time=(2026,10,22,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
def main():
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);out=Path(a.parse_args().output).resolve()
 if out==P or P in out.parents:raise RuntimeError('output must be outside immutable scientific source folder')
 r=subprocess.run([sys.executable,'-B',str(P/'reproduce.py')],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 out.mkdir(parents=True,exist_ok=True)
 pdf=(P/'paper.pdf').read_bytes();(out/'tail-generation.pdf').write_bytes(pdf)
 zipname='tail-generation-source-and-verification.zip'
 zipmake(out/zipname,[('tail_generation_source/'+p.relative_to(P).as_posix(),p.read_bytes()) for p in P.rglob('*') if p.is_file()])
 for name in ['zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt']:(out/name).write_bytes((P/name).read_bytes())
 zipmake(out/'tail-generation-upload-kit.zip',[('tail-generation.pdf',pdf),(zipname,(out/zipname).read_bytes()),('zenodo-metadata.json',(P/'zenodo-metadata.json').read_bytes()),('zenodo-deposit.json',(P/'zenodo-deposit.json').read_bytes()),('README.txt',(P/'UPLOAD_README.txt').read_bytes())])
 files=[out/n for n in ['tail-generation.pdf',zipname,'tail-generation-upload-kit.zip','zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt']]
 print(json.dumps({'status':'PASS','frozen_pdf_recompiled':False,'network_used':False,'publication_performed':False,'files':[{'name':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]},sort_keys=True,indent=2))
if __name__=='__main__':main()
