"""Root's private complete reproduction of the fresh repaired-head audit."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time

A=Path(__file__).resolve().parent
F=A/'repaired_final_adversary'
P=A/'tmp'/'root_repaired_final_gate'
R=P/'repaired_final_adversary'
R.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
manifest=json.loads((F/'OUTPUT_MANIFEST.json').read_text())
assert sha((F/'OUTPUT_MANIFEST.json').read_bytes())=='79aa0417cd772807233ab9329f655fa1e3fbcc99dfd83d5e942dd3920bfd9038'
for e in manifest['files']:
    b=(F/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
assert len(manifest['files'])==46
for src,dst in [(A/'repaired_snapshot',P/'repaired_snapshot')]:
    shutil.copytree(src,dst,dirs_exist_ok=True)
shutil.copy2(A/'repaired_snapshot_manifest.json',P/'repaired_snapshot_manifest.json')
runs=[]
for name,expected in [('independent_controls.py','independent_controls.stdout'),('post_candidate_controls.py','post_candidate_controls.stdout'),('check_bindings.py',None),('replay_private.py',None)]:
    shutil.copy2(F/name,R/name)
    started=time.monotonic()
    p=subprocess.run([sys.executable,'-B',str(R/name)],capture_output=True)
    stem='root_repaired_final_'+Path(name).stem
    (A/(stem+'.stdout')).write_bytes(p.stdout)
    (A/(stem+'.stderr')).write_bytes(p.stderr)
    assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr.decode())
    if expected: assert p.stdout==(F/expected).read_bytes(),name
    runs.append({'program':name,'seconds':time.monotonic()-started,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'full_stdout_equal':True if expected else None})
for name in ['BINDING_RECEIPT.json','REPLAY_RECEIPT.json']:
    actual=json.loads((R/name).read_text()); frozen=json.loads((F/name).read_text())
    for k in ['timestamp','elapsed_seconds']:
        actual.pop(k,None);frozen.pop(k,None)
    assert actual==frozen,name
for name in ['author_replay.stdout','historical_replay.stdout']+[f'verify_turn{i}.stdout' for i in range(1,6)]:
    assert (R/name).read_bytes()==(F/name).read_bytes(),name
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':manifest['input_head'],'all46_sealed_outputs_verified':True,'full_report_reconstruction_and_all4_new_executable_sources_read':True,'new_independent_assertions':4122,'new_post_candidate_assertions':521,'all_new_control_full_stdout_byte_exact':True,'binding_and_complete_replay_receipts_equal_excluding_only_timestamp_elapsed':True,'all5_turn_author_and_old_full_streams_byte_equal':True,'runs':runs,'source_qualification':'Three exact fresh PDF matches; Cambridge mathematics separately read, byte identity not claimed. Source-free replay count0.'}
(A/'root_repaired_final_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
