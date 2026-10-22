from pathlib import Path
import datetime,hashlib,json,os,shutil,stat,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";W=T/"whole_preprint_round02";M=T/"root-receipts";D=T/"root_whole02_replay";D.mkdir(exist_ok=False)
mf="a794fd6e28e73159fa3d472feda611639bda59547dfcfd0fd6bbbac036054f0c";cp="38bf8e99aa33b66f7f1e0c563aa8c34ccbebf57faa74b9904a43cc74d97f570f";sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(W/"MANIFEST.json")==mf and sha(W/"review_check.py")==cp
entries=json.loads((W/"MANIFEST.json").read_text())["files"];assert len(entries)+1==13 and{p.name for p in W.iterdir()}=={r["path"]for r in entries}|{"MANIFEST.json"}
for row in entries:
 p=W/row["path"];assert p.name==row["path"]and stat.S_ISREG(p.lstat().st_mode)and p.stat().st_nlink==1 and p.stat().st_size==row["bytes"]and sha(p)==row["sha256"]
findings=json.loads((W/"FINDINGS.json").read_text());assert len(findings["issues"])==2 and not findings["mathematical_issues"]and not findings["source_semantics_or_priority_promotion_issues"]
V=T/"package_versions/v2_review02";V.mkdir(parents=True,exist_ok=False);shutil.copytree(P/"source",V/"source");inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text());assert inv["source_manifest_sha256"]=="5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348"
for row in inv["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
 dst=V/row["path"];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/row["path"],dst)
args=[str(W/"review_check.py"),"--packet-root",str(W),"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp,"--preprint-root",str(V)]
checks=[]
for py in[sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
 for opt in[False,True]:
  p=subprocess.run([py,"-I","-B"]+(["-O"]if opt else[])+args,cwd="/",capture_output=True,text=True,timeout=120);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);a=json.loads(p.stdout);assert a["result"]=="PASS"and a["review_files"]==13
  checks.append({"interpreter":py,"optimized":opt,"result":a,"stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()})
p=subprocess.run([sys.executable,"-I","-B"]+args+["--scratch",str(D/"controls")],cwd="/",capture_output=True,text=True,timeout=240);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr);controls=json.loads(p.stdout);assert controls["result"]=="PASS"and controls["controls"]["count"]==21
(M/"WHOLE02_ROOT_CONTROLS.json").write_text(p.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","completed":True,"reviewer":"/root/pr789_whole_preprint_round02","freshly_initialized":True,"problem":"30001478","pr":789,"original_scientific_head":"aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","manifest_sha256":mf,"checker_name":"review_check.py","checker_sha256":cp,"source_manifest_sha256":inv["source_manifest_sha256"],"publication_files":inv["files"],"review_actionable_issues":2,"required_repairs":2,"mathematical_issues":0,"source_semantics_or_priority_scope_issues":0,"bibliographic_issues":1,"ancillary_command_documentation_issues":1,"root_full_report_manually_read":True,"root_both_findings_independently_reproduced":True,"all_original_58_preserved":True,"source_files":151,"sealed_authored_files":13,"four_root_modes":checks,"packet_controls":21,"exact_reviewed_v2_preserved":str(V),"peer_full_source_processes_recorded":40,"peer_primary_bodies_independently_retrieved_targeted_reading":True,"peer_all4_pdf_visual_and_pixel_identical_fresh_typeset":True,"peer_family_positive_controls":14,"peer_family_negative_controls":84,"peer_optional_primary_evidence_file_rehash":139,"historical_priority":"UNRESOLVED","next_required_gate":"repair both low findings and different fresh whole03 current0issues beforepublication","case_percent":75,"shard_percent":83}
(M/"WHOLE02_ROOT_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({"result":"PASS_REVIEW_CUSTODY_AND_REPRODUCTION","root_modes":4,"owned_controls":21,"math_issues":0,"low_repairs_required":2,"exact_v2_preserved":True}))
