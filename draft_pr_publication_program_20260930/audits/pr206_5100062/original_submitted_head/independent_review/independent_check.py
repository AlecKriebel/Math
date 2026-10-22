"""Independent exact structural checks and separate numerical k903,a diagnostics."""
from collections import Counter
from math import gcd
from pathlib import Path
import sympy as s,json
C=Counter();D=Counter()
def ck(g,b):
 assert b,g
 C[g]+=1
x,y,f=s.symbols('x y f');den=(x-f)**2+y*y
qx=f+(x-f)/den;qy=y/den
ck('complex_U_inversion',s.cancel(qx+s.I*qy-f-1/(x-s.I*y-f))==0)
ck('complex_V_inversion',s.cancel(qx-s.I*qy-f-1/(x+s.I*y-f))==0)
x0,y0,x1,y1=s.symbols('x0 y0 x1 y1');z0=x0+s.I*y0;w0=x0-s.I*y0;z1=x1+s.I*y1;w1=x1-s.I*y1
ck('complex_signed_determinant',s.expand((w0*z1-z0*w1)/(2*s.I)-(x0*y1-y0*x1))==0)
a,b,L=s.symbols('a b L',positive=True);c=s.sqrt(a*a-b*b)
for eps in [-1,1]:
 foc=eps*c;px=eps*a*a/c
 # Restrict the ellipse to either isotropic line x +/- i y=f.
 residual=x*x/a**2-(x-foc)**2/b**2-1
 ck('isotropic_line_double_contact',s.simplify(residual+c*c/(a*a*b*b)*(x-px)**2)==0)
 for eta in [-1,1]:
  py=eta*s.I*b*b/c;Z=px+s.I*py;W=px-s.I*py
  ck('exact_contact_on_ellipse',s.simplify(px*px/a**2+py*py/b**2-1)==0)
  ck('common_tangent_dual',s.simplify((a*a-L)*px*px/a**4+(b*b-L)*py*py/b**4-1)==0)
  ck('unramified_over_contact',s.simplify(px*px/(a*a-L)+py*py/(b*b-L)-1+L*L/((a*a-L)*(b*b-L)))==0)
  ck('exact_one_focal_denominator',s.simplify((Z-foc)*(W-foc))==0 and s.simplify(Z-W)!=0)
  ck('other_focal_denominator_regular',s.simplify((Z+foc)*(W+foc))!=0)
# Abstract orbit through a sigma-fixed flag: sigma(j)=-j and tau(j)=1-j.
for N in range(3,2004,2):
 fixed={j for j in range(N) if (2*j)%N==0}
 ck('odd_orbit_one_sigma_fixed',fixed=={0})
 contacts=fixed|{(j+1)%N for j in fixed}
 ck('exactly_two_singular_vertices',contacts=={0,1})
 ck('only_one_adjacent_pair',{(j,(j+1)%N) for j in contacts if (j+1)%N in contacts}=={(0,1)})
