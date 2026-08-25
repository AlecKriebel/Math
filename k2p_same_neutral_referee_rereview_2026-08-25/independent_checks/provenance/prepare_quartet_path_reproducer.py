#!/usr/bin/env python3
"""Extract only the inputs needed for the quartet path-dependence reproducer."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


RELATIVES = (
    "work/quartet_separation_closure/PROOF.md",
    "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json",
    "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json",
    "work/quartet_separation_closure/test_quartet_semantics_mutations.py",
    "work/quartet_separation_closure/verify_quartet_logic.py",
    "proof_compression_submission/article/main.tex",
    "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
    "work/global_theorem_closure/GLOBAL_PROOF.md",
    "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--destination", type=Path, action="append", required=True)
    args = parser.parse_args()
    prefix = "k2p_principal_d_plus_submission_referee/"
    with zipfile.ZipFile(args.archive) as archive:
        for destination in args.destination:
            for relative in RELATIVES:
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(prefix + relative))
    print(f"extracted_files_per_tree={len(RELATIVES)} trees={len(args.destination)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
