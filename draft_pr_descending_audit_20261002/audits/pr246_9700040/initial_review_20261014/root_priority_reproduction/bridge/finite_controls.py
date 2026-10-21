"""Exact finite falsification controls; Python standard library only.

These checks support, but do not replace, the proofs in INDEPENDENT_REPORT.md.
They compare insertion, integer counting, recursive Young-lattice path counts,
factorial determinants, and exact rational weights through distinct operations.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from math import factorial
from pathlib import Path
import json


def insert(tableau, x):
    rows = [list(row) for row in tableau]
    for row in rows:
        for j, y in enumerate(row):
            if y > x:
                row[j], x = x, y
                break
        else:
            row.append(x)
            return tuple(map(tuple, rows))
    rows.append([x])
    return tuple(map(tuple, rows))


def insertion(word):
    t = ()
    for x in word:
        t = insert(t, x)
    return t


def restriction(t, q):
    return tuple(tuple(x for x in row if x <= q) for row in t if row[0] <= q)


def shape(t):
    return tuple(map(len, t))


@lru_cache(None)
def partitions(n, largest=None):
    if n == 0:
        return ((),)
    largest = n if largest is None else min(n, largest)
    return tuple((i,) + tail for i in range(largest, 0, -1)
                 for tail in partitions(n-i, i))


def contained(mu, nu):
    return len(mu) <= len(nu) and all(a <= b for a, b in zip(mu, nu))


def predecessors(nu):
    for i, x in enumerate(nu):
        if i+1 == len(nu) or x > nu[i+1]:
            m = list(nu)
            m[i] -= 1
            yield tuple(x for x in m if x)


@lru_cache(None)
def skew_paths(mu, nu):
    if not contained(mu, nu):
        return 0
    if mu == nu:
        return 1
    return sum(skew_paths(mu, p) for p in predecessors(nu))


def determinant(a):
    a = [list(row) for row in a]
    answer = F(1)
    for j in range(len(a)):
        k = next((i for i in range(j, len(a)) if a[i][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[j], a[k] = a[k], a[j]
            answer = -answer
        pivot = a[j][j]
        answer *= pivot
        for i in range(j+1, len(a)):
            factor = a[i][j] / pivot
            for k in range(j+1, len(a)):
                a[i][k] -= factor * a[j][k]
    return answer


def D(t, nu, mu=()):
    if not contained(mu, nu):
        return F(0)
    ell = max(len(nu), len(mu))
    nu = nu + (0,)*(ell-len(nu))
    mu = mu + (0,)*(ell-len(mu))
    def h(r):
        return t**r / factorial(r) if r >= 0 else F(0)
    return determinant([[h(nu[i]-mu[j]-i+j) for j in range(ell)]
                        for i in range(ell)])


def check_small_label_restriction():
    count = checks = 0
    witness = None
    for n in range(9):
        for word in permutations(range(1, n+1)):
            count += 1
            t = insertion(word)
            for q in range(n+1):
                smaller = insertion([x for x in word if x <= q])
                assert restriction(t, q) == smaller, (word, q)
                checks += 1
                if witness is None and shape(smaller) != shape(insertion(word[:q])):
                    witness = dict(word=word, q=q, smallest_values_shape=shape(smaller),
                                   first_positions_shape=shape(insertion(word[:q])))
    assert witness is not None  # A false P/Q shortcut must actually be detected.
    return dict(permutations=count, restriction_equalities=checks,
                false_prefix_shortcut_witness=witness)


def check_chain_counting():
    # All two-cut shape chains, with zero-size blocks allowed, up to total n=7.
    chains_checked = permutations_checked = 0
    for n in range(8):
        cuts = [(a,b) for a in range(n+1) for b in range(a,n+1)]
        counts = {cut: Counter() for cut in cuts}
        for word in permutations(range(1,n+1)):
            permutations_checked += 1
            t = ()
            shapes = [()]
            for x in word:
                t = insert(t,x)
                shapes.append(shape(t))
            for a,b in cuts:
                counts[a,b][(shapes[a],shapes[b],shapes[n])] += 1
        for (a,b), frequencies in counts.items():
            assert sum(frequencies.values()) == factorial(n)
            for (lam1,lam2,lam3), observed in frequencies.items():
                expected = (skew_paths((),lam3)*skew_paths((),lam1)
                            *skew_paths(lam1,lam2)*skew_paths(lam2,lam3))
                assert observed == expected, (n,a,b,lam1,lam2,lam3,observed,expected)
                chains_checked += 1
    return dict(permutations=permutations_checked, chain_frequencies=chains_checked)


def check_determinants():
    checked = 0
    allshapes = [p for n in range(11) for p in partitions(n)]
    for nu in allshapes:
        for mu in allshapes:
            if not contained(mu,nu):
                continue
            d = sum(nu)-sum(mu)
            for t in (F(0),F(1),F(2,3)):
                expected = t**d * F(skew_paths(mu,nu), factorial(d))
                assert D(t,nu,mu) == expected, (t,nu,mu)
                checked += 1
    return dict(contained_shape_time_pairs=checked, maximum_terminal_size=10)


def check_weights():
    # x=(1,2,4), theta=2. Use raw weights (remove common e^-4).
    deltas = (F(1),F(1),F(2))
    allshapes = [p for n in range(9) for p in partitions(n)]
    raw = [F(0) for _ in range(9)]
    bounds = [(1,2,4),(3,2,4),(3,1,2),(1,1,1)]
    constrained = {b:F(0) for b in bounds}
    total = 0
    for nu in allshapes:
        n = sum(nu)
        for mid in allshapes:
            if not contained(mid,nu):
                continue
            for first in allshapes:
                if not contained(first,mid):
                    continue
                shapes = ((),first,mid,nu)
                candidate = D(F(1),nu)
                nica = D(F(2),nu)
                bo = F(1)
                for j,dt in enumerate(deltas):
                    mu,lam = shapes[j],shapes[j+1]
                    a,b = sum(mu),sum(lam)
                    d = b-a
                    candidate *= D(dt,lam,mu)
                    nica *= D(dt/2,lam,mu)
                    # Poisson d! times telescoped up-path probability.
                    bo *= (dt**d/F(factorial(d)) * skew_paths(mu,lam)
                           * F(skew_paths((),lam),skew_paths((),mu))
                           * F(factorial(a),factorial(b)))
                assert candidate == nica == bo
                raw[n] += candidate
                for r in bounds:
                    if all((s[0] if s else 0) <= k-1 for s,k in zip(shapes[1:],r)):
                        constrained[r] += candidate
                total += 1
    for n,w in enumerate(raw):
        assert w == F(4**n,factorial(n)),(n,w)
    # Missing the independent birth Poisson d! is detected at d=2.
    correct = D(F(1),(2,))**2
    wrong = F(1,2)
    assert correct == F(1,4) and wrong != correct
    return dict(chains=total, maximum_terminal_size=8,
                exact_unconstrained_raw_mass=[str(x) for x in raw],
                constrained_raw_sums={str(k):str(v) for k,v in constrained.items()},
                missing_poisson_factorial_control=dict(correct=str(correct),wrong=str(wrong)))


if __name__ == '__main__':
    result = dict(started_utc=datetime.now(timezone.utc).isoformat(),
                  restriction=check_small_label_restriction(),
                  chains=check_chain_counting(),
                  determinants=check_determinants(),
                  weights=check_weights())
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    result['status'] = 'all exact assertions passed'
    target = Path(__file__).with_name('FINITE_CONTROL_RESULTS.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
