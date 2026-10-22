#!/usr/bin/env python3
"""Externally pinned bootstrap. Requires trusted isolated Python/stdlib."""
import hashlib
from pathlib import Path
import stat
import subprocess
import sys
MANIFEST_SHA = 'af6631e1537a26720df4234f41974a8de54185e5bd625bc24d6997f3174c1958'
VERIFIER_SHA = '5603afacfc7d8754eb5a94b61097863b01776dcca023210e46e6e96090695945'
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
