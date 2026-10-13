#!/usr/bin/env python3
"""Independent A4 HT Theorem 5.1 exact lattice-character computation.

No modular S/T matrices, integrable-weight loops, author code, or libraries.
Ring elements are integer coefficient vectors modulo Phi_50.
"""
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import cmath
import json
import math
import sys

N = 50
D = 20
RHO = (2, 1, 0, -1, -2)

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def reduce(poly):
    a = list(poly) + [0] * max(0, D-len(poly))
    for j in range(len(a)-1, D-1, -1):
        c = a[j]
        if c:
            a[j] = 0
            # Phi_50 = x^20-x^15+x^10-x^5+1.
            a[j-5] += c
            a[j-10] -= c
            a[j-15] += c
            a[j-20] -= c
    return tuple(a[:D])

ZERO = (0,) * D
ONE = (1,) + (0,) * (D-1)

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def scale(a,n):
    return tuple(n*x for x in a)

def mul(a,b):
    c=[0]*(2*D-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return reduce(c)

def z(e):
    p=[0]*(e%N+1)
    p[e%N]=1
    return reduce(p)

def conj(a):
    r=ZERO
    for j,c in enumerate(a):
        r=add(r,scale(z(-j),c))
    return r

def norm(a):
    return mul(a,conj(a))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def parity(p):
    return (-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))

WEYL=[]
for p in permutations(range(5)):
    w=tuple(RHO[j] for j in p)
    WEYL.append((p,w,parity(p),dot(RHO,w)))

def lattice_point(a):
    return (a[0],a[1]-a[0],a[2]-a[1],a[3]-a[2],-a[3])

LATTICE=[lattice_point(a) for a in product(range(5),repeat=4)]
check(len(set(LATTICE))==625,'quotient representative duplication')
check(all(sum(v)==0 and dot(v,v)%2==0 for v in LATTICE),'A4 lattice failure')

def character(v):
    # exp(2 pi i <nu,v>/5) = z^(10 <nu,v>).
    counts=Counter(dot(nu,v)%5 for nu in LATTICE)
    r=ZERO
    for e,c in counts.items():
        r=add(r,scale(z(10*e),c))
    return r,dict(sorted(counts.items()))

def gauss(q):
    F=ZERO
    B=ZERO
    surviving=[]
    for p,w,s,d in WEYL:
        v=tuple(q*a-b for a,b in zip(RHO,w))
        ch,counts=character(v)
        trivial=all((v[j]-v[4])%5==0 for j in range(4))
        check(ch==scale(ONE,625 if trivial else 0),'character orthogonality failure')
        F=add(F,scale(mul(z(-d),ch),s))
        if trivial:
            B=add(B,scale(z(-d),s))
            surviving.append(dict(permutation=p,w_rho=w,sign=s,rho_dot_w_rho=d,character_counts=counts))
    check(len(surviving)==5,'not five surviving permutations')
    check(F==scale(B,625),'collapsed versus full lattice sum mismatch')
    return F,B,surviving

def dedekind(q,p):
    check(p>0,'Dedekind denominator must be positive here')
    def saw(n):
        r=n%p
        return Fraction(r,p)-Fraction(1,2) if r else Fraction(0)
    return sum((saw(n)*saw(q*n) for n in range(1,p)),Fraction(0))

def eval_complex(a):
    root=cmath.exp(2j*math.pi/50)
    return sum(c*root**j for j,c in enumerate(a))

def sparse(a):
    return {str(j):c for j,c in enumerate(a) if c}

if '--false-guard' in sys.argv:
    check(False,'deliberate false guard must fail even under Python -O')

check(z(50)==ONE,'root order identity')
check(add(add(z(0),z(20)),add(z(40),add(z(10),z(30))))==ZERO,'Phi5 subgroup identity')
SQRT5=add(ONE,scale(add(z(10),z(-10)),2))
check(mul(SQRT5,SQRT5)==scale(ONE,5),'sqrt5 identity')
# Positive real embedding is proved in INDEPENDENT_DERIVATION.md from
# sqrt5=1+4*cos(72 degrees)>0. This float is a diagnostic only.
embedding_diagnostic=eval_complex(SQRT5).real

# p=1, nu=0, and phase S(q/1)=0: HT numerator is A.
A=ZERO
for p,w,s,d in WEYL:
    A=add(A,scale(z(-5*d),s))
A2=norm(A)
check(A2!=ZERO,'S3 denominator zero')

results={}
for q in [1,2,3,4,6,7,-1,-2]:
    F,B,surviving=gauss(q)
    S=12*dedekind(q,5)
    phase_exponent=25*S # exp(pi i S) = z^(25 S).
    check(phase_exponent.denominator==1,'phase not integral power of z50')
    phase=z(int(phase_exponent))
    expected=add(scale(ONE,3475 if q%5 in [1,4] else 4025),scale(SQRT5,1550 if q%5 in [1,4] else 1800))
    check(scale(norm(B),625)==mul(expected,A2),'exact normalized magnitude target failed')
    amplitude=25*eval_complex(mul(phase,B))/eval_complex(A)
    # This numerical value is diagnostic, not an exact proof step.
    results[str(q)]=dict(F=sparse(F),B=sparse(B),B_norm=sparse(norm(B)),survivors=surviving,dedekind_symbol=str(S),phase_exponent=int(phase_exponent),phase_times_B=sparse(mul(phase,B)),normalized_squared_magnitude=sparse(expected),numerical_amplitude=[amplitude.real,amplitude.imag],numerical_squared_magnitude=abs(amplitude)**2)

for q,inv in [(1,1),(2,3),(3,2),(4,4)]:
    check(results[str(q)]['B_norm']==results[str(inv)]['B_norm'],'inverse q magnitude failure')
for q in [1,2]:
    F,B,_=gauss(q)
    Fm,Bm,_=gauss(-q)
    # w0 reverses rho, det(w0)=(-1)^10=+1; exact reversal.
    check(Bm==conj(B),'orientation numerator conjugation failure')
    e=int(25*12*dedekind(q,5))
    em=int(25*12*dedekind(-q,5))
    check(mul(z(em),Bm)==conj(mul(z(e),B)),'complete orientation phase conjugation failure')

print(json.dumps(dict(mechanism='HT Th5.1 A4 lattice character orthogonality',ring='Z[z]/(z^20-z^15+z^10-z^5+1), z=exp(2pi i/50)',rho=RHO,rank=4,positive_roots=10,rho_squared=dot(RHO,RHO),covolume_squared=5,quotient_size=625,A=sparse(A),A_norm=sparse(A2),sqrt5=sparse(SQRT5),sqrt5_embedding_numerical_diagnostic=embedding_diagnostic,results=results,exact_checks='all passed',s3_boundary='p=1: F=A, |p|^4=1, Dedekind phase=1, ratio=1',numerical_controls='ordinary double precision diagnostic only'),indent=2))
