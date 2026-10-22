#!/usr/bin/env python3
"""Add the accepted package to the pinned PR branch, without a checkout/index."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
PREFIX="unsolved_math_prioritization/attempts/30004665/publication_20261017"
BRANCH="string-cone-30004665-canonical-counterexample-20261011"
ORIGINAL="5a2e1b726ee8b0a207cf18dc2403ac57baf74d35"

def git(*args,data=None):
 r=subprocess.run(["git","-c","gc.auto=0",*args],cwd=REPO,input=data,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 return r.stdout

def pr():
 return json.loads(subprocess.check_output(["gh","pr","view","1205","--repo","AlecKriebel/Math","--json","headRefOid,headRefName,state,isDraft"],cwd=REPO,text=True))

def tree(entries):
 return git("mktree","-z",data=b"\0".join(entries)+b"\0").decode().strip()

def insert(base,parts,oid):
 entries=[s for s in git("ls-tree","-z",base).split(b"\0") if s] if base else []
 target=parts[0].encode(); found=next((s for s in entries if s.split(b"\t",1)[1]==target),None)
 if len(parts)>1:
  child=found.split()[2].decode() if found else None
  oid=insert(child,parts[1:],oid)
 entries=[s for s in entries if s.split(b"\t",1)[1]!=target]
 entries.append(f"040000 tree {oid}\t{parts[0]}".encode())
 return tree(entries)

def main():
 if git("branch","--show-current").strip()!=b"main":raise RuntimeError("Stay on main")
 build=json.loads((ROOT/"BUILD_RECEIPT.json").read_text())
 gate=json.loads((ROOT/"FINAL_REVIEW_GATE.json").read_text())
 pub=json.loads((ROOT/"PUBLICATION_RECEIPT.json").read_text())
 tracker=json.loads((ROOT/"tracker/TRACKER_RECEIPT.json").read_text())
 if gate["status"]!="pass" or pub["state"]!="published" or not tracker["readback_verified"]:raise RuntimeError("All review/publication/tracker gates required")
 for key in ("pdf","verification_zip"):
  entry=build[key]
  if hashlib.sha256((ROOT/entry["path"]).read_bytes()).hexdigest()!=entry["sha256"] or gate[key+"_sha256"]!=entry["sha256"]:raise RuntimeError("Reviewed file drift")
  actual=next(f for f in pub["files"] if f["name"]==entry["path"])
  if actual["sha256"]!=entry["sha256"] or actual["size"]!=entry["bytes"]:raise RuntimeError("Published file drift")
 current=pr(); receipt_path=ROOT/"PR_BRANCH_RECEIPT.json"
 if receipt_path.exists():
  old=json.loads(receipt_path.read_text())
  if current["headRefOid"]==old["commit"]:print(json.dumps(old,indent=2));return
  raise RuntimeError("Recorded PR branch update differs from current head")
 if current["headRefOid"]!=ORIGINAL or current["headRefName"]!=BRANCH or current["state"]!="OPEN":raise RuntimeError("Pinned original PR moved")
 submitted=json.loads((ROOT.parent/"SUBMITTED_SNAPSHOT.json").read_text())
 for f in submitted["files"]:
  if git("rev-parse",ORIGINAL+":"+f["path"]).decode().strip()!=f["blob"]:raise RuntimeError("Original file binding mismatch")
 local=ROOT/"pr_publication_files"; local.mkdir(exist_ok=True)
 for key in ("pdf","verification_zip"):shutil.copyfile(ROOT/build[key]["path"],local/build[key]["path"])
 shutil.copyfile(ROOT/"zenodo-deposit.json",local/"zenodo-deposit.json")
 shutil.copyfile(ROOT/"PUBLICATION_RECEIPT.json",local/"PUBLICATION_RECEIPT.json")
 draft=(ROOT/"PR_ACCEPTANCE_DRAFT.md").read_text()
 tail="The original eight authored files remain the historical proof/audit edition."
 draft=draft[:draft.index(tail)]
 note=(draft+"The original eight authored files remain the historical proof/audit edition. "
       "The present package is the current reproducible publication edition.\n\n"
       "Published preprint: ["+pub["doi"]+"]("+pub["doi_url"]+"). "
       "Zenodo record: "+pub["record_url"]+". Version 1.0, 17 October 2026; exact metadata and both file checksums verified by the repository deposit kit.\n\n"
       "Fresh whole-package review round 1 identified a provenance issue, now corrected globally. A different fresh round 2 reviewer found no remaining mathematical, priority-framing, provenance, metadata or layout blocker on these exact files. "
       "Public review evidence: https://github.com/AlecKriebel/Math/tree/main/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1205_30004665/reviews .\n\n"
       "DOI and scoped notes appended through Google Workspace CLI to the requested tracker, with exact readback at "+tracker["updatedRange"]+".\n")
 (local/"README.md").write_text(note)
 entries=[]
 for p in sorted(local.iterdir()):
  if not p.is_file():raise RuntimeError("Unexpected publication child")
  oid=git("hash-object","-w","--",str(p)).decode().strip()
  entries.append(f"100644 blob {oid}\t{p.name}".encode())
 child=tree(entries); root=insert(ORIGINAL,PREFIX.split("/"),child)
 commit=git("commit-tree",root,"-p",ORIGINAL,data=b"Publish audited canonical-W D4 corrective note and verification package\n").decode().strip()
 changed=git("diff-tree","--no-commit-id","--name-only","-r",commit).decode().splitlines()
 if len(changed)!=5 or any(not s.startswith(PREFIX+"/") for s in changed):raise RuntimeError("Unexpected PR changes")
 for f in submitted["files"]:
  if git("rev-parse",commit+":"+f["path"]).decode().strip()!=f["blob"]:raise RuntimeError("Historical original file changed")
 if pr()["headRefOid"]!=ORIGINAL:raise RuntimeError("PR changed before push")
 git("push","origin",commit+":refs/heads/"+BRANCH)
 if git("ls-remote","origin","refs/heads/"+BRANCH).split()[0].decode()!=commit:raise RuntimeError("Remote branch readback differs")
 receipt={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pr":1205,"base":ORIGINAL,"commit":commit,"branch":BRANCH,"paths":changed,"original_eight_blobs_preserved":True,"shared_index_modified":False,"doi":pub["doi"]}
 receipt_path.write_text(json.dumps(receipt,indent=2)+"\n")
 body=("## Accepted result and publication\n\n"+note+"\nThe original eight-file MANIFEST.json binds its historical proof/audit edition. The publication_20261017 child folder supplements that edition with the reviewed PDF, portable verification archive, matching Zenodo metadata and publication receipt. QUEUE.md is unchanged; eligibility was determined from this PR's explicit full-solution outcome.\n")
 (ROOT/"PR_BODY_FINAL.md").write_text(body)
 print(json.dumps(receipt,indent=2))

if __name__=="__main__":main()
