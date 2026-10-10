#!/usr/bin/env python3
"""Optional source and hardening controls using caller-supplied original bytes."""
import argparse,hashlib,json,subprocess,sys,tempfile,shutil
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--author-root',required=True,type=Path)
parser.add_argument('--pdf-dir',required=True,type=Path)
parser.add_argument('--corpus-dir',required=True,type=Path)
args=parser.parse_args()
base=args.author_root.resolve();pdf=args.pdf_dir.resolve();corpus=args.corpus_dir.resolve();out=[]
source=Path(__file__).resolve().parent/'verify_sources.py'
if hashlib.sha256((base/'MANIFEST.json').read_bytes()).hexdigest()!='7cec8ef8716ab0e930d6c03f2cd4d8559214d9329ccde8ef258cd9a8d3c7ae55':raise RuntimeError('unrecognized author manifest')
if hashlib.sha256((base/'verify_packet.py').read_bytes()).hexdigest()!='629cc9238c6c8ec49257c8f42fcdc0946f9561978a4ebbe2c9b9a3149b651884':raise RuntimeError('unrecognized author verifier')
for mode in range(3):
 flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
 def run(command):return subprocess.run([sys.executable,*flags,'-I','-B',*map(str,command)],capture_output=True,timeout=90)
 a=run([source]);
 if a.returncode or json.loads(a.stdout)['status']!='NOT_RUN':raise RuntimeError('absent sources must not imply PASS')
 b=run([source,'--pdf-dir',pdf,'--corpus-dir',corpus]);
 if b.returncode or json.loads(b.stdout)['status']!='PASS_REQUESTED_CHECKS':raise RuntimeError('requested sources did not pass')
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);src=td/'sources';src.mkdir()
  tests=[]
  for name in ['missing_pdf','truncated_pdf','same_size_corrupt_pdf','symlink_pdf','missing_corpus']:
   f=src/'OWR_2016_14.pdf'
   if f.exists() or f.is_symlink(): f.unlink()
   if name=='truncated_pdf':f.write_bytes(b'%PDF')
   elif name=='same_size_corrupt_pdf':
    raw=(pdf/'OWR_2016_14.pdf').read_bytes();f.write_bytes(bytes([raw[0]^1])+raw[1:])
   elif name=='symlink_pdf':f.symlink_to(pdf/'OWR_2016_14.pdf')
   r=run([source,'--corpus-dir' if name=='missing_corpus' else '--pdf-dir',src])
   if r.returncode!=1 or not r.stderr.startswith(b'REJECT:'):raise RuntimeError('source did not fail closed '+name)
   tests.append(name)
  patched=td/'verify_packet.py';old=(base/'verify_packet.py').read_text();new=old.replace('KeyError,TypeError,subprocess.SubprocessError','KeyError,TypeError,SyntaxError,subprocess.SubprocessError')
  if new==old:raise RuntimeError('patch did not apply')
  patched.write_text(new)
  r=run([patched,'--root',base,'--manifest-sha256','7cec8ef8716ab0e930d6c03f2cd4d8559214d9329ccde8ef258cd9a8d3c7ae55'])
  if r.returncode:raise RuntimeError('patched clean packet failed')
  packet=td/'packet';shutil.copytree(base,packet);item=packet/'check_math.py';item.write_text(item.read_text()+'\ndef invalid syntax\n')
  manifest=json.loads((packet/'MANIFEST.json').read_text())
  for row in manifest['files']:
   if row['path']==item.name:row['bytes']=item.stat().st_size;row['sha256']=hashlib.sha256(item.read_bytes()).hexdigest()
  path=packet/'MANIFEST.json';path.write_text(json.dumps(manifest));pin=hashlib.sha256(path.read_bytes()).hexdigest()
  r=run([patched,'--root',packet,'--manifest-sha256',pin])
  if r.returncode!=1 or not r.stderr.startswith(b'REJECT:'):raise RuntimeError('patched syntax rejection failed')
  out.append({'optimization':mode,'omitted_sources':'NOT_RUN','requested_source_checks':'PASS','source_negative_controls':tests,'optional_hardening_clean_replay':'PASS','optional_hardening_syntax_reject':'REJECT with exit 1'})
print(json.dumps({'status':'PASS','runs':out,'originals_modified':False},indent=2))
