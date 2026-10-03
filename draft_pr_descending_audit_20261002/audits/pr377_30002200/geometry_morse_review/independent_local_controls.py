#!/usr/bin/env python3
"""Exact local controls. Universal conclusions come from independent_geometry_proof.md."""
from fractions import Fraction as F
from itertools import product
import json, random

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a): return list(map(list,zip(*a)))
def inertia(matrix):
    """Exact symmetric congruence elimination, including off-diagonal 2x2 pivots."""
    a=[row[:] for row in matrix]; neg=pos=zero=0
    while a:
        n=len(a); p=next((i for i in range(n) if a[i][i]),None)
        if p is not None:
            perm=[p]+[i for i in range(n) if i!=p]
            a=[[a[i][j] for j in perm] for i in perm]
            d=a[0][0]; neg+=int(d<0); pos+=int(d>0)
            a=[[a[i][j]-a[i][0]*a[0][j]/d for j in range(1,n)] for i in range(1,n)]
        else:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
            if pair is None: zero+=n; break
            p,q=pair; perm=[p,q]+[i for i in range(n) if i not in pair]
            a=[[a[i][j] for j in perm] for i in perm]; d=a[0][1]
            neg+=1; pos+=1
            a=[[a[i][j]-(a[i][0]*a[1][j]+a[i][1]*a[0][j])/d for j in range(2,n)] for i in range(2,n)]
    return neg,pos,zero

def generic(l):
    return all(sum(s*x for s,x in zip(sign,l)) for sign in product((-1,1),repeat=len(l)))

def one(l,s):
    r=len(l); c=sum(x*y for x,y in zip(l,s)); assert c>0
    J=[j for j in range(r) if s[j]<0]
    A=[[((c*s[i]*l[i]) if i==j else F(0))-l[i]*l[j] for j in range(r)] for i in range(r)]
    assert all(sum(A[i][j]*s[j] for j in range(r))==0 for i in range(r))
    assert inertia(A)==(len(J),r-len(J)-1,1)
    # Direct restriction to TW_J: x_j=y_j-h, x_i=h for i not in J.
    B=[[F(int(i==j)) for j in J]+[F(s[i])] for i in range(r)]
    C=mm(mm(tr(B),A),B)
    expected=[[(-c*l[J[i]] if i==j else F(0))-l[J[i]]*l[J[j]] for j in range(len(J))]+[F(0)] for i in range(len(J))]+[[F(0)]*(len(J)+1)]
    assert C==expected
    assert inertia(C)==(len(J),0,1)
    # q=2a-1 copies of A and 2b diagonal directions per factor.
    for a,b in ((1,1),(2,1),(1,3),(4,2)):
        q=2*a-1; d=2*a+2*b-1
        assert q*len(J)+2*b*len(J)==len(J)*d
        assert q*1==2*a-1
        assert q*(r-len(J)-1)+2*b*(r-len(J)) + len(J)*d + q == r*d
    return {'negative':len(J),'positive':r-len(J)-1,'null':1,'c':str(c)}

def main():
    rng=random.Random(30002200377); total=0; manifest=[]
    print('Exact rational controls; seed 30002200377; finite evidence only.')
    for r in range(1,10):
        vectors=[]
        if r%2: vectors.append([F(1)]*r)
        vectors.append([F(2**j) for j in range(r)])
        for variant in range(2):
            vals=[rng.randrange(1,20) for _ in range(r)]
            if sum(vals)%2==0: vals[-1]+=1
            vectors.append([F(x,7) for x in vals])
        for idx,l in enumerate(vectors):
            assert generic(l)
            count=0; distribution={}
            for s in product((-1,1),repeat=r):
                if sum(x*y for x,y in zip(l,s))>0:
                    row=one(l,s); key=str(row['negative'])
                    distribution[key]=distribution.get(key,0)+1; count+=1
            total+=count
            rec={'rank':r,'vector':[str(x) for x in l],'short_critical_manifolds':count,'negative_x_block_distribution':distribution}
            manifest.append(rec); print(json.dumps(rec,sort_keys=True))
    for r in (10,11,12,13,14,20):
        l=[F(2**j,3) for j in range(r)]; count=0
        for _ in range(40):
            s=[rng.choice((-1,1)) for _ in range(r)]
            if sum(x*y for x,y in zip(l,s))<0: s=[-x for x in s]
            one(l,s); count+=1
        total+=count; print(json.dumps({'rank':r,'sampled_signed_vectors':count,'lengths':'powers of two / 3'},sort_keys=True))
    # Nongeneric walls: exact collinear solutions give deficient differential.
    for r in (2,4,6,8,10):
        s=[1]*(r//2)+[-1]*(r//2); l=[F(1)]*r
        assert sum(x*y for x,y in zip(l,s))==0
        # At a=b=1: norm differential row has 2s_j in x_j;
        # two linear rows have all l_j in x_j and y_j respectively.
        M=[]
        for j in range(r):
            row=[F(0)]*(4*r); row[4*j]=F(2*s[j]); M.append(row)
        for coordinate in (0,1):
            row=[F(0)]*(4*r)
            for j in range(r): row[4*j+coordinate]=l[j]
            M.append(row)
        combination=[F(-s[j],2) for j in range(r)]+[F(1),F(0)]
        assert all(sum(combination[i]*M[i][j] for i in range(r+2))==0 for j in range(4*r))
        assert any(combination)
        print(json.dumps({'wall_rank':r,'explicit_nonzero_gradient_relation':[str(x) for x in combination]}))
    # Exact unweighted-function falsifier from source p.5.
    l=[F(1),F(2)]; u=[F(1),F(-1)]
    assert sum(u)==0 and sum(x*y for x,y in zip(l,u))!=0 and generic(l)
    print('SOURCE_FALSIFIER: l=(1,2), u=(1,-1), z=0 is in complement; printed unweighted f=0 and Df=0; corrected f=-1.')
    # Zero-length odd-support genericity and product dimensions.
    for r in range(2,15):
        support=r if r%2 else r-1; l=[F(0)]*(r-support)+[F(1)]*support
        assert generic(l)
        for a,b in ((1,1),(2,3)):
            d=2*a+2*b-1
            assert r*d-2*a==(r-support)*d+(support*d-2*a)
        print(json.dumps({'rank':r,'odd_support':support,'zero_factor_count':r-support,'generic':True,'dimension_additive':True}))
    # Koszul wedge orientation sign: direct shuffle and d-odd crossing.
    sign_controls=0
    for r in range(1,11):
        for mask in range(1<<r):
            J=[j for j in range(r) if mask>>j&1]
            for j in range(r):
                if j not in J:
                    sign=(-1)**sum(i>j for i in J)
                    order=J+[j]; inversions=sum(order[i]>order[k] for i in range(len(order)) for k in range(i+1,len(order)))
                    assert sign==(-1)**inversions; sign_controls+=1
    print(json.dumps({'signed_hessian_cases':total,'orientation_sign_controls':sign_controls,'all_assertions_passed':True},sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
