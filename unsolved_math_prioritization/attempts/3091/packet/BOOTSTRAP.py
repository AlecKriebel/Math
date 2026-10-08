#!/usr/bin/env python3
"""Authenticate this bootstrap externally before executing any publication code."""
from pathlib import Path
import hashlib,stat,subprocess,sys
VERIFIER_SHA='f3a87e294b65a7ae97a7ac9afd6275b75a4855b226b494426f021c47bd5b2c4f'
MANIFEST_SHA='3bd74b9cdaba22e6edd01f0961a72096c27c67d533ae4664ba01716630391c4b'
def main():
    if len(sys.argv)<2:raise ValueError('usage: BOOTSTRAP.py PACKET [replay options]')
    root=Path(sys.argv[1]).absolute()
    if root.is_symlink() or not root.is_dir():raise ValueError('bad packet root')
    for name,pin in [('VERIFY_PUBLICATION.py',VERIFIER_SHA),('PUBLICATION_MANIFEST.json',MANIFEST_SHA)]:
        p=root/name
        if p.is_symlink() or not stat.S_ISREG(p.stat().st_mode):raise ValueError('bad authenticated file')
        if p.stat().st_size>2000000 or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:raise ValueError('bootstrap pin mismatch: '+name)
    p=root/'BOOTSTRAP.py'
    if p.is_symlink() or not p.is_file() or p.read_bytes()!=Path(__file__).read_bytes():raise ValueError('different bootstrap copy')
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'VERIFY_PUBLICATION.py'),str(root),*sys.argv[2:]],check=False).returncode
if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
