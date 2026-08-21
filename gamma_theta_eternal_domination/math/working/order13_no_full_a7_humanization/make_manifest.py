#!/usr/bin/env python3
"""Write hashes and sizes for the retained humanization package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = (
    "NOTE.md",
    "RESEARCH_LOG.md",
    "run_closure_radius.py",
    "closure-radius-2.cnf",
    "closure-radius-2-proof.additions.drat",
    "replay_radius2.py",
    "radius2-replay-result.json",
    "closure-radius-2-core.cnf",
    "closure-radius-2-core-census.txt",
    "closure-radius-1.model",
    "closure-radius-1.json",
    "closure-radius-1.graph.json",
    "closure-radius-2-anchors-01.model",
    "closure-radius-2-anchors-01.json",
    "closure-radius-2-anchors-01.graph.json",
    "closure-radius-2-anchors-02.model",
    "closure-radius-2-anchors-02.json",
    "closure-radius-2-anchors-02.graph.json",
    "closure-radius-2-anchors-12.model",
    "closure-radius-2-anchors-12.json",
    "closure-radius-2-anchors-12.graph.json",
    "verify_two_slice_controls.py",
    "two-slice-controls-result.json",
    "build_semantic_reduction.py",
    "semantic.json",
    "run_ablation.py",
    "summarize_model.py",
    "ablation-omit-theta.model",
    "ablation-omit-theta.graph.json",
    "ablation-omit-theta.verifier-b.json",
    "ablation-omit-gamma.model",
    "ablation-omit-gamma.graph.json",
    "ablation-omit-gamma.verifier-b.json",
    "ablation-omit-closure.model",
    "ablation-omit-closure.graph.json",
    "ablation-omit-closure.verifier-b.json",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    missing = [name for name in FILES if not (HERE / name).is_file()]
    if missing:
        raise AssertionError(f"missing manifest files: {missing}")
    payload = {
        "status": "COMPLETE",
        "scope": (
            "Order-13 structured residual core humanization, radius-two "
            "UNSAT certificate candidate, and sharp partial-closure controls."
        ),
        "limitations": [
            "No universal theorem and no gamma-theta counterexample.",
            (
                "The radius-two UNSAT generator and proof passed independent "
                "clean-room reconstruction and strict replay in "
                "reviews/order13_radius2_humanization_hostile/."
            ),
            "The result covers only the already reduced order-13 parameter-three residual branch.",
            "SAT controls are partial-family controls with gamma_infinity=4, not eternal equality examples.",
        ],
        "files": {
            name: {
                "bytes": (HERE / name).stat().st_size,
                "sha256": digest(HERE / name),
            }
            for name in FILES
        },
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "manifest.json").write_text(raw, encoding="utf-8")
    print(raw, end="")


if __name__ == "__main__":
    main()
