#!/usr/bin/env python3
"""Source-free exact controls, written before candidate/verifier access."""
from fractions import Fraction as F
from itertools import combinations, product, permutations
from math import comb
import sympy as S
EDGES=list(combinations(range(4),2))
CYCLE={tuple(sorted(e)) for e in [(0,1),(1,2),(2,3),(3,0)]}

def pattern_prob(masses, matrix, pattern):
    out=F(0)
    for tup in product(range(len(masses)), repeat=4):
        prob=F(1)
        for i in tup: prob*=masses[i]
        for i,j in EDGES:
            w=matrix[tup[i]][tup[j]]
            prob*= w if (i,j) in pattern else 1-w
        out+=prob
    return out

def unlabeled_prob(masses,matrix,degree_target):
    out=F(0)
    for mask in range(64):
        patt={e for z,e in enumerate(EDGES) if mask>>z&1}
        deg=sorted(sum(i in e for e in patt) for i in range(4))
        if deg==degree_target: out+=pattern_prob(masses,matrix,patt)
    return out

# All 64 graphs certify exactly three labeled C4s, and factor-three identity.
num_cycles=0
for mask in range(64):
    patt={e for z,e in enumerate(EDGES) if mask>>z&1}
    deg=sorted(sum(i in e for e in patt) for i in range(4))
    if deg==[2,2,2,2]: num_cycles+=1
assert num_cycles==3
print('normalization: 64 masks, exactly 3 labeled C4s')

# Rank-one expansion in the four latent variables, independent moment substitution.
x=S.symbols('x0:4'); a,b,m=S.symbols('a b m', nonnegative=True)
poly=S.prod(x[i]*x[j] for i,j in CYCLE)*S.prod(1-x[i]*x[j] for i,j in EDGES if (i,j) not in CYCLE)
expect=0
for exponents,coeff in S.Poly(S.expand(poly),*x).terms():
    expect+=coeff*S.prod({2:a,3:b}[z] for z in exponents)
assert S.expand(expect-(a*a-b*b)**2)==0
c=S.symbols('c', nonnegative=True)
assert S.factor((m*m/4)-(m*m*c*c*(1-c*c)))==m*m*(2*c*c-1)**2/4
print('rank-one symbolic identity and quadratic max certificate: PASS')

# Exact discrete latent laws (finite controls, not proof of measurable universality).
latent_grid=[F(i,4) for i in range(5)]
count=0
for weights in product(range(5),repeat=5):
    if sum(weights)!=4: continue
    mean=sum(F(w,4)*v for w,v in zip(weights,latent_grid))
    aa=sum(F(w,4)*v**2 for w,v in zip(weights,latent_grid))
    bb=sum(F(w,4)*v**3 for w,v in zip(weights,latent_grid))
    p=mean**2
    value=3*(aa**2-bb**2)**2
    bound=3*p**2/16 if p<=F(1,2) else 3*p**4*(1-p)**2
    assert value<=bound
    if mean: assert bb*mean>=aa**2
    count+=1
print('finite latent-law controls:',count,'PASS')

# Derivatives by literal six-factor product enumeration, for arbitrary rational masses.
for masses in [[F(2,3),F(1,3)],[F(2,5),F(2,5),F(1,5)],[F(2,7)]*3+[F(1,7)]]:
    n=len(masses); s2=sum(v*v for v in masses)
    for ii in range(n):
      for jj in range(ii,n):
        derivative=F(0)
        for tup in product(range(n),repeat=4):
          weight=F(1)
          for i in tup: weight*=masses[i]
          for edge in EDGES:
            u,v=edge
            if sorted([tup[u],tup[v]])!=[ii,jj]: continue
            term=weight*(1 if edge in CYCLE else -1)
            for e in EDGES:
              if e==edge: continue
              baseline=F(tup[e[0]]!=tup[e[1]])
              term*=baseline if e in CYCLE else 1-baseline
            derivative+=3*term
        mass=masses[ii]*masses[jj]*(1 if ii==jj else 2)
        coefficient=-6*(s2-masses[ii]**2) if ii==jj else 6*((masses[ii]+masses[jj])**2-s2)
        assert derivative==mass*coefficient,(masses,ii,jj,derivative,mass*coefficient)
print('multipartite derivative enumeration, n=2,3,4: PASS')
assert 3*sum(comb(6,r) for r in range(2,7))==171
print('uniform elementary remainder constant: 171')

# Interior dense exact tie with positive paw.
oldmass=[F(2,5),F(2,5),F(1,5)]
oldmat=[[F(i!=j) for j in range(3)] for i in range(3)]
newmass=[F(2,5),F(1,3),F(6,25),F(2,75)]
newmat=[[F(0) for j in range(4)] for i in range(4)]
for i,j in [(0,1),(0,2),(0,3),(1,2)]: newmat[i][j]=newmat[j][i]=F(1)
def density(masses, matrix): return sum(masses[i]*masses[j]*matrix[i][j] for i in range(len(masses)) for j in range(len(masses)))
po=density(oldmass,oldmat); pn=density(newmass,newmat)
co=3*pattern_prob(oldmass,oldmat,CYCLE); cn=3*pattern_prob(newmass,newmat,CYCLE)
paw=unlabeled_prob(newmass,newmat,[1,2,2,3])
assert po==pn==F(16,25)
assert co==cn==F(144,625)
assert paw==24*newmass[0]*newmass[1]*newmass[2]*newmass[3]==F(64,3125)
print('exact tying example: p=',po,' C4=',co,' paw=',paw)
print('ALL INDEPENDENT CONTROLS PASSED')
