#!/usr/bin/env python3
"""Exact algebraic diagnostics only. No branched-surface realization is claimed."""
from fractions import Fraction as Q
from collections import Counter
import json

checks=Counter()
def check(x,label):
    assert x,label
    checks[label]+=1
def mv(A,v):return tuple(sum(a*b for a,b in zip(row,v)) for row in A)
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))) for i in range(len(A)))
def det2(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def norm(v):return tuple(x/sum(v) for x in v)
I=((1,0),(0,1))
A=((2,1),(0,1))
U=((1,1),(0,1))
Ap,Up=I,I
for k in range(31):
    check(Ap==((2**k,2**k-1),(0,1)),'exact_expanding_powers')
    check(Up==((1,k),(0,1)),'exact_unipotent_powers')
    check(det2(Up)==1,'unipotent_determinant')
    Ap,Up=mm(A,Ap),mm(U,Up)
for x in range(7):
    for y in range(7):
        if x+y==0:continue
        w=(Q(x),Q(y))
        aw,uw=mv(A,w),mv(U,w)
        check(w[0]*aw[1]-w[1]*aw[0]==-y*(x+y),'eigenray_determinant_A')
        check(w[0]*uw[1]-w[1]*uw[0]==-y*y,'eigenray_determinant_U')
        check(sum(aw)>0 and sum(uw)>0,'nonannihilation')
        if y:
            check(w[0]*aw[1]!=w[1]*aw[0] and w[0]*uw[1]!=w[1]*uw[0],
                  'no_positive_second_coordinate_eigenray')
check(mv(A,(1,0))==(2,0),'boundary_eigenray')
check(mv(U,(1,0))==(1,0),'unit_eigenvalue')
check(U!=I,'nonidentity')
# Dropping nonannihilation permits a nonzero cone-preserving nilpotent map.
N=((0,1),(0,0))
check(mm(N,N)==((0,0),(0,0)),'missing_hypothesis_negative_control')
check(mv(N,(1,0))==(0,0),'missing_hypothesis_negative_control')
check(det2(N)==0 and N[0][0]+N[1][1]==0,'missing_hypothesis_negative_control')

# Branch cone x+y=z. Check its extreme rays and its induced 2D map exactly.
B=((1,1,0),(1,0,0),(2,1,0))
r1,r2=(1,0,1),(0,1,1)
check(mv(B,r1)==tuple(x+y for x,y in zip(r1,r2)),'extreme_ray_cone_preservation')
check(mv(B,r2)==r1,'extreme_ray_cone_preservation')
check(tuple(sum(r*B[i][j] for i,r in enumerate((1,1,-1))) for j in range(3))==(0,0,0),
      'branch_equation_identity')
for denominator in range(1,18):
    for numerator in range(denominator+1):
        t=Q(numerator,denominator)
        w=(t/2,(1-t)/2,Q(1,2))
        image=mv(B,w)
        fw=norm(image)
        check(sum(image)==1+t>0,'positive_normalization_denominator')
        check(fw[0]+fw[1]==fw[2]==Q(1,2),'normalized_branch_equation')
        check(2*fw[0]==1/(1+t),'projective_interval_formula')
        check(Q(1,2)<=2*fw[0]<=1,'compact_interval_mapping')
        check(norm(mv(B,tuple(13*x for x in w)))==fw,'projective_scale_invariance')

# Exact quadratic field Q(sqrt(5)), with phi=(1+sqrt(5))/2.
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):return x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
phi=(Q(1,2),Q(1,2))
one=(Q(1),Q(0))
zero=(Q(0),Q(0))
v=(phi,one,add(phi,one))
image=[]
for row in B:
    val=zero
    for coefficient,entry in zip(row,v):
        val=add(val,(coefficient*entry[0],coefficient*entry[1]))
    image.append(val)
check(tuple(image)==tuple(mul(phi,entry) for entry in v),'exact_irrational_branch_eigenvector')
check(add(v[0],v[1])==v[2],'exact_irrational_branch_equation')
check(mul(phi,phi)==add(phi,one),'quadratic_field_identity')

print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
                  'checks_by_category':dict(sorted(checks.items())),
                  'scope':'Algebraic diagnostics, with an additional missing-hypothesis control and exact irrational eigenvector. No embedding, splitting, radius-growth, or classification certificate.',
                  'dependencies':'Python standard library only'},indent=2,sort_keys=True))
