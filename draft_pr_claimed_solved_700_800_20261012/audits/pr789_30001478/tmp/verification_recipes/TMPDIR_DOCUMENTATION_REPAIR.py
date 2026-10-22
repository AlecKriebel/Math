from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";V=T/"package_versions/v1_review01"
assert not(M/"TMPDIR_DOCUMENTATION_REPAIR.json").exists()
old=json.loads((P/"PACKAGE_INVENTORY.json").read_text());assert old["source_manifest_sha256"]=="6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be"and(P/"source/MANIFEST.json").read_bytes()==(V/"source/MANIFEST.json").read_bytes()
peer=json.loads((M/"WHOLE01_ROOT_REPLAY.json").read_text());assert peer["result"]=="PASS"and peer["required_repairs"]==0 and peer["nonblocking_findings"]==1
identity=lambda raw:{"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
p=S/"README.md";text=p.read_text();needle="Optional --bodies-root /absolute/original-case-tmp"
assert text.count(needle)==1
paragraph="""For the optional, separate frozen test_publication.py wrapper-control harness, use an existing owned absolute ordinary temporary directory outside the closed source. On macOS a default TMPDIR under /var contains a symlink component, which the strict wrapper correctly rejects during positive relocation. Preserve the ancestry checks and all 58 originals. For example, after creating /absolute/owned/replay-tmp, run:
TMPDIR=/absolute/owned/replay-tmp python3 -I -B audit/intake/original/unsolved_math_prioritization/attempts/30001478/test_publication.py --expected-manifest f1aab7f750c4c2aba55ba52addbfdd211de3b47edb6fa898387b2720b713e58d

The unchanged separate suite passes all 24 controls with an ordinary TMPDIR. It is additional to the advertised core verify_source.py --replay, which passed on this Mac without that environment adjustment; the core does not run this separate wrapper-control harness. This is an environment requirement of the frozen ancillary harness, not a mathematical restriction.

"""
p.write_text(text.replace(needle,paragraph+needle))
rows=[]
for f in sorted(S.rglob("*")):
 if f.is_file()and f!=S/"MANIFEST.json":assert not f.is_symlink();rows.append({"path":f.relative_to(S).as_posix(),**identity(f.read_bytes())})
assert len(rows)+1==151
(S/"MANIFEST.json").write_text(json.dumps({"schema":"pr789-closed-source/v1","files":rows},indent=2)+"\n");pin=identity((S/"MANIFEST.json").read_bytes())["sha256"]
cmd=[sys.executable,"-I","-B",str(S/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"typeset/main.pdf"),"--output-dir",str(P)]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);new=json.loads(r.stdout);(P/"PACKAGE_INVENTORY.json").write_text(json.dumps(new,indent=2)+"\n")
changed=[a["path"]for a,b in zip(old["files"],new["files"])if a!=b];assert changed==["source-and-verification.zip","zenodo-upload-kit.zip"]
source_changed=[f.relative_to(S).as_posix()for f in S.rglob("*")if f.is_file()and f.read_bytes()!=(V/"source"/f.relative_to(S)).read_bytes()]
assert sorted(source_changed)==["MANIFEST.json","README.md"]
plan=json.loads((T/"READINESS_PLAN.json").read_text())
record={"round":1,"reviewer":peer["reviewer"],"freshly_initialized":True,"packet":"whole_preprint_round01","manifest_sha256":peer["manifest_sha256"],"checker_name":peer["checker_name"],"checker_sha256":peer["checker_sha256"],"root_replay_receipt":"root-receipts/WHOLE01_ROOT_REPLAY.json","root_replay_sha256":identity((M/"WHOLE01_ROOT_REPLAY.json").read_bytes())["sha256"],"reviewed_source_manifest_sha256":peer["source_manifest_sha256"],"reviewed_publication_files":peer["publication_files"],"actionable_issues":1}
plan.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_manifest_sha256=pin,publication_files=new["files"],actual_whole_preprint_rounds=1,completed_whole_reviews=[record],final_current_round_clean=False,original_scientific_head=plan["reviewed_head"],PR_completion_estimate_percent=78)
(T/"READINESS_PLAN.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
repair={"utc":plan["utc"],"result":"L1_REPRODUCTION_DOCUMENTATION_CLARIFIED","old_source_manifest_sha256":old["source_manifest_sha256"],"new_source_manifest_sha256":pin,"source_checker_sha256":identity((S/"verify_source.py").read_bytes())["sha256"],"changed_source_paths":sorted(source_changed),"changed_distribution_paths":changed,"source_files":151,"old_exact_reviewed_package_preserved":str(V),"old_whole_review_packet_immutable":True,"all_original_58_and_all4_math_priority_packets_unchanged":True,"TeX_PDF_metadata_deposit_bytes_unchanged":True,"publication_version_still":"1.0 first unpublished release","no_PDF_recompilation_or_authoring_marker_repeat":True,"next_required_gate":"different freshly initialized whole-preprint review of current package","case_percent":78,"shard_percent":83}
(M/"TMPDIR_DOCUMENTATION_REPAIR.json").write_text(json.dumps(repair,indent=2)+"\n")
r=subprocess.run([sys.executable,"-I","-B",str(S/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--bodies-root",str(T)],capture_output=True,text=True,timeout=120)
assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(r.stdout);assert a["result"]=="PASS"and a["external_evidence_files_rehashed"]==139 and len(a["finite_replay_processes"])==4
(M/"V2_OPTIONAL_BODY_CUSTODY.json").write_text(r.stdout)
r=subprocess.run([sys.executable,"-B",str(T/"publication_driver.py"),"check"],capture_output=True,text=True,timeout=120);assert r.returncode==0,(r.stdout,r.stderr)
print(json.dumps({"result":"PASS_DOCUMENTATION_REPAIR","source_manifest_sha256":pin,"source_checker_sha256":repair["source_checker_sha256"],"source_files":151,"changed_source_paths":source_changed,"changed_six_paths":changed,"new_six":new["files"],"current_optional_bodies":139,"fresh_review02_required":True}))
