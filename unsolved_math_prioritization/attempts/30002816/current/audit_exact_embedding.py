#!/usr/bin/env python3
"""Independent exact-coordinate validator; reads inputs and writes only stdout.

The expected exterior coefficients are constructed from 4x4 determinants,
independently of the author's exterior-product routine. Integer pairs represent
Gaussian integers. All coefficient arithmetic is exact; no floating-point,
assert statements, source execution, network, or symbolic package is used.
"""
import argparse
import errno
from fractions import Fraction
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import sys


class AuditFailure(Exception):
    pass


def require(ok, code, detail=""):
    if not ok:
        raise AuditFailure(code + (": " + detail if detail else ""))


def ga(a, b):
    return a[0] + b[0], a[1] + b[1]


def gm(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def gc(a):
    return a[0], -a[1]


def gscale(a, k):
    return a[0]*k, a[1]*k


def sparse_add(target, key, value):
    total = target.get(key, 0) + value
    if total:
        target[key] = total
    else:
        target.pop(key, None)


PAIRS = list(combinations(range(6), 2))
QUADS = list(combinations(range(12), 4))
PERMS = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
         for p in permutations(range(4))]
LABELS = [["diag", a, a] for a in range(15)]
for a, b in combinations(range(15), 2):
    LABELS.extend([["real", a, b], ["imag", a, b]])
NORMS = [1]*15 + [2]*210


def determinant4_gaussian(matrix):
    total = (0, 0)
    for perm, sign in PERMS:
        term = (sign, 0)
        for row in range(4):
            term = gm(term, matrix[row][perm[row]])
            if term == (0, 0):
                break
        total = ga(total, term)
    return total


def reference_raw():
    """Return 4 times each elementary complex-matrix image in real coordinates."""
    result = {}
    for a, (i, j) in enumerate(PAIRS):
        for b, (r, s) in enumerate(PAIRS):
            columns = []
            for index, imag_sign in ((i, -1), (j, -1), (r, 1), (s, 1)):
                columns.append({2*index: (1, 0), 2*index+1: (0, imag_sign)})
            support = sorted(set().union(*(c.keys() for c in columns)))
            entries = {}
            for quad in combinations(support, 4):
                matrix = [[columns[col].get(row, (0, 0)) for col in range(4)]
                          for row in quad]
                value = determinant4_gaussian(matrix)
                if value != (0, 0):
                    entries[quad] = value
            result[a, b] = entries
    return result


def reference_columns():
    raw = reference_raw()
    result = []
    for kind, a, b in LABELS:
        col = {}
        for quad in set(raw[a, b]) | set(raw[b, a]):
            ab = raw[a, b].get(quad, (0, 0))
            ba = raw[b, a].get(quad, (0, 0))
            if kind == "diag":
                value = ab
            elif kind == "real":
                value = ga(ab, ba)
            else:
                value = gm((0, 1), ga(ab, gscale(ba, -1)))
            require(value[1] == 0, "REFERENCE_REALITY")
            if value[0]:
                col[quad] = value[0]
        result.append(col)
    return result


def load_certificate(path):
    with path.open(encoding="utf-8") as f:
        obj = json.load(f)
    required = {"description", "real_basis_order", "complex_bivector_pairs_0based",
                "columns", "gram_diagonal", "gram_off_diagonal", "inverse_on_image"}
    require(set(obj) == required, "SCHEMA_KEYS")
    require(obj["real_basis_order"] == [v for j in range(1, 7) for v in (f"e{j}", f"f{j}")],
            "REAL_BASIS_ORDER")
    require(obj["complex_bivector_pairs_0based"] == [list(p) for p in PAIRS],
            "COMPLEX_BASIS_ORDER")
    require(type(obj["columns"]) is list and len(obj["columns"]) == 225,
            "COLUMN_COUNT")
    require(obj["gram_diagonal"] == NORMS and obj["gram_off_diagonal"] == 0,
            "GRAM_METADATA")
    require(obj["inverse_on_image"] == "diag(gram_diagonal)^(-1) times A^T",
            "INVERSE_METADATA")
    columns = []
    for index, col in enumerate(obj["columns"]):
        require(set(col) == {"label", "entries"}, "COLUMN_SCHEMA")
        require(col["label"] == LABELS[index], "HERMITIAN_BASIS_ORDER")
        require(type(col["entries"]) is list, "ENTRY_SCHEMA")
        entries = {}
        previous = None
        for entry in col["entries"]:
            require(type(entry) is list and len(entry) == 2, "ENTRY_SCHEMA")
            key, value = entry
            require(type(key) is list and len(key) == 4 and
                    all(type(i) is int for i in key) and
                    0 <= key[0] < key[1] < key[2] < key[3] < 12, "ENTRY_INDEX")
            key = tuple(key)
            require(previous is None or previous < key, "ENTRY_ORDER_OR_DUPLICATE")
            require(type(value) is str, "ENTRY_VALUE_TYPE")
            try:
                coefficient = Fraction(value)
            except (ValueError, ZeroDivisionError):
                raise AuditFailure("ENTRY_VALUE_PARSE")
            require(coefficient and str(coefficient) == value, "ENTRY_VALUE_CANONICAL")
            require((4*coefficient).denominator == 1, "ENTRY_DENOMINATOR")
            entries[key] = int(4*coefficient)
            previous = key
        columns.append(entries)
    return columns


