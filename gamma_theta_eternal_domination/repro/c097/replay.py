#!/usr/bin/env python3
"""Fail-closed replay of the complete order-13 parameter-three exclusion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


CAMPAIGN = Path(__file__).resolve().parents[2]
ACCEPTANCE = CAMPAIGN / "results" / "order13_k3_complete_acceptance.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(script: Path, *, timeout: int) -> dict:
    completed = subprocess.run(
        [sys.executable, "-I", "-B", "-W", "error", str(script)],
        cwd=CAMPAIGN,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{script.relative_to(CAMPAIGN)} failed with exit "
            f"{completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    result = json.loads(completed.stdout)
    if result.get("verdict") != "PASS":
        raise RuntimeError(
            f"{script.relative_to(CAMPAIGN)} did not return PASS"
        )
    return result


def main() -> None:
    acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    c096 = acceptance["accepted_claims"]["C-096"]
    c097 = acceptance["accepted_claims"]["C-097"]

    pinned = {
        c096["instance"]["path"]: c096["instance"]["sha256"],
        c096["proof"]["path"]: c096["proof"]["sha256"],
        c096["review"]["path"]: c096["review"]["sha256"],
        c097["instance"]["path"]: c097["instance"]["sha256"],
        c097["proof"]["path"]: c097["proof"]["sha256"],
        c097["review"]["path"]: c097["review"]["sha256"],
    }
    hash_checks = {
        relative: sha256(CAMPAIGN / relative) == expected
        for relative, expected in pinned.items()
    }
    if not all(hash_checks.values()):
        raise RuntimeError(f"artifact hash mismatch: {hash_checks}")

    four_neutral = run_json(
        CAMPAIGN
        / "math"
        / "working"
        / "order13_no_full_tight_five_five"
        / "replay.py",
        timeout=120,
    )
    sharp_control = run_json(
        CAMPAIGN
        / "math"
        / "working"
        / "order13_no_full_tight_five_five"
        / "verify_q3_control.py",
        timeout=120,
    )
    residual = run_json(
        CAMPAIGN
        / "reviews"
        / "order13_no_full_a7_hostile"
        / "checker.py",
        timeout=600,
    )

    result = {
        "schema": "gamma-theta-c097-replay-v1",
        "verdict": "PASS",
        "claim": (
            "No 13-vertex graph satisfies "
            "gamma(G)=gamma_infinity(G)=3<theta(G)."
        ),
        "universal_conjecture_status": "UNRESOLVED",
        "hash_checks": hash_checks,
        "four_neutral_replay": {
            "verdict": four_neutral["verdict"],
            "formula_byte_identity": four_neutral["checks"][
                "formula_byte_identity"
            ],
            "strict_rup": four_neutral["checks"]["rup_only"],
        },
        "three_neutral_control": {
            "verdict": sharp_control["verdict"],
            "graph6": sharp_control["labeled_graph6"],
            "parameters": sharp_control["parameters"],
            "greatest_family_size": sharp_control["greatest_kernel_sizes"]["3"],
        },
        "residual_replay": {
            "verdict": residual["verdict"],
            "formula_byte_identity": residual["source"]["checks"][
                "byte_identical_clean_room_reconstruction"
            ],
            "coverage": residual["local_semantics"]["coverage"],
            "addition_only_rup": residual["proofs"]["addition_only"][
                "replay"
            ]["zero_RAT_lemmas"],
            "theta_gap_ablation_sat": residual[
                "theta_gap_ablation_control"
            ]["reported_SAT"],
        },
        "scope_limits": acceptance["scope_limits"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
