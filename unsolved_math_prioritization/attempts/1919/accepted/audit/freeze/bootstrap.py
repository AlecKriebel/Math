#!/usr/bin/env python3
"""Externally pinned launcher for the independent finite audit."""
import hashlib,stat,subprocess,sys
from pathlib import Path
MANIFEST = 'd7d4da929fa81626df3a30ecab6420144b7e78e669aa01df31435c2669b9f44c'
VERIFIER = '3c59c13ea69872363abf54aa422a06e1d72a58d755a3d1d6cbafac3d7b9f3aa9'
if sys.flags.isolated != 1:
    raise SystemExit('REJECT: isolated Python required')
if len(sys.argv) != 2:
    raise SystemExit('usage: bootstrap.py AUDIT_PACKET')
base=Path(__file__).resolve().parent
root=Path(sys.argv[1])
if root.is_symlink() or not root.is_dir():
    raise SystemExit('REJECT: unsafe packet root')
for p,pin in [(base/'FREEZE_MANIFEST.json',MANIFEST),(root/'verify_audit.py',VERIFIER)]:
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or p.is_symlink() or s.st_size>100000 or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:
        raise SystemExit('REJECT: external pin mismatch')
flags=['-I','-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize else [])
raise SystemExit(subprocess.run([sys.executable,*flags,str(root/'verify_audit.py'),'--packet',str(root),'--manifest',str(base/'FREEZE_MANIFEST.json'),'--manifest-sha256',MANIFEST],check=False).returncode)
