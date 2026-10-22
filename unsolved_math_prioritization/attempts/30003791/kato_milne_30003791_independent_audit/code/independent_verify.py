#!/usr/bin/env python3
"""Independent exact controls and frozen-payload integrity checks.

Uses no author arithmetic implementation, no network, and no third-party package.
Finite algebra checks are not proofs of universal linkage or vanishing.
Default inputs are siblings of this audit directory; explicit paths are accepted.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path, PurePosixPath
import random
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_BYTES = 20996
ARCHIVE_SHA256 = "6ab69c7efbb362416f44de1fb8c642eaa5ce0877aec1869b67859012f2f428e5"
PRIMES = (2, 3, 5, 7, 11, 13)


def require(condition, description):
    if not condition:
        raise ValueError(description)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def freeze_check(root, archive):
    frozen = archive.read_bytes()
    require(len(frozen) == ARCHIVE_BYTES, "archive byte count")
    require(sha(frozen) == ARCHIVE_SHA256, "archive SHA-256")
    manifest = json.loads((root / "MANIFEST.json").read_text())
    declared = {"MANIFEST.json"}
    for record in manifest["files"]:
        name = record["path"]
        relative = PurePosixPath(name)
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe path")
        require(name not in declared, "duplicate manifest entry")
        declared.add(name)
        path = root / name
        require(not path.is_symlink() and path.is_file(), "not a regular payload file")
        require(path.resolve().is_relative_to(root.resolve()), "escaping payload path")
        content = path.read_bytes()
        require(len(content) == record["bytes"] and sha(content) == record["sha256"], name)
    actual = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symlink in authored tree")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    require(actual == declared and len(actual) == 9, "payload file set mismatch")
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        require(len(names) == len(set(names)) == 9 and set(names) == declared, "ZIP names")
        for entry in bundle.infolist():
            require(not stat.S_ISLNK(entry.external_attr >> 16), "ZIP symlink")
            require(bundle.read(entry.filename) == (root / entry.filename).read_bytes(),
                    "ZIP and directory differ")
    with tempfile.TemporaryDirectory(prefix="kato-independent-replay-") as cwd:
        raw = subprocess.check_output([sys.executable, "-B", str(root / "code/check_controls.py")], cwd=cwd)
        require(raw == (root / "verification/controls.json").read_bytes(), "author replay differs")
        replay = json.loads(raw)
        require(replay["status"] == "PASS", "author replay status")
    return {"status": "PASS", "archive_bytes": len(frozen), "archive_sha256": sha(frozen),
            "safe_payload_files": len(actual), "author_control_replay": "byte-identical from temporary cwd"}


# Sparse matrices over F_p[u,v,v^-1], independent of the author's crossed-product
# normal-form engine. Keys are (row, column, u exponent, v exponent).
def matrix_sum(p, *terms):
    out = {}
    for multiplier, matrix in terms:
        for key, value in matrix.items():
            out[key] = (out.get(key, 0) + multiplier * value) % p
    return {key: value for key, value in out.items() if value}


def matrix_mul(left, right, p):
    out = {}
    rows = {}
    for (r, c, u, v), value in right.items():
        rows.setdefault(r, []).append((c, u, v, value))
    for (r, c, u, v), x in left.items():
        for d, w, z, y in rows.get(c, ()):
            key = (r, d, u + w, v + z)
            out[key] = (out.get(key, 0) + x * y) % p
    return {key: value for key, value in out.items() if value}


def matrix_power(matrix, exponent, p):
    out = {(k, k, 0, 0): 1 for k in range(p)}
    for _ in range(exponent):
        out = matrix_mul(out, matrix, p)
    return out


def presentation_check():
    result = []
    for p in PRIMES:
        one = {(k, k, 0, 0): 1 for k in range(p)}
        i = matrix_sum(p, (1, {(k, k, 1, 0): 1 for k in range(p)}),
                       (1, {(k, k, 0, 0): (-k) % p for k in range(p)}))
        j = {((k + 1) % p, k, 0, int(k == p - 1)): 1 for k in range(p)}
        invj = {((k - 1) % p, k, 0, -int(k == 0)): 1 for k in range(p)}
        a = matrix_sum(p, (1, {(k, k, p, 0): 1 for k in range(p)}),
                       (-1, {(k, k, 1, 0): 1 for k in range(p)}))
        b = {(k, k, 0, 1): 1 for k in range(p)}
        invb = {(k, k, 0, -1): 1 for k in range(p)}
        tests = [matrix_mul(j, invj, p) == one, matrix_mul(invj, j, p) == one,
                 matrix_sum(p, (1, matrix_power(i, p, p)), (-1, i)) == a,
                 matrix_power(j, p, p) == b,
                 matrix_mul(matrix_mul(j, i, p), invj, p) == matrix_sum(p, (1, i), (1, one))]
        newi = matrix_sum(p, (-1, i))
        tests += [matrix_sum(p, (1, matrix_power(newi, p, p)), (-1, newi)) == matrix_sum(p, (-1, a)),
                  matrix_power(invj, p, p) == invb,
                  matrix_mul(matrix_mul(invj, newi, p), j, p) == matrix_sum(p, (1, newi), (1, one)),
                  matrix_sum(p, (-1, newi)) == i,
                  matrix_mul(b, matrix_power(invj, p - 1, p), p) == j]
        require(all(tests), "matrix presentation identity")
        # Inverting j without negating i reverses the translation: it is not the
        # claimed presentation for odd p. This deliberately wrong variant is rejected.
        wrong = matrix_mul(matrix_mul(invj, i, p), j, p) == matrix_sum(p, (1, i), (1, one))
        require(wrong == (p == 2), "negative matrix control")
        require(((-1) ** 3 % p == 1) == (p == 2), "appended symbol sign")
        result.append({"p": p, "matrix_identities": len(tests),
                       "incorrect_sign_variant_rejected": p != 2,
                       "old_detector": 1, "new_detector": (-1) % p})
    return result


def add_term(out, key, value, p):
    out[key] = (out.get(key, 0) + value) % p
    if not out[key]:
        del out[key]


# A logarithmic form has key (exponent tuple, ordered differential-index tuple).
def exterior_derivative(form, p):
    out = {}
    for (exponents, slots), coefficient in form.items():
        for index, exponent in enumerate(exponents):
            if index in slots:
                continue
            newslots = tuple(sorted((index,) + slots))
            sign = (-1) ** sum(slot < index for slot in slots)
            add_term(out, (exponents, newslots), sign * exponent * coefficient, p)
    return out


def differential_check():
    rng = random.Random(30003791)
    checks = {"p_basis_reconstructions": 0, "p_basis_derivatives": 0,
              "top_exact_residues": 0, "artin_schreier_residues": 0,
              "d_squared_zero": 0, "wrong_nonconstant_detectors_rejected": 0}
    for p in PRIMES:
        for r in range(1, 6):
            zero = (0,) * r
            for _ in range(20):
                polynomial = {zero: 1}
                for _ in range(80):
                    exponents = tuple(rng.randrange(-25, 26) for _ in range(r))
                    add_term(polynomial, exponents, rng.randrange(p), p)
                decomposition = {}
                for exponents, coefficient in polynomial.items():
                    residue = tuple(e % p for e in exponents)
                    quotients = tuple(e // p for e in exponents)
                    decomposition.setdefault(residue, {})[quotients] = coefficient
                rebuilt = {}
                for residue, coefficients in decomposition.items():
                    for q, c in coefficients.items():
                        add_term(rebuilt, tuple(p * a + b for a, b in zip(q, residue)), pow(c, p, p), p)
                require(rebuilt == polynomial, "p-basis reconstruction with negative exponents")
                checks["p_basis_reconstructions"] += 1
                for index in range(r):
                    direct = {e: e[index] * c % p for e, c in polynomial.items() if e[index] * c % p}
                    by_basis = {e: (e[index] % p) * c % p for e, c in rebuilt.items() if (e[index] % p) * c % p}
                    require(direct == by_basis, "algebraic p-basis derivation")
                    checks["p_basis_derivatives"] += 1
                wp = {}
                for e, c in polynomial.items():
                    add_term(wp, tuple(p * a for a in e), pow(c, p, p), p)
                    add_term(wp, e, -c, p)
                require(wp.get(zero, 0) == 0, "Artin-Schreier constant coefficient")
                checks["artin_schreier_residues"] += 1
                eta = {}
                for omitted in range(r):
                    slots = tuple(k for k in range(r) if k != omitted)
                    for e, c in polynomial.items():
                        add_term(eta, (e, slots), c * rng.randrange(p), p)
                d_eta = exterior_derivative(eta, p)
                require(d_eta.get((zero, tuple(range(r))), 0) == 0, "top exact residue")
                checks["top_exact_residues"] += 1
                q = rng.randrange(r + 1)
                slots = tuple(sorted(rng.sample(range(r), q)))
                omega = {(e, slots): c for e, c in polynomial.items()}
                require(exterior_derivative(exterior_derivative(omega, p), p) == {}, "d squared")
                checks["d_squared_zero"] += 1
            unit = (1,) + (0,) * (r - 1)
            wrong = exterior_derivative({(unit, tuple(range(1, r))): 1}, p)
            require(wrong.get((unit, tuple(range(r))), 0) == 1, "nonconstant detector negative control")
            checks["wrong_nonconstant_detectors_rejected"] += 1
    return checks


def degrees_check():
    count = 0
    for n in range(2, 25):
        theta = tuple(range(1, n - 1))
        for extras in ((n - 1, n), (n - 1, n, n + 1)):
            require(len(theta) == n - 2, "factor degree")
            require(len(theta + extras) + 1 == n + len(extras) - 1, "appended degree")
            for selected in extras:
                remaining = tuple(x for x in extras if x != selected)
                require(set(theta + (selected,) + remaining) == set(theta + extras), "nonzero-by-append slots")
            count += 1
    return {"pair_triple_degree_cases": count, "universal_field_linkage_tested": False}


def main():
    parent = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-root", type=Path, default=parent / "kato_milne_30003791")
    parser.add_argument("--archive", type=Path, default=parent / "KATO_MILNE_30003791_SAFE_FREEZE.zip")
    args = parser.parse_args()
    result = {"schema": "kato-milne-independent-controls-v1", "status": "PASS",
              "scope": "Integrity, exact finite controls and negative controls only; no universal linkage proof.",
              "freeze": freeze_check(args.author_root.resolve(), args.archive.resolve()),
              "independent_matrix_presentation": presentation_check(),
              "independent_differential_controls": differential_check(), "degree_controls": degrees_check()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
