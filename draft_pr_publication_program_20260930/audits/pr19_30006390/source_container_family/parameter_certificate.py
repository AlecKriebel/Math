"""First-party exact checks for the direct source-theorem substitutions.

No conjectural estimate is tested or claimed. No external dependencies are used.
Run from any directory; the JSON certificate is written beside this script.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def prime_plane(q):
    # Canonical homogeneous representatives, independent of candidate code.
    points = []
    for v in product(range(q), repeat=3):
        if not any(v):
            continue
        first = next(a for a in v if a)
        inverse = pow(first, -1, q)
        canonical = tuple(a * inverse % q for a in v)
        if canonical == v:
            points.append(v)
    lines = [
        frozenset(i for i, v in enumerate(points) if sum(a*b for a, b in zip(v, w)) % q == 0)
        for w in points
    ]
    return points, lines


def exact_plane_certificate(q):
    points, lines = prime_plane(q)
    n, s = q*q+q+1, q+1
    assert len(points) == len(lines) == n
    assert all(len(line) == s for line in lines)
    assert all(len(left & right) == 1 for left, right in combinations(lines, 2))
    degrees = Counter(v for line in lines for v in line)
    assert all(degrees[v] == s for v in range(n))
    norms = {}
    for t in range(1, s+1):
        td = Counter(T for line in lines for T in combinations(sorted(line), t))
        norm_squared = sum((Fraction(d, comb(s, t)*n)**2 for d in td.values()), Fraction())
        expected = Fraction(1, n) if t == 1 else Fraction(1, n*comb(s, t))
        assert norm_squared == expected
        assert sum((Fraction(d, comb(s, t)*n) for d in td.values()), Fraction()) == 1
        norms[str(t)] = str(norm_squared)
    first_term = Fraction(300*s**4, n)
    assert first_term > Fraction(1, 500)
    marginal = Fraction(1, 2**s)
    joint = Fraction(1, 2**len(lines[0] | lines[1]))
    assert joint == Fraction(1, 2**(2*q+1)) == 2*marginal*marginal
    # Ordinary blockers' complements are exactly complete-line independent sets.
    # Exhaustively inspect all point sets for q=2,3 only.
    equivalence_checks = 0
    if q <= 3:
        whole = set(range(n))
        for mask in range(2**n):
            blocker = {v for v in range(n) if mask & (1 << v)}
            independent_complement = all(not line <= whole-blocker for line in lines)
            assert all(line & blocker for line in lines) == independent_complement
            equivalence_checks += 1
    return {
        "q": q, "n": n, "s": s, "degree_measure_norm_squared": norms,
        "technical_t1_term": str(first_term),
        "joint_empty_probability": str(joint),
        "product_empty_marginals": str(marginal*marginal),
        "blocking_complement_checks": equivalence_checks,
    }


def main():
    # Ascending coefficients in 150000(q+1)^4-(q^2+q+1).
    polynomial_coefficients = [149999, 599999, 899999, 600000, 150000]
    assert all(c > 0 for c in polynomial_coefficients)
    for q in [1, 2, 3, 4, 5, 7, 9, 16, 31, 101, 10**6]:
        s, n = q+1, q*q+q+1
        assert s*s-n == q > 0
        assert n < s*s <= 10**9*s**7
        assert sum(c*q**i for i, c in enumerate(polynomial_coefficients)) == 150000*s**4-n > 0
    out = {
        "scope": "Source theorem parameter audit; not an asymptotic conjecture certificate",
        "universal_packaged_obstruction": "For q>=1, alpha,beta,eta in (0,1): alpha*beta*eta*n<n<s^2<10^9*s^7",
        "universal_technical_obstruction": "Regularity gives norm1^2=1/n; the theorem requires 300*s^4/n<=1/(delta*n)<=p/500<1/500, hence n>150000*s^4",
        "technical_positive_polynomial_ascending_coefficients": polynomial_coefficients,
        "normalization": "sigma_t(T)=degree(T)/(binom(s,t)*edge_count); unweighted counting-measure Euclidean norm",
        "direct_scope_only": True,
        "finite_planes": [exact_plane_certificate(q) for q in (2, 3, 5, 7)],
        "status": "PASS",
    }
    dest = Path(__file__).with_name("parameter_certificate.json")
    dest.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status": out["status"], "finite_planes": len(out["finite_planes"]),
                      "blocking_complement_checks": sum(x["blocking_complement_checks"] for x in out["finite_planes"]),
                      "output": str(dest)}))


if __name__ == "__main__":
    main()
