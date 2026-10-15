"""Run unchanged, personally read original finite helpers in private ROOT folders."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A=Path(__file__).resolve().parent
R=A.parents[2]
S=A/'source_snapshot'
D=A/'root_original_actual_reproduction'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def encode(o):return (json.dumps(o,indent=2)+'\n').encode()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    raw=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
mf_raw=(A/'snapshot_manifest.json').read_bytes()
assert sha(mf_raw)=='7180aa194d0fe99806e8aed1a92cbbc456676f26e0b2a18ad24cfcef4cd77833'
mf=json.loads(mf_raw);assert len(mf['files'])==18 and mf['whole_repository_diff_files']==19
for z in mf['files']:
    p=S/z['relative_path'];raw=p.read_bytes()
    assert p.is_file() and not p.is_symlink() and len(raw)==z['bytes'] and sha(raw)==z['sha256']
    assert stat.S_IMODE(p.stat().st_mode)==0o444
assert (S/'verify_binary_process.py').read_bytes()==(S/'review/verify_binary_process.py').read_bytes()
assert (S/'PARTIAL.md').read_bytes()==(S/'review/PARTIAL.md').read_bytes()
assert (S/'binary_verification.json').read_bytes()==(S/'review/submitted_results.json').read_bytes()
ledger=(S/'turns.jsonl').read_bytes();turns=[json.loads(z) for z in ledger.splitlines()]
assert ledger.endswith(b'\n') and [z['turn'] for z in turns]==[1] and all(type(z['turn']) is int for z in turns)
with (A/'ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py').open('xb') as f:f.write(Path(__file__).read_bytes())
D.mkdir(mode=0o700,exist_ok=False)
operator=Path(__file__).read_bytes()
(D/'ROOT_EXECUTION_SOURCE.py').write_bytes(operator)
results={};captures=[]
for name,source_name,saved_name,count in [('current_author','verify_binary_process.py','binary_verification.json',885),('historical_submitted','review/verify_binary_process.py','review/submitted_results.json',885),('historical_independent','review/independent_checks.py','review/independent_results.json',3044)]:
    folder=D/name;folder.mkdir(mode=0o700)
    script=folder/'PRELAUNCH_SOURCE.py';source=(S/source_name).read_bytes();script.write_bytes(source)
    saved=(S/saved_name).read_bytes();(folder/'ORIGINAL_SAVED_RESULT.json').write_bytes(saved)
    if name=='historical_independent':(folder/'PARTIAL.md').write_bytes((S/'review/PARTIAL.md').read_bytes())
    argv=['/usr/bin/python3','-B',str(script)]
    rec={'schema':'pr45-root-unchanged-finite-helper-capture/v1','actual_execution':False,'completed':False,'pid':None,'argv':argv,'cwd':str(folder),'started_utc':stamp(),'source_origin':pin(S/source_name),'prelaunch_source':pin(script),'assertions_enabled':True,'stdin_supplied':False,'scientific_scope':'Finite rational identities only; no computational certification of infinite arbitrary couplings, source characterization, priority or novelty.'}
    with (folder/'stdout.bin').open('xb') as out,(folder/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=folder,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env={**os.environ,'PYTHONOPTIMIZE':'0','PYTHONDONTWRITEBYTECODE':'1'})
        rec.update(actual_execution=True,pid=child.pid)
        code=child.wait()
    rec.update(completed=True,exit_code=code,finished_utc=stamp(),source_unchanged=script.read_bytes()==source,stdout=pin(folder/'stdout.bin'),stderr=pin(folder/'stderr.bin'))
    actual=(folder/'independent_results.json').read_bytes() if name=='historical_independent' and code==0 else (folder/'stdout.bin').read_bytes()
    rec.update(byte_exact_saved_result=actual==saved,status='PASS' if code==0 and actual==saved and (folder/'stderr.bin').read_bytes()==b'' else 'FAIL')
    (folder/'CAPTURE.json').write_bytes(encode(rec));captures.append(rec)
    assert rec['status']=='PASS' and rec['source_unchanged'] is True
    parsed=json.loads(actual);assert equal(parsed,json.loads(saved))
    if name=='historical_independent':
        assert type(parsed['passed']) is int and parsed['passed']==count and type(parsed['failed']) is int and parsed['failed']==0 and len(parsed['checks'])==count and all(type(v) is str and v=='PASS' for v in parsed['checks'].values())
        assert equal(json.loads((folder/'stdout.bin').read_bytes()),{k:v for k,v in parsed.items() if k!='checks'})
    else:assert parsed['status']=='PASS' and type(parsed['exact_assertions']) is int and parsed['exact_assertions']==count
    (folder/'ACTUAL_RESULT.json').write_bytes(actual);results[name]=parsed
assert (S/'turns.jsonl').read_bytes()==ledger
record={'schema':'pr45-root-complete-original-helper-reproduction/v1','status':'PASS_ACTUAL_COMPLETE_UNCHANGED_ORIGINAL_HELPER_RESULTS','created_utc':stamp(),'actual_root_pid':os.getpid(),'original_head':'d9b4acf5d070d1f04ffac86a4f08916a5629ff16','source_snapshot_manifest_sha256':sha(mf_raw),'author_result':results['current_author'],'historical_submitted_result':results['historical_submitted'],'independent_result':results['historical_independent'],'all_three_entire_outputs_byte_exact':True,'all_three_entire_objects_typed_equal':True,'complete_actual_captures':captures,'original_ledger':pin(S/'turns.jsonl'),'original_ledger_entire_bytes_unchanged':True,'original_substantive_attempts':1,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_target_solved':False,'historical_runtime_or_human_peer_review_certified':False,'limitations':'Actual present executions of unchanged arithmetic only; written all-fixed-couplings reasoning and the broad characterization gap remain separate.'}
(D/'ROOT_REPRODUCTION_RESULT.json').write_bytes(encode(record))
assert Path(__file__).read_bytes()==operator
print(json.dumps({'status':record['status'],'actual_root_pid':os.getpid(),'actual_children':[z['pid'] for z in captures],'author_assertions':885,'historical_submitted_assertions':885,'independent_assertions':3044,'all_three_entire_outputs_byte_exact':True,'new_substantive_attempts':0,'full_target_solved':False,'root_result':pin(D/'ROOT_REPRODUCTION_RESULT.json')}))
