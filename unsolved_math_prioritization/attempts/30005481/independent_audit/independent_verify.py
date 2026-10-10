#!/usr/bin/env python3
"""Independent exact review. Does not import or execute the author verifier.

Sparse polynomial and PSD checks use Python Fraction arithmetic. SymPy is used
only for univariate-in-epsilon identities, a Sylvester determinant, and rational
root isolation. Input files are read-only.
"""
from fractions import Fraction as R
from pathlib import Path
from itertools import permutations
import hashlib, json, re
import sympy as S
ROOT=Path(__file__).resolve().parents[1]/'authored'
checks=[]
def ok(test,name):
    if not test: raise AssertionError(name)
    checks.append(name)
def clean(p): return {k:R(v) for k,v in p.items() if v}
def add(p,q):
    out=p.copy()
    for k,v in q.items(): out[k]=out.get(k,R(0))+v
    return clean(out)
def scale(p,c): return clean({k:v*c for k,v in p.items()})
def mul(p,q):
    out={}
    for a,u in p.items():
        for b,v in q.items():
            k=tuple(x+y for x,y in zip(a,b));out[k]=out.get(k,R(0))+u*v
    return clean(out)
def power(p,k,n):
    a={(0,)*n:R(1)}
    for _ in range(k):a=mul(a,p)
    return a
def var(n,i): return {tuple(int(k==i) for k in range(n)):R(1)}
def const(n,c): return clean({(0,)*n:R(c)})
def direction(p,v):
    out={}
    for k,c in p.items():
        for i,a in enumerate(k):
            if a and v[i]:
                z=list(k);z[i]-=1;z=tuple(z)
                out[z]=out.get(z,R(0))+c*a*v[i]
    return clean(out)
def substitute(p,replacements,n):
    out={}
    for k,c in p.items():
        v=const(n,c)
        for r,a in zip(replacements,k):v=mul(v,power(r,a,n))
        out=add(out,v)
    return out
def elementary(variables,n):
    e=[const(n,1)]+[{} for _ in variables]
    for x in variables:
        for i in range(len(variables),0,-1):e[i]=add(e[i],mul(x,e[i-1]))
    return e
def expr_to_sparse(expr,variables):
    return {tuple(k):R(str(v)) for k,v in S.Poly(expr,*variables).terms()}
def sparse_to_sympy(p,variables):
    return sum(S.Rational(c.numerator,c.denominator)*S.prod(x**k for x,k in zip(variables,a)) for a,c in p.items())
def inertia_by_congruence(matrix):
    # Exact symmetric elimination, choosing a nonzero diagonal; no eigenvalues,
    # selected author principal blocks, matrix ranks, or principal minors.
    m=[list(map(R,row)) for row in matrix]; pivots=[]
    while m:
        k=next((i for i in range(len(m)) if m[i][i]),None)
        if k is None:
            ok(all(not x for row in m for x in row),'zero residual Schur matrix')
            return pivots,len(m)
        m[0],m[k]=m[k],m[0]
        for row in m: row[0],row[k]=row[k],row[0]
        d=m[0][0];ok(d>0,'positive exact congruence pivot');pivots.append(d)
        m=[[m[i][j]-m[i][0]*m[0][j]/d for j in range(1,len(m))]for i in range(1,len(m))]
    return pivots,0

raw=(ROOT/'MANIFEST.json').read_bytes()
ok(hashlib.sha256(raw).hexdigest()=='a59097544b285a4d5452cad2b8dac7d80d4f437098b123f71e04ad06242d9fa7','pinned manifest')
manifest=json.loads(raw)
for name,m in manifest['files'].items():
    b=(ROOT/name).read_bytes();ok(len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],'input integrity '+name)
X=[var(5,i) for i in range(5)];e=elementary(X,5)
p=add(add(scale(e[5],4500),scale(mul(e[1],e[4]),-220)),scale(mul(power(e[1],2,5),e[3]),7))
evec=[1]*5;w=[6,1,1,1,1]
W=add(mul(direction(p,evec),direction(p,w)),scale(mul(p,direction(direction(p,evec),w)),-1))
a,b,c=S.symbols('a b c');abc=[a,b,c]
y=[var(3,i) for i in range(3)]
certs=json.loads((ROOT/'SLICE_GRAM_CERTIFICATES.json').read_bytes());gram_results={}
for name,subs,lf,factor in [
    ('symmetric',[{},y[0],y[1],y[2],{}],add(add(y[0],y[1]),y[2]),49),
    ('s4slice',[y[0],y[1],y[2],y[2],y[2]],add(add(y[0],y[1]),scale(y[2],-7)),9)]:
    cert=certs[name];M=[[R(v) for v in row] for row in cert['matrix']]
    ok(all(M[i][j]==M[j][i] for i in range(len(M)) for j in range(len(M))),'symmetric Gram '+name)
    mons=[expr_to_sparse(S.sympify(mon,locals=dict(zip(['a','b','c'],abc))),abc) for mon in cert['monomials']]
    gram={}
    for i in range(len(M)):
        for j in range(len(M)):gram=add(gram,scale(mul(mons[i],mons[j]),M[i][j]))
    lhs=substitute(W,subs,3);rhs=scale(mul(power(lf,2,3),gram),factor)
    ok(lhs==rhs,'independent Fraction slice identity '+name)
    pivots,nullity=inertia_by_congruence(M)
    ok(len(pivots)==cert['rank'],'independent rank '+name)
    gram_results[name]={'size':len(M),'positive_inertia':len(pivots),'zero_inertia':nullity,'negative_inertia':0,'congruence_pivots':[str(x) for x in pivots],'wronskian_slice_terms':len(lhs)}

