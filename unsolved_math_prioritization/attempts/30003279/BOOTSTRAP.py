#!/usr/bin/env python3
"""Copy and authenticate this launcher outside the packet before use.
Its fixed wrapper digest prevents a modified packet verifier from self-accepting.
The independently supplied publication-manifest digest anchors the whole packet.
"""
import argparse
import hashlib
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

WRAPPER_SHA256 = '8b8a65e7da2b92144bedc3606fceb6d239f1143e1fc4ef88fc5e1801608b0a52'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,required=True)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    p.add_argument('--check-only',action='store_true')
    p.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    a = p.parse_args(); root = a.packet.absolute()
    try:
        if not re.fullmatch('[0-9a-f]{64}',a.expected_manifest): raise ValueError('Invalid external pin')
        if not stat.S_ISDIR(root.lstat().st_mode): raise ValueError('Packet root must be a real directory')
        wrapper = root/'VERIFY_PUBLICATION.py'
        if not stat.S_ISREG(wrapper.lstat().st_mode): raise ValueError('Wrapper must be regular')
        if hashlib.sha256(wrapper.read_bytes()).hexdigest() != WRAPPER_SHA256: raise ValueError('External wrapper anchor mismatch')
        flags = ['-'+'O'*sys.flags.optimize] if sys.flags.optimize else []
        cmd = [sys.executable,'-I','-B',*flags,str(wrapper),'--packet',str(root),'--expected-manifest',a.expected_manifest,'--filesystem-profile',a.filesystem_profile,'--mode='+a.mode]
        if a.check_only: cmd.append('--check-only')
        env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}; env['PYTHONDONTWRITEBYTECODE'] = '1'
        return subprocess.run(cmd,env=env).returncode
    except (ValueError,OSError) as error:
        print('BOOTSTRAP REJECT: '+str(error),file=sys.stderr); return 1

if __name__ == '__main__': sys.exit(main())
