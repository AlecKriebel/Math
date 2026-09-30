"""Exact independent symbolic and rational controls; requires SymPy."""
import sympy as S
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
s,d,sp,f,h,lf,du=S.symbols('s d sp f h lf du', real=True)
g=S.symbols('g0:3',real=True);k=S.symbols('k0:3',real=True);u=S.symbols('u0:3',real=True)
weights=S.symbols('F0:3',real=True)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
# Differentiate the original face functional using arbitrary jet variables.
ptt=lf+du-s*h;ut=(-s*(u[0]+g[0]),s*g[1],s*g[2])
eta_t=h*ptt+dot(g,k)+dot([weights[i]*u[i] for i in range(3)],ut)+s*d*f*h+dot(ut,g)+dot(u,k)+d*(h*h+f*ptt)
zero={du:0,**{v:0 for v in u}}
expected=(d-s)*h*h-s*g[0]**2+s*g[1]**2+s*g[2]**2+d*f*lf
ck(S.expand(eta_t.subs(zero)-h*lf-dot(g,k)-expected)==0)
# Equality with augmented energy, without imposing the equations.
q=h+s*f;r=[g[i]+u[i] for i in range(3)];w=u[0]
eta2=h*h+dot(g,g)+2*u[0]**2+u[1]**2+u[2]**2+s*s*f*f+2*dot(u,g)+2*s*h*f
ck(S.expand(eta2-q*q-dot(r,r)-w*w)==0)
qgrad=[k[i]+s*g[i]+(sp*f if i==0 else 0) for i in range(3)]
flux=q*(lf+du)+dot(r,qgrad)
ck(S.expand(eta_t.subs({d:s,weights[0]:2,weights[1]:1,weights[2]:1})-flux+2*s*r[0]**2+sp*f*r[0])==0)
# Direct transformation and discrepancy evolution without assuming w=u1.
Q,R,W,P,DP,DQ=S.symbols('Q R W P DP DQ')
r1t=DQ-2*s*R+s*W-sp*P
pxt=DQ-sp*P-s*DP
u1t=r1t-pxt
ck(S.expand((-s*R-u1t).subs(DP,R-u[0])+s*(W-u[0]))==0)
# Constant principal matrices for (q,r1,r2,r3,p,w): symmetric eigenvalues ±1,0.
for j in (1,2,3):
 A=S.zeros(6);A[0,j]=A[j,0]=1
 ck(A==A.T);ck(S.expand(A.charpoly().as_expr()-S.Symbol('lambda')**4*(S.Symbol('lambda')**2-1))==0)
# Source algebraic conditions on a face, with delta=s and F=(2,1,1).
for a,b,Fv in ((s,s,2),(0,-s,1),(0,-s,1)):
 ck(S.expand(4*Fv*a*(s+b)-(s+a+Fv*b)**2)==0)
# Leading transverse oscillatory coefficients, computed by symbolic differentiation.
y,N=S.symbols('y N',real=True);chi=S.Function('chi')(y)
fN=chi*S.cos(N*y)
trans=s*S.diff(fN,y)**2+d*fN*S.diff(fN,y,2)
leading=N*N*chi**2*(s*S.sin(N*y)**2-d*S.cos(N*y)**2)
rem=S.expand(trans-leading)
ck(S.Poly(rem.subs({S.sin(N*y):S.Symbol('sn'),S.cos(N*y):S.Symbol('cs')}),N).degree()<=1)
# Exact scalar witness: rational integrand after the half-powers cancel.
x,e=S.symbols('x e',positive=True)
a=(1-x)*(1-e/x)/S.sqrt(x)
form=S.expand(a*a-2*x*x*S.diff(a,x)**2)
anti=S.integrate(form,x)
ck(S.simplify(S.diff(anti,x)-form)==0)
I=S.expand(anti.subs(x,1)-anti.subs(x,e))
target=S.Rational(7,2)*(e*e-1)-(e*e/2+6*e+S.Rational(1,2))*S.log(e)
ck(S.simplify(I-target)==0)
ck(S.simplify(a.subs(x,e))==0);ck(S.simplify(a.subs(x,1))==0)
eps=F(1,2**16)
A=F(7,2)*(eps**2-1);B=eps**2/2+6*eps+F(1,2)
ck(A+B*16*F(2,3)>F(11,6))
# Independent logarithmic-coordinate diagnostic: x=exp(t), a=x^-1/2 v(t).
t=S.symbols('t',real=True);v=S.Function('v')(t)
al=S.exp(-t/2)*v
weighted=S.expand(al*al*S.exp(t)-2*S.exp(t)*S.diff(al,t)**2)
ck(S.simplify(weighted-(v*v/2-2*S.diff(v,t)**2+2*v*S.diff(v,t)))==0)
# A Dirichlet sine on a log interval of length L has positive form when L>2*pi.
# log(2)>2/3 and pi<22/7 already give 16*log(2)>2*pi.
ck(16*F(2,3)>2*F(22,7))
root=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':checks,'artifact_sha256':hashlib.sha256((root/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest(),'scope':'Symbolic face energy and initial derivative, hyperbolic principal block, oscillatory leading coefficient, exact witness integral, and independent logarithmic-coordinate positivity control. No PDE instability or general Lyapunov nonexistence.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
