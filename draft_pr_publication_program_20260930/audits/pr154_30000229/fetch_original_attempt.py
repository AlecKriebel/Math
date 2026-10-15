#!/usr/bin/env python3
"""Preserve only the eligible PR154's complete original attempt, using actual Git object checks."""
import base64,concurrent.futures,datetime,hashlib,json,subprocess
from pathlib import Path
A=Path(__file__).resolve().parent
HEAD="58bee8514677549ee5a7cd699028a5f3a616c5bc"
TARGET="unsolved_math_prioritization/attempts/30000229"
GH="/opt/homebrew/Cellar/gh/2.85.0/bin/gh"
def require(c,m):
 if not c:raise RuntimeError(m)
def api(e):
 r=subprocess.run([GH,"api","repos/AlecKriebel/Math/"+e],capture_output=True,text=True,timeout=90)
 require(r.returncode==0,r.stderr[:1000]);return json.loads(r.stdout)
def save(n,x):
 p=A/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+"\n")
intake=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/ordered_intake_20261012/after_PR152_publication")
eligible=json.loads((intake/"PR154_STATUS_ONLY.json").read_text())
require(eligible["literal_status"]=="claimed_solved" and eligible["original_head"]==HEAD,"Literal eligibility gate failed")
pr=api("pulls/154");require(pr["state"]=="open" and pr["draft"] and pr["head"]["sha"]==HEAD,"Original PR changed")
commit=api("git/commits/"+HEAD);root=commit["tree"]["sha"]
for part in TARGET.split("/"):
 tree=api("git/trees/"+root);require(not tree.get("truncated"),"Nonrecursive tree truncated")
 matches=[x for x in tree["tree"] if x["path"]==part and x["type"]=="tree"];require(len(matches)==1,"Target directory absent")
 root=matches[0]["sha"]
tree=api("git/trees/"+root+"?recursive=1");require(not tree.get("truncated"),"Attempt tree truncated")
blobs=[x for x in tree["tree"] if x["type"]=="blob"]
require(blobs and all(x["mode"] in ["100644","100755"] and not x["path"].startswith("/") and ".." not in Path(x["path"]).parts for x in blobs),"Unsafe original file path/type")
def fetch(x):
 j=api("git/blobs/"+x["sha"]);require(j["encoding"]=="base64","Blob encoding differs")
 b=base64.b64decode(j["content"]);oid=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
 require(oid==j["sha"]==x["sha"],"Original blob identity differs")
 p=A/"original_submission/files"/TARGET/x["path"];p.parent.mkdir(parents=True,exist_ok=True)
 require(not p.exists(),"Original file already exists");p.write_bytes(b)
 return {"repository_path":TARGET+"/"+x["path"],"relative_attempt_path":x["path"],"Git_blob":oid,"mode":x["mode"],"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"local_path":str(p)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:files=list(pool.map(fetch,blobs))
require(api("pulls/154")["head"]["sha"]==HEAD,"Original head moved during read-only download")
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
save("INTAKE.json",{**eligible,"UTC":now,"status":"ELIGIBLE_ORIGINAL_ATTEMPT_ALL_BLOBS_PRESERVED","target_directory":TARGET,"attempt_tree":root,"original_file_count":len(files),"PR_url":pr["html_url"],"original_PR_body":pr["body"],"original_PR_title":pr["title"],"original_commit":commit,"mathematical_audit_percent":0,"case_workflow_percent":10,"prior_PR152_merge_pending":True,"prior_PR152_publication_and_tracker_actual":True,"provider_mutations":False})
save("ORIGINAL_FILE_MANIFEST.json",{"UTC":now,"original_head":HEAD,"attempt_tree":root,"files":sorted(files,key=lambda x:x["repository_path"]),"all_original_blobs_read_and_Git_identity_verified":True})
(A/"RESEARCH_LOG.md").write_text(now+" — PR154 literal claimed_solved2/5 originalhead"+HEAD+" eligible after153 unsolved status-only skip. Entire original attempt downloaded and Git-blob authenticated. Case10%; mathematical/priority audit0%. PR152 exact publication/tracker already accepted, separate MAIN merge pending; no provider/index/ref mutations. Target hypothesis still unverified.\n")
print(json.dumps({"status":"PASS","original_files":len(files),"original_head":HEAD,"attempt_tree":root,"case_percent":10}))
for x in files:print(x["relative_attempt_path"],x["bytes"])

