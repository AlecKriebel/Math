"""Integrate only PR256 after verified publication and tracker append.

Uses native Git objects against current main; does not touch the shared index
or checkout. It makes no GitHub release.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/alec/Documents/Math")
D = HERE.parent / "initial_review_20261013"
PUB = HERE.parent / "publication"
OUT = PUB / "native-pr-integration"
OUT.mkdir(parents=True, exist_ok=True)
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
    result = subprocess.run(args, capture_output=True)
    (OUT / f"{sequence:02d}-stdout.json").write_bytes(result.stdout)
    (OUT / f"{sequence:02d}-stderr.txt").write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError(f"Native call {sequence} failed; do not blindly replay mutations")
    return json.loads(result.stdout)

clearance = json.loads((HERE / "FINAL_CLEARANCE.json").read_text())
assert clearance["mathematical_verdict"] == "PASS"
assert clearance["fresh_clean_reviews"] >= 2
receipt = json.loads((PUB / "ZENODO_VERIFIED_PUBLICATION.json").read_text())
assert receipt["submitted"] is True and receipt["metadata_and_files_verified"] is True
tracker = json.loads((PUB / "TRACKER_VERIFIED_APPEND.json").read_text())
assert tracker["verified"] is True and tracker["doi_url"] == receipt["doi_url"]
doi = receipt["doi_url"]
original = D / "submitted/unsolved_math_prioritization/attempts/5100017"
staged = HERE / "pr_update/5100017"
assert staged.is_dir()
pr = api("GET", "repos/AlecKriebel/Math/pulls/256")
assert pr["state"] == "open" and pr["draft"]
oldhead = pr["head"]["sha"]
assert oldhead == "9445a90b57f76493bd901edc544b09dec393e20f"
base = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
basetree = api("GET", "repos/AlecKriebel/Math/git/commits/" + base)["tree"]["sha"]
queue = api("GET", "repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref=" + base)
text = base64.b64decode(queue["content"]).decode()
rows = [line for line in text.splitlines() if re.search(r"\|\s*5100017\s*/", line)]
assert len(rows) == 1
oldrow = rows[0]
cells = [cell.strip() for cell in oldrow.split("|")][1:-1]
assert cells[7] in {"queued", "claimed_solved"}
cells[7] = "claimed_solved"
cells[8] = "1/5"
cells[10] = (
    "2026-10-13: k307 signed outer-pedal area centroid proved on its exact "
    "nonzero-area domain for least even elliptic-caustic families, including stars. "
    "Explicit centroid and fixed zero-area circle; all-M validity for simple orbits; "
    "N4 converse repaired. Independent algebraic/geometric reproduction and two fresh "
    "preprint reviews passed. Original observation and classical methods credited; "
    "bounded priority search, no firstness claim. Unrefereed AI-assisted preprint: " + doi
)
newrow = "| " + " | ".join(cells) + " |"
newqueue = text.replace(oldrow, newrow)
assert newqueue.count(newrow) == 1
# Replacement must touch exactly this target row.
assert newqueue.replace(newrow, oldrow) == text
entries = [{"path": "unsolved_math_prioritization/QUEUE.md", "mode": "100644",
            "type": "blob", "content": newqueue}]
for path in sorted(staged.rglob("*")):
    if path.is_file():
        entries.append({"path": "unsolved_math_prioritization/attempts/5100017/" +
                        path.relative_to(staged).as_posix(),
                        "mode": "100644", "type": "blob", "content": path.read_text()})
# Include the finalized owned package and fresh review/clearance records.
paths = [p for p in HERE.iterdir() if p.is_file() and p.suffix in
         {".tex", ".pdf", ".zip", ".md", ".json", ".py", ".txt"}]
paths += [HERE / "LICENSE", D / "RESEARCH_LOG.md"]
paths += [p for p in (HERE / "verification").rglob("*")
          if p.is_file() and "__pycache__" not in p.parts]
paths += [p for p in HERE.glob("review_*/*") if p.is_file() and
          p.suffix in {".md", ".py", ".json"}]
paths += [PUB / "ZENODO_VERIFIED_PUBLICATION.json", PUB / "TRACKER_VERIFIED_APPEND.json"]
for path in sorted(set(paths)):
    data = path.read_bytes()
    entry = {"path": path.relative_to(ROOT).as_posix(), "mode": "100644", "type": "blob"}
    if path.suffix in {".pdf", ".zip"}:
        entry["sha"] = api("POST", "repos/AlecKriebel/Math/git/blobs",
                           {"content": base64.b64encode(data).decode(), "encoding": "base64"})["sha"]
    else:
        entry["content"] = data.decode()
    entries.append(entry)
newtree = api("POST", "repos/AlecKriebel/Math/git/trees",
              {"base_tree": basetree, "tree": entries})["sha"]
commit = api("POST", "repos/AlecKriebel/Math/git/commits",
             {"message": "Finalize audited k307 proof and published preprint",
              "tree": newtree, "parents": [base, oldhead]})["sha"]
assert api("GET", "repos/AlecKriebel/Math/pulls/256")["head"]["sha"] == oldhead
updated = api("PATCH", "repos/AlecKriebel/Math/git/refs/heads/" + pr["head"]["ref"],
              {"sha": commit, "force": False})
assert updated["object"]["sha"] == commit
title = "5100017: prove k307 outer-pedal signed centroid with exact domain"
body = (
    "The ordered feet from a fixed point on the boundary tangent lines of a "
    "least-even-period elliptic billiard have a phase-independent signed area "
    "centroid wherever signed area is nonzero. This supplies an explicit formula, "
    "the exact exceptional circle for negative d, and all-point definedness for "
    "simple even orbits. The four-period converse is made explicit.\n\n"
    "Independent algebraic and geometric audits, reproduced exact certificates "
    "and high-precision physical orbit controls passed. Two fresh sequential "
    "preprint reviews found no remaining actionable issue. The original observation "
    "is credited to Reznik–Garcia–Koiller; bounded priority audits found no earlier "
    "covering proof and do not certify firstness.\n\n"
    "Preprint and verification package: " + doi + "\n\n"
    "AI tools were used extensively. This is unrefereed and has not received "
    "external human peer review."
)
api("PATCH", "repos/AlecKriebel/Math/pulls/256", {"title": title, "body": body})
result = {"utc": datetime.now(timezone.utc).isoformat(), "original_head": oldhead,
          "prepared_head": commit, "main_parent": base, "tree": newtree,
          "doi_url": doi, "target_queue_row": newrow, "title": title, "body": body,
          "shared_checkout_and_index_mutations": 0, "native_merge_pending": True}
(PUB / "PR_PREPARED.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k not in {"body", "target_queue_row"}}, indent=2))
