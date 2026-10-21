from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts"
assert not(P/"PACKAGE_INVENTORY.json").exists(),"Already built: reconcile"
identity=lambda raw:{"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
(P/"output/pdf").mkdir(parents=True,exist_ok=True);shutil.copyfile(P/"typeset/main.pdf",P/"output/pdf/paper.pdf")
bindings={n:identity(p.read_bytes())for n,p in[("main.tex",S/"main.tex"),("paper.pdf",P/"output/pdf/paper.pdf")]}
(S/"PREPRINT_BINDINGS.json").write_text(json.dumps(bindings,indent=2)+"\n")
rows=[]
for p in sorted(S.rglob("*")):
 if p.is_file()and p!=S/"MANIFEST.json":assert not p.is_symlink();rows.append({"path":p.relative_to(S).as_posix(),**identity(p.read_bytes())})
(S/"MANIFEST.json").write_text(json.dumps({"schema":"pr789-closed-source/v1","files":rows},indent=2)+"\n")
pin=identity((S/"MANIFEST.json").read_bytes())["sha256"]
cmd=[sys.executable,"-I","-B",str(S/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"typeset/main.pdf"),"--output-dir",str(P)]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);assert r.returncode==0,(r.stdout,r.stderr);release=json.loads(r.stdout)
(P/"PACKAGE_INVENTORY.json").write_text(json.dumps(release,indent=2)+"\n")
r=subprocess.run([sys.executable,"-I","-B",str(S/"verify_source.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--replay","--bodies-root",str(T)],capture_output=True,text=True,timeout=300)
(M/"FIRST_PORTABLE_VERIFICATION.stdout").write_text(r.stdout)
assert r.returncode==0,(r.stdout,r.stderr);receipt=json.loads(r.stdout);assert receipt["result"]=="PASS"and receipt["external_evidence_files_rehashed"]==139 and len(receipt["finite_replay_processes"])==10
freeze={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"SOURCE_AND_SIX_FROZEN_FOR_FRESH_WHOLE_REVIEW","source_manifest_sha256":pin,"source_checker_sha256":identity((S/"verify_source.py").read_bytes())["sha256"],"source_files":len(rows)+1,"original_files":58,"release_files":release["files"],"PDF_pages":4,"Tectonic_exit":0,"editor_compilation":"success","all_four_rendered_pages_root_visually_inspected":True,"renders":[{"path":p.relative_to(P).as_posix(),**identity(p.read_bytes())}for p in sorted((P/"render_root").glob("*.png"))],"optional_primary_evidence_files_rehashed":139,"source_replay_processes":10,"external_human_peer_review":False,"formal_proof_verification":False,"whole_preprint_review_completed":False,"paper_ready":False,"case_percent":65,"shard_percent":83}
(M/"PACKAGE_FREEZE_V1.json").write_text(json.dumps(freeze,indent=2)+"\n")
print(json.dumps({"result":"PASS","source_files":len(rows)+1,"source_manifest_sha256":pin,"source_checker_sha256":freeze["source_checker_sha256"],"PDF_pages":4,"source_replay_processes":10,"optional_body_files":139,"six":[{"path":x["path"],"bytes":x["bytes"],"sha256":x["sha256"]}for x in release["files"]]}))
