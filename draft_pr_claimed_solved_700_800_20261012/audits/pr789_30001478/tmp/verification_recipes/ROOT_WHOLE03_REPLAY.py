from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";W=T/"whole_preprint_round03";scratch=T/"root_whole03_replay";scratch.mkdir(exist_ok=False)
MF="daccffd8724d722877239b4daed73a7c5657134d71809d3a370049d61c4ff39c";CP="e3c6961ebfc89eb77a169f8e53b1c4861628055ea2586dfc78e1a22c276551e1"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(W/"MANIFEST.json")==MF and sha(W/"verify_review.py")==CP
entries=json.loads((W/"MANIFEST.json").read_text())["files"];assert len(entries)==42
assert {p.name for p in W.iterdir()}=={x["path"]for x in entries}|{"MANIFEST.json"}
for e in entries:
 p=W/e["path"];assert p.name==e["path"]and stat.S_ISREG(p.lstat().st_mode)and p.stat().st_nlink==1 and p.stat().st_size==e["bytes"]and sha(p)==e["sha256"]
v=json.loads((W/"VERDICT.json").read_text());assert v["verdict"]=="PASS_NO_REQUIRED_REPAIRS"and v["actionable_findings"]==[]and v["completion_percent"]==100
assert v["source_manifest_sha256"]==sha(S/"MANIFEST.json")=="50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de"
assert v["severity_counts"]=={"critical":0,"high":0,"medium":0,"low":0}
py312="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";modes=[]
bank=T/"whole_preprint_round03_scratch/primary"
args=["--packet-root",str(W),"--expected-manifest-sha256",MF,"--expected-checker-sha256",CP,"--source-root",str(S),"--release-root",str(P),"--primary-root",str(bank),"--replay"]
for py in[sys.executable,py312]:
 for opt in[False,True]:
  r=subprocess.run([py,"-I","-B"]+(["-O"]if opt else[])+[str(W/"verify_review.py")]+args,cwd="/",capture_output=True,text=True,timeout=60)
  assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
  a=json.loads(r.stdout);assert a["result"]=="PASS"and a["review_files"]==43 and a["fresh_primary_files_rehashed"]==23 and a["independent_math_replayed"]is True and a["actionable_findings"]==0
  modes.append({"python":py,"optimized":opt,"result":a,"stdout_sha256":hashlib.sha256(r.stdout.encode()).hexdigest()})
controls=[]
for i,py in enumerate([sys.executable,py312]):
 dest=M/("WHOLE03_PACKET_CONTROLS_"+str(i)+".json")
 r=subprocess.run([py,"-I","-B",str(W/"control_checker.py")]+args[:-1]+["--scratch",str(scratch/("controls_"+str(i))),"--output",str(dest)],cwd="/",capture_output=True,text=True,timeout=180)
 assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
 a=json.loads(dest.read_text());assert a["result"]=="PASS"and a["positive_controls"]==4 and a["negative_controls"]==20
 controls.append({"python":py,"result":"PASS","positive":4,"negative":20,"receipt":dest.name,"sha256":sha(dest)})
# Confirm all recorded full outer replay scopes, without representing custody as a new mathematical proof.
for name in["CORE_0_normal","CORE_0_O","CORE_1_normal","CORE_1_O","OPTIONAL_BODIES"]:
 a=json.loads((W/(name+".json")).read_text());b=json.loads(a["stdout"])
 assert a["returncode"]==0 and not a["stderr"]and b["result"]=="PASS"and len(b["finite_replay_processes"])==10
 assert b["external_evidence_files_rehashed"]==(139 if name=="OPTIONAL_BODIES"else 0)
for e in entries:
 p=W/e["path"];assert sha(p)==e["sha256"]and p.stat().st_nlink==1
inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","completed":True,"reviewer":"/root/pr789_whole_preprint_round03","freshly_initialized":True,"problem":"30001478","pr":789,"original_scientific_head":"aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","manifest_sha256":MF,"checker_name":"verify_review.py","checker_sha256":CP,"source_manifest_sha256":inv["source_manifest_sha256"],"publication_files":inv["files"],"review_actionable_issues":0,"required_repairs":0,"all_severity_counts":v["severity_counts"],"root_full_REPORT_and_three_complete_derivations_and_README_and_two_checker_sources_manually_read":True,"root_closed_files":43,"four_root_modes":modes,"root_control_runs":controls,"peer_recorded_full_core_outer_runs":4,"peer_recorded_full_optional_outer_runs":1,"peer_recorded_inner_processes_total":50,"peer_optional_external_evidence_files":139,"root_fresh_primary_rehash_scope_files":23,"priority_remains":"UNRESOLVED","external_human_peer_review":False,"formal_proof_verification":False,"case_percent":88,"shard_percent":83}
(M/"WHOLE03_ROOT_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","review_files":43,"checker_modes":4,"root_control_runs":2,"positive_controls_per_run":4,"negative_controls_per_run":20,"current_source":inv["source_manifest_sha256"],"remaining_actionable_issues":0}))

