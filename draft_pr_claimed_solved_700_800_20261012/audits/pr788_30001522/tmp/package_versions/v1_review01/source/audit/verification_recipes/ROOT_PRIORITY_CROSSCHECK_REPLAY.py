from pathlib import Path
import sys,hashlib,json,subprocess
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"priority_classical_crosscheck";S=T/"root_priority_crosscheck_replay_scratch";S.mkdir(exist_ok=True)
mp="59f34e7069f38d90cbc0a336b5069146a44f9fba06d88053701ca0f0f73f0395";cp="d4abcbb44bb2bce9374923d0f0c888e7dc3fd543a92b5ea7cf5a102f852aaa9d"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(W/"MANIFEST.json")!=mp or sha(W/"custody_check.py")!=cp:raise RuntimeError("Crosscheck seal pin")
rows=[]
for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 tag="314"if py==sys.executable else"312"
 for opt in [False,True]:
  r=subprocess.run([py,"-I","-B",*(["-O"]if opt else[]),str(W/"custody_check.py"),"--packet",str(W),"--case-root",str(T),"--expected-manifest-sha",mp,"--expected-checker-sha",cp],cwd="/",capture_output=True,text=True,timeout=120)
  if r.returncode or r.stderr:raise RuntimeError(r.stderr)
  got=json.loads(r.stdout)
  if got["status"]!="PASS"or got["direct_external_bindings"]!=64:raise RuntimeError("Bad source scope")
  rows.append({"python":py,"optimized":opt,"result":got})
 r=subprocess.run([py,"-I","-B",str(W/"test_custody.py"),"--packet",str(W),"--case-root",str(T),"--scratch",str(S)],cwd="/",capture_output=True,text=True,timeout=300)
 if r.returncode or r.stderr:raise RuntimeError(r.stderr)
 got=json.loads(r.stdout)
 if got["status"]!="PASS"or got["negative_cases"]!=30:raise RuntimeError("Crosscheck controls failed")
 (T/"root-receipts"/("ROOT_PRIORITY_CROSSCHECK_CONTROLS_"+tag+".json")).write_text(r.stdout)
(T/"root-receipts/ROOT_PRIORITY_CROSSCHECK_REPLAY.json").write_text(json.dumps({"status":"PASS","modes":rows,"negative_controls_each_interpreter":30,"oldseal_48_originals_unchanged":True,"truth_or_priority_mechanically_certified":False},indent=2)+"\n")
print(json.dumps({"status":"PASS","positive_modes":4,"negative_controls_each_interpreter":30,"C1_context_source_check":"PASS"}))
