#!/usr/bin/env python3
"""Independent audit controls. Does not import or edit author-packet code.

Represent Laurent monomials by triples modulo (1,1,1), with minimum zero;
construct H from its factorization; test reconstruction by Gaussian inversion
and direct finite-field Fourier sums. Exact arithmetic only.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, prod
from pathlib import Path
from random import Random
import hashlib
import json

checks = 0

def check(value):
    global checks
    assert value
    checks += 1

def canon(e):
    m = min(e)
    return tuple(x-m for x in e)

def poly(terms):
    result = defaultdict(Q)
    for e, c in terms:
        result[canon(e)] += c
    return {e:c for e,c in result.items() if c}

def add(*polys):
    return poly((e,c) for f in polys for e,c in f.items())

def scale(k, f):
    return poly((e,k*c) for e,c in f.items())

def mul(f,g):
    return poly((tuple(a+b for a,b in zip(e,t)),c*d)
                for e,c in f.items() for t,d in g.items())

def mon(e):
    return poly([(e,1)])

def inv(f):
    return poly((tuple(-a for a in e),c) for e,c in f.items())

ONE = mon((0,0,0))
X,Y,Z = [mon(e) for e in [(1,0,0),(0,1,0),(0,0,1)]]
aa = add(X,Y,Z)
bb = add(mul(X,Y),mul(X,Z),mul(Y,Z))
u,v = add(aa,bb),mul(aa,bb)
D = ONE
for variable in (X,Y,Z):
    d = add(variable,scale(-1,ONE))
    D = mul(D,mul(d,d))
H = scale(-1,mul(mul(D,add(u,scale(2,ONE))),add(v,scale(2,u),scale(-3,ONE))))
check(D == add(mul(u,u),scale(-4,v)))
check(H)
check(len(H) == 54)
check(H == inv(H))
for perm in permutations(range(3)):
    check(poly((tuple(e[i] for i in perm),c) for e,c in H.items()) == H)

def xy(f):
    return {(a-c,b-c):k for (a,b,c),k in f.items()}

coeff = xy(H)
check(coeff[(5,1)] == -1)
check(all(gcd(abs(a),abs(b)) == 1 for a,b in coeff))
check(sum(coeff.values()) == 0)
restriction = defaultdict(Q)
for (a,b),c in coeff.items():
    restriction[a] += c
check(not any(restriction.values()))
check(sum(c*Q(2)**a*Q(3)**b for (a,b),c in coeff.items()) == Q(-354725,162))

# Exact rational-denominator negative control on the fifth root grid.
# In Q[t,t^-1]/(t^5-1), (t+t^-1-1)^-1=t^2+t^-2-1.
delta_inv = ONE
for index in range(3):
    e = [0,0,0]
    e[index] = 2
    delta_inv = mul(delta_inv,add(mon(tuple(e)),inv(mon(tuple(e))),scale(-1,ONE)))
fifth_rational_residue = sum(c for (a,b),c in xy(mul(H,delta_inv)).items()
                            if a % 5 == 0 and b % 5 == 0)
check(fifth_rational_residue == 12)
fifth_polynomial_residue = sum(c for (a,b),c in coeff.items() if a % 5 == b % 5 == 0)
check(fifth_polynomial_residue == 0)

# Finite jet cancellation at non-consecutive dilation parameters.
jet_controls = [0,6,13,20,31]
for J in jet_controls:
    L = J//2+2
    ps = [j*j+1 for j in range(1,L+1)]
    weights = [Q(1,prod(p*p-q*q for q in ps if p != q)) for p in ps]
    check(len(set(ps)) == L)
    for degree in range(J+1):
        dilation_sum = sum(c*p**degree for p,c in zip(ps,weights))
        for i in range(degree+1):
            j = degree-i
            moment = sum(c*a**i*b**j for (a,b),c in coeff.items())
            check(moment*dilation_sum == 0)
    # Disjoint gcd shells give a nonzero polynomial, regardless of jet length.
    check(all(weights))
    check(len({(p*a,p*b) for p in ps for a,b in coeff}) == L*54)

# Recover arbitrary gcd-shell data by an independent downward recurrence.
rng = Random(10400067)
sample = {(a,b):rng.randrange(-7,8) for a in range(-18,19) for b in range(-18,19)}
shells = defaultdict(int)
for (a,b),c in sample.items():
    shells[gcd(abs(a),abs(b))] += c
residues = {n:sum(c for (a,b),c in sample.items() if a%n == b%n == 0)
            for n in range(1,40)}
check(residues[39] == shells[0])
recovered = {}
for d in range(18,0,-1):
    recovered[d] = residues[d]-residues[39]-sum(recovered[m] for m in range(2*d,19,d))
    check(recovered[d] == shells[d])

def matrix_inverse(a):
    n = len(a)
    aug = [[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k = next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[k] = aug[k],aug[j]
        q = aug[j][j]
        aug[j] = [x/q for x in aug[j]]
        for i in range(n):
            if i != j:
                q = aug[i][j]
                aug[i] = [x-q*y for x,y in zip(aug[i],aug[j])]
    check(all(aug[i][j] == (i==j) for i in range(n) for j in range(n)))
    return [row[n:] for row in aug]

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

reconstruction_bounds = list(range(6))
for d in reconstruction_bounds:
    nodes = list(range(-d,d+1))
    V = [[Q(a)**i for a in nodes] for i in range(2*d+1)]
    V_inv = matrix_inverse(V)
    # Full-square input, including points outside the theta hexagon.
    C = [[Q(rng.randrange(-29,30),rng.randrange(1,10)) for b in nodes] for a in nodes]
    M = mm(mm(V,C),list(zip(*V)))
    result = mm(mm(V_inv,M),list(zip(*V_inv)))
    for row,expected in zip(result,C):
        for x,y in zip(row,expected):
            check(x == y)

def is_prime(n):
    return n > 1 and all(n%a for a in range(2,int(n**0.5)+1))

fourier_controls = []
for d in [1,2,3,5]:
    N = 2*d+1
    q = next(k*N+1 for k in range(2,1000) if is_prime(k*N+1))
    root = next(t for t in range(2,q) if pow(t,N,q)==1 and
                all(pow(t,a,q)!=1 for a in range(1,N) if N%a==0))
    points = [pow(root,i,q) for i in range(N)]
    C = {(a,b):rng.randrange(-20,21) for a in range(-d,d+1) for b in range(-d,d+1)}
    F = {(x,y):sum(c*pow(x,a,q)*pow(y,b,q) for (a,b),c in C.items())%q
         for x in points for y in points}
    for (a,b),c in C.items():
        value = sum(pow(x,-a,q)*pow(y,-b,q)*v for (x,y),v in F.items())*pow(N*N,-1,q)%q
        check(value == c%q)
    fourier_controls.append({'d':d,'N':N,'field_prime':q})

# Boundary negative control: N=2d aliases x^d and x^-d exactly.
for d in range(1,9):
    N = 2*d
    check((d%N,0) == (-d%N,0))
    check(d != -d)

packet = Path(__file__).resolve().parents[1]/'packet'
manifest = packet/'AUTHOR_MANIFEST.json'
check(hashlib.sha256(manifest.read_bytes()).hexdigest() ==
      '11afc2553555cd72a0cb571a71c74d8dd2daa300ed1662d3bc74b4396353ee5c')
check(len(list(packet.iterdir())) == 18)
for filename in ['AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
    for path,digest in json.loads((packet/filename).read_text())['files'].items():
        check(hashlib.sha256((packet/path).read_bytes()).hexdigest() == digest)

print(json.dumps({'status':'PASS','exact_assertions':checks,'H_terms':len(H),
 'jet_degrees':jet_controls,'gaussian_reconstruction_bounds':reconstruction_bounds,
 'direct_finite_field_fourier_controls':fourier_controls,
 'denominator_negative_control':{'Delta':'t+t^-1-1','n':5,
                                'A_n(H)':0,'A_n(H/Delta_product)':str(fifth_rational_residue)},
 'scope':'Independent exact controls; no knot realizability or global comparison claim.'},indent=2))
