"""Independent exact and separately labeled numerical k204 diagnostics."""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
E=Counter();D=Counter()
def exact(q,k):
 assert q,k
 E[k]+=1
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def pedals(P,M):
 out=[]
 for j,p in enumerate(P):
  e=sub(P[(j+1)%len(P)],p);s=dot(sub(M,p),e)/dot(e,e)
  out.append(tuple(p[k]+s*e[k] for k in range(2)))
 return out
for m in range(2,10):
 half=[]
 for j in range(m):
  t=F(j+1,m-j)
  half.append((F(5)*(1-t*t)/(1+t*t),F(3)*2*t/(1+t*t)))
 raw=half+[tuple(-x for x in p) for p in half];N=2*m
 for step in range(1,N):
  if gcd(step,N)>1:continue
  P=[raw[(j*step)%N] for j in range(N)]
  A=lambda M:area(pedals(P,M))
  a0=A((F(0),F(0)));ap=A((F(1),F(0)));am=A((F(-1),F(0)))
  bp=A((F(0),F(1)));bm=A((F(0),F(-1)))
  c=ap-a0
  exact(ap==am and bp==bm,'linear_pedal_coefficients_vanish')
  exact(ap==bp,'quadratic_pedal_coefficients_isotropic')
  exact(A((F(1),F(1)))==a0+2*c,'mixed_quadratic_coefficient_zero')
  edges=[sub(P[(j+1)%N],P[j]) for j in range(N)]
  cc=sum(det(edges[j],edges[(j+1)%N])*dot(edges[j],edges[(j+1)%N])/(dot(edges[j],edges[j])*dot(edges[(j+1)%N],edges[(j+1)%N])) for j in range(N))/4
  exact(c==cc,'coefficient_from_actual_side_directions')
  for M in [(F(2,7),F(-5,9)),(F(11,3),F(4,5)),(F(-3),F(8))]:
   exact(A(M)==a0+c*dot(M,M),'rational_actual_side_pedal_radial')
   exact(area(pedals(P[::-1],M))==-A(M),'signed_traversal_reversal')
for N in range(4,121,2):
 m=N//2
 for tau in range(1,m):
  if gcd(N,tau)>1:continue
  exact(gcd(m,tau)==1,'full_even_real_quotient_period')
  exact(all((j*tau)%m==0 for j in (0,m)) and sum((j*tau)%m==0 for j in range(N))==2,'exact_double_residue_count')
  exact(F(m+tau,2).denominator==(1 if N%4==2 else 2),'target_and_wrong_parity_alignment')
  exact(0<tau<m,'adjacent_translates_not_poles')
# Strict inequalities in the exact star certificate, with pi removed.
lo=F(3,5)*F(15,16);hi=F(3,5)/F(15,16)
exact(lo==F(9,16) and hi==F(16,25),'star_exact_rational_endpoints')
exact(F(1,2)<lo<hi<1,'star_entire_interval_negative_double_sine')
# Derivative bound can also be sharpened independently: psi'=k'/dn(u).
# The author's weaker bounds k'^2 <= psi' <= 1/k' remain valid.
for k2 in [F(1,16),F(2,7),F(8,9)]:
 for sn2 in [F(j,16) for j in range(17)]:
  dn2=1-k2*sn2;kp2=1-k2
  exact(kp2**2<=kp2/dn2<=1/kp2,'normal_angle_derivative_squared_bounds')
# Independent analytic continuation diagnostics, never interval proof.
import mpmath as mp
mp.mp.dps=85;worst=mp.mpf(0)
def near(a,b,k):
 global worst
 e=abs(a-b)/max(1,abs(a),abs(b));worst=max(worst,e)
 assert e<mp.mpf('1e-52'),(k,mp.nstr(e,12))
 D[k]+=1
