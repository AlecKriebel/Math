from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts";W=T/"admin_scope/packet"
pins={"DRIVER_CONTROLS.py":"3ff99091083bca1e8c2beb54238865d86cd4fefcb0c42da9f83278aff49cb88d","PUBLIC_VERIFY.py":"101928f4a7217437e9085c1f9e3a2c87938fa683a35670d1c9d8ad5b9e65669f"}
results=[]
for n,pin in pins.items():
 assert hashlib.sha256((W/n).read_bytes()).hexdigest()==pin
 cmd=[sys.executable,"-I","-B",str(W/n)]+(["--controls-only"]if n=="PUBLIC_VERIFY.py"else[])
 r=subprocess.run(cmd,cwd=T,capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
 a=json.loads(r.stdout);assert a["result"]in["MOCKED_GUARDS_PASS","PASS_METADATA_PROJECTION_CONTROLS_ONLY"]
 if n=="DRIVER_CONTROLS.py":
  assert len(a["controls"])==49 and all(x["control_pass"]for x in a["controls"])
  guard=[x for x in a["controls"]if x["case"]=="actual_pending_gate_rejected_read_only"];assert len(guard)==1 and guard[0]["accepted"]is False
 else:assert len(a["controls"])==13
 dest=M/("ROOT_V4_PENDING_"+n.removesuffix(".py")+"_CONTROLS.json");dest.write_text(r.stdout)
 results.append({"checker":n,"sha256":pin,"controls":len(a["controls"]),"result":a["result"],"receipt":dest.name})
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_PENDING_GATE_REJECTED_AND_CANONICAL_METADATA_CONTROLS","actual_current_readiness_result":json.loads((T/"FINAL_READINESS.json").read_text())["result"],"actual_current_publication_authorized":False,"source_manifest_sha256":"b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa","results":results,"API_or_publication_mutation":False}
(M/"ROOT_V4_PENDING_ADMIN_GUARDS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":out["result"],"controls":[x["controls"]for x in results],"production_authorized":False}))

