#!/usr/bin/env python3
"""Exact, dependency-free controls; no network or source corpora are required."""
from fractions import Fraction as F
from collections import Counter
from functools import reduce
from math import gcd
import json

# Q[z]/Phi_28(z), z embedded as exp(2*pi*i/28).
PHI = [1,0,-1,0,1,0,-1,0,1,0,-1,0,1]
D = 12

def elt(a):
    if isinstance(a, (int, F)): a = [a]
    a = list(map(F, a))
    a += [F(0)] * max(0, D-len(a))
    for n in range(len(a)-1, D-1, -1):
        c = a[n]
        if c:
            for j in range(D+1): a[n-D+j] -= c*PHI[j]
    return tuple(a[:D])

ZERO, ONE = elt(0), elt(1)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,c): return tuple(x*c for x in a)
def mul(a,b):
    c = [F(0)]*(2*D-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    return elt(c)
def power(a,n):
    if n < 0: raise ValueError('Negative power is not implemented')
    b = ONE
    while n:
        if n & 1: b = mul(b,a)
        a = mul(a,a); n //= 2
    return b
def z(n): return elt([0]*(n%28)+[1])
def conj(a):
    out = ZERO
    for n,c in enumerate(a): out = add(out,scale(z(-n),c))
    return out
def fmt(a): return {str(i):str(c) for i,c in enumerate(a) if c}
def eye(n): return [[ONE if r==c else ZERO for c in range(n)] for r in range(n)]
def mm(a,b):
    return [[reduce(add,(mul(a[r][k],b[k][c]) for k in range(len(b))),ZERO)
             for c in range(len(b[0]))] for r in range(len(a))]
def mp(a,n):
    b=eye(len(a))
    for _ in range(n): b=mm(b,a)
    return b

def check(c,msg):
    global checks
    checks += 1
    if not c: raise RuntimeError(msg)
checks=0

# Positive sqrt(7) is the classical quadratic Gauss sum divided by i.
i=z(7)
g=mul(neg(i),reduce(add,(scale(z(4*a),1 if a in (1,2,4) else -1) for a in range(1,7)),ZERO))
check(power(z(1),28)==ONE,'primitive-root relation')
check(power(z(1),14)==neg(ONE),'half-period')
check(mul(g,g)==elt(7),'sqrt(7) identity')
check(conj(g)==g,'sqrt(7) is real')
S=[[scale(mul(mul(neg(g),i),sub(z(2*a*b),z(-2*a*b))),F(1,7)) for b in (1,3,5)] for a in (1,3,5)]
T=[[z(t) if r==c else ZERO for c in range(3)] for r,t in enumerate((0,8,24))]
check(mm(S,S)==eye(3),'S squared')
check(all(conj(x)==x for row in S for x in row),'S is real')
check(mp(T,7)==eye(3),'T has order dividing seven')
check(mp(mm(S,T),3)==[[z(4) if r==c else ZERO for c in range(3)] for r in range(3)],'modular relation')

# Known SU(2)_5 even fusion rules on labels 0,2,4.
N=[[[1,0,0],[0,1,0],[0,0,1]],
   [[0,1,0],[1,1,1],[0,1,1]],
   [[0,0,1],[0,1,1],[1,1,0]]]
for a in range(3):
    for r in range(3):
        for col in range(3):
            lhs=mul(reduce(add,(scale(S[j][col],N[a][r][j]) for j in range(3)),ZERO),S[0][col])
            rhs=mul(S[r][col],S[a][col])
            check(lhs==rhs,'division-free Verlinde check')

# Ribbon balancing recovers S from the actual fusion rules, twists and dimensions.
for a in range(3):
    for b in range(3):
        lhs=mul(S[a][b],mul(T[a][a],T[b][b]))
        rhs=reduce(add,(scale(mul(T[c][c],S[0][c]),N[a][b][c]) for c in range(3)),ZERO)
        check(lhs==rhs,'ribbon balancing identity')

A=mm(mm(S,mp(T,7)),S)
B=mm(mm(mm(mm(S,mp(T,4)),S),mp(T,2)),S)
expectedB=[[ZERO,ZERO,z(6)],[neg(z(4)),ZERO,ZERO],[ZERO,ONE,ZERO]]
check(A==eye(3),'L(7,1) matrix')
check(B==expectedB,'L(7,2) exact matrix')
check(mul(A[0][0],conj(A[0][0]))==ONE,'first squared amplitude')
check(mul(B[0][0],conj(B[0][0]))==ZERO,'second squared amplitude')

def word(cf,s=S,t=T):
    a=s
    for c in cf: a=mm(mm(a,mp(t,c)),s)
    return a

def tv(cf,s=S,t=T):
    a=word(cf,s,t)[0][0]
    return mul(a,conj(a))

def negcf(p,q):
    out=[]
    while q:
        a=(p+q-1)//q;out.append(a);p,q=q,a*q-p
    return out
lens=[]
for q in range(1,7):
    cf=negcf(7,q);v=tv(cf)
    expected=ONE if q in (1,6) else ZERO
    check(v==expected,'all orientations and inverse-q controls')
    lens.append({'p':7,'q':q,'negative_continued_fraction':cf,'tv':1 if v==ONE else 0})
check(tv([1])==mul(S[0][0],S[0][0]),'S3 normalization')
check(tv([0])==ONE,'S2 times S1 normalization')
check(tv([4,2])==tv([5,1,3]),'continued-fraction blowup invariance')
Tc=[[conj(x) for x in row] for row in T]
check(tv([7],S,Tc)==ONE and tv([4,2],S,Tc)==ZERO,'opposite braiding control')
check(tv([7],S,eye(3))==ONE and tv([4,2],S,eye(3))==mul(S[0][0],S[0][0]),'identity-twist negative control is not falsely modular')
# Identity twists fail the requisite modular relation; they are not alternate category data.
check(mp(S,3)!=eye(3),'identity twists rejected by modular relation')

# The proposed cyclic order-14 cocycle test, evaluated solely as rational phases.
def phases(q,k=1):
    n=pow(q,-1,7);out=Counter()
    for a in range(14):
        if (7*a)%14:continue
        phase=sum((F(k*a*((a*j)%14+(a*n)%14-((a*j+a*n)%14)),196) for j in range(1,7)),F(0))%1
        out[phase]+=1
    return out
hist=phases(1)
check(hist==Counter({F(0):1,F(1,7):2,F(2,7):2,F(4,7):2}),'cyclic phase histogram')
for k in range(14): check(phases(1,k)==phases(2,k),'cyclic twists do not separate')
for q in (1,2,4):check(phases(q)==hist,'quadratic-residue reindexing')
check(phases(3)!=hist,'nonresidue phase histogram negative control')

# Funar Theorem 1.1 specialization: k=1, q=5, v=4.
FA=((1,25),(4,101));FB=((1,1),(100,101))
def det(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def im(A,B):return tuple(tuple(sum(A[r][j]*B[j][c] for j in range(2)) for c in range(2)) for r in range(2))
check(det(FA)==det(FB)==1,'Funar determinants')
check(FA[0][0]+FA[1][1]==102 and FB[0][0]+FB[1][1]==102,'Funar hyperbolic trace')
check((-4)%5 in {a*a%5 for a in range(1,5)} and 4%4==0,'Funar exact parameter hypotheses')
# Find an SL2 conjugator using the two linear equations. This finite check does not
# replace the theorem guaranteeing all moduli and integral non-conjugacy.
witnesses=[]
for m in range(2,101):
    C=None
    for x in range(m):
        for y in range(m):
            for w in range(m):
                if (25*w-x-100*y)%m:continue
                c=((x,y),(4*y%m,w))
                if det(c)%m==1:
                    C=c;break
            if C:break
        if C:break
    check(C is not None,'finite congruence witness exists')
    AC,CB=im(FA,C),im(C,FB)
    check(all((AC[r][c]-CB[r][c])%m==0 for r in range(2) for c in range(2)),'finite conjugacy identity')
    witnesses.append({'modulus':m,'conjugator':C})

# Check tensor-factorization at the matrix level for this actual category.
def tensor(A,B):
    return [[mul(A[r//len(B)][c//len(B)],B[r%len(B)][c%len(B)])
             for c in range(len(A)*len(B))] for r in range(len(A)*len(B))]
SS, TT=tensor(S,S),tensor(T,T)
for cf in ([7],[4,2],[3,2,2]):
    check(tv(cf,SS,TT)==mul(tv(cf),tv(cf)),'Deligne tensor-product amplitude control')

output={'problem_id':10400173,'checks_passed':checks,'arithmetic':'Exact fractions in Q[z]/Phi_28 plus exact integers',
        'scope':'Algebraic controls for the stated modular data and published-theorem parameter specialization; no proof of novelty or full bundled resolution.',
        'a6_lens_values':lens,'a6_B_matrix':[[fmt(x) for x in row] for row in B],
        'cyclic_14_phase_histogram':{str(x):hist[x] for x in sorted(hist)},
        'funar_A':FA,'funar_B':FB,'funar_finite_congruence_moduli':list(range(2,101)),
        'all_moduli_and_nonhomeomorphism_source':'Funar 2013, Theorem 1.1; not established by finite controls',
        'status':'unsolved','turns_used':5}
print(json.dumps(output,indent=2,sort_keys=True))
