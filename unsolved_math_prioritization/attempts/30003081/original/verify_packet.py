#!/usr/bin/env python3
"""Verify an externally pinned flat inventory and replay at the current optimization level."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

class VerificationError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def no_duplicate_keys(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, 'duplicate JSON key')
        result[k] = v
    return result

def verify(root, pin):
    require(not root.is_symlink(), 'symlink packet root')
    require(root.is_dir(), 'missing packet root')
    require(bool(re.fullmatch('[0-9a-f]{64}', pin)), 'invalid manifest pin')
    mf=root/'MANIFEST.json'
    require(mf.exists() and stat.S_ISREG(mf.lstat().st_mode), 'manifest is not regular')
    raw=mf.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==pin, 'manifest pin mismatch')
    data=json.loads(raw,object_pairs_hook=no_duplicate_keys)
    require(set(data)=={'schema','files'}, 'manifest fields')
    require(data['schema']=='source-free-flat-v1', 'manifest schema')
    require(isinstance(data['files'],list), 'manifest inventory type')
    expected={'MANIFEST.json'}
    for row in data['files']:
        require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'}, 'entry fields')
        name=row['path']
        require(isinstance(name,str) and bool(re.fullmatch('[A-Za-z0-9_.-]+',name)) and name not in {'.','..'},'unsafe path')
        require(name not in expected,'duplicate path')
        expected.add(name)
        require(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
        require(isinstance(row['sha256'],str) and bool(re.fullmatch('[0-9a-f]{64}',row['sha256'])),'invalid digest')
        p=root/name
        require(p.exists() and stat.S_ISREG(p.lstat().st_mode),'nonregular or missing member: '+name)
        b=p.read_bytes()
        require(len(b)==row['bytes'],'size mismatch: '+name)
        require(hashlib.sha256(b).hexdigest()==row['sha256'],'hash mismatch: '+name)
        if name.endswith('.py'):
            require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(b))),'assert-only risk: '+name)
    require({p.name for p in root.iterdir()}==expected,'unexpected packet members')
    mode=sys.flags.optimize
    require(mode in (0,1,2),'unsupported optimization mode')
    flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
    program=('import runpy,sys; '
             'mode='+str(mode)+'; '
             '\nif sys.flags.optimize != mode: raise RuntimeError("child optimization mismatch")\n'
             'runpy.run_path(sys.argv[1],run_name="__main__")')
    with tempfile.TemporaryDirectory(prefix='unexpected-replay-') as cwd:
        p=subprocess.run([sys.executable,*flags,'-I','-B','-c',program,str((root/'check_math.py').resolve())],cwd=cwd,capture_output=True,timeout=60)
    require(p.returncode==0,'mathematical replay failed: '+p.stderr.decode(errors='replace'))
    require(p.stdout==(root/'MATH_RESULTS.json').read_bytes(),'replay output mismatch')
    return {'status':'PASS','optimization':mode,'manifest_sha256':pin,'payload_files':len(data['files']),
            'source_reverification':'NOT_RUN: source bytes deliberately absent',
            'mathematics':'Finite diagnostics replayed; universal arguments require written review.'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--manifest-sha256',required=True)
    a=p.parse_args()
    try:
        result=verify(a.root,a.manifest_sha256)
    except (VerificationError,ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True))
    return 0

if __name__=='__main__':
    sys.exit(main())
