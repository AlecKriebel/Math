#!/usr/bin/env python3
"""Exact, standard-library-only checks; no network, no third-party inputs."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb
import json

CHECKS = 0

def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(message)


def det(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError('determinant requires a square matrix')
    out = Q(1)
    for i in range(n):
        p = next((j for j in range(i,n) if a[j][i]), None)
        if p is None:
            return Q(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            out = -out
        out *= a[i][i]
        pivot = a[i][i]
        for j in range(i+1,n):
            f = a[j][i]/pivot
            for k in range(i+1,n):
                a[j][k] -= f*a[i][k]
    return out


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def matvec(a,v):
    return tuple(dot(row,v) for row in a)


def compositions(n,k):
    if k == 1:
        yield (n,)
    else:
        for j in range(n+1):
            for tail in compositions(n-j,k-1):
                yield (j,)+tail


def check_semigroup():
    counts=[]
    normal_total=0
    for r in range(13):
        values=set()
        normal=0
        for m in compositions(r,6):
            if m[0] and m[5]:
                continue
            normal += 1
            # q=(1,b,d,a,c,bc-ad), lowest lex (a,b,c,d).
            value=(r,m[3],m[1]+m[5],m[4]+m[5],m[2])
            require(value not in values,'two normal monomials have the same value')
            values.add(value)
            support=[(m[3]+j,m[1]+m[5]-j,m[4]+m[5]-j,m[2]+j)
                     for j in range(m[5]+1)]
            require(min(support)==value[1:],'wrong least term of normal monomial')
            require(all(0<=x<=r for a in support for x in a),'degree box violation')
        expected=comb(r+5,5)-(comb(r+3,5) if r>=2 else 0)
        require(normal==expected==len(values),'wrong degree count')
        normal_total+=normal
        counts.append([r,normal])
    # Equal leading values in the defining relation, but nonzero difference.
    p34={(0,1,1,0):1,(1,0,0,1):-1}
    p13p24={(0,1,1,0):1}
    difference={e:p34.get(e,0)-p13p24.get(e,0) for e in set(p34)|set(p13p24)}
    difference={e:v for e,v in difference.items() if v}
    require(min(p34)==min(p13p24),'least bc terms should agree')
    require(difference=={(1,0,0,1):-1},'subtraction did not expose the ad term')
    y1={(1,0):1}; y2={(1,0):1,(1,1):1}
    diff={e:y2.get(e,0)-y1.get(e,0) for e in set(y1)|set(y2)}
    diff={e:v for e,v in diff.items() if v}
    require(min(y1)==min(y2)==(1,0),'birational chart negative control has distinct leading values')
    require(min(diff)==(1,1),'birational chart cancellation control failed')
    return {'degrees':counts,'normal_monomials_checked':normal_total}


def wedge_chart(k,n,seq):
    d=len(seq)
    polys={tuple(range(1,k+1)):{(0,)*d:1}}
    # Product of matrices acts rightmost factor first.
    for position in range(d-1,-1,-1):
        i,j=seq[position]
        out={I:dict(p) for I,p in polys.items()}
        for I,p in polys.items():
            if i not in I or j in I:
                continue
            new=list(I)
            new[new.index(i)]=j
            inversions=sum(new[a]>new[b] for a in range(k) for b in range(a+1,k))
            sign=(-1)**inversions
            J=tuple(sorted(new))
            q=out.setdefault(J,{})
            for exponent,coeff in p.items():
                e=list(exponent); e[position]+=1; e=tuple(e)
                q[e]=q.get(e,0)+sign*coeff
                if q[e]==0:
                    del q[e]
        polys={I:p for I,p in out.items() if p}
    return polys


def check_roots():
    examples=[(2,4,[(1,3),(1,4),(2,3),(2,4)]),
              (3,6,[(1,6),(4,6),(5,6),(1,5),(2,5),(4,5),(1,4),(2,4),(3,4)])]
    report=[]
    for k,n,S in examples:
        d=len(S)
        require(d==k*(n-k),'wrong sequence length')
        polys=wedge_chart(k,n,S)
        require(len(polys)==comb(n,k),'a Plucker coordinate vanished identically')
        require(polys[tuple(range(1,k+1))]=={(0,)*d:1},'highest coordinate is not one')
        terms=0
        for I,p in polys.items():
            for a,coefficient in p.items():
                terms+=1
                require(coefficient!=0,'retained zero coefficient')
                require(all(x in (0,1) for x in a),'not multiaffine')
                weight=[0]*n
                for exponent,(i,j) in zip(a,S):
                    weight[i-1]+=exponent
                    weight[j-1]-=exponent
                expected=[int(i<=k)-int(i in I) for i in range(1,n+1)]
                require(weight==expected,'wrong torus weight')
                require(sum(x*(j-i) for x,(i,j) in zip(a,S))==sum(I)-k*(k+1)//2,
                        'wrong root-height homogeneity')
        report.append({'k':k,'n':n,'coordinates':len(polys),'nonzero_terms':terms})
    return report


def check_cube():
    mu=((3,3,3),(3,3,2),(2,2,2),(1,1,1),(3,3,0),
        (2,1,0),(1,1,0),(3,0,0),(2,0,0))
    partitions=[x for x in product(range(4),repeat=3) if x[0]>=x[1]>=x[2]]
    def diagonal(m,l):
        c=Counter(row-col for row in range(3) for col in range(l[row],m[row]))
        return max(c.values(),default=0)
    V=[tuple(diagonal(m,l) for m in mu) for l in partitions]
    c=tuple(Q(x,2) for x in (3,3,2,1,2,1,1,1,1))
    U=((0,1,0,0,-1,-1,0,0,1),(0,0,0,0,1,0,0,-1,-1),
       (0,1,-1,0,0,-1,1,0,0),(0,0,1,0,0,-1,-1,0,0),
       (0,0,0,0,0,1,0,0,-1),(0,0,1,-1,0,0,-1,0,0),
       (0,0,0,1,0,0,-1,0,0),(1,-1,0,0,0,0,0,0,0),
       (0,0,0,0,0,-1,1,0,1))
    require(len(V)==20==len(set(V)),'wrong or repeated degree-one points')
    require(det(U)==1,'cube map is not unimodular')
    for v in V:
        require(all(x in (0,1) for x in matvec(U,v)),'degree-one point outside cube')
    expected=tuple(Q(x,2) for x in (1,0,1,0,0,0,0,0,1))
    require(matvec(U,c)==expected,'wrong fractional image')
    require(all(0<=x<=1 for x in expected),'extra point outside cube')
    require(any(x.denominator==2 for x in expected),'extra point spuriously integral')
    w=(0,-1,1,0,1,0,-1,0,-1)
    for v in V:
        require(dot(w,v) in (0,1),'separating inequality fails at degree one')
    require(dot(w,c)==Q(-1,2),'no strict separation of the extra vertex')
    columns=(0,1,2,3,4,5,9,10,16)
    basis=[[V[j][i] for j in columns] for i in range(9)]
    require(det(basis)==-1,'value points do not supply the asserted lattice basis')
    # Wrong duplicate row must be rejected by a determinant test.
    bad=list(U); bad[0]=bad[1]
    require(det(bad)==0,'singular-map negative control failed')
    return {'partitions_checked':20,'cube_map_determinant':1,'lattice_basis_determinant':-1,
            'extra_vertex_image':[str(x) for x in expected],'separator_extra_value':'-1/2',
            'source_example_scope':'one Gr(3,6) body; not a root-sequence realization'}


def check_braid():
    def mul(A,B):
        return [[sum(A[i][j]*B[j][k] for j in range(3)) for k in range(3)] for i in range(3)]
    def root(i,t):
        M=[[Q(int(j==k)) for k in range(3)] for j in range(3)]
        M[i][i-1]=Q(t)
        return M
    cases=0
    for a,b,c in product(range(-3,4),repeat=3):
        if a+c==0:
            continue
        A=Q(b*c,a+c); B=Q(a+c); C=Q(a*b,a+c)
        left=mul(mul(root(1,a),root(2,b)),root(1,c))
        right=mul(mul(root(2,A),root(1,B)),root(2,C))
        require(left==right,'braid identity failed')
        cases+=1
    M1=((-1,1,1),(1,0,0),(0,1,0));M2=((0,1,0),(0,0,1),(1,1,-1))
    require(det(M1)==det(M2)==1,'a tropical chamber is not unimodular')
    def tau(p):
        a,b,c=p;m=min(a,c);return b+c-m,m,a+b-m
    p=(1,1,2);q=(2,1,1)
    lhs=tuple(a+b for a,b in zip(tau(p),tau(q)))
    rhs=tau(tuple(a+b for a,b in zip(p,q)))
    require(lhs==(3,2,3) and rhs==(2,3,2) and lhs!=rhs,'global-linearity negative control failed')
    for p in product(range(-2,3),repeat=3):
        M=M1 if p[0]<=p[2] else M2
        require(matvec(M,p)==tau(p),'wrong tropical chamber formula')
    return {'rational_identity_samples':cases,'tropical_samples':125,
            'nonlinear_witness_sum_images':list(lhs),'nonlinear_witness_image_sum':list(rhs)}


def main():
    result={'scope':'exact supplemental controls for partial results; not a solution',
            'semigroup':check_semigroup(),'roots':check_roots(),
            'cube':check_cube(),'braid':check_braid()}
    result['checks']=CHECKS
    print(json.dumps(result,indent=2,sort_keys=True)+'\n',end='')

if __name__=='__main__':
    main()
