"""Independent exact finite controls; none substitute for the written proof.

Uses only Python standard library. Inputs are created here, without candidate
code or source text. The infinite probability theorem is in the derivation.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    p = 0
    for j in range(len(a[0])):
        q = next((i for i in range(p, len(a)) if a[i][j]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        x = a[p][j]
        a[p] = [v/x for v in a[p]]
        for i in range(len(a)):
            if i != p and a[i][j]:
                x = a[i][j]
                a[i] = [v-x*w for v, w in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def canonical(v):
    # Quotient modulo diagonal: subtract first coordinate.
    return tuple(x-v[0] for x in v[1:])


def solve(cols, target):
    n = len(cols)
    assert all(len(c) == n for c in cols)
    a = [[Fraction(cols[j][i]) for j in range(n)] + [Fraction(target[i])]
         for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if a[i][j])
        a[j], a[p] = a[p], a[j]
        q = a[j][j]
        a[j] = [v/q for v in a[j]]
        for i in range(n):
            if i != j:
                q = a[i][j]
                a[i] = [v-q*w for v, w in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def cube_controls():
    checked = 0
    max_classes = {}
    for k in range(2, 5):
        cube = list(product((0, 1), repeat=k))
        one = (1,)*k
        for j in range(0, min(k-1, 3)+1):
            # Test all cube-generated spaces at the stated dimensions.
            seen = set()
            for basis in combinations(cube, j):
                base = (one,)+basis
                if rank(base) != j+1:
                    continue
                vertices = tuple(v for v in cube if rank(base+(v,)) == j+1)
                if vertices in seen:
                    continue
                seen.add(vertices)
                classes = {canonical(v) for v in vertices}
                assert len(vertices) <= 2**(j+1)
                assert len(classes) == len(vertices)-1
                assert len(classes) <= 2**(j+1)-1
                checked += 1
                max_classes[str((k, j))] = max(max_classes.get(str((k, j)), 0), len(classes))
    return {"spaces_checked": checked, "max_classes": max_classes}


def fibers(s):
    out = defaultdict(list)
    for mask in range(1 << len(s)):
        row = tuple((mask >> i) & 1 for i in range(len(s)))
        out[sum(a*b for a, b in zip(s, row))].append(row)
    return out.values()


def family_controls():
    tested = row_restrictions = roots = same_band = degenerate = 0
    # All finite selected sets up to 8; 1 is also tested deterministically.
    ground = tuple(range(1, 9))
    for mask in range(1 << len(ground)):
        s = tuple(a for i, a in enumerate(ground) if (mask >> i) & 1)
        for family in fibers(s):
            k = len(family)
            one = (1,)*k
            cols = [tuple(row[j] for row in family) for j in range(len(s))]
            R = rank([one]+cols)-1
            assert k <= 2**R
            tested += 1
            if R == 0:
                degenerate += 1
            for r in range(1, R+1):
                base = [one]
                for c in cols:
                    if rank(base+[c]) > len(base):
                        base.append(c)
                        if len(base) == r+1:
                            break
                ids = next(ids for ids in combinations(range(k), r+1)
                           if rank([tuple(c[i] for i in ids) for c in base]) == r+1)
                restricted = [family[i] for i in ids]
                assert len(set(restricted)) == r+1
                qcols = [canonical(tuple(row[j] for row in restricted))
                         for j in range(len(s))]
                assert rank(qcols) == r
                row_restrictions += 1
                # Greedy largest independent pivots in the restricted family.
                piv, pcols = [], []
                for j in reversed(range(len(s))):
                    if rank(pcols+[qcols[j]]) > len(pcols):
                        piv.append(j)
                        pcols.append(qcols[j])
                assert len(piv) == r
                assert all(s[piv[j]] > s[piv[j+1]] for j in range(r-1))
                for j in range(r):
                    for a_index, a in enumerate(s):
                        if a > s[piv[j]] and a_index not in piv:
                            assert rank(pcols[:j]+[qcols[a_index]]) == j
                target = [-sum(a*c[h] for j, (a, c) in enumerate(zip(s, qcols)) if j not in piv)
                          for h in range(r)]
                recovered = solve(pcols, target)
                assert recovered == tuple(Fraction(s[j]) for j in piv)
                roots += 1
                # Explicit integer-log bands and enlarged-interval assignment.
                z = [math.floor(math.log(s[j])) for j in piv]
                if len(set(z)) < len(z):
                    same_band += 1
                for j, a in enumerate(s):
                    if j in piv:
                        continue
                    allowed = sum(math.log(a) < zz+1 for zz in z)
                    assert rank(pcols[:allowed]+[qcols[j]]) == allowed
    return {"families_checked": tested, "row_restrictions_checked": row_restrictions,
            "pivot_root_checks": roots, "same_log_band_cases": same_band,
            "zero_rank_families": degenerate}


def odds_controls():
    ground = tuple(range(2, 9))
    probs = {}
    for mask in range(1 << len(ground)):
        s = frozenset(a for i, a in enumerate(ground) if (mask >> i) & 1)
        p = Fraction(1)
        for a in ground:
            p *= Fraction(1, a) if a in s else Fraction(a-1, a)
        probs[s] = p
    checks = 0
    for s, p in probs.items():
        for size in range(len(s)+1):
            for piv in combinations(sorted(s), size):
                b = s.difference(piv)
                odds = Fraction(1)
                for x in piv:
                    odds *= Fraction(1, x-1)
                assert p == probs[b]*odds
                assert odds <= Fraction(2**size, math.prod(piv))
                checks += 1
    assert sum(probs.values()) == 1
    return {"deletion_identities_checked": checks, "ground_starts_at_2": True,
            "deterministic_1_excluded_from_odds": True}


def analytic_controls():
    eps = 1/20
    diffs = [(1+eps)*math.log((2**(j+1)-1)/(2**j-1))-1 for j in range(2, 20)]
    assert max(diffs) < 0
    assert (1+eps)*math.log(3)-1 > 0
    assert (1+eps)*math.log(7/3) < 1
    telescopes = 0
    for r in range(1, 7):
        qs = [2**(j+1)-1 for j in range(1, r+1)]
        for z in product(range(4), repeat=r):
            if any(z[j] < z[j+1] for j in range(r-1)):
                continue
            u = Fraction(1, 2)
            a = sum((z[j]-z[j+1])*math.log(qs[j]) for j in range(r-1))
            a += (z[-1]+1-float(u))*math.log(qs[-1])
            lhs = (1+eps)*a-sum(z)
            rhs = ((1+eps)*math.log(3)-1)*z[0]
            rhs += sum(((1+eps)*math.log(qs[j]/qs[j-1])-1)*z[j] for j in range(1, r))
            rhs += (1+eps)*(1-float(u))*math.log(qs[-1])
            assert abs(lhs-rhs) < 1e-12
            telescopes += 1
    # Subset union convolution bound, full arbitrary finite ground sets.
    convchecks = 0
    for mask in range(1 << 8):
        s = tuple(a+1 for a in range(8) if (mask >> a) & 1)
        for split in range(9):
            lo = tuple(a for a in s if a < split)
            hi = tuple(a for a in s if a >= split)
            whole = max(map(len, fibers(s)))
            high = max(map(len, fibers(hi)))
            assert whole <= (2**len(lo))*high
            convchecks += 1
    return {"telescoping_cases": telescopes, "later_coefficients_strictly_negative": True,
            "largest_later_coefficient": max(diffs), "convolution_cases": convchecks,
            "candidate_constant": (math.log(3)-1)*math.log(2)**2}


def main():
    result = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "runtime": sys.version,
        "scope": "Independent finite controls of a written universal proof; no candidate imports",
        "cube": cube_controls(),
        "family": family_controls(),
        "odds": odds_controls(),
        "analytic": analytic_controls(),
        "all_checks_passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
