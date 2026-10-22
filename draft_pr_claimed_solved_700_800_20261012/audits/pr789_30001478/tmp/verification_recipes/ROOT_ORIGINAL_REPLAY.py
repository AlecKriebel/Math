from pathlib import Path
import datetime,hashlib,json,subprocess,os,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");I=T/"intake";A=I/"original/unsolved_math_prioritization/attempts/30001478";M=T/"root-receipts";W=T/"root_original_replay";W.mkdir(exist_ok=True)
idn=json.loads((I/"ROOT_SOURCE_IDENTITY.json").read_text());known={x["path"].split("attempts/30001478/",1)[1]:x for x in idn["original_files"]}
for n in["verify_publication.py","PUBLICATION_MANIFEST.json"]:
 b=(A/n).read_bytes();assert hashlib.sha256(b).hexdigest()==known[n]["sha256"]
pin=known["PUBLICATION_MANIFEST.json"]["sha256"];rows=[]
for py in[sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 for opt in[False,True]:
  cmd=[py,"-I","-B"]+(["-O"]if opt else[])+[str(A/"verify_publication.py"),"--expected-manifest",pin]
  run=subprocess.run(cmd,cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=1000)
  if run.returncode or run.stderr:raise RuntimeError(run.stdout+run.stderr)
  out=json.loads(run.stdout);assert out["status"]=="PASS"and out["regular_files"]==58 and out["immutable_archives"]==3 and out["immutable_archive_members"]==44 and[out["named_controls"]for out in out["control_suites"]]==[47,16,20]
  rows.append({"python":py,"optimized":opt,"result":out})
controls=subprocess.run([sys.executable,"-I","-B",str(A/"test_publication.py"),"--expected-manifest",pin,"--full-relocation"],cwd="/",env=dict(os.environ,TMPDIR=str(W)),capture_output=True,text=True,timeout=1000)
if controls.returncode or controls.stderr:raise RuntimeError(controls.stdout+controls.stderr)
ctrl=json.loads(controls.stdout);assert ctrl["status"]=="PASS"and ctrl["relocation_full_replay"]
(M/"ROOT_ORIGINAL_PUBLICATION_CONTROLS.json").write_text(json.dumps(ctrl,indent=2)+"\n")
receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","pr":789,"problem":"30001478","original_head":idn["reviewed_head"],"source_identity_sha256":hashlib.sha256((I/"ROOT_SOURCE_IDENTITY.json").read_bytes()).hexdigest(),"original_manifest_sha256":pin,"original_wrapper_sha256":known["verify_publication.py"]["sha256"],"original_files":58,"immutable_archives":3,"archive_members":44,"four_full_modes":rows,"wrapper_controls":ctrl,"actual_patch_test_replayed":True,"original_source_58_unchanged":True,"universal_proof_and_source_semantics_not_certified_by_finite_tests":True,"new_substantive_proof_turns":0,"case_percent":20,"shard_percent":83}
(M/"ROOT_ORIGINAL_REPLAY.json").write_text(json.dumps(receipt,indent=2)+"\n");print(json.dumps({"result":"PASS","original_files":58,"four_full_modes":4,"immutable_archives":3,"named_original_suites":[47,16,20],"wrapper_controls":ctrl["named_control_count"],"case_percent":20,"shard_percent":83}))
