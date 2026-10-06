#!/usr/bin/env python3
"""Replay, portability and fail-closed tests, all in temporary directories."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rehash(root):
    # Test helper deliberately updates the manifest after a semantic mutation.
    m = json.loads((root/'manifest.json').read_text())
    for name in m['files']:
        b = (root/name).read_bytes()
        m['files'][name] = {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (root/'manifest.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')


def run(root, optimized=False):
    args = [sys.executable] + (['-O'] if optimized else []) + [str(root/'verify.py')]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run(args,cwd=root.parent,env=env,text=True,capture_output=True,timeout=20)


def main():
    root=Path(__file__).resolve().parent
    passed=[]
    for optimized in [False,True]:
        r=run(root,optimized)
        require(r.returncode==0,'Baseline replay failed: '+r.stderr)
        passed.append('optimized' if optimized else 'normal')
    with tempfile.TemporaryDirectory(prefix='projective-line-audit-') as t:
        base=Path(t)
        relocated=base/'relocated package with spaces'
        shutil.copytree(root,relocated)
        require(run(relocated).returncode==0,'Relocation replay failed')
        passed.append('relocation')
        data=json.loads((root/'certificate.json').read_text())
        cases=[]
        for i in range(6):
            for j in range(4):
                d=copy.deepcopy(data);d['relations'][i]['terms'][j][0]*=-1
                cases.append(('source_sign_'+str(i)+'_'+str(j),d))
        for i in range(4):
            d=copy.deepcopy(data);d['generator_images'][i]='Y' if d['generator_images'][i]=='X' else 'X'
            cases.append(('generator_image_'+str(i),d))
        for i in range(2):
            for j in range(2):
                d=copy.deepcopy(data);d['theta_matrix'][i][j]='0'
                cases.append(('matrix_entry_'+str(i)+'_'+str(j),d))
        d=copy.deepcopy(data);d['relations'].pop();cases.append(('missing_relation',d))
        d=copy.deepcopy(data);d['parameter_condition']='all beta including beta=1';cases.append(('singular_parameter_scope',d))
        for name,d in cases:
            p=base/name;shutil.copytree(root,p)
            (p/'certificate.json').write_text(json.dumps(d))
            rehash(p)
            for optimized in [False,True]:
                r=run(p,optimized)
                require(r.returncode!=0,name+' incorrectly accepted')
                require('Manifest mismatch' not in r.stderr,name+' failed only on hashes')
            passed.append(name)
        mutations=[
            ('untwisted_product',"right = theta[names[word[1]-1]]","right = xc if names[word[1]-1] == 'X' else yc"),
            ('reversed_free_product','word = w + ww','word = ww + w'),
            ('wrong_reduction_sign','expected = b*U*U+(b-1)*U*V+(b+1)*V*U','expected = b*U*U+(b+1)*U*V+(b+1)*V*U'),
            ('wrong_source_formula','x1*(a*x1-x3)+x3*(x1-a*x3)','x1*(b*x1-x3)+x3*(x1-a*x3)'),
        ]
        for name,old,new in mutations:
            p=base/name;shutil.copytree(root,p)
            s=(p/'verify.py').read_text();require(s.count(old)==1,'Mutation target not unique')
            (p/'verify.py').write_text(s.replace(old,new));rehash(p)
            for optimized in [False,True]:
                r=run(p,optimized)
                require(r.returncode!=0 and 'Manifest mismatch' not in r.stderr,name+' not rejected semantically')
            passed.append(name)
        for kind in ['extra_file','extra_directory','bytecode_cache','symlink','fifo','unrehashed_edit']:
            p=base/kind;shutil.copytree(root,p)
            if kind=='extra_file':(p/'extra.txt').write_text('unexpected')
            elif kind=='extra_directory':(p/'extra').mkdir()
            elif kind=='bytecode_cache':(p/'__pycache__').mkdir()
            elif kind=='symlink':
                (p/'README.md').unlink();(p/'README.md').symlink_to(root/'README.md')
            elif kind=='fifo':
                (p/'README.md').unlink();os.mkfifo(p/'README.md')
            else:(p/'proof.md').write_text((p/'proof.md').read_text()+'\nAlteration\n')
            require(run(p).returncode!=0,kind+' accepted')
            passed.append(kind)
    print(json.dumps({'status':'PASS','test_count':len(passed),'tests':passed},sort_keys=True,indent=2))


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
