"""Source-first exact controls, created without candidate/audit/history exposure."""
from fractions import Fraction as F
from itertools import combinations, product
from functools import reduce
from math import gcd
import json

def norm(v):
    assert any(v)
    den=1
    for a in v:
        a=F(a); den=den*a.denominator//gcd(den,a.denominator)
    vals=[int(F(a)*den) for a in v]
    g=reduce(gcd,(abs(a) for a in vals))
    vals=[a//g for a in vals]
    if next(a for a in vals if a)<0: vals=[-a for a in vals]
    return tuple(vals)

def cross(a,b):
    return norm((a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]))

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def arrange(lines):
    lines=sorted(set(map(norm,lines)))
    pts=sorted(set(cross(a,b) for a,b in combinations(lines,2)))
    covers=sorted(set(cross(a,b) for a,b in combinations(pts,2))) if len(pts)>1 else [lines[0]]
    supports={l: [i for i,p in enumerate(pts) if dot(l,p)==0] for l in covers}
    if not pts: return {'n':0,'k_all':0,'k_arr':0,'points':[]}
    return dict(n=len(pts),k_all=max(map(len,supports.values())),k_arr=max(sum(dot(l,p)==0 for p in pts) for l in lines),points=pts,lines=lines,covers=covers,supports=supports)

def certify(data,weights,dual):
    cover=[sum(w for l,w in weights.items() if dot(l,p)==0) for p in data['points']]
    assert min(cover)>=1
    assert all(sum(dual[i] for i in s)<=1 for s in data['supports'].values())
    primal=sum(weights.values()); dobj=sum(dual)
    assert primal==dobj
    return dict(primal=str(primal),dual=str(dobj),coverage=list(map(str,cover)),weights={str(l):str(w) for l,w in weights.items()},point_dual=list(map(str,dual)))

def balanced_min_square(M,n):
    q,r=divmod(M,n)
    return (n-r)*q*q+r*(q+1)*(q+1)

out={}
fermat2=arrange([(1,-1,0),(1,1,0),(0,1,-1),(0,1,1),(1,0,-1),(1,0,1)])
axes=[(1,0,0),(0,1,0),(0,0,1)]
weights={l:F(1,3) for l in fermat2['lines']}
weights.update({l:F(1,6) for l in axes})
dual=[F(1,2) if p in [(1,0,0),(0,1,0),(0,0,1)] else F(1,4) for p in fermat2['points']]
out['fermat2']=dict(n=fermat2['n'],k_all=fermat2['k_all'],k_arr=fermat2['k_arr'],points=fermat2['points'],certificate=certify(fermat2,weights,dual),arrangement_only_uniform_cost='3')

# Exact maximum multiplicity under the genus budget; relaxation alone, no existence claim.
genus=[]
for n in range(1,10):
    for d in range(1,13):
        budget=(d-1)*(d-2)
        maxM=max(M for M in range(n*d+1) if balanced_min_square(M,n)-M<=budget)
        genus.append(dict(n=n,d=d,budget=budget,maxM=maxM))
out['balanced_genus_controls']=genus

# Every enumerated vector checks both exact balancing and Cauchy. This check is independent of curves.
count=0
for n in range(1,6):
    minima={}
    for m in product(range(5),repeat=n):
        M=sum(m); sq=sum(a*a for a in m)
        minima[M]=min(minima.get(M,sq),sq)
        assert n*sq>=M*M
        count+=1
    for M in range(4*n+1): assert minima[M]==balanced_min_square(M,n)
out['genus_vector_checks']=count

# Polynomial for a strict violation M >= k*d+1: n times Cauchy-genus deficit.
polys=[]
for n,k in [(3,2),(7,3),(12,4),(16,4),(9,3),(25,5),(17,4)]:
    a=k*k-n; b=2*k+n*(3-k); c=1-3*n
    for d in range(1,101):
        M=k*d+1
        assert a*d*d+b*d+c==M*M-n*M-n*(d*d-3*d+2)
    candidates=[d for d in range(2,101) if a*d*d+b*d+c<=0]
    polys.append(dict(n=n,k=k,a=a,b=b,c=c,allowed_degrees_through_100=candidates,finite_from_positive_a=a>0))
out['strict_genus_polynomials']=polys
print(json.dumps(out,sort_keys=True,indent=2))
