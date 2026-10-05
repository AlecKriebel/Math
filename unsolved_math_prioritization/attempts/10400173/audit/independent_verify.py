#!/usr/bin/env python3
"""Independent integer-only Kirby-color audit in Z[w]/(1+w+...+w^6).

No import, parsing, or execution of the author's verifier or controls.
The embedding is w=exp(2*pi*i/7). All checks survive python -O.
"""
from itertools import product
from math import gcd
from fractions import Fraction
from collections import Counter
import json

ZERO=(0,)*6
ONE=(1,0,0,0,0,0)
def add(*args):
    return tuple(sum(a[j] for a in args) for j in range(6))
def scale(a,n): return tuple(n*x for x in a)
def monomial(n):
    n %= 7
    return tuple(int(j==n) for j in range(6)) if n<6 else (-1,)*6
def multiply(a,b):
    # Cyclic convolution modulo w^7=1, then use sum(w^i)=0.
    v=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b): v[(i+j)%7] += x*y
    return tuple(v[i]-v[6] for i in range(6))
def power(a,n):
    if n<0: raise ValueError('Only nonnegative powers')
    out=ONE
    for _ in range(n): out=multiply(out,a)
    return out
def conjugate(a): return add(*(scale(monomial(-j),x) for j,x in enumerate(a)))
def fmt(a): return list(a)
checks=[]
def require(condition,name):
    if not condition: raise RuntimeError(name)
    checks.append(name)

w=monomial(1)
require(add(*(monomial(j) for j in range(7)))==ZERO,'Phi7 relation')
require(power(w,7)==ONE and all(power(w,j)!=ONE for j in range(1,7)),'exact order seven')
# Phi7(x+1) is Eisenstein at 7; hence this quotient has characteristic-zero
# field of fractions Q(w), so equality of canonical coefficients is decisive.

d=[ONE,add(ONE,monomial(1),monomial(-1)),
   add(ONE,monomial(1),monomial(-1),monomial(2),monomial(-2))]
N=[[[1,0,0],[0,1,0],[0,0,1]],
   [[0,1,0],[1,1,1],[0,1,1]],
   [[0,0,1],[0,1,1],[1,1,0]]]
exponents=[0,2,6]
delta=add(*(power(a,2) for a in d))
for i in range(3):
    require(conjugate(d[i])==d[i],f'real dimension {i}')
    for j in range(3):
        require(multiply(d[i],d[j])==add(*(scale(d[k],N[i][j][k]) for k in range(3))),f'fusion dimensions {i},{j}')
# Derive the unnormalized Hopf pairing from the ribbon balancing identity.
H=[[add(*(scale(multiply(d[k],monomial(exponents[k]-exponents[i]-exponents[j])),N[i][j][k]) for k in range(3))) for j in range(3)] for i in range(3)]
expected=[[ONE,d[1],d[2]],[d[1],scale(d[2],-1),ONE],[d[2],ONE,scale(d[1],-1)]]
require(H==expected,'derived Hopf matrix')
for i,j in product(range(3),repeat=2):
    require(add(*(multiply(H[i][k],H[k][j]) for k in range(3)))==(delta if i==j else ZERO),f'H squared {i},{j}')
# No square root or trigonometric evaluation enters these computations.
tau=add(*(multiply(power(d[i],2),monomial(exponents[i])) for i in range(3)))
require(multiply(tau,conjugate(tau))==delta,'unit modulus anomaly after dividing by sqrt(delta)')
require(power(tau,2)==multiply(delta,monomial(2)),'squared anomaly matches w')

def numerator(cf,reverse=False):
    # Vacuum entry of H T^a1 H ... T^an H, by sum over simple colors.
    # RT differs by delta^(-(n+1)/2) and a phase. Thus TV denominator
    # is delta^(n+1), and numerator is A times its conjugate.
    sign=-1 if reverse else 1
    if not cf: return ONE
    total=ZERO
    for labels in product(range(3),repeat=len(cf)):
        term=multiply(d[labels[0]],d[labels[-1]])
        phase=sum(cf[j]*exponents[labels[j]] for j in range(len(cf)))
        term=multiply(term,monomial(sign*phase))
        for j in range(len(cf)-1):
            term=multiply(term,H[labels[j]][labels[j+1]])
        total=add(total,term)
    return total

