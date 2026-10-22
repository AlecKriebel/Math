from pathlib import Path
import sys,os,json,subprocess,hashlib
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");W=T/"priority_question";I=T/"intake";S=T/"root_priority_question_replay_scratch";S.mkdir(exist_ok=True)
mp="bb312addd8615d21b2043764f194884232ed08b85a55bda688e5648dc89cc913";cp="c67eb9c3e4bbd518ae0737c5f32db7ed4d974223e84b14429d46e01ddf29b487"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(W/"MANIFEST.json")!=mp or sha(W/"verify_packet.py")!=cp:raise RuntimeError("Sealed question family pin differs")
records=[]
for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 tag="314"if py==sys.executable else"312"
 for opt in [False,True]:
  for bodies in [False,True]:
   cmd=[py,"-I","-B",*(["-O"]if opt else[]),str(W/"verify_packet.py"),"--packet-root",str(W),"--intake-root",str(I),"--manifest-sha256",mp,"--checker-sha256",cp]
   if bodies:cmd+=["--bodies-root",str(T/"priority_question_scratch")]
   r=subprocess.run(cmd,cwd="/",capture_output=True,text=True,timeout=120)
   if r.returncode or r.stderr:raise RuntimeError(r.stderr)
   got=json.loads(r.stdout)
   if got["result"]!="PASS"or got["external_body_files_replayed"]!=(33 if bodies else 0):raise RuntimeError("Body/core scope differs")
   records.append({"python":py,"optimized":opt,"fullbodycustody":bodies,"result":got})
 dest=T/"root-receipts"/("ROOT_PRIORITY_QUESTION_CONTROLS_"+tag+".json")
 r=subprocess.run([py,"-I","-B",str(W/"negative_controls.py"),"--packet-root",str(W),"--intake-root",str(I),"--bodies-root",str(T/"priority_question_scratch"),"--scratch-root",str(S),"--output",str(dest)],cwd="/",capture_output=True,text=True,timeout=300)
 if r.returncode or r.stderr:raise RuntimeError(r.stderr)
 got=json.loads(r.stdout)
 if got["result"]!="PASS"or got["negative_cases_per_mode"]!=12 or got["modes"]!=2:raise RuntimeError("Controls fail")
 summary=json.loads(dest.read_text())
 if sum(not x["expected_accept"]for x in summary["rows"])!=24 or not all(x["passed"]for x in summary["rows"]):raise RuntimeError("Stored control outcomes differ")
(T/"root-receipts/ROOT_PRIORITY_QUESTION_REPLAY.json").write_text(json.dumps({"status":"PASS","modes":records,"negative_controls_each_interpreter":24,"primary_versions":16,"full_external_pdf_text_render_rows":33,"all48originals_unchanged":True,"priority_or_absence_mechanically_certified":False},indent=2)+"\n")
print(json.dumps({"status":"PASS","core_full_interpreter_modes":8,"negative_controls_each_interpreter":24,"originals":48,"primary_versions":16}))
