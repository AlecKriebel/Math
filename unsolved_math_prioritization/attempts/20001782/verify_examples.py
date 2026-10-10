"""Small exact regression checks; these do not prove the general conjecture.

Run with Python 3.10+: python verify_examples.py
Only the standard library is used. Mathematical proofs are in ATTEMPT_*.md.
"""
from fractions import Fraction as F
from itertools import product, permutations
from math import factorial
import json


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(r + 1, len(a)):
            p = a[i][c]
            a[i] = [x - p * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def squared(v):
    return sum(x * x for x in v)


rectangular = []
for d in range(2, 6):
    for k in range(1, d):
        for L in (3, 5, 11):
            lengths = (1,) * k + (L,) * (d - k)
            # a=4, r=1/2, hence the short radius is exactly 2.
            points = [tuple(n * ell for n, ell in zip(v, lengths))
                      for v in product(range(-2, 3), repeat=d)]
            short = [v for v in points if squared(v) <= 4]
            assert rank(short) == k
            # Enumerate coordinate permutations preserving the two metric blocks.
            nperm = sum(all(lengths[i] == lengths[p[i]] for i in range(d))
                        for p in permutations(range(d)))
            assert nperm == factorial(k) * factorial(d - k)
            group_order = (2 ** d) * nperm
            four_R_squared = k + (d - k) * L * L
            assert L * L <= four_R_squared
            rectangular.append(dict(d=d, k=k, L=L, rank=k,
                                    group_order=group_order,
                                    four_R_squared=four_R_squared))


ladders = []
for d in range(2, 6):
    for L in (4, 6, 9):
        points = set()
        for z in product(range(-2, 3), repeat=d):
            for s in (0, 1):
                points.add((z[0], L * z[1] + s,
                            *(L * z[i] for i in range(2, d))))
        zero = (0,) * d
        one = (0, 1, *((0,) * (d - 2)))
        at_zero = {}
        at_one = {}
        for rho in (1, 2):
            at_zero[rho] = {v for v in points if squared(v) <= rho * rho}
            at_one[rho] = {tuple(v[i] - one[i] for i in range(d))
                          for v in points
                          if squared(tuple(v[i] - one[i] for i in range(d)))
                          <= rho * rho}
            reflected = {(v[0], -v[1], *v[2:]) for v in at_zero[rho]}
            assert reflected == at_one[rho]
            assert rank(at_zero[rho]) == 2
        expected = {zero, one, (1, *((0,) * (d - 1))),
                    (-1, *((0,) * (d - 1)))}
        assert at_zero[1] == expected
        # Exact forbidden-edge margins to the next pair and transverse rows.
        assert L - 1 > 2 and L > 2
        ladders.append(dict(d=d, L=L, rank_at_1=2, rank_at_2=2,
                            cluster_size_at_2=len(at_zero[2]),
                            four_R_squared=1+(L-1)**2+(d-2)*L**2))


def sign_a_plus_b_sqrt2(a, b):
    """Exact sign for a+b sqrt(2), with rational inputs."""
    a, b = F(a), F(b)
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    compare = (a*a > 2*b*b) - (a*a < 2*b*b)
    return compare if a > 0 else -compare


# alpha=sqrt(2)-1; prove the exact inequalities used in Attempt 5.
assert sign_a_plus_b_sqrt2(-1, 1) > 0
assert sign_a_plus_b_sqrt2(F(3, 2), -1) > 0
irrational_examples = []
for d in range(2, 13):
    # (2R)^2=d+5-4sqrt(2), alpha^2=3-2sqrt(2).
    assert sign_a_plus_b_sqrt2(d+4, -4) > 0  # 2R>1
    assert sign_a_plus_b_sqrt2(d+2, -2) > 0  # 2R>alpha
    irrational_examples.append(dict(d=d, module_rank=d+1,
                                     four_R_squared=[d+5, -4]))


I = (1, 0, 0, 1)


def mul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


mod3_controls = []
for expected_order, A in ((2, (-1, 0, 0, 1)),
                          (3, (0, -1, 1, -1)),
                          (4, (0, -1, 1, 0)),
                          (6, (0, -1, 1, 1))):
    for n in range(-12, 13):
        U, Uinv = (1, n, 0, 1), (1, -n, 0, 1)
        B = mul(mul(U, A), Uinv)
        powers, P = [], I
        for _ in range(expected_order):
            powers.append(P)
            P = mul(P, B)
        assert P == I and len(set(powers)) == expected_order
        assert len({tuple(a % 3 for a in P) for P in powers}) == expected_order
        mod3_controls.append(dict(order=expected_order, shear=n))


real_bounds = []
for d in range(1, 13):
    for m in range(1, 41):
        Fdm = max(2**(d-2*s)*m**s for s in range(d//2+1))
        expected = (2**(d % 2)*m**(d//2) if m >= 4 else 2**d)
        assert Fdm == expected
        real_bounds.append((d, m))


result = {
    "scope": "Finite exact controls of displayed examples and formulas; not a proof of the open target.",
    "rectangular_examples": rectangular,
    "ladder_examples": ladders,
    "irrational_examples": irrational_examples,
    "mod3_conjugated_cyclic_controls": len(mod3_controls),
    "real_character_formula_controls": len(real_bounds),
    "all_checks_passed": True,
}
print(json.dumps(result, indent=2))
