#!/usr/bin/env python3
"""Exact finite regression controls. These do not prove all-height zero claims."""
from fractions import Fraction as F
from itertools import combinations
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def prime_factors(n):
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            k = 0
            while n % p == 0:
                n //= p
                k += 1
            out.append((p, k))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def mu(n):
    fac = prime_factors(n)
    return 0 if any(k > 1 for _, k in fac) else (-1) ** len(fac)


def lam(n, primes):
    fac = prime_factors(n)
    return 0 if any(p not in primes for p, _ in fac) else (-1) ** sum(k for _, k in fac)


def convolution(a, b, limit):
    c = [0] * (limit + 1)
    for d in range(1, limit + 1):
        if a[d]:
            for k in range(1, limit // d + 1):
                c[d * k] += a[d] * b[k]
    return c


def euler_multiplier(P, Q, limit):
    u = [0] * (limit + 1)
    u[1] = 1
    for p in sorted(P ^ Q):
        v = [0] * (limit + 1)
        v[1] = 1
        if p in Q:
            if p <= limit:
                v[p] = 1
        else:
            k, power = 1, p
            while power <= limit:
                v[power] = (-1) ** k
                k += 1
                power *= p
        u = convolution(u, v, limit)
    return u


def run():
    checks = {}
    count = 0
    for n in range(1, 513):
        require(sum(mu(d) for d in range(1, n + 1) if n % d == 0) == int(n == 1), "Mobius convolution")
        count += 1
    checks["mobius_divisor_identities"] = count

    base = [2, 3, 5, 7]
    subsets = [frozenset(c) for k in range(5) for c in combinations(base, k)]
    limit = 128
    count = 0
    for P in subsets:
        lp = [0] + [lam(n, P) for n in range(1, limit + 1)]
        for Q in subsets:
            lq = [0] + [lam(n, Q) for n in range(1, limit + 1)]
            u = euler_multiplier(P, Q, limit)
            ui = euler_multiplier(Q, P, limit)
            result = convolution(u, lq, limit)
            inv = convolution(u, ui, limit)
            for n in range(1, limit + 1):
                require(result[n] == lp[n], "Euler perturbation coefficient")
                require(inv[n] == int(n == 1), "Euler multiplier inverse")
                count += 2
    checks["euler_perturbation_coefficient_equalities"] = count

    count = 0
    for denominator in range(2, 9):
        xs = [F(1)] + [F(denominator + k, denominator) for k in range(1, 13)]
        aa = [1] + [(-1) ** k if k % 4 else 0 for k in range(1, 13)]
        for q in range(1, 13):
            ms = [((q*x).numerator + (q*x).denominator - 1)//(q*x).denominator for x in xs]
            grouped = {}
            for m, a in zip(ms, aa):
                grouped[m] = grouped.get(m, 0) + a
            D1 = sum(F(a)/x for a, x in zip(aa, xs))
            E1 = sum(F(a)*(F(q,m)-1/x) for a,x,m in zip(aa,xs,ms))
            for exponent in range(1, 7):
                D = sum(F(a)/x**exponent for a, x in zip(aa, xs))
                B = sum(F(a, m**exponent) for m, a in grouped.items())
                E = sum(F(a)*(F(q,m)**exponent-x**(-exponent)) for a,x,m in zip(aa,xs,ms))
                bound = F(exponent,q)*sum(abs(a)*x**(-exponent-1) for a,x in zip(aa,xs))
                require(q**exponent*B == D+E, "Rounded series identity")
                require(abs(E) <= bound, "Integer-real rounding bound")
                count += 2
            B1 = sum(F(a,m) for m,a in grouped.items())
            require(q*(B1-F(E1+D1,q)) == 0, "Forced target zero")
            count += 1
    checks["rational_rounding_and_correction_equalities_or_bounds"] = count

    # The exact one-zero-loss and repeated-zero toy example, without floating pi.
    require(1-F(3,2)/F(3,2) == 0, "General frequency zero")
    require(1-F(3,2)/2 == F(1,4), "Rounding destroys the zero")
    require(F(3,4)-F(3,2)/2 == 0, "Constant correction restores real zero")
    # At s=1+2*pi*i*j/log(2), 2**(-s)=1/2 for every integer j.
    checks["rounding_zero_loss_and_restoration_exact_fixtures"] = 3

    # Gaussian rational pairs, avoiding floating-point tests of escaping roots.
    def mul(z,w):
        return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
    def sub(z,w):
        return (z[0]-w[0],z[1]-w[1])
    one=(F(1),F(0))
    zero=(F(0),F(0))
    for N in range(1,33):
        root=(F(2),F(N))
        inverse=(F(2,4+N*N),F(-N,4+N*N))
        def h(s):
            return mul(sub(s,one),sub(one,mul(s,inverse)))
        require(h(one)==zero,"Fixed root")
        require(h(root)==zero,"Escaping root")
    checks["escaping_root_exact_equalities"] = 64
    return {
        "schema":"dirichlet-single-zero-controls-v1",
        "arithmetic":"Python arbitrary-precision integers and fractions only",
        "checks":checks,
        "total_predicates":sum(checks.values()),
        "mathematical_scope":"Finite algebra and rational inequalities only; no global zero exclusion or proof of the original target.",
        "result":"PASS"
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
