#!/usr/bin/env python3
"""Independent integer/multiplication and Laplace-minor audit, Python stdlib only.

Does not import or execute the author's checker, and does not modify its files.
General claims require the proofs in AUDIT.md, not extrapolation from this run.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import gcd, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "root_controls"


def mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def power_relator_matrix(n, degree):
    # Build J from the effect of each fiber generator, then use binary powering.
    j = tuple(tuple(int(i == k) + int(i == k - 1) for k in range(n))
              for i in range(n))
    result = tuple(tuple(int(i == k) for k in range(n)) for i in range(n))
    while degree:
        if degree & 1:
            result = mul(result, j)
        j = mul(j, j)
        degree >>= 1
    return tuple(tuple(result[i][k] - int(i == k) for k in range(n))
                 for i in range(n))


@lru_cache(maxsize=200000)
def laplace(a):
    if not a:
        return 1
    if len(a) == 1:
        return a[0][0]
    # Expand a sparsest row; exact signed integer arithmetic, not Bareiss.
    i = min(range(len(a)), key=lambda r: sum(x != 0 for x in a[r]))
    result = 0
    for j, x in enumerate(a[i]):
        if x:
            small = tuple(tuple(y for k, y in enumerate(row) if k != j)
                          for r, row in enumerate(a) if r != i)
            result += (-1 if (i + j) & 1 else 1) * x * laplace(small)
    return result


def all_determinantal_divisors(a):
    n = len(a)
    divisors = [1]
    for k in range(1, n + 1):
        values = []
        for rr in combinations(range(n), k):
            for cc in combinations(range(n), k):
                values.append(abs(laplace(tuple(tuple(a[i][j] for j in cc)
                                                for i in rr))))
        divisor = 0
        for value in values:
            divisor = gcd(divisor, value)
        divisors.append(divisor)
    return divisors


def nullity_over_prime(a, p):
    # Construct a pivot basis of columns; distinct from the author's row RREF.
    basis = {}
    for column in zip(*a):
        v = [x % p for x in column]
        for k, base in sorted(basis.items()):
            coefficient = v[k]
            v = [(x - coefficient * y) % p for x, y in zip(v, base)]
        pivot = next((k for k, x in enumerate(v) if x), None)
        if pivot is not None:
            inverse = pow(v[pivot], p - 2, p)
            basis[pivot] = [(x * inverse) % p for x in v]
    return len(a) - len(basis)


def main():
    cert = json.loads((AUTHOR / "height_cover_certificate.json").read_text())
    smith_cases = []
    for case in cert["integral_cases"]:
        n, d = case["rank"], case["height_index"]
        a = power_relator_matrix(n, d)
        delta = all_determinantal_divisors(a)
        assert delta[-1] == 0 and delta[-2] == d ** (n - 1)
        smith = [delta[k] // delta[k - 1] for k in range(1, n)]
        assert smith == case["nonzero_smith"]
        assert prod(smith) == case["torsion_order"] == d ** (n - 1)
        assert case["rational_betti"] == 2
        smith_cases.append({"m": n, "d": d, "smith": smith})
    modular_cases = 0
    for n in range(1, 25):
        for d in range(1, 31):
            a = power_relator_matrix(n, d)
            for p in (2, 3, 5, 7, 11, 13):
                q, residual = 1, d
                while residual % p == 0:
                    q *= p
                    residual //= p
                actual = 1 + nullity_over_prime(a, p)
                assert actual == 1 + min(n, q)
                modular_cases += 1
    for case in cert["prime_power_cases"]:
        n, p, q = case["rank"], case["prime"], case["height_index"]
        assert q >= n
        assert 1 + nullity_over_prime(power_relator_matrix(n, q), p) == n + 1
        assert case["mod_p_betti"] == case["minimum_generator_number"] == n + 1
    for p in (2, 3, 5, 7):
        for n in range(1, p + 1):
            delta = all_determinantal_divisors(power_relator_matrix(n, p))
            assert [delta[k] // delta[k - 1] for k in range(1, n)] == [p] * (n - 1)
    delta = all_determinantal_divisors(power_relator_matrix(3, 2))
    assert delta == [1, 1, 4, 0]
    assert 1 + nullity_over_prime(power_relator_matrix(3, 2), 2) == 3
    filenames = ("CYCLIC_HEIGHT_COVERS.md", "check_height_covers.py",
                 "height_cover_certificate.json", "SOURCE_MANIFEST.json")
    result = {
        "status": "PASS finite exact checks; infinite proof audited separately",
        "independence": "Binary matrix multiplication, sparsest-row Laplace determinants, column pivot basis; author checker not imported or executed",
        "smith_cases": smith_cases,
        "author_prime_power_cases_checked": len(cert["prime_power_cases"]),
        "general_modular_cases_checked": modular_cases,
        "general_modular_formula": "b1(H_(m,d);Fp) = 1 + min(m, p^v_p(d))",
        "boundary_m3_d2": {"smith": [1, 4], "mod2_betti": 3},
        "input_sha256": {f: sha256((AUTHOR / f).read_bytes()).hexdigest()
                         for f in filenames},
    }
    (HERE / "independent_height_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS: {len(smith_cases)} Smith cases, {len(cert['prime_power_cases'])} author prime-power cases, {modular_cases} general modular cases.")


if __name__ == "__main__":
    main()
