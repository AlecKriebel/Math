#!/usr/bin/env python3
"""Normal/-O/relocation and adversarial tests on disposable package copies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok,message):
    if not ok: raise ValueError(message)


def run(root,optimized=False,script='verify_review.py'):
    return subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/script)],
                          cwd=root.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                          text=True,capture_output=True,timeout=30)


def rehash(root):
    manifest=json.loads((root/'manifest.json').read_text())
    for name in manifest['files']:
        b=(root/name).read_bytes()
        manifest['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (root/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')


def main():
    need(len(sys.argv)==1,'No arguments accepted')
    root=Path(__file__).absolute().parent
    results=[]
    for optimized in (False,True):
        p=run(root,optimized)
        need(p.returncode==0,'Baseline failed: '+p.stderr)
        results.append('optimized_baseline' if optimized else 'normal_baseline')
    with tempfile.TemporaryDirectory(prefix='prime-quotient-second-review-') as d:
        temp=Path(d)
        relocated=temp/'relocated path with spaces'
        shutil.copytree(root,relocated)
        for optimized in (False,True):
            p=run(relocated,optimized)
            need(p.returncode==0,'Relocation failed: '+p.stderr)
            results.append('optimized_relocation' if optimized else 'normal_relocation')
        for name in ['extra_file','extra_directory','bytecode','missing_file','unrehashed_edit',
                     'symlink_document','symlink_verifier','fifo','manifest_extra','manifest_duplicate']:
            work=temp/name;shutil.copytree(root,work)
            if name=='extra_file':(work/'surprise.txt').write_text('extra')
            elif name=='extra_directory':(work/'extra').mkdir()
            elif name=='bytecode':(work/'__pycache__').mkdir()
            elif name=='missing_file':(work/'README.md').unlink()
            elif name=='unrehashed_edit':(work/'README.md').write_text('changed')
            elif name.startswith('symlink'):
                target='verify_review.py' if name=='symlink_verifier' else 'README.md'
                (work/target).unlink();(work/target).symlink_to(root/target)
            elif name=='fifo':(work/'README.md').unlink();os.mkfifo(work/'README.md')
            elif name=='manifest_extra':
                m=json.loads((work/'manifest.json').read_text());m['files']['ghost']={}
                (work/'manifest.json').write_text(json.dumps(m))
            else:
                p=work/'manifest.json';s=p.read_text();p.write_text(s.replace('"schema": 1','"schema": 1, "schema": 1'))
            for optimized in (False,True):
                p=run(work,optimized)
                need(p.returncode!=0,'Inventory control was accepted: '+name)
            results.append(name)
        mutations=[
            ('source_generator',"(1,'','31')","(1,'','41')"),
            ('quotient_sign',"Q = [(1,'b','XX'),(-1,'','XY')", "Q = [(1,'b','XX'),(1,'','XY')"),
            ('inverse_pullback',"'X':plus(X,times(B,Y)), 'Y':plus(times(B,X),Y)",
             "'X':plus(X,scale(-1,times(B,Y))), 'Y':plus(scale(-1,times(B,X)),Y)"),
            ('ore_sign',"(1,'b','UV'),(-1,'','UV')", "(1,'b','UV'),(1,'','UV')"),
            ('gf4_modulus','if a&4: a ^= 7','if a&4: a ^= 5'),
            ('fractional_determinant','==scale(4,R)','==scale(2,R)'),
        ]
        for name,old,new in mutations:
            work=temp/name;shutil.copytree(root,work)
            p=work/'check_algebra.py';source=p.read_text()
            need(source.count(old)==1,'Mutation is not unique: '+name)
            p.write_text(source.replace(old,new));rehash(work)
            for optimized in (False,True):
                output=run(work,optimized,script='check_algebra.py')
                need(output.returncode!=0,'Semantic control was accepted: '+name)
                output=run(work,optimized)
                need(output.returncode!=0 and 'Manifest content mismatch' not in output.stderr,
                     'Rehashed semantic mutation was not rejected by algebra: '+name)
            results.append(name)
    print(json.dumps({'status':'PASS','named_test_count':len(results),'tests':results,
                     'all_negative_controls_in_normal_and_optimized_modes':True},
                     sort_keys=True,indent=2))


if __name__=='__main__':
    try: main()
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
