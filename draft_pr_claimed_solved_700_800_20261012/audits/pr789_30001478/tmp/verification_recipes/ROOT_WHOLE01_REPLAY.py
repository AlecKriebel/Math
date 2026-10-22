from pathlib import Path
import datetime,hashlib,json,os,shutil,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";W=T/"whole_preprint_round01";M=T/"root-receipts";D=T/"root_whole01_replay";D.mkdir(exist_ok=False)
mf="01cdfc5148cf15b9251dd3a20f3c6cdcebc96f29576183634d6215c074d311a1";cp="d63c0aca0b293579c19ee7252b28fe8241862c5b73bf2ed0eee186d213e31884"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(W/"MANIFEST.json")==mf and sha(W/"verify_packet.py")==cp
entries=json.loads((W/"MANIFEST.json").read_text())["files"];assert len(entries)+1==41 and{p.name for p in W.iterdir()}=={r["path"]for r in entries}|{"MANIFEST.json"}
for row in entries:
 p=W/row["path"];assert row["path"]==p.name and stat.S_ISREG(p.lstat().st_mode)and p.stat().st_nlink==1 and p.stat().st_size==row["bytes"]and sha(p)==row["sha256"]
v=json.loads((W/"VERDICT.json").read_text());assert not v["required_repairs"]and len(v["nonblocking_findings"])==1 and v["completion_percent"]==100
inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text());V=T/"package_versions/v1_review01";V.mkdir(parents=True,exist_ok=False);shutil.copytree(P/"source",V/"source")
for row in inv["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
 src=P/row["path"];dst=V/row["path"];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
for row in inv["files"]:assert(V/row["path"]).stat().st_size==row["bytes"]and sha(V/row["path"])==row["sha256"]
py312="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";checks=[]
for py in[sys.executable,py312]:
 for opt in[False,True]:
  cmd=[py,"-I","-B"]+(["-O"]if opt else[])+[str(W/"verify_packet.py"),"--packet-root",str(W),"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp,"--preprint-root",str(V),"--replay"]
  p=subprocess.run(cmd,cwd="/",env=dict(os.environ,TMPDIR=str(D)),capture_output=True,text=True,timeout=120);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);a=json.loads(p.stdout);assert a["result"]=="PASS"and a["fresh_source_files_authenticated"]==151 and a["fresh_distribution_files_authenticated"]==6
  checks.append({"interpreter":py,"optimized":opt,"result":a})
cmd=[sys.executable,"-I","-B",str(W/"test_packet.py"),"--packet-root",str(W),"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp,"--scratch",str(D/"controls"),"--other-python",py312]
p=subprocess.run(cmd,cwd="/",capture_output=True,text=True,timeout=240);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);controls=json.loads(p.stdout);assert controls["result"]=="PASS";(M/"WHOLE01_ROOT_CONTROLS.json").write_text(p.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","completed":True,"reviewer":"/root/pr789_whole_preprint_round01","freshly_initialized":True,"problem":"30001478","pr":789,"original_scientific_head":"aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","manifest_sha256":mf,"checker_name":"verify_packet.py","checker_sha256":cp,"source_manifest_sha256":inv["source_manifest_sha256"],"publication_files":inv["files"],"review_actionable_issues":1,"required_repairs":0,"nonblocking_findings":1,"mathematical_issues":0,"source_credit_priority_scope_issues":0,"review_note":"L1 ancillary frozen standalone test_publication requires ordinary owned TMPDIR on Mac; core --replay unaffected. Root will clarify README before final fresh review.","all_original_58_preserved":True,"source_files":151,"sealed_authored_files":41,"four_root_modes":checks,"packet_positive_controls":controls["positive_controls"],"packet_negative_controls":controls["negative_controls"],"exact_reviewed_v1_preserved":str(V),"peer_full_source_processes_recorded":40,"peer_fresh_primary_PDFs_recorded":6,"peer_optional_body_count_recorded":139,"root_fresh_primary_file_rehash_in_this_packet_replay":0,"historical_priority":"UNRESOLVED","root_full_report_manually_read":True,"case_percent":75,"shard_percent":83}
(M/"WHOLE01_ROOT_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","root_modes":4,"packet_positives":controls["positive_controls"],"packet_negatives":controls["negative_controls"],"required_repairs":0,"nonblocking_note":1,"v1_preserved":True}))
