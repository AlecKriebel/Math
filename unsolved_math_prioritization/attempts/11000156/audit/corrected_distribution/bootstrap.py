#!/usr/bin/env python3
"""External freeze-specific bootstrap. Verify this file against trusted pins first."""
import hashlib
from pathlib import Path
import stat
import subprocess
import sys
MANIFEST_SHA = 'c4c7a8b35ff946adbd92aed28d62a9272b9e256b322267b9f84e37d12454eb06'
VERIFIER_SHA = '1ef67e127ba3a14441a517197684ab5cee86c0d438d764687163d87a8546554e'
base=Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit('usage: bootstrap.py PACKET_DIRECTORY')
root=Path(sys.argv[1])
manifest=base/'FREEZE_MANIFEST.json'
verifier=root/'verify.py'
for p,digest in [(manifest,MANIFEST_SHA),(verifier,VERIFIER_SHA)]:
    try:
        st=p.lstat()
        if not stat.S_ISREG(st.st_mode) or p.is_symlink() or st.st_size>100000:
            raise ValueError('unsafe bootstrap input')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
            raise ValueError('bootstrap pin mismatch')
    except (OSError,ValueError) as exc:
        raise SystemExit('REJECT: '+str(exc))
flags=['-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize==1 else [])
raise SystemExit(subprocess.run([sys.executable,*flags,str(verifier),'--packet',str(root),'--manifest',str(manifest),'--manifest-sha256',MANIFEST_SHA],check=False).returncode)
