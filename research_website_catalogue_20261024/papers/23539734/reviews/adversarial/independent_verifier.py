#!/usr/bin/env python3
"""Read-only adversarial finite controls. Imports no submission or review helper.

Uses discrete-log enumeration, integer circular autocorrelations, full functional
graphs with tails, and exact mixed exceptional assignments. No writes; stdout
only. Finite controls cannot prove the cited infinite-prime inputs.
"""
from collections import Counter
from fractions import Fraction as Q
from math import gcd, isqrt
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

COUNTS = Counter()


def check(value, family):
    if not value:
        raise RuntimeError(family)
    COUNTS[family] += 1


@lru_cache(None)
def primes(n):
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, isqrt(p) + 1))]


@lru_cache(None)
def distinct_factors(n):
    return [q for q in primes(n) if n % q == 0]


@lru_cache(None)
def phi(n):
    return sum(gcd(n, k) == 1 for k in range(n))


@lru_cache(None)
def mobius(n):
    factors = distinct_factors(n)
    return 0 if any(n % (q*q) == 0 for q in factors) else (-1)**len(factors)


def h(t):
    return min(Q(1), max(Q(0), 2*t - 1))


def logs(p):
    for g in range(2, p):
        sequence = []
        a = 1
        while a not in sequence:
            sequence.append(a)
            a = a*g % p
        if len(sequence) == p - 1:
            check(a == 1 and set(sequence) == set(range(1, p)),
                  'complete_cyclic_enumeration')
            return {a: k for k, a in enumerate(sequence)}
    raise RuntimeError('no generator')


def graph(p):
    successor = [u*p + ((u*u + 1)*v % p)
                 for u in range(p) for v in range(p)]
    periods = [0]*(p*p)
    visited = set()
    for start in range(p*p):
        if start in visited:
            continue
        path = []
        position = {}
        z = start
        while z not in visited and z not in position:
            position[z] = len(path)
            path.append(z)
            z = successor[z]
        if z in position:
            cycle = path[position[z]:]
            for z in cycle:
                periods[z] = len(cycle)
        visited.update(path)
    check(len(visited) == p*p, 'all_graph_points_visited')
    return successor, periods


