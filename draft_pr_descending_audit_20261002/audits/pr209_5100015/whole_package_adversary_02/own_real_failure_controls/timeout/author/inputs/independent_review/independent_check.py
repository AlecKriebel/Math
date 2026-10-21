#!/usr/bin/env python3
"""Independent k303,b algebra, direct geometry, and analytic-lemma diagnostics."""
import json, math, hashlib
from pathlib import Path
from fractions import Fraction as F
import sympy as S
import mpmath as M
names=[]; exact_count=0
def exact(name,e,gens=(),relations=()):
 global exact_count
 p=S.together(e).as_numer_denom()[0]
 if relations:p=S.groebner(relations,*gens,order='lex').reduce(S.expand(p))[1]
 assert S.simplify(p)==0,(name,p)
 names.append(name);exact_count+=1
s,c,d,t,C,D,m,a,b=S.symbols('s c d t C D m a b')
den=1-m*s*s*t*t
pm=S.Matrix([-a*(s*C*D-t*c*d)/den,b*(c*C+s*t*d*D)/den])
pp=S.Matrix([-a*(s*C*D+t*c*d)/den,b*(c*C-s*t*d*D)/den])
rels=[c*c+s*s-1,d*d+m*s*s-1,C*C+t*t-1,D*D+m*t*t-1]
gens=(c,d,C,D,s,t,m,a,b)
exact('symmetric endpoint determinant',S.det(S.Matrix.hstack(pm,pp))-2*a*b*t*C*d/den,gens,rels)
dminus=(d*D+m*s*t*c*C)/den;dplus=(d*D-m*s*t*c*C)/den
exact('dn trace area coefficient',a*b*t*C/D*(dminus+dplus)-2*a*b*t*C*d/den)
# Sum of endpoints at w, with dn(w)=b/a, has the exact center-pedal foot.
x,y,cw=S.symbols('x y cw');Dw=S.symbols('Dw')
q=S.Matrix([-a*b*b*x/(a*a-(a*a-b*b)*x*x),a*a*b*y/(a*a-(a*a-b*b)*x*x)])
sumP=S.Matrix([-2*a*x*cw*(b/a)/Dw,2*b*y*cw/Dw]);L=S.diag(b/a,1)/(2*cw)
for j in (0,1):exact('center pedal linear identity coordinate '+str(j),q[j]-(L*sumP)[j].subs(Dw,(a*a-(a*a-b*b)*x*x)/(a*a)))
exact('center pedal scale determinant',L.det()-b/(4*a*cw*cw))
# Pure signed-area edge identity on arbitrary polygons, independent of elliptic coordinates.
def det(P,Q):return P[0]*Q[1]-P[1]*Q[0]
def area(P):return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
for N in range(3,24):
 for seed in range(1,9):
  P=[(F((i*i+seed*7)%19-9),F((i*i*i+seed*3)%23-11)) for i in range(N)]
  V=[(P[(i+1)%N][0]-P[i][0],P[(i+1)%N][1]-P[i][1]) for i in range(N)]
  assert area(V)==2*area(P)-sum(det(P[i],P[(i+2)%N]) for i in range(N))/2
  exact_count+=1
