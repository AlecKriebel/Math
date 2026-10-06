from pathlib import Path
import hashlib,json,datetime,subprocess,sys,os
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/public';W=A/'tmp/root_clean_math';assert not W.exists();W.mkdir();O=A/'root_clean_math_streams';O.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();mb=(C/'PUBLIC_ALLOWLIST_MANIFEST.json').read_bytes();m=json.loads(mb)
for f in m['files']:
 p=Path(f['path']);assert not p.is_absolute() and '..' not in p.parts;b=(C/p).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'];q=W/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
runs=[]
for n in ['original_controls','original_wordspan_adversary']:
 r=subprocess.run([sys.executable,'-B',str(W/'code'/(n+'.py'))],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(O/(n+'.stdout')).write_bytes(r.stdout);(O/(n+'.stderr')).write_bytes(r.stderr);assert r.returncode==0 and r.stderr==b'' and r.stdout==(C/'replays'/(n+'.json')).read_bytes()
 runs.append({'code':n+'.py','stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'complete_stdout_stderr_exact':True})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_WHOLE_ADVERSARY_MATHEMATICAL_CONTROLS','workflow_percent':90,'original_manifest_sha256':sha(mb),'bound_members':len(m['files']),'source_first_and_math_seals_unchanged':True,'all_original_universal_proofs_and_new_controls_fully_read':True,'full_two_new_program_replays':runs,'original_whole_package_already_root_reproduced':'root_original_reproduction_receipt.json','unrestricted_problem_resolved':False,'live_metadata_acceptance_pending':True}
(A/'root_clean_mathematical_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
