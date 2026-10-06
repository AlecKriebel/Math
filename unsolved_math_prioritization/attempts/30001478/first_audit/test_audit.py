#!/usr/bin/env python3
"""Replays and adversarial controls on temporary copies, without bytecode imports."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok,message):
    if not ok:
        raise ValueError(message)


def run(root,script='verify_audit.py',optimized=False):
    return subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/script)],
                          cwd=root.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                          text=True,capture_output=True,timeout=120)


def rehash(root):
    manifest=json.loads((root/'manifest.json').read_text())
    for name in manifest['files']:
        data=(root/name).read_bytes()
        manifest['files'][name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    (root/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')


def main():
    root=Path(__file__).resolve().parent
    passed=[]
    for optimized in (False,True):
        result=run(root,optimized=optimized)
        require(result.returncode==0,'Baseline failed: '+result.stderr)
        passed.append('optimized_baseline' if optimized else 'normal_baseline')
    with tempfile.TemporaryDirectory(prefix='independent-projective-line-') as name:
        temp=Path(name)
        relocated=temp/'relocated package with spaces'
        shutil.copytree(root,relocated)
        for optimized in (False,True):
            result=run(relocated,optimized=optimized)
            require(result.returncode==0,'Relocation failed: '+result.stderr)
            passed.append('optimized_relocation' if optimized else 'normal_relocation')
        for control in ('extra_file','extra_directory','root_bytecode','nested_bytecode',
                        'symlink','fifo','missing_file','unrehashed_edit'):
            work=temp/control;shutil.copytree(root,work)
            if control=='extra_file':(work/'extra.dat').write_text('extra')
            elif control=='extra_directory':(work/'extra').mkdir()
            elif control=='root_bytecode':(work/'__pycache__').mkdir()
            elif control=='nested_bytecode':(work/'author'/'__pycache__').mkdir()
            elif control=='symlink':
                (work/'README.md').unlink();(work/'README.md').symlink_to(root/'README.md')
            elif control=='fifo':
                (work/'README.md').unlink();os.mkfifo(work/'README.md')
            elif control=='missing_file':(work/'README.md').unlink()
            else:(work/'README.md').write_text('changed')
            for optimized in (False,True):
                result=run(work,optimized=optimized)
                require(result.returncode!=0,'Inventory mutation accepted: '+control)
            passed.append(control)
        # These mutations are rehashed and must fail in the independent math,
        # not merely through package checksums. Both interpreter modes are used.
        mutations=[
            ('wrong_source_generator','(3,1): ONE, (3,3): cneg(ALPHA)',
             '(4,1): ONE, (3,3): cneg(ALPHA)'),
            ('wrong_quotient_sign','(0,1): NEG, (1,0): ONE, (1,1): cneg(BETA)',
             '(0,1): ONE, (1,0): ONE, (1,1): cneg(BETA)'),
            ('inverse_theta','0:nadd(X, nscale(BETA,Y)), 1:nadd(nscale(BETA,X),Y)',
             '0:nadd(X, nscale(cneg(BETA),Y)), 1:nadd(nscale(cneg(BETA),X),Y)'),
            ('wrong_characteristic_two_field','if x&4: x ^= 7','if x&4: x ^= 5'),
        ]
        for control,old,new in mutations:
            work=temp/control;shutil.copytree(root,work)
            text=(work/'independent_check.py').read_text()
            require(text.count(old)==1,'Ambiguous mutation target: '+control)
            (work/'independent_check.py').write_text(text.replace(old,new));rehash(work)
            for optimized in (False,True):
                result=run(work,'independent_check.py',optimized)
                require(result.returncode!=0 and 'Hash mismatch' not in result.stderr,
                        'Semantic mutation accepted: '+control)
            passed.append(control)
    print(json.dumps({'status':'PASS','named_test_count':len(passed),'tests':passed,
                      'negative_controls_checked_in_normal_and_optimized_modes':True},sort_keys=True,indent=2))


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
