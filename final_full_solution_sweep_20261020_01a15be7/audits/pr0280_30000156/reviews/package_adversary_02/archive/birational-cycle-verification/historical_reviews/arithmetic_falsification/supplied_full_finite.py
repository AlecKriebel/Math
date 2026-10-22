"""Independent exact finite audit of L(u,v)=(u,(u^2+1)v).

Stdlib only. Uses full functional graphs (including tails at inadmissible primes),
subgroup inclusion-exclusion, root multiplicities over multiplier values, and
an independently implemented cyclotomic ring for exact Gauss-sum checks.
It does not import or execute any submission helper or prior review.
No finite range proves an asymptotic, infinitude, or historical novelty.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from math import gcd, isqrt
import json
import platform
import sys

COUNTS = Counter()

def require(condition, label, detail=None):
    if not condition:
        raise AssertionError((label, detail))
    COUNTS[label] += 1

def primes_through(bound):
    sieve = bytearray([1]) * (bound + 1)
    sieve[0:2] = b"\0\0"
    for n in range(2, isqrt(bound) + 1):
        if sieve[n]:
            sieve[n*n:bound+1:n] = b"\0" * (((bound - n*n) // n) + 1)
    return [i for i in range(2, bound + 1) if sieve[i]]

def factorization(n):
    out = {}
    q = 2
    while q*q <= n:
        while n % q == 0:
            out[q] = out.get(q, 0) + 1
            n //= q
        q += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out

def totient(n):
    result = n
    for q in factorization(n):
        result = result // q * (q - 1)
    return result

def mobius(n):
    f = factorization(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)

@lru_cache(None)
def divisors(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)

def unit_order(a, p):
    if a == 0:
        return None
    return next(d for d in divisors(p-1) if pow(a, d, p) == 1)

def is_primitive(a, p):
    return a != 0 and all(pow(a, (p-1)//q, p) != 1 for q in factorization(p-1))

def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p-1)//2, p)
    require(value in (1, p-1), "Euler_criterion_values", (a, p, value))
    return 1 if value == 1 else -1

def graph(p):
    # Nodes are the integers 0..p^2-1; u is the quotient, v the remainder.
    successor = [u*p + ((u*u + 1)*v % p) for u in range(p) for v in range(p)]
    indegree = [0] * (p*p)
    for b in successor:
        indegree[b] += 1
    visited = bytearray(p*p)
    periods = [0] * (p*p)  # 0 denotes a point that is not itself periodic.
    cycle_histogram = Counter()
    for start in range(p*p):
        if visited[start]:
            continue
        path = []
        index = {}
        cur = start
        while not visited[cur] and cur not in index:
            index[cur] = len(path)
            path.append(cur)
            cur = successor[cur]
        if cur in index:
            cycle = path[index[cur]:]
            d = len(cycle)
            cycle_histogram[d] += 1
            for node in cycle:
                periods[node] = d
        for node in path:
            visited[node] = 1
    return successor, indegree, periods, cycle_histogram

def reduced(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)

def monic_division(dividend, divisor):
    work = list(reduced(dividend))
    divisor = reduced(divisor)
    assert divisor[-1] == 1
    quotient = [0] * max(1, len(work)-len(divisor)+1)
    while len(work) >= len(divisor) and work != [0]:
        k = len(work)-len(divisor)
        leading = work[-1]
        quotient[k] = leading
        for j, c in enumerate(divisor):
            work[k+j] -= leading*c
        work = list(reduced(work))
    return reduced(quotient), reduced(work)

@lru_cache(None)
def cyclotomic(n):
    # Independent recursive exact construction: X^n-1 = product Phi_d.
    result = [-1] + [0] * (n-1) + [1]
    for d in divisors(n):
        if d < n:
            result, remainder = monic_division(result, cyclotomic(d))
            assert remainder == (0,)
    require(len(result)-1 == totient(n), "cyclotomic_degree", n)
    return reduced(result)

def ring_reduce(exponent_coefficients, n):
    # First use X^n=1, then reduce modulo Phi_n. Handles integers and fractions.
    poly = [0]*n
    for exp, coefficient in exponent_coefficients.items():
        poly[exp % n] += coefficient
    return monic_division(poly, cyclotomic(n))[1]

def add(left, right, scale=1):
    out = Counter(left)
    for exp, coefficient in right.items():
        out[exp] += scale*coefficient
    return out

def multiply(left, right, n):
    out = Counter()
    for a, x in left.items():
        for b, y in right.items():
            out[(a+b) % n] += x*y
    return out

def conjugate(poly, n):
    return {(-exp) % n: coefficient for exp, coefficient in poly.items()}

records = []
boundary_records = []
all_primes = primes_through(503)
for p in all_primes:
    admissible = p % 4 == 3
    if not admissible and p > 101:
        continue
    successor, indegree, periods, cycles = graph(p)
    point_histogram = Counter(d for d in periods if d)
    image_size = sum(i > 0 for i in indegree)
    zero_parameters = [u for u in range(p) if (u*u+1) % p == 0]
    periodic_points = sum(d > 0 for d in periods)
    require(sum(d*count for d, count in cycles.items()) == periodic_points,
            "cycle_to_point_weight", p)
    require(image_size == p*p - len(zero_parameters)*(p-1),
            "image_size_exact_all_primes", p)
    require(periodic_points == image_size, "periodic_vs_tail_all_primes", p)
    require(len(zero_parameters) == (0 if admissible else 1 if p == 2 else 2),
            "vanishing_denominator_scope", p)
    if not admissible:
        require(any(d != 1 for d in indegree), "inadmissible_not_permutation", p)
        for u in zero_parameters:
            for v in range(1, p):
                z = u*p+v
                require(periods[z] == 0 and successor[z] == u*p
                        and successor[u*p] == u*p,
                        "zero_multiplier_depth_one_tail", (p, u, v))
        boundary_records.append({"p": p, "zero_parameters": zero_parameters,
                                 "image_size": image_size,
                                 "periodic_points": periodic_points,
                                 "transient_points": p*p-periodic_points})
        continue
    require(all(d == 1 for d in indegree), "admissible_permutation_indegree", p)
    require(all(d > 0 for d in periods), "admissible_all_points_periodic", p)
    orders = [unit_order((u*u+1) % p, p) for u in range(p)]
    primitive_u = sum(d == p-1 for d in orders)
    require(primitive_u == sum(is_primitive((u*u+1) % p, p) for u in range(p)),
            "primitive_by_prime_factor_test", p)
    # Alternate P formula: inclusion-exclusion over proper prime-index subgroups.
    exclusion_total = 0
    rad = 1
    for q in factorization(p-1):
        rad *= q
    for d in divisors(rad):
        exclusion_total += mobius(d)*sum(pow((u*u+1) % p, (p-1)//d, p) == 1
                                        for u in range(p))
    require(exclusion_total == primitive_u, "primitive_subgroup_inclusion_exclusion", p)
    # Count by multiplier values, not fiber parameters.
    primitives = [a for a in range(1, p) if is_primitive(a, p)]
    require(len(primitives) == totient(p-1), "all_primitive_multipliers_count", p)
    roots_count = sum(1+legendre(a-1, p) for a in primitives)
    require(roots_count == primitive_u, "primitive_root_multiplicity_count", p)
    for u in range(p):
        a = (u*u+1) % p
        for v in range(p):
            z = u*p+v
            require(periods[z] == (1 if v == 0 else orders[u]),
                    "full_graph_period_vs_divisor_order", (p, u, v))
            inverse_node = u*p + (pow(a, p-2, p)*(successor[z] % p) % p)
            require(inverse_node == z, "Fermat_inverse_on_each_point", (p, u, v))
    # Derive whole point histogram from all multiplier orders.
    predicted_histogram = Counter({1: p})
    predicted_cycles = Counter({1: p})
    for order in orders:
        predicted_histogram[order] += p-1
        predicted_cycles[order] += (p-1)//order
    require(point_histogram == predicted_histogram, "all_period_point_histogram", p)
    require(cycles == predicted_cycles, "all_period_cycle_histogram", p)
    # Threshold controls include every possible normalized period and either side.
    eps = F(1, 10*p)
    xs = {F(-1), F(0), F(1,p)-eps, F(1,p), F(1,p)+eps,
          F(1,2), F(3,5), F(3,4), F(9,10), F(p-1,p)-eps,
          F(p-1,p), F(p-1,p)+eps, F(1), F(1)+eps}
    for d in divisors(p-1):
        xs.update((F(d,p)-eps, F(d,p), F(d,p)+eps))
    threshold_examples = []
    for x in sorted(xs):
        actual = F(sum(count for d, count in point_histogram.items() if d <= p*x), p*p)
        universal = F(p*int(1 <= p*x)+(p-1)*sum(d <= p*x for d in orders), p*p)
        require(actual == universal, "cdf_general_exact", (p, x))
        if F(1,2) <= x < 1:
            predicted = 1-F((p-1)*primitive_u, p*p) if x < F(p-1,p) else F(1)
            require(actual == predicted, "cdf_half_interval_piecewise_exact", (p, x))
        if x == 1:
            require(actual == 1, "cdf_at_one", p)
        if x in (F(1,2), F(3,4), F(p-1,p)):
            threshold_examples.append({"x": str(x), "D": str(actual),
                                       "primitive_only_exclusion_valid": x < F(p-1,p)})
    theta = F(totient(p-1), p-1)
    W = 2**len(factorization(p-1))
    error = abs(F(primitive_u,p)-theta)
    require(error*error <= theta*theta*F((W-1)**2,p),
            "original_character_estimate_squared", p)
    # Sharper bound: quadratic character contributes only 1, remaining W-2 terms sqrt(p).
    # Equivalent rationalized check for |P/p-theta| <= theta[(W-2)sqrt(p)+1]/p.
    t = abs(F(primitive_u,p)-theta)*p/theta - 1
    require(t <= 0 or t*t <= (W-2)**2*p,
            "quadratic_character_sharpened_estimate", p)
    records.append({"p": p, "primitive_parameter_count": primitive_u,
                    "theta": str(theta), "D_at_three_quarters":
                    str(F(sum(n for d,n in point_histogram.items() if 4*d <= 3*p),p*p)),
                    "point_count": p*p, "cycle_count": sum(cycles.values()),
                    "period_histogram": {str(d): n for d,n in sorted(point_histogram.items())},
                    "threshold_examples": threshold_examples})

# Formula (3) evaluated in a genuine exact cyclotomic ring, without Ramanujan sums.
for N in range(2, 65):
    theta = F(totient(N), N)
    for exponent in range(N):
        coefficients = Counter()
        for character_k in range(N):
            d = N//gcd(character_k, N)
            coefficients[(character_k*exponent) % N] += theta*F(mobius(d), totient(d))
        got = ring_reduce(coefficients, N)
        require(got == (int(gcd(exponent,N) == 1),),
                "primitive_indicator_exact_character_evaluation", (N, exponent, got))

character_records = []
for p in primes_through(31):
    if p == 2:
        continue
    N = p-1
    g = next(a for a in range(1,p) if is_primitive(a,p))
    logs = {pow(g,k,p): k for k in range(N)}
    eta_sign = legendre(-1,p)
    def char(k,a):
        return None if a % p == 0 else (k*logs[a % p]) % N
    def G(k):
        # zeta_(pN)^p and zeta_(pN)^N are primitive Nth and pth roots.
        return Counter((p*char(k,a)+N*a) % (p*N) for a in range(1,p))
    def J(k,l):
        terms = Counter()
        for t in range(p):
            a,b = char(k,t), char(l,1-t)
            if a is not None and b is not None:
                terms[(a+b) % N] += 1
        return terms
    eta = N//2
    G_eta = G(eta)
    require(ring_reduce(add(multiply(G_eta, conjugate(G_eta,p*N),p*N),{0:p},-1),p*N)
            == (0,), "quadratic_Gauss_norm_exact", p)
    S_trivial = sum((u*u+1) % p != 0 for u in range(p))
    require(S_trivial == p-(0 if p%4 == 3 else 2),
            "trivial_character_zero_extension_all_odd_primes", p)
    for k in range(1,N):
        G_k = G(k)
        norm = multiply(G_k, conjugate(G_k,p*N),p*N)
        require(ring_reduce(add(norm,{0:p},-1),p*N) == (0,),
                "all_nontrivial_Gauss_norm_exact", (p,k))
        S = Counter()
        for u in range(p):
            a = char(k,u*u+1)
            if a is not None:
                S[a] += 1
        jacobi = J(eta,k)
        require(ring_reduce(add(S,jacobi,-eta_sign),N) == (0,),
                "square_root_to_Jacobi_all_odd_primes", (p,k))
        product_k = (eta+k) % N
        if product_k == 0:
            require(ring_reduce(add(jacobi,{0:-eta_sign},-1),N) == (0,),
                    "inverse_character_Jacobi_exception_exact", p)
            require(ring_reduce(add(S,{0:-1},-1),N) == (0,),
                    "quadratic_sum_minus_one_exact", p)
        else:
            J_embedded = {p*exp: coeff for exp,coeff in jacobi.items()}
            left = multiply(G_eta,G_k,p*N)
            right = multiply(J_embedded,G(product_k),p*N)
            require(ring_reduce(add(left,right,-1),p*N) == (0,),
                    "Gauss_Jacobi_product_exact", (p,k))
        # Exact S magnitude as a second path, with the sign and exception present.
        target = 1 if k == eta else p
        require(ring_reduce(add(multiply(S,conjugate(S,N),N),{0:target},-1),N) == (0,),
                "character_sum_norm_exact", (p,k))
    character_records.append({"p":p,"primitive_generator":g,
                              "characters_tested":N-1,"eta_minus_one":eta_sign,
                              "trivial_sum":S_trivial,
                              "coefficient_ring":"Z[zeta_(p(p-1))] for Gauss products"})

# Crude growth constants on a range, including all highly composite controls in it.
for n in range(1,20001):
    phi = totient(n)
    require(2*phi*phi >= n,"totient_square_lower_bound",n)
    W = 2**len(factorization(n))
    require(W**4 <= 64**4*n,"omega_growth_constant_64",n)

# Rational algebra checks use exact specialized iterates; identities are proved in REVIEW.md.
algebra_records = []
for u in (F(-3,2),F(-1),F(0),F(1),F(5,3)):
    for v in (F(-7,4),F(0),F(1)):
        a = u*u+1
        forward = (u,a*v)
        inverse_forward = (forward[0],forward[1]/(forward[0]*forward[0]+1))
        require(inverse_forward == (u,v),"rational_specialized_two_sided_inverse",(u,v))
        if u == 1 and v == 1:
            for n in range(1,21):
                require(a**n*v != v,"infinite_order_falsification_controls",n)
                algebra_records.append({"n":n,"L_n_at_1_1":["1",str(a**n*v)]})

output = {
    "status":"PASS", "counts":dict(sorted(COUNTS.items())),
    "assertions":sum(COUNTS.values()),
    "runtime":{"executable":sys.executable,"python":sys.version,"platform":platform.platform(),
               "dependencies":"Python standard library only"},
    "finite_scope":{"admissible_primes_through":503,
                    "inadmissible_primes_through":101,
                    "admissible_prime_count":len(records),
                    "whole_admissible_plane_points":sum(r["point_count"] for r in records),
                    "character_all_odd_primes_through":31,
                    "primitive_indicator_group_orders":"2..64",
                    "integer_growth_controls":"1..20000"},
    "admissible_records":records,"inadmissible_records":boundary_records,
    "character_records":character_records,"algebra_records":algebra_records,
    "scope_warning":"Exact finite evidence only. No finite experiment establishes infinitude, asymptotics, nonconvergence, source applicability, or historical novelty."
}
print(json.dumps(output,indent=2,sort_keys=True))
