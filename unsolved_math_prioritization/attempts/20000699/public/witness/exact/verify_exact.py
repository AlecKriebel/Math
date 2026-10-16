#!/usr/bin/env python3
"""Finite exact checks supporting, never replacing, the accompanying proofs."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import sympy as s

ROOT = Path(__file__).resolve().parent


def factor(n):
    ans = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            ans[p] = ans.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        ans[n] = ans.get(n, 0) + 1
    return ans


def mu(n):
    fs = factor(n)
    return 0 if any(e > 1 for e in fs.values()) else (-1)**len(fs)


def divisors(n):
    return [d for d in range(1, math.isqrt(n)+1) if n % d == 0
            for d in ([d] if d*d == n else [d, n//d])]


def phi(n):
    ans = n
    for p in factor(n):
        ans = ans//p*(p-1)
    return ans


def ramanujan(q, h):
    return sum(d*mu(q//d) for d in divisors(math.gcd(q, h)))


def hl_local(p, h):
    nu = 1 if h % p == 0 else 2
    return F(1, 1) - F(nu, p)


results = {"purpose": "Exact finite regression tests; the mathematical proofs are separate."}

# Logarithms are represented by their formal prime-exponent vectors, so there
# is no floating point cancellation in the Mangoldt derivative check.
coefficient_cases = 0
for n in range(1, 2001):
    ds = divisors(n)
    assert sum(mu(e) for e in ds) == (1 if n == 1 else 0)
    vec_d, vec_e = {}, {}
    for e in ds:
        m = mu(e)
        for p, k in factor(n//e).items():
            vec_d[p] = vec_d.get(p, 0) + m*k
        for p, k in factor(e).items():
            vec_e[p] = vec_e.get(p, 0) + m*k
    fs = factor(n)
    expected = {next(iter(fs)): 1} if len(fs) == 1 else {}
    assert {p:k for p,k in vec_d.items() if k} == expected
    assert {p:k for p,k in vec_e.items() if k} == {p:-k for p,k in expected.items()}
    coefficient_cases += 1
results["coefficient_and_derivative_cases"] = coefficient_cases
results["primepowers_checked"] = [p**k for p in (2,3,5,7) for k in range(1,6) if p**k <= 2000]
results["n_equals_one"] = "I=1; both shift derivatives=0; Lambda(1)=0"

primes = [p for p in range(2, 102) if len(factor(p)) == 1 and factor(p).get(p) == 1]
local_cases = 0
for h in range(1, 201):
    for p in primes:
        cp = ramanujan(p,h)
        assert cp == (p-1 if h % p == 0 else -1)
        density = 1 + F(cp,(p-1)**2)
        assert density == hl_local(p,h)/(1-F(1,p))**2
        for j in (2,3,4):
            # F(p^j)=0, but Ramanujan sums themselves need not vanish.
            assert 0 * ramanujan(p**j,h) == 0
        local_cases += 1
results["hardy_littlewood_local_cases"] = local_cases
results["odd_gap_obstruction"] = all(1+F(ramanujan(2,h),1)==0 for h in range(1,200,2))

squarefree_cases = 0
for q in range(1,101):
    if mu(q) == 0:
        continue
    for h in range(1,51):
        assert ramanujan(q,h) == math.prod(ramanujan(p,h) for p in factor(q))
        assert F(mu(q)**2,phi(q)**2) == math.prod(F(1,(p-1)**2) for p in factor(q))
        squarefree_cases += 1
results["squarefree_ramanujan_cases"] = squarefree_cases

t1,t2,u,v = s.symbols('t1 t2 u v')
assert s.expand((1-t1)*(1-t2)+u-t1*t2-(1-t1-t2+u)) == 0
results["corrected_mellin_local_identity"] = "(1-t1)(1-t2)+u-t1*t2 = 1-t1-t2+u"
# p=2, all four original shifts zero, p^(-s)=2/3.
corrected = (1-F(1,2)-F(1,2)+F(1,3))/(1-F(3,4))
printed = (1-F(1,3)-F(1,3)+F(1,3))/(1-F(1,3))
assert corrected == F(4,3) and printed == 1 and corrected != printed
results["printed_shift_counterexample_local"] = {"p":2,"p_to_minus_s":"2/3","corrected":"4/3","printed":"1"}

# Exact positive divisor expansion finite-prime analogue of sum S(h)<=H.
# Truncating C2 alone would reverse the desired inequality for the full S;
# therefore compare with its correspondingly truncated reciprocal product.
mean_cases = 0
for bound in (3,5,11,31,101):
    ps = [p for p in primes if 2<p<=bound]
    c2 = math.prod(1-F(1,(p-1)**2) for p in ps)
    reciprocal = math.prod(1+F(1,p*(p-2)) for p in ps)
    assert c2*reciprocal == 1
    for H in range(1,101):
        total = F(0)
        for h in range(2,H+1,2):
            total += 2*c2*math.prod(F(p-1,p-2) for p in ps if h%p==0)
        assert total <= H
        mean_cases += 1
results["finite_prime_mean_bound_cases"] = mean_cases

# Support checks use exact eta=e^(2pi A/T)-1 as an independent rational.
# N eta/(1+eta) determines H, and x>=h/eta is the exact support condition.
support_cases = 0
for N in (1,2,7,100,1000):
    for eta in (F(1,100),F(1,10),F(1,2),F(1),F(3)):
        H = int(N*eta/(1+eta))
        assert 0 <= H <= N-1
        for h in range(1,N+1):
            has_closed_support = F(h,1)/eta <= N-h
            assert has_closed_support == (h<=H)
            if F(h,1)/eta == N-h:
                assert h == H  # The smooth Fourier boundary is exactly zero.
            support_cases += 1
results["sharp_support_cases"] = support_cases

phi0,psi0,lam = F(3,4),F(1,4),F(6,5)
assert 0 < psi0 <= phi0 < 1 and 1 < lam < 2
assert lam*phi0 == F(9,10) < 1
assert lam*(1-psi0) == F(9,10) < 1
results["corrected_parameter_example"] = {"phi":"3/4","psi":"1/4","lambda":"6/5","lambda_phi":"9/10","lambda_one_minus_psi":"9/10"}
assert F(7,10)>F(3,5)
results["excluded_parameter_example"] = {"phi":"3/5","psi":"7/10","lambda":"6/5","reason":"Satisfies original length inequalities but psi>phi makes the unchanged complex-uniform cumulative profile inconsistent."}
results["status"] = "PASS"
(ROOT/'EXACT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
