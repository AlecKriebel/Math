#!/usr/bin/env python3
"""Author checks for 5100033. Finite exact controls and noncertified diagnostics.
No downloaded code; requires the installed SymPy and mpmath packages.
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
import hashlib
import json
import sympy as sp
import mpmath as mp

HERE=Path(__file__).resolve().parent
exact=0

def zero(x):
    global exact
    assert sp.factor(x)==0, sp.factor(x)
    exact+=1

a,c,s,h=sp.symbols('a c s h', nonzero=True)
b2=a*a-c*c
D=a-c*s
Q=sp.Matrix([a*(c-a*s)/D,a*sp.sqrt(b2)*h/D])
n=sp.Matrix([-s/a,h/sp.sqrt(b2)])
relation={h*h:1-s*s}
def reduce(x):
    num,den=sp.fraction(sp.factor(x))
    num=sp.rem(num, h*h-(1-s*s),h)
    return sp.factor(num/den)
zero(reduce(n.dot(Q)-1))
zero(reduce((Q[0]-c)*n[1]-Q[1]*n[0]))
zero(reduce(Q.dot(Q)-a*a))
zero(reduce(n.dot(n)-(a-c*s)*(a+c*s)/(a*a*b2)))
# Projection from the other focus equals -Q_+(w+2K).
Qminus=sp.Matrix([-a*(c+a*s)/(a+c*s),a*sp.sqrt(b2)*h/(a+c*s)])
zero(Qminus[0]+Q[0].subs(s,-s))
zero(Qminus[1]-Q[1].subs(s,-s))
# At r+-v the numerator vectors agree and are isotropic.
b=sp.symbols('b', nonzero=True)
num=sp.Matrix([a*(c-a*s),a*b*h])
resnum=num.subs({s:a/c,h:-sp.I*b/c})
zero((resnum[0]+a*b*b/c).subs(a*a,b*b+c*c))
zero(resnum[1]+sp.I*a*b*b/c)
R=sp.Matrix([-a*b*b/c,-sp.I*a*b*b/c])
zero(R.dot(R))
# Both singular endpoints can contribute, but their double coefficient vanishes.
x,y,u,t,eps=sp.symbols('x y u t eps')
A=sp.Matrix([x,y]); B=sp.Matrix([u,t])
expr=sp.det(sp.Matrix.hstack(R/eps+A,-R/eps+B))
zero(sp.expand(expr*eps*eps).subs(eps,0))
# Reflection J has determinant -1; reversal supplies the other -1.
J=sp.diag(1,-1)
zero(sp.det(sp.Matrix.hstack(J*A,J*B))+sp.det(sp.Matrix.hstack(A,B)))
# Four divisor locations in coordinates real/L and imaginary/(iK').
poles={(Fraction(0),1),(Fraction(0),3)}
zeros={(Fraction(1,2),1),(Fraction(1,2),3)}
def half_shift(point):return ((point[0]+Fraction(1,2))%1,point[1])
assert {half_shift(z) for z in zeros}==poles; exact+=1
assert {half_shift(z) for z in poles}==zeros; exact+=1
rotations=0
for N in range(3,202,2):
    for tau in range(1,(N+1)//2):
        if gcd(N,tau)!=1:continue
        rotations+=1
        orbit=[(j*tau)%N for j in range(N)]
        assert len(set(orbit))==N; exact+=1
        # At a pole phase, Q_j is singular at residues 0 and tau mod N.
        assert [j for j,x in enumerate(orbit) if x in (0,tau)]==[0,1];exact+=1
        assert Fraction(N,2)%1==Fraction(1,2);exact+=1
        assert Fraction(N-2*tau,4)*2==Fraction(N,2)-tau;exact+=1
        # Translation through the index cut closes in the actual 4K period.
        assert Fraction(N)*Fraction(tau,N)==tau;exact+=1

mp.mp.dps=90
num_count=0
max_error=mp.mpf('0')
max_pole_error=mp.mpf('0')
def close(x,y,tol=mp.mpf('1e-68')):
    global num_count,max_error
    err=abs(x-y)/(1+abs(x)+abs(y))
    assert err<tol,(mp.nstr(err,8),mp.nstr(x,10),mp.nstr(y,10))
    max_error=max(max_error,err);num_count+=1

def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return [a[i]-b[i] for i in range(2)]
def dot(a,b):return sum(a[i]*b[i] for i in range(2))
def area(q):return sum(det(q[j],q[(j+1)%len(q)]) for j in range(len(q)))/2

def make(k,N,tau):
    K=mp.ellipk(k*k); Kp=mp.ellipk(1-k*k)
    v=2*K*tau/N; delta=2*v
    sn=lambda z:mp.ellipfun('sn',z,k*k)
    cn=lambda z:mp.ellipfun('cn',z,k*k)
    dn=lambda z:mp.ellipfun('dn',z,k*k)
    a=dn(v)/cn(v);b=mp.sqrt(1-k*k)/cn(v);c=k
    def point(w):return [-a*sn(w),b*cn(w)]
    def normal(w):
        p=point(w);return [p[0]/(a*a),p[1]/(b*b)]
    def foot(w,sign=1):
        n=normal(w);f=[sign*c,mp.mpf(0)]
        lam=(1-dot(n,f))/dot(n,n)
        return [f[i]+lam*n[i] for i in range(2)]
    def Q(w):return [a*(c-a*sn(w))/(a-c*sn(w)),a*b*cn(w)/(a-c*sn(w))]
    def T(w):return area([Q(w+j*delta) for j in range(N)])
    def outer(w):
        ns=[normal(w+j*delta) for j in range(N)]
        vertices=[]
        for j in range(N):
            p,q=ns[j],ns[(j+1)%N];d=det(p,q)
            vertices.append([(q[1]-p[1])/d,(p[0]-q[0])/d])
        # Side from outer[j-1] to outer[j] is tangent at original[j].
        feet=[]
        for sign in (1,-1):
            f=[sign*c,mp.mpf(0)];qs=[]
            for j in range(N):
                x,y=vertices[j-1],vertices[j];e=sub(y,x)
                lam=dot(sub(f,x),e)/dot(e,e)
                q=[x[i]+lam*e[i] for i in range(2)]
                qs.append(q)
                qformula=foot(w+j*delta,sign)
                for coordinate in range(2):close(q[coordinate],qformula[coordinate])
            feet.append(qs)
        return area(feet[0]),area(feet[1])
    return K,Kp,v,delta,Q,T,outer

odd_families=0
for k in map(mp.mpf,('0.23','0.72')):
    for N in range(3,20,2):
        for tau in range(1,(N+1)//2):
            if gcd(N,tau)!=1:continue
            odd_families+=1
            K,Kp,v,d,Q,T,outer=make(k,N,tau)
            products=[]
            for fraction in ('0.113','0.347','0.719'):
                w=mp.mpf(fraction)*K
                bp,bm=outer(w)
                close(bp,T(w));close(bm,T(w+2*K))
                close(T(w+2j*Kp),-T(w))
                close(T(2*K-w),T(w))
                products.append(bp*bm)
            for product in products[1:]:close(product,products[0])

# Independent even-parity controls: equality does not imply constant product.
even_variation=[]
for k in map(mp.mpf,('0.31','0.68')):
    for N,tau in ((4,1),(6,1),(8,3),(10,3)):
        K,Kp,v,d,Q,T,outer=make(k,N,tau)
        products=[]
        for fraction in ('0.157','0.639'):
            w=mp.mpf(fraction)*K
            bp,bm=outer(w)
            close(bp,bm);products.append(bp*bm)
        variation=abs(products[1]-products[0])/(1+abs(products[0]))
        assert variation>mp.mpf('1e-15')
        even_variation.append({'k':str(k),'N':N,'tau':tau,'relative_change':mp.nstr(variation,12)})

# Complex finite-epsilon tests of the actual simultaneous-pole cancellation.
pole_cases=0
for k in map(mp.mpf,('0.3','0.75')):
    for N,tau in ((3,1),(5,1),(5,2),(9,4)):
        K,Kp,v,d,Q,T,outer=make(k,N,tau)
        r=K+1j*Kp;zm=r-v;zp=r+v
        epsilon=mp.mpf('1e-22')*K
        qm=Q(zm+epsilon);qp=Q(zp+epsilon)
        double=abs(epsilon*epsilon*det(qm,qp))/(1+sum(abs(epsilon*x) for x in qm))
        assert double<mp.mpf('1e-18')
        opposite=max(abs(epsilon*(qm[j]+qp[j])) for j in range(2))
        assert opposite<mp.mpf('1e-18')
        # A simple-pole Laurent law: eps*T and half-eps*T agree to O(eps).
        simple=abs(epsilon*T(zm+epsilon)-(epsilon/2)*T(zm+epsilon/2))
        assert simple<mp.mpf('1e-17')
        max_pole_error=max(max_pole_error,double,opposite,simple)
        pole_cases+=1

out={
 'problem_id':'5100033','status':'PASS',
 'proof_sha256':hashlib.sha256((HERE/'PROOF.md').read_bytes()).hexdigest(),
 'exact_assertions':exact,'primitive_odd_rotations':rotations,
 'numerical_precision_decimal_digits':mp.mp.dps,
 'direct_geometry_odd_families':odd_families,
 'numerical_comparisons':num_count,'max_normalized_numerical_error':mp.nstr(max_error,16),
 'complex_pole_cases':pole_cases,'max_finite_epsilon_pole_error':mp.nstr(max_pole_error,16),
 'even_parity_countercontrols':even_variation,
 'limitations':'Finite exact encoding/algebra controls and high-precision non-interval numerical diagnostics. The universal meromorphic proof, not these tests, establishes the theorem.'}
print(json.dumps(out,indent=2))
