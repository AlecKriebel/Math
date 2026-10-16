from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"whole_review01_restarted";P=T/"package_versions/v1_review01";S=T/"root_whole01_replay";S.mkdir(exist_ok=True)
mp="fbf881db4593ffd94717cb3ff588db12c749bc726100490acb722657b36f2a7e";cp="70a29133907274743fb802f6e443c68c709afcd3c2014e54b4a6ea374510a33c"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(W/"MANIFEST.json")==mp and sha(W/"verify_review.py")==cp and sha(W/"REPORT.md")=="fdff14bd7752e6101923055b35fb8bf5242ac54fb40b22243429b85f9361a741"
m=json.loads((W/"MANIFEST.json").read_text());entries=m["files"];entries=entries if isinstance(entries,list)else[dict(path=n,**r)for n,r in entries.items()]
assert {p.name for p in W.iterdir()}=={r["path"]for r in entries}|{"MANIFEST.json"}
for row in entries:
 p=W/row["path"];assert p.name==row["path"]and stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink()and p.stat().st_size==row["bytes"]and sha(p)==row["sha256"]
rows=[]
for py in[sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 for optimized in[False,True]:
  args=[py,"-I","-B"]+(["-O"]if optimized else[])+[str(W/"verify_review.py"),"--packet-root",str(W),"--preprint-root",str(P),"--manifest-sha256",mp,"--checker-sha256",cp,"--primary-root",str(T/"scratch_whole_review01_restarted")]
  if py==sys.executable and not optimized:args+=["--replay"]
  r=subprocess.run(args,cwd="/",env=dict(os.environ,TMPDIR=str(S)),capture_output=True,text=True,timeout=300)
  if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
  data=json.loads(r.stdout);assert data["result"]=="PASS"and data["fresh_primary_files_rehashed"]==23 and data["historical_76_custody_reproduced"]is False
  rows.append({"python":py,"optimized":optimized,"result":data})
r=subprocess.run([sys.executable,"-I","-B",str(W/"test_review_controls.py"),"--packet-root",str(W),"--preprint-root",str(P),"--scratch-root",str(S),"--manifest-sha256",mp,"--checker-sha256",cp],cwd="/",env=dict(os.environ,TMPDIR=str(S)),capture_output=True,text=True,timeout=300)
if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
controls=json.loads(r.stdout);assert controls["result"]=="PASS"and controls["count"]==28
(T/"root-receipts/WHOLE01_ROOT_CONTROLS.json").write_text(r.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","manifest_sha256":mp,"checker_sha256":cp,"source_manifest_sha256":"bdfe29cd2a46d035cda5d83a101775283125c17b1f432b0f0f0994b5ba0819ff","closed_authored_files":len(entries)+1,"baseline_modes":rows,"packet_control_cases":28,"baseline_positives_in_control_cases":2,"damaged_packet_negatives_in_control_cases":26,"actionable_child_issues":0,"optional_date_observation":1,"root_scope_precision_to_apply":True,"historic76_body_bank_replayed_now":False,"fresh23_custody_replayed":True}
(T/"root-receipts/WHOLE01_ROOT_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","fresh_primary_files":23,"baseline_modes":4,"packet_control_cases":28,"required_child_repairs":0,"root_editorial_precision_and_date_pending":True}))
