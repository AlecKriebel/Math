"""Authenticate PR173 original files without reading author review verdicts."""
from pathlib import Path
import importlib.util,json,datetime,base64,hashlib
A=Path(__file__).resolve().parent;P=A.parents[1]
s=importlib.util.spec_from_file_location("safe_primitives",P/"audits/pr156_30005432/prepare_scoped_merge.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
head="eb68ee2ecda39a8ec2748796d716c7a7598b7bc6";target="unsolved_math_prioritization/attempts/30003677"
r=m.api("pulls/173");m.require(r["head"]["sha"]==head and r["state"]=="open" and r["draft"],"Original PR changed")
j=m.api("git/commits/"+head);root=j["tree"]["sha"];node=m.lookup(root,target);m.require(node and node[1]=="tree","Exact attempt subtree absent")
out=[]
def visit(tree,prefix):
 t=m.api("git/trees/"+tree);m.require(not t.get("truncated"),"Truncated attempt tree")
 for row in t["tree"]:
  path=prefix+"/"+row["path"]
  if row["type"]=="tree":visit(row["sha"],path)
  else:
   m.require(row["type"]=="blob","Unsupported object")
   blob=m.api("git/blobs/"+row["sha"]);m.require(blob["encoding"]=="base64","Unexpected encoding");b=base64.b64decode(blob["content"])
   m.require(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==row["sha"],"Original Git identity mismatch")
   p=A/"original_submission/files"/path;m.require(not p.exists(),"Already acquired; inspect before replay");p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444)
   out.append(dict(repo_path=path,local_path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),Git_blob=row["sha"],Git_mode=row["mode"],retained_mode="0444"))
visit(node[2],target)
m.save(A/"original_submission/PR_METADATA.json",r);m.save(A/"original_submission/HEAD_COMMIT.json",j)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();m.save(A/"ORIGINAL_FILE_MANIFEST.json",dict(UTC=now,PR=173,original_head=head,original_tree=root,files=out,all_Git_blob_SHA1_authenticated=True,all_exact_SHA256_bound=True,original_inputs_frozen_mode="0444"))
status=json.loads((P/"status_intakes_after_pr170/PR173_STATUS_ONLY.json").read_text());m.require(status["literal_original_QUEUE_status"]=="claimed_solved" and status["effort"]=="2/5","Eligibility differs")
m.save(A/"ORIGINAL_INTAKE.json",status)
m.save(A/"CURRENT_CASE_STATUS.json",dict(UTC=now,PR=173,problem_id=30003677,original_head=head,original_QUEUE_status="claimed_solved",original_effort="2/5",case_percent=5,mathematical_clearance=False,priority_started=False,status="ORIGINAL_FILES_AUTHENTICATED_MATH_INTAKE_NOT_YET_REVIEWED",fully_completed_count=34,published_count=19,MAIN_writer_authority=False,goal_complete=False))
(A/"RESEARCH_LOG.md").write_text("# PR173 research log\n\n"+now+" — Exact original claimed_solved2/5 head and "+str(len(out))+" attempt files authenticated by GitSHA1 and SHA256 and frozen0444. Case5%; mathematics not accepted and priority not started. Programme34/dated99=34.34%,19published. PR171–172 originallynonclaimed status-only skipped untouched. No MAIN/shared Git/index/ref/checkout writer authority or PR/publication mutation. Author review/verifier verdicts not read.\n")
print(json.dumps(dict(PR=173,title=r["title"],head=head,tree=root,files=[dict(path=x["repo_path"],bytes=x["bytes"]) for x in out],case_percent=5),indent=2))
