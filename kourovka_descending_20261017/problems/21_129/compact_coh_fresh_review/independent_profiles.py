#!/usr/bin/env python3
"""Independent Coxeter arithmetic: Leibniz polynomial determinant, exact Q(sqrt5).
No imports from the author's implementation and no Faddeev-LeVerrier recursion.
"""
from fractions import Fraction as F
from itertools import permutations
from math import prod, gcd
from pathlib import Path
import hashlib, json

Z=(F(0),F(0)); O=(F(1),F(0))
def q(a=0,b=0): return F(a),F(b)
def add(x,y): return x[0]+y[0],x[1]+y[1]
def neg(x): return -x[0],-x[1]
def sub(x,y): return add(x,neg(y))
def mul(x,y): return x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def polyadd(p,r):
    out=[Z]*max(len(p),len(r))
    for i,x in enumerate(p):out[i]=add(out[i],x)
    for i,x in enumerate(r):out[i]=add(out[i],x)
    return out

def polymul(p,r):
    out=[Z]*(len(p)+len(r)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(r):out[i+j]=add(out[i+j],mul(x,y))
    return out

def identity(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def mm(a,b):return [[sumq(mul(x,y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sumq(xs):
    out=Z
    for x in xs:out=add(out,x)
    return out

def coxeter(typ):
    n=int(typ[1:]); a=[[q(2) if i==j else Z for j in range(n)] for i in range(n)]
    if typ[0] in 'FH':edges=[(i,i+1) for i in range(n-1)]
    elif typ[0]=='D':edges=[(i,i+1) for i in range(n-2)]+[(n-3,n-1)]
    elif typ[0]=='E':edges=[(i,i+1) for i in range(n-2)]+[(2,n-1)]
    for i,j in edges:a[i][j]=a[j][i]=q(-1)
    if typ[0]=='F':a[2][1]=q(-2)
    if typ[0]=='H':a[0][1]=a[1][0]=q(F(-1,2),F(-1,2))
    columns=[]
    for j in range(n):
        v=[O if i==j else Z for i in range(n)]
        for i in reversed(range(n)):
            value=sumq(mul(a[i][k],v[k]) for k in range(n))
            v[i]=sub(v[i],value)
        columns.append(v)
    return list(map(list,zip(*columns)))

def det_charpoly(c):
    n=len(c); out=[Z]*(n+1); nonzero=0
    for perm in permutations(range(n)):
        if any(i!=j and c[i][j]==Z for i,j in enumerate(perm)):continue
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        p=[q(sign)]
        for i,j in enumerate(perm):
            p=polymul(p,[neg(c[i][j]),O] if i==j else [neg(c[i][j])])
        out=polyadd(out,p); nonzero+=1
    return out, nonzero

def div_monic(p,r):
    p=p[:];out=[Z]*(len(p)-len(r)+1)
    for i in range(len(out)-1,-1,-1):
        out[i]=p[i+len(r)-1]
        for j,v in enumerate(r):p[i+j]=sub(p[i+j],mul(out[i],v))
    assert all(x==Z for x in p)
    return out

def cyclotomic(n):
    p=[q(-1)]+[Z]*(n-1)+[O]
    for d in range(1,n):
        if n%d==0:p=div_monic(p,cyclotomic(d))
    return p

def positive(x):
    a,b=x
    if b==0:return a>0
    if a>=0 and b>=0:return True
    if a<=0 and b<=0:return False
    if a>0:return a*a>5*b*b
    return 5*b*b>a*a

def fmt(x):return str(x[0]) if not x[1] else f'({x[0]})+({x[1]})sqrt(5)'
def main():
    root=Path(__file__).resolve().parent
    author=root.parent/'homological'
    rows=json.loads((author/'profiles.json').read_text())
    results=[]
    for row in rows:
        c=coxeter(row['type']); n=len(c); h=row['h']; pol,terms=det_charpoly(c)
        assert [fmt(x) for x in reversed(pol)]==row['coxeter_characteristic_descending']
        cur=identity(n)
        for k in range(1,h+1):
            cur=mm(cur,c)
            assert (cur==identity(n))==(k==h)
        exp=row['exponents']
        if row['type']=='H4':
            assert polymul(pol,[(a,-b) for a,b in pol])==cyclotomic(30)
            a=q(F(1,2),F(-1,2))
            def g(t):return add(q(t*t-2),mul(a,q(t+1)))
            brackets=[(F(19,10),False),(F(2),True),(F(-7,5),True),(F(-13,10),False)]
            for t,sign in brackets:assert positive(g(t))==sign
        else:
            expected=[O]
            for order in sorted({h//gcd(h,e) for e in exp}):
                primitive=[k*h//order for k in range(1,order+1) if gcd(k,order)==1]
                actual=[e for e in exp if h//gcd(h,e)==order]
                assert sorted(actual)==sorted(primitive*(len(actual)//len(primitive)))
                for _ in range(len(actual)//len(primitive)):expected=polymul(expected,cyclotomic(order))
            assert pol==expected
        poincare=[1]
        for e in exp[1:]:
            t=[0]*(len(poincare)+1)
            for k,v in enumerate(poincare):t[k]+=v;t[k+1]+=e*v
            poincare=t
        chi=sum((-1)**i*x for i,x in enumerate(poincare))
        assert poincare==row['decone_poincare_ascending']
        assert chi==row['decone_euler']
        assert (-1)**(n-1)*chi==prod(e-1 for e in exp[1:])==row['top_l2_betti_Q']>0
        results.append({'type':row['type'],'determinant_nonzero_leibniz_terms':terms,'characteristic_descending':[fmt(x) for x in reversed(pol)],'exact_order':h,'top_l2_from_euler':abs(chi),'passed':True})
    hashes={name:hashlib.sha256((author/name).read_bytes()).hexdigest() for name in ['COARSE_COHOMOLOGY_FILTER.md','PROFILE_TABLE.md','SPECTRAL_FILTER.md','profiles.json','compute_profiles.py']}
    out={'method':'Independent exact Q(sqrt5) reflection action, Leibniz polynomial determinant, exact matrix order, cyclotomic and H4 sign checks','results':results,'author_inputs_sha256':hashes,'passed':True}
    (root/'independent_arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
