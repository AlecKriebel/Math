"""Independently replay the stable whole-package controls in an owned private clone."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent
C=A/'clean_final_adversary'
W=A/'tmp/root_clean_package'
assert not W.exists()
(W/'public/controls').mkdir(parents=True)
(W/'public').mkdir(exist_ok=True)
O=A/'root_clean_package_streams';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
codes={}
for name in ['replay_package.py','final_gate.py']:
    source=C/'public/controls'/name
    codes[name]=sha(source.read_bytes())
    shutil.copyfile(source,W/'public/controls'/name)
(W/'private/sources').mkdir(parents=True)
sources=[]
for source in sorted((C/'private/sources').glob('*.pdf')):
    shutil.copyfile(source,W/'private/sources'/source.name)
    sources.append({'name':source.name,'sha256':sha(source.read_bytes()),'bytes':source.stat().st_size})
assert len(sources)==5
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
runs=[]
def run(label,args):
    r=subprocess.run([sys.executable,'-B',str(W/'public/controls'/args[0]),*args[1:]],cwd=W,env=env,capture_output=True)
    (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,(label,r.stderr.decode())
    assert r.stderr==b''
    assert r.stdout==(C/'public/logs'/(label+'.stdout')).read_bytes(),(label,'full stdout differs')
    assert r.stderr==(C/'public/logs'/(label+'.stderr')).read_bytes(),(label,'stderr differs')
    runs.append({'label':label,'returncode':0,'complete_stdout_stderr_byte_match':True,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
    print(label+': PASS full stdout/stderr byte-exact',flush=True)
run('package_replay',['replay_package.py','--snapshot',str(A/'snapshot'),'--own',str(W)])
local=json.loads((W/'public/package_replay_receipt.json').read_text())
remote=json.loads((C/'public/package_replay_receipt.json').read_text())
for receipt in [local,remote]:
    for record in receipt['records']:
        for key in ['started_utc','finished_utc','elapsed_seconds']:record.pop(key)
assert local==remote,'whole package receipt differs outside its declared timing fields'
for record in local['records']:
    for suffix in ['stdout','stderr']:
        name=record['label']+'.'+suffix
        b=(W/'public/logs'/name).read_bytes()
        assert b==(C/'public/logs'/name).read_bytes()
        (O/name).write_bytes(b)
run('final_gate_prepared',['final_gate.py','--inputs',str(A),'--own',str(W),'--git',str(A.parents[2]),'--source-dir',str(W/'private/sources')])
localgate=json.loads((W/'public/final_gate_prepared_receipt.json').read_text())
remotegate=json.loads((C/'public/final_gate_prepared_receipt.json').read_text())
localgate.pop('observed_utc');remotegate.pop('observed_utc')
assert localgate==remotegate,'whole prepared-gate receipt differs outside its single declared UTC field'
for name,digest in codes.items():assert sha((C/'public/controls'/name).read_bytes())==digest
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_WHOLE_PACKAGE','workflow_percent':96,'discovery_percent':0,'code_sha256':codes,'all_code_read_in_full_before_execution':True,'sources':sources,'runs':runs,'aggregate_programs':8,'entire_aggregate_receipt_matches_except_declared_timing':True,'entire_prepared_gate_receipt_matches_except_observed_utc':True,'prepared_gate_result':localgate['result'],'sealed_public_manifest_check_pending':True,'exact_live_body_ready_gate_and_actual_merge_pending':True}
(A/'root_clean_package_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'author_assertions':local['author_assertions'],'independent_assertions':local['historical_independent_assertions'],'prepared_gate':localgate['result']['status']},sort_keys=True))
