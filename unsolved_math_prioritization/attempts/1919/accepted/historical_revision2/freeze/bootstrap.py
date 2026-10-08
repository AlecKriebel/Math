#!/usr/bin/env python3
"""Externally pinned bootstrap. Requires trusted isolated Python/stdlib."""
import hashlib
from pathlib import Path
import stat
import subprocess
import sys
MANIFEST_SHA = '4a68c2510b717b1e6e4afcf267fdc0b40bf97a8156eab1c4c44c51f65e7410da'
VERIFIER_SHA = '7fb843326a441b6898836dc50b59fea41a6c9bf071352ad3470008a76f84e469'
if sys.flags.isolated != 1:
    raise SystemExit('REJECT: isolated Python mode required')
if len(sys.argv)!=2:
    raise SystemExit('usage: bootstrap.py PACKET_DIRECTORY')
base=Path(__file__).resolve().parent
root=Path(sys.argv[1])
if root.is_symlink() or not root.is_dir():
    raise SystemExit('REJECT: unsafe packet root')
manifest=base/'FREEZE_MANIFEST.json'
verifier=root/'verify.py'
for path,pin in [(manifest,MANIFEST_SHA),(verifier,VERIFIER_SHA)]:
    try:
        info=path.lstat()
        if not stat.S_ISREG(info.st_mode) or path.is_symlink() or info.st_size>100000:
            raise ValueError('unsafe bootstrap input')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:
            raise ValueError('bootstrap pin mismatch')
    except (OSError,ValueError) as exc:
        raise SystemExit('REJECT: '+str(exc))
flags=['-I','-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize==1 else [])
raise SystemExit(subprocess.run([sys.executable,*flags,str(verifier),'--packet',str(root),'--manifest',str(manifest),'--manifest-sha256',MANIFEST_SHA],check=False).returncode)