names.append('signed edge-area identity on arbitrary integer polygons')
for N in range(3,102):
 for tau in range(1,(N+1)//2):
  if math.gcd(N,tau)!=1:continue
  q=N//math.gcd(N,2);r=N//q
  shifts=[F(2*tau*i,N)%1 for i in range(N)]
  assert set(shifts)=={F(j,q) for j in range(q)}
  assert all(shifts.count(F(j,q))==r for j in range(q))
  assert (q%2==1)==(N%4!=0)
  if q%2:assert F(1,2) not in shifts
  exact_count+=4 if q%2 else 3
names.append('quotient subgroup orders/multiplicities and odd half-period exclusion')
M.mp.dps=80
numeric_count=0;err=M.mpf(0);families=0
def near(x,y):
 global numeric_count,err
 e=abs(x-y)/(1+abs(y));err=max(err,e);numeric_count+=1
 assert e<M.mpf('1e-65'),(e,x,y)
def dot(P,Q):return sum(x*y for x,y in zip(P,Q))
for N in [3,5,6,7,9,10,14]:
 for mm in [M.mpf('.07'),M.mpf('.61'),M.mpf('.96')]:
  K=M.ellipk(mm);Kp=M.ellipk(1-mm);kp=M.sqrt(1-mm)
  jf=lambda name,z:M.ellipfun(name,z,mm)
  alpha=M.mpf('2.3');beta=alpha*kp
  for tau in range(1,(N+1)//2):
   if math.gcd(tau,N)!=1:continue
   families+=1;v=2*tau*K/N;aa=alpha*jf('dn',v)/jf('cn',v);bb=beta/jf('cn',v);w=K-v
   fv=lambda z:jf('sn',z)*jf('cn',z)/jf('dn',z)
   trace=lambda z:sum(jf('dn',z+2*i*v) for i in range(N))
   coeff=aa*aa*bb**4*fv(v)*(2*fv(v)-fv(2*v))/(4*alpha*beta*jf('cn',w)**2)
   const=coeff*trace(0)*trace(K)
   products=[]
   for phase in [M.mpf('.031'),M.mpf('.41'),M.mpf('1.21')]:
    u=phase*K
    pos=lambda z:(-aa*jf('sn',z),bb*jf('cn',z))
    P=[pos(u+2*i*v) for i in range(N)]
    normals=[(p[0]/aa**2,p[1]/bb**2) for p in P]
    Q=[(n[0]/dot(n,n),n[1]/dot(n,n)) for n in normals]
    R=[]
    for i,n in enumerate(normals):
     n2=normals[(i+1)%N];de=det(n,n2);assert abs(de)>M.mpf('1e-30')
     R.append(((n2[1]-n[1])/de,(n[0]-n2[0])/de))
    A=area(R);B=area(Q);products.append(A*B);near(A*B,const)
    near(A,aa*aa*bb*bb/(alpha*beta)*fv(v)*trace(u+v))
    near(B,bb*bb/(4*jf('cn',w)**2)*(2*fv(v)-fv(2*v))*trace(u+K-v))
    for i in range(N):
     z=u+2*i*v;left=pos(z+K-v);right=pos(z+K+v)
     near(Q[i][0],bb/aa*(left[0]-right[0])/(2*jf('cn',w)))
     near(Q[i][1],(left[1]-right[1])/(2*jf('cn',w)))
     # Direct outer-side incidence and orthogonal foot constraints.
     near(dot(normals[i],R[i]),1);near(dot(normals[(i+1)%N],R[i]),1)
     near(dot(normals[i],Q[i]),1)
    near(area(list(reversed(R)))*area(list(reversed(Q))),A*B)
    near(area(R*3)*area(Q*3),9*A*B)
   # Complex diagnostics, away from poles, of the proved entire-product lemma.
   q=N//math.gcd(N,2)
   U=lambda z:sum(jf('dn',z+2*K*j/q) for j in range(q))
   for z in [M.mpc('.17','.23')*K,M.mpc('.41','.18')*K]:near(U(z)*U(z+K),U(0)*U(K))
   center=K+1j*Kp
   near(U(center),0)
# Deliberately excluded four-period direct geometry, in exact rational arithmetic.
a0=F(4);b0=F(3)
control=[]
for P in [[(F(4),F(0)),(F(0),F(3)),(F(-4),F(0)),(F(0),F(-3))],[(F(16,5),F(9,5)),(F(-16,5),F(9,5)),(F(-16,5),F(-9,5)),(F(16,5),F(-9,5))]]:
 ns=[(p[0]/a0**2,p[1]/b0**2) for p in P];Q=[(n[0]/dot(n,n),n[1]/dot(n,n)) for n in ns];R=[]
 for i,n in enumerate(ns):
  n2=ns[(i+1)%4];de=det(n,n2);R.append(((n2[1]-n[1])/de,(n[0]-n2[0])/de))
 control.append(area(R)*area(Q))
assert control==[F(1152),F(1250)];exact_count+=1
print(json.dumps({'status':'PASS','exact_assertions':exact_count,'exact_groups':names,'numerical_diagnostics':numeric_count,'families':families,'decimal_precision':M.mp.dps,'maximum_scaled_error':M.nstr(err,10),'excluded_N4_exact_products':list(map(str,control)),'versions':{'sympy':S.__version__,'mpmath':M.__version__},'scope':'Analytic proof establishes all periods/phases. Numerical complex-function and direct-geometry checks are not interval certificates or replacements for the meromorphic proof.'},indent=2))