# Independently derive the quintic symbol by substitution in the multivariate p.
t,z=S.symbols('t epsilon');T=var(1,0)
r=[1,1,1,1,-4]
G=-sparse_to_sympy(substitute(p,[add(const(1,u),scale(T,-1)) for u in r],1),[t])/750
ok(S.Poly(G,t).all_coeffs()==[1,0,-23,66,-68,24],'direct operator coefficients')
# Invert delta coefficient-by-coefficient without using the author F expression.
F=sum(coeff*t**k[0]/(k[0]-4) for k,coeff in S.Poly(G,t).terms() if k[0]!=4)
Fe=S.expand(F+z*t*S.diff(F,t));Ge=S.expand(G+z*t*S.diff(G,t))
c2=S.factor(-Fe.subs(t,2)/16)
f=S.expand(Fe+c2*t**4)
quotient,remainder=S.div(f,(t-2)**2,t)
ok(remainder==0,'derived endpoint has double root two')
Q=S.Poly(quotient,t)
ok(S.expand(c2+(1+4*z)*S.Rational(185,24))==0,'derived endpoint coefficient')
qcoeff=Q.all_coeffs(); dq=S.Poly(S.diff(quotient,t),t).all_coeffs()
# Independent Sylvester determinant for a cubic and its quadratic derivative.
Syl=S.Matrix([qcoeff+[0],[0]+qcoeff,dq+[0,0],[0]+dq+[0],[0,0]+dq])
disc=S.factor(-Syl.det()/qcoeff[0])
expected=(4*z+1)*(167620*z**3-8871*z**2+2820*z-752)/5184
ok(S.factor(disc-expected)==0,'independent Sylvester discriminant')
D=S.Poly(S.cancel(disc*5184/(4*z+1)),z)
ok(D.count_roots(-S.oo,S.oo)==1,'Sturm count one real threshold root')
lo=S.Rational(146702017518327,10**15);hi=S.Rational(146702017518329,10**15)
ok(D.eval(lo)<0<D.eval(hi),'15-place rational isolating bracket')
# Explicit rational controls before and after threshold, with exact root counts.
controls={}
for val in [S.Rational(0),S.Rational(1,7),S.Rational(1,6),S.Rational(1),S.Rational(100)]:
    q=S.Poly(quotient.subs(z,val),t)
    nr=q.count_roots(0,S.oo)
    ok(nr==(3 if D.eval(val)>0 else 1),'Sturm positive roots control '+str(val))
    controls[str(val)]={'cubic_positive_distinct_roots':int(nr),'D_sign':int(S.sign(D.eval(val)))}
# Derive p_epsilon hook form and the centered operator directly from coefficients.
dp=scale(mul(e[1],direction(p,evec)),R(1,5))
claimed=add(add(scale(mul(e[1],e[4]),680),scale(mul(power(e[1],2,5),e[3]),-74)),scale(mul(power(e[1],3,5),e[2]),R(21,5)))
ok(dp==claimed,'direct deformation hook coefficients')
direct_delta=-sparse_to_sympy(substitute(dp,[add(const(1,u),scale(T,-1)) for u in r],1),[t])/750
ok(S.expand(direct_delta-t*S.diff(G,t))==0,'direct deformation operator equality')
cone=sparse_to_sympy(substitute(p,[add(const(1,u),T) for u in w],1),[t])
ok(S.expand(cone-750*t**2*(t+1)**2*(t+8))==0,'direct cone line identity')
# All-input operator coefficient check for shifted e_(n-1), small dimensions:
# centered root specialization gives the complete coefficient identity in r.
for n in range(2,8):
    rr=S.symbols('r:'+str(n-1));ss=S.symbols('s');roots=list(rr)+[-sum(rr)]
    g=S.prod(t-v for v in roots)
    shifted=[v-ss*t for v in roots]
    # e_(n-1) through the coefficient generating function.
    zz=S.symbols('zz');enm1=S.Poly(S.prod(1+zz*v for v in shifted),zz).coeff_monomial(zz**(n-1))
    ok(S.expand(enm1-(-1)**(n-1)*S.diff(g,t).subs(t,ss*t))==0,'shifted family operator n='+str(n))
result={'disposition':'PASS_SCOPED_PARTIAL_RESULTS','input_manifest_sha256':hashlib.sha256(raw).hexdigest(),'independent_checks':len(checks),'method':'Independent Fraction sparse-polynomial reconstruction and exact Gram congruence; independently derived inverse symbols; Sylvester determinant and Sturm controls','gram_inertia':gram_results,'threshold_discriminant':str(disc),'threshold_rational_bracket':[str(lo),str(hi)],'root_controls':controls,'full_conjecture':'unresolved','weak_SOS_boundary':'not determined','universal_proofs':'reviewed in AUDIT.md; not formalized','sympy':S.__version__}
print(json.dumps(result,indent=2))
