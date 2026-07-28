#!/usr/bin/env python3
"""Write hashes and claim classes for the reciprocity checkpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = {
    "NOTE.md": "PROVED_AND_OPEN_SCOPE",
    "RESEARCH_LOG.md": "RESEARCH_LOG",
    "verify_countermodel.py": "RIGOROUS_VERIFIER",
    "countermodel_result.json": "RIGOROUS_RESULT",
    "verify_countermodel.log": "RIGOROUS_REPLAY_LOG",
    "exhaustive_two_vertex_extension.py": "OBSERVED_FINITE_GENERATOR",
    "extension_result.json": "OBSERVED_FINITE_RESULT",
    "extension_run.log": "OBSERVED_FINITE_LOG",
    "search_countermodel.py": "EXPLORATORY_GENERATOR",
    "random_partition_9.json": "EXPLORATORY_RESULT",
    "random_partition_12.json": "EXPLORATORY_RESULT",
    "build_exact_kernel_cnf.py": "EXPLORATORY_EXACT_CNF_GENERATOR",
    "make_manifest.py": "MANIFEST_GENERATOR",
}


def main() -> None:
    records = []
    for relative, classification in FILES.items():
        path = HERE / relative
        data = path.read_bytes()
        records.append(
            {
                "path": relative,
                "classification": classification,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = {
        "schema": "greatest-family-reciprocity-manifest-v1",
        "date": "2026-07-28",
        "rigorous_claims": [
            (
                "GEjbug has (gamma,i,alpha,gamma_infinity,theta)="
                "(2,2,3,3,3) and its literal greatest triple-family "
                "violates pairwise complementary-exchange reciprocity."
            ),
            (
                "Conditional on equality reciprocity, the C-108 active "
                "response relation is symmetric."
            ),
        ],
        "open_claim": (
            "Pairwise reciprocity under "
            "gamma=alpha=gamma_infinity=k remains open."
        ),
        "finite_guardrail": (
            "The two-vertex extension census and random partition sweeps "
            "are OBSERVED only; they are not a universal theorem or a "
            "gamma-theta resolution."
        ),
        "files": records,
    }
    (HERE / "MANIFEST.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