for N in range(4,1003,2):
 ck('even_orbit_negative_control',{j for j in range(N) if (2*j)%N==0}=={0,N//2})
# A single coordinate is singular in both adjacent inverted vertices.
t=s.symbols('t');u0,u1,v0,v1,A0,A1,B0,B1=s.symbols('u0 u1 v0 v1 A0 A1 B0 B1')
U0=u0+u1*t;U1=v0+v1*t;V0=A0/t**2+A1/t;V1=B0/t**2+B1/t
cross=s.expand(V0*U1-U0*V1)
for n in [-4,-3]:ck('no_order_four_or_three_area_pole',cross.coeff(t,n)==0)
odd=s.expand((cross-cross.subs(t,-t))/2)
ck('involution_removes_double_pole',odd.coeff(t,-2)==0)
reg=s.expand(odd*(t+t*t))
for n in [-4,-3,-2,-1]:ck('opposite_zero_removes_pole',reg.coeff(t,n)==0)
# Genuine even negative controls independently check same-caustic tangency.
rat=s.Rational;DD=[(4,0),(0,3),(-4,0),(0,-3)];RR=[(rat(16,5),rat(9,5)),(-rat(16,5),rat(9,5)),(-rat(16,5),-rat(9,5)),(rat(16,5),-rat(9,5))]
for P in [DD,RR]:
 P=[s.Matrix(p) for p in P];BB=s.diag(rat(1,16),rat(1,9));CC=s.diag(rat(256,25),rat(81,25))
 ck('even_control_primitive',len({tuple(p) for p in P})==4)
 for j,p in enumerate(P):
  q=P[(j+1)%4];r=P[j-1];ll=s.Matrix.vstack(p.T,q.T).inv()*s.Matrix([1,1]);ck('even_control_common_caustic',s.simplify(ll.dot(CC*ll)-1)==0)
  inc=p-r;inc=inc/s.sqrt(inc.dot(inc));out=q-p;out=out/s.sqrt(out.dot(out));nn=BB*p;err=inc-2*inc.dot(nn)*nn/nn.dot(nn)-out
  ck('even_control_reflection',all(s.simplify(v)==0 for v in err))
# Independent direct unit inversion on canonical actual orbits. Numeric only.
import mpmath as mp
mp.mp.dps=100;maxerr=mp.mpf(0)
def close(g,x,y):
 global maxerr
 e=abs(x-y)/max(1,abs(x),abs(y));maxerr=max(maxerr,e)
 assert e<mp.mpf('1e-55'),(g,mp.nstr(e,8))
 D[g]+=1
def area(P):return sum(P[j][0]*P[(j+1)%len(P)][1]-P[j][1]*P[(j+1)%len(P)][0] for j in range(len(P)))/2
for k in [mp.mpf('.19'),mp.mpf('.61'),mp.mpf('.92')]:
 par=k*k;K=mp.ellipk(par);Kp=mp.ellipk(1-par);kp=mp.sqrt(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [3,5,7,9,11,15]:
  for tau in range(1,N//2+1):
   if gcd(tau,N)!=1:continue
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v)
   def P(u):return [(-a*sn(u+j*delta),b*cn(u+j*delta)) for j in range(N)]
   def inv(ps,f,rho=1):
    qs=[]
    for x,y in ps:
     den=(x-f)**2+y*y;qs.append((f+rho*rho*(x-f)/den,rho*rho*y/den))
    return qs
   def ff(u,f):return area(inv(P(u),f))
   ref=None
   for phase in [mp.mpf('.083'),mp.mpf('.357'),mp.mpf('.829')]:
    u=phase*K;ps=P(u);fp=ff(u,k);fm=ff(u,-k)
    if ref is None:ref=fp*fm
    close('odd_product_direct_real',fp*fm,ref)
    for f,val in [(k,fp),(-k,fm)]:
     close('signed_reversal_fixed_focus',area(inv(list(reversed(ps)),f)),-val)
     close('radius_scaling_area',area(inv(ps,f,2)),16*val)
   u=mp.mpf('.174')*K+mp.mpf('.129')*1j*Kp
   close('generic_complex_product',ff(u,k)*ff(u,-k),ref)
   # The sigma-fixed parameter s0 contacts the negative-focus isotropic line.
   s0=K+1j*Kp-v;eps=mp.mpf('1e-9')*(1+mp.mpf('.3')*1j)
   pp=P(s0);close('coalescing_first_vertices_x',pp[0][0],pp[1][0]);close('coalescing_first_vertices_y',pp[0][1],pp[1][1])
   close('negative_contact_x',pp[0][0],-a*a/k);close('negative_contact_y',pp[0][1],-1j*b*b/k)
   close('opposite_area_zero_at_fixed_flag',ff(s0,k),0)
   for f in [k,-k]:close('local_reversal_Laurent_odd',ff(s0+eps,f),-ff(s0-eps,f))
   close('near_pole_product',ff(s0+eps,k)*ff(s0+eps,-k),ref)
root=Path(__file__).resolve().parent
r={'verdict':'PASS','exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'precision_digits':100,'maximum_scaled_residual':mp.nstr(maxerr,14),'limits':'Finite controls, including near-pole diagnostics, are not interval proofs; written audit checks all-period geometry and multiplicities.'};(root/'independent_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
