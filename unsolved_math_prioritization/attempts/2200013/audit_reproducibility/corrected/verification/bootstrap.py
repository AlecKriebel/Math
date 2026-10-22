#!/usr/bin/env python3
"""Independently pin this bootstrap before execution; its constants pin the rest."""
import argparse, hashlib, pathlib, subprocess, sys
MANIFEST_SHA256 = 'cf8ddfc1ea755b8a9c136d6bdf420ea274b6add35be7fba66a02090efe087ed0'
REPLAY_SHA256 = '3445d032b94e7da0cc9f48daa1b7cf290e29ca62d780cb7684e448d6e296ddac'
p=argparse.ArgumentParser()
p.add_argument('--root',type=pathlib.Path,required=True)
p.add_argument('--manifest',type=pathlib.Path,required=True)
a=p.parse_args()
try:
    if a.root.is_symlink() or a.manifest.is_symlink() or (a.root/'replay.py').is_symlink():
        raise ValueError('symlink bootstrap input')
    if hashlib.sha256(a.manifest.read_bytes()).hexdigest()!=MANIFEST_SHA256:
        raise ValueError('bootstrap manifest mismatch')
    if hashlib.sha256((a.root/'replay.py').read_bytes()).hexdigest()!=REPLAY_SHA256:
        raise ValueError('bootstrap replay mismatch')
except (OSError,ValueError) as e:
    print('REJECT:',e)
    sys.exit(2)
mode=['-'+'O'*sys.flags.optimize] if sys.flags.optimize else []
sys.exit(subprocess.call([sys.executable,'-I','-B',*mode,str((a.root/'replay.py').resolve()),'--root',str(a.root.resolve()),'--manifest',str(a.manifest.resolve()),'--manifest-sha256',MANIFEST_SHA256]))