def phi(col, pure=False):
    return sum(col.get((2*i, 2*i+1, 2*j, 2*j+1), 0) for i, j in PAIRS
               if not pure or (i < 3 and j < 3) or (i >= 3 and j >= 3))


def validate_columns(columns):
    reference = reference_columns()
    for index, (actual, expected) in enumerate(zip(columns, reference)):
        require(actual == expected, "COORDINATE_MISMATCH", f"column {index}")
    for a, col in enumerate(columns):
        for b in range(a, 225):
            product = sum(value*columns[b].get(key, 0) for key, value in col.items())
            require(product == (16*NORMS[a] if a == b else 0), "GRAM_IDENTITY")
        kind, i, j = LABELS[a]
        require(phi(col) == (4 if kind == "diag" else 0), "PHI_TRACE")
        p, q = PAIRS[i]
        require(phi(col, pure=True) == (4 if kind == "diag" and
                    ((p < 3 and q < 3) or (p >= 3 and q >= 3)) else 0),
                "Q_PURE_TRACE")
    return reference


# Sparse polynomials indexed by sorted tuples of variable numbers.
def poly_add(p, q, scale=1):
    out = dict(p)
    for monomial, coefficient in q.items():
        sparse_add(out, monomial, scale*coefficient)
    return out


def gaussian_polynomial_product(p, q):
    out = {}
    for left, lc in p.items():
        for right, rc in q.items():
            key = tuple(sorted(left + right))
            total = ga(out.get(key, (0, 0)), gm(lc, rc))
            if total != (0, 0):
                out[key] = total
            else:
                out.pop(key, None)
    return out


def symbolic_bivector():
    a = [{(2*j,): (1, 0), (2*j+1,): (0, 1)} for j in range(6)]
    b = [{(12+2*j,): (1, 0), (13+2*j,): (0, 1)} for j in range(6)]
    output = []
    for i, j in PAIRS:
        left = gaussian_polynomial_product(a[i], b[j])
        right = gaussian_polynomial_product(a[j], b[i])
        for key, coefficient in right.items():
            total = ga(left.get(key, (0, 0)), gscale(coefficient, -1))
            if total != (0, 0):
                left[key] = total
            else:
                left.pop(key, None)
        output.append(left)
    return output


def symbolic_real_plane():
    # Four columns a, Ja, b, Jb; each entry is a signed variable.
    rows = []
    for j in range(6):
        rows.append([(1, 2*j), (-1, 2*j+1), (1, 12+2*j), (-1, 13+2*j)])
        rows.append([(1, 2*j+1), (1, 2*j), (1, 13+2*j), (1, 12+2*j)])
    result = {}
    for quad in QUADS:
        determinant = {}
        for perm, sign in PERMS:
            selected = [rows[row][perm[i]] for i, row in enumerate(quad)]
            coefficient = sign
            for factor, _ in selected:
                coefficient *= factor
            sparse_add(determinant, tuple(sorted(var for _, var in selected)), coefficient)
        if determinant:
            result[quad] = determinant
    return result


