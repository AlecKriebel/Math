#!/usr/bin/env python3
"""Offline exact finite checks; not a proof of the general theorem.

Run with python -I -B to exclude untrusted cwd/PYTHONPATH imports.
All acceptance conditions use explicit exceptions, never assert.
"""
import sys
if not sys.flags.isolated:
    raise SystemExit("REJECT: run Python with -I (isolated mode)")
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def no_duplicates(items):
    obj = {}
    for key, value in items:
        require(key not in obj, "duplicate JSON key")
        obj[key] = value
    return obj


def reject_constant(value):
    raise ValueError("nonfinite JSON number")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=no_duplicates,
                      parse_constant=reject_constant)


def exact_keys(obj, keys):
    require(type(obj) is dict and set(obj) == set(keys), "object key/type mismatch")


def integer(value, low, high):
    require(type(value) is int and low <= value <= high, "exact integer required")
    return value


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def deriv(a):
    return trim([i*a[i] for i in range(1, len(a))] or [F(0)])


def divmod_poly(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], "division by zero polynomial")
    q = [F(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        shift = len(a) - len(b)
        coeff = a[-1] / b[-1]
        q[shift] += coeff
        for i, v in enumerate(b):
            a[i+shift] -= coeff*v
        a = trim(a)
    return trim(q), a


def quotient(a, b):
    q, r = divmod_poly(a, b)
    require(r == [0], "inexact polynomial quotient")
    return q


def gcd_poly(a, b):
    while b != [0]:
        a, b = b, divmod_poly(a, b)[1]
    return [x/a[-1] for x in a]


def squarefree(p):
    return quotient(p, gcd_poly(p, deriv(p)))


def variations(values):
    signs = [1 if x > 0 else -1 for x in values if x != 0]
    return sum(signs[i] != signs[i-1] for i in range(1, len(signs)))


def distinct_real_count(p):
    p = squarefree(p)
    if len(p) == 1:
        return 0
    chain = [p, deriv(p)]
    while chain[-1] != [0]:
        rem = divmod_poly(chain[-2], chain[-1])[1]
        if rem == [0]:
            break
        chain.append([-x for x in rem])
    minus = [q[-1] * (-1)**(len(q)-1) for q in chain]
    plus = [q[-1] for q in chain]
    return variations(minus) - variations(plus)


def analyze(coefficients):
    require(type(coefficients) is list and 2 <= len(coefficients) <= 10,
            "coefficient list length outside finite audit scope")
    for x in coefficients:
        integer(x, -1000000, 1000000)
    require(coefficients[-1] != 0, "leading zero")
    p = list(map(F, coefficients))
    d = len(p)-1
    q = add(mul(p, p), deriv(p))
    require(len(q)-1 == 2*d, "degree identity")
    sq = squarefree(q)
    outside = quotient(sq, gcd_poly(sq, p))
    nonreal_distinct = len(sq)-1-distinct_real_count(sq)
    outside_nonreal = len(outside)-1-distinct_real_count(outside)
    # Count multiplicity via successive gcd layers; each layer contributes
    # one copy of each still-present root, even for mixed multiplicities.
    real_mult, layer = 0, q
    while len(layer) > 1:
        real_mult += distinct_real_count(layer)
        layer = gcd_poly(layer, deriv(layer))
    # Exact identity in the inverse coordinate: A is the coefficient reversal.
    # G(w) = w*A/(A-w^(d+1)); G-w = w^(d+2)/(A-w^(d+1)).
    a = p[::-1]
    den = add(a, [F(0)]*(d+1)+[F(-1)])
    numer = add([F(0)]+a, [F(0)]+[-v for v in den])
    require(numer == [F(0)]*(d+2)+[F(1)], "local fixed-point identity")
    require(den[0] != 0, "invalid coordinate denominator")
    require(nonreal_distinct % 2 == 0 and outside_nonreal % 2 == 0,
            "conjugation parity")
    if d >= 2:
        require(outside_nonreal >= d-1, "finite theorem instance failed")
    return {"degree": d, "degree_Q": 2*d,
            "distinct_nonreal_Q": nonreal_distinct,
            "distinct_nonreal_outside_P": outside_nonreal,
            "real_Q_with_multiplicity": real_mult,
            "infinity_fixed_multiplicity": d+2}


def verify_manifest(root, path, pin):
    require(type(pin) is str and re.fullmatch(r"[0-9a-f]{64}", pin) is not None,
            "invalid external SHA-256 pin")
    require(not path.is_symlink(), "manifest symlink")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == pin, "external pin mismatch")
    manifest = read_json(path)
    exact_keys(manifest, ["schema_version", "files"])
    integer(manifest["schema_version"], 1, 1)
    require(type(manifest["files"]) is list and len(manifest["files"]) == 4,
            "manifest file list")
    names = set()
    for entry in manifest["files"]:
        exact_keys(entry, ["path", "bytes", "sha256"])
        name = entry["path"]
        require(type(name) is str and name in
                {"REPORT.md", "verify.py", "cases.json", "SOURCE_METADATA.json"},
                "unexpected manifest member")
        require(name not in names, "duplicate manifest member")
        names.add(name)
        integer(entry["bytes"], 1, 1000000)
        require(type(entry["sha256"]) is str and
                re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                "invalid member hash")
        target = root/name
        require(not target.is_symlink() and target.is_file(), "unsafe file")
        data = target.read_bytes()
        require(len(data) == entry["bytes"], "member byte count")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], "member hash")
    require({p.name for p in root.iterdir()} == names, "unmanifested public entries")


