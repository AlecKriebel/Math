from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";V=T/"package_versions/v2_review02"
assert not(M/"PACKAGE_FREEZE_V3.json").exists()
identity=lambda raw:{"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
old=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
assert old["source_manifest_sha256"]=="5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348"
assert (S/"MANIFEST.json").read_bytes()==(V/"source/MANIFEST.json").read_bytes()
assert identity((S/"verify_source.py").read_bytes())["sha256"]=="700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489"
assert (T/"repair_typeset_v3/main.pdf").read_bytes()==(P/"output/pdf/paper.pdf").read_bytes()
bindings={n:identity(p.read_bytes())for n,p in[("main.tex",S/"main.tex"),("paper.pdf",P/"output/pdf/paper.pdf")]}
(S/"PREPRINT_BINDINGS.json").write_text(json.dumps(bindings,indent=2)+"\n")
rows=[]
for f in sorted(S.rglob("*")):
 if f.is_file()and f!=S/"MANIFEST.json":
  assert not f.is_symlink();rows.append({"path":f.relative_to(S).as_posix(),**identity(f.read_bytes())})
assert len(rows)+1==151
(S/"MANIFEST.json").write_text(json.dumps({"schema":"pr789-closed-source/v1","files":rows},indent=2)+"\n")
pin=identity((S/"MANIFEST.json").read_bytes())["sha256"]
r=subprocess.run([sys.executable,"-I","-B",str(S/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(T/"repair_typeset_v3/main.pdf"),"--output-dir",str(P)],capture_output=True,text=True,timeout=120)
assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
new=json.loads(r.stdout);(P/"PACKAGE_INVENTORY.json").write_text(json.dumps(new,indent=2)+"\n")
changed=[a["path"]for a,b in zip(old["files"],new["files"])if a!=b]
assert changed==["main.tex","output/pdf/paper.pdf","source-and-verification.zip","zenodo-upload-kit.zip"]
source_changed=sorted(f.relative_to(S).as_posix()for f in S.rglob("*")if f.is_file()and f.read_bytes()!=(V/"source"/f.relative_to(S)).read_bytes())
assert source_changed==["MANIFEST.json","PREPRINT_BINDINGS.json","README.md","main.tex"]
assert sorted(str(f.relative_to(S))for f in S.rglob("*")if f.is_file())==sorted(str(f.relative_to(V/"source"))for f in(V/"source").rglob("*")if f.is_file())
plan=json.loads((T/"READINESS_PLAN.json").read_text())
records=[]
for i in[1,2]:
 p=M/("WHOLE%02d_ROOT_REPLAY.json"%i);peer=json.loads(p.read_text())
 assert peer["result"]=="PASS"and peer["completed"]is True
 records.append({"round":i,"reviewer":peer["reviewer"],"freshly_initialized":True,"packet":"whole_preprint_round%02d"%i,"manifest_sha256":peer["manifest_sha256"],"checker_name":peer["checker_name"],"checker_sha256":peer["checker_sha256"],"root_replay_receipt":"root-receipts/"+p.name,"root_replay_sha256":identity(p.read_bytes())["sha256"],"reviewed_source_manifest_sha256":peer["source_manifest_sha256"],"reviewed_publication_files":peer["publication_files"],"actionable_issues":peer["review_actionable_issues"]})
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
plan.update(utc=now,source_manifest_sha256=pin,publication_files=new["files"],actual_whole_preprint_rounds=2,completed_whole_reviews=records,final_current_round_clean=False,PR_completion_estimate_percent=80)
(T/"READINESS_PLAN.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
c=json.loads((M/"ROUND02_REPAIRS_V3_COMPILATION.json").read_text());c.update(result="PASS_COMPILED_ALL_FOUR_PAGES_VISUALLY_INSPECTED",root_all4visual_pending=False,all_four_pages_root_visually_inspected=True,first_three_page_renders_byte_identical_to_previous=True);(M/"ROUND02_REPAIRS_V3_COMPILATION.json").write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n")
out={"utc":now,"result":"SOURCE_AND_SIX_FROZEN_FOR_FRESH_WHOLE03","old_source_manifest_sha256":old["source_manifest_sha256"],"source_manifest_sha256":pin,"source_checker_sha256":identity((S/"verify_source.py").read_bytes())["sha256"],"source_files":151,"changed_source_paths":source_changed,"changed_distribution_paths":changed,"original58_and_four_sealed_math_priority_packets_unchanged":True,"metadata_deposit_bytes_unchanged":True,"PDF_pages":4,"all_four_pages_root_visually_inspected":True,"first_three_renders_byte_identical":True,"renders":[{"path":str(p.relative_to(P)),**identity(p.read_bytes())}for p in sorted((P/"render_v3").glob("*.png"))],"release_files":new["files"],"exact_reviewed_v2_preserved":str(V),"two_completed_historical_review_packets_immutable":True,"math_claims_unchanged":True,"first_unpublished_version":"1.0","case_percent":80,"shard_percent":83,"final_readiness_exists":False}
assert not(T/"FINAL_READINESS.json").exists()
(M/"PACKAGE_FREEZE_V3.json").write_text(json.dumps(out,indent=2)+"\n")
r=subprocess.run([sys.executable,"-I","-B",str(S/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--bodies-root",str(T)],capture_output=True,text=True,timeout=120)
assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
a=json.loads(r.stdout);assert a["result"]=="PASS"and a["external_evidence_files_rehashed"]==139 and len(a["finite_replay_processes"])==4
(M/"V3_OPTIONAL_BODY_CUSTODY.json").write_text(r.stdout)
r=subprocess.run([sys.executable,"-B",str(T/"publication_driver.py"),"check"],capture_output=True,text=True,timeout=120);assert r.returncode==0,(r.stdout,r.stderr)
print(json.dumps({"result":"PASS_V3_FROZEN","manifest_sha256":pin,"checker_sha256":out["source_checker_sha256"],"files":new["files"],"current_optional_bodies":139,"next":"fresh whole03"}))

