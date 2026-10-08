#!/usr/bin/env python3
"""Authenticate this file's SHA-256 externally before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
import hashlib,os,stat
from pathlib import Path
MANIFEST_SHA256 = 'ed5335a9d1adce66096e29002e7af95fea09ec983eb980e5cc649d0459a11dbb'
VERIFIER_SHA256 = 'd11639d8913a6d091ecb35382cc342ea9c9b3fa6ce10ff98539bdebe925a1427'
VERIFIER_BYTES = 11444
CONTROLS_SHA256 = '5e962ff97a18ec59d81e10fd1f20a9465d644f9acd17e00b2a7fa91c09dff6c0'
CONTROLS_BYTES = 12467
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
