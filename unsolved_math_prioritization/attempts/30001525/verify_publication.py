#!/usr/bin/env python3
"""Externally anchored source-free replay; finite checks do not prove all-degree claims."""
import argparse, hashlib, json, shutil, stat, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
PINS={
 'packet/MANIFEST.json':'b1af9079189bd88ba892e682dc848de46448237539e68b5f624cab2aaab253fa',
 'independent_audit/AUDIT_MANIFEST.json':'8b49a48a912741102e20a28555abd12e399f5ac3755c13bc77b76e8df1d8b5b8',
 'independent_audit/patched/MANIFEST.json':'60c9eda3262986779bd268570aebc485ff28f0e5f45338f449df451a2db1479f'}
MODES=('normal','-O','-OO')
def require(ok,message):
    if not ok: raise RuntimeError(message)
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def safe(name):
    require(isinstance(name,str),'Nonstring path')
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p)==name and name!='.' and '\\' not in name,'Unsafe path')
def integrity(anchor):
    p=ROOT/'PUBLIC_MANIFEST.json'
    require(stat.S_ISREG(p.lstat().st_mode),'Manifest must be a regular file')
    b=p.read_bytes();require(digest(b)['sha256']==anchor,'External manifest anchor mismatch')
    m=json.loads(b);require(m['problem_id']==30001525 and m['status']=='unsolved' and m['turns']=='5/5','Disposition mismatch')
    names=set(m['files']);require('PUBLIC_MANIFEST.json' not in names,'Self-reference')
    names.add('PUBLIC_MANIFEST.json');dirs=set()
    for name in names:
        safe(name);dirs.update(str(p) for p in PurePosixPath(name).parents if str(p)!='.')
    found=set();found_dirs=set()
    for p in ROOT.rglob('*'):
        name=p.relative_to(ROOT).as_posix();mode=p.lstat().st_mode
        if stat.S_ISREG(mode):found.add(name)
        elif stat.S_ISDIR(mode):found_dirs.add(name)
        else:raise RuntimeError('Nonregular or linked member: '+name)
    require(found==names and dirs==found_dirs,'Exact inventory mismatch')
    for name,meta in m['files'].items():require(digest((ROOT/name).read_bytes())==meta,'Payload mismatch: '+name)
    for name,pin in PINS.items():
        p=ROOT/name;raw=p.read_bytes();require(digest(raw)['sha256']==pin,'Frozen manifest mismatch: '+name)
        entries=json.loads(raw)['files'];seen=set()
        for e in entries:
            safe(e['path']);require(e['path'] not in seen,'Duplicate manifest entry');seen.add(e['path'])
            require(digest((p.parent/e['path']).read_bytes())=={k:e[k] for k in ('bytes','sha256')},'Frozen payload mismatch: '+e['path'])
    return m

def child(path,mode,cwd):
    command=[sys.executable,'-I','-B']+([] if mode=='normal' else [mode])+[str(path)]
    r=subprocess.run(command,cwd=cwd,text=True,capture_output=True,timeout=300)
    require(r.returncode==0,'Child failed: '+path.name+' '+mode+' '+r.stderr)
    return r.stdout.strip()

def main(anchor):
    m=integrity(anchor);runs=[]
    frozen=json.loads((ROOT/'independent_audit/AUDIT_RESULTS.json').read_bytes())
    expected=json.loads(json.dumps(frozen));verified=sum(e['verified'] for e in expected['source_byte_verification'])
    for e in expected['source_byte_verification']:
        e['verified']=False;e['reason']='Public PDF absent; mathematical checks do not require copied sources.'
    expected['optimization_safe_check_count']-=verified
    require(frozen['optimization_safe_check_count']==6486 and expected['optimization_safe_check_count']==6480,'Check-count qualification changed')
    for mode in MODES:
        with tempfile.TemporaryDirectory(prefix='skyline-public-replay-') as td:
            temp=Path(td);copy=temp/'relocated package';shutil.copytree(ROOT,copy)
            cwd=temp/'different working directory';cwd.mkdir()
            require(not (copy/'sources').exists(),'Source-free replay required')
            audit=copy/'independent_audit'
            output=child(audit/'audit_verify.py',mode,cwd)
            actual=json.loads((audit/'AUDIT_RESULTS.json').read_bytes())
            require(actual==expected,'Independent audit replay differs beyond explicitly absent PDF verification')
            child(audit/'build_patches.py',mode,cwd)
            for name in ('PATCHES.diff','patched/verify.py','patched/PROOF.md'):
                require((audit/name).read_bytes()==(ROOT/'independent_audit'/name).read_bytes(),'Actual correction patch replay mismatch: '+name)
            child(audit/'patched/verify.py',mode,cwd)
            require((audit/'patched/TEST_RESULTS.json').read_bytes()==(ROOT/'packet/TEST_RESULTS.json').read_bytes(),'Corrected verifier output changed')
            tests=actual['child_process_tests'];require(len(tests)==30,'Child-test count mismatch')
            false_passes=[t for t in tests if t['version']=='original' and t['mode']!='normal' and t['case']!='unmodified']
            rejections=[t for t in tests if t['version']=='patched' and t['case']!='unmodified']
            require(len(false_passes)==8 and all(t['returncode']==0 for t in false_passes),'Original optimized false-PASS diagnostic mismatch')
            require(len(rejections)==12 and all(t['returncode']!=0 for t in rejections),'Corrected mathematical mutants were not rejected')
            runs.append({'mode':mode,'independent_checks':actual['optimization_safe_check_count'],'S4_degrees':101,'audit_child_processes':30,'corrected_mathematical_mutant_rejections':12,'original_optimized_false_passes':8,'actual_patch_reproduced':True,'corrected_output_byte_identical':True,'source_PDF_bytes_checked':0})
    integrity(anchor)
    return {'result':'PASS_SOURCE_FREE_PUBLICATION','problem_id':30001525,'status':'unsolved','turns':'5/5','manifest_sha256':anchor,'packet_files':len(m['files'])+1,'frozen_files_unchanged':True,'runs':runs,'scope':'Finite exact and integrity checks only; all-degree partial results depend on the written proof and cited theorems. Original optimized execution is explicitly invalid as mathematical validation. No full S8 or arbitrary-n cyclic skyline basis; no novelty claim.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest-sha256',required=True);args=parser.parse_args()
    print(json.dumps(main(args.manifest_sha256),indent=2,sort_keys=True))
