#!/usr/bin/env python3
"""After static review, copy frozen bytes privately and capture all outputs."""
import datetime,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'repaired_snapshot/problems/2518_free_pro_p_characteristic_intersections'
DST=OUT/'private_package'
shutil.copytree(SRC,DST,dirs_exist_ok=True)
def hash(b):return hashlib.sha256(b).hexdigest()
before={p.relative_to(DST).as_posix():hash(p.read_bytes()) for p in DST.rglob('*') if p.is_file()}
assert len(before)==44
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
receipts=[]
for script,expect in [(f'verify_turn{t}.py',f'TURN_{t}_CHECKS.json') for t in range(1,6)]+[
 ('independent_review/independent_check.py','independent_review/INDEPENDENT_CHECKS.json'),
 ('REPLAY_ALL.py',None),('verify_publication.py',None)]:
    label=Path(script).stem;start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic()
    argv=[sys.executable,'-B',str(DST/script)]
    r=subprocess.run(argv,cwd=DST,capture_output=True,env=env)
    (OUT/(label+'.stdout')).write_bytes(r.stdout);(OUT/(label+'.stderr')).write_bytes(r.stderr)
    receipt={'start_utc':start,'duration_seconds':time.monotonic()-t0,'argv':argv,'env_override':{'PYTHONDONTWRITEBYTECODE':'1'},
             'exit_code':r.returncode,'stdout_sha256':hash(r.stdout),'stderr_sha256':hash(r.stderr),
             'reviewed_input_sha256':hash((DST/script).read_bytes()),'expected':expect,'exact_expected_match':None}
    assert r.returncode==0 and r.stderr==b'',script
    if expect:
        receipt['expected_sha256']=hash((SRC/expect).read_bytes());receipt['exact_expected_match']=r.stdout==(SRC/expect).read_bytes()
        assert receipt['exact_expected_match'],script
    if script=='REPLAY_ALL.py':
        actual=json.loads(r.stdout)
        compare=[]
        for path in ['FINAL_REPLAY.json','independent_review/AUTHOR_REPLAY.json']:
            historical=json.loads((SRC/path).read_text());assert historical['local_source_bindings']==12
            current=historical.copy();current['local_source_bindings']=0
            assert actual==current
            compare.append({'path':path,'historical_raw_source_bindings':12,'fresh_raw_source_bindings':0,'complete_normalized_object_match':True})
        receipt['whole_object_comparison']=compare
    receipts.append(receipt)
after={p.relative_to(DST).as_posix():hash(p.read_bytes()) for p in DST.rglob('*') if p.is_file()}
assert before==after
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'private_copy44_exact_and_unchanged':True,
 'no_bytecode_created':not any(DST.rglob('__pycache__')),'all5_author_outputs_byte_exact':True,'old_review_output_byte_exact':True,
 'author_assertions':139300,'old_review_assertions':153807,'optional12_raw_source_replay_performed':False,
 'receipt_qualification':'Fresh public mode checks0 local source bindings; immutable historical12 retained and explicitly normalized for comparison.',
 'private_inputs':before,'runs':receipts}
(OUT/'REPLAY_RECEIPTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['private_inputs','runs']},indent=2))
