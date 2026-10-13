"""Publish narrowly owned candidate files to native main; never a release."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
D = HERE.parent / "initial_review_20261013"
ROOT = Path("/Users/alec/Documents/Math")
OUT = HERE / "tmp/checkpoint-publication"
OUT.mkdir(parents=True, exist_ok=True)
GH = "/opt/homebrew/Cellar/gh/2.85.0/bin/gh"
count = 0

def api(method, endpoint, payload=None):
    global count
    count += 1
    args = [GH, "api", "--method", method, endpoint]
    if payload is not None:
        request = OUT / f"{count:02d}-request.json"
        request.write_text(json.dumps(payload))
        args += ["--input", str(request)]
    r = subprocess.run(args, capture_output=True)
    (OUT / f"{count:02d}-stdout.json").write_bytes(r.stdout)
    (OUT / f"{count:02d}-stderr.txt").write_bytes(r.stderr)
    if r.returncode:
        raise RuntimeError(f"Native request {count} failed; receipts retained")
    return json.loads(r.stdout)

paths = [D / n for n in ["ROOT_PRIORITY_ACCEPTANCE.md", "RESEARCH_LOG.md",
                         "candidate_repair_01/REPAIR_RECORD.json"]]
paths += [D / "priority_billiards_adversary_01" / n for n in
          ["PRIORITY_AUDIT_REPORT.md", "CIRCLE_FOCUS_INTERMEDIATE_SCOPE.md",
           "EXACT_COMPARISON_CONTROLS.json", "PRIMARY_SOURCE_MANIFEST.json"]]
paths += [D / "priority_recent_adversary_01" / n for n in
          ["PRIORITY_REPORT.md", "AUDIT_DISPOSITION.json",
           "ZENODO_ORIGINAL_CONTENT_COMPARISON.json"]]
paths += [p for p in HERE.iterdir() if p.is_file() and p.suffix in
          {".md", ".py", ".json", ".tex", ".pdf", ".zip", ".txt"}]
paths += [HERE / "LICENSE"]
paths += [p for p in (HERE / "verification").rglob("*")
          if p.is_file() and "__pycache__" not in p.parts]
pr = api("GET", "repos/AlecKriebel/Math/pulls/256")
assert pr["state"] == "open" and pr["draft"]
assert pr["head"]["sha"] == "9445a90b57f76493bd901edc544b09dec393e20f"
parent = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
tree = api("GET", "repos/AlecKriebel/Math/git/commits/" + parent)["tree"]["sha"]
entries = []
inventory = []
for p in sorted(set(paths)):
    assert p.resolve().is_relative_to(HERE.parent) and not p.is_symlink()
    data = p.read_bytes()
    path = p.relative_to(ROOT).as_posix()
    entry = {"path": path, "mode": "100644", "type": "blob"}
    if p.suffix in {".pdf", ".zip"}:
        entry["sha"] = api("POST", "repos/AlecKriebel/Math/git/blobs",
                           {"content": base64.b64encode(data).decode(),
                            "encoding": "base64"})["sha"]
    else:
        entry["content"] = data.decode()
    entries.append(entry)
    inventory.append({"path": path, "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()})
newtree = api("POST", "repos/AlecKriebel/Math/git/trees",
              {"base_tree": tree, "tree": entries})["sha"]
commit = api("POST", "repos/AlecKriebel/Math/git/commits",
             {"message": "Checkpoint k307 priority audits and candidate preprint package",
              "tree": newtree, "parents": [parent]})["sha"]
published = api("PATCH", "repos/AlecKriebel/Math/git/refs/heads/main",
                {"sha": commit, "force": False})
assert published["object"]["sha"] == commit
current = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
if current != commit:
    assert api("GET", "repos/AlecKriebel/Math/compare/" + commit + "..." + current)["status"] == "ahead"
receipt = {"utc": datetime.now(timezone.utc).isoformat(), "commit": commit,
           "parent": parent, "readback_main": current, "owned_files": inventory,
           "candidate_only": True, "overall_completion_percent": 65,
           "Zenodo_publication": False, "PR_merge": False,
           "shared_checkout_and_index_mutations": 0}
(HERE / "CANDIDATE_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({k: v for k, v in receipt.items() if k != "owned_files"}, indent=2))
