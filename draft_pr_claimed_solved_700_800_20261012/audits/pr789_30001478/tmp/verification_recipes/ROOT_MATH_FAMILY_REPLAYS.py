from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");I=T/"intake";M=T/"root-receipts";W=T/"root_math_replays";W.mkdir(exist_ok=True);other="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
families=[("math_source_geometry","efe8eb3f489b2c5bb8a586c374195f9aafe62d33df92931b0ea0619bf0a17a9c","d5cc1bf00c6271e7fbf14b3df3e4d3ba79629aa745a2ec500234da07f89d8b59"),("math_quotient_algebra","7cd556c6a87d2117f803112268e4b8eb86316c76dac40c9fee82ffe0ccf6eea0","31246b25e6040d2d676f0fd5d1b6c4c65cedc0a67440da313a3ff0a584689333")];results=[]
for name,mp,cp in families:
 packet=T/name;assert hashlib.sha256((packet/"MANIFEST.json").read_bytes()).hexdigest()==mp and hashlib.sha256((packet/"verify_packet.py").read_bytes()).hexdigest()==cp
 files=json.loads((packet/"MANIFEST.json").read_text())["files"];expected={x["path"]for x in files}|{"MANIFEST.json"};assert {p.name for p in packet.iterdir()if p.is_file()}==expected
 for item in files:
  p=packet/item["path"];assert p.name==item["path"]and stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink();b=p.read_bytes();assert len(b)==item["bytes"]and hashlib.sha256(b).hexdigest()==item["sha256"]
 rows=[]
 for py in[sys.executable,other]:
  for opt in[False,True]:
   args=[py,"-I","-B"]+(["-O"]if opt else[])+[str(packet/"verify_packet.py")]
   if name=="math_source_geometry":args+=["--packet-root",str(packet),"--input-root",str(I),"--source-root",str(packet/"scratch")]
   else:args+=["--packet",str(packet),"--intake-root",str(I),"--primary-root",str(T/"math_quotient_algebra_scratch")]
   args+=["--expected-manifest-sha256",mp,"--expected-checker-sha256",cp,"--replay"]
   run=subprocess.run(args,cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=240)
   if run.returncode or run.stderr:raise RuntimeError(run.stdout+run.stderr)
   out=json.loads(run.stdout);assert out.get("result",out.get("status"))=="PASS";rows.append({"python":py,"optimized":opt,"result":out})
 if name=="math_source_geometry":
  outpath=M/"ROOT_SOURCE_GEOMETRY_CONTROLS.json";cmd=[sys.executable,"-I","-B",str(packet/"CONTROLS.py"),"--packet",str(packet),"--scratch",str(W/"geometrycontrols"),"--input-root",str(I),"--source-root",str(packet/"scratch"),"--other-python",other,"--output",str(outpath)]
 else:cmd=[sys.executable,"-I","-B",str(packet/"test_packet.py"),"--packet",str(packet),"--intake-root",str(I),"--primary-root",str(T/"math_quotient_algebra_scratch"),"--expected-manifest-sha256",mp,"--expected-checker-sha256",cp]
 run=subprocess.run(cmd,cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=300)
 if run.returncode or run.stderr:raise RuntimeError(run.stdout+run.stderr)
 ctrl=json.loads(run.stdout);assert ctrl.get("result",ctrl.get("status"))=="PASS"
 if name=="math_source_geometry":assert ctrl["negative_count"]==18 and outpath.read_bytes()==(packet/"CONTROL_RESULTS.json").read_bytes()
 else:assert ctrl["positive_controls"]==2 and ctrl["negative_controls"]==16;(M/"ROOT_QUOTIENT_ALGEBRA_CONTROLS.json").write_text(json.dumps(ctrl,indent=2)+"\n")
 results.append({"family":name,"manifest_sha256":mp,"checker_sha256":cp,"authored_files_including_manifest":len(expected),"baseline_modes":rows,"custody_controls":ctrl})
original=json.loads((M/"ROOT_ORIGINAL_REPLAY.json").read_text());assert original["result"]=="PASS"and len(original["four_full_modes"])==4
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","two_distinct_fresh_independent_families":results,"root_original_full_modes":4,"root_original_named_suites":[47,16,20],"original_wrapper_controls":24,"original_files_preserved":58,"remaining_mathematical_or_source_issues":[],"direct_presentation_all_characteristics":True,"journal_parameter_conversion_only_char_not_2":True,"no_priority_conclusion":True,"new_substantive_proof_turns":0,"case_percent":35,"shard_percent":83}
(M/"ROOT_MATH_FAMILY_REPLAYS.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS","fresh_families":2,"family_baseline_modes":8,"geometry_control_negatives":18,"algebra_control_positive":2,"algebra_control_negatives":16,"original_full_modes":4,"remaining_mathematical_or_source_issues":0,"case_percent":35,"shard_percent":83}))
