#!/usr/bin/env python3
"""Audit immutability and scope of candidate commit 6a69254e."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
REPOSITORY = CAMPAIGN.parent
CANDIDATE = CAMPAIGN / "math" / "working" / "qq1_anchor_auxiliary_ladder"
CANDIDATE_COMMIT = "6a69254e73ed83ac98f832cc5c95d83522398705"
CANDIDATE_MANIFEST_SHA256 = (
    "eaa02cbf2abc9249dee09e0bdfb591b9cd5c87a1970c3086aac82f2674ecda68"
)


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def committed_bytes(path: Path) -> bytes:
    relative = path.relative_to(REPOSITORY)
    completed = subprocess.run(
        ["git", "show", f"{CANDIDATE_COMMIT}:{relative}"],
        cwd=REPOSITORY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    demand(not completed.stderr, f"git show wrote stderr for {relative}")
    return completed.stdout


def main() -> None:
    resolved = subprocess.run(
        ["git", "rev-parse", CANDIDATE_COMMIT],
        cwd=REPOSITORY,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.strip()
    demand(resolved == CANDIDATE_COMMIT, "candidate commit does not resolve exactly")

    manifest_path = CANDIDATE / "CANDIDATE_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    demand(digest(manifest_bytes) == CANDIDATE_MANIFEST_SHA256, "candidate manifest changed")
    demand(committed_bytes(manifest_path) == manifest_bytes, "manifest differs from candidate commit")
    manifest = json.loads(manifest_bytes)
    demand(
        manifest["classification"] == "REFUTED_CANDIDATE_WITH_FIXED_EXACT_CONTROL",
        "candidate classification is not a refutation",
    )

    artifact_hashes = {}
    for relative, expected in manifest["artifacts_sha256"].items():
        path = CANDIDATE / relative
        actual_bytes = path.read_bytes()
        actual = digest(actual_bytes)
        demand(actual == expected, f"{relative} disagrees with candidate manifest")
        demand(committed_bytes(path) == actual_bytes, f"{relative} differs from candidate commit")
        artifact_hashes[relative] = actual

    ablation = read_json(CANDIDATE / "ABLATION_RESULTS.json")
    demand(ablation["classification"] == "OBSERVED_DISCOVERY_ONLY", "ablation promoted")
    demand("no proof logs" in ablation["scope"], "ablation omits proof-log disclaimer")
    demand("no finite or all-order theorem" in ablation["scope"], "ablation overclaims scope")
    demand(ablation["base"]["status"] == "UNSAT", "base observation changed")
    demand(
        all(row["status"] in {"SAT", "UNSAT"} for row in ablation["ablations"].values()),
        "unexpected ablation status",
    )
    demand(
        not any(
            path.suffix.lower() in {".drat", ".lrat", ".frat", ".proof"}
            for path in CANDIDATE.iterdir()
        ),
        "candidate unexpectedly contains a proof log",
    )

    note = (CANDIDATE / "NOTE.md").read_text(encoding="utf-8")
    compact_note = " ".join(note.split())
    demand(note.count(r"\text{``protect \(p,q\) against every auxiliary partner''}") == 1, "first scope quote duplicated or missing")
    demand(note.count(r"\text{``protect every pair touching \(T=\{x,p,q\}\)''}") == 1, "second scope quote duplicated or missing")
    demand("**OBSERVED_DISCOVERY_ONLY**" in note, "note omits discovery-only label")
    demand("These outcomes have no proof logs and are not promoted" in note, "note promotes UNSAT")
    demand("not a counterexample" in compact_note, "note omits gamma-theta disclaimer")
    demand(
        "does not eliminate canonical QQ1 under equality" in compact_note,
        "note overstates QQ1 scope",
    )

    not_claimed = set(manifest["scope"]["not_claimed"])
    demand("No counterexample to the gamma-theta conjecture." in not_claimed, "missing counterexample disclaimer")
    demand("No elimination of canonical QQ1 under gamma=3." in not_claimed, "missing QQ1 disclaimer")
    demand("No certified order-16 or order-17 UNSAT result." in not_claimed, "missing finite disclaimer")
    demand("No all-order theorem from the SAT/CEGAR traces." in not_claimed, "missing solver disclaimer")

    result = {
        "schema": "qq1-anchor-auxiliary-hostile-candidate-audit-v1",
        "status": "PASS",
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_manifest_sha256": digest(manifest_bytes),
        "candidate_artifact_sha256": dict(sorted(artifact_hashes.items())),
        "scope": {
            "candidate_classification": manifest["classification"],
            "ablation_classification": ablation["classification"],
            "unlogged_unsat": "OBSERVED_DISCOVERY_ONLY",
            "scope_quotes_each_occur_once": True,
            "conjecture_counterexample_claimed": False,
            "gamma3_qq1_exclusion_claimed": False,
            "finite_unsat_claimed": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
