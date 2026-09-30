"""Exact polynomial and cyclotomic controls for the scoped graph-patch result.
Requires SymPy; no floating-point numerical evidence is used.
"""
from pathlib import Path
from hashlib import sha256
from math import factorial
import json
import sympy as S
r,t,c,s,x,y,z=S.symbols('r t c s x y z')
counts={}
def check(ok,name):
    assert bool(ok),name
    counts[name]=counts.get(name,0)+1
def equal(a,b,name): check(S.expand(a-b)==0,name)
def integral(p):
    return S.factor(sum(v*S.Rational(factorial(i)*factorial(j),factorial(i+j+2)) for (i,j),v in S.Poly(S.expand(p),r,t).terms()))
def basis(k):
    ans=[]
    for a in range(k+1):
        for b in range(k+1-a):
            d=k-a-b
            f=S.Integer(1)
            for n,lam in [(a,1-r-t),(b,r),(d,t)]:
                f*=S.prod(k*lam-j for j in range(n))/S.factorial(n)
            ans.append((S.Rational(b,k),S.Rational(d,k),S.Poly(S.expand(f),r,t)))
    return ans
bases={k:basis(k) for k in range(2,7)}
def ip(k,p):
    p=S.Poly(S.expand(p),r,t)
    return S.expand(sum(p.eval({r:a,t:b})*f.as_expr() for a,b,f in bases[k]))
for k,bs in bases.items():
    for j,(a,b,f) in enumerate(bs):
        for l,(aa,bb,ff) in enumerate(bs):
            check(f.eval({r:aa,t:bb})==int(j==l),'Lagrange nodal identity')
    for i in range(k+1):
        for j in range(k+1-i):
            equal(ip(k,r**i*t**j),r**i*t**j,'polynomial reproduction')
    equal(sum(f.as_expr() for a,b,f in bs),1,'partition of unity')
# Generic physical triangle (0,0),(1,0),(c,s), s>0.
# Integrate each physical Hessian entry after pullback.
def moments(k,p):
    pulled=S.expand(p.subs({x:r+c*t,y:s*t},simultaneous=True))
    e=ip(k,pulled)-pulled
    return [integral(s*S.diff(e,r,2)),integral(-c*S.diff(e,r,2)+S.diff(e,r,t)),integral((c*c*S.diff(e,r,2)-2*c*S.diff(e,r,t)+S.diff(e,t,2))/s)]
expected=[[-s*(2*c-1)/2,3*c*(c-1)/4,0],[-s*s/3,s*(2*c-1)/12,c*(c-1)/2],[0,-s*s/12,s*(2*c-1)/3],[0,0,s*s/2]]
for p,want in zip([x**3,x*x*y,x*y*y,y**3],expected):
    actual=moments(2,p)
    for u,v in zip(actual,want): equal(u,v,'generic cubic Hessian moments')
base=ip(2,r**3)
equal(base,S.Rational(3,2)*r*r-r/2,'single triangle interpolant')
equal(integral(S.diff(base-r**3,r,2)),S.Rational(1,2),'single triangle nonzero moment')
# Quartic radial diagnostic, exact before imposing unit-circle geometry.
v=moments(3,(x*x+y*y)**2)
trace=S.factor(v[0]+v[2])
formula=-(c*c+s*s)*((c-1)**2+s*s)/(3*s)
equal(S.cancel(trace-formula),0,'radial quartic full triangle formula')
num=S.factor((trace-2*(c-1)/(3*s))*3*s)
check(S.rem(S.Poly(num,s),S.Poly(s*s+c*c-1,s))==0,'unit-circle reduction')
for a in range(1,15):
    cc=S.Rational(a*a-1,a*a+1);ss=S.Rational(2*a,a*a+1)
    check(cc*cc+ss*ss==1,'rational unit circle')
    check(trace.subs({c:cc,s:ss})==2*(cc-1)/(3*ss)<0,'odd-degree negative diagnostic')
# Exact cyclic-character sums. This includes composite rotation orders.
for k in range(2,21,2):
    for q in [k+5,k+7]:
        phi=S.Poly(S.cyclotomic_poly(q,z),z)
        for a in range(k+2):
            ell=2*a-(k+1)
            for rr in range(3):
                w=ell+2-2*rr
                check(w%2!=0 and 0<abs(w)<q,'nonresonant Hessian character')
                poly=S.Poly(sum(z**((j*w)%q) for j in range(q)),z)
                check(poly.rem(phi).is_zero,'cyclotomic Hessian cancellation')
        for d in range(q):
            check(not S.Poly(z**d+1,z).rem(phi).is_zero,'no opposite polygon vertices')
# Exact rotation covariance of the cubic moment tensor, using the generic formulas.
# Pull polynomial by R, then transform its moment by R M R^T.
def moment_matrix(p,cc,ss):
    coeff=S.Poly(S.expand(p),x,y)
    M=S.zeros(2)
    for idx,mon in enumerate([x**3,x*x*y,x*y*y,y**3]):
        term=coeff.coeff_monomial(mon)
        aa,ab,bb=[S.sympify(v).subs({c:cc,s:ss}) for v in expected[idx]]
        M+=term*S.Matrix([[aa,ab],[ab,bb]])
    return M
# Direct integration with a general rational matrix independently uses its inverse.
def direct_moment(p,B):
    inv=B.inv();pulled=S.expand(p.subs({x:B[0,0]*r+B[0,1]*t,y:B[1,0]*r+B[1,1]*t},simultaneous=True))
    e=ip(2,pulled)-pulled
    H=S.hessian(e,(r,t));phys=inv.T*H*inv
    return S.Matrix(2,2,lambda i,j:integral(S.det(B)*phys[i,j]))
R=S.Matrix([[S.Rational(3,5),-S.Rational(4,5)],[S.Rational(4,5),S.Rational(3,5)]])
B=S.Matrix([[1,S.Rational(2,3)],[0,S.Rational(5,4)]])
for j in range(1,7):
    U=R**j
    for p in [x**3,x*x*y,x*y*y,y**3]:
        pp=p.subs({x:U[0,0]*x+U[0,1]*y,y:U[1,0]*x+U[1,1]*y},simultaneous=True)
        expectedM=U*moment_matrix(pp,S.Rational(2,3),S.Rational(5,4))*U.T
        diff=direct_moment(p,U*B)-expectedM
        for val in diff: equal(val,0,'rotation covariance by direct Hessian integration')
# Exact determinant linearization and cofactor involution, including indefinite jets.
h1,h2,h3,e1,e2,e3,u=S.symbols('h1 h2 h3 e1 e2 e3 u')
H=S.Matrix([[h1,h2],[h2,h3]]);E=S.Matrix([[e1,e2],[e2,e3]])
cof=lambda A:S.Matrix([[A[1,1],-A[0,1]],[-A[1,0],A[0,0]]])
equal((H+u*E).det()-H.det(),u*sum(a*b for a,b in zip(cof(H),E))+u*u*E.det(),'determinant linearization')
for val in cof(cof(E))-E: equal(val,0,'cofactor involution')
for k in range(2,31): check(2*k-2>=k,'quadratic remainder order')
root=Path(__file__).resolve().parent
receipt={'verdict':'PASS','assertions':sum(counts.values()),'groups':counts,'sympy_version':S.__version__,'artifact_sha256':sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite polynomial, tensor, and cyclotomic diagnostics. Analytic Taylor/Poincare estimates and global scope qualifications are proved in the text; no global odd-fan refinement family is certified.'}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
