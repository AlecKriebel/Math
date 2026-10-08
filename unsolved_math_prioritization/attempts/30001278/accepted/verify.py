#!/usr/bin/env python3
"""Exact, bounded mathematical controls. No network or source fixtures needed.

This is not a proof assistant and does not verify the imported Hodge-theoretic
theorems. No Python assert is used; optimized Python runs the same checks.
"""

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from math import comb, gcd, prod
import argparse
import json


PUBLIC_FILES = {
    "01_UPPER_BREAK.md", "02_KUMMER_TOWER.md", "03_HEIGHT_ANNIHILATORS.md",
    "04_CYCLOTOMIC_LATTICES.md", "05_INERTIA_ORDER.md", "NORMALIZATIONS.md",
    "README.md", "SOURCE_MAP.md", "SOURCE_METADATA.json", "CLAIM_LEDGER.json",
    "CHECK_RESULTS.json", "NEGATIVE_RESULTS.json", "negative_controls.py", "verify.py"
}


def strict_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, "duplicate JSON key: " + key)
            out[key] = value
        return out
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


def vp(x, p):
    if x == 0:
        raise ValueError("valuation of zero is not used")
    x = abs(x)
    v = 0
    while x % p == 0:
        v += 1
        x //= p
    return v


def parameters(p, r):
    if p < 3 or r < 1:
        raise ValueError("this packet requires p >= 3 and r >= 1")
    a = 0
    while r > (p - 1) * p**a:
        a += 1
    b = Q(r, (p - 1) * p**a)
    return a, b


def target(p, e, n, r):
    a, b = parameters(p, r)
    return 1 + e * (n + a + b) - Q(1, p**(n + a))


def upper(p, e, n, r):
    a, b = parameters(p, r)
    s = n + a
    return 1 + e * s + max(e * b - Q(1, p**s), Q(e, p - 1))


def polynomial_multiply(a, b, modulus):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % modulus
    return c


def polynomial_power(a, r, modulus):
    ans = [1]
    for _ in range(r):
        ans = polynomial_multiply(ans, a, modulus)
    return ans


def times_u_mod(vector, monic, modulus):
    """Multiply by u using ordinary polynomial long division, not binomials."""
    degree = len(monic) - 1
    require(len(vector) == degree and monic[-1] == 1, "bad polynomial basis")
    leading = vector[-1]
    out = [0] + vector[:-1]
    for i in range(degree):
        out[i] = (out[i] - leading * monic[i]) % modulus
    return out


def exact_nilpotence(E, p, n, r):
    modulus = p**n
    f = polynomial_power(E, r, modulus)
    degree = len(f) - 1
    x = [1] + [0] * (degree - 1)
    for N in range(1, degree * n + 1):
        x = times_u_mod(x, f, modulus)
        if not any(x):
            return N
    raise RuntimeError("universal nilpotence bound failed")


def binomial_nilpotence(p, n, r):
    for m in range(r, r + n):
        if all(m - j + vp(comb(m, j), p) >= n for j in range(r)):
            return m
    raise RuntimeError("binomial upper bound failed")


