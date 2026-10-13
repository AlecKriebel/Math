"""Explicit scope, ordinary nonforce main checkpoint and full body readback."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parent.parent
GIT="/opt/homebrew/Cellar/git/2.38.2/bin/git"
BASE=sys.argv[1]
D=A/"actual_disposition_checkpoint_20261006"
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value, reason):
    if not value:raise RuntimeError(reason)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
def run(args):
    start=now()
    child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({"argv":[GIT,*args],"PID":child.pid,"UTC_start":start,"UTC_end":now(),
        "exit_code":child.returncode,"stdout_bytes":len(out),"stdout_sha256":sha(out),
        "stderr_bytes":len(err),"stderr_sha256":sha(err),
        "small_stdout":out.decode("utf-8","replace") if len(out)<12000 else None,
        "stderr":err.decode("utf-8","replace")})
    dump(D/"PROCESS_JOURNAL.json",{"actual_operator_PID":os.getpid(),"events":events})
    require(child.returncode==0,"Git action failed; inspect actual journal/state before retry")
    return out
def pin(path):
    require(path.is_file() and not path.is_symlink(),"Regular public file required")
    body=path.read_bytes()
    return {"path":str(path.relative_to(C)),"bytes":len(body),"sha256":sha(body)}
require(not D.exists(),"Existing actual run: inspect before retry")
D.mkdir()
require(run(["branch","--show-current"]).strip()==b"main","Not main")
require(run(["rev-parse","HEAD"]).decode().strip()==BASE,"Base advanced")
require(run(["ls-remote","origin","refs/heads/main"]).decode().split()[0]==BASE,"Remote advanced")
require(not run(["diff","--cached","--name-only"]),"Index not empty")
ready=json.loads((A/"ROOT_DISPOSITION_READY_20261006.json").read_text())
require(ready["fresh_disposition_review_PASS"] and not ready["publication_authorization"],"Fresh disposition gate")
native=json.loads((A/"native_prior_disposition_20261006/PREPARED_RECEIPT.json").read_text())
require(native["base_commit"]==BASE and native["same_head_closed_without_merge"],"Native base/closure")
private={"private_backend","private_sources","private_primary_sources","tmp","pdfs","__pycache__"}
def public(path):
    return path.is_file() and not path.is_symlink() and not private.intersection(path.parts) and (path.suffix in {".json",".md",".py"} or path.name==".gitignore")
excluded_root={"MATH_AUDIT_CHECKPOINT_ACTUAL_RECEIPT_20261006.json"}
selected={x for x in A.iterdir() if public(x) and x.name not in excluded_root}
for name in ["historical_priority_adversary_20261006","modern_citation_priority_adversary_20261006",
    "quasiperiodic_counterexample_priority_20261006","priority_cross_family_adjudicator_20261006",
    "fresh_disposition_adversary_20261006","native_prior_disposition_20261006","actual_closure_20261006"]:
    selected.update(x for x in (A/name).rglob("*") if public(x))
selected.update([P/"CURRENT_PROGRESS.json",P/"RESEARCH_LOG.md",A/"RESEARCH_LOG.md"])
for entry in native["native_pins"]:
    path=C/entry["path"]
    actual=pin(path)
    require(actual==entry,"Prepared native body changed")
    selected.add(path)
members=[pin(x) for x in sorted(selected)]
selection=A/"DISPOSITION_CHECKPOINT_SELECTION_20261006.json"
dump(selection,{"schema":"pr111-source-scope-checkpoint-selection/v1","UTC":now(),"base_commit":BASE,
    "members":members,"private_third_party_bodies_included":False,"original_budget":"2/5","new_central_proof_turns":0,
    "classification":"already_solved for overbroad imported target only; stronger theorem valid, exact prior/novelty unresolved",
    "same_head_closed_without_merge":True,"publication":False,"workflow_estimate_percent":95,
    "program_completed_at_snapshot":18,"program_estimate_percent_at_snapshot":18/99*100,
    "persistent_goal_status":"active","self_hash_omitted":True})
selected.add(selection)
pins={str(x.relative_to(C)):pin(x) for x in selected}
tracked=set(run(["diff","--name-only","--diff-filter=ACMRTUXB","-z"]).decode().split("\0"))-{''}
require(tracked<=set(pins),"Foreign tracked edits outside selection")
run(["add","--",*sorted(pins)])
staged=set(run(["diff","--cached","--name-only","-z"]).decode().split("\0"))-{''}
require(staged<=set(pins) and len(staged)>40,"Unexpected staged scope/count")
require(not run(["diff","--cached","--diff-filter=D","--name-only"]),"Deletion staged")
for path in staged:
    body=run(["show",":"+path])
    require(len(body)==pins[path]["bytes"] and sha(body)==pins[path]["sha256"],"Staged byte mismatch")
run(["commit","-m","Close PR111 imported-target priority issue and preserve verified R5 counterexample"])
commit=run(["rev-parse","HEAD"]).decode().strip()
require(run(["rev-parse","HEAD^"]).decode().strip()==BASE,"Wrong parent")
changes=set(run(["diff-tree","--no-commit-id","--name-only","-r","-z",commit]).decode().split("\0"))-{''}
require(changes==staged,"Unexpected committed paths")
for path in staged:
    body=run(["show",commit+":"+path])
    require(len(body)==pins[path]["bytes"] and sha(body)==pins[path]["sha256"],"Committed byte mismatch")
run(["push","origin","HEAD:refs/heads/main"])
require(run(["ls-remote","origin","refs/heads/main"]).decode().split()[0]==commit,"Remote post-push mismatch")
run(["fetch","--no-tags","--no-write-fetch-head","origin","refs/heads/main"])
require(run(["rev-parse","origin/main"]).decode().strip()==commit,"Fetched main mismatch")
for path in staged:
    body=run(["show","origin/main:"+path])
    require(len(body)==pins[path]["bytes"] and sha(body)==pins[path]["sha256"],"Remote fetched byte mismatch")
require(not run(["diff","--cached","--name-only"]),"Post-commit index not empty")
receipt={"schema":"pr111-source-scope-checkpoint-actual/v1","UTC":now(),"actual_operator_PID":os.getpid(),
    "base_commit":BASE,"commit":commit,"selected_count":len(pins),"changed_count":len(staged),
    "changed_members":[pins[x] for x in sorted(staged)],"actual_nonforce_push_passed":True,
    "actual_remote_fetch_and_full_selected_changed_body_readback_passed":True,"native_correction_committed":True,
    "completion_metadata_pending":True,"writer_release_pending":True,"PR_workflow_estimate_percent":95,
    "persistent_goal_status":"active"}
dump(D/"RECEIPT.json",receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_members'},sort_keys=True))
