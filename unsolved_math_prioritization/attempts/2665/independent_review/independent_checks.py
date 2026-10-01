#!/usr/bin/env python3
"""Separate finite exact controls for the five scoped Kirby partials.
No knot embeddings or external topology are certified by these checks.
"""
import json,random
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import gcd,prod
import sympy as S
C=Counter()
def ck(v,label):
    assert bool(v),label
    C[label]+=1
rng=random.Random(2665)
t=S.symbols('t')
# Known lattice bases transformed by unrelated elementary transvections.
for case in range(80):
    a,b,c=[rng.randrange(-4,5) for _ in range(3)]
    core=S.Matrix([[a,b+1],[b,c]])
    if not core.det():continue
    alpha=S.Matrix([rng.randrange(-5,6),rng.randrange(-5,6)])
    E=S.zeros(4);E[0,1]=1;E[1,2:]=alpha.T;E[2:,1]=alpha;E[2:,2:]=core
    P=S.eye(4)
    for j in range(12):
        i,k=rng.sample(range(4),2);Q=S.eye(4);Q[i,k]=rng.choice([-2,-1,1,2]);P=P*Q
    V=P.T*E*P;J=V-V.T;Pi=P.inv();v=Pi[:,0];w=Pi[:,1]+rng.randrange(-5,6)*v
    ck(V*v==S.zeros(4,1),'singular_kernel')
    ck(gcd(*[int(x) for x in v])==1,'primitive_kernel')
    ck((v.T*J*w)[0]==1,'symplectic_partner')
    projection=S.eye(4)+v*(w.T*J)-w*(v.T*J)
    ck(projection**2==projection,'integral_projection')
    ck(v.T*J*projection==S.zeros(1,4) and w.T*J*projection==S.zeros(1,4),'orthogonal_projection')
    w=w-(w.T*V*w)[0]*v
    B=S.Matrix.hstack(v,w,Pi[:,2],Pi[:,3])
    ck(abs(B.det())==1 and B.T*V*B==E,'exact_reduced_basis')
    for z in range(-2,5):ck((z*V-V.T).det()==z*(z*core-core.T).det(),'determinant_t_factor')
# Independent closure via repeated full product sets, not graph queue traversal.
def divs(n):return [i for i in range(1,n+1) if n%i==0]
def sets(N):
    k=(N-1)//2;T={(2*x*y)**2%N for x in divs(k) for y in divs(k+1)}
    layers=[{1}]
    while True:
        new={a*b%N for a in layers[-1] for b in T}
        if new==layers[-1]:return T,layers
        layers.append(new)
for N in range(3,84,2):
    T,layers=sets(N);H=layers[-1]
    ck(1 in T and all(gcd(a,N)==1 for a in T),'special_units')
    ck({pow(a,-1,N) for a in T}==T,'inverse_closed')
    ck(all(a*b%N in H for a in H for b in H),'group_closure')
    for a in H:
        da=next(i for i,x in enumerate(layers) if a in x)
        for b in H:
            db=next(i for i,x in enumerate(layers) if b in x)
            dab=next(i for i,x in enumerate(layers) if a*b%N in x)
            ck(dab<=da+db,'arithmetic_distance_triangle')
    k=N//2;d=-k*(k+1)
    for a in range(1,N):
        if gcd(a,N)!=1:continue
        for h in H:
            b=a*h%N
            ck(((a-b)*d)%6==0,'formal_w_integrality')
            w=F((a-b)*d,6)
            u=(3*int(w)*pow(2*b,-1,N))%N;z=(2*b*u-3*int(w))//N
            ck(b*d+6*w==a*d and 2*b*u-N*z-3*w==0,'formal_matching_both_coefficients')
T,L=sets(37)
ck(T=={1,4,7,9,16,28,33,36},'N37_T')
ck(3 not in L[2] and 3 in L[3] and L[-1]-L[2]=={3,25},'N37_distance_three')
ck(prod([4,16,33])%37==3,'N37_word')
T,L=sets(13);H=L[-1]
missing={p for p in combinations(sorted(H),2) if p[1]*pow(p[0],-1,13)%13 not in T}
ck(missing=={(1,12),(3,10),(4,9)},'N13_matching')
for ss in combinations(H,5):ck(sum(set(p)<=set(ss) for p in missing)>=2,'hyperbolic_five_label_obstruction')
# Direct congruence and rank-one determinant identities.
a,b,c,x,y,f=S.symbols('a b c x y f');A=S.Matrix([[a,b+1],[b,c]]);w=S.Matrix([x,y]);B=A+f*w*w.T
ck(S.expand(B.det()-A.det()-f*(c*x*x-(2*b+1)*x*y+a*y*y))==0,'symbolic_rank_one_update')
for N,a,P,out in [(13,1,[[2,-1],[1,0]],[[30,-8],[-9,1]]),(13,12,[[3,-1],[-2,1]],[[30,-3],[-4,-1]]),(37,1,[[3,-1],[1,0]],[[120,-21],[-22,1]]),(37,3,[[15,1],[-1,0]],[[120,27],[26,3]])]:
    P=S.Matrix(P);V=S.Matrix([[a,N//2+1],[N//2,0]])
    ck(P.det()==1 and P.T*V*P==S.Matrix(out),'annular_normal_forms')
# Evaluate the original two-loop polynomial at arbitrary rational q first.
def theta(n,k,u,z,w,q):
    d=-k*(k+1);AA=n*d-F(k*(k+1)*(2*k+1),2)+6*w;BB=F(2*n*u-(2*k+1)*z-3*w,2)
    return AA*(-2-F(2*d+1,3)*q)-4*BB*(1+d*q)
for k in range(-10,11):
    d=-k*(k+1)
    for f in (-11,-2,-1,1,2,11):
        for u in (-5,0,7):
            n,z,w=3,-2,5
            delta0=theta(n+f,k,u,z,w,0)-theta(n,k,u,z,w,0)
            delta4=theta(n+f,k,u,z,w,-4)-theta(n,k,u,z,w,-4)
            ck((1-4*d)*delta0-delta4==F(4*f*d*(4*d-1),3),'two_loop_evaluation_elimination')
            if d:ck(delta0!=0 or delta4!=0,'fixed_spine_nonzero')
for d,f,ans in [(-42,11,104104),(-342,2,1248528)]:ck(abs(F(4*f*d*(4*d-1),3))==ans,'exact_gap_values')
for N,a,b,u,z,w in [(13,1,12,8,-3,77),(37,1,3,20,-6,114)]:
    for q in (F(-4),F(-1,2),F(0),F(1,3),F(9)):
        ck(theta(a,N//2,0,0,0,q)==theta(b,N//2,u,z,w,q),'formal_full_polynomial_match')
ck(F(77,2).denominator==2,'half_integral_v3_allowed')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'families':dict(C),'sympy_version':S.__version__,
 'limits':'Independent finite lattice, modular, matrix and two-loop arithmetic controls only. External source theorems, surface confinement, ambient linking and knot realization require the written audit.'},indent=2))
