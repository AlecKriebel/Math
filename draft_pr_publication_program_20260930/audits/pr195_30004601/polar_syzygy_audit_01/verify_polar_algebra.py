#!/usr/bin/env python3
"""Independent exact rational checks. Standard library only; no original code read.

This corroborates, rather than substitutes for, the open-set argument in REPORT.
The ambient derivatives are formed by the product rule before restriction.
"""
from fractions import Fraction as F
from itertools import combinations
import json

ROWS = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),
        (0,0,1,0),(0,0,0,1),(1,0,1,1)]
SECTIONS = {
    'ternary': [(1,0,0),(0,1,0),(0,0,1),(1,2,3)],
    'binary': [(1,0),(0,1),(2,3),(7,11)],
}

def mons(n,d):
    if n == 1:
        return [(d,)]
    return [(i,)+b for i in range(d,-1,-1) for b in mons(n-1,d-i)]

def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))

def add(p,q,scale=1):
    out = dict(p)
    for e,c in q.items():
        out[e] = out.get(e,F(0)) + scale*c
        if not out[e]:
            del out[e]
    return out

def multiply(p,q):
    out = {}
    for a,c in p.items():
        for b,d in q.items():
            e = plus(a,b)
            out[e] = out.get(e,F(0)) + c*d
    return {e:c for e,c in out.items() if c}

def linear(c):
    n = len(c)
    return {tuple(int(i==j) for i in range(n)):F(c[j]) for j in range(n) if c[j]}

def product(ps,n):
    out = {(0,)*n:F(1)}
    for p in ps:
        out = multiply(out,p)
    return out

def rref(mat):
    a = [[F(v) for v in row] for row in mat]
    height,width = len(a),len(a[0])
    pivots=[]
    row=0
    for col in range(width):
        loc=next((i for i in range(row,height) if a[i][col]),None)
        if loc is None:
            continue
        a[row],a[loc]=a[loc],a[row]
        u=a[row][col]
        a[row]=[v/u for v in a[row]]
        for i in range(height):
            if i != row and a[i][col]:
                u=a[i][col]
                a[i]=[v-u*w for v,w in zip(a[i],a[row])]
        pivots.append(col)
        row+=1
        if row==height:
            break
    return a,pivots

def determinant(a):
    a=[[F(v) for v in row] for row in a]
    out=F(1)
    for j in range(len(a)):
        i=next((i for i in range(j,len(a)) if a[i][j]),None)
        if i is None:
            return F(0)
        if i!=j:
            a[i],a[j]=a[j],a[i]
            out=-out
        v=a[j][j]
        out*=v
        for i in range(j+1,len(a)):
            fac=a[i][j]/v
            for k in range(j+1,len(a)):
                a[i][k]-=fac*a[j][k]
    return out

def certificate(a):
    rr,cols=rref(a)
    # Independent rows of the original matrix, using a transposed rank pass.
    _,rows=rref(list(map(list,zip(*a))))
    rank=len(cols)
    assert len(rows)==rank
    det=determinant([[a[i][j] for j in cols] for i in rows])
    assert det
    free=[j for j in range(len(a[0])) if j not in cols]
    kernel=[]
    for j in free:
        v=[F(0)]*len(a[0])
        v[j]=F(1)
        for i,p in enumerate(cols):
            v[p]=-rr[i][j]
        assert all(sum(x*y for x,y in zip(row,v))==0 for row in a)
        kernel.append([str(x) for x in v])
    # Full independent column span plus exact null vectors proves both bounds.
    return {'rows':len(a),'columns':len(a[0]),'rank':rank,
            'minor_row_indices_zero_based':rows,
            'minor_column_indices_zero_based':cols,'minor_determinant':str(det),
            'kernel_basis':kernel}

def restrict_factors(c):
    n=len(c[0])
    return [tuple(sum(row[j]*c[j][k] for j in range(4)) for k in range(n))
            for row in ROWS]

def ambient_polars(c):
    n=len(c[0]); ls=[linear(v) for v in restrict_factors(c)]
    # Q_j restricted to the section, not derivative of the restricted Q.
    return [sum_polars(j,ls,n) for j in range(4)]

