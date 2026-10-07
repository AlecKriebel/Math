#!/usr/bin/env python3
"""Actual temporary corruption tests. Originals are never changed."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def require(ok,label):
    if not ok: raise ValueError(label)

def invoke(root,mode=(),env=None):
    return subprocess.run([sys.executable,'-I','-B',*mode,str(root/'verify_publication.py'),'--integrity-only'],cwd=root.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)

def main():
    original={p.relative_to(ROOT).as_posix():p.read_bytes() for p in ROOT.rglob('*') if p.is_file()}
    require(invoke(ROOT).returncode==0,'Original integrity must pass')
    manifest=json.loads(original['PACKAGE_MANIFEST.json'])
    detected=[]
    with tempfile.TemporaryDirectory(prefix='rough M [relocated] ') as td:
        root=Path(td)/'package with spaces'
        shutil.copytree(ROOT,root)
        require(invoke(root).returncode==0 and invoke(root,['-O']).returncode==0,'Relocated baselines')
        for item in manifest['files']:
            name=item['file']; target=root/name; old=target.read_bytes()
            # A comment byte addition changes the actual payload; no simulated failure.
            target.write_bytes(old+b'\nCORRUPTION\n')
            for flags in ([],['-O']):
                result=invoke(root,flags)
                require(result.returncode!=0,'Undetected payload corruption: '+name)
            target.write_bytes(old); detected.append('payload:'+name)
        for name in ['PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.sha256']:
            target=root/name; old=target.read_bytes(); target.write_bytes(old+b' ')
            require(invoke(root).returncode!=0 and invoke(root,['-O']).returncode!=0,'Undetected manifest corruption')
            target.write_bytes(old); detected.append('manifest:'+name)
        target=root/'frozen_v2/PROOF.md'; old=target.read_bytes(); target.unlink()
        require(invoke(root).returncode!=0,'Missing file not detected'); detected.append('missing_file')
        target.write_bytes(old)
        (root/'unexpected.txt').write_text('unexpected')
        require(invoke(root).returncode!=0,'Extra file not detected'); detected.append('unlisted_file')
        (root/'unexpected.txt').unlink()
        target.unlink(); target.symlink_to(ROOT/'frozen_v2/PROOF.md')
        require(invoke(root).returncode!=0,'Symlink not detected'); detected.append('symlink_file')
        target.unlink(); target.write_bytes(old)
        for flags in (['-O'],['-OO']):
            result=subprocess.run([sys.executable,'-I','-B',*flags,str(root/'run_audit_a.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            require(result.returncode!=0 and b'REFUSED' in result.stderr,'Optimized audit A guard'); detected.append('audit_a_guard:'+flags[0])
        env=os.environ.copy(); env['PYTHONOPTIMIZE']='2'
        result=subprocess.run([sys.executable,'-B',str(root/'run_audit_a.py')],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        require(result.returncode!=0 and b'REFUSED' in result.stderr,'Environmental audit A guard'); detected.append('audit_a_guard:environment')
        # Bypass the outer integrity verifier ONLY for this negative fixture,
        # to confirm the assertion-based checker really fails under normal Python.
        target=root/'audit_a/independent_checks.py'; old=target.read_bytes()
        needle=b'assert len(pair_points) == 36 and len(points) == 12'
        require(old.count(needle)==1,'Audit A mutation target must be unique')
        target.write_bytes(old.replace(needle,b'assert len(pair_points) == 36 and len(points) == 11'))
        result=subprocess.run([sys.executable,'-I','-B',str(root/'run_audit_a.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        require(result.returncode!=0 and b'AssertionError' in result.stderr,'Audit A mathematical corruption not detected')
        detected.append('audit_a_wrong_intersection_count'); target.write_bytes(old)
        require(invoke(root).returncode==0,'Restored copy integrity')
    after={p.relative_to(ROOT).as_posix():p.read_bytes() for p in ROOT.rglob('*') if p.is_file()}
    require(original==after,'Original package changed')
    print(json.dumps({'status':'PASS','detected_corruptions':len(detected),'controls':detected,'original_bytes_unchanged':True},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
