#!/usr/bin/env python3
"""Independent audit adversarial harness. Copies are disposable; originals stay read-only."""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def check(value,message):
    if not value:
        raise RuntimeError(message)


def load(path):
    spec=importlib.util.spec_from_file_location('independent_audit_verifier',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rejected(call,name):
    try:call()
    except (ValueError,FileNotFoundError,RuntimeError,KeyError,NotADirectoryError):return name
    raise RuntimeError('Accepted deliberate corruption: '+name)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-dir',type=Path,required=True)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--source-dir',type=Path,required=True)
    args=parser.parse_args()
    args.author_dir=args.author_dir.resolve();args.archive=args.archive.resolve();args.source_dir=args.source_dir.resolve()
    root=Path(__file__).resolve().parent
    v=load(root/'independent_verify.py')
    results=[]
    # This imports no author mathematical implementation.
    bad=[list(row) for row in v.U];bad[0]=bad[1][:]
    results.append(rejected(lambda:v.cube_controls(matrix=bad),'duplicate_cube_row'))
    bad=[list(row) for row in v.U];bad[0]=[-x for x in bad[0]]
    results.append(rejected(lambda:v.cube_controls(matrix=bad),'wrong_cube_orientation'))
    bad=[list(row) for row in zip(*v.U)]
    results.append(rejected(lambda:v.cube_controls(matrix=bad),'transposed_cube_map'))
    bad=list(v.C);bad[0]+=1
    results.append(rejected(lambda:v.cube_controls(vertex=bad),'shifted_fractional_vertex'))
    bad=list(v.C);bad[0]=1
    results.append(rejected(lambda:v.cube_controls(vertex=bad),'rounded_fractional_vertex'))
    bad=list(v.MU);bad[1]=(3,2,2)
    results.append(rejected(lambda:v.cube_controls(mu=bad),'incorrect_young_diagram'))
    bad=list(v.MU);bad[0],bad[1]=bad[1],bad[0]
    results.append(rejected(lambda:v.cube_controls(mu=bad),'permuted_young_diagram_coordinates'))
    bad=list(v.MU);bad[0]=bad[1]
    results.append(rejected(lambda:v.cube_controls(mu=bad),'duplicated_young_diagram'))
    results.append(rejected(lambda:v.need(False,'sentinel'),'false_runtime_check'))
    # Graded-lattice full-generation hypothesis is essential even at full rational rank.
    A=((1,1),(0,2));B=((1,1),(0,1))
    check(v.determinant(A)==2 and v.determinant(B)==1,'bad sublattice control')
    check(v.inverse(A)[1][1].denominator==2,'index-two sublattice unexpectedly unimodular')
    # Freeze corruption tests include a maliciously re-sealed altered proof.
    with tempfile.TemporaryDirectory(prefix='plabic-independent-negative-') as tmp:
        tmp=Path(tmp)
        cases=['changed_proof','missing_proof','added_file','added_directory','symlink_member',
               'resealed_changed_proof','changed_manifest','changed_archive']
        for case in cases:
            copied=tmp/case
            shutil.copytree(args.author_dir,copied)
            archive=args.archive
            if case in ('changed_proof','resealed_changed_proof'):
                p=copied/'MATHEMATICS.md';p.write_bytes(p.read_bytes()+b'\nAltered proof.\n')
                if case=='resealed_changed_proof':
                    m=json.loads((copied/'MANIFEST.json').read_text())
                    for item in m['files']:
                        if item['name']==p.name:
                            item['bytes']=p.stat().st_size;item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
                    (copied/'MANIFEST.json').write_text(json.dumps(m))
            elif case=='missing_proof':(copied/'MATHEMATICS.md').unlink()
            elif case=='added_file':(copied/'extra.txt').write_text('extra')
            elif case=='added_directory':(copied/'extra').mkdir()
            elif case=='symlink_member':
                (copied/'MATHEMATICS.md').unlink();(copied/'MATHEMATICS.md').symlink_to('README.md')
            elif case=='changed_manifest':
                p=copied/'MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            elif case=='changed_archive':
                archive=tmp/'altered.zip';archive.write_bytes(args.archive.read_bytes()+b' ')
            results.append(rejected(lambda:v.freeze_controls(copied,archive),case))
        copied_sources=tmp/'sources';shutil.copytree(args.source_dir,copied_sources)
        p=copied_sources/'owr2016.pdf';b=bytearray(p.read_bytes());b[-20]^=1;p.write_bytes(b)
        results.append(rejected(lambda:v.source_controls(args.author_dir,copied_sources),'same_length_source_corruption'))
    # Portable normal, -O, -OO and environment-variable runs must be byte-identical.
    base=[str(root/'independent_verify.py'),'--author-dir',str(args.author_dir),
          '--archive',str(args.archive),'--source-dir',str(args.source_dir)]
    modes=[('normal',[],{}),('optimized',['-O'],{}),('doubly_optimized',['-OO'],{}),
           ('environment_optimized',[],{'PYTHONOPTIMIZE':'2'})]
    outputs=[];optimization=[];author=[]
    base_env={k:v for k,v in os.environ.items() if k != "PYTHONOPTIMIZE"}
    for name,flags,env in modes:
        run=subprocess.run([sys.executable,'-B',*flags,*base],cwd='/tmp',capture_output=True,
                           env={**base_env,**env})
        check(run.returncode==0,'independent replay failed: '+name+' '+run.stderr.decode())
        outputs.append(run.stdout)
        # Deliberately false runtime requirement must still raise in optimized subprocesses.
        sentinel='import runpy; d=runpy.run_path('+repr(str(root/'independent_verify.py'))+'); d["need"](False,"optimization sentinel")'
        false=subprocess.run([sys.executable,'-B',*flags,'-c',sentinel],cwd='/tmp',capture_output=True,
                             env={**base_env,**env})
        check(false.returncode!=0 and b'optimization sentinel' in false.stderr,'optimization disabled a check')
        optimization.append({'mode':name,'replay':'PASS','false_runtime_requirement_rejected':True})
        a=subprocess.run([sys.executable,'-B',*flags,str(args.author_dir/'verify_release.py'),
                          '--source-dir',str(args.source_dir)],cwd='/tmp',capture_output=True,
                         env={**base_env,**env})
        check(a.returncode==0,'author replay failed '+name)
        direct=subprocess.run([sys.executable,'-B',*flags,str(args.author_dir/'verify_math.py')],
                              cwd='/tmp',capture_output=True,env={**base_env,**env})
        check(direct.returncode==0 and direct.stdout==(args.author_dir/'expected_math.json').read_bytes(),
              'direct author mathematical optimization replay failed '+name)
        author_sentinel='import runpy; d=runpy.run_path('+repr(str(args.author_dir/'verify_math.py'))+'); d["require"](False,"author optimization sentinel")'
        author_false=subprocess.run([sys.executable,'-B',*flags,'-c',author_sentinel],cwd='/tmp',
                                    capture_output=True,env={**base_env,**env})
        check(author_false.returncode!=0 and b'author optimization sentinel' in author_false.stderr,
              'author optimization disabled a runtime check')
        n=subprocess.run([sys.executable,'-B',*flags,str(args.author_dir/'verify_negative_controls.py')],
                         cwd='/tmp',capture_output=True,env={**base_env,**env})
        check(n.returncode==0,'author negatives failed '+name)
        author.append({'mode':name,'release':json.loads(a.stdout),'negative_controls':json.loads(n.stdout),
                       'direct_math_byte_replay':'PASS','false_author_runtime_requirement_rejected':True})
    check(all(out==outputs[0] for out in outputs),'optimization changed independent result bytes')
    check(outputs[0]==(root/'independent_results.json').read_bytes(),'independent expected result drift')
    examined=[root/'independent_verify.py',Path(__file__),args.author_dir/'verify_math.py',
              args.author_dir/'verify_release.py',args.author_dir/'verify_negative_controls.py']
    for p in examined:
        check(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(p.read_text()))),
              'optimization-sensitive assert present in '+p.name)
    print(json.dumps({'status':'PASS','independent_corruptions_rejected':len(results),
                     'independent_corruption_cases':results,'index_two_sublattice_control':'PASS',
                     'optimization_modes':optimization,'assert_statements':0,
                     'author_replay':author},indent=2,sort_keys=True))

if __name__=='__main__':main()