def negcf(p,q):
    terms=[]
    while q:
        a=-(-p//q)
        terms.append(a)
        p,q=q,a*q-p
    return terms

def decode(cf):
    r=Fraction(cf[-1])
    for a in reversed(cf[:-1]): r=a-1/r
    return r

lens=[]
for q in range(1,7):
    cf=negcf(7,q)
    require(decode(cf)==Fraction(7,q),f'continued fraction 7/{q}')
    a=numerator(cf)
    numerator_tv=multiply(a,conjugate(a))
    denominator_tv=power(delta,len(cf)+1)
    val=1 if q in (1,6) else 0
    require(numerator_tv==scale(denominator_tv,val),f'TV L(7,{q})')
    require(numerator(cf,True)==conjugate(a),f'reversed braiding L(7,{q})')
    lens.append({'p':7,'q':q,'negative_continued_fraction':cf,'TV':val})
require(numerator([7])==delta,'one-component Kirby sum equals global dimension')
require(numerator([4,2])==ZERO,'two-component Kirby sum vanishes exactly')
require(numerator([5,1,3])==ZERO,'Kirby blowup preserves target vanishing')
require(multiply(numerator([1]),conjugate(numerator([1])))==delta,'S3 value 1/delta')
require(numerator([0])==delta,'S2 times S1 value one')
require(H[0][1]!=ZERO,'identity twists cannot make H scalar')
# Coefficient denominator is nonzero: physical dimensions are positive because
# sin(pi/7), sin(3pi/7), sin(5pi/7)>0. Independent exact algebra also shows delta!=0.
require(delta!=ZERO,'global dimension nonzero')
# One-dimensional surgery slope check, using the integral generators.
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
s=[[0,-1],[1,0]]
def gluing(cf):
    out=s
    for a in cf: out=mm(mm(out,[[1,a],[0,1]]),s)
    return out
require(gluing([7])==[[-1,0],[7,-1]],'integral target slope 7/1')
require(gluing([4,2])==[[-2,1],[7,-4]],'integral target slope 7/2')

# Cyclic cocycle independently simplified. Let a=2r and n=q^-1 mod 7.
# The carry sum is sum_{j=1}^6 floor(((aj mod14)+(an mod14))/14).
# Retain residues in Z/7 rather than Fraction phases.
def cyclic(q,k):
    n=pow(q,-1,7)
    hist=Counter()
    for r in range(7):
        a=2*r
        carries=sum(((a*j)%14+(a*n)%14)//14 for j in range(1,7))
        hist[(k*r*carries)%7]+=1
    return hist
require(cyclic(1,1)==Counter({0:1,1:2,2:2,4:2}),'cyclic carry histogram')
for k in range(14):require(cyclic(1,k)==cyclic(2,k),f'cyclic cocycle power {k}')
require((3*3)%7==2,'oriented homotopy residue')
require(2 not in {1,6},'target q outside homeomorphism orbit of one')

# Sokolov 1997 formula (*) specialized independently at p=r=7.
# d=gcd(p,2r)=7, c=2pr/d^2=2, so TV=d/(2r) iff q=+/-1 mod d.
def sokolov_target(q):
    p=r=7
    g=gcd(p,2*r)
    c=2*p*r//(g*g)
    require(g==7 and c==2, f'Sokolov specialization q={q}')
    return Fraction(g,2*r) if q%g in (1,g-1) else Fraction(0)
require(sokolov_target(1)==Fraction(1,2),'Sokolov L71 value one-half')
require(sokolov_target(2)==0,'Sokolov L72 value zero')
# Full SU(2)_5 = even sector times the rank-two semion sector.
# The semion generator (label 5) has theta=i. The Kirby numerators are
# 1-i for [7], and 2 for [4,2], with squared denominators 2^2 and 2^3.
semion71=Fraction(1**2+(-1)**2,2**2)
semion72=Fraction(2**2,2**3)
require(semion71==semion72==Fraction(1,2),'semion normalization bridge')
require(sokolov_target(1)==semion71*1 and sokolov_target(2)==semion72*0,'full/even TV target consistency')

A=[[1,25],[4,101]]; B=[[1,1],[100,101]]
require(A[0][0]*A[1][1]-A[0][1]*A[1][0]==1,'Funar det A')
require(B[0][0]*B[1][1]-B[0][1]*B[1][0]==1,'Funar det B')
require(5%4==1 and (-4)%5==1 and 4%4==0,'Funar hypotheses k=1 q=5 v=4')
# Record theorem dependency rather than falsely generalizing a bounded search.
output={'problem_id':10400173,'independent':True,'arithmetic':'Integer coefficients in Z[w]/Phi7; no floating point or author-code imports',
 'checks_passed':len(checks),'checks':checks,'global_dimension_coefficients':fmt(delta),
 'hopf_pairing_coefficients':[[fmt(x) for x in row] for row in H],
 'kirby_numerator_L71':fmt(numerator([7])),'kirby_numerator_L72':fmt(numerator([4,2])),
 'lens_values':lens,'sokolov_full_su2_values':{'L71':'1/2','L72':'0'},'all_moduli_and_nonhomeomorphism':'Imported Funar Theorem 1.1; not asserted by finite checks',
 'verdict':'PASS mathematical lens calculation; whole problem remains unsolved'}
print(json.dumps(output,indent=2,sort_keys=True))
