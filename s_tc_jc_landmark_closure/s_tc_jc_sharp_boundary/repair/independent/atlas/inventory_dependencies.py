#!/usr/bin/env python3
"""Inventory finite-atlas dependencies across trees and ZIP members."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile


NAMES = {
    "regenerate_nonroot_algebra.py", "regenerate_cycle_algebra.py",
    "regenerate_nonroot_topology_atlases.py", "regenerate_directed_pair_universe.cpp",
    "regenerate_signature_relation.cpp", "review_directed_pair_universe.cpp",
    "core_enumerator.py", "quartet_invariant_exact_certificate.json",
    "compile_cycle_theta_atlas_v2.py", "generate_cut_assignments.py",
    "prototype_seven_census.py", "primitive_networks.py", "primitive_compiler.py",
    "generate_cycle_theta_end_to_end.py", "certificate_library.py",
    "k4_features.npz", "all_F_patterns.json", "hard_cross_pair_cover.json",
    "cut_sign_library.json", "cycle_theta_support_completion_corrected.json",
    "verify_seven_port_closure.py", "review_seven_port_closure.py",
    "audit_gate2_nonroot_full_closure.py", "exact_open_cube_sign.py",
    "theta_k5_strong_signatures.bin", "theta_k5_weak_signatures.bin",
    "theta_k6_strong_signatures.bin", "theta_k6_weak_signatures.bin",
    "theta_k5_directed_pairs.tsv", "theta_k6_directed_pairs.tsv",
    "canonical_theta_k5_strict_signs.json",
    "canonical_theta_k6_special_strict_signs.json",
    "directed_k5_end_to_end_assignments.json",
    "directed_k6_end_to_end_assignments.json", "cut_end_to_end_assignments.json",
    "cycle_theta_end_to_end_assignments_v2.json", "seven_port_closure.json",
}


def file_hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(roots: list[Path]) -> dict:
    ordinary = []
    archives = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.name in NAMES:
                ordinary.append({"name": path.name, "path": str(path), "bytes": path.stat().st_size, "sha256": file_hash(path)})
            if path.is_file() and path.suffix.lower() == ".zip":
                try:
                    with zipfile.ZipFile(path) as archive:
                        for member in archive.infolist():
                            name = Path(member.filename).name
                            if name in NAMES:
                                archives.append({"name": name, "archive": str(path), "member": member.filename, "bytes": member.file_size})
                except zipfile.BadZipFile:
                    pass
    found = {row["name"] for row in ordinary} | {row["name"] for row in archives}
    return {
        "ordinary": sorted(ordinary, key=lambda x: (x["name"], x["path"])),
        "archive_members": sorted(archives, key=lambda x: (x["name"], x["archive"], x["member"])),
        "missing_everywhere": sorted(NAMES - found),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps(inventory(args.roots), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
