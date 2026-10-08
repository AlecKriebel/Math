#!/usr/bin/env python3
"""Authenticate this bootstrap externally before executing any publication code."""
from pathlib import Path
import hashlib,stat,subprocess,sys
VERIFIER_SHA='ed1e54d463b58c4b388e0407d38346878a671c34199b8b7af6d0651b3096843e'
MANIFEST_SHA='9ea0fcf80bfb4775769e45c700bb78a4845ab44623d2b079c0548a9307448064'
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
