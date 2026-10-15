"""Publish final owned bookkeeping after the actual native PR256 merge."""
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/alec/Documents/Math")
P = ROOT / "draft_pr_descending_audit_20261002"
D = HERE.parent / "initial_review_20261013"
PUB = HERE.parent / "publication"
OUT = PUB / ("completion-publication-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
OUT.mkdir(exist_ok=False)
GH = "/opt/homebrew/Cellar/gh/2.85.0/bin/gh"
sequence = 0

def api(method, endpoint, payload=None):
    global sequence
    sequence += 1
    args = [GH, "api", "--method", method, endpoint]
    if payload is not None:
        request = OUT / f"{sequence:02d}-request.json"
        request.write_text(json.dumps(payload))
        args += ["--input", str(request)]
    r = subprocess.run(args, capture_output=True)
    (OUT / f"{sequence:02d}-stdout.json").write_bytes(r.stdout)
    (OUT / f"{sequence:02d}-stderr.txt").write_bytes(r.stderr)
    if r.returncode:
        raise RuntimeError("Native completion call failed; receipts retained")
    return json.loads(r.stdout)

pr = api("GET", "repos/AlecKriebel/Math/pulls/256")
assert pr["merged"] is True and pr["merge_commit_sha"] == "12e92adf4450e46e130cc48ee21bc10dfa6f397a"
paths = [P / "RESEARCH_LOG.md", P / "CURRENT_GOAL_SELECTION_20261013.json",
         D / "RESEARCH_LOG.md", HERE / "PACKAGE_STATE.json",
         HERE / "publish_completion.py", PUB / "PR_MERGED.json"]
entries = [{"path": p.relative_to(ROOT).as_posix(), "mode": "100644",
            "type": "blob", "content": p.read_text()} for p in paths]
for name in ["FINAL_ACCEPTANCE.json", "DISPOSITION.md", "final_queue_state.json",
             "RESEARCH_LOG.md", "FINAL_PACKAGE_MANIFEST.json"]:
    p = HERE / "pr_update/5100017" / name
    entries.append({"path": "unsolved_math_prioritization/attempts/5100017/" + name,
                    "mode": "100644", "type": "blob", "content": p.read_text()})
for attempt in range(4):
    parent = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
    tree = api("GET", "repos/AlecKriebel/Math/git/commits/" + parent)["tree"]["sha"]
    newtree = api("POST", "repos/AlecKriebel/Math/git/trees",
                  {"base_tree": tree, "tree": entries})["sha"]
    commit = api("POST", "repos/AlecKriebel/Math/git/commits",
                 {"message": "Record verified k307 publication tracker and native merge; select next claimed result",
                  "tree": newtree, "parents": [parent]})["sha"]
    try:
        assert api("PATCH", "repos/AlecKriebel/Math/git/refs/heads/main",
                   {"sha": commit, "force": False})["object"]["sha"] == commit
        break
    except RuntimeError:
        rejection = json.loads((OUT / f"{sequence:02d}-stdout.json").read_text())
        latest = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
        if rejection.get("status") != "422" or latest == parent or attempt == 3:
            raise
        # Rebuild the owned-path-only tree on the fresh Main; never force a ref.
else:
    raise RuntimeError("No completion checkpoint was published")
current = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
if current != commit:
    assert api("GET", "repos/AlecKriebel/Math/compare/" + commit + "..." + current)["status"] == "ahead"
receipt = {"utc": datetime.now(timezone.utc).isoformat(), "commit": commit,
           "parent": parent, "readback_main": current, "owned_files": len(entries),
           "case_completion_percent": 100, "program_counts": [38, 15, 15, 0],
           "goal_active_incomplete": True, "next_current_head_claimed_PR": 255,
           "shared_checkout_and_index_mutations": 0}
receipt["transport_receipts"] = str(OUT)
(PUB / "COMPLETION_PUBLICATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
