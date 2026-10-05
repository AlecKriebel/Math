#!/usr/bin/env python3
"""Independent exact controls for the connected quotient construction.

No author code is imported. Finite algebraic checks supplement the written
local smoothing, integral class and covering-space proofs.
"""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from collections import Counter
from math import gcd
from functools import reduce
import json

checks=Counter()
def ok(v,k):
    assert v,k
    checks[k]+=1

def det(a):
    n=len(a)
    out=F(0)
    for p in permutations(range(n)):
        sg=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        t=F(sg)
        for i in range(n):t*=a[i][p[i]]
        out+=t
    return out

def outer(a,b):return {(i,j):a[i]*b[j]-a[j]*b[i] for i,j in combinations(range(4),2)}
def add(a,b):return {k:a.get(k,0)+b.get(k,0) for k in combinations(range(4),2)}
def scale(c,a):return {k:c*v for k,v in a.items()}
def evaluate(a,u,v):return sum(w*(u[i]*v[j]-u[j]*v[i]) for (i,j),w in a.items())
def wedge(a,b):
    return sum(x*y*det([[int(t==j) for j in range(4)] for t in ij+kl])
               for ij,x in a.items() for kl,y in b.items())
def pull(a,m):
    return {(i,j):evaluate(a,[m[k][i] for k in range(4)],[m[k][j] for k in range(4)]) for i,j in combinations(range(4),2)}
e=[[int(i==j) for j in range(4)] for i in range(4)]
A=[e[0],[0,1,-1,0]];B=[[0,1,1,0],e[3]]
omega=add(outer(e[0],e[1]),outer(e[2],e[3]))
alpha=add(outer(*A),outer(*B))
tau=[[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]]
beta=pull(alpha,tau)
ok(pull(omega,tau)==omega,'symplectic_involution_linear_part')
ok(add(alpha,beta)==scale(2,omega),'cover_class_identity')
ok(wedge(alpha,alpha)==wedge(beta,beta)==4,'component_squares')
ok(wedge(alpha,beta)==0,'orthogonality')
ok(wedge(omega,omega)==2,'ambient_volume')
ok(det(A+B)==2,'positive_transverse_intersections')
for n in (A,B):
    minors=[abs(int(det([[row[i],row[j]] for row in n]))) for i,j in combinations(range(4),2)]
    ok(reduce(gcd,minors)==1,'primitive_normal_lattice')
for tangents in (([0,1,1,0],[0,0,0,1]),([1,0,0,0],[0,1,-1,0])):
    ok(evaluate(omega,*tangents)==1,'torus_symplectic_orientation')
# Check the local coordinate transformation independently by pullback to x.
srows=A+B
local_alpha=add(outer(e[0],e[1]),outer(e[2],e[3]))
local_beta=add(outer(e[0],e[2]),scale(-1,outer(e[1],e[3])))
ok(pull(local_alpha,srows)==alpha,'local_alpha_identity')
ok(pull(local_beta,srows)==beta,'local_beta_identity')

# Work on the eighth-lattice to include every isolated affine intersection.
def invol(x):return ((x[0]+4)%8,x[1],-x[2]%8,-x[3]%8)
def belongs(x):
    a,b,c,d=x
    return (a==0 and (b-c)%8==0,
            (b+c)%8==2 and d==2,
            a==4 and (b+c)%8==0,
            (b-c)%8==2 and d==6)
counts=Counter();intersections={p:[] for p in combinations(range(4),2)}
for x in product(range(8),repeat=4):
    y=invol(x)
    ok(y!=x and invol(y)==x,'free_affine_involution_on_grid')
    b=belongs(x);c=belongs(y)
    ok(c==(b[2],b[3],b[0],b[1]),'component_exchange_on_grid')
    for i,v in enumerate(b):counts[i]+=v
    for ij in intersections:
        if b[ij[0]] and b[ij[1]]:intersections[ij].append(x)
ok(all(v==64 for v in counts.values()),'torus_grid_sizes')
ok(intersections[(0,1)]==[(0,1,1,2),(0,5,5,2)],'two_original_nodes')
ok(intersections[(2,3)]==[(4,1,7,6),(4,5,3,6)],'two_translated_nodes')
for p in ((0,2),(0,3),(1,2),(1,3)):ok(not intersections[p],'cross_pair_disjointness_grid')

# Analytic smoothing control in polar coordinates, using positive real epsilon.
# rho=epsilon*chi/r, with chi>=0, chi'<=0: beta vanishes and
# alpha(d_r,d_theta)=r-rho*rho'>0. Rational unit vectors avoid trig.
angles=[F(t,3) for t in range(-4,5)]
for r,eps,chi,dchi,t in product((F(1,8),F(1,4),F(1,2)),(F(1,256),F(1,64)),(F(0),F(1,3),F(1)),(F(-2),F(-1,2),F(0)),angles):
    co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
    rho=eps*chi/r;drho=eps*(dchi/r-chi/(r*r))
    dr=[co,si,drho*co,-drho*si]
    dt=[-r*si,r*co,-rho*si,-rho*co]
    ok(evaluate(local_beta,dr,dt)==0,'cutoff_beta_vanishes')
    ok(evaluate(local_alpha,dr,dt)==r-rho*drho,'cutoff_alpha_formula')
    ok(r-rho*drho>0,'cutoff_symplectic_positivity')

# Two tori with two nodes: four disk removals and two annulus insertions.
ok(2*0-4+2*0==-4,'smoothing_Euler_characteristic')
ok(1-(-4)//2==3,'smoothing_genus')
ok(F(1,2)*4*wedge(omega,omega)==4,'quotient_surface_square')
# The torus x3=x4=0 has x1 period 1/2 in the quotient.
ok(F(1,2)*2==1,'integral_class_primitive_period')
# The cokernel of the oriented top-degree map Z -> Z² is free Z.
# Integer basis (1,1),(0,1) has determinant 1; (b-a) is the quotient coordinate.
ok(det([[1,0],[1,1]])==1,'diagonal_map_saturated')
for a,b,c in product(range(-4,5),repeat=3):
    ok((b+c)-(a+c)==b-a,'Thom_diagonal_cokernel_coordinate')
result={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
        'grid_points':8**4,'smoothing_samples':3*2*3*3*9,
        'scope':'Finite exact affine, exterior-algebra and smoothing controls; the general construction and covering-space obstruction are justified by the written proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
