#!/usr/bin/env python3
"""Externally pin this launcher; run using a trusted Python with -I -S -B."""
from pathlib import Path
import hashlib,os,stat,sys
EXPECTED_VERIFIER='32f1100d1b717d9a785a17804f9ed24d2ac3fecc542f526d8a26dccae818f7fc'
EXPECTED_MANIFEST='fc003433b6074ea37e08b717fc2453b9a6f57c8d237206c2dcbf62d031451763'
def reject(m):
    print('REJECT: '+m,file=sys.stderr);sys.exit(1)
def read(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or st.st_size>2000000:reject('nonregular or oversized trust member')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd)
        if (a.st_dev,a.st_ino)!=(st.st_dev,st.st_ino):reject('trust member changed')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(2000001)
        z=os.fstat(fd)
        if (a.st_size,a.st_mtime_ns,a.st_ctime_ns)!=(z.st_size,z.st_mtime_ns,z.st_ctime_ns) or len(b)!=st.st_size:reject('unstable trust member')
    finally:os.close(fd)
    return b
def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):reject('require -I -S -B')
    here=Path(__file__).absolute().parent;args=sys.argv[1:]
    root=Path(args.pop(0)).absolute() if args and not args[0].startswith('--') else here
    if root.is_symlink() or not root.is_dir():reject('invalid root')
    if read(root/'BOOTSTRAP.py')!=read(Path(__file__)):reject('different bootstrap copy')
    code=read(root/'VERIFY_PUBLICATION.py')
    if hashlib.sha256(code).hexdigest()!=EXPECTED_VERIFIER:reject('verifier external pin')
    if hashlib.sha256(read(root/'PUBLICATION_MANIFEST.json')).hexdigest()!=EXPECTED_MANIFEST:reject('manifest external pin')
    sys.argv=[str(root/'VERIFY_PUBLICATION.py'),str(root)]+args
    exec(compile(code,str(root/'VERIFY_PUBLICATION.py'),'exec'),{'__name__':'__main__','__file__':str(root/'VERIFY_PUBLICATION.py')})
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,TypeError,RecursionError) as e:reject(str(e))
