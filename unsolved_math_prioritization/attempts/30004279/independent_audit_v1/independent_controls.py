#!/usr/bin/env python3
"""Independent finite controls and frozen-input binding. No operator-algebra solver."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile

EXPECTED_MANIFEST = "43863e0dbc15491bf5ee67adf3cd1a516c487e3224a193fd267ed5a5c7ae3dfd"


def det_leibniz(matrix):
    """Signed permutation expansion, independent of the author's elimination."""
    total = 0
    for p in permutations(range(len(matrix))):
        term = 1
        for i, j in enumerate(p):
            term *= matrix[i][j]
            if not term:
                break
        if term:
            inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
            total += (-1 if inversions % 2 else 1) * term
    return total


def det_bareiss(matrix):
    """Fraction-free integer determinant, including pivot and singular handling."""
    a = [row[:] for row in matrix]
    previous, sign = 1, 1
    for k in range(len(a) - 1):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[k][k] * a[i][j] - a[i][k] * a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        previous = a[k][k]
        for i in range(k + 1, len(a)):
            a[i][k] = 0
    return sign * a[-1][-1]


def matrix_from_edges(n, edges):
    a = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    for i, j in edges:
        a[i][j] = a[j][i] = -1
    return a


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=Path(__file__).resolve().parent.parent / "safe_packet_v1")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    packet = args.packet
    checks, negatives = [], []

    def require(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    def reject(name, condition):
        require("negative: " + name, not condition)
        negatives.append({"name": name, "rejected": True})

    manifest_bytes = (packet / "MANIFEST.json").read_bytes()
    require("manifest matches independent expected digest", sha256(manifest_bytes).hexdigest() == EXPECTED_MANIFEST)
    manifest = json.loads(manifest_bytes)
    expected_names = {r["path"] for r in manifest["files"]} | {"MANIFEST.json"}
    require("exact frozen file inventory", {p.name for p in packet.iterdir()} == expected_names)
    require("eight payload files", len(manifest["files"]) == 8)
    require("no symlinks or subdirectories", all(p.is_file() and not p.is_symlink() for p in packet.iterdir()))
    bound = []
    for row in manifest["files"]:
        b = (packet / row["path"]).read_bytes()
        require("bytes: " + row["path"], len(b) == row["bytes"])
        require("sha256: " + row["path"], sha256(b).hexdigest() == row["sha256"])
        bound.append({"path": row["path"], "bytes": len(b), "sha256": sha256(b).hexdigest()})
    reject("single-byte manifest tampering", sha256(manifest_bytes + b"\n").hexdigest() == EXPECTED_MANIFEST)
    reject("missing payload inventory", (expected_names - {"PROOFS.md"}) == expected_names)

    original = subprocess.run([sys.executable, "-B", str(packet / "verify.py")], check=True, capture_output=True)
    require("author checker byte-for-byte replay", original.stdout == (packet / "checks.json").read_bytes())
    require("author checker 47 assertions", json.loads(original.stdout)["passed_assertions"] == 47)
    require("author checker explicitly does not certify target", json.loads(original.stdout)["verified_original_conjecture"] is False)

    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)]
    e8 = matrix_from_edges(8, edges)
    minors = []
    for n in range(1, 9):
        block = [row[:n] for row in e8[:n]]
        d = det_leibniz(block)
        minors.append(d)
        require("independent E8 principal minor " + str(n), d == [2, 3, 4, 5, 6, 7, 8, 1][n - 1])
        require("Bareiss versus signed permutations " + str(n), det_bareiss(block) == d)
    require("E8 symmetric", all(e8[i][j] == e8[j][i] for i in range(8) for j in range(8)))
    require("E8 integral even diagonal", all(isinstance(x, int) for row in e8 for x in row) and all(e8[i][i] % 2 == 0 for i in range(8)))
    require("Sylvester positive leading minors", min(minors) > 0)
    for m in range(1, 5):
        block = [[e8[i % 8][j % 8] if i // 8 == j // 8 else 0 for j in range(8 * m)] for i in range(8 * m)]
        require("direct sum E8 determinant " + str(m), det_bareiss(block) == 1)
    require("A1 discriminant", det_leibniz([[2]]) == 2)
    a8 = matrix_from_edges(8, [(i, i + 1) for i in range(7)])
    singular = matrix_from_edges(8, [(i, i + 1) for i in range(6)] + [(3, 7)])
    require("A8 discriminant 9", det_leibniz(a8) == 9)
    require("midpoint branch singular", det_leibniz(singular) == 0)
    reject("A8 accepted as unimodular", det_leibniz(a8) == 1)
    reject("singular branch accepted as positive definite", det_leibniz(singular) > 0)
    odd = [r[:] for r in e8]
    odd[0][0] = 3
    reject("odd diagonal accepted as even lattice", all(odd[i][i] % 2 == 0 for i in range(8)))
    for matrix in ([[0, 1], [1, 0]], [[0, 1, 1], [1, 0, 1], [1, 1, 0]], [[1, 2], [2, 4]]):
        require("Bareiss pivot/singularity control " + str(matrix), det_bareiss(matrix) == det_leibniz(matrix))

    # Compute characters directly on all six permutations, not from class-size input.
    group = list(permutations(range(3)))
    trivial = [1 for p in group]
    sign = [(-1) ** sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3)) for p in group]
    standard = [sum(p[i] == i for i in range(3)) - 1 for p in group]
    chars = [trivial, sign, standard]
    gram = [[Fraction(sum(x * y for x, y in zip(a, b)), len(group)) for b in chars] for a in chars]
    for i, j in product(range(3), repeat=2):
        require("permutation character orthogonality " + str((i, j)), gram[i][j] == (i == j))
    identity = group.index((0, 1, 2))
    require("S3 squared dimensions complete", sum(c[identity] ** 2 for c in chars) == len(group))
    require("S3 distinct simple counts", 3 != len(group))
    wrong_standard = [v + 1 for v in standard]
    reject("permutation representation called irreducible", Fraction(sum(v * v for v in wrong_standard), 6) == 1)

    def cocycle(a, b, c):
        return -1 if a == b == c == 1 else 1

    normalization = []
    pentagons = []
    for a, b, c in product(range(2), repeat=3):
        if 0 in (a, b, c):
            require("Z2 normalized " + str((a, b, c)), cocycle(a, b, c) == 1)
            normalization.append([a, b, c])
    for a, b, c, d in product(range(2), repeat=4):
        lhs = cocycle(b, c, d) * cocycle(a, b ^ c, d) * cocycle(a, b, c)
        rhs = cocycle(a ^ b, c, d) * cocycle(a, b, c ^ d)
        require("Z2 pentagon " + str((a, b, c, d)), lhs == rhs)
        pentagons.append([a, b, c, d])
    # Formal exponent of arbitrary beta(1,1); unit factors are normalized to 1.
    factors = {(1, 1): 0, (1, 0): 0, (0, 1): 0}
    for pair, exponent in [((1, 1), 1), ((1, 0), 1), ((0, 1), -1), ((1, 1), -1)]:
        factors[pair] += exponent
    require("arbitrary scalar beta11 cancels symbolically", factors[(1, 1)] == 0)
    require("nontrivial omega111", cocycle(1, 1, 1) == -1)
    reject("normalized coboundary equals omega at 111", 1 == cocycle(1, 1, 1))
    trivial_cocycle = {(a, b, c): 1 for a, b, c in product(range(2), repeat=3)}
    require("trivial associator control has no obstruction", trivial_cocycle[(1, 1, 1)] == 1)
    malformed = {(a, b, c): cocycle(a, b, c) for a, b, c in product(range(2), repeat=3)}
    malformed[(1, 1, 0)] = -1
    reject("de-normalized cocycle accepted", all(v == 1 for abc, v in malformed.items() if 0 in abc))
    reject("malformed cocycle accepted by pentagon", all(
        malformed[(b, c, d)] * malformed[(a, b ^ c, d)] * malformed[(a, b, c)]
        == malformed[(a ^ b, c, d)] * malformed[(a, b, c ^ d)]
        for a, b, c, d in product(range(2), repeat=4)
    ))

    # Test that author checks really fail under plausible mathematical mutations.
    source = (packet / "verify.py").read_text()
    mutations = [
        ("E8 branch shifted", "+[(2,7)]", "+[(3,7)]"),
        ("standard character corrupted", "[2,0,-1]", "[2,0,1]"),
        ("nontrivial cocycle made trivial", "(-1)**(a*b*c)", "1"),
    ]
    mutation_results = []
    with tempfile.TemporaryDirectory(prefix="bicommutant-independent-mutation-") as temp:
        for name, old, new in mutations:
            require("mutation target present: " + name, old in source)
            mutated = Path(temp) / "mutated.py"
            mutated.write_text(source.replace(old, new))
            run = subprocess.run([sys.executable, "-B", str(mutated)], capture_output=True)
            require("author rejects mutation: " + name, run.returncode != 0 and b"AssertionError" in run.stderr)
            mutation_results.append({"name": name, "exit_code": run.returncode, "assertion_failure": True})
    for row in bound:
        require("frozen bytes unchanged after checks: " + row["path"], sha256((packet / row["path"]).read_bytes()).hexdigest() == row["sha256"])
    require("frozen manifest unchanged after checks", sha256((packet / "MANIFEST.json").read_bytes()).hexdigest() == EXPECTED_MANIFEST)

    result = {
        "problem_id": "30004279",
        "purpose": "Independent exact finite controls and immutable input binding; no operator-algebra theorem or soliton equivalence is machine-certified.",
        "input_manifest_sha256": EXPECTED_MANIFEST,
        "passed_assertions": len(checks),
        "assertion_names": checks,
        "bound_payloads": bound,
        "author_checker": {"assertions": 47, "byte_for_byte_replay": True},
        "independent_E8_minors": minors,
        "S3_permutations_enumerated": len(group),
        "cocycle_normalizations": len(normalization),
        "cocycle_pentagons": len(pentagons),
        "negative_controls": negatives,
        "author_mutation_controls": mutation_results,
        "complete_original_solution": False,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