def sum_polars(j,ls,n):
    out={}
    for i,row in enumerate(ROWS):
        if row[j]:
            out=add(out,product(ls[:i]+ls[i+1:],n),row[j])
    return out

def macaulay(polars,n,k):
    bases=mons(n,k)
    columns=[]
    for p in polars:
        for m in mons(n,k-6):
            columns.append({plus(e,m):v for e,v in p.items()})
    return [[col.get(e,F(0)) for col in columns] for e in bases]

def scalar_system(c):
    n=len(c[0]); ls=restrict_factors(c)
    # Unknowns: u_x[0:n],...,u_w[0:n],lambda_0,...,lambda_6.
    a=[]
    for i,row in enumerate(ROWS):
        for k in range(n):
            v=[F(0)]*(4*n+7)
            for j in range(4):
                v[j*n+k]=F(row[j])
            v[4*n+i]=-F(ls[i][k])
            a.append(v)
    a.append([F(0)]*(4*n)+[F(1)]*7)
    return a

def verify():
    out={'arithmetic':'fractions.Fraction; standard library only',
         'ambient_factor_rows':ROWS,'section_results':{}}
    for name,c in SECTIONS.items():
        n=len(c[0]); ls=restrict_factors(c); fs=ambient_polars(c)
        assert all(any(v for v in l) for l in ls)
        pair_certs=[]
        for i,j in combinations(range(7),2):
            witnesses=[]
            for a,b in combinations(range(n),2):
                d=ls[i][a]*ls[j][b]-ls[i][b]*ls[j][a]
                if d:
                    witnesses.append({'coordinate_columns':[a,b],'determinant':d})
            assert witnesses
            pair_certs.append({'factor_pair':[i,j],'first_nonzero_minor':witnesses[0]})
        assert determinant([[c[j][k] for k in [0,1]] for j in [0,1]])
        data={'ambient_restriction_rows':c,'restricted_factors':ls,
              'pairwise_nonproportionality':pair_certs,
              'scalar_syzygy_system':certificate(scalar_system(c)),
              'macaulay':{}}
        for k in ([6,7,8,9] if n==2 else [6,7]):
            cert=certificate(macaulay(fs,n,k))
            cert['quotient_dimension']=len(mons(n,k))-cert['rank']
            data['macaulay'][str(k)]=cert
        # Euler identity survives restriction using all four ambient coordinates.
        euler={}
        for ci,fi in zip(c,fs):
            euler=add(euler,multiply(linear(ci),fi))
        assert euler=={e:7*v for e,v in product([linear(l) for l in ls],n).items()}
        data['restricted_ambient_Euler_identity_verified']=True
        out['section_results'][name]=data
    b=out['section_results']['binary']
    t=out['section_results']['ternary']
    assert b['scalar_syzygy_system']['rank']==14
    assert t['scalar_syzygy_system']['rank']==19
    assert [b['macaulay'][str(k)]['quotient_dimension'] for k in [6,7,8,9]]==[3,1,0,0]
    assert [t['macaulay'][str(k)]['quotient_dimension'] for k in [6,7]]==[24,24]
    c=SECTIONS['binary']; fs=ambient_polars(c)
    aa=[11,11,-73,25]; relation={}
    for v,ci,fi in zip(aa,c,fs):
        relation=add(relation,multiply(linear(ci),fi),v)
    assert not relation
    rho=[1,-11,3]
    assert [sum(rho[i]*c[j][k] for i,j in enumerate([0,2,3])) for k in range(2)]==[0,0]
    out['explicit_binary_relation']={'rho':[1,-11,3],
        'scalar_multipliers_a_b_c_d':[11,-73,25,4],
        'ambient_polar_coefficients':['11*s','11*t','-73*(2*s+3*t)','25*(7*s+11*t)'],
        'exact_polynomial_identity_verified':True}
    out['ternary_X_Z_W_determinant']=str(determinant([SECTIONS['ternary'][i] for i in [0,2,3]]))
    assert out['ternary_X_Z_W_determinant']=='-2'
    return out

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
