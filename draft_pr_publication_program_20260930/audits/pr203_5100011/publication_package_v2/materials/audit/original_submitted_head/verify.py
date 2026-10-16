"""k203,a exact finite controls and separately labeled numerical diagnostics.
Locally authored; standard-library/SymPy/mpmath only. No network.
"""
from fractions import Fraction as F
from collections import Counter
from math import gcd
from pathlib import Path
import json,hashlib
C=Counter();D=Counter()
def ck(g,b):
 assert b,g
 C[g]+=1
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def pedal(p,M):
 r=[]
 for i,P in enumerate(p):
  d=sub(p[(i+1)%len(p)],P);tt=dot(sub(M,P),d)/dot(d,d)
  r.append(tuple(P[j]+tt*d[j] for j in range(2)))
 return r
# Rational centrally symmetric polygons, including star orderings. No assertion
# that these auxiliary polygons are billiard orbits.
for m in range(2,22):
 half=[]
 for j in range(m):
  t=F(j+1,m+2);half.append((4*(1-t*t)/(1+t*t),6*t/(1+t*t)))
 base=half+[tuple(-x for x in p) for p in half];N=2*m
 for step in range(1,N):
  if gcd(step,N)!=1:continue
  p=[base[(step*i)%N] for i in range(N)]
  e=[sub(p[(i+1)%N],p[i]) for i in range(N)]
  coeff=sum(det(e[i],e[(i+1)%N])*dot(e[i],e[(i+1)%N])/(dot(e[i],e[i])*dot(e[(i+1)%N],e[(i+1)%N])) for i in range(N))/4
  a0=area(pedal(p,(F(0),F(0))))
  for M in [(F(0),F(0)),(F(1),F(2)),(F(3),F(4)),(F(-3),F(4)),(F(0),F(5)),(F(7,3),F(-2,5))]:
   am=area(pedal(p,M));ck('radial_signed_area',am==a0+dot(M,M)*coeff)
   ck('fixed_polygon_reflection_M',am==area(pedal(p,(M[0],-M[1]))))
   ck('fixed_polygon_negative_M',am==area(pedal(p,tuple(-x for x in M))))
   ck('reversal_signed_area',area(pedal(list(reversed(p)),M))==-am)
# Symbolic symmetry and Laurent cancellation controls.
import sympy as sp
nx,ny,x,y=sp.symbols('nx ny x y');n=sp.Matrix([nx,ny]);M=sp.Matrix([x,y]);J=sp.diag(1,-1)
def q(n,M):return M+(1-(n.T*M)[0])*n/(n.T*n)[0]
ck('universal_real_shift_projection',all(sp.cancel(t)==0 for t in q(-n,M)+q(n,-M)))
ck('universal_imag_shift_projection',all(sp.cancel(t)==0 for t in q(J*n,M)-J*q(n,J*M)))
z=sp.symbols('z');aa=sp.symbols('a0:2');bb=sp.symbols('b0:2');dd=sp.symbols('d0:2');gg=sp.symbols('g0:2');hh=sp.symbols('h0:2')
p=[aa[i]/z**2+bb[i]+dd[i]*z**2 for i in range(2)];dif=[2*gg[i]*z+hh[i]*z**3/3 for i in range(2)];expr=sp.expand(det(p,dif)/2)
for power in [-4,-3,-2]:ck('no_higher_Laurent_pole',expr.coeff(z,power)==0)
ck('simple_Laurent_residue',sp.expand(expr.coeff(z,-1)-det(aa,gg))==0)
for N in range(4,405,4):
 m=N//2;n=N//4
 for tau in range(1,N//2):
  if gcd(N,tau)!=1:continue
  ck('primitive_real_lattice',gcd(tau,m)==1)
  ck('K_in_cyclic_orbit',(n*tau)%m==n)
  ck('neighbors_not_poles',tau%m!=0)
  ck('double_cover_same_residues',Counter((j*tau)%m for j in range(N))==Counter({i:2 for i in range(m)}))
for a2 in range(2,15):
 for b2 in range(1,a2):
  for j in [1,2,3]:
   lam=F(j*b2,4);al=a2-lam;be=b2-lam;c2=a2-b2
   E=F(1,a2)/be-F(1,b2)/al
   ck('complex_transversality',E==lam*c2/(a2*b2*al*be)>0)
# Numerical tests of actual canonical billiards and analytic continuation.
import mpmath as mp
mp.mp.dps=85;maxerr=mp.mpf(0)
def close(g,a,b):
 global maxerr
 err=abs(a-b)/max(1,abs(a),abs(b));maxerr=max(maxerr,err)
 assert err<mp.mpf('1e-62'),(g,mp.nstr(err,10))
 D[g]+=1
for k in [mp.mpf('.23'),mp.mpf('.71'),mp.mpf('.93')]:
 par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Kp=mp.ellipk(1-par);alpha=mp.mpf(2);beta=alpha*kp
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 def qm(u,M):
  nn=(-sn(u)/alpha,cn(u)/beta);dd=dot(nn,nn)
  return tuple(M[j]+(1-dot(nn,M))*nn[j]/dd for j in range(2))
 for N in [4,8,12,16,20]:
  for tau in range(1,N//2):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;step=2*v;a=alpha*dn(v)/cn(v);b=beta/cn(v)
   S=lambda u:sum(dn(u+j*step) for j in range(N))
   for M in [(mp.mpf(0),mp.mpf(0)),(mp.mpf(1),mp.mpf(2)),(mp.mpf(-3),mp.mpf('.25'))]:
    Ts=lambda u:area([qm(u+j*step,M) for j in range(N)])
    ref=None;ratio=None
    for phase in [mp.mpf('.07'),mp.mpf('.31'),mp.mpf('.84')]:
     w=phase*K;P=[(-a*sn(w+j*step),b*cn(w+j*step)) for j in range(N)]
     B=[(-alpha*sn(w+v+j*step),beta*cn(w+v+j*step)) for j in range(N)]
     Q=pedal(P,M);ap=area(P);am=area(Q);ai=area(B)
     if ref is None:ref=ap*am;ratio=am/ai
     close('actual_product_constancy',ap*am,ref)
     close('actual_pedal_contact_ratio',am/ai,ratio)
     close('canonical_pedal_formula',am,Ts(w+v))
     close('universal_area_dn_formula',ap,a*b*sn(v)*cn(v)/dn(v)*S(w))
     close('contact_area_dn_formula',ai,alpha*beta*sn(v)*cn(v)/dn(v)*S(w+v))
     close('real_radial_reflection',am,area(pedal(P,(M[0],-M[1]))))
    u=mp.mpf('.233')*K+mp.mpf('.179')*1j*Kp
    close('complex_reduced_real_period',Ts(u),Ts(u+4*K/N))
    close('complex_imag_antiperiod',Ts(u+2j*Kp),-Ts(u))
    close('complex_two_pole_proportionality',Ts(u)/S(u+K),Ts(mp.mpf('.157')*K)/S(mp.mpf('.157')*K+K))
    eps=mp.mpf('.213')*K+mp.mpf('.091')*1j*Kp;r=K+1j*Kp
    for j in range(2):close('complex_even_about_pole',qm(r+eps,M)[j],qm(r-eps,M)[j])
root=Path(__file__).resolve().parent
result={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'numeric_precision_digits':85,'maximum_scaled_error':mp.nstr(maxerr,14),'limits':'Finite exact controls and high-precision diagnostics support the written general proof; numerical calculations are not interval certificates.'}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
