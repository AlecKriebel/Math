#!/usr/bin/env python3
"""Write deterministic input and review SHA-256 manifests."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


INPUTS = (
    "docs/DEFINITIONS_LOCK.md",
    "docs/ROOT_REDUCTION_THEOREM.md",
    "docs/GENERATOR_AND_SUPPORT_THEOREM.md",
    "docs/LOCAL_ATLAS_THEOREM.md",
    "docs/GLOBAL_THEOREM_DRAFT.md",
    "primary/core_universe.py",
    "primary/completion_universe.py",
    "primary/support_universe.py",
    "primary/graph_model.py",
    "primary/jc_tensor.py",
    "primary/atlas_compiler.py",
    "primary/cycle_theta_union_compiler.py",
    "primary/certificates/core_universe.json",
    "primary/certificates/completion_universe.json",
    "primary/certificates/support_universe.json",
    "primary/certificates/invariant_multihomogeneity.json",
    "primary/certificates/descriptor_bits_cache.json.gz",
    "primary/certificates/bounded_atlas_summary.json",
    "primary/certificates/bounded_relations_n3.jsonl.gz",
    "primary/certificates/bounded_sign_library_n3.json",
    "primary/certificates/bounded_relations_n4.jsonl.gz",
    "primary/certificates/bounded_sign_library_n4.json",
    "primary/certificates/bounded_relations_n5.jsonl.gz",
    "primary/certificates/bounded_sign_library_n5.json",
    "primary/certificates/bounded_relations_n6.jsonl.gz",
    "primary/certificates/bounded_sign_library_n6.json",
    # Legacy relation names are retained in the manifest for forensic clarity;
    # they do not satisfy the current compiler's hard-cover contract.
    "primary/certificates/theta_relations_n4.jsonl.gz",
    "primary/certificates/theta_relations_n5.jsonl.gz",
    "primary/certificates/theta_relations_n6.jsonl.gz",
    "primary/certificates/cycle_theta_union_summary.json",
    "primary/certificates/cycle_theta_union_relations.jsonl.gz",
    "primary/certificates/cycle_theta_union_signs.json",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    input_lines = []
    for relative in INPUTS:
        path = REPO / relative
        input_lines.append(
            f"{digest(path)}  {relative}" if path.exists() else f"MISSING  {relative}"
        )
    (HERE / "INPUTS.sha256").write_text("\n".join(input_lines) + "\n")

    excluded = {"MANIFEST.sha256"}
    review_files = sorted(
        path for path in HERE.rglob("*")
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts
    )
    lines = [f"{digest(path)}  {path.relative_to(HERE)}" for path in review_files]
    (HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    print(f"inputs={len(input_lines)} review_files={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
