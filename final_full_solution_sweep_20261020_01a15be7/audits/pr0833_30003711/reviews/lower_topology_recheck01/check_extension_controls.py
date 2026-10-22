#!/usr/bin/env python3
"""Independent exact Eisenstein-matrix and group-cohomology input controls.
No assertion is used: controls remain active in optimized Python.
Poincare duality is a mathematical argument, not computed by this program.
"""
import itertools,json
F=range(3); P=list(itertools.product(F,repeat=3))
Z=(0,0); ONE=(1,0); W=(0,1)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def emul(x,y):
    a,b=x;c,d=y
    return (a*c-b*d,a*d+b*c-b*d)
def epow(x,n):
    z=ONE
    for _ in range(n):z=emul(z,x)
    return z
def mm(X,Y):
    return tuple(tuple(sum_e(emul(X[i][k],Y[k][j]) for k in range(3)) for j in range(3)) for i in range(3))
def sum_e(xs):
    s=Z
    for x in xs:s=add(s,x)
    return s
def scale(x,M):return tuple(tuple(emul(x,v) for v in row) for row in M)
def det(M):
    terms=[]
    for p in itertools.permutations(range(3)):
        inversions=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        t=ONE
        for i in range(3):t=emul(t,M[i][p[i]])
        terms.append(neg(t) if inversions%2 else t)
    return sum_e(terms)
I=tuple(tuple(ONE if i==j else Z for j in range(3)) for i in range(3))
A=((Z,Z,ONE),(ONE,Z,Z),(Z,ONE,Z))
B=tuple(tuple(epow(W,i) if i==j else Z for j in range(3)) for i in range(3))
def mpow(M,n):
    r=I
    for _ in range(n):r=mm(r,M)
    return r
matrices={(a,b,c):scale(epow(W,c),mm(mpow(A,a),mpow(B,b))) for a,b,c in P}
def mul(g,h,law='correct'):
    a,b,c=g;d,e,f=h
    twist={'correct':b*d,'swapped':a*e,'abelian':0}[law]
    return ((a+d)%3,(b+e)%3,(c+f+twist)%3)
def require(condition,label):
    if not condition:raise RuntimeError(label)
def rank3(rows,ncols):
    R=[list(row) for row in rows];rank=0
    for j in range(ncols):
        p=next((i for i in range(rank,len(R)) if R[i][j]%3),None)
        if p is None:continue
        R[rank],R[p]=R[p],R[rank]
        t=pow(R[rank][j]%3,-1,3);R[rank]=[(x*t)%3 for x in R[rank]]
        for i in range(rank+1,len(R)):
            t=R[i][j]%3
            if t:R[i]=[(a-t*b)%3 for a,b in zip(R[i],R[rank])]
        rank+=1
    return rank
idx={g:i for i,g in enumerate(P)}
rows=[]
for g,h in itertools.product(P,repeat=2):
    row=[0]*27
    row[idx[g]]-=1;row[idx[h]]-=1;row[idx[mul(g,h)]]+=1
    rows.append(row)
h1dim=27-rank3(rows,27)
require(len(set(matrices.values()))==27,'27 distinct actual matrices')
require(all(det(M)==ONE for M in matrices.values()),'determinant1')
require(all(mm(matrices[g],matrices[h])==matrices[mul(g,h)] for g,h in itertools.product(P,repeat=2)),'matrix multiplication formula')
require(all(mul(mul(g,h),k)==mul(g,mul(h,k)) for g,h,k in itertools.product(P,repeat=3)),'associativity')
require(h1dim==2,'H1 dimension2')
require(all(mul(mul(g,g),g)==(0,0,0) for g in P),'exponent3')
def coboundary_ok(sign=-1):
    def f(g):a,b,c=g;return (c+sign*a*b)%3
    return all((f(h)-f(mul(g,h))+f(g))%3==(g[0]*h[1])%3 for g,h in itertools.product(P,repeat=2))
require(coboundary_ok(),'uv exact coboundary')
negative_controls={
'wrong_matrix_commutator':mm(B,A)==scale(epow(W,2),mm(A,B)),
'abelian_group_substitution':all(mm(matrices[g],matrices[h])==matrices[mul(g,h,'abelian')] for g,h in itertools.product(P,repeat=2)),
'swapped_cocycle_without_relabel':all(mm(matrices[g],matrices[h])==matrices[mul(g,h,'swapped')] for g,h in itertools.product(P,repeat=2)),
'wrong_cochain_plus_ab':coboundary_ok(1),
'wrong_H1_dimension3':h1dim==3,
'false_nonzero_inflated_uv':not coboundary_ok(),
}
require(not any(negative_controls.values()),'all six deliberate corruptions must fail')
print(json.dumps({'exact_arithmetic':'Z[omega], omega^2+omega+1=0; F3','distinct_SU3_lift_matrices':27,'matrix_products':729,'associativity_triples':19683,'cup_coboundary_pairs':729,'H1_equation_rank':27-h1dim,'H1_dimension':h1dim,'negative_controls_rejected':list(negative_controls),'passed':True},indent=2))
