#!/usr/bin/env python3
"""Authenticate this file's SHA-256 externally before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
import hashlib,os,stat
from pathlib import Path
MANIFEST_SHA256 = '47e5b6fb495acb06f2d423eeb03d7aecdf9e564a4c9462701e1c6045c70589b4'
VERIFIER_SHA256 = 'e94759256cf171a390d7634e91529d074e5a849a1f3784fc1b0284b65640deb6'
VERIFIER_BYTES = 31557
CONTROLS_SHA256 = '34f749537de3cd1e93db352ca04f95aef94afde0f552855a7160373ab9a5cdc5'
CONTROLS_BYTES = 29152
def need(ok):
 if not ok:raise ValueError('bootstrap integrity')
def ordinary(path):
 for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode))
 st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=2000000)
 with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
  fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino,st.st_size)==(fs.st_dev,fs.st_ino,fs.st_size));raw=f.read(2000001)
 need(len(raw)==st.st_size);return raw
def main():
 controls=len(sys.argv)==3 and sys.argv[1]=='--controls'
 need(controls or len(sys.argv)==2);root=Path(os.path.abspath(sys.argv[2] if controls else sys.argv[1]))
 for p in (root,*root.parents):need(stat.S_ISDIR(p.lstat().st_mode))
 trusted=ordinary(Path(__file__));need(ordinary(root/'BOOTSTRAP.py')==trusted)
 manifest=ordinary(root/'PUBLICATION_MANIFEST.json');need(hashlib.sha256(manifest).hexdigest()==MANIFEST_SHA256)
 verifier=ordinary(root/'verify_publication.py');need(len(verifier)==VERIFIER_BYTES and hashlib.sha256(verifier).hexdigest()==VERIFIER_SHA256)
 if controls:
  harness=ordinary(root/'MUTATION_TESTS.py');need(len(harness)==CONTROLS_BYTES and hashlib.sha256(harness).hexdigest()==CONTROLS_SHA256)
  sys.argv=['MUTATION_TESTS.py',str(root),hashlib.sha256(trusted).hexdigest()]
  exec(compile(harness,'<authenticated-publication-controls>','exec'),{'__name__':'__main__','__file__':str(root/'MUTATION_TESTS.py')})
  return
 sys.argv=['verify_publication.py',MANIFEST_SHA256,hashlib.sha256(trusted).hexdigest(),str(root)]
 exec(compile(verifier,'<authenticated-publication-verifier>','exec'),{'__name__':'__main__'})
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError):print('REJECT: bootstrap integrity validation failed',file=sys.stderr);sys.exit(1)
