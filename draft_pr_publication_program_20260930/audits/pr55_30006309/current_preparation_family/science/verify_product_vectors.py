#!/usr/bin/env python3
"""Exact diagnostics for the product-face proof. Python standard library only.
No discriminant polynomial, regularity oracle or large triangulation enumeration.
Volumes are gcds of maximal minors, so lower-dimensional lattice normalization
is checked rather than replaced by ambient Euclidean volume.
"""
from itertools import combinations, permutations, product
from math import comb, gcd, factorial
from functools import reduce
from fractions import Fraction
import json

checks=0
def check(ok,label):
    global checks
    assert ok,label
    checks+=1

def det(M):
    M=[list(map(Fraction,row)) for row in M];out=Fraction(1)
    for i in range(len(M)):
        p=next((j for j in range(i,len(M)) if M[j][i]),None)
        if p is None:return 0
        if p!=i:M[i],M[p]=M[p],M[i];out=-out
        q=M[i][i];out*=q
        for j in range(i+1,len(M)):
            r=M[j][i]/q
            for k in range(i,len(M)):M[j][k]-=r*M[i][k]
    assert out.denominator==1
    return int(out)

def vol(vertices):
    k=len(vertices)-1
    if k==0:return 1
    a=vertices[0];D=[[v[i]-a[i] for v in vertices[1:]] for i in range(len(a))]
    return reduce(gcd,(abs(det([D[i] for i in rows])) for rows in combinations(range(len(a)),k)),0)

def faces(tops):
    return {tuple(sorted(s)) for top in tops for r in range(1,len(top)+1) for s in combinations(top,r)}

def eta(A,tops,face_dim,dim):
    out=[[0]*len(A) for _ in range(dim+1)]
    for f in faces(tops):
        verts=[A[i] for i in f];k=len(f)-1
        if face_dim(verts)==k:
            v=vol(verts);check(v>0,'positive exact face volume')
            for i in f:out[k][i]+=v
    return out

def simplex_vertices(n):return [tuple([0]*n)]+[tuple(int(i==j) for i in range(n)) for j in range(n)]
def minimal_simplex_face(verts,n,L=1):
    active=sum(all(v[i]==0 for v in verts) for i in range(n))
    active+=all(sum(v)==L for v in verts)
    return n-active

def box_face(verts,L):
    return len(L)-sum(all(v[i]==0 for v in verts) or all(v[i]==L[i] for v in verts) for i in range(len(L)))
def paths(j,l):
    # Each word in horizontal/vertical steps gives one staircase simplex.
    for right in combinations(range(j+l),j):
        right=set(right);x=y=0;out=[(0,0)]
        for k in range(j+l):
            if k in right:x+=1
            else:y+=1
            out.append((x,y))
        yield out

def product_tops(T,D_count):
    U=[]
    for top in T:
        top=tuple(sorted(top));j=len(top)-1;l=D_count-1
        for path in paths(j,l):U.append(tuple(top[i]*D_count+v for i,v in path))
    return U

# Finite-difference coefficients, including dimension one and empty lower ranges.
for n in range(1,17):
    for j in range(n+1):
        c=sum((-1)**(2*n-1-j-l)*comb(n,l+1)*comb(j+l+1,j+1) for l in range(n))
        target=n if j==n else (-1 if j==n-1 else 0)
        check(c==target,'binomial cancellation')

cases=[]
def run(name,n,A,T,base_face):
    Delta=simplex_vertices(n-1);B=[a+v for a in A for v in Delta]
    U=product_tops(T,len(Delta));d=2*n-1
    E=eta(A,T,base_face,n)
    def prod_face(verts):
        return base_face([v[:n] for v in verts])+minimal_simplex_face([v[n:] for v in verts],n-1)
    F=eta(B,U,prod_face,d)
    projected=[[sum(row[i*n:(i+1)*n]) for i in range(len(A))] for row in F]
    for k in range(d+1):
        expected=[0]*len(A)
        for j in range(n+1):
            l=k-j
            if 0<=l<=n-1:
                c=comb(n,l+1)*comb(k+1,j+1)
                expected=[x+c*y for x,y in zip(expected,E[j])]
        check(projected[k]==expected,'whole projected massive level')
    actual=[sum((-1)**(d-k)*projected[k][i] for k in range(d+1)) for i in range(len(A))]
    wanted=[n*E[n][i]-E[n-1][i] for i in range(len(A))]
    check(actual==wanted,'projected discriminant vector equals Hurwitz vector')
    basevol=sum(vol([A[i] for i in top]) for top in T)
    pvol=sum(vol([B[i] for i in top]) for top in U)
    check(pvol==comb(d,n)*basevol,'product normalized volume')
    cases.append({'case':name,'dimension':n,'base_points':len(A),'product_points':len(B),
        'base_simplices':len(T),'product_simplices':len(U),'base_normalized_volume':basevol,
        'product_normalized_volume':pvol,'projected_vector':actual,
        'unused_base_points':len(A)-len(set(i for t in T for i in t))})

A=[(i,) for i in range(4)]
run('interval_coarse',1,A,[(0,3)],lambda v:box_face(v,(3,)))
run('interval_fine',1,A,[(0,1),(1,2),(2,3)],lambda v:box_face(v,(3,)))
A=list(product(range(2),repeat=2));idx={x:i for i,x in enumerate(A)}
T=[tuple(idx[x] for x in tri) for tri in [[(0,0),(1,0),(1,1)],[(0,0),(0,1),(1,1)]]]
run('unit_square',2,A,T,lambda v:box_face(v,(1,1)))
A=list(product(range(3),range(2)));idx={x:i for i,x in enumerate(A)}
T=[tuple(idx[x] for x in tri) for tri in [[(0,0),(2,0),(2,1)],[(0,0),(0,1),(2,1)]]]
run('rectangle_nonunimodular_coarse',2,A,T,lambda v:box_face(v,(2,1)))
A=[x for x in product(range(3),repeat=2) if sum(x)<=2];idx={x:i for i,x in enumerate(A)}
run('double_triangle_coarse',2,A,[tuple(idx[x] for x in [(0,0),(2,0),(0,2)])],lambda v:minimal_simplex_face(v,2,2))
T=[[(0,0),(1,0),(0,1)],[(1,0),(2,0),(1,1)],[(0,1),(1,1),(0,2)],[(1,0),(0,1),(1,1)]]
run('double_triangle_fine',2,A,[tuple(idx[x] for x in t) for t in T],lambda v:minimal_simplex_face(v,2,2))
A=list(product(range(2),repeat=3));idx={x:i for i,x in enumerate(A)};T=[]
for perm in permutations(range(3)):
    x=[0,0,0];top=[idx[tuple(x)]]
    for i in perm:x[i]=1;top.append(idx[tuple(x)])
    T.append(tuple(top))
run('unit_cube',3,A,T,lambda v:box_face(v,(1,1,1)))
A=[x for x in product(range(3),repeat=3) if sum(x)<=2];idx={x:i for i,x in enumerate(A)}
run('double_tetrahedron_coarse',3,A,[tuple(idx[tuple(2*y for y in x)] for x in simplex_vertices(3))],lambda v:minimal_simplex_face(v,3,2))
print(json.dumps({'status':'PASS','exact_assertions':checks,'case_count':len(cases),'cases':cases,
    'limits':['No enumeration of all triangulations','No test replaces GKZ normal-fan input',
    'No certification of an analytic-free foundation for GKZ','No singular-toric extension claimed']},indent=2))
