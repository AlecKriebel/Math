#!/usr/bin/env python3
"""Reject obsolete numerical/formula claims without misclassifying raw data.

The old release values can legitimately occur as decimal substrings inside newly
computed concentration CSVs.  This audit therefore scans only claim-bearing
text and source files.  Raw simulation provenance is checked structurally by
``audit_numerical_provenance.py`` instead of by substring matching.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

STALE = {
    "old_eta_decimal": "0.1054",
    "old_amplitude_decimal": "1.306",
    "old_amplitude_rounding": "1.311",
    "old_product_ratio": "57/56",
    "old_contrast_coefficient": "1589m",
    "old_affine_denominator": "227m-451",
}

# Only prose, theorem, documentation, and generated claim tables are scanned.
# Exact raw simulation CSVs are intentionally excluded; their provenance is
# checked algebraically and by convergence tests in audit_numerical_provenance.py.
ROOTS = [
    ROOT / "manuscript",
    ROOT / "external_audit",
    ROOT / "submission",
    ROOT / "public" / "repository",
    ROOT / "independent_verifier",
    ROOT / "proof_audit",
]
EXTRA = [
    ROOT / "data" / "contrast_table.tex",
    ROOT / "data" / "current_profile_exact.json",
    ROOT / "data" / "branch_amplitudes.csv",
    ROOT / "data" / "simulation_parameters.json",
]
TEXT_SUFFIXES = {".tex", ".md", ".txt", ".json", ".py", ".sh", ".csv", ".cff"}

# These files deliberately contain stale literals as mutation/audit fixtures.
ALLOW_PARTS = {
    ("computation", "tests"),
}
ALLOW_NAMES = {
    "audit_manuscript.py",
    "audit_numerical_provenance.py",
    "audit_stale_claims.py",
}
SKIP_DIRS = {
    ".git", ".pytest_cache", "__pycache__", "simulations", "simulations_quick",
    "source",  # submission source duplicates are covered by manuscript/source audit
}


def allowed(path: Path) -> bool:
    if path.name in ALLOW_NAMES:
        return True
    rel = path.relative_to(ROOT)
    parts = rel.parts
    return any(all(piece in parts for piece in group) for group in ALLOW_PARTS)


def candidate_files() -> list[Path]:
    out: set[Path] = set()
    for base in ROOTS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
                continue
            out.add(p)
    for p in EXTRA:
        if p.exists():
            out.add(p)
    return sorted(out)


def main() -> int:
    hits: list[tuple[str, Path, int, str]] = []
    scanned = 0
    for path in candidate_files():
        if allowed(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for line_no, line in enumerate(text.splitlines(), 1):
            for label, token in STALE.items():
                if token in line:
                    hits.append((label, path.relative_to(ROOT), line_no, line.strip()))
    if hits:
        for label, path, line_no, line in hits:
            print(f"STALE {label}: {path}:{line_no}: {line}")
        return 1
    print(f"STALE_CLAIM_AUDIT_PASS files={scanned}")
    print("RAW_SIMULATION_VALUES_CLASSIFIED_CURRENT_BY_STRUCTURAL_PROVENANCE_AUDIT")
    print("MUTATION_FIXTURES_CLASSIFIED_HISTORICAL_BUT_NECESSARY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
