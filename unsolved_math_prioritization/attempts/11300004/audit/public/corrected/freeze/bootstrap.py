#!/usr/bin/env python3
"""Externally pinned bootstrap. Requires trusted isolated Python/stdlib."""
import hashlib
from pathlib import Path
import stat
import subprocess
import sys
MANIFEST_SHA = '9097b3da520bdee1facde8b7fdb92b7b23e974fb7cbb726c2903ccbc1965cd56'
VERIFIER_SHA = '4f55b4aee1cae738e45891f9ad53fe3e1c901aeef3b4b87af6669beffe3cd331'
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