def matrix_character(a, p, m, n):
    q = p**n
    require((1 - a) % p**m == 0, "character outside selected base field")
    return (a % q, ((1 - a) // p**m) % q, 0, 1)


def matrix_multiply(A, B, q):
    a, b, c, d = A
    e, f, g, h = B
    return ((a * e + b * g) % q, (a * f + b * h) % q,
            (c * e + d * g) % q, (c * f + d * h) % q)


def mathematical_controls():
    counts = {}
    parameter_cases = 0
    exceptional_cases = 0
    endpoint_cases = 0
    for p in (3, 5, 7, 11, 13):
        for r in range(1, 401):
            a, b = parameters(p, r)
            require(Q(1, p) < b <= 1, "normalization interval")
            require(Q(r, p - 1) == p**a * b, "normalization identity")
            for n in range(1, 6):
                for e in (1, 2, 3, 7, 17, 64):
                    s = n + a
                    B = target(p, e, n, r)
                    U = upper(p, e, n, r)
                    delta = max(Q(0), Q(e * (p**a - r), (p - 1) * p**a)
                                + Q(1, p**s))
                    require(U - B == delta, "exact upper/different loss")
                    require((U == B) == (r >= p**a + 1), "integer-region equivalence")
                    require((e * (r - p**a) >= Q(p - 1, p**n)) == (U == B),
                            "integer threshold conversion")
                    require(B > 0, "positive target")
                    # The old theorem uses n*r in the weight normalizer, but
                    # retains the same exponent n in its other terms.
                    old_B = target(p, e, n, n * r)
                    require(old_B >= B, "old bound cannot imply sharper by sign error")
                    require((old_B == B) == (n == 1), "strict monotonicity for n>1")
                    F = lambda j: 1 + e * j + (Q(e * r * p**n, p - 1) - 1) / p**j
                    require(F(s) == B, "tower target identity")
                    require(F(s) - F(s - 1) == e * (1 - Q(r, p**a))
                            + Q(p - 1, p**s), "tower difference identity")
                    require(r < p**(a + 1), "strict Galois-control threshold")
                    require((p**s > Q(r * p**n, p - 1)) == (b < 1),
                            "strict finite-level precision endpoint")
                    require(e * p * b > e, "lower-level precision exceeds mod p")
                    if delta:
                        exceptional_cases += 1
                        require(F(s) > F(s - 1), "exceptional tower optimization")
                        if a:
                            require(delta < Q(e, p * (p - 1)) + Q(1, p**s),
                                    "exceptional loss upper bound")
                    if b == 1:
                        endpoint_cases += 1
                        require(U == B, "endpoint covered independently")
                    parameter_cases += 1
    counts["exact_parameter_cases"] = parameter_cases
    counts["exceptional_parameter_cases"] = exceptional_cases
    counts["beta_one_parameter_cases"] = endpoint_cases

    scalar_cases = 0
    scalar_failure_cases = 0
    for p in (3, 5, 7):
        for n in range(1, 6):
            for r in range(1, 31):
                m = binomial_nilpotence(p, n, r)
                require(r <= m <= r + n - 1, "scalar nilpotence bounds")
                require((m == r) == (n <= 1 + vp(r, p)), "sharp scalar criterion")
                minimum = min(k + vp(comb(r, k), p) for k in range(1, r + 1))
                require(minimum == 1 + vp(r, p), "binomial coefficient minimum")
                for e in (1, 2, 3):
                    E = [-p] + [0] * (e - 1) + [1]
                    measured = exact_nilpotence(E, p, n, r)
                    require(measured == e * m, "independent polynomial reduction")
                    scalar_cases += 1
                if n > 1 + vp(r, p):
                    require((r * p) % p**n != 0, "explicit nonvanishing coefficient")
                    scalar_failure_cases += 1
    counts["independent_scalar_polynomial_cases"] = scalar_cases
    counts["false_N_equals_er_witnesses"] = scalar_failure_cases

    general_cases = 0
    exact_divisible_cases = 0
    for p in (3, 5):
        for n in range(1, 5):
            for r in range(1, 16):
                R = p**(n - 1) * ((r + p**(n - 1) - 1) // p**(n - 1))
                for e in (1, 2, 3):
                    for coefficients in ((1, -1, 2), (-1, 2, 1)):
                        E = [p * coefficients[i] for i in range(e)] + [1]
                        require(vp(E[0], p) == 1, "Eisenstein constant")
                        N = exact_nilpotence(E, p, n, r)
                        require(N <= e * R, "general rounded-height bound")
                        require(N <= e * r * n, "universal monomial bound")
                        if r % p**(n - 1) == 0:
                            require(N == e * r, "general divisible-height exactness")
                            exact_divisible_cases += 1
                        general_cases += 1
    counts["general_Eisenstein_polynomial_cases"] = general_cases
    counts["general_divisible_height_cases"] = exact_divisible_cases

    lattice_cases = 0
    lattice_product_cases = 0
    for p in (3, 5, 7):
        for m in range(1, 4):
            for n in range(1, 4):
                modulus = p**n
                for t in range(modulus):
                    a = 1 + p**m * t
                    A = matrix_character(a, p, m, n)
                    require((A == (1, 0, 0, 1)) == (t == 0), "exact lattice kernel")
                    require(gcd(A[0], p) == 1, "invertible lattice action")
                    require(A[0] % p == 1 and A[3] == 1, "trivial residual diagonal")
                    lattice_cases += 1
                    for u in range(min(p, modulus)):
                        b = 1 + p**m * u
                        require(matrix_multiply(A, matrix_character(b, p, m, n), modulus)
                                == matrix_character(a * b, p, m, n), "lattice group law")
                        lattice_product_cases += 1
                e = (p - 1) * p**(m - 1)
                cyclotomic_relative = e * ((m + n - Q(1, p - 1))
                                          - (m - Q(1, p - 1)))
                require(cyclotomic_relative == e * n, "relative cyclotomic different")
                require(target(p, e, n, 1) - cyclotomic_relative
                        == 1 + Q(e, p - 1) - Q(1, p**n) > 0,
                        "non-split lattice is not a counterexample")
    counts["lattice_character_residue_cases"] = lattice_cases
    counts["lattice_group_law_cases"] = lattice_product_cases

    cyclotomic_bound_cases = 0
    ore_cases = 0
    general_linear_cases = 0
    for p in (3, 5, 7, 11):
        for n in range(1, 6):
            for e in (1, 2, 5, 17):
                for r in (1, 2, p - 1, p, p**2 - p + 1, p**2, p**2 + 1):
                    a, b = parameters(p, r)
                    s = n + a
                    B = target(p, e, n, r)
                    split_bound = e * (n - Q(1, p - 1))
                    require(B - split_bound == 1 + e * (a + b + Q(1, p - 1))
                            - Q(1, p**s) > 0, "split cyclotomic margin")
                    cyclotomic_bound_cases += 1
                    for t in range(s + 1):
                        for tame in (1, p - 1, p + 1):
                            require(gcd(tame, p) == 1, "tame multiplier")
                            m = tame * p**t
                            ore = e * t + 1 - Q(1, m)
                            require(ore < B, "inertia-order sufficient criterion")
                            # Distinct derivative-term residue classes ensure
                            # no cancellation; this tests the index arithmetic.
                            if m <= 300:
                                require(len({i - 1 for i in range(1, m + 1)}) == m,
                                        "distinct derivative exponents")
                            ore_cases += 1
                for d in range(1, 9):
                    gl_order = p**(d*d*(n-1)) * prod(p**d - p**i for i in range(d))
                    require(vp(gl_order, p) == d*d*(n-1) + d*(d-1)//2,
                            "general linear group order valuation")
                    general_linear_cases += 1
    counts["cyclotomic_margin_cases"] = cyclotomic_bound_cases
    counts["inertia_order_margin_cases"] = ore_cases
    counts["general_linear_order_cases"] = general_linear_cases

    require(parameters(3, 7) == (2, Q(7, 18)), "residual example normalization")
    require(target(3, 1, 2, 7) == Q(871, 162), "residual example target")
    require(upper(3, 1, 2, 7) == Q(11, 2), "residual example upper break")
    require(upper(3, 1, 2, 7) - target(3, 1, 2, 7) == Q(10, 81),
            "residual example missing margin")
    require(binomial_nilpotence(3, 2, 7) == 8, "residual example annihilator")
    require(target(3, 1, 2, 8) == Q(440, 81), "optimized old bound")
    require(target(3, 1, 2, 8) - target(3, 1, 2, 7) == Q(1, 18),
            "optimized old bound remains too large")
    require(2**2 * (2 - 1) + 2 * (2 - 1) // 2 == 5 > 2 + 2,
            "rank-two ambient criterion does not settle example")
    for p in (3, 5, 7):
        try:
            parameters(p, 0)
        except ValueError:
            pass
        else:
            raise RuntimeError("undefined r=0 normalization was accepted")
    counts["named_residual_example"] = {
        "p": 3, "e": 1, "n": 2, "r": 7, "a": 2, "b": "7/18",
        "target": "871/162", "upper": "11/2", "upper_loss": "10/81",
        "optimal_scalar_N_for_E_equals_u_minus_p": 8,
        "optimized_old_bound": "440/81", "remaining_scalar_loss": "1/18"
    }
    return {
        "result": "PASS_BOUNDED_EXACT_CONTROLS",
        "scope": "Finite arithmetic and algebra controls; no unrestricted proof or field enumeration.",
        "counts": counts,
        "all_five_approaches_settle_unrestricted_problem": False,
        "no_novelty_claim": True
    }


def verify_integrity(root, expected_manifest_sha256=None):
    root = Path(root)
    require(not root.is_symlink(), "packet root must not be a symlink")
    for node in root.rglob("*"):
        require(not node.is_symlink(), "symlinks are forbidden")
        require(node.is_file(), "packet must be a flat set of regular files")
    raw = (root / "MANIFEST.json").read_bytes()
    if expected_manifest_sha256 is not None:
        require(sha256(raw).hexdigest() == expected_manifest_sha256,
                "external manifest trust anchor mismatch")
    manifest = strict_json(root / "MANIFEST.json")
    require(set(manifest) == {"schema", "problem_id", "disposition", "files"},
            "unexpected manifest fields")
    require(manifest["schema"] == "local-ramification-author-v1", "manifest schema")
    require(manifest["problem_id"] == 30001278, "manifest problem binding")
    require(manifest["disposition"] == "unresolved_partial", "manifest disposition")
    entries = manifest["files"]
    require(isinstance(entries, list), "manifest files must be a list")
    for entry in entries:
        require(isinstance(entry, dict) and set(entry) == {"path", "bytes", "sha256"},
                "manifest file entry schema")
        require(isinstance(entry["path"], str) and entry["path"] in PUBLIC_FILES,
                "unapproved public packet path")
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0, "invalid byte count")
        require(isinstance(entry["sha256"], str) and len(entry["sha256"]) == 64
                and all(c in "0123456789abcdef" for c in entry["sha256"]),
                "invalid SHA-256 fingerprint")
    listed = {entry["path"] for entry in entries}
    require(len(listed) == len(entries), "duplicate manifest paths")
    require(listed == PUBLIC_FILES, "manifest approved-file inventory mismatch")
    actual = {f.name for f in root.iterdir() if f.name != "MANIFEST.json"}
    require(actual == listed, "public packet inventory mismatch")
    for entry in entries:
        path = Path(entry["path"])
        require(not path.is_absolute() and ".." not in path.parts, "invalid manifest path")
        data = (root / path).read_bytes()
        require(len(data) == entry["bytes"], "size mismatch: " + str(path))
        require(sha256(data).hexdigest() == entry["sha256"], "hash mismatch: " + str(path))
    return {"result": "PASS", "files": len(entries)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--math-only", action="store_true",
                        help="print mathematical summary without manifest and retained-result comparison")
    parser.add_argument("--expected-manifest-sha256",
                        help="verify against a separately retained manifest fingerprint")
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    require(not (args.math_only and args.expected_manifest_sha256),
            "math-only mode cannot verify an integrity trust anchor")
    integrity = None if args.math_only else verify_integrity(root, args.expected_manifest_sha256)
    result = mathematical_controls()
    if args.math_only:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        expected = strict_json(root / "CHECK_RESULTS.json")
        require(result == expected, "retained mathematical result differs")
        print(json.dumps({"integrity": integrity, "mathematics": result}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
