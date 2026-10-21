"""Independent exact analytic and boundary controls. Python standard library only.

Complements the supplied orbit/cyclotomic replays. No finite computation proves
Siegel--Walfisz, an infinite progression, or a limiting-distribution assertion.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

C = Counter()

def ck(condition, family):
    if not condition:
        raise AssertionError(family)
    C[family] += 1

B = 10000
prime = bytearray([1]) * (B + 1)
prime[:2] = b"\0\0"
phi = list(range(B + 1))
mu = [1] * (B + 1)
for q in range(2, B + 1):
    if prime[q]:
        for j in range(q, B + 1, q):
            phi[j] = phi[j] // q * (q - 1)
            mu[j] *= -1
        for j in range(q*q, B + 1, q*q):
            mu[j] = 0
        for j in range(q*q, B + 1, q):
            prime[j] = 0
ps = [p for p in range(2, B + 1) if prime[p]]

mean_rows = []
for X in [3, 7, 31, 100, 500, 2500, 10000]:
    pp = [p for p in ps if p <= X]
    # Direct residue tests, independent of divisor incidence in phi(p-1).
    pi1 = [sum(p % d == 1 % d for p in pp) for d in range(1, X)]
    S1 = sum((F(phi[p-1], p-1) for p in pp), F())
    mobius_rearrangement = sum((F(mu[d] * pi1[d-1], d)
                                for d in range(1, X)), F())
    ck(S1 == mobius_rearrangement, "exact_all_prime_mobius_rearrangement")
    S2 = sum((F(phi[(p-1)//2], p-1) for p in pp if p % 2 == 1), F())
    S3 = sum((F(phi[p-1], p-1) for p in pp if p % 4 == 3), F())
    ck(S3 == 2*S2 - S1 + 1, "exact_class_three_from_S1_S2")
    for K in [1, 2, 5, 20, 50]:
        if K >= X:
            continue
        tail = sum((F(abs(mu[d]) * pi1[d-1], d)
                    for d in range(K + 1, X)), F())
        ck(tail <= F(X, K), "absolute_mobius_tail_X_over_K")
    mean_rows.append({"X": X, "prime_count": len(pp),
                      "class_three_count": sum(p % 4 == 3 for p in pp),
                      "all_prime_mean_float_diagnostic_only": float(S1 / len(pp)),
                      "class_three_mean_float_diagnostic_only":
                      float(S3 / sum(p % 4 == 3 for p in pp)),
                      "identities_exact": True})

# Coefficient of Lemma 2 at m=2 is 3A/4. Check each odd n's pair.
for n in range(1, B//2 + 1, 2):
    pair = F(mu[n], 2*n*phi[2*n]) + F(mu[2*n], 4*n*phi[4*n]) if 4*n <= B else None
    if pair is not None:
        ck(pair == F(3, 8)*F(mu[n], n*phi[n]),
           "m2_Euler_coefficient_pair")

def eta(a, p):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p-1)//2, p) == 1 else -1)

def order(a, p):
    if a % p == 0:
        return None
    v = 1
    for k in range(1, p):
        v = v*a % p
        if v == 1:
            return k
    raise AssertionError("missing_order")

boundaries = []
for p in [p for p in ps if p <= 997]:
    ck(sum(eta(u*u+1, p) for u in range(p)) == -1 if p > 2 else True,
       "quadratic_exception_direct_integer_sum")
    if p % 4 != 3:
        if p > 101:
            continue
        roots = [u for u in range(p) if (u*u+1) % p == 0]
        image = {(u, (u*u+1)*v % p) for u in range(p) for v in range(p)}
        ck(len(image) == p*p-len(roots)*(p-1), "inadmissible_image_count")
        ck(len(roots) == (1 if p == 2 else 2), "inadmissible_root_count")
        ck(len(image) < p*p, "inadmissible_negative_control")
        continue
    orders = [order((u*u+1) % p, p) for u in range(p)]
    P = orders.count(p-1)
    ck(P % 2 == 0, "primitive_parameter_sign_pairing")
    f = lambda t: max(F(), min(F(1), 2*t-1))
    continuous_moment = F(p*f(F(1,p))+(p-1)*sum(f(F(d,p)) for d in orders), p*p)
    ck(continuous_moment == (1-F(2,p))*F((p-1)*P,p*p),
       "bounded_continuous_test_exact_primitive_moment")
    for x in [F(1, 2), F(3, 4), F(99, 100), F(p-1, p), F(1)]:
        actual = F(p*int(1 <= p*x)+(p-1)*sum(d <= p*x for d in orders), p*p)
        if x < F(p-1, p):
            ck(actual == 1-F((p-1)*P, p*p), "fixed_threshold_strict_cutoff")
        else:
            ck(actual == 1, "cutoff_equality_includes_primitive_cycles")
    if p in [3, 7, 11, 19, 43, 131, 503]:
        boundaries.append({"p": p, "primitive_parameters": P,
                           "theta": str(F(phi[p-1], p-1)),
                           "D_half": str(1-F((p-1)*P, p*p)),
                           "cutoff_x": str(F(p-1, p)), "D_at_cutoff": "1",
                           "D_three_quarters": str(F(p+(p-1)*sum(4*d <= 3*p for d in orders), p*p))})

ck(F(7, 24) > F(13, 48), "original_extraction_gap")
ck(2*F(3, 4)-1 == F(1, 2), "class_three_mean_constant")
print(json.dumps({"status": "PASS", "assertions": sum(C.values()),
                  "counts": dict(sorted(C.items())),
                  "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                  "mean_identity_rows": mean_rows, "boundary_rows": boundaries,
                  "scope": "Exact finite controls. Infinite results require the written derivation and unconditional theorems."},
                 indent=2, sort_keys=True))
