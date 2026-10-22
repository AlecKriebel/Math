#!/usr/bin/env python3
"""Exact fixed-certificate checks; no optimizer or symbolic package required."""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1

P=[(-4,2),(-3,-1),(-2,-4),(-1,3),(1,-3),(2,4),(3,1),(4,-2)]
N=[(-4,1),(-3,-2),(-2,3),(-1,-4),(1,4),(2,-3),(3,2),(4,-1)]
forms=[(1,0),(0,1),(2,1),(-1,2)]

def linear(a,p):return a[0]*p[0]+a[1]*p[1]
def uv(p):return linear((1,-3),p),linear((3,1),p)
def phi(p):
 u,v=uv(p);return u**8+v**8+u*u+v*v

ck(len(set(P))==8);ck(len(set(N))==8);ck(not set(P)&set(N))
expected=[[-4,-3,-2,-1,1,2,3,4]]*2+[[-8,-7,-6,-1,1,6,7,8]]*2
marginals=[]
for f,target in zip(forms,expected):
 pp=sorted(linear(f,p) for p in P);nn=sorted(linear(f,p) for p in N)
 ck(pp==target);ck(nn==target);ck(Counter(pp)==Counter(nn));marginals.append(pp)
for p in P:ck(max(map(abs,uv(p)))<=10)
for p in N:ck(max(map(abs,uv(p)))==11)
ck(set(map(phi,P))=={100000100,200000200})
ck(set(map(phi,N))=={214365572,220123852})
T=210000000
for p in P:ck(phi(p)<T)
for p in N:ck(phi(p)>T)

F={p for p in product(range(-4,5),repeat=2) if max(map(abs,uv(p)))<=10}
G=(F-set(P))|set(N)
ck(len(F)==45);ck(len(G)==45);ck(set(P)<=F);ck(not set(N)&F);ck(F!=G)
for a in forms:ck(Counter(linear(a,p) for p in F)==Counter(linear(a,p) for p in G))
# The four kernels are precisely the four listed directions up to sign.
for a,b in forms:
 normal=(-b,a)
 ck(any(normal[0]*v-normal[1]*u==0 for u,v in forms))
# Exact matrix certificate A^T A=10I and inverse images of the square's corners.
A=((1,-3),(3,1))
for i,j in product(range(2),repeat=2):ck(sum(A[k][i]*A[k][j] for k in range(2))==(10 if i==j else 0))
vertices={(2,4),(-4,2),(-2,-4),(4,-2)}
ck({uv(p) for p in vertices}==set(product((-10,10),repeat=2)))
for p in P+N:
 u,v=uv(p);ck((Q(u+3*v,10),Q(-3*u+v,10))==p)
# Hessian in (u,v) is diag(56u^6+2,56v^6+2), hence at least2I.
# Test the exact decomposition on rational points/vectors; universal nonnegativity
# is established by the sixth powers in the written proof.
for u,v,z,w in product([Q(-3,2),Q(0),Q(2,3)],repeat=4):
 lhs=(56*u**6+2)*(z-3*w)**2+(56*v**6+2)*(3*z+w)**2
 rhs=20*(z*z+w*w)+56*u**6*(z-3*w)**2+56*v**6*(3*z+w)**2
 ck(lhs==rhs);ck(lhs>=20*(z*z+w*w))

hi=Q(2501,250);lo=Q(2749,250)
upper=2*hi**8+2*hi**2;lower=lo**8
ck(upper<T);ck(lower>T);ck(Q(4,1000)==Q(1,250))
# Translation diagnostics, including extreme corners of the closed epsilon cube.
for h in product([Q(-1,1000),Q(0),Q(1,1000)],repeat=2):
 shifted=lambda p:(p[0]+h[0],p[1]+h[1])
 for p in P:ck(phi(shifted(p))<=upper<T)
 for p in N:ck(phi(shifted(p))>=lower>T)
 for a in forms:ck(Counter(linear(a,shifted(p)) for p in P)==Counter(linear(a,shifted(p)) for p in N))
# Pairwise disjoint translated open patches follow from integer center spacing.
for i,p in enumerate(P+N):
 for q in (P+N)[i+1:]:ck(max(abs(p[k]-q[k]) for k in range(2))>=1>Q(2,1000))

root=Path(__file__).parent
r={'problem_id':20001312,'status':'PASS_EXACT_CERTIFICATE','assertions':checks,
 'positive_points':P,'negative_points':N,'common_marginals':marginals,'lattice_body_points':len(F),
 'positive_phi_values':sorted(set(map(phi,P))),'negative_phi_values':sorted(set(map(phi,N))),
 'uniform_translation_radius':'1/1000','positive_uniform_upper_bound':str(upper),'negative_uniform_lower_bound':str(lower),
 'level':T,'proof_sha256':hashlib.sha256((root/'KNOWN_COUNTEREXAMPLE.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact finite signed certificate and rational uniform margins; convexity, all-function and almost-everywhere quantifiers are proved analytically.'}
print(json.dumps(r,indent=2,sort_keys=True))
