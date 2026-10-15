"""Integrate only PR254 after verified publication and tracker append.

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
OUT = PUB / ("native-pr-integration-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
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
original = D / "submitted/unsolved_math_prioritization/attempts/5100020"
staged = HERE / "pr_update/5100020"
assert staged.is_dir()
assert not (PUB / 'PR_PREPARED.json').exists(), 'Prepared native head already exists; reconcile before retry'
pr = api("GET", "repos/AlecKriebel/Math/pulls/254")
assert pr["state"] == "open" and pr["draft"]
oldhead = pr["head"]["sha"]
assert oldhead == "73efd1fb8ba2d3039ed6692b3ad1dfa1e3085755"
livequeue = api("GET", "repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref="+oldhead)
liverows = [x for x in base64.b64decode(livequeue["content"]).decode().splitlines() if "5100020 / AMR-050-0020" in x]
assert len(liverows)==1 and liverows[0].split("|")[8].strip()=="claimed_solved"
base = api("GET", "repos/AlecKriebel/Math/git/ref/heads/main")["object"]["sha"]
basetree = api("GET", "repos/AlecKriebel/Math/git/commits/" + base)["tree"]["sha"]
queue = api("GET", "repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref=" + base)
text = base64.b64decode(queue["content"]).decode()
rows = [line for line in text.splitlines() if re.search(r"\|\s*5100020\s*/", line)]
assert len(rows) == 1
oldrow = rows[0]
cells = [cell.strip() for cell in oldrow.split("|")][1:-1]
assert cells[7] in {"queued", "claimed_solved"}
cells[7] = "claimed_solved"
cells[8] = "1/5"
cells[10] = (
    "2026-10-13: k403,a signed original-orbit origin-pedal times origin-antipedal "
    "area product proved for least odd strict elliptical-caustic families, including "
    "coprime stars; finite real intersections, direct circle extension, exact N4 "
    "negative control. Distinct meromorphic/geometric reproduction, bounded "
    "classical/recent priority audits and two sequential fresh preprint reviews "
    "passed. Observation and classical/prior pedal inputs credited; no firstness "
    "certificate. Unrefereed AI-assisted preprint: " + doi
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
        entries.append({"path": "unsolved_math_prioritization/attempts/5100020/" +
                        path.relative_to(staged).as_posix(),
                        "mode": "100644", "type": "blob", "content": path.read_text()})
# Include the finalized owned package and fresh review/clearance records.
paths = [p for p in HERE.iterdir() if p.is_file() and p.suffix in
         {".tex", ".pdf", ".zip", ".md", ".json", ".py", ".txt"}]
paths += [HERE / "LICENSE", D / "RESEARCH_LOG.md", HERE / "output/pdf/odd_origin_area_product.pdf"]
paths += [p for p in (HERE / "verification").rglob("*")
          if p.is_file() and "__pycache__" not in p.parts]
for folder in HERE.glob("review_*"):
    fm = folder / "FINAL_AUDIT_MANIFEST.json"
    if fm.exists():
        review=json.loads(fm.read_text());paths.append(fm)
        for pin in review['public_authored_files']:
            item=folder/pin['path'];assert item.resolve().is_relative_to(folder.resolve())
            assert item.stat().st_size==pin['bytes'] and hashlib.sha256(item.read_bytes()).hexdigest()==pin['sha256']
            paths.append(item)
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
             {"message": "Finalize audited k403a proof and published preprint",
              "tree": newtree, "parents": [base, oldhead]})["sha"]
assert api("GET", "repos/AlecKriebel/Math/pulls/254")["head"]["sha"] == oldhead
updated = api("PATCH", "repos/AlecKriebel/Math/git/refs/heads/" + pr["head"]["ref"],
              {"sha": commit, "force": False})
assert updated["object"]["sha"] == commit
title = "5100020: prove odd origin-pedal × antipedal signed-area invariant k403,a"
body = (
    "The signed area product of an elliptic billiard orbit's origin pedal and "
    "origin antipedal is phase independent for every least odd period with a "
    "strict confocal elliptical caustic, including admitted coprime stars. "
    "The construction-specific divisor analysis retains opposite-endpoint poles "
    "and proves finite real antipedal intersections. A direct circular extension "
    "and an exact same-caustic N4 counterexample delimit the theorem.\n\n"
    "Distinct independent meromorphic and Cartesian audits and reproduced exact "
    "and high-precision diagnostics passed. Two fresh sequential manuscript/package "
    "reviews found no remaining actionable issue. The original Reznik–Garcia–Koiller "
    "observation, classical Jacobi/cyclic and complex billiard methods, and earlier "
    "campaign pedal mechanism are credited. Extensive bounded primary-source "
    "priority audits found no covering earlier proof; historical firstness is not "
    "certified.\n\n"
    "Five-page preprint and portable verification package: " + doi + "\n\n"
    "AI tools were used extensively. This is unrefereed and has not received "
    "external human peer review or proof-assistant formalization. The requested "
    "Google Workspace tracker DOI row has been verified."
)
api("PATCH", "repos/AlecKriebel/Math/pulls/254", {"title": title, "body": body})
result = {"utc": datetime.now(timezone.utc).isoformat(), "original_head": oldhead,
          "prepared_head": commit, "main_parent": base, "tree": newtree,
          "doi_url": doi, "target_queue_row": newrow, "title": title, "body": body,
          "shared_checkout_and_index_mutations": 0, "native_merge_pending": True}
(PUB / "PR_PREPARED.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k not in {"body", "target_queue_row"}}, indent=2))