rows = []
graph_points = 0
ps = primes(1009)[1:]
for p in ps:
    n = p - 1
    log = logs(p)
    aa = [(u*u + 1) % p for u in range(p)]
    r = aa.count(0)
    check(r == (2 if p % 4 == 1 else 0), 'exceptional_root_count')
    orders = [None if a == 0 else n//gcd(n, log[a]) for a in aa]
    P = orders.count(n)
    ph = phi(n)
    theta = Q(ph, n)
    W = 2**len(distinct_factors(n))
    check((P*n - (p-r)*ph)**2 <= ph*ph*(W-1)**2*p,
          'primitive_estimate_exact_squared')
    check(W**4 <= 64**4*n, 'omega_64_bound')
    regular_hist = Counter({1: p-r})
    for d in orders:
        if d is not None:
            regular_hist[d] += p-1
    R = p*(p-r)
    check(sum(regular_hist.values()) == R, 'regular_point_normalization')
    check(regular_hist[1] == 2*p-r-1, 'regular_fixed_count')
    # Independent primitive count over field values and their square preimages.
    eta = lambda a: (0 if a % p == 0 else (1 if log[a % p] % 2 == 0 else -1))
    roots_count = sum(1+eta(a-1) for a in range(1, p)
                      if gcd(n, log[a]) == 1)
    check(P == roots_count, 'primitive_by_square_preimage_multiplicity')
    check(sum(eta(a) for a in aa) == -1, 'quadratic_exception_minus_one')
    moment = sum(Q(c, R)*h(Q(d, p)) for d, c in regular_hist.items())
    check(moment == Q((p-2)*(p-1)*P, p*R), 'regular_ramp_moment')
    cutoffs = {Q(0), Q(1,2), Q(3,4), Q(99,100), Q(1), Q(n,p)}
    for d in regular_hist:
        cutoffs.update([Q(d,p)-Q(1,10*p), Q(d,p), Q(d,p)+Q(1,10*p)])
    for x in sorted(cutoffs):
        cdf = Q(sum(c for d,c in regular_hist.items() if Q(d,p) <= x), R)
        if Q(1,2) <= x < Q(n,p):
            check(cdf == 1-Q((p-1)*P,R), 'cdf_strict_primitive_exclusion')
        if x >= Q(n,p):
            check(cdf == 1, 'cdf_at_or_above_moving_cutoff')
        if x == 0:
            check(cdf == 0, 'cdf_zero')
    if p <= 251:
        # Formal coefficient identity S(X)-eta(-1)J(X)=1+...+X^(n-1).
        # Every nonprincipal character evaluates the RHS to zero.
        s = [0]*n
        j = [0]*n
        for a in aa:
            if a:
                s[log[a]] += 1
        for t in range(p):
            if (1-t) % p:
                j[log[(1-t) % p]] += eta(t)
        check(all(s[e]-eta(-1)*j[e] == 1 for e in range(n)),
              'formal_group_ring_jacobi_identity_all_characters')
        # Exact autocorrelation gives the squared magnitude for every character
        # via finite Fourier transform: principal (p-r)^2, quadratic 1, others p.
        for shift in range(n):
            autocorrelation = sum(s[e]*s[(e-shift) % n] for e in range(n))
            predicted = Q((p-r)**2-p+(1-p)*(-1)**shift,n)
            if shift == 0:
                predicted += p
            check(autocorrelation == predicted,
                  'integer_autocorrelation_character_norms')
    if p <= 97:
        successor, periods = graph(p)
        check(len(set(successor)) == p*p-r*(p-1), 'full_graph_image_count')
        check(sum(d == 0 for d in periods) == r*(p-1), 'exact_transient_count')
        observed_regular = Counter()
        for z, period in enumerate(periods):
            u, v = divmod(z,p)
            expected = 1 if v == 0 else (0 if aa[u] == 0 else orders[u])
            check(period == expected, 'functional_graph_period_or_transient')
            if aa[u]:
                observed_regular[period] += 1
                inverse = u*p + ((successor[z] % p)*pow(aa[u],p-2,p) % p)
                check(inverse == z, 'regular_two_sided_inverse')
        check(observed_regular == regular_hist, 'graph_vs_discrete_log_histogram')
        graph_points += p*p
    if r and p <= 101:
        # Every possible retained count; mixed, enormous finite assigned periods.
        assigned = [Q(0), Q(1), Q(p), Q(p*p), Q(10**100)]
        for e in range(r*p+1):
            mixture = [assigned[k % len(assigned)] for k in range(e)]
            for x in [Q(1,2),Q(3,4),Q(1),Q(10**99)]:
                c = sum(c for d,c in regular_hist.items() if Q(d,p) <= x)
                completed = Q(c+sum(t/p <= x for t in mixture),R+e)
                check(abs(completed-Q(c,R)) <= Q(r,p),
                      'mixed_completion_every_retained_count_cdf')
            completed_moment = (R*moment+sum(h(t/p) for t in mixture))/(R+e)
            check(abs(completed_moment-moment) <= Q(r,p),
                  'mixed_completion_every_retained_count_moment')
    rows.append({'p':p,'r':r,'P':P,'theta':str(theta),'regular_ramp':str(moment)})

# Primitive indicator by exact Ramanujan sums, including repeated prime factors.
for n in range(1, 251):
    ds = [d for d in range(1,n+1) if n % d == 0]
    for k in range(n):
        value = Q(phi(n),n)*sum(
            Q(mobius(d),phi(d))*sum(c*mobius(d//c) for c in ds
                                  if d % c == 0 and k % c == 0)
            for d in ds)
        check(value == int(gcd(n,k) == 1), 'exact_ramanujan_primitive_indicator')

# Mobius rearrangement including prime 2, and exact absolute tail control.
for X in [2,3,10,31,100,251]:
    qs = primes(X)
    direct = sum((Q(phi(p-1),p-1) for p in qs),Q())
    rearranged = sum((Q(mobius(d),d)*sum((p-1) % d == 0 for p in qs)
                      for d in range(1,X)),Q())
    check(direct == rearranged,'mobius_prime_mean_rearrangement_including_two')
    for K in [1,2,5,10,20]:
        if K < X:
            tail = sum((Q(abs(mobius(d)),d)*sum((p-1) % d == 0 for p in qs)
                        for d in range(K+1,X)),Q())
            check(tail <= Q(X,K),'mobius_absolute_tail')
check(Q(1,2)*(1-Q(5,12)) == Q(7,24) > Q(13,48), 'strict_mean_constant_gap')

output = {'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'python':sys.version,'total_checks':sum(COUNTS.values()),
          'counts':dict(sorted(COUNTS.items())),
          'odd_prime_bound':1009,'odd_primes':len(ps),
          'class3_primes':sum(p % 4 == 3 for p in ps),
          'full_graph_bound':97,'full_graph_points':graph_points,
          'group_ring_character_bound':251,
          'scope':'Exact finite consistency and counterexample search only; no asymptotic inference',
          'prime_rows':rows}
print(json.dumps(output,indent=2,sort_keys=True))
