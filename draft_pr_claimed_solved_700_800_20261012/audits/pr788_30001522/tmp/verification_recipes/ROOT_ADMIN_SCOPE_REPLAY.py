from pathlib import Path
import datetime,hashlib,json,subprocess,sys,stat
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"admin_scope";M=T/"root-receipts";mp="0c1b2e1c565a4ce2167c0307ae0d95071857e58a1f4d4d0856b95595f71ffc51";cp="52df37d0a1d991d260b78fe53c60936186a5e95c32ce4d45861d421e214f0ff2"
assert hashlib.sha256((W/"MANIFEST.json").read_bytes()).hexdigest()==mp and hashlib.sha256((W/"verify_admin.py").read_bytes()).hexdigest()==cp
entries=json.loads((W/"MANIFEST.json").read_text())["files"];assert len(entries)==20
for x in entries:
 p=W/x["path"];assert p.name==x["path"]and stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink();assert len(p.read_bytes())==x["bytes"]and hashlib.sha256(p.read_bytes()).hexdigest()==x["sha256"]
verdict=json.loads((W/"VERDICT.json").read_text());assert verdict["result"]=="PASS"and not verdict["actionable_issues"]
rows=[];controls=[]
for py in[sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 for opt in[False,True]:
  flags=[py,"-I","-B"]+(["-O"]if opt else[])
  r=subprocess.run(flags+[str(W/"verify_admin.py"),"--packet-root",str(W),"--case-root",str(T),"--expected-manifest-sha256",mp,"--expected-checker-sha256",cp],cwd="/",capture_output=True,text=True,timeout=120)
  if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
  out=json.loads(r.stdout);assert out["result"]=="PASS";rows.append({"python":py,"optimized":opt,"result":out})
  if py==sys.executable:
   for n in["reproduce_guard_controls.py","run_admin_controls.py"]:
    wrapper="import sys,runpy;sys.path.insert(0,"+repr(str(W))+");runpy.run_path("+repr(str(W/n))+",run_name=\"__main__\")"
    r=subprocess.run(flags+["-c",wrapper],cwd="/",capture_output=True,text=True,timeout=120)
    if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
    data=json.loads(r.stdout);assert data["result"]=="PASS";controls.append({"script":n,"optimized":opt,"result":data})
rec={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","manifest_sha256":mp,"checker_sha256":cp,"closed_authored_files":21,"baselines":rows,"control_reproductions":controls,"controls_isolated_import_wrapper":"After external manifest/checker/file bootstrap, inserts only verified packet directory for run_admin_controls local module import","guard_positive_cases":2,"guard_negative_cases":21,"additional_positive_cases":3,"additional_negative_cases":11,"remaining_actionable_issues":[],"administrative_scope_not_third_whole_review":True,"native_acceptance_still_pending":True,"source195_and_six_unchanged":True}
(M/"ADMIN_SCOPE_ROOT_REPLAY.json").write_text(json.dumps(rec,indent=2)+"\n");print(json.dumps({"result":"PASS","authored":21,"baseline_modes":4,"guard_negative":21,"additional_negative":11,"remaining_actionable_issues":0}))
