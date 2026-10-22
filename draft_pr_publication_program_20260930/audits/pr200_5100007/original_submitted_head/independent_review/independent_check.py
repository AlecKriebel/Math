"""Independent k115 algebra, parity, and direct-geometry controls.
General proof is audited in REVIEW.md. Numeric diagnostics are not certificates.
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json,hashlib,pathlib
import sympy as s
C=Counter();D=Counter()
def ck(g,b):
 assert b,g
 C[g]+=1
# Independently expand distances starting only from squared outer axes.
z,t,x=s.symbols('z t x');q=1-t
Ao2=(1-z*t)**2/q**2;Bo2=(1-z)/q**2
raw=((Ao2-Bo2)*x+Bo2+z)**2-4*z*Ao2*x
fact=s.factor(raw)
U=1-z*t*(2-t);V=1-t*(2-z*t)
ck('universal_raw_factorization',s.cancel(fact-(1-z*x)*(U**2-z*V**2*x)/q**4)==0)
ck('universal_real_factor_lower_bound',s.expand(U**2-z*V**2-(1-z)*(1-z*t*t)**2)==0)
# Re-derive two tangent equations by addition in a polynomial ring.
sn,cn,dn,h,c,d,k=s.symbols('sn cn dn h c d k')
rules=[(cn**2,1-sn**2),(dn**2,1-k*sn**2),(c**2,1-h**2),(d**2,1-k*h**2)]
def reduce(e):
 p=s.Poly(s.expand(e),dn,d,cn,c,sn,h,k)
 for var,rep in [(dn,1-k*sn**2),(d,1-k*h**2),(cn,1-sn**2),(c,1-h**2)]:
  p=s.rem(p.as_expr(),var**2-rep,var)
 return s.expand(p)
den=1-k*sn**2*h**2
for sign in [-1,1]:
 S=sn*c*d+sign*h*cn*dn;Z=cn*c-sign*sn*h*dn*d
 # proposed X/a=-sn*d/c;Y/b=cn/c
 ck('universal_tangent_substitution',reduce(sn*d*S+cn*Z-c*den)==0)
S1=sn*c*d-h*cn*dn;S2=sn*c*d+h*cn*dn
Z1=cn*c+sn*h*dn*d;Z2=cn*c-sn*h*dn*d
ck('universal_tangent_determinant',reduce(S1*Z2-S2*Z1+2*h*c*dn*den)==0)
# Norm cancellation independently as convolution on Z/m.
for N in range(4,521,4):
 m=N//2;n=N//4
 for tau in range(1,N//2):
  if gcd(N,tau)!=1:continue
  ck('odd_primitive_turning_number',tau%2==1)
  ck('translation_order',gcd(tau,m)==1)
  # All lattice points encoded in half-real-period units; inverse tau mod m.
  shift=(n*tau)%m;ck('quarter_shift_is_K',shift==n)
  pole_mult=2 if N==4 else 4
  poles=Counter();zeros=Counter()
  for j in range(m):
   poles[(-j*tau)%m]+=pole_mult
   zeros[(n-j*tau)%m]+=2
   if N!=4:
    zeros[(n+tau-j*tau)%m]+=1;zeros[(n-tau-j*tau)%m]+=1
  ck('full_divisor_convolution',poles==zeros)
  ck('exception_iff_N4',(tau==n)==(N==4))
for N in range(6,82,4):
 m=N//2;rot={F(j,m)%1 for j in range(m)}
 ck('wrong_parity_negative_control',F(1,2) not in rot)
# Direct high precision geometry is separate from the exact controls above.
import mpmath as mp
mp.mp.dps=90
maxerr=mp.mpf(0)
def close(label,x,y):
 global maxerr
 e=abs(x-y)/max(1,abs(x),abs(y));maxerr=max(maxerr,e)
 assert e<mp.mpf('1e-65'),(label,e)
 D[label]+=1
for mod in [mp.mpf('0.11'),mp.mpf('0.63'),mp.mpf('0.94')]:
 par=mod**2;kp=mp.sqrt(1-par);K=mp.ellipk(par);Kp=mp.ellipk(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [4,8,12,20,28]:
  for tau in range(1,N//2):
   if gcd(tau,N)!=1:continue
   v=2*K*tau/N;step=2*v;a=dn(v)/cn(v);b=kp/cn(v)
   def vertices(u):return [(-a*sn(u+j*step),b*cn(u+j*step)) for j in range(N)]
   def outer(u):
    ps=vertices(u);qs=[]
    for i,P in enumerate(ps):
     R=ps[(i+1)%N];det=P[0]*R[1]-R[0]*P[1]
     qs.append((a*a*(R[1]-P[1])/det,b*b*(P[0]-R[0])/det))
    return qs
   def prod(qs,f):return mp.fprod(mp.sqrt((x-f)**2+y*y) for x,y in qs)
   base=None
   for frac in [mp.mpf('0.071'),mp.mpf('0.417'),mp.mpf('0.893')]:
    u=frac*K;ps=vertices(u);qs=outer(u)
    R=prod(qs,mod)
    if base is None:base=R
    close('full_direct_product',R,base);close('two_focus_pairing',R,prod(qs,-mod))
    for j,((X,Y),P) in enumerate(zip(qs,ps)):
     w=u+(j+mp.mpf('.5'))*step
     close('independent_intersection_x',X,-a*dn(v)/cn(v)*sn(w))
     close('independent_intersection_y',Y,b/cn(v)*cn(w))
     assert (X/a)**2+(Y/b)**2>1;D['strictly_exterior']+=1
     # Chord between consecutive orbit vertices has discriminant zero on C.
     Rr=ps[(j+1)%N];vx=Rr[0]-P[0];vy=Rr[1]-P[1]
     aa=vx*vx+vy*vy/(kp*kp);bb=2*(P[0]*vx+P[1]*vy/(kp*kp));cc=P[0]**2+P[1]**2/(kp*kp)-1
     close('caustic_tangency_discriminant',bb*bb,4*aa*cc)
   # Complex zero locations and real positivity are independently tested.
   if N>4:
    for sign in [-1,1]:
     zz=1j*Kp+K+sign*step
     close('complex_J_zero',dn(step)**2-par*cn(step)**2*sn(zz)**2,0)
     der=-2*par*cn(step)**2*sn(zz)*cn(zz)*dn(zz)
     assert abs(der)>mp.mpf('1e-15');D['simple_J_zero']+=1
   zz=K*mp.mpf('.241')+1j*Kp*mp.mpf('.237')
   close('quarter_complex_shift',sn(zz+K+1j*Kp),dn(zz)/(mod*cn(zz)))
root=pathlib.Path(__file__).resolve().parent
r={'verdict':'PASS','exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'precision_digits':90,'max_scaled_error':mp.nstr(maxerr,15),'limits':'Finite controls are not proof substitutes; REVIEW.md audits all-period divisor argument.'}
(root/'independent_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
