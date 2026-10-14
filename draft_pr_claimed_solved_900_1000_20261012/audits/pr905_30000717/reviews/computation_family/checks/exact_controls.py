#!/usr/bin/env python3
"""Independent sparse-polynomial/Fraction controls; no SymPy or packet imports.

Every predicate uses an explicit fail-closed guard.  Finite algebra controls do
not quantify over all SOS certificates.  That deduction is audited in AUDIT.md.
"""
from fractions import Fraction as Q
from itertools import permutations, product
import json
from pathlib import Path

checks = []
def require(ok, label):
    if not ok:
        raise RuntimeError(label)
    checks.append(label)

def clean(p):
    return {e: Q(c) for e, c in p.items() if c}
def add(*ps):
    out = {}
    for p in ps:
        for e,c in p.items():
            out[e] = out.get(e, Q(0)) + c
    return clean(out)
def scale(p, c):
    return clean({e: Q(c)*v for e,v in p.items()})
def mul(p, q):
    out = {}
    for a,c in p.items():
        for b,d in q.items():
            e = tuple(x+y for x,y in zip(a,b))
            out[e] = out.get(e,Q(0)) + c*d
    return clean(out)
def power(p, n):
    if not p and n>0:
        return {}
    one = {(0,)*len(next(iter(p))): Q(1)}
    out = one
    for _ in range(n):
        out = mul(out,p)
    return out
def var(i,n=3):
    return {tuple(int(i==j) for j in range(n)): Q(1)}
def derivative(p,i):
    out={}
    for e,c in p.items():
        if e[i]:
            f=list(e);f[i]-=1
            out[tuple(f)]=c*e[i]
    return clean(out)
def substitute(p, args):
    n=len(next(iter(args[0])))
    out={}
    for e,c in p.items():
        term={(0,)*n:c}
        for base,d in zip(args,e):
            if d:
                term=mul(term,power(base,d))
        out=add(out,term)
    return out
def line(p,v):
    out={}
    for e,c in p.items():
        val=c
        for a,d in zip(v,e): val*=Q(a)**d
        degree=sum(e)
        out[(degree,)]=out.get((degree,),Q(0))+val
    return clean(out)
def evaluate(p,v):
    return sum(line(p,v).values(),Q(0))
def matrix_rank(A):
    B=[[Q(x) for x in row] for row in A]
    r=0
    for j in range(len(B[0])):
        piv=next((i for i in range(r,len(B)) if B[i][j]),None)
        if piv is None: continue
        B[r],B[piv]=B[piv],B[r]
        z=B[r][j];B[r]=[x/z for x in B[r]]
        for i in range(len(B)):
            if i!=r:
                z=B[i][j];B[i]=[x-z*y for x,y in zip(B[i],B[r])]
        r+=1
        if r==len(B): break
    return r
def determinant(A):
    B=[[Q(x) for x in row] for row in A];out=Q(1)
    for j in range(len(B)):
        piv=next((i for i in range(j,len(B)) if B[i][j]),None)
        if piv is None:return Q(0)
        if piv!=j:B[piv],B[j]=B[j],B[piv];out=-out
        z=B[j][j];out*=z
        for i in range(j+1,len(B)):
            f=B[i][j]/z
            B[i]=[x-f*y for x,y in zip(B[i],B[j])]
    return out
def serial(p):
    return [{'exponents':list(e),'coefficient':str(c)} for e,c in sorted(p.items())]

X=[var(i) for i in range(3)]
R=add(*(power(v,6) for v in X),
      *(scale(mul(power(u,4),power(v,2)),-1) for u,v in permutations(X,2)),
      scale(mul(mul(power(X[0],2),power(X[1],2)),power(X[2],2)),3))
F=add(*(power(v,3) for v in X),
      *(scale(mul(power(u,2),v),-1) for u,v in permutations(X,2)),
      scale(mul(mul(X[0],X[1]),X[2]),3))
a,b,c=X
schur=add(mul(power(add(a,scale(b,-1)),2),add(a,b,scale(c,-1))),
          mul(mul(c,add(a,scale(c,-1))),add(b,scale(c,-1))))
require(F==schur,'Schur ordered nonnegativity identity, sparse coefficients')
require(substitute(F,[power(v,2) for v in X])==R,'Square specialization gives Robinson sextic')
for perm in permutations(range(3)):
    require(substitute(R,[X[i] for i in perm])==R,'Robinson coordinate symmetry '+str(perm))
for signs in product((-1,1),repeat=3):
    require(substitute(R,[scale(v,e) for v,e in zip(X,signs)])==R,'Robinson sign symmetry '+str(signs))
# Let a=c+w+u, b=c+w. Nonnegative coefficients directly certify ordered case.
u,w,c=X
ordered=substitute(F,[add(c,w,u),add(c,w),c])
require(all(v>=0 for v in ordered.values()),'Ordered nonnegative-variable expansion has nonnegative coefficients')
require(ordered=={(2,0,1):Q(1),(1,1,1):Q(1),(0,2,1):Q(1),(3,0,0):Q(1),(2,1,0):Q(2)},'Ordered expansion matches five exact monomials')

