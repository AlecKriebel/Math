"""Idempotency-aware same-head closure after the fresh disposition review."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A = Path(__file__).resolve().parent
C = A.parents[2]
D = A / "actual_closure_20261006"
GH = "/opt/homebrew/Cellar/gh/2.85.0/bin/gh"
HEAD = "8a7270989d7064a4b97badecaa4b311db5e6d49f"
MARKER = "<!-- pr111-source-scope-disposition-20261006 -->"
events = []
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value, reason):
    if not value: raise RuntimeError(reason)
def digest(body): return hashlib.sha256(body).hexdigest()
def dump(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
def run(args):
    start = now()
    child = subprocess.Popen([GH, *args], cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    i = len(events)
    (D / (str(i) + ".stdout.bin")).write_bytes(out)
    (D / (str(i) + ".stderr.bin")).write_bytes(err)
    events.append({"argv":[GH,*args],"PID":child.pid,"start_UTC":start,"end_UTC":now(),
        "returncode":child.returncode,"stdout_file":str(i)+".stdout.bin","stderr_file":str(i)+".stderr.bin",
        "stdout_sha256":digest(out),"stderr_sha256":digest(err)})
    dump(D / "PROCESS_JOURNAL.json", {"actual_operator_PID":os.getpid(),"events":events})
    require(child.returncode == 0, err.decode("utf-8","replace")[:1000])
    return out
def live():
    return json.loads(run(["pr","view","111","--repo","AlecKriebel/Math","--json",
        "number,state,isDraft,headRefOid,baseRefName,url,closedAt,mergedAt"]))

require(not D.exists(), "Existing actual run: inspect journal/state before retry")
ready = json.loads((A / "ROOT_DISPOSITION_READY_20261006.json").read_text())
require(ready["fresh_disposition_review_PASS"] and ready["mathematical_clearance"]
        and ready["narrow_classical_target_disposition_supported"] and not ready["publication_authorization"], "Disposition gate")
note = A / ready["closing_comment_file"]
body = note.read_text()
require(digest(note.read_bytes()) == ready["closing_comment_sha256"], "Closing body changed")
D.mkdir()
(D / ".gitignore").write_text("*.bin\n")
before = live()
require(before["state"] == "OPEN" and before["isDraft"] and before["headRefOid"] == HEAD
        and before["baseRefName"] == "main", "PR changed; re-evaluate before action")
pages = json.loads(run(["api","repos/AlecKriebel/Math/issues/111/comments","--paginate","--slurp"]))
matches = [x for page in pages for x in page if MARKER in x["body"]]
require(len(matches) <= 1, "Duplicate disposition comments")
if matches:
    comment = matches[0]
    require(comment["body"] == body, "Existing disposition differs")
else:
    result = run(["pr","comment","111","--repo","AlecKriebel/Math","--body-file",str(note)]).decode().strip()
    cid = result.rsplit("issuecomment-",1)[-1]
    require(cid.isdigit(), "Comment creation result ambiguous: inspect before retry")
    comment = json.loads(run(["api","repos/AlecKriebel/Math/issues/comments/"+cid]))
    require(comment["body"] == body, "Actual comment body readback differs")
again = live()
require(again["state"] == "OPEN" and again["headRefOid"] == HEAD, "PR changed after comment")
run(["pr","close","111","--repo","AlecKriebel/Math"])
after = live()
require(after["state"] == "CLOSED" and after["headRefOid"] == HEAD and after["mergedAt"] is None
        and after["closedAt"], "Same-head unmerged closure not verified")
record = {"schema":"pr111-actual-source-scope-closure/v1","UTC":now(),"actual_operator_PID":os.getpid(),
    "PR":111,"original_head":HEAD,"before":before,"after":after,"same_head_closed_without_merge":True,
    "closing_comment_url":comment["html_url"],"closing_comment_id":comment["id"],
    "closing_comment_sha256":digest(note.read_bytes()),"actual_comment_full_body_readback_exact":True,
    "disposition":"already_solved_only_for_overbroad_imported_manifold_target_classical_obstruction",
    "stronger_R5_mathematics_verified":True,"stronger_R5_identical_prior_authenticated":False,
    "stronger_R5_substantive_novelty_established":False,"native_correction_pending":True,
    "original_budget":"2/5","new_central_proof_search_turns":0,"DOI":None,"Zenodo_actions":False,
    "tracker_actions":False,"branch_deleted":False,"primary_checkout_mutated":False,
    "workflow_estimate_percent":85,"persistent_goal_status":"active"}
dump(D / "RECEIPT.json",record)
print(json.dumps(record,sort_keys=True))
