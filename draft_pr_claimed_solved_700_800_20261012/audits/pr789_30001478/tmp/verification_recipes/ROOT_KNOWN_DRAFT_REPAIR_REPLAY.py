from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts";W=T/"admin_scope/packet";p=W/"KNOWN_DRAFT_REPAIR_CONTROLS.py"
pin="917eb3eb201f8bd6ba628f8e93d738c1c7a447d3aa42de42ac3e571286c19cb5";assert hashlib.sha256(p.read_bytes()).hexdigest()==pin
runs=[]
for opt in[False,True]:
 dest=T/"admin_scope"/("KNOWN_DRAFT_REPAIR_CONTROLS_ROOT_"+("O"if opt else"NORMAL")+".json")
 r=subprocess.run([sys.executable,"-I","-B"]+(["-O"]if opt else[])+[str(p),"--out",str(dest)],cwd=T,capture_output=True,text=True,timeout=120)
 assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
 a=json.loads(dest.read_text());assert a["result"]=="MOCKED_KNOWN_DRAFT_REPAIR_CONTROLS_PASS"and a["controls"]==40 and a["credentials_read"]is False and a["network_accessed"]is False and a["real_mutations"]is False
 (M/("ROOT_KNOWN_DRAFT_REPAIR_CONTROLS_"+("O"if opt else"NORMAL")+".json")).write_bytes(dest.read_bytes())
 runs.append({"optimized":opt,"controls":40,"result":a["result"],"receipt_sha256":hashlib.sha256(dest.read_bytes()).hexdigest()})
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","recipe_sha256":"e11b7f1426e28fbe0b3407dad777fb9ae4287213e1f5eabc96ad22f9bf36b8d2","independent_checker_sha256":pin,"driver_sha256":"a02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96","known_record_id":23423736,"runs":runs,"code_review_gaps_closed":["State reread cannot reach a different existing record","Missing PDF cannot be reuploaded by original stage","Driver pin authenticated before import"],"actual_record_updated":False,"scope":"Isolated behavior controls with fake token/state/HTTP; actual completed4review gate, snapshot and checkpoint separately required."}
(M/"ROOT_KNOWN_DRAFT_REPAIR_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS","modes":2,"controls_per_mode":40,"real_mutations":False}))

