#!/usr/bin/env python3
"""Freeze and replay the final source-free corrected distribution."""
from pathlib import Path
import gzip,hashlib,io,json,os,tarfile,tempfile
from test_distribution import exact,remove,readonly,emit,require
BASE=Path(__file__).resolve().parent
ROOT=BASE/'corrected_distribution'
ARCHIVE=BASE/'corrected_source_free_packet.tar.gz'
PREFIX='boundary_twist_11000156_corrected'
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w',format=tarfile.PAX_FORMAT) as tf:
 for p in [ROOT,*sorted(ROOT.rglob('*'))]:
  name=PREFIX+('/'+str(p.relative_to(ROOT)) if p!=ROOT else '')
  info=tarfile.TarInfo(name);info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
  if p.is_dir():info.type=tarfile.DIRTYPE;info.mode=0o555;tf.addfile(info)
  else:
   require(p.is_file() and not p.is_symlink(),'unexpected archive member')
   data=p.read_bytes();info.mode=0o444;info.size=len(data);tf.addfile(info,io.BytesIO(data))
with ARCHIVE.open('wb') as out:
 with gzip.GzipFile(fileobj=out,mode='wb',mtime=0,filename='') as gz:gz.write(buf.getvalue())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
temp=Path(tempfile.mkdtemp(prefix='boundary-corrected-final-'))
try:
 with tarfile.open(ARCHIVE,'r:gz') as tf:
  files=[]
  for m in tf.getmembers():
   require(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isfile() or m.isdir()),'unsafe archive path')
   p=temp/m.name
   if m.isdir():p.mkdir(parents=True,exist_ok=True)
   else:
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(tf.extractfile(m).read());files.append(m.name)
 root=temp/PREFIX;readonly(root);result=exact(root)
 require({str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}=={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file()},'archive replay byte mismatch')
 receipt={'schema':'boundary-twist-corrected-final-archive-replay-v1','archive':{'filename':ARCHIVE.name,'bytes':ARCHIVE.stat().st_size,'sha256':sha(ARCHIVE)},'all_members_match_corrected_distribution':True,'file_members':files,'exact_replay':result,'scope':'source-free integrity and finite mathematics; not main-problem certification'}
 emit(BASE/'CORRECTED_ARCHIVE_REPLAY.json',receipt)
 emit(BASE/'CORRECTED_DELIVERY.json',dict(receipt['archive'],manifest_sha256=sha(ROOT/'FREEZE_MANIFEST.json'),bootstrap_sha256=sha(ROOT/'bootstrap.py'),verifier_sha256=sha(ROOT/'packet/verify.py'),correction='Wajnryb source attribution only',status='unsolved',turns='5/5'))
 print(json.dumps(receipt['archive']))
finally:remove(temp)
