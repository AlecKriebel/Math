#!/usr/bin/env python3
"""Nonauthor exact audit in Q(zeta_12,zeta_5), not author's Phi_60 basis.

No third-party dependencies. Does not modify the candidate or author certificate.
"""
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import time

PAIRS = ((3, 2), (20, 14), (119, 84))
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "tubular"


def psign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def polynomial_product(a, b):
    ans = defaultdict(int)
    for ea, ca in a.items():
        for eb, cb in b.items():
            ans[tuple(x+y for x, y in zip(ea, eb))] += ca*cb
    return dict(ans)


def derive_determinant():
    zero = (0, 0, 0)
    rows = []
    for i, (p, q) in enumerate(PAIRS):
        exponent = tuple(int(j == i) for j in range(3))
        rows.append(({zero: p}, {exponent: -q}, {zero: 1, exponent: -1}))
    ans = defaultdict(int)
    for perm in permutations(range(3)):
        term = {zero: psign(perm)}
        for i, j in enumerate(perm):
            term = polynomial_product(term, rows[i][j])
        for e, c in term.items():
            ans[e] += c
    ans = {e: c for e, c in ans.items() if c}
    assert all(c % 2 == 0 for c in ans.values())
    return {e: c//2 for e, c in ans.items()}


def powers_mod_monic(order, coefficients):
    """powers of X in Z[X]/(X^degree + sum coefficients[j] X^j)."""
    degree = len(coefficients)
    ans = []
    v = [1] + [0]*(degree-1)
    for _ in range(order):
        ans.append(tuple(v))
        high = v[-1]
        v = [0] + v[:-1]
        v = [x-high*c for x, c in zip(v, coefficients)]
    assert v == [1] + [0]*(degree-1)
    return ans


def independent_roots60():
    # u = exp(2pi i/12), v = exp(2pi i/5), w = u*v.
    # w has exponent 17 relative to standard zeta_60, hence is primitive.
    # Coprime conductors 12 and 5 give [Q(u,v):Q] = 4*4 = 16.
    us = powers_mod_monic(12, [1, 0, -1, 0])  # Phi_12 = X^4-X^2+1.
    vs = powers_mod_monic(5, [1, 1, 1, 1])  # Phi_5 = X^4+X^3+X^2+X+1.
    rs = [tuple(a*b for a in us[k % 12] for b in vs[k % 5]) for k in range(60)]
    assert len(set(rs)) == 60
    return rs


def enumerate_roots(polynomial):
    rs = independent_roots60()
    zeros = []
    # Every monomial in determinant has exponent coefficients 0 or 1.
    terms = tuple(polynomial.items())
    for exponents in product(range(60), repeat=3):
        vec = [0]*16
        for powers, coefficient in terms:
            index = sum(a*b for a, b in zip(powers, exponents)) % 60
            root = rs[index]
            for j, value in enumerate(root):
                vec[j] += coefficient*value
        if not any(vec):
            zeros.append(list(exponents))
    return zeros


def subset_partitions(s):
    """All set partitions; used only for the six coefficient indices."""
    if not s:
        yield []
        return
    first, *rest = s
    for partition in subset_partitions(rest):
        yield [[first]] + partition
        for i in range(len(partition)):
            yield partition[:i] + [[first]+partition[i]] + partition[i+1:]


def small_relation_checks(coefficients):
    r6 = powers_mod_monic(6, [1, -1])  # Phi_6 = X^2-X+1.
    pairs = []
    triples = []
    for indices in combinations(range(6), 2):
        if abs(coefficients[indices[0]]) == abs(coefficients[indices[1]]):
            pairs.append(list(indices))
    # Normalize first root to 1, enumerate all relative sixth-root phases.
    for indices in combinations(range(6), 3):
        for phases in product(range(6), repeat=2):
            terms = zip(indices, (0,)+phases)
            result = [0, 0]
            for index, exponent in terms:
                for j in range(2):
                    result[j] += coefficients[index]*r6[exponent][j]
            if result == [0, 0]:
                triples.append({"indices": list(indices), "phases": [0]+list(phases)})
    # Superset of possible minimal partitions: no singletons or 3-blocks,
    # and 2-blocks must come from the independently checked equal pair.
    admitted = []
    total = 0
    pairset = {tuple(x) for x in pairs}
    for partition in subset_partitions(list(range(6))):
        total += 1
        if any(len(b) in (1, 3) for b in partition):
            continue
        if any(len(b) == 2 and tuple(sorted(b)) not in pairset for b in partition):
            continue
        admitted.append(sorted([sorted(b) for b in partition], key=lambda x: (len(x), x)))
    assert total == 203
    return {"all_set_partitions_checked": total, "equal_magnitude_pairs": pairs,
            "three_term_relation_phases_mu6": triples, "possible_minimal_partitions": admitted}


def main():
    started = time.monotonic()
    p = derive_determinant()
    expected = {(1,0,0):-99, (0,1,0):812, (0,0,1):-714,
                (1,1,0):-714, (1,0,1):820, (0,1,1):-105}
    assert p == expected, p
    coeffs = tuple(p[e] for e in ((1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)))
    small = small_relation_checks(coeffs)
    assert small["equal_magnitude_pairs"] == [[2, 3]]
    assert small["three_term_relation_phases_mu6"] == []
    assert len(small["possible_minimal_partitions"]) == 2
    zeros = enumerate_roots(p)
    assert zeros == [[0, 0, 0]], zeros
    hashes = {name: hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()
              for name in ("ABELIAN_HOLONOMY_DELTA.md", "PELL_CANDIDATE.md",
                           "check_abelian_holonomy.py", "abelian_holonomy_certificate.json")}
    result = {"utc": datetime.now(timezone.utc).isoformat(), "result":"PASS_EXACT_CHECKS",
              "author_file_sha256": hashes,
              "determinant_divided_by_two": [{"powers":list(e), "coefficient":p[e]} for e in sorted(p)],
              "independent_basis":"u^i v^j, 0<=i,j<4; Phi12(u)=0, Phi5(v)=0; primitive 60th root w=u*v",
              "root_triples_checked":60**3, "zero_exponents":zeros,
              "minimal_partition_finite_checks":small,
              "seconds":time.monotonic()-started,
              "scope":"Exact determinant, finite relation arithmetic and mu60 enumeration. Arbitrary-order completeness and affine-representation scope are separately audited in AUDIT.md."}
    (HERE/"independent_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
