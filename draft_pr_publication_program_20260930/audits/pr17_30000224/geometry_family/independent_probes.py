#!/usr/bin/env python3
"""Independent exact probes, standard library only; no frozen verifier import."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
checks = []

def check(label, ok):
    if not ok:
        raise AssertionError(label)
    checks.append(label)

def add(p, q):
    r = dict(p)
    for m, c in q.items():
        r[m] = r.get(m, F(0)) + c
        if not r[m]:
            del r[m]
    return r

def scale(p, c):
    return {m: c*v for m, v in p.items() if c*v}

def mul(p, q):
    r = {}
    for a, c in p.items():
        for b, d in q.items():
            m = tuple(x+y for x, y in zip(a,b))
            r[m] = r.get(m, F(0)) + c*d
    return {m:c for m,c in r.items() if c}

def mono(m, c=1):
    return {tuple(m): F(c)} if c else {}

def sub(p,q):
    return add(p,scale(q,F(-1)))

def key(m, order):
    return m if order == 'lex' else (sum(m), m)

def lt(p, order):
    m=max(p,key=lambda m:key(m,order))
    return m,p[m]

def divides(a,b):
    return all(x<=y for x,y in zip(a,b))

def rem(p, basis, order='lex'):
    r={}
    p=dict(p)
    while p:
        a,c=lt(p,order)
        for g in basis:
            b,d=lt(g,order)
            if divides(b,a):
                p=sub(p,mul(mono(tuple(x-y for x,y in zip(a,b)),c/d),g))
                break
        else:
            r=add(r,mono(a,c))
            del p[a]
    return r

def spoly(p,q,order='lex'):
    a,c=lt(p,order);b,d=lt(q,order)
    l=tuple(max(x,y) for x,y in zip(a,b))
    return sub(mul(mono(tuple(x-y for x,y in zip(l,a)),1/c),p),
               mul(mono(tuple(x-y for x,y in zip(l,b)),1/d),q))

def gb(polys,order='lex'):
    basis=[]
    for p in polys:
        p=rem(p,basis,order)
        if p:
            basis.append(scale(p,1/lt(p,order)[1]))
    pairs=list(combinations(range(len(basis)),2))
    count=0
    while pairs:
        i,j=pairs.pop(0)
        count+=1
        if count>20000:
            raise RuntimeError('Buchberger pair limit')
        a=lt(basis[i],order)[0];b=lt(basis[j],order)[0]
        if all(min(x,y)==0 for x,y in zip(a,b)):
            continue
        p=rem(spoly(basis[i],basis[j],order),basis,order)
        if p:
            p=scale(p,1/lt(p,order)[1])
            n=len(basis)
            pairs.extend((k,n) for k in range(n))
            basis.append(p)
    check('Buchberger all pairs reduce to zero '+str(len(checks)),
          all(not rem(spoly(p,q,order),basis,order) for p,q in combinations(basis,2)))
    return basis

def fmt(p,names):
    return [{'exponents':list(m),'coefficient':str(c)}
            for m,c in sorted(p.items(),reverse=True)]

def intersection(A,B,nvars):
    one=mono((0,)*(nvars+1));t=mono((1,)+(0,)*nvars)
    lift=lambda p:{(0,)+m:c for m,c in p.items()}
    G=gb([mul(t,lift(p)) for p in A]+[mul(sub(one,t),lift(p)) for p in B])
    return [{m[1:]:c for m,c in p.items()} for p in G if all(m[0]==0 for m in p)]

def same_ideal(A,B,order='lex'):
    GA=gb(A,order);GB=gb(B,order)
    return all(not rem(p,GB,order) for p in A) and all(not rem(p,GA,order) for p in B)

def rref(A):
    A=[[F(x) for x in row] for row in A]
    nr=len(A);nc=len(A[0]) if A else 0
    piv=[];r=0
    for j in range(nc):
        k=next((k for k in range(r,nr) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        v=A[r][j];A[r]=[x/v for x in A[r]]
        for k in range(nr):
            if k!=r and A[k][j]:
                v=A[k][j];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
        piv.append(j);r+=1
        if r==nr:break
    return A,piv

def kernel(A):
    E,piv=rref(A);nc=len(A[0]);out=[]
    for j in range(nc):
        if j in piv:continue
        v=[F(0)]*nc;v[j]=1
        for i,k in enumerate(piv):v[k]=-E[i][j]
        out.append(v)
    return out

def derivative(p,j):
    out={}
    for m,c in p.items():
        if m[j]:
            n=list(m);n[j]-=1
            out[tuple(n)]=c*m[j]
    return out

def unidiv(p,q):
    p=dict(p);out={}
    while p and max(p)>=max(q):
        d=max(p)-max(q);c=p[max(p)]/q[max(q)]
        out[d]=out.get(d,F(0))+c
        for e,v in q.items():
            p[e+d]=p.get(e+d,F(0))-c*v
            if not p[e+d]:del p[e+d]
    return out,p

def unigcd(polys):
    g={}
    for p in polys:
        while p:
            _,r=unidiv(g,p);g,p=p,r
    return g

# Reconstruct Jacobian directly from parametrizing polynomials, then solve
# independent coefficient systems (the frozen U and verification script are unused).
f=[mono((4,0)),mono((3,1)),mono((1,3)),mono((0,4))]
J=[[derivative(p,j) for p in f] for j in range(2)]
check('Jacobian first endpoint minor is four s to sixth',sub(mul(J[0][0],J[1][1]),mul(J[0][1],J[1][0]))==mono((6,0),4))
check('Jacobian second endpoint minor is four t to sixth',sub(mul(J[0][2],J[1][3]),mul(J[0][3],J[1][2]))==mono((0,6),4))
check('Euler contraction is the invertible scalar four',all(add(mul(mono((1,0)),J[0][k]),mul(mono((0,1)),J[1][k]))==scale(f[k],4) for k in range(4)))
syzygy_slices=[];frame=None
for d in range(9):
    inds=[(d-i,i) for i in range(d+1)]
    rows=[(j,(d+3-i,i)) for j in range(2) for i in range(d+4)]
    cols=[(j,m) for j in range(4) for m in inds]
    A=[]
    for j,m in rows:
        A.append([mul(J[j][k],mono(a)).get(m,F(0)) for k,a in cols])
    K=kernel(A)
    check('Jacobian syzygy slice degree '+str(d),len(K)==max(0,2*(d-2)))
    syzygy_slices.append({'coefficient_degree':d,'matrix_shape':[len(A),len(cols)],'kernel_dimension':len(K)})
    if d==3:
        frame=[[{m:v[k*(d+1)+i] for i,m in enumerate(inds) if v[k*(d+1)+i]} for k in range(4)] for v in K]
check('Reconstructed frame directly annihilates both Jacobian rows',all(not add(add(mul(J[j][0],v[0]),mul(J[j][1],v[1])),add(mul(J[j][2],v[2]),mul(J[j][3],v[3]))) for j in range(2) for v in frame))
minors=[sub(mul(frame[0][i],frame[1][j]),mul(frame[1][i],frame[0][j])) for i,j in combinations(range(4),2)]
chart_minors=[{m[0]:c for m,c in p.items()} for p in minors]
check('Derived cubic frame has no rank drop on t nonzero',max(unigcd(chart_minors))==0)
check('Derived cubic frame has no rank drop at t zero',any(p.get((6,0),0) for p in minors))
gradient=[f[3],scale(f[2],-1),scale(f[1],-1),f[0]]
linear=[(1,0),(0,1)]
system=[]
for k in range(4):
    for m in [(4-i,i) for i in range(5)]:
        system.append([mul(frame[j][k],mono(a)).get(m,0) for j in range(2) for a in linear]+[gradient[k].get(m,0)])
E,piv=rref(system)
check('Quadric differential belongs to derived conormal frame',4 not in piv)
solution=[F(0)]*4
for i,k in enumerate(piv):solution[k]=E[i][4]
check('Quadric conormal subline has no common zero',solution[0]*solution[3]-solution[1]*solution[2]!=0)

# Reconstruct the exact toric ideal from a Groebner/Hilbert-series certificate.
q=sub(mono((1,0,0,1)),mono((0,1,1,0)))
Fcurve=sub(mono((0,3,0,0)),mono((2,0,1,0)))
g=sub(mono((1,0,2,0)),mono((0,2,0,1)))
h=sub(mono((0,0,3,0)),mono((0,1,0,2)))
curve=[q,Fcurve,g,h]
Gcurve=gb(curve,'grlex')
LM=[lt(p,'grlex')[0] for p in Gcurve]
LM=list(dict.fromkeys(LM))
LM=[m for m in LM if not any(n!=m and divides(n,m) for n in LM)]
num={0:1}
for k in range(1,len(LM)+1):
    for group in combinations(LM,k):
        degree=sum(max(m[j] for m in group) for j in range(4))
        num[degree]=num.get(degree,0)+(-1)**k
num={k:v for k,v in num.items() if v}
target={}
for i,a in {0:1,1:2,2:2,3:-1}.items():
    for j,b in {0:1,1:-2,2:1}.items():
        target[i+j]=target.get(i+j,0)+a*b
target={k:v for k,v in target.items() if v}
check('Toric ideal universal Hilbert-series numerator',num==target)
check('Degree eight semigroup full interval',set(a+b for a in (0,1,3,4) for b in (0,1,3,4))==set(range(9)))

# Independent exact linkage/intersection/colon computation.
lines=[mono((1,0,1,0)),mono((1,0,0,1)),mono((0,1,1,0)),mono((0,1,0,1))]
CI=[q,g]
GI=intersection(lines,curve,4)
check('Two skew lines intersect quartic ideal in claimed CI',same_ideal(GI,CI))
wy=lines[0]
intersection_wy=intersection(CI,[wy],4)
colon_wy=[]
for p in intersection_wy:
    check('Every intersection-wy generator divisible by wy',all(divides((1,0,1,0),m) for m in p))
    colon_wy.append({tuple(x-y for x,y in zip(m,(1,0,1,0))):c for m,c in p.items()})
check('Claimed CI colon wy equals the quartic ideal',same_ideal(colon_wy,curve))
GCI=gb(CI)
check('Quartic ideal times entire skew-line ideal belongs to CI',all(not rem(mul(a,b),GCI) for a in curve for b in lines))
check('Skew-line generator wy is outside quartic ideal',bool(rem(wy,Gcurve,'grlex')))

# Segre factorization from substitution, plus the localized principal equation.
def subst(p,values):
    n=len(next(iter(values[0])))
    out={}
    for m,c in p.items():
        term=mono((0,)*n,c)
        for i,e in enumerate(m):
            for _ in range(e):term=mul(term,values[i])
        out=add(out,term)
    return out
segre=[mono((1,0,1,0)),mono((1,0,0,1)),mono((0,1,1,0)),mono((0,1,0,1))]
segrecurve=sub(mono((0,1,3,0)),mono((1,0,0,3)))
check('Segre quadric substitution',not subst(q,segre))
check('Segre cubic factorization',subst(g,segre)==mul(mono((1,1,0,0)),segrecurve))
localized=[mono((1,0,0,0)),mono((0,1,0,0)),mono((0,0,1,0)),mono((-1,1,1,0))]
check('Localized cubic g is minus y over w times F',subst(g,localized)==mul(mono((-1,0,1,0),-1),Fcurve))
check('Localized cubic h is minus y squared over w squared times F',subst(h,localized)==mul(mono((-2,0,2,0),-1),Fcurve))

# Cech quotient exponent enumeration, separately from a black-box cohomology formula.
def cech_h0(n):return list(range(n+1)) if n>=0 else []
def cech_h1(n):return list(range(n+1,0)) if n<=-2 else []
cohomology=[]
for r in range(1,21):
    basis=[(a,b) for a in cech_h0(0) for b in cech_h1(-2*r)]
    check('Cech obstruction for divisor multiplicity '+str(r),len(basis)==2*r-1)
    cohomology.append({'r':r,'H1_dimension':len(basis),'second_chart_exponents':[b for a,b in basis],
                       'section_dimension_at_k_r':(r+1)**2+len(basis),
                       'quadric_coordinate_dimension_at_k_r':(r+1)**2})
double_sections=[]
for e in range(-7,21):
    dim=len(cech_h0(e+8))+len(cech_h0(8))
    check('Double-structure quadratic section bound e='+str(e),not cech_h1(e+8) and dim==e+18 and dim>=11)
    double_sections.append({'e':e,'h0_twist_2':dim,'ambient_quadrics':10})

# Exact warning example for total-degree degeneration, preserving the same radical.
u2=mono((2,0,0));uvplusv=add(mono((1,1,0)),mono((0,0,1)))
Gdeg=gb([u2,uvplusv],'grlex')
check('Every Groebner basis top homogeneous part is a monomial',all(sum(sum(m)==sum(lt(p,'grlex')[0]) for m in p)==1 for p in Gdeg))
initial=[mono(lt(p,'grlex')[0]) for p in Gdeg]
expected=[mono((2,0,0)),mono((1,1,0)),mono((1,0,1)),mono((0,0,2))]
check('Highest-degree initial ideal in CM degeneration warning',same_ideal(initial,expected,'grlex'))
check('Nonzero socle x survives in initial quotient',bool(rem(mono((1,0,0)),initial,'grlex')))
check('All three variables annihilate socle x',all(not rem(mul(mono((1,0,0)),mono(v)),initial,'grlex') for v in [(1,0,0),(0,1,0),(0,0,1)]))
homogenized=[mono((2,0,0,0)),add(mono((1,1,0,0)),mono((0,0,1,1))),mono((1,0,1,0)),mono((0,0,2,0))]
check('Explicit flat homogenization family is a Groebner basis',all(not rem(spoly(p,q,'grlex'),homogenized,'grlex') for p,q in combinations(homogenized,2)))
check('Homogenization leading monomials contain no family parameter',all(lt(p,'grlex')[0][3]==0 for p in homogenized))

result={'scope':'Exact finite probes accompany universal proofs; they do not settle unrestricted thickenings.',
        'assertions_passed':len(checks),'checks':checks,'syzygy_slices':syzygy_slices,
        'derived_cubic_frame':[[fmt(p,['s','t']) for p in v] for v in frame],
        'quadric_gradient_linear_coefficients':list(map(str,solution)),
        'toric_leading_monomials':LM,'toric_hilbert_numerator_over_1_minus_T_pow_4':num,
        'toric_groebner_basis':[fmt(p,['w','x','y','z']) for p in Gcurve],
        'complete_intersection_groebner_basis':[fmt(p,['w','x','y','z']) for p in GCI],
        'intersection_generators':[fmt(p,['w','x','y','z']) for p in GI],
        'colon_wy_generators':[fmt(p,['w','x','y','z']) for p in colon_wy],
        'degeneration_groebner_basis':[fmt(p,['x','y','z']) for p in Gdeg],
        'cohomology_samples':cohomology,'homogeneous_double_section_samples':double_sections,
        'linkage':'Exact Groebner certificates: I intersect a=(q,g), (q,g):wy=a, a I subset(q,g), wy outside a. Thus (q,g):I=a.',
        'degeneration_warning':'K[x,y,z]/(x^2,xy+z) is CM (isomorphic to K[x,y]/x^2), radical(x,z); highest-degree initial ideal (x^2,xy,xz,z^2) has nonzero m-socle x, same radical, depth zero. The family (x^2,xy+z*t,xz,z^2) is free over K[t] on its standard monomials, hence flat.'}
(HERE/'probe_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'assertions_passed':len(checks),'syzygy_slices':syzygy_slices,'toric_LM':LM,'linkage':'verified','degeneration_warning':'verified'},indent=2))
