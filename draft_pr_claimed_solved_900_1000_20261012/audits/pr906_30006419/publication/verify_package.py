#!/usr/bin/env python3
"""Authenticate PR906's closed package and replay in isolated disposable copies."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

PIN='acab12ef33c8e2dc566337cfe01b94f2fe81f06ede4b31f1c363e055741fb0df'
HEAD='32eaecaa8907dbf674e65b138b000cdcc49004ae'
PROOFS={'author/PROOF.md':'2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef',
        'author/KOREVAAR_SCHOEN.md':'4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe'}

def require(ok,message):
    if not ok: raise RuntimeError(message)

def read_regular(path):
    before=path.lstat()
    require(stat.S_ISREG(before.st_mode),'Nonregular path: '+str(path))
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
    try:
        opened=os.fstat(fd)
        require(stat.S_ISREG(opened.st_mode) and
                (before.st_dev,before.st_ino)==(opened.st_dev,opened.st_ino),
                'Path changed while opening: '+str(path))
        with os.fdopen(fd,'rb',closefd=False) as f: return f.read()
    finally: os.close(fd)

def sha(data): return hashlib.sha256(data).hexdigest()

def validate(root,expected=None,pdf=None):
    require(not root.is_symlink() and root.is_dir(),'Invalid package root')
    require(not Path(__file__).is_symlink(),'Symlinked verifier')
    raw=read_regular(root/'PACKAGE_MANIFEST.json')
    if expected is not None:
        require(bool(re.fullmatch(r'[0-9a-f]{64}',expected)) and sha(raw)==expected,
                'External package manifest anchor mismatch')
    m=json.loads(raw)
    require(m['problem_id']=='30006419' and type(m['pr']) is int and m['pr']==906,
            'Wrong target scope')
    require(m['original_pr_head']==HEAD and m['original_public_manifest_sha256']==PIN,
            'Wrong original provenance')
    records=m['files'];require(isinstance(records,dict) and records,'Empty payload inventory')
    directories=set()
    for name,record in records.items():
        require(isinstance(name,str),'Nonstring path')
        q=PurePosixPath(name)
        require(not q.is_absolute() and q.as_posix()==name and '\\' not in name and
                all(p not in ('','.','..') for p in q.parts),'Unsafe payload path')
        require(type(record['bytes']) is int and record['bytes']>=0 and
                isinstance(record['sha256'],str) and
                re.fullmatch(r'[0-9a-f]{64}',record['sha256']),'Invalid hash record')
        directories.update(p.as_posix() for p in q.parents if p.as_posix()!='.')
    files,dirs=set(),set()
    for path in root.rglob('*'):
        mode=path.lstat().st_mode;name=path.relative_to(root).as_posix()
        if stat.S_ISREG(mode): files.add(name)
        elif stat.S_ISDIR(mode): dirs.add(name)
        else: raise RuntimeError('Symlink or special entry: '+name)
    require(files==set(records)|{'PACKAGE_MANIFEST.json'},'File inventory mismatch')
    require(dirs==directories,'Directory inventory mismatch')
    for name,record in records.items():
        data=read_regular(root/name)
        require(len(data)==record['bytes'] and sha(data)==record['sha256'],
                'Payload mismatch: '+name)
    packet=root/'original_packet'
    require(sha(read_regular(packet/'PUBLIC_MANIFEST.json'))==PIN,'Original public pin mismatch')
    for name,pin in PROOFS.items():
        require(sha(read_regular(packet/name))==pin,'Original proof pin mismatch: '+name)
    if pdf is not None:
        data=read_regular(pdf);record=records['note.pdf']
        require(len(data)==record['bytes'] and sha(data)==record['sha256'],'Separate PDF mismatch')
    return m,sha(raw)

def equivalent(actual,expected,path='result'):
    """Historical tolerances with explicit bool/numeric type separation."""
    if isinstance(expected,bool):
        require(type(actual) is bool and actual==expected,'Boolean mismatch: '+path)
    elif isinstance(expected,float):
        require(type(actual) in (float,int) and math.isfinite(actual) and
                math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-10),
                'Numerical replay mismatch: '+path)
    elif isinstance(expected,dict):
        require(isinstance(actual,dict) and actual.keys()==expected.keys(),'Key mismatch: '+path)
        for key in expected: equivalent(actual[key],expected[key],path+'/'+key)
    elif isinstance(expected,list):
        require(isinstance(actual,list) and len(actual)==len(expected),'List mismatch: '+path)
        for i,item in enumerate(expected): equivalent(actual[i],item,path+'/'+str(i))
    else:
        require(type(actual) is type(expected) and actual==expected,'Exact replay mismatch: '+path)

def worker(root,pin):
    require(sys.flags.optimize==0,'Replay worker must be nonoptimized')
    validate(root,pin)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    with tempfile.TemporaryDirectory(prefix='pr906-package-replay-') as td:
        temp=Path(td);r=temp/'package';shutil.copytree(root,r)
        def run(name,*args):
            result=subprocess.run([sys.executable,'-I','-B',str(r/name),*map(str,args)],
                    cwd=temp,env=env,capture_output=True,text=True,timeout=600)
            require(result.returncode==0,'Replay failed: '+name+'\n'+result.stderr)
            return json.loads(result.stdout)
        spec=importlib.util.spec_from_file_location('pr906_original_verifier',
                                                  r/'original_packet/verify_publication.py')
        original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
        original.equivalent=equivalent
        historical=original.replay(r/'original_packet',PIN)
        require(historical['status']=='PASS' and historical['author_exact_controls']==257 and
                historical['audit_b_executed_mixed_checks']==673 and
                historical['source_identity_checks_omitted']==2,'Historical replay scope mismatch')
        mutations=run('original_packet/mutation_tests.py','--expected-manifest',PIN)
        require(mutations['status']=='PASS' and mutations['rejected_mutations']==67,
                'Historical mutation count mismatch')
        proofdir='reviews/reshetnyak_proof_family/'
        review_integrity=run(proofdir+'verify_manifest.py')
        require(review_integrity['public_allowlist_passed'],'Proof review inventory failed')
        saved=read_regular(r/(proofdir+'CONTROL_RESULTS.json'))
        proof=run(proofdir+'independent_controls.py')
        require(proof['all_passed'] is True and proof['check_count']==6,'Proof finite controls failed')
        equivalent(json.loads(read_regular(r/(proofdir+'CONTROL_RESULTS.json'))),json.loads(saved))
        (r/(proofdir+'CONTROL_RESULTS.json')).write_bytes(saved)
        ks_path=temp/'ks_results.json'
        ks=run('reviews/ks_proof_family/independent_checks.py','--output',ks_path)
        require(ks['passed'] is True and ks['failures']==[],'KS finite controls failed')
        ks_full=json.loads(ks_path.read_text())
        ks_saved=json.loads(read_regular(r/'reviews/ks_proof_family/CHECK_RESULTS.json'))
        equivalent({k:v for k,v in ks_full.items() if k!='utc'},
                   {k:v for k,v in ks_saved.items() if k!='utc'})
        independent_path=temp/'independent_results.json'
        run('reviews/computation_family/independent_checker.py','--packet',r/'original_packet',
            '--output',independent_path)
        independent=json.loads(independent_path.read_text())
        require(independent['status']=='PASS' and independent['exact_control_count']==43,
                'Independent computation scope mismatch')
        equivalent(independent,json.loads(read_regular(
            r/'reviews/computation_family/INDEPENDENT_RESULTS_normal.json')))
        extended_path=temp/'extended_results.json'
        run('reviews/computation_family/replay_and_mutation_checker.py',
            '--packet',r/'original_packet','--mutations-only','--output',extended_path)
        extended=json.loads(extended_path.read_text())
        require(extended['status']=='PASS' and extended['extended_rejected_mutations']==19 and
                all(x['rejected'] is True for x in extended['mutations']),
                'Extended mutation scope mismatch')
        validate(r,pin);validate(root,pin)
    return {'status':'PASS','problem_id':'30006419','package_manifest_sha256':pin,
            'historical_replay':historical,'original_integrity_mutations':67,
            'fresh_proof_control_families':6,'fresh_KS_controls':ks,
            'fresh_exact_computation_controls':43,'extended_integrity_controls':extended,
            'child_optimization_level':0,'strict_bool_numeric_comparator':True,
            'source_retrieval_performed':False,
            'scope':'Finite exact/mixed/numerical checks and integrity support the written analytic proofs; no formal proof or priority certification.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest')
    ap.add_argument('--pdf',type=Path)
    ap.add_argument('--integrity-only','--check-only',action='store_true')
    ap.add_argument('--worker',action='store_true',help=argparse.SUPPRESS)
    args=ap.parse_args();root=Path(__file__).absolute().parent
    manifest,pin=validate(root,args.expected_manifest,args.pdf)
    if args.integrity_only:
        result={'status':'PASS_INTEGRITY','problem_id':'30006419','payload_files':len(manifest['files']),
                'package_manifest_sha256':pin,'external_anchor_checked':args.expected_manifest is not None}
    elif args.worker:
        result=worker(root,pin)
    else:
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
        proc=subprocess.run([sys.executable,'-I','-B',str(root/'verify_package.py'),
                            '--worker','--expected-manifest',pin],env=env,cwd=root.parent,
                            capture_output=True,text=True,timeout=1800)
        require(proc.returncode==0,'Isolated replay failed:\n'+proc.stderr)
        result=json.loads(proc.stdout);validate(root,pin,args.pdf)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
