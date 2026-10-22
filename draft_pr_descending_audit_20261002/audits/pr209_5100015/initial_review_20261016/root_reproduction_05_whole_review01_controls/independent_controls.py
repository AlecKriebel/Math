"""Fresh finite adversarial controls: rigid Euclidean frames/units, nonprimitive
listings, extreme moduli, and every shifted residue of composite odd traces.
No candidate checker imported; no network; not interval certification or proof.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import datetime,hashlib,json
import mpmath as mp
mp.mp.dps=120
O=Path(__file__).resolve().parent
count={};maxerr=mp.mpf(0)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def area(p):return sum(det(x,p[(i+1)%len(p)]) for i,x in enumerate(p))/2
def test(name,cond):
 assert cond,name
 count[name]=count.get(name,0)+1
def near(name,x,y,tol=mp.mpf('1e-70')):
 global maxerr
 e=abs(x-y)/max(mp.mpf(1),abs(x),abs(y));maxerr=max(maxerr,e)
 test(name,e<tol)
def geometry(p,n,center):
 h=[1+dot(z,center) for z in n];r=[]
 for i,ni in enumerate(n):
  j=(i+1)%len(n);nj=n[j];de=det(ni,nj)
  r.append(((h[i]*nj[1]-ni[1]*h[j])/de,(ni[0]*h[j]-h[i]*nj[0])/de))
 q=[]
 for i,ri in enumerate(r):
  line=sub(ri,r[i-1]);normal=(-line[1],line[0]);offset=dot(normal,sub(ri,center))/dot(normal,normal)
  foot=(center[0]+offset*normal[0],center[1]+offset*normal[1]);q.append(foot)
  near('foot_actual_outer_side_incidence',det(sub(foot,ri),line),0)
  near('foot_actual_outer_side_orthogonality',dot(sub(foot,center),line),0)
 rc=[sub(z,center) for z in r];qc=[sub(z,center) for z in q]
 return area(rc),area(qc)
rows=[]
for kstr,N,tau in [('0.00000001',3,1),('0.37',5,2),('0.83',9,4),('0.99999999',7,3),('0.91',10,3),('0.56',14,5),('0.7',9,3),('0.7',18,3)]:
 k=mp.mpf(kstr);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);v=2*tau*K/N;al=mp.mpf('1.7');be=al*kp
 sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
 a=al*dn(v)/cn(v);b=be/cn(v);f=lambda z:sn(z)*cn(z)/dn(z)
 least=N//gcd(tau,N);repeat=gcd(tau,N);q=least//gcd(least,2);r=least//q
 C=mp.fprod((cn(2*K*j/q)/sn(2*K*j/q))**2 for j in range(1,(q-1)//2+1))
 predicted=a*a*b**4*f(v)*(2*f(v)-f(2*v))/(4*al*be*cn(K-v)**2)*repeat**2*r*r*kp**q/C**2
 vals=[]
 for phase in ['0.123','0.789','1.301']:
  u=mp.mpf(phase)*K
  p=[(-a*sn(u+2*j*v),b*cn(u+2*j*v)) for j in range(N)]
  n=[(x/a**2,y/b**2) for x,y in p]
  ap,aq=geometry(p,n,(mp.mpf(0),mp.mpf(0)));vals.append(ap*aq)
  near('closed_formula_nonprimitive_and_extreme',ap*aq,predicted)
  near('least_period_repeat_geometry',ap*aq,repeat**2*mp.fprod(geometry(p[:least],n[:least],(0,0))))
  for scale,reflect in [('0.0000000001',1),('10000000000',-1)]:
   s=mp.mpf(scale);t=mp.mpf('.731');co=mp.cos(t);si=mp.sin(t);center=(s*mp.mpf('2e5'),-s*mp.mpf('3e5'))
   rot=lambda z:(co*z[0]-reflect*si*z[1],si*z[0]+reflect*co*z[1])
   pp=[(center[0]+s*rot(z)[0],center[1]+s*rot(z)[1]) for z in p]
   nn=[(rot(z)[0]/s,rot(z)[1]/s) for z in n]
   # n'.(p'-center)=1 gives the translated/rotated physical tangent.
   for p1,n1 in zip(pp,nn):near('transformed_tangent_incidence',dot(n1,sub(p1,center)),1)
   bp,bq=geometry(pp,nn,center)
   near('individual_signed_area_rigid_frame_units',bp,reflect*s*s*ap)
   near('individual_signed_pedal_rigid_frame_units',bq,reflect*s*s*aq)
   near('product_length_four_units',bp*bq,s**4*predicted)
 near('phase_constancy_new_extreme_samples',max(vals),min(vals))
 rows.append(dict(k=kstr,N=N,tau=tau,least=least,repeat=repeat,predicted_product=mp.nstr(predicted,45)))
# Exact rational four-period controls in three arbitrary distinct unit scales.
exact=[]
for a,b in [(F(5),F(2)),(F(7,3),F(4,3)),(F(2,1000),F(1,1000))]:
 # Diamond product 8a²b²; rectangle product2(a²+b²)², common
 # lambda=a²b²/(a²+b²). Rectangle coordinates use sqrtS but area
 # and caustic/reflection checks reduce rationally to the values below.
 S=a*a+b*b;L=a*a*b*b/S
 test('exact_N4_strict_caustic',0<L<b*b)
 test('exact_N4_diamond_tangency',(a*a-L)/(a*a)+(b*b-L)/(b*b)==1)
 test('exact_N4_rectangle_vertical_tangent',a**4/S==a*a-L)
 test('exact_N4_rectangle_horizontal_tangent',b**4/S==b*b-L)
 test('exact_N4_products_gap',2*S*S-8*a*a*b*b==2*(a*a-b*b)**2>0)
 exact.append(dict(a=str(a),b=str(b),lam=str(L),diamond_product=str(8*a*a*b*b),rectangle_product=str(2*S*S)))
poles=[]
for kstr in ['0.00000001','0.73','0.99999999']:
 k=mp.mpf(kstr);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);Ki=mp.ellipk(1-m)
 dn=lambda z:mp.ellipfun('dn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);sn=lambda z:mp.ellipfun('sn',z,m)
 for q in [1,3,9,15]:
  shifts=[2*K*j/q for j in range(q)];C=mp.fprod((cn(shifts[j])/sn(shifts[j]))**2 for j in range(1,(q-1)//2+1))
  U=lambda z:sum(dn(z+h) for h in shifts);V=lambda z:mp.fprod(dn(z+h) for h in shifts)
  for j,h in enumerate(shifts):
   pole=1j*Ki-h;eps=mp.mpc('1e-22','-3e-23')
   near('every_shifted_U_residue',eps*U(pole+eps),-1j,mp.mpf('1e-35'))
   near('every_shifted_V_residue_normalization',eps*V(pole+eps),-1j*C,mp.mpf('1e-35'))
   near('every_complementary_trace_zero',U(pole+K),0)
  for z in [K*mp.mpf('.213')+1j*Ki*mp.mpf('.17'),K*mp.mpf('.653')-1j*Ki*mp.mpf('.27')]:
   near('classical_product_to_sum_extreme_composite',V(z),C*U(z))
   near('trace_normalization_extreme_composite',U(z)*U(z+K),kp**q/C**2)
  poles.append(dict(k=kstr,q=q,all_shifted_poles=q))
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',program_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),mpmath=mp.__version__,digits=mp.mp.dps,checks=count,total_checks=sum(count.values()),maximum_scaled_error=mp.nstr(maxerr,20),geometry=rows,exact_N4=exact,poles=poles,limits='Finite arbitrary-precision diagnostics, not interval certificates; exact rational N4 identities separately labelled. Written universal proof is independently checked in independent_proof.md.')
(O/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['geometry','exact_N4','poles']},indent=2))
