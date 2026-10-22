from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");W=T/"admin_scope/packet";M=T/"root-receipts"
pin="702b8dbf1b6a71a8b721910d57a3bfdd1990e18d8b605eb2a4a0cdcd5445ded1"
assert hashlib.sha256((W/"DRIVER_CONTROLS.py").read_bytes()).hexdigest()==pin
r=subprocess.run([sys.executable,"-I","-B",str(W/"DRIVER_CONTROLS.py")],cwd=T,capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);v=json.loads(r.stdout);assert v["result"]=="MOCKED_GUARDS_PASS"
(M/"ROOT_ADMIN_V3_GUARD_CONTROLS.json").write_text(r.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_V3_ADMIN_GUARD_CONTROLS","checker_script_sha256":pin,"driver_sha256":hashlib.sha256((T/"publication_driver.py").read_bytes()).hexdigest(),"source_manifest_sha256":"50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de","source_files":151,"controls_receipt_sha256":hashlib.sha256(r.stdout.encode()).hexdigest(),"production_or_tracker_mutation":False,"completed_whole_reviews_required":2,"actual_current_terminal_gate_exists":(T/"FINAL_READINESS.json").exists(),"scope":"Mocked guard/coupling/path/type/eligibility tests against real six artifacts, not a mathematical or priority proof. Final actual publication, tracker, merge and admin seal remain pending."}
(M/"ROOT_ADMIN_V3_GUARD_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":out["result"],"script_sha256":pin,"production_mutation":False}))
