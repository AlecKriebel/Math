#!/usr/bin/env python3
"""Replay exact computations in isolated copies; never overwrite package evidence.

Requires Python 3.12 and SymPy 1.14.0 for the recorded byte-identical replay.
Run python replay.py --output /path/to/new_replay_report.json.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import sympy

ROOT=Path(__file__).resolve().parent
SCRIPTS=['branch_integrality.py','audit_independent_model.py','audit_division_free.py','audit_saved_cases.py','publication_controls.py']
EXPECTED=['exact_results.json','validation_controls.json','audit_independent_results.json','audit_division_free_results.json','audit_saved_results.json']

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def verify_manifest():
    path=ROOT/'MANIFEST.json'
    if not path.exists():
        return {'verified':False,'reason':'Manifest not yet generated; staging replay only.'}
    manifest=json.loads(path.read_text())
    expected=set(manifest['files'])
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=path}
    if actual!=expected:
        raise RuntimeError('Package file inventory differs from manifest')
    for rel,record in manifest['files'].items():
        raw=(ROOT/rel).read_bytes()
        if len(raw)!=record['bytes'] or digest(raw)!=record['sha256']:
            raise RuntimeError('Manifest mismatch: '+rel)
    return {'verified':True,'files':len(expected),'manifest_sha256':digest(path.read_bytes())}

def process(command,cwd):
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    env.pop('PYTHONPATH',None)
    return subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True)

def run_mode(mode):
    flags=['-O'] if mode=='optimized' else []
    with tempfile.TemporaryDirectory(prefix='low_twist_replay_') as tmp:
        check=Path(tmp)/'checks';shutil.copytree(ROOT/'checks',check)
        # A result is trusted only after a fresh successful producer run.
        for name in EXPECTED+['publication_controls_results.json']:
            target=check/name
            if target.exists():target.unlink()
        records=[]
        for name in SCRIPTS:
            print(mode+': '+name,flush=True,file=sys.stderr)
            completed=process([sys.executable,*flags,name],check)
            if completed.returncode:
                raise RuntimeError(mode+' '+name+' failed: '+completed.stderr.splitlines()[-1])
            records.append({'script':name,'exit_code':0,'stdout':completed.stdout})
        comparisons={}
        for name in EXPECTED:
            produced=(check/name).read_bytes();expected=(ROOT/'checks'/name).read_bytes()
            if produced!=expected:raise RuntimeError(mode+' replay bytes differ: '+name)
            comparisons[name]={'bytes':len(produced),'sha256':digest(produced),'exact_match':True}
        if records[0]['stdout']!=(ROOT/'checks'/'optimized_run.txt').read_text():
            raise RuntimeError('Main stdout differs from recorded optimized run')
        controls=json.loads((check/'publication_controls_results.json').read_text())
        original=json.loads((check/'exact_results.json').read_text())
        mutations=[]
        for label in ['dimension','coverage','zero_witness','wrong_bidegree','wrong_branch']:
            mutated=json.loads(json.dumps(original))
            case=mutated['examples']['line'];result=case['search'][0]
            if label=='dimension':result['dimension']+=1
            elif label=='coverage':case['minimum_twist']+=1
            elif label=='zero_witness':result['witness_incidence_polynomial']='0'
            elif label=='wrong_bidegree':result['witness_incidence_polynomial']='z*a'
            elif label=='wrong_branch':result['witness_incidence_polynomial']='c'
            (check/'exact_results.json').write_text(json.dumps(mutated,indent=2)+'\n')
            completed=process([sys.executable,*flags,'audit_saved_cases.py'],check)
            if completed.returncode==0:raise RuntimeError('Saved-result mutation accepted: '+label)
            # Require the intended explicit checker failure, not an unrelated crash.
            if not completed.stderr.rstrip().splitlines()[-1].startswith('AssertionError:'):
                raise RuntimeError('Unexpected mutation failure: '+label)
            mutations.append({'mutation':label,'rejected':True,'exit_code':completed.returncode})
        return {'mode':mode,'scripts':records,'byte_comparisons':comparisons,
                'main_stdout_exact_match':True,'publication_controls':controls,
                'saved_result_mutations':mutations}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if sympy.__version__!='1.14.0':
        raise RuntimeError('Byte-exact replay requires SymPy 1.14.0')
    manifest=verify_manifest()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(run_mode,['normal','optimized']))
    if results[0]['publication_controls']!=results[1]['publication_controls']:
        raise RuntimeError('Normal/optimized control results differ')
    report={'status':'PASS','problem_id':30003253,'overall_problem_status':'UNSOLVED',
            'python':platform.python_version(),'sympy':sympy.__version__,
            'manifest_check':manifest,'isolated_replays':results,
            'scripts_sha256':{n:digest((ROOT/'checks'/n).read_bytes()) for n in SCRIPTS},
            'scope':'Exact replay of 12 authored examples, 49 searched spaces, 12 witnesses, 14 independent structural/regression checks, main controls, 17 added guard controls per mode, and 5 saved-result tamper controls per mode. No claim of a general surface criterion, new priority, external peer review, or formal proof verification.'}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:
        output=args.output.resolve()
        if output==ROOT or ROOT in output.parents:
            raise RuntimeError('Choose an output outside the immutable package')
        output.write_text(text)
    else:print(text,end='')
    print('PASS: isolated normal/-O replays, exact hashes, and mutation controls',file=sys.stderr)

if __name__=='__main__':main()
