#!/usr/bin/env python3
"""Authenticate this file's SHA-256 externally before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
import hashlib,os,stat
from pathlib import Path
MANIFEST_SHA256 = '941877dce620dea4a6ba80f1f32f0637488abda10ed864ba009a8f4863cf8a6f'
VERIFIER_SHA256 = '4cefb428e9596a9b6697cb4305bda93adeb48b3163690717ebb94ad21c289620'
VERIFIER_BYTES = 51851
CONTROLS_SHA256 = '1c4dbc429d5c34f04c91174ef31894f148062900582346dd095f8675401510ee'
CONTROLS_BYTES = 20993
def need(ok,message='bootstrap integrity'):
 if not ok:raise ValueError(message)
def ordinary(path):
 for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode),'linked root or ancestor')
 st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=2000000,'ordinary bounded single-link bootstrap input')
 with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
  fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino,st.st_size)==(fs.st_dev,fs.st_ino,fs.st_size),'bootstrap input replaced during read');raw=f.read(2000001)
 need(len(raw)==st.st_size,'bootstrap input size changed');return raw
def main():
 controls=len(sys.argv)==3 and sys.argv[1]=='--controls'
 need(controls or (len(sys.argv)==2 and sys.argv[1]!='--controls'),'packet argument count');root=Path(os.path.abspath(sys.argv[2] if controls else sys.argv[1]))
 for p in (root,*root.parents):need(stat.S_ISDIR(p.lstat().st_mode),'linked root or ancestor')
 trusted=ordinary(Path(__file__));need(ordinary(root/'BOOTSTRAP.py')==trusted,'packet bootstrap differs from externally trusted bytes')
 manifest=ordinary(root/'PUBLICATION_MANIFEST.json');need(hashlib.sha256(manifest).hexdigest()==MANIFEST_SHA256,'external manifest SHA-256 mismatch')
 verifier=ordinary(root/'verify_publication.py');need(len(verifier)==VERIFIER_BYTES and hashlib.sha256(verifier).hexdigest()==VERIFIER_SHA256,'verifier SHA-256 or size mismatch')
 if controls:
  harness=ordinary(root/'MUTATION_TESTS.py');need(len(harness)==CONTROLS_BYTES and hashlib.sha256(harness).hexdigest()==CONTROLS_SHA256,'controls SHA-256 or size mismatch')
  sys.argv=['MUTATION_TESTS.py',str(root),hashlib.sha256(trusted).hexdigest()]
  exec(compile(harness,'<authenticated-publication-controls>','exec'),{'__name__':'__main__','__file__':str(root/'MUTATION_TESTS.py')})
  return
 sys.argv=['verify_publication.py',MANIFEST_SHA256,hashlib.sha256(trusted).hexdigest(),str(root)]
 exec(compile(verifier,'<authenticated-publication-verifier>','exec'),{'__name__':'__main__'})
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError) as exc:print('REJECT: bootstrap integrity validation failed: '+('filesystem errno '+str(exc.errno) if isinstance(exc,OSError) else str(exc)),file=sys.stderr);sys.exit(1)