def selftest():
    rejected = 0
    for bad in [True, False, 1.0, float("nan"), float("inf"), -float("inf"),
                "1", None, {}, []]:
        try:
            integer(bad, 0, 10)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("bad scalar accepted")
    for bad in [[0, 0], [True, 1, 1], [0, 1.0, 1], [0, float("nan"), 1],
                [0, float("inf"), 1], [0, -float("inf"), 1], [0, 1, 0],
                [0, 1000001, 1], "0,0,1", [0], [0]*10+[1]]:
        try:
            analyze(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("bad polynomial accepted")
    for data in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}']:
        try:
            json.loads(data, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("bad JSON accepted")
    for p, expected in [([0, 0, 1], 1), ([-1, 0, 1], 2),
                        ([1, 0, 1], 0), ([0, 0, 0, 1], 1),
                        ([4, 0, -5, 0, 1], 4), ([1], 0)]:
        require(distinct_real_count(list(map(F, p))) == expected, "Sturm unit check")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    require(os.geteuid() != 0, "verification must run as actual nonroot")
    verify_manifest(args.root, args.manifest, args.expected_sha256)
    ledger = read_json(args.root/"cases.json")
    exact_keys(ledger, ["schema_version", "purpose", "cases"])
    integer(ledger["schema_version"], 1, 1)
    require(ledger["purpose"] == "finite exact regression checks, not universal proof",
            "case purpose")
    require(type(ledger["cases"]) is list and len(ledger["cases"]) == 24,
            "finite case count")
    seen = set()
    for case in ledger["cases"]:
        exact_keys(case, ["id", "coefficients_low_to_high", "expected"])
        require(type(case["id"]) is str and re.fullmatch(r"[a-z0-9_]{1,50}", case["id"]),
                "case identifier")
        require(case["id"] not in seen, "duplicate case identifier")
        seen.add(case["id"])
        result = analyze(case["coefficients_low_to_high"])
        exact_keys(case["expected"], result)
        for value in case["expected"].values():
            integer(value, 0, 100)
        require(result == case["expected"], "case expectation mismatch")
    rejected = selftest()
    print(json.dumps({"status": "PASS", "uid": os.geteuid(),
                      "finite_cases": len(seen), "negative_type_controls": rejected,
                      "universal_proof_checked_by_code": False,
                      "literature_classification": "KNOWN-SOLVED"}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print("REJECT: " + str(error), file=sys.stderr)
        sys.exit(1)
