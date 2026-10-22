from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"whole_review02";P=T/"preprint";S=T/"root_whole02_replay";S.mkdir(exist_ok=True)
mp="51d47023b58324c9b32406660f839de0bc350b69a29240de928d80d15b62bf3d";cp="53760033a9635614a2ed538d5b0cd265bda2a3368420fa859cf822a66dbfa218"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(W/"MANIFEST.json")!=mp or sha(W/"custody_check.py")!=cp:raise RuntimeError("Final whole-review pin differs")
entries=json.loads((W/"MANIFEST.json").read_text())["files"]
assert {p.name for p in W.iterdir()}=={r["path"]for r in entries}|{"MANIFEST.json"}
for row in entries:
 p=W/row["path"];assert p.name==row["path"]and stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink()and p.stat().st_size==row["bytes"]and sha(p)==row["sha256"]
verdict=json.loads((W/"VERDICT.json").read_text());assert not verdict["actionable_issues"]and not verdict["required_repairs"]and verdict["source_manifest_sha256"]=="0af7587170f147a5a0075ebeacb007cca8a4a4eee68d536bbe9339125622fd4d"
rows=[];other="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
for py in[sys.executable,other]:
 for optimized in[False,True]:
  args=[py,"-I","-B"]+(["-O"]if optimized else[])+[str(W/"custody_check.py"),"--packet",str(W),"--expected-manifest-sha256",mp,"--expected-checker-sha256",cp,"--preprint-root",str(P),"--primary-root",str(T/"scratch_whole_review02"),"--replay"]
  r=subprocess.run(args,cwd="/",env=dict(os.environ,TMPDIR=str(S)),capture_output=True,text=True,timeout=180)
  if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
  got=json.loads(r.stdout);assert got["result"]=="PASS"and got["preprint_inputs_rehashed"]==202 and got["primary_evidence_files_rehashed"]==19 and len(got["finite_replays"])==2
  rows.append({"python":py,"optimized":optimized,"result":got})
controls_path=T/"root-receipts/WHOLE02_ROOT_CONTROLS.json"
r=subprocess.run([sys.executable,"-I","-B",str(W/"custody_controls.py"),"--packet",str(W),"--scratch",str(S/"controls"),"--out",str(controls_path),"--preprint-root",str(P),"--primary-root",str(T/"scratch_whole_review02"),"--expected-manifest-sha256",mp,"--expected-checker-sha256",cp,"--other-python",other],cwd="/",env=dict(os.environ,TMPDIR=str(S)),capture_output=True,text=True,timeout=300)
if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
got=json.loads(r.stdout);assert got["result"]=="PASS"and got["controls"]==24
assert controls_path.read_bytes()==(W/"CUSTODY_CONTROL_RESULTS.json").read_bytes()
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","manifest_sha256":mp,"checker_sha256":cp,"source_manifest_sha256":verdict["source_manifest_sha256"],"authored_review_files":len(entries)+1,"baseline_modes":rows,"custody_control_cases":24,"baseline_positives":4,"rejection_cases":20,"sealed_control_receipt_byte_identical":True,"current202_inputs_bound":True,"fresh19_primary_evidence_bound":True,"historic76_replayed":False,"remaining_actionable_issues":[],"current_six_and_source_unchanged":True,"formal_topology_or_priority_certification":False}
(T/"root-receipts/WHOLE02_ROOT_REPLAY.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","authored_review_files":len(entries)+1,"baseline_modes":4,"current_inputs":202,"fresh_primary":19,"control_cases":24,"remaining_actionable_issues":0}))
