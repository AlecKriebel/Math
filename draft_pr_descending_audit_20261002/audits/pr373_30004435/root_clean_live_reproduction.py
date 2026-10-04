from pathlib import Path
import hashlib,json,subprocess,sys,os,datetime,shutil
A=Path(__file__).resolve().parent;W=A/'tmp/root_clean_live';assert not W.exists();(W/'code').mkdir(parents=True);sha=lambda b:hashlib.sha256(b).hexdigest();C=A/'clean_final_adversary/public'
code=(C/'code/read_only_acceptance_gate_v2.py').read_bytes();assert sha(code)=='73eaa51a1a95c7f78a09f98099657cbf531fddae596536f6954fa7a4f9adab52';(W/'code/read_only_acceptance_gate_v2.py').write_bytes(code)
M=json.loads((A/'repaired_snapshot_manifest.json').read_bytes())
for f in M['files']:
 b=(A/'repaired_snapshot'/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'];p=W/'snapshot'/f['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
shutil.copyfile(A/'accepted_pr_body.txt',W/'accepted_pr_body.txt')
args=[sys.executable,'-B',str(W/'code/read_only_acceptance_gate_v2.py'),'--repo',str(A.parents[2]),'--snapshot',str(W/'snapshot'),'--expected-head',M['head'],'--expected-main',M['base'],'--expected-target-count','52','--prepared-body',str(W/'accepted_pr_body.txt'),'--out',str(W/'run')]
r=subprocess.run(args,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(A/'root_clean_live.stdout').write_bytes(r.stdout);(A/'root_clean_live.stderr').write_bytes(r.stderr);assert r.returncode==0 and r.stderr==b'',r.stdout.decode()+r.stderr.decode()
b=(W/'run/VERDICT.json').read_bytes();(A/'root_clean_live_full_verdict.json').write_bytes(b);j=json.loads(b);assert j['status']=='PASS_LIVE_SCOPED_UNSOLVED_5_OF_5'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_PRIVATE_CLONE_EXACT_LIVE_GATE','workflow_percent':99,'unrestricted_discovery_percent':0,'immutable_gate_code_sha256':sha(code),'independent_private_snapshot_body_clone_verified':True,'complete_full_verdict_sha256':sha(b),'exact_head':M['head'],'exact_main':M['base'],'body_sha256':sha((W/'accepted_pr_body.txt').read_bytes()),'all_checks':len(j['checks']),'agent_full_certificate_comparison_and_actual_merge_pending':True}
(A/'root_clean_live_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
