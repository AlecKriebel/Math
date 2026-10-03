#!/usr/bin/env python3
"""Independent exact diagnostics for the credited Berkovich--Garvan theorem.

Uses hook-length enumeration and logarithmic-derivative recurrences, rather
than the author's repeated multiplication/division verifier. No external
packages. Finite diagnostics supplement the source/proof audit.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
import json

checks = Counter()
def require(value, category):
    assert value, category
    checks[category] += 1

def primes(n):
    result = []
    for p in range(2, n + 1):
        if n % p == 0:
            result.append(p)
            while n % p == 0:
                n //= p
        if n == 1:
            break
    return result

def mobius(n):
    ps = primes(n)
    return 0 if any(n % (p*p) == 0 for p in ps) else (-1)**len(ps)

def totient(n):
    return sum(gcd(n,k) == 1 for k in range(1,n+1))

def coefficients(exponents):
    """F=prod(1-q^k)^e_k; n F_n=-sum_{j=1}^n b_j F_{n-j}."""
    H = len(exponents)-1
    b = [0]*(H+1)
    for k in range(1,H+1):
        for j in range(k,H+1,k):
            b[j] += k*exponents[k]
    out = [1]
    for n in range(1,H+1):
        numerator = -sum(b[j]*out[n-j] for j in range(1,n+1))
        require(numerator % n == 0, 'integral_recurrence')
        out.append(numerator//n)
    return out

def convolve(a,b):
    H = min(len(a),len(b))-1
    return [sum(a[j]*b[n-j] for j in range(n+1)) for n in range(H+1)]

def target_exponents(N,H):
    phi = totient(N)
    return [0]+[phi*int(k%N == 0)-int(gcd(k,N) == 1) for k in range(1,H+1)]

def core_exponents(t,H):
    return [0]+[t*int(k%t == 0)-1 for k in range(1,H+1)]

def partitions(n, maximum=None):
    if n == 0:
        yield ()
        return
    if maximum is None:
        maximum = n
    for first in range(min(n,maximum),1-1,-1):
        for rest in partitions(n-first,first):
            yield (first,)+rest

def hooks(lam):
    return {lam[i]-j + sum(row>j for row in lam[i+1:])
            for i in range(len(lam)) for j in range(lam[i])}

def summand(a,i,k):
    return a*k*(k-1)//2+i*k

def Q(n):
    a = len(n)
    assert sum(n) == 0
    return sum(summand(a,i,k) for i,k in enumerate(n))

def lattice(a,H):
    # Each summand is nonnegative. For |k|>=2 it is at least |k|;
    # hence every vector with Q<=H lies in these finite coordinate ranges.
    allowed = [[(k,summand(a,i,k)) for k in range(-H-2,H+3)
                if summand(a,i,k)<=H] for i in range(a)]
    def generate(prefix, budget):
        i = len(prefix)
        if i == a-1:
            k = -sum(prefix)
            if summand(a,i,k) <= budget:
                yield prefix+(k,)
        else:
            for k,cost in allowed[i]:
                if cost <= budget:
                    yield from generate(prefix+(k,),budget-cost)
    yield from generate((),H)

def transform(n,j):
    m = list(n[1:]+n[:1])
    if j:
        m[j-1] += 1
        m[-1] -= 1
    return tuple(m)

def theta_exponents(a,M,r,H):
    # The two bracket progressions are counted WITH multiplicity, including
    # the coincident progressions at M=2r. No boolean membership shortcut.
    return [0]+[int(k%M == 0)+(a-2)*int(k%(a*M) == 0)
                +int((k-a*r)%(a*M) == 0)
                +int((k-a*(M-r))%(a*M) == 0)
                -int((k-r)%M == 0)-int((k-(M-r))%M == 0)
                for k in range(1,H+1)]

# Direct partition counts independently check both positive core identities.
Hcore = 24
cores = {t:[0]*(Hcore+1) for t in range(1,9)}
partition_count = 0
for n in range(Hcore+1):
    for lam in partitions(n):
        partition_count += 1
        hs = hooks(lam)
        for t in cores:
            if all(h%t for h in hs):
                cores[t][n] += 1
for t, counts in cores.items():
    require(counts == coefficients(core_exponents(t,Hcore)), 'hook_core_identity')
    if t >= 2:
        theta = [0]*(Hcore+1)
        for n in lattice(t,Hcore):
            theta[Q(n)] += 1
        require(theta == counts, 'core_lattice_identity')
require(cores[1] == [1]+[0]*Hcore, 'boundary_cases')
require(cores[2][2] == 0 and cores[2][3] == 1, 'boundary_cases')

# Möbius and q-shift controls, including nonsquarefree composite integers.
H = 80
case_counts = Counter()
Ns = list(range(1,241))+[252,315,360,420,504,630,840,900,945,1260]
for N in Ns:
    ds = [d for d in range(1,N+1) if N%d == 0]
    phi = totient(N)
    direct = [0]+[phi*int(k%N == 0)-sum(mobius(d) for d in ds if k%d == 0)
                  for k in range(1,H+1)]
    require(direct == target_exponents(N,H), 'mobius_exponents')
    A = Fraction(N*phi-sum(d*mobius(d) for d in ds),24)
    radical_product = 1
    for p in primes(N):
        radical_product *= 1-p
    require(A == Fraction(N*phi-radical_product,24), 'normalization')
    require(A>=0, 'normalization')
    if N == 1:
        require(coefficients(direct) == [1]+[0]*H, 'boundary_cases')
        continue
    p = 2 if N%2 == 0 else primes(N)[-1]
    M,t = N,1
    alpha = 0
    while M%p == 0:
        M //= p
        alpha += 1
    t = p**(alpha-1)
    Np = p*M
    require(M%2 == 1 and gcd(p,M) == 1, 'complete_parameter_split')
    require(t*totient(Np) == phi, 'prime_power_lifting')
    lifted = [0]+[target_exponents(Np,H)[k]
        +totient(Np)*(t*int(k%N == 0)-int(k%Np == 0)) for k in range(1,H+1)]
    require(lifted == direct, 'prime_power_lifting')
    if M == 1:
        case_counts['prime_power'] += 1
        require(target_exponents(p,H) == core_exponents(p,H), 'prime_base')
    else:
        case_counts['coprime_p_times_odd_M' if alpha == 1 else 'higher_power_times_odd_M'] += 1
        representatives = [r for r in range(1,M) if 2*r<M and gcd(r,M)==1]
        residues = sorted([r for r in representatives]+[M-r for r in representatives])
        require(residues == [r for r in range(1,M) if gcd(r,M)==1], 'residue_pairing')
        paired = [0]*(H+1)
        for r in representatives:
            for k in range(1,H+1):
                paired[k] += ((2*p-2)*int(k%Np == 0)
                    +int((k-p*r)%Np == 0)+int((k-p*(M-r))%Np == 0)
                    -int((k-r)%M == 0)-int((k-(M-r))%M == 0))
        require(paired == target_exponents(Np,H), 'paired_D_factorization')
    if N <= 80:
        require(min(coefficients(direct)) >= 0, 'normalized_coefficients')

# Explicit fractional q-shifts prevent unnoticed integral-power assumptions.
for N,expected in [(1,Fraction(0)),(2,Fraction(1,8)),(3,Fraction(1,3)),(4,Fraction(3,8))]:
    ds = [d for d in range(1,N+1) if N%d == 0]
    actual = Fraction(N*totient(N)-sum(d*mobius(d) for d in ds),24)
    require(actual == expected, 'fractional_shift_examples')
    if N in (2,3):
        require(actual != Fraction(N*N-1,12), 'negative_controls')

# All j, zero coordinates, negative coordinates and affine lattice maps.
vector_count = 0
for a in range(2,9):
    for n in lattice(a,12):
        vector_count += 1
        for j in range(a):
            nn = transform(n,j)
            require(sum(nn)==0 and Q(nn)-Q(n)==a*n[j]+j, 'affine_theta_shift')
            for M,r in [(2,1),(4,3),(7,1),(7,6)]:
                e = M*Q(n)+r*(a*n[j]+j)
                require(e == (M-r)*Q(n)+r*Q(nn) and e>=0, 'specialization_nonnegativity')

# Exact theta identities with rigorous finite bounds, including M=2r and
# composite a. Compare independent lattice enumeration with log recurrence.
theta_cases = [(2,2,1),(2,4,3),(3,2,1),(3,7,6),(4,3,1),
               (4,4,2),(5,3,2),(6,5,1),(6,5,4)]
Htheta = 32
for a,M,r in theta_cases:
    theta = [0]*(Htheta+1)
    for n in lattice(a,Htheta//(M-r)):
        for j in range(a):
            e = M*Q(n)+r*(a*n[j]+j)
            require(e>=0, 'theta_enumeration_nonnegative')
            if e<=Htheta:
                theta[e] += 1
    exponents = theta_exponents(a,M,r,Htheta)
    require(theta == coefficients(exponents), 'specialized_theta_identity')
    d_exponents = [exponents[k]+a*int(k%(a*M)==0)-int(k%M==0)
                   for k in range(Htheta+1)]
    d_exponents[0] = 0
    base = [0]+[a*int(k%(a*M)==0)-int(k%M==0) for k in range(1,Htheta+1)]
    require(coefficients(d_exponents) == convolve(theta,coefficients(base)), 'D_product_identity')
    require(min(coefficients(d_exponents))>=0, 'D_nonnegativity')

# Controls that fail if the bracket ratio or crucial odd-M assumption is lost.
correct = theta_exponents(3,5,2,Htheta)
wrong = [0]+[int(k%5==0)+int(k%15==0)
    -int((k-6)%15==0)-int((k-9)%15==0)
    +int((k-2)%5==0)+int((k-3)%5==0) for k in range(1,Htheta+1)]
require(coefficients(correct) != coefficients(wrong), 'negative_controls')
require(2*len([r for r in range(1,2) if 2*r<2 and gcd(r,2)==1]) != totient(2), 'negative_controls')
require(target_exponents(6,H) != target_exponents(3,H), 'negative_controls')

result = {
 'status':'PASS', 'assertions':sum(checks.values()), 'checks_by_category':dict(sorted(checks.items())),
 'partitions_enumerated':partition_count, 'core_partition_degree':Hcore,
 'core_parameters':list(cores), 'normalized_product_degree':H,
 'factorization_parameters':Ns, 'case_counts':dict(case_counts),
 'affine_shift_lattice_vectors':vector_count, 'theta_degree':Htheta,
 'theta_cases':[{'a':a,'M':M,'r':r} for a,M,r in theta_cases],
 'method':'Hook-length enumeration, exhaustive bounded lattice sums, logarithmic-derivative coefficient recurrences and integer exponent identities; standard library only.',
 'limitation':'Bounded exact diagnostics. The all-parameter result follows from the audited, credited core/theta identities and general factorization.'
}
print(json.dumps(result,indent=2,sort_keys=True))
