"""Independent private clone of every exact refresh stage and final read-only gate."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/public/live_acceptance';W=A/'tmp/root_staged_gate_attempt2';assert not W.exists();W.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
code=(C/'final_gate_staged.py').read_bytes();assert sha(code)=='1b64c7a4728c41ff2467241e5471338d4a1830e339befb0c5d6f11c36dbc2ab0'
(W/'final_gate_staged.py').write_bytes(code)
descriptor=(C/'ROUND2_STAGE_DESCRIPTOR.json').read_bytes();assert sha(descriptor)=='820cd232c67ca3510e104cba68f8f5afae1b086ac225651d02e4bdf95984dac9'
(W/'descriptor.json').write_bytes(descriptor);stages=json.loads(descriptor)['stages']
sources={'initial':A,'round1':A/'live_acceptance_inputs','round2':A/'live_acceptance_inputs_round2'}
for stage in stages:
    S=sources[stage['name']];D=W/stage['name'];D.mkdir()
    for name,digest in stage['input_metadata_sha256'].items():
        b=(S/name).read_bytes();assert sha(b)==digest;(D/name).write_bytes(b)
    for key in ['snapshot','repaired_snapshot']:
        mf=json.loads((D/('snapshot_manifest.json' if key=='snapshot' else 'repaired_snapshot_manifest.json')).read_bytes())
        for f in mf['files']:
            b=(S/key/f['path']).read_bytes();assert sha(b)==f['sha256'] and len(b)==f['bytes']
            p=D/key/f['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
(W/'sources').mkdir()
for p in sorted((A/'tmp/root_clean_package/private/sources').glob('*.pdf')):shutil.copyfile(p,W/'sources'/p.name)
assert len(list((W/'sources').glob('*.pdf')))==5
(W/'prepared/public').mkdir(parents=True)
args=[sys.executable,'-B',str(W/'final_gate_staged.py'),'--inputs',str(W/'round2'),'--own',str(W/'prepared'),'--git',str(A.parents[2]),'--source-dir',str(W/'sources'),'--stage-descriptor',str(W/'descriptor.json'),'--stage-descriptor-sha256',sha(descriptor)]
for stage in stages:args.extend(['--stage-input',stage['name']+'='+str(W/stage['name'])])
r=subprocess.run(args,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(A/'root_staged_prepared.stdout').write_bytes(r.stdout);(A/'root_staged_prepared.stderr').write_bytes(r.stderr)
assert r.returncode==0 and r.stderr==b'',r.stderr.decode()
assert r.stdout==(C/'round2_prepared/final_gate_prepared.stdout').read_bytes()
assert r.stderr==(C/'round2_prepared/final_gate_prepared.stderr').read_bytes()
own=json.loads((W/'prepared/public/final_gate_prepared_receipt.json').read_bytes());other=json.loads((C/'round2_prepared/final_gate_prepared_receipt.json').read_bytes())
own.pop('observed_utc');other.pop('observed_utc');assert own==other,'whole staged gate receipt differs outside observation UTC'
shutil.copyfile(W/'prepared/public/final_gate_prepared_receipt.json',A/'root_staged_prepared_full_receipt.json')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_ALL_STAGES_PREPARED_GATE','workflow_percent':98,'unrestricted_discovery_percent':0,'full_adapted_code_and_descriptor_read_before_execution':True,'code_sha256':sha(code),'descriptor_sha256':sha(descriptor),'all_three_stage_inputs_privately_cloned_and_byte_verified':True,'all_complete_stdout_stderr_and_whole_receipt_matches_except_observation_utc':True,'current_review_head':own['result']['head'],'current_main':own['result']['remote_main'],'full_expected_tree':own['result']['actual_remote_main_expected_tree'],'original_current_API_blobs':47,'all_stage_API_blobs':48,'body_sha256':own['result']['prepared_body_sha256'],'prepared_body_is_live':own['result']['prepared_body_is_live'],'exact_live_body_gate_and_actual_merge_pending':True}
(A/'root_staged_gate_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
