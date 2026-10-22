from pathlib import Path
import os,sys,subprocess,json,hashlib
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp")
O=T/"intake/original/unsolved_math_prioritization/attempts/30001522";S=T/"root_reproduction_scratch";S.mkdir(exist_ok=True);out=T/"root_reproduction";out.mkdir(exist_ok=True)
identity=json.loads((T/"intake/ROOT_SOURCE_IDENTITY.json").read_text())
for x in identity["original_files"]:
 b=(T/"intake/original"/x["path"]).read_bytes()
 if len(b)!=x["bytes"] or hashlib.sha256(b).hexdigest()!=x["sha256"]:raise RuntimeError("Immutable input changed")
env=dict(os.environ,TMPDIR=str(S));rows=[]
for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 dest=out/("ORIGINAL_REPLAY_"+("314" if py==sys.executable else "312")+".json")
 r=subprocess.run([py,"-I","-B",str(O/"PUBLICATION_CONTROL_TESTS.py"),str(O),str(dest)],cwd="/",env=env,text=True,capture_output=True,timeout=1200)
 (out/(dest.stem+".stdout.txt")).write_text(r.stdout)
 if r.returncode or r.stderr:raise RuntimeError(r.stderr)
 data=json.loads(dest.read_text())
 if data["status"]!="PASS":raise RuntimeError("Replay failed")
 rows.append({"python":py,"full_modes":len(data["full_replays"]),"publication_negative_controls":len(data["publication_controls"]),"status":data["status"]})
for x in identity["original_files"]:
 if hashlib.sha256((T/"intake/original"/x["path"]).read_bytes()).hexdigest()!=x["sha256"]:raise RuntimeError("Original input modified")
(out/"ROOT_REPLAY_SUMMARY.json").write_text(json.dumps({"status":"PASS","rows":rows,"48_originals_unchanged":True,"finite_controls_formal_topology_proof":False},indent=2)+"\n")
print(json.dumps(rows))
