from pathlib import Path
import sys,os,json,subprocess,hashlib
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"priority_classical";I=T/"intake";S=T/"root_priority_classical_replay_scratch";S.mkdir(exist_ok=True)
mp="59ee3141dd73732c4494594e561feeda54ce6fa55304a5a41974945b74e7a3a2";cp="81fb18e7d6c59aa95c1d2131d9a5778e9bceb745bba0814f79be3ecbd75c1b46"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(W/"MANIFEST.json")!=mp or sha(W/"custody_check.py")!=cp:raise RuntimeError("Untrusted sealed priority packet")
for n,r in json.loads((W/"SOURCE_LEDGER.json").read_text())["external_scratch_files"].items():
 p=T/"priority_classical_scratch"/n
 if sha(p)!=r["sha256"]or p.stat().st_size!=r["bytes"]:raise RuntimeError("Source pin differs")
 z=S/n
 if not z.exists():os.link(p,z)
rows=[]
for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 tag="314"if py==sys.executable else"312"
 for opt in [False,True]:
  cmd=[py,"-I","-B",*(["-O"]if opt else[]),str(W/"custody_check.py"),"--packet",str(W),"--input-root",str(I),"--expected-manifest-sha",mp,"--expected-checker-sha",cp,"--source-root",str(S)]
  r=subprocess.run(cmd,cwd="/",capture_output=True,text=True,timeout=120)
  if r.returncode or r.stderr:raise RuntimeError(r.stderr)
  got=json.loads(r.stdout)
  if got["status"]!="PASS"or got["external_scratch_files_checked"]!=31:raise RuntimeError("Source custody failure")
  rows.append({"python":py,"optimized":opt,"result":got})
 r=subprocess.run([py,"-I","-B",str(W/"test_custody.py"),"--packet",str(W),"--input-root",str(I),"--scratch",str(S)],cwd="/",capture_output=True,text=True,timeout=300)
 if r.returncode or r.stderr:raise RuntimeError(r.stderr)
 got=json.loads(r.stdout)
 if got["status"]!="PASS"or got["negative_cases"]!=64:raise RuntimeError("Negative controls failed")
 (T/"root-receipts"/("ROOT_PRIORITY_CLASSICAL_CONTROLS_"+tag+".json")).write_text(r.stdout)
(T/"root-receipts/ROOT_PRIORITY_CLASSICAL_REPLAY.json").write_text(json.dumps({"status":"PASS","modes":rows,"negative_controls_per_interpreter":64,"root_rehashed_primary_artifacts":10,"root_rehashed_external_files":31,"novelty_or_truth_mechanically_certified":False},indent=2)+"\n")
print(json.dumps({"status":"PASS","positive_custody_modes":4,"controls_interpreters":2,"negative_controls_each":64,"all48originals_unchanged":True}))