def verify_general_projector(columns):
    z = symbolic_bivector()
    image = {}
    expected_trace = {}
    expected_q = {}
    for label, column in zip(LABELS, columns):
        kind, a, b = label
        h = gaussian_polynomial_product(z[a], {k: gc(v) for k, v in z[b].items()})
        coordinate = {k: v[1 if kind == "imag" else 0] for k, v in h.items()
                      if v[1 if kind == "imag" else 0]}
        if kind == "diag":
            require(all(v[1] == 0 for v in h.values()), "PROJECTOR_DIAGONAL_REAL")
            expected_trace = poly_add(expected_trace, coordinate, 4)
            i, j = PAIRS[a]
            if (i < 3 and j < 3) or (i >= 3 and j >= 3):
                expected_q = poly_add(expected_q, coordinate, 4)
        for quad, coefficient in column.items():
            image[quad] = poly_add(image.get(quad, {}), coordinate, coefficient)
    image = {quad: polynomial for quad, polynomial in image.items() if polynomial}
    plane = symbolic_real_plane()
    require(set(image) == set(plane), "GENERAL_PROJECTOR_SUPPORT")
    for quad in image:
        require(image[quad] == {key: 4*value for key, value in plane[quad].items()},
                "GENERAL_PROJECTOR_IDENTITY", str(quad))
    actual_trace, actual_q = {}, {}
    for i, j in PAIRS:
        polynomial = image.get((2*i, 2*i+1, 2*j, 2*j+1), {})
        actual_trace = poly_add(actual_trace, polynomial)
        if (i < 3 and j < 3) or (i >= 3 and j >= 3):
            actual_q = poly_add(actual_q, polynomial)
    require(actual_trace == expected_trace, "GENERAL_PROJECTOR_PHI")
    require(actual_q == expected_q, "GENERAL_PROJECTOR_Q")
    return {"independent_real_variables": 24, "verified_exterior_coordinates": len(QUADS),
            "nonzero_coordinate_polynomials": len(image),
            "polynomial_terms_after_cancellation": sum(len(p) for p in image.values())}


def verify_mixed_plucker():
    mixed = {(i, j+3): 3*i+j for i in range(3) for j in range(3)}
    count = 0
    for a, b, c, d in combinations(range(6), 4):
        actual = {}
        for left, right, sign in (((a, b), (c, d), 2),
                                 ((a, c), (b, d), -2),
                                 ((a, d), (b, c), 2)):
            if left in mixed and right in mixed:
                sparse_add(actual, tuple(sorted((mixed[left], mixed[right]))), sign)
        expected = {}
        if b < 3 <= c:
            sparse_add(expected, tuple(sorted((3*a+c-3, 3*b+d-3))), -2)
            sparse_add(expected, tuple(sorted((3*a+d-3, 3*b+c-3))), 2)
            count += 1
        require(actual == expected, "MIXED_PLUCKER_MINORS")
    require(count == 9, "MIXED_MINOR_COUNT")
    return count


def verify_readonly(root):
    require(os.getuid() == 1000 and os.geteuid() == 1000, "UID_NOT_1000")
    status = Path("/proc/self/status").read_text()
    capabilities = next(line.split()[1] for line in status.splitlines() if line.startswith("CapEff:"))
    require(int(capabilities, 16) == 0, "EFFECTIVE_CAPABILITIES")
    for target, mode in ((root / "checks" / "EMBEDDING_CERTIFICATE.json", "ab"),
                         (root / ".audit_readonly_probe", "xb")):
        try:
            with target.open(mode):
                pass
        except OSError as exc:
            require(exc.errno == errno.EROFS, "NOT_READONLY_MOUNT", str(exc.errno))
        else:
            raise AuditFailure("READONLY_PROBE_OPENED")
    return {"uid": os.getuid(), "euid": os.geteuid(), "effective_capabilities": capabilities,
            "existing_and_new_file_open": "EROFS"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--readonly-root", type=Path)
    args = parser.parse_args()
    readonly = verify_readonly(args.readonly_root) if args.readonly_root else None
    columns = load_certificate(args.certificate)
    validate_columns(columns)
    symbolic = verify_general_projector(columns)
    minor_count = verify_mixed_plucker()
    print(json.dumps({"status": "PASS", "arithmetic": "integer pairs and exact rational parsing",
                      "python_optimization": sys.flags.optimize, "columns": 225,
                      "rank": 225, "gram_diagonal": {"1": 15, "2": 210},
                      "phi_trace": True, "q_pure_trace": True,
                      "general_projector": symbolic, "mixed_minors": minor_count,
                      "readonly": readonly}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (AuditFailure, ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        sys.exit(1)
