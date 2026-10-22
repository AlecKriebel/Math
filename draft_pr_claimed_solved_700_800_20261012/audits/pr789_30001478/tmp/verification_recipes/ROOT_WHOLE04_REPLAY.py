from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";W=T/"whole_preprint_round04";scratch=T/"root_whole04_replay";scratch.mkdir(exist_ok=False)
MF="2b5c5913281f9acae38ce23d700fc9eb587ebb43e69747080f9ad6caaf8934a6";CP="184a9758ad377710af8dcb02b72dd7614e0f7afb3658bac3b44ac7c33be53d9c"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(W/"MANIFEST.json")==MF and sha(W/"verify_review.py")==CP
entries=json.loads((W/"MANIFEST.json").read_text())["files"];assert len(entries)==36
actual={p.relative_to(W).as_posix()for p in W.rglob("*")if p.is_file()};assert actual=={x["path"]for x in entries}|{"MANIFEST.json"}
for e in entries:
 p=W/e["path"];assert stat.S_ISREG(p.lstat().st_mode)and p.stat().st_nlink==1 and p.stat().st_size==e["bytes"]and sha(p)==e["sha256"]
v=json.loads((W/"VERDICT.json").read_text());assert v["result"]=="PASS_COMPLETE_WHOLE_PREPRINT_REVIEW"and v["actionable_findings"]==[]and v["completion_percent"]==100
assert v["source_manifest_sha256"]==sha(S/"MANIFEST.json")=="b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa"and v["severity_counts"]=={"critical":0,"high":0,"medium":0,"low":0}
py312="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
args=["--packet",str(W),"--expected-manifest-sha256",MF,"--expected-checker-sha256",CP,"--source",str(S),"--package",str(P)]
modes=[]
for py in[sys.executable,py312]:
 for opt in[False,True]:
  r=subprocess.run([py,"-I","-B"]+(["-O"]if opt else[])+[str(W/"verify_review.py")]+args+["--replay"],cwd="/",capture_output=True,text=True,timeout=90)
  assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(r.stdout)
  assert a["result"]=="PASS"and a["own_files"]==37 and a["own_math_replayed"]is True and a["source_files"]==151
  modes.append({"python":py,"optimized":opt,"result":a,"stdout_sha256":hashlib.sha256(r.stdout.encode()).hexdigest()})
controls=[]
for i,py in enumerate([sys.executable,py312]):
 dest=M/("WHOLE04_PACKET_CONTROLS_"+str(i)+".json")
 r=subprocess.run([py,"-I","-B",str(W/"run_controls.py")]+args+["--scratch",str(scratch/("controls_"+str(i))),"--output",str(dest)],cwd="/",capture_output=True,text=True,timeout=180)
 assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(dest.read_text());assert a["result"]=="PASS"and a["positive_controls"]==2 and a["negative_controls"]==24 and a["expensive_candidate_core_repeated"]is False
 controls.append({"python":py,"result":"PASS","positive":2,"negative":24,"receipt":dest.name,"sha256":sha(dest)})
cores=json.loads((W/"receipts/CORE_REPLAYS.json").read_text());assert len(cores)==4
for c in cores:
 p=W/"receipts"/(c["label"]+".stdout.txt");assert c["returncode"]==0 and not c["stderr"]and sha(p)==c["stdout_sha256"]=="44ab8a183882c3d1e293c46b0a01065a3409dd78b36885b25d7aaf0fe472a8c1"
 a=json.loads(p.read_text());assert a["result"]=="PASS"and len(a["finite_replay_processes"])==10 and a["external_evidence_files_rehashed"]==0
b=json.loads((W/"receipts/OPTIONAL_BODY_CUSTODY.json").read_text());assert b["result"]=="PASS"and b["external_evidence_files_rehashed"]==139 and len(b["finite_replay_processes"])==4
bank=T/"whole_preprint_round04_scratch/primary";primary=[]
for row in json.loads((W/"PRIMARY_RETRIEVALS.json").read_text()):
 for suffix,key in[(".pdf","sha256"),(".txt","text_sha256")]:
  p=bank/(row["name"]+suffix);assert p.is_file()and not p.is_symlink()and p.stat().st_nlink==1 and sha(p)==row[key]
  if suffix==".pdf":assert p.stat().st_size==row["bytes"]
  primary.append({"name":p.name,"sha256":sha(p),"bytes":p.stat().st_size})
assert len(primary)==14
for e in entries:assert sha(W/e["path"])==e["sha256"]
inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","completed":True,"reviewer":"/root/pr789_whole_preprint_round04","freshly_initialized":True,"problem":"30001478","pr":789,"original_scientific_head":"aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","manifest_sha256":MF,"checker_name":"verify_review.py","checker_sha256":CP,"source_manifest_sha256":inv["source_manifest_sha256"],"publication_files":inv["files"],"review_actionable_issues":0,"required_repairs":0,"all_severity_counts":v["severity_counts"],"root_full_REPORT_three_complete_derivations_README_checker_control_sources_manually_read":True,"root_closed_files":37,"four_root_modes":modes,"root_control_runs":controls,"peer_full_core_outer_modes":4,"peer_full_inner_processes":40,"peer_separate_optional_body_custody_jobs":4,"peer_optional_external_files":139,"root_fresh_primary_files_rehashed":primary,"root_rehash_scope_is_byte_custody_not_full_new_reading":True,"canonical_metadata_only_delta_verified":True,"all149_other_source_files_andPDF_unchanged_fromV3":True,"priority_remains":"UNRESOLVED","external_human_peer_review":False,"formal_proof_verification":False,"case_percent":88,"shard_percent":83}
(M/"WHOLE04_ROOT_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","review_files":37,"checker_modes":4,"root_control_runs":2,"positive_per_run":2,"negative_per_run":24,"fresh_primary_bytes_rehashed_files":14,"remaining_actionable_issues":0}))

