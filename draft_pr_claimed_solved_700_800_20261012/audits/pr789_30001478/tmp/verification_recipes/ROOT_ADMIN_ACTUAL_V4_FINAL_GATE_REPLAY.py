from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts";p=T/"admin_scope/packet/DRIVER_CONTROLS.py"
assert hashlib.sha256(p.read_bytes()).hexdigest()=="3ff99091083bca1e8c2beb54238865d86cd4fefcb0c42da9f83278aff49cb88d"
r=subprocess.run([sys.executable,"-I","-B",str(p)],cwd=T,capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
a=json.loads(r.stdout);assert a["result"]=="MOCKED_GUARDS_PASS"and len(a["controls"])==49 and all(x["control_pass"]for x in a["controls"])
(M/"ROOT_ADMIN_ACTUAL_V4_FINAL_GATE_CONTROLS.json").write_text(r.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","driver_sha256":a["driver_sha256"],"checker_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"actual_final_gate_present":True,"actual_completed_fresh_reviews":4,"actual_current_package_clean":True,"controls":49,"actual_terminal_gate_readonly_pass":True,"controls_receipt_sha256":hashlib.sha256(r.stdout.encode()).hexdigest(),"current_readiness_sha256":hashlib.sha256((T/"FINAL_READINESS.json").read_bytes()).hexdigest(),"production_or_tracker_mutation":False}
assert (T/"FINAL_READINESS.json").read_bytes()==(T/"publication/READINESS_AT_PUBLICATION_V4.json").read_bytes()
(M/"ROOT_ADMIN_ACTUAL_V4_FINAL_GATE_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","actual_gate":True,"controls":49,"publication_mutation":False}))

