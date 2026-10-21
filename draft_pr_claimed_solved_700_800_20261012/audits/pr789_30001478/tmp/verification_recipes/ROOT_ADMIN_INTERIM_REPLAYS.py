from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");W=T/"admin_scope/packet";M=T/"root-receipts";D=T/"root_admin_interim";D.mkdir(exist_ok=True);assert not(M/"ROOT_ADMIN_INTERIM_REPLAYS.json").exists()
pins={"DRIVER_CONTROLS.py":"a7fb28e9e1e5d0b736302bb2569e0f94ce6b35f46c6b844176f8d9d3a2e0b6a6","MERGE_SCOPE.py":"175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff"}
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_INTERIM_ADMIN_REPLAYS","not_final_sealed_administrative_acceptance":True,"pins":pins,"checks":[]}
for name,args in[("DRIVER_CONTROLS.py",[]),("MERGE_SCOPE.py",["--base","5c2581a075676de40c70feb617d85311c8dd80a4","--public-github"])]:
 assert hashlib.sha256((W/name).read_bytes()).hexdigest()==pins[name]
 p=subprocess.run([sys.executable,"-I","-B",str(W/name)]+args,cwd=T,env=dict(os.environ,TMPDIR=str(D)),capture_output=True,text=True,timeout=240);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);value=json.loads(p.stdout)
 assert value["result"]in("PASS_REPAIRED_DRIVER_CONTROLS","PASS_SCOPE_DESIGN_AND_CONTROLS","PASS","MOCKED_GUARDS_PASS"),value.get("result")
 (M/("ROOT_ADMIN_INTERIM_"+name.removesuffix(".py")+".json")).write_text(p.stdout)
 out["checks"].append({"script":name,"result":value["result"],"stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()})
(M/"ROOT_ADMIN_INTERIM_REPLAYS.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":out["result"],"checks":out["checks"]}))
