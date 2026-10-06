#!/usr/bin/env python3
"""Replay the frozen author's verifier and explicit rejection tests in fresh copies.
This does not claim to prove mathematical semantics or resistance to replacing code
and its manifest together. The external archive pin supplies source identity.
"""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent/'author'

def need(ok,message):
    if not ok:raise ValueError(message)

def rehash(root,name):
    m=json.loads((root/'MANIFEST.json').read_text());raw=(root/name).read_bytes()
    m['files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    (root/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')

def execute(root,optimized=False):
    flags=['-I','-B']+(['-O'] if optimized else [])
    p=subprocess.run([sys.executable,*flags,str(root/'verify.py')],cwd='/',capture_output=True,text=True,timeout=90)
    return p

def run():
    tests=[]
    for optimized in [False,True]:
        p=execute(AUTHOR,optimized)
        need(p.returncode==0,'original replay failed')
        tests.append({'test':'frozen_baseline','optimized':optimized,'expect':'pass','passed':True,'returncode':p.returncode})
    cases=['relocated_baseline','extra_file','extra_bytecode','extra_cache_directory','expected_directory','expected_symlink','expected_fifo','missing_file','same_size_tamper','manifest_extra_key','manifest_missing_key','claim_wrong_id','claim_wrong_status','claim_wrong_n','claim_wrong_lower','claim_wrong_upper','claim_wrong_start','claim_wrong_stop','claim_wrong_intervals','claim_wrong_degree','claim_wrong_coefficient','forged_results','exploration_certified']
    claim_changes={'claim_wrong_id':('problem_id',30001168),'claim_wrong_status':('status','solved'),'claim_wrong_n':('n',3),'claim_wrong_lower':('weight_lower',[998,1000]),'claim_wrong_upper':('weight_upper',[1002,1000]),'claim_wrong_start':('time_start',[1,5]),'claim_wrong_stop':('time_stop',[2,1]),'claim_wrong_intervals':('intervals',749),'claim_wrong_degree':('last_degree',7),'claim_wrong_coefficient':('a2_n4',[1,90])}
    for case in cases:
      with tempfile.TemporaryDirectory(prefix='yamabe-audit-') as tmp:
        root=Path(tmp)/'relocated'/ 'author';shutil.copytree(AUTHOR,root)
        if case=='extra_file':(root/'unlisted.txt').write_text('unexpected')
        elif case=='extra_bytecode':(root/'certificate.pyc').write_bytes(b'not executable bytecode')
        elif case=='extra_cache_directory':(root/'__pycache__').mkdir()
        elif case.startswith('expected_'):
            target=root/'proof.md';target.unlink()
            if case=='expected_directory':target.mkdir()
            elif case=='expected_symlink':target.symlink_to(root/'README.md')
            elif case=='expected_fifo':os.mkfifo(target)
        elif case=='missing_file':(root/'proof.md').unlink()
        elif case=='same_size_tamper':
            target=root/'proof.md';raw=target.read_bytes();target.write_bytes(b'!'+raw[1:])
        elif case.startswith('manifest_'):
            m=json.loads((root/'MANIFEST.json').read_text())
            if case=='manifest_extra_key':m['files']['../unexpected']={'bytes':0,'sha256':'0'*64}
            else:del m['files']['proof.md']
            (root/'MANIFEST.json').write_text(json.dumps(m))
        elif case in claim_changes:
            target=root/'claim.json';d=json.loads(target.read_text());key,value=claim_changes[case];d[key]=value;target.write_text(json.dumps(d));rehash(root,'claim.json')
        elif case=='forged_results':
            target=root/'RESULTS.json';d=json.loads(target.read_text());d['worst_interval_index']=1;target.write_text(json.dumps(d));rehash(root,'RESULTS.json')
        elif case=='exploration_certified':
            target=root/'EXPLORATORY_RESULTS.json';d=json.loads(target.read_text());d['certified_signs']=True;target.write_text(json.dumps(d));rehash(root,'EXPLORATORY_RESULTS.json')
        for optimized in [False,True]:
            p=execute(root,optimized);expected=case=='relocated_baseline'
            need((p.returncode==0)==expected,'unexpected mutation outcome: '+case)
            tests.append({'test':case,'optimized':optimized,'expect':'pass' if expected else 'reject','passed':True,'returncode':p.returncode})
    checks=[]
    for optimized in [False,True]:
        flags=['-I','-B']+(['-O'] if optimized else [])
        with tempfile.TemporaryDirectory(prefix='yamabe-independent-') as tmp:
            script=Path(tmp)/'independent_check.py';shutil.copyfile(HERE/'independent_check.py',script)
            p=subprocess.run([sys.executable,*flags,str(script)],cwd='/',capture_output=True,text=True,timeout=90)
            need(p.returncode==0,'independent relocation failed')
            need(json.loads(p.stdout)==json.loads((HERE/'INDEPENDENT_RESULTS.json').read_text()),'independent result changed')
            checks.append({'test':'independent_normal_or_optimized_relocated','optimized':optimized,'passed':True})
    return {'status':'PASS','accepted_author_manifest_sha256':hashlib.sha256((AUTHOR/'MANIFEST.json').read_bytes()).hexdigest(),'author_test_count':len(tests),'author_tests':tests,'independent_tests':checks,'limitations':'Pinned-source integrity and enumerated mutations only. Not a formal proof and not protection against jointly rewriting code plus manifest.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
