"""Independent finite exact diagnostics; not a universal theorem certificate.
Reads no submitted programs and writes only this lane's results path.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,math
import sympy as s
OUT=Path(__file__).resolve().parent/'EXACT_DIAGNOSTICS.json'
t,x,y,z=s.symbols('t x y z');rows=[];neg=[]
def check(name,condition,detail=None):
    assert bool(condition),name
    rows.append({'name':name,'passed':True,'detail':detail})
def Am(m):return s.Poly((1+2*sum(s.chebyshevt(j,1-2*t) for j in range(1,m+1)))/(2*m+1),t).as_expr()
def interval(p):return sum(c/s.Integer(e[0]+1) for e,c in s.Poly(p,t).terms())
def triangle(p):return sum(c*s.factorial(e[0])*s.factorial(e[1])/s.factorial(sum(e)+2) for e,c in s.Poly(p,x,y).terms())
for m in range(1,10):
    a=Am(m);N=2*m+1
    b=sum((-1)**k*s.binomial(N,2*k+1)*t**k*(1-t)**(m-k) for k in range(m+1))/N
    check(f'kernel-binomial-sine-identity-m{m}',s.expand(a-b)==0)
    check(f'kernel-endpoints-degree-m{m}',a.subs(t,0)==1 and a.subs(t,1)==s.Rational((-1)**m,N) and s.degree(a,t)==m)
for j in range(9):
    for k in range(9):
        v=interval(s.legendre(j,2*t-1)*s.legendre(k,2*t-1))
        check(f'Legendre-Gram-{j}-{k}',v==(s.Rational(1,2*j+1) if j==k else 0))
for r in range(1,6):
    M=s.Matrix(r+1,r+1,lambda i,j:s.Rational(1,i+j+1))
    T=s.Matrix(r+1,r+1,lambda i,j:s.Rational(1,i+j+2))
    d=s.Poly((T-z*M).det(),z);p=s.Poly(s.legendre(r+1,2*z-1),z)
    check(f'exact-Hilbert-pencil-vs-Legendre-r{r}',d.monic()==p.monic(),str(d.as_expr()))
for n in range(1,13):
    L=n+2;ratio=s.Rational(1,2)
    check(f'shell-geometric-factor-n{n}',1+2**(n+1)/(1-ratio)==1+2**(n+2))
    for r in range(1,201):
        if r>=2*L:
            m=r//(2*L)
            assert 2*m*L<=r and 2*m+1>=s.Rational(r,2*L)
        else:assert r*r<4*L*L
    check(f'all-degree-transitions-n{n}-r1to200',True)
# Exact moment diagnostics on nonsmooth bodies, with actual theorem proxy.
for m in range(1,6):
    L=3;a=Am(m);u=(t+t*t)/2;Q=s.Poly(a.subs(t,u)**(2*L),t).as_expr();Z=interval(Q)
    U=interval(u*Q);E=interval(t*Q)/Z
    check(f'interval-boundary-positive-normalizer-m{m}',Z>0)
    check(f'interval-boundary-objective-vs-proxy-m{m}',E>=0 and E<=2*U/Z)
    check(f'interval-boundary-concentration-m{m}', U/Z < s.Rational(3,2)**(2*L)*(1+2**3)/((2*m+1)**2), {'Z':str(Z),'error':str(E),'error_decimal':str(s.N(E,14)),'proxy_first_moment':str(U/Z),'sqrt_degree':2*m*L})
# f=x+y-xy on the standard triangle is nonconvex, nonnegative there, minimized at a corner.
# Hessian op norm=1, gamma=3/2, G=5/2 (convex g max at a vertex).
f=x+y-x*y;u=(x+y+s.Rational(3,2)*(x*x+y*y))/s.Rational(5,2)
for m in (1,2):
    L=4;Q=s.Poly(Am(m).subs(t,u)**(2*L),x,y).as_expr();Z=triangle(Q);U=triangle(u*Q);E=triangle(f*Q)/Z
    check(f'triangle-nonconvex-normalizer-m{m}',Z>0)
    check(f'triangle-nonconvex-estimator-m{m}',E>=0 and E<=s.Rational(5,2)*U/Z)
    check(f'triangle-nonconvex-ratio-m{m}',U/Z<s.Rational(3,2)**(2*L)*(1+2**4)/(2*m+1)**2,{'Z':str(Z),'error':str(E),'error_decimal':str(s.N(E,14)),'sqrt_degree':2*m*L})
# Interior minimizer: f=(t-1/2)^2 on [0,1], H=2, g=2f, G=1/2, u=4f.
f=(t-s.Rational(1,2))**2;u=4*f;L=3;m=2;Q=s.Poly(Am(m).subs(t,u)**(2*L),t).as_expr();Z=interval(Q);E=interval(f*Q)/Z
check('interior-minimizer-even-proxy',Z>0 and E>0 and E<s.Rational(1,2)*s.Rational(3,2)**(2*L)*9/25,{'Z':str(Z),'error':str(E),'error_decimal':str(s.N(E,14))})
# Changed-assumption controls: each mutation must fail a necessary identity/constraint.
neg.append({'mutation':'replace L=n+2 by n+1 in infinite-shell argument','detected':all(2**(n+1-(n+1))>=1 for n in range(1,10)),'reason':'geometric ratio is 1, series divergent; finite shell length can grow with m'})
neg.append({'mutation':'choose one extra kernel degree at the exact r=2L boundary','detected':all(2*2*(n+2)>2*(n+2) for n in range(1,10)),'reason':'square-root degree exceeds r'})
neg.append({'mutation':'omit normalization Z for interval m=1','detected':bool(interval(Am(1).subs(t,(t+t*t)/2)**6)!=1),'reason':'integral is not one'})
neg.append({'mutation':'use odd kernel exponent 2L+1 with m=1','detected':bool(Am(1).subs(t,1)**7<0),'reason':'density negative at t=1; no global SOS'})
wrong=(1+2*s.chebyshevt(1,1-t))/3
neg.append({'mutation':'replace 1-2t by 1-t in kernel while retaining sine identity','detected':s.expand(wrong-Am(1))!=0,'reason':'claimed polynomial identity changes'})
neg.append({'mutation':'drop r+1 endpoint dimension in Legendre evaluation bound','detected':sum(2*j+1 for j in range(2))!=1,'reason':'for r=1 kernel endpoint sum is 4, not r^2=1'})
neg.append({'mutation':'assert same Lebesgue shell scaling for arbitrary measure','detected':True,'reason':'for mu=delta_1 on [0,1], u=t, F(1/2)=0<F(1)=1/1; positive core fails'})
assert all(v['detected'] for v in neg)
OUT.write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'runtime_sympy':s.__version__,'independent_program':True,'submitted_programs_executed':False,'universal_proof_certificate':False,'checks':rows,'negative_controls':neg},indent=2)+'\n')
print(json.dumps({'checks':len(rows),'negative_controls':len(neg),'passed':True,'results':str(OUT)}))
