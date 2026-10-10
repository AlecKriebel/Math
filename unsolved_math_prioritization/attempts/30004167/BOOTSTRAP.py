#!/usr/bin/env python3
"""Authenticate this file's SHA-256 externally before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B')
import hashlib,os,stat
from pathlib import Path
MANIFEST_SHA256 = '14f65c592fb12a4340db08875ade8418ce9755445f41dc6b49228a8bce290cd4'
VERIFIER_SHA256 = 'f3b5abef279ef563b07ed91bd528d644c13ecee933927789e85c0ac2859267d4'
VERIFIER_BYTES = 12579
def need(ok):
    if not ok:raise ValueError('bootstrap integrity')
def ordinary(path):
    for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode))
    st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=2000000)
    with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
        fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino,st.st_size)==(fs.st_dev,fs.st_ino,fs.st_size));raw=f.read(2000001)
    need(len(raw)==st.st_size);return raw
def main():
    need(len(sys.argv)==4);root=Path(os.path.abspath(sys.argv[1]))
    for p in (root,*root.parents):need(stat.S_ISDIR(p.lstat().st_mode))
    trusted=ordinary(Path(__file__));need(ordinary(root/'BOOTSTRAP.py')==trusted)
    manifest=ordinary(root/'PUBLICATION_MANIFEST.json');need(hashlib.sha256(manifest).hexdigest()==MANIFEST_SHA256)
    verifier=ordinary(root/'verify_publication.py');need(len(verifier)==VERIFIER_BYTES and hashlib.sha256(verifier).hexdigest()==VERIFIER_SHA256)
    sys.argv=['verify_publication.py',MANIFEST_SHA256,hashlib.sha256(trusted).hexdigest(),str(root),sys.argv[2],sys.argv[3]]
    exec(compile(verifier,'<authenticated-publication-verifier>','exec'),{'__name__':'__main__'})
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError):
        print('REJECT: bootstrap integrity validation failed',file=sys.stderr);sys.exit(1)
