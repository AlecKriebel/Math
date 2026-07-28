#!/usr/bin/env python3
"""Hash and strictly replay the retained radius-two RUP certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
CNF = HERE / "closure-radius-2.cnf"
PROOF = HERE / "closure-radius-2-proof.additions.drat"
EXPECTED = {
    "cnf": {
        "bytes": 4_667_702,
        "sha256": "8bd4ae50e2ac06deb6560c4ff482eb19d7b64a4769029284da4660ccbefd1b55",
    },
    "proof": {
        "bytes": 9_367_094,
        "lines": 168_880,
        "sha256": "f5fcbe26885ab229636d511d2b1ee47203478002fb22ce34407f1182d1c1eeea",
    },
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    with PROOF.open("rb") as handle:
        proof_lines = sum(1 for _ in handle)
    observed = {
        "cnf": {"bytes": CNF.stat().st_size, "sha256": digest(CNF)},
        "proof": {
            "bytes": PROOF.stat().st_size,
            "lines": proof_lines,
            "sha256": digest(PROOF),
        },
    }
    if observed != EXPECTED:
        raise AssertionError({"expected": EXPECTED, "observed": observed})
    checker = CAMPAIGN / "tools" / "drat_trim_2023_05_22" / "drat-trim"
    completed = subprocess.run(
        [
            str(checker),
            str(CNF),
            str(PROOF),
            "-I",
            "-f",
            "-W",
            "-U",
            "-t",
            "120",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if (
        completed.returncode != 0
        or "s VERIFIED" not in completed.stdout
        or "0 RAT lemmas" not in completed.stdout
    ):
        raise AssertionError(completed.stdout)
    payload = {
        "status": "PASS",
        "artifacts": observed,
        "checker": str(checker.relative_to(CAMPAIGN)),
        "mode": ["ASCII", "forward", "warning-fatal", "RUP-only"],
        "checker_output": completed.stdout,
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "radius2-replay-result.json").write_text(raw, encoding="utf-8")
    print(raw, end="")


if __name__ == "__main__":
    main()
