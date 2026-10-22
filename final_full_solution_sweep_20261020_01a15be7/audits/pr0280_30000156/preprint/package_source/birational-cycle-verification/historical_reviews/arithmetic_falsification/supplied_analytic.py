"""Independent exact controls; no original author's checker is imported.

Run /opt/homebrew/bin/python3 -E -B checks.py
All character identities use integer cyclotomic polynomial arithmetic.
These finite controls supplement DERIVATION.md, not prove infinite claims.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
START = time.perf_counter()
COUNTS = Counter()


def check(condition, family):
    if not condition:
        raise AssertionError(family)
    COUNTS[family] += 1


def primes(limit):
    a = bytearray(b'\1') * (limit+1)
    a[:2] = b'\0\0'
    for q in range(2,isqrt(limit)+1):
        if a[q]:
            a[q*q:limit+1:q] = b'\0' * ((limit-q*q)//q+1)
    return [q for q in range(2,limit+1) if a[q]]


@lru_cache(None)
def factors(n):
    result = []
    q = 2
    while q*q <= n:
        exponent = 0
        while n % q == 0:
            exponent += 1
            n //= q
        if exponent:
            result.append((q,exponent))
        q += 1
    if n > 1:
        result.append((n,1))
    return tuple(result)


@lru_cache(None)
def divisors(n):
    result = [1]
    for q,e in factors(n):
        result = [a*q**b for a in result for b in range(e+1)]
    return tuple(sorted(result))


def phi(n):
    r = n
    for q,e in factors(n):
        r = r//q*(q-1)
    return r


def mobius(n):
    f = factors(n)
    return 0 if any(e>1 for q,e in f) else (-1)**len(f)


def trim(v):
    while len(v)>1 and not v[-1]:
        v.pop()
    return v


def divide_exact(a,b):
    a = trim(list(a))
    b = trim(list(b))
    assert b[-1] == 1
    quotient = [0] * max(1, len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        shift = len(a)-len(b)
        c = a[-1]
        quotient[shift] = c
        for j,t in enumerate(b):
            a[shift+j] -= c*t
        trim(a)
    assert not any(a)
    return tuple(trim(quotient))


@lru_cache(None)
def cyclotomic(n):
    a = [-1] + [0]*(n-1) + [1]
    for d in divisors(n):
        if d<n:
            a = divide_exact(a,cyclotomic(d))
    return tuple(a)


def reduce_poly(a,n):
    a = trim(list(a))
    f = cyclotomic(n)
    while len(a)>=len(f):
        shift = len(a)-len(f)
        c = a[-1]
        if c:
            for j,t in enumerate(f):
                a[shift+j] -= c*t
        trim(a)
    return tuple(a)


def poly_equal(a,b,n):
    difference = [0]*max(len(a),len(b))
    for j,c in enumerate(a):
        difference[j] += c
    for j,c in enumerate(b):
        difference[j] -= c
    return reduce_poly(difference,n) == (0,)


def cyclic_product(a,b,n,conjugate=False):
    result = [0]*n
    for i,c in enumerate(a):
        if c:
            for j,d in enumerate(b):
                if d:
                    result[(i-j if conjugate else i+j)%n] += c*d
    return result


def logarithms(p):
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q,e in factors(p-1)):
            break
    table = {}
    value = 1
    for e in range(p-1):
        table[value] = e
        value = value*g % p
    assert len(table)==p-1 and value==1
    return g, table


def char_vector(p,k,logs):
    n = p-1
    result = [0]*n
    for u in range(p):
        a = (u*u+1)%p
        if a:
            result[k*logs[a]%n] += 1
    return result


def jacobi_vector(p,a,b,logs,ring=None):
    n = p-1
    m = ring or n
    scale = m//n
    result = [0]*m
    for s in range(1,p):
        t = (1-s)%p
        if t:
            result[scale*(a*logs[s]+b*logs[t])%m] += 1
    return result


def gauss_vector(p,k,logs):
    n = p-1
    m = p*n
    result = [0]*m
    for t in range(1,p):
        result[(p*k*logs[t]+n*t)%m] += 1
    return result


for n in range(1,601):
    for k in range(n):
        indicator = Fraction(phi(n),n)*sum(
            Fraction(mobius(d),phi(d))*sum(m*mobius(d//m) for m in divisors(gcd(d,k)))
            for d in divisors(n))
        check(indicator==int(gcd(k,n)==1), 'primitive_indicator')

for n in range(1,20001):
    check(2*phi(n)**2 >= n, 'phi_lower_bound')
    check(2**(4*len(factors(n))) <= 64**4*n, 'omega_bound')

for p in primes(103)[1:]:
    n = p-1
    g, logs = logarithms(p)
    eta_index = n//2
    eta_minus_one = (-1)**(n//2)
    for k in range(1,n):
        s = char_vector(p,k,logs)
        j = jacobi_vector(p,eta_index,k,logs)
        check(poly_equal(s,[eta_minus_one*c for c in j],n), 'quadratic_jacobi_identity')
        check(poly_equal(cyclic_product(s,s,n,conjugate=True),[1 if k==eta_index else p],n),
              'quadratic_character_exact_norm')
        if k==eta_index:
            check(poly_equal(s,[-1],n), 'exceptional_quadratic_sum')
    if p<=19:
        m = p*n
        gs = {k:gauss_vector(p,k,logs) for k in range(1,n)}
        for k,v in gs.items():
            check(poly_equal(cyclic_product(v,v,m,conjugate=True),[p],m),'gauss_exact_norm')
        for a in range(1,n):
            for b in range(1,n):
                c = (a+b)%n
                if c:
                    j = jacobi_vector(p,a,b,logs,ring=m)
                    check(poly_equal(cyclic_product(gs[a],gs[b],m),cyclic_product(j,gs[c],m),m),
                          'gauss_jacobi_product')

finite_rows = []
for p in [q for q in primes(997) if q%4==3]:
    n = p-1
    g, logs = logarithms(p)
    orders = [n//gcd(logs[(u*u+1)%p],n) for u in range(p)]
    P = orders.count(n)
    theta = Fraction(phi(n),n)
    check((P-p*theta)**2 <= theta**2*(2**len(factors(n))-1)**2*p, 'primitive_count_bound')
    for x in [Fraction(1,2),Fraction(3,4),Fraction(99,100)]:
        if n>p*x:
            short_points = p+(p-1)*sum(o<=p*x for o in orders)
            check(short_points == p*p-(p-1)*P, 'point_weighted_threshold_count')
    if p<=47:
        seen = set()
        direct_periods = {}
        for u in range(p):
            for v in range(p):
                if (u,v) in seen:
                    continue
                orbit = []
                current = (u,v)
                while current not in seen:
                    seen.add(current)
                    orbit.append(current)
                    current = (current[0],(current[0]**2+1)*current[1]%p)
                check(current==(u,v), 'direct_permutation_cycle_return')
                for point in orbit:
                    direct_periods[point] = len(orbit)
        check(len(direct_periods)==p*p, 'direct_all_point_coverage')
        for (u,v), period in direct_periods.items():
            check(period==(1 if v==0 else orders[u]), 'direct_period_vs_order')
    finite_rows.append({'p':p,'primitive_parameters':P,'theta':str(theta),
                        'cdf_on_stated_fixed_thresholds_eventually':str(Fraction(p*p-(p-1)*P,p*p))})

K = 1
odd_product = Fraction(1)
crt_rows = []
for q in primes(31)[1:]:
    K *= q
    odd_product *= Fraction(q-1,q)
    r = 1+K*((3-1)*pow(K,-1,4)%4)
    check(r%4==3 and r%K==1 and gcd(r,4*K)==1,'crt_reduced_class')
    crt_rows.append({'last_odd_prime':q,'Q':K,'modulus':4*K,'residue':r,
                     'theta_upper_bound':str(odd_product/2)})

check(Fraction(1,4)+Fraction(1,48)==Fraction(13,48), 'density_split_constant')
check(Fraction(7,24)==Fraction(14,48)>Fraction(13,48), 'strict_contradiction_constant')
check(Fraction(1,2)*(1-Fraction(5,12))==Fraction(7,24), 'euler_product_lower_constant')

output = {'passed':True,'generated_utc':datetime.now(timezone.utc).isoformat(),
          'runtime':{'executable':sys.executable,'version':sys.version,
                     'ignore_environment':sys.flags.ignore_environment,'dont_write_bytecode':sys.flags.dont_write_bytecode},
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'elapsed_seconds':time.perf_counter()-START,
          'control_counts':dict(sorted(COUNTS.items())), 'total_controls':sum(COUNTS.values()),
          'limitations':'Finite exact controls only. Infinite claims are proved in DERIVATION.md using credited unconditional arithmetic inputs.',
          'finite_rows':finite_rows,'crt_rows':crt_rows}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['finite_rows','crt_rows']},indent=2))
