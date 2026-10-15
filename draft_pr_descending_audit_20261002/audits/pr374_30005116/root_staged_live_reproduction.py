from pathlib import Path
import subprocess,sys,json,hashlib,datetime,os,shutil
A=Path(__file__).resolve().parent;W=A/'tmp/root_staged_gate_attempt2';L=W/'live';assert not L.exists();(L/'public').mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((W/'final_gate_staged.py').read_bytes())=='1b64c7a4728c41ff2467241e5471338d4a1830e339befb0c5d6f11c36dbc2ab0'
assert sha((W/'descriptor.json').read_bytes())=='820cd232c67ca3510e104cba68f8f5afae1b086ac225651d02e4bdf95984dac9'
r=subprocess.run(['gh','pr','view','374','--json','headRefOid,isDraft,state,body,mergeable,mergeStateStatus'],capture_output=True);assert r.returncode==0 and not r.stderr
(A/'root_final_body_readback.stdout').write_bytes(r.stdout);(A/'root_final_body_readback.stderr').write_bytes(r.stderr);j=json.loads(r.stdout)
assert j['headRefOid']=='2bb07868e8fb5ac48cae8ec0b7f69aed02b36807' and j['state']=='OPEN' and not j['isDraft'] and j['body'].encode()==(A/'live_accepted_pr_body_round2.txt').read_bytes()
args=[sys.executable,'-B',str(W/'final_gate_staged.py'),'--inputs',str(W/'round2'),'--own',str(L),'--git',str(A.parents[2]),'--source-dir',str(W/'sources'),'--stage-descriptor',str(W/'descriptor.json'),'--stage-descriptor-sha256',sha((W/'descriptor.json').read_bytes()),'--require-exact-api-body','--require-ready']
for stage in json.loads((W/'descriptor.json').read_bytes())['stages']:args.extend(['--stage-input',stage['name']+'='+str(W/stage['name'])])
r=subprocess.run(args,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(A/'root_staged_live.stdout').write_bytes(r.stdout);(A/'root_staged_live.stderr').write_bytes(r.stderr);assert r.returncode==0 and r.stderr==b'',r.stderr.decode()
shutil.copyfile(L/'public/final_gate_live_receipt.json',A/'root_staged_live_full_receipt.json')
x=json.loads((L/'public/final_gate_live_receipt.json').read_bytes());assert x['result']['prepared_body_is_live'] and x['result']['phase']=='exact_live_acceptance'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_EXACT_LIVE_GATE','workflow_percent':99,'all_three_private_cloned_stages_used':True,'same_immutable_code_and_descriptor':True,'receipt_sha256':sha((A/'root_staged_live_full_receipt.json').read_bytes()),'full_result':x['result'],'agent_certificate_comparison_and_actual_merge_pending':True}
(A/'root_staged_live_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
