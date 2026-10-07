#!/usr/bin/env python3
"""Independent exact controls and verifier fault injection; no source material.

Usage: python -B INDEPENDENT_CHECKS.py PATH_TO_FROZEN_AUTHOR_PACKET
All faults are introduced in temporary copies, never in the author packet.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ANCHOR = "f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59"
counts = {}


def check(name, condition):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    counts[name] = counts.get(name, 0) + 1


def matrix_product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def main():
    if len(sys.argv) != 2:
        raise RuntimeError("Provide the frozen author packet directory.")
    source = Path(sys.argv[1]).resolve()
    original = {p.name: p.read_bytes() for p in source.iterdir()}
    check("manifest_anchor", hashlib.sha256(original["MANIFEST.json"]).hexdigest() == ANCHOR)
    manifest = json.loads(original["MANIFEST.json"])
    check("exact_inventory", set(original) == {m["path"] for m in manifest["files"]} | {"MANIFEST.json"})
    for m in manifest["files"]:
        check("independent_size_binding", len(original[m["path"]]) == m["bytes"])
        check("independent_hash_binding", hashlib.sha256(original[m["path"]]).hexdigest() == m["sha256"])

    # Gaussian-integer computation is independent of the author's trace recurrence.
    real, imag = 1, 0
    for n in range(1, 1025):
        real, imag = 3 * real - 4 * imag, 4 * real + 3 * imag
        check("gaussian_norm", real * real + imag * imag == 25 ** n)
        check("gaussian_trace_residue", (2 * real) % 5 == 1)
        check("gaussian_nonidentity", (real, imag) != (5 ** n, 0))
        check("gaussian_negative_power_nonidentity", (real, -imag) != (5 ** n, 0))

    B = [[3, -4], [4, 3]]
    Bmod = [[x % 5 for x in row] for row in B]
    B2mod = [[x % 5 for x in row] for row in matrix_product(B, B)]
    check("nonzero_idempotent_mod_five", B2mod == Bmod and Bmod != [[0, 0], [0, 0]])
    identity = [[F(1), F(0)], [F(0), F(1)]]
    A = [[F(x, 5) for x in row] for row in B]
    AT = [list(row) for row in zip(*A)]
    check("rotation_inverse", matrix_product(AT, A) == identity)
    check("rotation_determinant", A[0][0] * A[1][1] - A[0][1] * A[1][0] == 1)
    quarter = [[0, -1], [1, 0]]
    square = matrix_product(quarter, quarter)
    check("finite_rotation_negative_control", matrix_product(square, square) == identity)
    hyperbolic = [[F(2), F(0)], [F(0), F(1, 2)]]
    check("determinant_one_insufficient", matrix_product(hyperbolic, hyperbolic) != identity)
    check("three_end_combinatorial_threshold", 3 - 1 >= 2)
    check("two_end_negative_control", 2 - 1 < 2)

    verifier = original["VERIFY.py"]
    modes = [[], ["-O"]]
    for flags in modes:
        proc = subprocess.run([sys.executable, *flags, "-B", str(source / "VERIFY.py"), ANCHOR], capture_output=True)
        check("author_verifier_positive_replay", proc.returncode == 0)
        for fault in ["wrong_anchor", "proof_byte_change", "missing_member", "extra_member", "symlink_member",
                      "duplicate_manifest_key", "duplicate_inventory_member", "unsafe_inventory_path", "boolean_size"]:
            with tempfile.TemporaryDirectory(prefix="veech-audit-") as temporary:
                root = Path(temporary)
                for name, data in original.items():
                    (root / name).write_bytes(data)
                expected = ANCHOR
                if fault == "wrong_anchor":
                    expected = "0" * 64
                elif fault == "proof_byte_change":
                    (root / "PROOF.md").write_bytes(original["PROOF.md"] + b"\n")
                elif fault == "missing_member":
                    (root / "README.md").unlink()
                elif fault == "extra_member":
                    (root / "UNEXPECTED.txt").write_text("fault injection\n")
                elif fault == "symlink_member":
                    (root / "README.md").unlink()
                    (root / "README.md").symlink_to(source / "README.md")
                else:
                    altered = json.loads(original["MANIFEST.json"])
                    if fault == "duplicate_manifest_key":
                        raw = b'{"schema":"duplicate",' + original["MANIFEST.json"].lstrip()[1:]
                    else:
                        if fault == "duplicate_inventory_member":
                            altered["files"].append(altered["files"][0].copy())
                        elif fault == "unsafe_inventory_path":
                            altered["files"][0]["path"] = "../outside"
                        elif fault == "boolean_size":
                            altered["files"][0]["bytes"] = True
                        raw = (json.dumps(altered, indent=2) + "\n").encode()
                    (root / "MANIFEST.json").write_bytes(raw)
                    expected = hashlib.sha256(raw).hexdigest()
                check("verifier_code_preserved_in_fixture", (root / "VERIFY.py").read_bytes() == verifier)
                proc = subprocess.run([sys.executable, *flags, "-B", str(root / "VERIFY.py"), expected], capture_output=True)
                check("reject_" + fault, proc.returncode != 0)

    check("author_packet_preserved", original == {p.name: p.read_bytes() for p in source.iterdir()})
    print(json.dumps({"status": "PASS", "author_manifest_sha256": ANCHOR,
                      "checks_by_family": counts, "total_controls": sum(counts.values()),
                      "limitations": "Exact finite controls and byte validation; the written arguments, not the finite computations, establish the all-n obstruction and the topology/conformal facts."}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
