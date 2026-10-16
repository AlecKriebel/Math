#!/usr/bin/env python3
"""Scoped main-only integration of the accepted PR149 result."""
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

A = Path(__file__).resolve().parent
C = A.parents[2]
GH = "/opt/homebrew/Cellar/gh/2.85.0/bin/gh"
REPO = "repos/AlecKriebel/Math"
EXPECTED = "926b608906b582c41aa89b3917c10b9998a5e29f"
ORIGINAL = "dde6ebe550ed7fe2e2fc8a1ff06fb13105be97ae"

def api(endpoint, method="GET", body=None):
    args = [GH, "api", REPO + "/" + endpoint, "--method", method]
    data = None
    if body is not None:
        args += ["--input", "-"]
        data = json.dumps(body)
    run = subprocess.run(args, input=data, text=True, capture_output=True)
    if run.returncode:
        raise RuntimeError(run.stderr[:1000])
    return json.loads(run.stdout)

def main():
    gate = json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text())
    pub = json.loads((A/"ZENODO_PUBLICATION_READBACK.json").read_text())
    if gate["status"] != "READY_FOR_AUTHORIZED_PUBLICATION" or pub["state"] != "published" or pub["id"] != 23306203:
        raise RuntimeError("publication not accepted")
    if api("git/ref/heads/main")["object"]["sha"] != EXPECTED:
        raise RuntimeError("MAIN moved; inspect new state")
    pr = api("pulls/149")
    if pr["head"]["sha"] != ORIGINAL or pr["state"] != "open" or pr["draft"]:
        raise RuntimeError("PR state/head changed")
    parent = api("git/commits/" + EXPECTED)
    native = A/"integration_preparation/native"
    overlay = {}
    for p in sorted(native.rglob("*")):
        if p.is_file():
            overlay["unsolved_math_prioritization/attempts/5100006/"+p.relative_to(native).as_posix()] = p
    overlay["unsolved_math_prioritization/QUEUE.md"] = A/"integration_preparation/QUEUE.accepted.md"
    names = [
        "ROOT_PUBLICATION_GATE.json", "PUBLICATION_CANDIDATE_INVENTORY.json",
        "ZENODO_PUBLICATION_READBACK.json", "WHOLE_PACKAGE_R1_ACCEPTANCE.json",
        "RESEARCH_LOG.md", "whole_package_review_r1/REVIEW.md",
        "whole_package_review_r1/RESULT.json",
        "whole_package_review_r1/REVIEWED_CANDIDATE_INVENTORY.json",
        "whole_package_review_r1/reviewed_support.zip",
        "whole_package_review_r2/REVIEW.md", "whole_package_review_r2/RESULT.json",
        "whole_package_review_r2/native_consistency.json",
        "whole_package_review_r2/repair_propagation.json",
        "whole_package_review_r2/independent_geometry_checks.py",
        "whole_package_review_r2/independent_geometry_results.json",
        "priority_recent_catalog_check/REPORT.md",
        "priority_recent_catalog_check/KNOWN_PAPER_BODY_CHECK.json",
        "priority_recent_catalog_check/AUTHOR_RELEASE_WINDOW_SUMMARY.json",
    ]
    names += ["publication_package_v1/"+p.relative_to(A/"publication_package_v1").as_posix()
              for p in sorted((A/"publication_package_v1").rglob("*")) if p.is_file()]
    prefix = A.relative_to(C).as_posix()+"/"
    for name in names:
        overlay[prefix+name] = A/name
    entries, pins = [], {}
    for name, path in sorted(overlay.items()):
        body = path.read_bytes()
        sha = hashlib.sha1(b"blob "+str(len(body)).encode()+b"\0"+body).hexdigest()
        entry = {"path":name, "mode":"100644", "type":"blob"}
        try:
            entry["content"] = body.decode("utf-8")
        except UnicodeDecodeError:
            blob = api("git/blobs","POST",{"content":base64.b64encode(body).decode(),"encoding":"base64"})
            if blob["sha"] != sha: raise RuntimeError("binary blob mismatch")
            entry["sha"] = sha
        entries.append(entry)
        pins[name] = {"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"git_blob":sha}
    tree = api("git/trees","POST",{"base_tree":parent["tree"]["sha"],"tree":entries})
    commit = api("git/commits","POST",{
        "message":"Merge PR149: exact focal-distance product period criterion\n\nAccept the original head with the adversarially verified full least-period classification and repeated-return counterexample. Published AI-assisted unrefereed note: https://doi.org/10.5281/zenodo.23306203. R1 reference locator repaired, fresh R2 PASS. Classical machinery credited; priority bounded and DG2023 full-text gap disclosed. Queue conflict resolved only for problem5100006; all other base-tree paths preserved. Tracker sign-in is pending.",
        "tree":tree["sha"],"parents":[EXPECTED,ORIGINAL]})
    record = {"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "status":"SCOPED_TWO_PARENT_MERGE_PREPARED_MAIN_NOT_UPDATED",
              "expected_main":EXPECTED,"original_PR_head":ORIGINAL,
              "parent_tree":parent["tree"]["sha"],"tree":tree["sha"],"commit":commit["sha"],
              "selected_files":pins,"native_paths":18,"queue_rows_changed":1,
              "DOI":pub["doi"],"tracker_updated":False}
    (A/"SCOPED_MERGE_PREPARATION.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({key:record[key] for key in ["status","expected_main","original_PR_head","tree","commit","native_paths","queue_rows_changed","DOI"]}))
    print("Selected paths:",len(entries))

if __name__ == "__main__":
    main()