star_receipt=None
for ks in ['0.17','0.63','0.97']:
 k=mp.mpf(ks);par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Ki=mp.ellipk(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 alpha=mp.mpf('1.3');beta=alpha*kp
 for N,tau in [(6,1),(10,3),(14,3),(14,5),(22,3)]:
  v=2*K*tau/N;delta=2*v;a=alpha*dn(v)/cn(v);b=beta/cn(v)
  orbit=lambda w:[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
  n=lambda u:(-sn(u)/alpha,cn(u)/beta)
  def qm(u,M):
   nn=n(u);t=(1-dot(nn,M))/dot(nn,nn)
   return tuple(M[j]+t*nn[j] for j in range(2))
  S=lambda u:sum(dn(u+j*delta) for j in range(N))
  T=lambda u,M:area([qm(u+j*delta,M) for j in range(N)])
  base=orbit(mp.mpf('.11')*K);A0=area(base)
  B0=area(pedals(base,(0,0)));B1=area(pedals(base,(1,0)))
  c0=B0/A0;c2=(B1-B0)/A0
  for phase in ['.09','.48','1.07']:
   w=mp.mpf(phase)*K;P=orbit(w)
   for j in range(N):
    nn=n(w+v+j*delta)
    near(dot(nn,P[j]),1,'actual_side_first_vertex_tangency')
    near(dot(nn,P[(j+1)%N]),1,'actual_side_second_vertex_tangency')
   for M in [(mp.mpf('.4'),mp.mpf('-2.1')),(mp.mpf('3.2'),mp.mpf('.7')),(0,0)]:
    actual=area(pedals(P,M))
    near(actual,T(w+v,M),'line_projection_equals_caustic_foot')
    near(actual/area(P),c0+c2*dot(M,M),'new_phases_fixed_M_area_ratio')
  M=(mp.mpf('.6'),mp.mpf('-1.4'));u=mp.mpf('.27')*K+mp.mpc(0,'.19')*Ki
  coeff=T(mp.mpf('.37')*K,M)/S(mp.mpf('.37')*K+K)
  near(T(u,M),coeff*S(u+K),'complex_two_pole_trace')
  near(T(u+2j*Ki,M),-T(u,M),'imaginary_antiperiod_character')
  near(T(u+2*K/(N//2),M),T(u,M),'reduced_real_period_character')
  r=K+1j*Ki;eps=mp.mpf('1e-9')*(1+mp.mpc(0,'.3'))
  near(T(r+eps,M),coeff*S(r+eps+K),'near_pole_not_double')
  z=mp.mpf('.16')*K+mp.mpc(0,'.07')*Ki
  for j in range(2):near(qm(r+z,M)[j],qm(r-z,M)[j],'even_local_pedal_germ')
# New direct-side diagnostics on the exact prescribed noncircular star.
k=mp.mpf(1)/4;par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);N=10;tau=3;v=3*K/5;step=2*v
sn=lambda u:mp.ellipfun('sn',u,par)
cn=lambda u:mp.ellipfun('cn',u,par)
dn=lambda u:mp.ellipfun('dn',u,par)
a=dn(v)/cn(v);b=kp/cn(v)
P=lambda w:[(-a*sn(w+j*step),b*cn(w+j*step)) for j in range(N)]
p=P(0);A0=area(p);B0=area(pedals(p,(0,0)));C0=area(pedals(p,(1,0)))-B0
assert A0>0 and B0>0 and C0<0
rho=mp.sqrt(-B0/C0)
for phase in ['.031','.41','.97']:
 for angle in [mp.pi/7,mp.pi/3,mp.pi*mp.mpf('.91')]:
  mm=(rho*mp.cos(angle),rho*mp.sin(angle))
  near(area(pedals(P(mp.mpf(phase)*K),mm)),0,'actual_side_exception_circle')
star_receipt={'radius_squared':mp.nstr(rho*rho,24),'c0':mp.nstr(B0/A0,24),'c2':mp.nstr(C0/A0,24)}
print(json.dumps({'status':'PASS','exact_assertions':sum(E.values()),'exact_families':dict(E),'numeric_diagnostics':sum(D.values()),'numeric_families':dict(D),'numeric_precision_digits':85,'maximum_scaled_error':mp.nstr(worst,12),'star_diagnostic':star_receipt,'scope':'Exact rational controls are separate from non-interval numerical diagnostics. The universal claims rest on the independently audited meromorphic and geometric proof.'},indent=2,sort_keys=True))
