#!/usr/bin/env python3
"""Independent PR195 checks; only Python standard library; no candidate imports.
This corroborates the analytic proof. Genericity is established by the proof's
open conditions, not by the existence of one successful numerical flag.
"""
from fractions import Fraction as F
from itertools import combinations
import json

AMBIENT = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,1)]


def rank(matrix):
    a=[[F(x) for x in row] for row in matrix]
    piv=0
    if not a:return 0
    for j in range(len(a[0])):
        row=next((i for i in range(piv,len(a)) if a[i][j]),None)
        if row is None:continue
        a[piv],a[row]=a[row],a[piv]
        v=a[piv][j];a[piv]=[x/v for x in a[piv]]
        for i in range(len(a)):
            if i!=piv and a[i][j]:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[piv])]
        piv+=1
        if piv==len(a):break
    return piv


def scalar_system(restriction):
    r=len(restriction[0]);L=[[sum(a[j]*restriction[j][k] for j in range(4)) for k in range(r)] for a in AMBIENT]
    n=4*r+7;eq=[]
    for i in range(7):
        for k in range(r):
            v=[0]*n
            for j in range(4):v[j*r+k]=AMBIENT[i][j]
            v[4*r+i]=-L[i][k];eq.append(v)
    eq.append([0]*(4*r)+[1]*7)
    assert all(any(v) for v in L)
    assert all(rank([L[i],L[j]])==2 for i,j in combinations(range(7),2))
    assert rank(restriction)==r
    assert rank([L[0],L[4],L[5]])==min(r,3)
    return eq,L,{'section_variables':r,'unknowns':n,'equations':len(eq),'rank':rank(eq),'linear_syzygy_dimension':n-rank(eq),'all_seven_distinct_projective_factors':True,'restriction_injective':True}


def divides(a,b):return all(x<=y for x,y in zip(a,b))

def member(t,gens):return any(divides(g,t) for g in gens)

def monomials(n,d):
    if n==1:yield (d,);return
    for k in range(d+1):
        for tail in monomials(n-1,d-k):yield (k,)+tail

def stable(gens):
    # Checking lowering moves on a monomial generating set is sufficient.
    for t in gens:
        for j,exp in enumerate(t):
            if exp:
                for i in range(j):
                    u=list(t);u[j]-=1;u[i]+=1
                    if not member(u,gens):return False
    return True

def main():
    ternary=[[1,0,0],[0,1,0],[0,0,1],[1,2,3]]
    binary=[[1,0],[0,1],[2,3],[7,11]]
    e3,l3,o3=scalar_system(ternary);e2,l2,o2=scalar_system(binary)
    assert o3['linear_syzygy_dimension']==0
    assert o2['linear_syzygy_dimension']==1
    assert rank(AMBIENT)==4
    # Syzygy coefficients u_x=11s,u_y=11t,u_z=-73(2s+3t),u_w=25(7s+11t).
    witness=[11,0,0,11,-146,-219,175,275]+[11,11,11,11,-73,25,4]
    assert all(sum(x*y for x,y in zip(row,witness))==0 for row in e2)
    # Distinctness in combinations is not assumed by Hilbert--Burch: check all multisets.
    coefficient_degree_options=[(a,b,c) for a in range(1,7) for b in range(a,7) for c in range(b,7) if a+b+c==6 and sum(x==1 for x in (a,b,c))==1]
    assert coefficient_degree_options==[(1,2,3)]
    numerator={0:1,6:-4,7:1,8:1,9:1}
    H2={d:sum(v*(d-shift+1) for shift,v in numerator.items() if d>=shift) for d in range(10)}
    assert [H2[d] for d in (6,7,8)]==[3,1,0]
    H3={5:21,6:24,7:24}
    kernels={d:H3[d-1]-H3[d]+H2[d] for d in (6,7)}
    assert kernels=={6:0,7:1}
    # A citation-boundary control: a full-ring generator divisible by x3 can
    # involve x4 and thus be invisible in the third sectional row.
    boundary=[(2,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,2,0,0),(0,1,1,0),(0,1,0,1),(0,0,2,0),(0,0,1,2)]
    assert stable(boundary)
    assert all(not any(i!=j and divides(a,b) for i,a in enumerate(boundary)) for j,b in enumerate(boundary))
    H=lambda i,d:sum(not member(t+(0,)*(4-i),boundary) for t in monomials(i,d))
    assert (H(3,2),H(3,3),H(2,3))==(0,0,0)
    print(json.dumps({'three_section':o3,'two_section':o2,'constant_polar_relation_dimension':4-rank(AMBIENT),'explicit_binary_scalar_syzygy_verified':True,'Hilbert_Burch_coefficient_degree_options':coefficient_degree_options,'binary_Hilbert_values':H2,'ternary_Hilbert_values':H3,'x3_kernels':kernels,'threshold_p':8,'first_x3_generator_degree_in_B3':7,'citation_boundary_control':{'strongly_stable':True,'minimal_full_ring_generator':[0,0,1,2],'third_row_triangle_equality':True,'requires_using_truncation_or_largest_variable':True}},indent=2))

if __name__=='__main__':main()
