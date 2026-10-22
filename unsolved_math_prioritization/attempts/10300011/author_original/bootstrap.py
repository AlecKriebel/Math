#!/usr/bin/env python3
"""Authenticate this bootstrap externally before running it. Strict payload gate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

MANIFEST_SHA256 = "93febcc968a3b244c9cdee7af00fb1ce24519ef03582039cd6b68c2733aab3ae"

def need(ok, message):
    if not ok: raise ValueError(message)

def digest(path):
    b=path.read_bytes(); return len(b),hashlib.sha256(b).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    need(not args.root.is_symlink(),'symlink root rejected')
    root=args.root.resolve()
    need(root.is_dir(),'root is not directory')
    actual_files=set(); actual_dirs=set()
    for base, dirs, files in os.walk(root,followlinks=False):
        for name in dirs+files:
            p=Path(base)/name; mode=p.lstat().st_mode
            need(not stat.S_ISLNK(mode),'symlink inventory member rejected')
            rel=p.relative_to(root).as_posix()
            if stat.S_ISDIR(mode): actual_dirs.add(rel)
            elif stat.S_ISREG(mode): actual_files.add(rel)
            else: raise ValueError('nonregular inventory member')
    need(actual_dirs=={'author'},'directory inventory mismatch')
    mf=root/'MANIFEST.json'
    need(mf.is_file(),'manifest missing')
    need(digest(mf)[1]==MANIFEST_SHA256,'pinned manifest mismatch')
    m=json.loads(mf.read_text())
    need(m.get('schema')=='sublamination-author-manifest-v1' and m.get('problem_id')==10300011,'manifest identity mismatch')
    expected=set(m['files'])|{'MANIFEST.json','bootstrap.py'}
    need(actual_files==expected,'file inventory mismatch')
    need(digest(root/'bootstrap.py')==digest(Path(__file__).resolve()),'candidate bootstrap differs from authenticated executing bootstrap')
    for rel,pin in m['files'].items():
        parts=Path(rel).parts
        need(not Path(rel).is_absolute() and '..' not in parts and len(parts)==2 and parts[0]=='author','unsafe manifest path')
        need(digest(root/rel)==(pin['bytes'],pin['sha256']),'payload digest mismatch: '+rel)
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'author'/'verify.py')],text=True,capture_output=True,timeout=90)
    need(c.returncode==0 and not c.stderr,'authenticated verifier failed')
    result=json.loads(c.stdout)
    need(result.get('status')=='PASS_SCOPED_CONTROLS' and result.get('general_solution') is False,'unexpected verifier scope')
    print(json.dumps({'status':'PASS_AUTHENTICATED_AUTHOR_BOUNDARY','manifest_sha256':MANIFEST_SHA256,'payload_files':len(m['files']),'author_result':result},sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(2)
