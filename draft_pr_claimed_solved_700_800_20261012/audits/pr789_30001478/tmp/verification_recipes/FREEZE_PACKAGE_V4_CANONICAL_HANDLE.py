from pathlib import Path
import copy,datetime,hashlib,json,shutil,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";V=T/"package_versions/v3_review03"
assert not V.exists()and not(M/"PACKAGE_FREEZE_V4.json").exists()
ident=lambda raw:{"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
old=json.loads((P/"PACKAGE_INVENTORY.json").read_text());assert old["source_manifest_sha256"]=="50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de"
oldgate=(T/"FINAL_READINESS.json").read_bytes();g=json.loads(oldgate);assert g["actual_whole_preprint_rounds"]==3 and g["result"]=="PASS"
assert hashlib.sha256(oldgate).hexdigest()=="27beef2982540a003d0f95a30153c51d8ef182b5a721418afa904ad3ee24c0ea"and oldgate==(T/"publication/READINESS_AT_PUBLICATION.json").read_bytes()
assert not(T/"publication/PUBLICATION_INTENT.json").exists()and not(T/"publication/PUBLISH_RECEIPT.json").exists()
receipt=json.loads((T/"publication/KNOWN_DRAFT_METADATA_RECONCILIATION.json").read_text());assert receipt["record_id"]==23423736 and receipt["submitted"]is False and len(receipt["metadata_differences"])==1
V.mkdir();shutil.copytree(S,V/"source")
for row in old["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
 src=P/row["path"];dst=V/row["path"];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 if "sha256"in row:assert ident(dst.read_bytes())=={k:row[k]for k in["bytes","sha256"]}
(V/"FINAL_READINESS_AT_CREATION_STAGE.json").write_bytes(oldgate)
(V/"READINESS_AT_PUBLICATION_ORIGINAL.json").write_bytes((T/"publication/READINESS_AT_PUBLICATION.json").read_bytes())
# First retire the current authorization before changing any release bytes.
pending=copy.deepcopy(g);pending.update(result="PENDING_FRESH_WHOLE04_CANONICAL_METADATA",final_current_round_clean=False,paper_ready=False,publication_status="SOLE_KNOWN_DRAFT_23423736_UNPUBLISHED_METADATA_REPAIR",PR_completion_estimate_percent=82,readiness_superseded_reason="Zenodo automatically canonicalizes the same Campbell thesis Handle; canonical authored metadata revision requires a new exact-package final review.")
(T/"FINAL_READINESS.json").write_text(json.dumps(pending,indent=2,ensure_ascii=False)+"\n")
p=S/"zenodo-metadata.json";raw=p.read_text();needle='"identifier": "https://hdl.handle.net/1842/22886",\n        "relation": "references",\n        "scheme": "url"'
replacement='"identifier": "1842/22886",\n        "relation": "references",\n        "scheme": "handle"'
assert raw.count(needle)==1
original=json.loads(raw);new=copy.deepcopy(original);new["metadata"]["related_identifiers"][3]={"identifier":"1842/22886","relation":"references","scheme":"handle"}
p.write_text(raw.replace(needle,replacement));assert json.loads(p.read_text())==new
diff=receipt["metadata_differences"][0];assert diff["field"]=="related_identifiers"and diff["wanted"]==original["metadata"]["related_identifiers"]and diff["actual"]==new["metadata"]["related_identifiers"]
rows=[]
for f in sorted(S.rglob("*")):
 if f.is_file()and f!=S/"MANIFEST.json":assert not f.is_symlink()and f.stat().st_nlink==1;rows.append({"path":f.relative_to(S).as_posix(),**ident(f.read_bytes())})
assert len(rows)+1==151
(S/"MANIFEST.json").write_text(json.dumps({"schema":"pr789-closed-source/v1","files":rows},indent=2)+"\n");pin=ident((S/"MANIFEST.json").read_bytes())["sha256"]
r=subprocess.run([sys.executable,"-I","-B",str(S/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(T/"repair_typeset_v3/main.pdf"),"--output-dir",str(P)],capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr)
release=json.loads(r.stdout);(P/"PACKAGE_INVENTORY.json").write_text(json.dumps(release,indent=2)+"\n")
changed=[a["path"]for a,b in zip(old["files"],release["files"])if a!=b];assert changed==["source-and-verification.zip","zenodo-deposit.json","zenodo-metadata.json","zenodo-upload-kit.zip"]
schanged=sorted(f.relative_to(S).as_posix()for f in S.rglob("*")if f.is_file()and f.read_bytes()!=(V/"source"/f.relative_to(S)).read_bytes());assert schanged==["MANIFEST.json","zenodo-metadata.json"]
assert sorted(str(f.relative_to(S))for f in S.rglob("*")if f.is_file())==sorted(str(f.relative_to(V/"source"))for f in(V/"source").rglob("*")if f.is_file())
peer=json.loads((M/"WHOLE03_ROOT_REPLAY.json").read_text());records=g["completed_whole_reviews"];assert len(records)==3 and records[-1]["actionable_issues"]==0
pending.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_manifest_sha256=pin,publication_files=release["files"],actual_whole_preprint_rounds=3,completed_whole_reviews=records,known_unpublished_draft_id=23423736,known_deposition_creations=1,published=False)
for n in["READINESS_PLAN.json","FINAL_READINESS.json"]:(T/n).write_text(json.dumps(pending,indent=2,ensure_ascii=False)+"\n")
out={"utc":pending["utc"],"result":"CANONICAL_HANDLE_V4_FROZEN_PENDING_FRESH_WHOLE04","source_manifest_sha256":pin,"source_checker_sha256":ident((S/"verify_source.py").read_bytes())["sha256"],"source_files":151,"changed_source_paths":schanged,"other149sourcefiles_byte_identical_to_exact_preserved_V3":True,"changed_distribution_paths":changed,"TeX_PDF_PDFbindings_checker_builder_and58originals_fourfamilies_unchanged":True,"release_files":release["files"],"exact_V3_preserved":str(V),"original_V3_gate_snapshot_sha256":"27beef2982540a003d0f95a30153c51d8ef182b5a721418afa904ad3ee24c0ea","original_U_READINESS_AT_PUBLICATION_bytes_immutable":True,"final_publish_snapshot_will_be":"publication/READINESS_AT_PUBLICATION_V4.json","known_only_unpublished_draft":23423736,"new_deposit_or_publish_or_remote_metadata_mutation":False,"canonical_metadata_change":{"from":{"identifier":"https://hdl.handle.net/1842/22886","relation":"references","scheme":"url"},"to":{"identifier":"1842/22886","relation":"references","scheme":"handle"},"meaning":"Same exact Campbell thesis handle, preserving order/relation/allotherfields; canonical authored metadata avoids any case-specific normalization adapter."},"official_primary_API_documentation":"https://developers.zenodo.org/#representation","API_documentation_support":"Related identifiers support Handle; identifier types are automatically detected and normalized to standard form.","first_unpublished_release_version":"1.0","new_PDF_authoring_or_recompilation":False,"case_percent":82,"shard_percent":83}
(M/"PACKAGE_FREEZE_V4.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
r=subprocess.run([sys.executable,"-I","-B",str(S/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--bodies-root",str(T)],capture_output=True,text=True,timeout=120);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(r.stdout);assert a["result"]=="PASS"and a["external_evidence_files_rehashed"]==139 and len(a["finite_replay_processes"])==4
(M/"V4_OPTIONAL_BODY_CUSTODY.json").write_text(r.stdout)
r=subprocess.run([sys.executable,"-B",str(T/"publication_driver.py"),"check"],capture_output=True,text=True,timeout=120);assert r.returncode==0,(r.stdout,r.stderr)
print(json.dumps({"result":"PASS_V4_FROZEN_NOT_AUTHORIZED_TO_PUBLISH","source_manifest_sha256":pin,"source_checker_sha256":out["source_checker_sha256"],"changed_source_paths":schanged,"same149otherfiles":True,"files":release["files"],"known_only_unpublished_record":23423736,"new_fresh_whole04_required":True}))

