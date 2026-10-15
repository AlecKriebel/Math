#!/usr/bin/env python3
"""Independent exact controls for the scoped EP653 construction obstructions."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
import sympy as s
checks={}
def ck(name,b):
    assert bool(b),name
    checks[name]='PASS'
def d2(p,q): return sum((a-b)**2 for a,b in zip(p,q))
def spectrum(P):
    if len(P)!=len(set(P)): raise AssertionError('duplicate point')
    values=[len({d2(p,q) for q in P if p!=q}) for p in P]
    return values, {len(P)-1-v for v in values}
def isgeneric(blocks):
    P=sum(blocks,[])
    if len(P)!=len(set(P)):return False
    for i,B in enumerate(blocks):
        ext=sum([C for j,C in enumerate(blocks) if j!=i],[])
        for p in B:
            v=[d2(p,q) for q in ext]
            if len(set(v))!=len(v):return False
            if set(v)&{d2(p,q) for q in B if p!=q}:return False
    return True
# Symbolic nonzero-polynomial checks cover all types of forbidden equality
# for a pin in one of three independently translated blocks.
T=s.symbols('x0 y0 x1 y1 x2 y2');xy=[s.Matrix(T[2*i:2*i+2]) for i in range(3)]
seeds=[[(0,0),(1,0),(0,2)],[(0,0),(1,1),(3,0)],[(0,0),(2,-1)]]
pts=[(i,tuple(xy[i]+s.Matrix(p))) for i,B in enumerate(seeds) for p in B]
poly_count=0
for a,(i,p) in enumerate(pts):
    for b,(j,q) in enumerate(pts):
        if b==a:continue
        for c,(l,r) in enumerate(pts):
            if c<=b or c==a or (j==i and l==i):continue
            poly=s.Poly(s.expand(d2(p,q)-d2(p,r)),*T)
            ck(f'proper_forbidden_equality_{a}_{b}_{c}',not poly.is_zero and poly.total_degree() in (1,2));poly_count+=1
# Deterministic admissible and inadmissible translations: no floating arithmetic.
A=[(0,0),(1,0),(0,2)]
B=[(j,0) for j in range(5)]
good=bad=0
for a,b in product(range(-5,6),repeat=2):
    C=[(x+a,y+b) for x,y in B]
    if not isgeneric([A,C]):bad+=1;continue
    values,D=spectrum(A+C);va,Da=spectrum(A);vb,Db=spectrum(B)
    ck(f'glue_counts_{a}_{b}',values==[len(B)+v for v in va]+[len(A)+v for v in vb])
    ck(f'glue_deficits_{a}_{b}',D==Da|Db);good+=1
ck('generic_grid_both_types',good>0 and bad>0)
square=[(0,0),(1,0),(0,1),(1,1)]
ck('nongeneric_square_changes_deficits',spectrum(square)[1]=={1} and spectrum(square[:2])[1]=={0} and not isgeneric([square[:2],square[2:]]))
# Sharp circular constructions use exact rational rotations. With t=1/(4n),
# theta=2 arctan(t) satisfies (n-1)theta<1/2<pi, so no chord folding occurs.
for n in range(2,31):
    t=F(1,4*n);c=(1-t*t)/(1+t*t);ss=2*t/(1+t*t)
    P=[];x,y=F(1),F(0)
    for _ in range(n):P.append((x,y));x,y=c*x-ss*y,ss*x+c*y
    values,D=spectrum(P)
    ck(f'circle_distinct_{n}',len(set(P))==n)
    ck(f'circle_unit_radius_{n}',all(x*x+y*y==1 for x,y in P))
    ck(f'circle_exact_counts_{n}',values==[max(i,n-1-i) for i in range(n)])
    ck(f'circle_attainment_{n}',len(D)==(n+1)//2)
    values_line,Dline=spectrum([(j,0) for j in range(n)])
    ck(f'line_attainment_{n}',values_line==values and len(Dline)==(n+1)//2)
    # Include a center pin as an exceptional point, a potentially extreme case.
    for t_exc in range(1,4):
        X=P+[(F(0),F(0))]+[(F(3+j),F(5+j*j)) for j in range(t_exc-1)]
        vals,dd=spectrum(X);N=len(X);m=n
        a=(m-1+1)//2;bound=min(N-1,N+t_exc-a)
        ck(f'exception_bound_{n}_{t_exc}',len(dd)<=bound)
        ck(f'center_pinned_count_{n}_{t_exc}',vals[n]<=t_exc)
        for j in range(min(N,4)):
            for k in range(j+1,min(N,4)):
                ck(f'two_pin_{n}_{t_exc}_{j}_{k}',N-2<=2*vals[j]*vals[k])
        h=N-len(dd)
        ck(f'defect_bound_{n}_{t_exc}',N-2<=2*h*(h+1))
# Algebraic off-by-one and exceptional-support checks.
n=s.symbols('n',integer=True,positive=True);h=s.symbols('h',real=True)
ck('quadratic_root',s.simplify(2*h*(h+1)-(n-2)).subs(h,(s.sqrt(2*n-3)-1)/2).simplify()==0)
for N in range(2,101):
    ck(f'line_interval_cardinality_{N}',N-((N-1+1)//2)==(N+1)//2)
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'proper_polynomial_checks':poly_count,'generic_grid_translations':good,'nongeneric_grid_translations':bad,'scope':'Exact finite controls only; no asymptotic resolution or historical-priority certification.','checks':checks,'reviewed_sha256':hashlib.sha256(Path(__file__).with_name('PARTIAL.md').read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
