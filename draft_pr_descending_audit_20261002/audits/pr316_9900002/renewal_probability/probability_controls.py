#!/usr/bin/env python3
"""Independent exact controls; finite checks are not an infinite theorem proof."""
from fractions import Fraction as Q
from itertools import product
import json

checks = 0

def check(condition):
    global checks
    assert condition
    checks += 1

def p(n):
    return Q(1, 1 << (1 << n))

def a(n):
    return 1 << (1 << (2*n))

def exact_inspected_law(law, t):
    """Enumerate actual finite paths, stopping at the first STRICT crossing."""
    completed = {x: Q(0) for x in law}
    stack = [(0, Q(1))]
    while stack:
        start, weight = stack.pop()
        for x, mass in law.items():
            w = weight * mass
            if start+x > t:
                completed[x] += w
            else:
                stack.append((start+x, w))
    return completed

def first_success_truncated(law, threshold, horizon):
    """Enumerate failure tuples; retain unfinished sums after horizon draws."""
    small = [(x, mass) for x, mass in law.items() if x < threshold]
    q = sum((mass for x, mass in law.items() if x >= threshold), Q(0))
    hit = moment = Q(0)
    for j in range(horizon):
        for seq in product(small, repeat=j):
            w = Q(1)
            length = 0
            for x, mass in seq:
                w *= mass
                length += x
            hit += w * law[threshold]
            moment += w*q*length
    for seq in product(small, repeat=horizon):
        w = Q(1)
        length = 0
        for x, mass in seq:
            w *= mass
            length += x
        moment += w*length
    return hit, moment

def path_interval(seq, t, strict=True):
    end = 0
    for x in seq:
        end += x
        if end > t if strict else end >= t:
            return x
    raise AssertionError("Sequence supplied too few intervals")

# Candidate-law arithmetic uses binary shifts, independently of author code.
rows = []
for n in range(2,7):
    an, prev, pn = a(n), a(n-1), p(n)
    t = an//2
    B = t//prev
    check(B*prev == t)
    check(2 <= prev < t < an)
    check(p(n+1) == pn*pn)
    check(Q(2*prev,1)/(pn*an) == 1/(pn*B))
    candidate_exponent = 1+(1 << (2*(n-1)))+(1 << n)-(1 << (2*n))
    check(candidate_exponent <= -(1 << (2*(n-1))))
    eps = pn/(1-pn) + 1/(pn*B)
    check(0 < eps < 1)
    # A rigorous interval enclosing the infinite tail follows from its proof.
    prefix = sum((p(k) for k in range(n,n+4)), Q(0))
    tail_ceiling = p(n+4)/(1-p(n+4))
    qlo, qhi = prefix, prefix+tail_ceiling
    check(pn <= qlo <= qhi <= pn/(1-pn))
    check(qhi-pn <= pn*pn/(1-pn))
    # Interval for p0 and therefore for the exact lower-support mean M_n.
    all_prefix = sum((p(k) for k in range(1,n+4)), Q(0))
    p0lo, p0hi = 1-all_prefix-tail_ceiling, 1-all_prefix
    Mlo = Q(3,2)*p0lo + sum((p(k)*a(k) for k in range(1,n)), Q(0))
    Mhi = Q(3,2)*p0hi + sum((p(k)*a(k) for k in range(1,n)), Q(0))
    check(Q(2,3) <= p0lo <= p0hi <= 1)
    check(0 < Mlo <= Mhi <= prev)
    mhi = Mhi + t*qhi
    check(mhi/an <= Q(prev,an)+pn/(2*(1-pn)))
    rows.append({'n':n, 'candidate_exponent':candidate_exponent,
                 'geometric_failure_bound':'2**'+str(candidate_exponent),
                 'error_majorant_verified':True})

# Whole-n inequalities underlying the analytical exponent argument.
for n in range(2,60):
    check((1 << n)+1 <= 2*(1 << (2*(n-1))))
    check((1 << (2*(n+1)))-(1 << (n+1)) > (1 << (2*n))-(1 << n))

# First-hit conditioning identities and actual inspected renewal paths.
law_cases = [
    {1:Q(1,2), 2:Q(1,4), 6:Q(1,8), 11:Q(1,8)},
    {1:Q(1,5), 2:Q(2,5), 6:Q(3,10), 11:Q(1,10)},
    {1:Q(3,5), 3:Q(1,5), 8:Q(3,20), 13:Q(1,20)},
    {1:Q(1,10), 3:Q(1,10), 8:Q(3,5), 13:Q(1,5)},
]
cases = 0
for law in law_cases:
    threshold = sorted(law)[2]
    q = sum((v for x,v in law.items() if x>=threshold), Q(0))
    r = 1-q
    M = sum((x*v for x,v in law.items() if x<threshold), Q(0))
    A = max(x for x in law if x<threshold)
    check(sum(law.values()) == 1)
    for horizon in (1,2,4,7):
        hit, moment = first_success_truncated(law,threshold,horizon)
        check(hit == law[threshold]/q*(1-r**horizon))
        check(moment == M/q*(1-r**horizon))
    for t in (A,threshold//2,threshold-1):
        actual = exact_inspected_law(law,t)
        check(sum(actual.values()) == 1)
        B = t//A
        block_event = law[threshold]/q*(1-r**(B+1))
        markov_union = law[threshold]/q-M/(q*t)
        check(actual[threshold] >= block_event)
        check(actual[threshold] >= markov_union)
        check(sum((v*min(x,t) for x,v in law.items()),Q(0)) == M+t*q)
        cases += 1

# Meaningful adversarial controls: remove one needed hypothesis at a time.
equal_tail_law = {1:Q(1,2),4:Q(1,4),8:Q(1,4)}
equal_tail = exact_inspected_law(equal_tail_law,2)
check(equal_tail[4] == Q(7,16))
check(equal_tail[4] == equal_tail[8])
large_wait_law = {1:Q(99,100),6:Q(1,100)}
large_wait = exact_inspected_law(large_wait_law,3)
check(large_wait[6] == 1-Q(99,100)**4)
check(large_wait[6] < Q(1,20))
check(1-Q(99,100)/(Q(1,100)*3) < 0)
check(path_interval([3,1,1],4) == 1)  # a first success too short to cross
check(path_interval([2,6],2) == 6)    # T equals inspection time: next interval
check(path_interval([2,6],2,False) == 2) # the wrong endpoint convention differs

print(json.dumps({'status':'PASS','assertions':checks,
                  'finite_law_time_cases':cases,
                  'failure_tuple_horizons':[1,2,4,7],
                  'parameter_rows':rows,
                  'controls':{'equal_tail_desired_probability':str(equal_tail[4]),
                              'large_wait_desired_probability':str(large_wait[6]),
                              'short_success_is_insufficient':True,
                              'strict_endpoint_convention_verified':True},
                  'scope':'Exact finite controls; infinite-law and limit conclusions rely on the separate analytical proof.'},indent=2))