Z=[(1,s,t) for s,t in product((1,-1),repeat=2)]+[(1,s,0) for s in (1,-1)]+[(1,0,t) for t in (1,-1)]+[(0,1,t) for t in (1,-1)]
require(len(Z)==len(set(Z))==10,'Ten distinct zero representatives')
for i,v in enumerate(Z):
    for w in Z[i+1:]:
        require(any(v[a]*w[b]!=v[b]*w[a] for a in range(3) for b in range(a+1,3)), 'Projectively distinct zero directions '+str((v,w)))
grad=[derivative(R,i) for i in range(3)]
K=[mul(X[j],grad[i]) for i in range(3) for j in range(3) if i!=j]
J=[add(mul(X[j],grad[i]),scale(mul(X[i],grad[j]),-1)) for i in range(3) for j in range(i+1,3)]
for v in Z:
    require(line(R,v)=={},'R identically zero on whole real line '+str(v))
    require(all(line(g,v)=={} for g in grad),'Gradient identically zero on whole line '+str(v))
    require(all(line(g,v)=={} for g in J+K),'J and K generators identically zero on whole line '+str(v))
for i in range(3):
    v=tuple(int(j==i) for j in range(3))
    require(line(R,v)=={(6,):Q(1)},'R=t^6 on axis '+str(i))
    require(all(line(g,v)=={} for g in J+K),'J and K contain axis '+str(i))
    require([line(g,v) for g in grad]==[{(5,):Q(6)} if j==i else {} for j in range(3)],'Gradient=6t^5 in axis direction '+str(i))
require(add(*(mul(v,g) for v,g in zip(X,grad)))==scale(R,6),'Euler identity for actual gradient ideal')

evaluation=[]
for d in range(5):
    basis=[(i,j,d-i-j) for i in range(d+1) for j in range(d-i+1)]
    matrix=[[int(evaluate({m:Q(1)},v)) for m in basis] for v in Z]
    rank=matrix_rank(matrix)
    if d<=3:require(rank==len(basis),'Degree '+str(d)+' full column rank via Fraction Gaussian elimination')
    else:require(rank==10<len(basis),'Degree four is not injective; extrapolation forbidden')
    rec={'degree':d,'basis':basis,'matrix':matrix,'rank':rank,'dimension':len(basis)}
    if d==3:
        det=determinant(matrix)
        require(det==Q(-128),'Cubic determinant exactly -128 via Fraction elimination')
        rec['determinant']=int(det)
    evaluation.append(rec)
# A nonzero quartic vanishes on all ten directions but not identically.
quartic=mul(mul(X[0],X[1]),add(power(X[0],2),scale(power(X[1],2),-1)))
require(bool(quartic) and all(evaluate(quartic,v)==0 for v in Z),'Explicit degree-four nonzero kernel element xy(x^2-y^2)')
require(line(quartic,(2,1,0))=={(4,):Q(6)},'Quartic kernel polynomial is nonzero off the zero directions')

# Literal Q control: G1=2y^2(xy-1), G2=2x^2(xy-1)+2xy.
x,y=var(0,2),var(1,2);one={(0,0):Q(1)}
xy=mul(x,y)
q=add(power(add(one,scale(xy,-1)),2),power(y,2),scale(one,Q(-1,2)))
k1=mul(y,derivative(q,0));k2=mul(x,derivative(q,1))
require(k1==scale(mul(power(y,2),add(xy,scale(one,-1))),2),'Q first product factorization')
require(k2==add(scale(mul(power(x,2),add(xy,scale(one,-1))),2),scale(xy,2)),'Q second product factorization')
require(substitute(k2,[var(0,1),{}])=={(2,):Q(-2)},'Q y=0 branch forces x=0 over reals')
require(evaluate(q,(0,0))==Q(1,2),'Q origin value +1/2')
require(evaluate(q,(2,Q(1,2)))==Q(-1,4),'Q negative witness -1/4')
# Evaluate Laurent x=t^-1,y=t as dictionary exponents allowed to be negative.
require(substitute(q,[{(-1,):Q(1)},{(1,):Q(1)}])=={(2,):Q(1),(0,):Q(-1,2)},'Q reciprocal path t^2-1/2')
require(substitute(k2,[{(-1,):Q(1)},{(1,):Q(1)}])=={(0,):Q(2)},'Q xy=1 branch impossible, second product is 2')

# Real-square leading coefficients cannot cancel; negative coefficients or
# complex coefficients would invalidate the analytic lemma (see AUDIT.md).
for degree in (1,2,3,4,17,100):
    qs=[{(degree,):Q(1),(0,):Q(2)},{(degree,):Q(-3)}]
    sq=add(*(mul(p,p) for p in qs))
    require(sq[(2*degree,)]==Q(10),'Real SOS positive leading coefficient at arbitrary test degree '+str(degree))
complex_cancel_example='(t^D)^2 + (i*t^D)^2 = 0; real coefficient assumption essential'
result={'verdict':'PASS_INDEPENDENT_FINITE_EXACT_CONTROLS','check_count':len(checks),'checks':checks,
        'arithmetic':'Python integers and fractions.Fraction; no symbolic-algebra dependency or packet imports',
        'Robinson':serial(R),'ordered_expansion':serial(ordered),'zero_directions':Z,
        'homogeneous_evaluation':evaluation,'quartic_kernel_example':serial(quartic),
        'literal_Q':serial(q),'boundary_complex_coefficients':complex_cancel_example,
        'scope':'Finite exact algebra only. Universal epsilon, finite SOS and unbounded-degree conclusions require the separately audited mathematical argument.'}
print(json.dumps(result,indent=2,sort_keys=True))
