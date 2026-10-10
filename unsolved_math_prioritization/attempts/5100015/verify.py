#!/usr/bin/env python3
"""k303,b author exact controls and separate high-precision diagnostics.
Self-authored; standard library plus installed SymPy/mpmath; no network.
Finite controls support the analytic proof, not a numerical all-phase claim.
The two exact six-period witness geometries are credited to campaign PR148.
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter
from pathlib import Path
import json,hashlib
import sympy as sp
C=Counter();D=Counter()
def ck(g,b):assert b,g;C[g]+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def area(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def tangent_and_center_pedal(p,a2,b2):
 n=[(x/a2,y/b2) for x,y in p];outer=[];pedal=[]
 for i,x in enumerate(n):
  y=n[(i+1)%len(p)];h=det(x,y);assert h!=0
  outer.append(((y[1]-x[1])/h,(x[0]-y[0])/h))
  nn=dot(x,x);pedal.append((x[0]/nn,x[1]/nn))
 return outer,pedal

# Exact Jacobi-addition algebra, treating the elliptic values as variables.
s,c,d,t,e,f,k2=sp.symbols('s c d t e f k2');den=1-k2*s*s*t*t
sp_= (s*e*f+t*c*d)/den;sm=(s*e*f-t*c*d)/den
cp=(c*e-s*t*d*f)/den;cm=(c*e+s*t*d*f)/den
num=sp.fraction(sp.factor(cm*sp_-sm*cp-2*t*e*d/den))[0]
ck('symbolic_edge_determinant',sp.expand(num).subs(c*c,1-s*s).subs(f*f,1-k2*t*t).expand()==0)
dp=(d*f-k2*s*c*t*e)/den;dm=(d*f+k2*s*c*t*e)/den
ck('symbolic_dn_pair_sum',sp.cancel(dp+dm-2*d*f/den)==0)
a,b,z,cw=sp.symbols('a b z cw',nonzero=True);cc=sp.symbols('cc');dnorm=1-(1-b*b/(a*a))*z*z
normal=sp.Matrix([-z/a,cc/b]);q=normal/(normal.dot(normal))
pair=sp.Matrix([-2*b*z*cw/dnorm,2*b*cc*cw/dnorm]);L=sp.diag(b/a,1)/(2*cw)
for j in range(2):
 num=sp.fraction(sp.cancel(q[j]-(L*pair)[j]))[0]
 ck('symbolic_center_projection_edge_map',sp.rem(sp.expand(num),cc**2+z**2-1,cc).expand()==0)
ck('symbolic_edge_map_determinant',sp.cancel(L.det()-b/(4*a*cw*cw))==0)

# Area-of-edge-vector identity for arbitrary ordered rational polygons.
for N in range(3,26):
 p=[(F((i*i+3*i)%17,5),F((i**3+2)%19,7)) for i in range(N)]
 for step in range(1,N):
  if gcd(step,N)!=1:continue
  pp=[p[(i*step)%N] for i in range(N)]
  edges=[sub(pp[(i+1)%N],pp[i]) for i in range(N)]
  skip=sum(det(pp[i],pp[(i+2)%N]) for i in range(N))/2
  ck('cyclic_edge_area_identity',area(edges)==2*area(pp)-skip)
  ck('global_minus_preserves_signed_area',area([(-x,-y) for x,y in edges])==area(edges))

# Primitive arithmetic and all reduced trace-shift multiplicities.
for N in range(3,102):
 if N%4==0:continue
 for tau in range(1,(N+1)//2):
  if gcd(tau,N)!=1:continue
  r=gcd(N,2);q=N//r;group=[F(j,q) for j in range(q)]
  shifts=[F(2*j*tau,N)%1 for j in range(N)]
  ck('effective_order_odd',q%2==1)
  ck('complete_reduced_subgroup',Counter(shifts)==Counter({j:r for j in group}))
  ck('no_K_in_odd_subgroup',F(1,2) not in group)
  ck('reflection_pairing_subgroup',set(group)==set((-j)%1 for j in group))

# Exact genuine six-period pair from PR148: verify tangent/pedal construction.
sqrt=sp.sqrt;R=sp.Rational
H=[(2,0),(R(4,3),sqrt(5)/3),(-R(4,3),sqrt(5)/3),(-2,0),(-R(4,3),-sqrt(5)/3),(R(4,3),-sqrt(5)/3)]
V=[(0,1),(-4*sqrt(2)/3,R(1,3)),(-4*sqrt(2)/3,-R(1,3)),(0,-1),(4*sqrt(2)/3,-R(1,3)),(4*sqrt(2)/3,R(1,3))]
six=[]
for p in (H,V):
 p=[tuple(map(sp.sympify,x)) for x in p];outer,pedal=tangent_and_center_pedal(p,sp.Integer(4),sp.Integer(1))
 for i,q in enumerate(pedal):
  norm=(p[i][0]/4,p[i][1]);ck('six_period_tangent_incidence',sp.simplify(dot(q,norm)-1)==0)
  ck('six_period_perpendicular',sp.simplify(det(q,norm))==0)
 ap,aq=map(sp.simplify,(area(outer),area(pedal)));ck('six_period_exact_product',sp.simplify(ap*aq-40)==0);six.append([str(ap),str(aq),str(sp.simplify(ap*aq))])
# Excluded N=4 negative control, not a claimed counterexample to the target.
P=[(F(4),F(0)),(F(0),F(3)),(-F(4),F(0)),(F(0),-F(3))]
Q=[(F(16,5),F(9,5)),(-F(16,5),F(9,5)),(-F(16,5),-F(9,5)),(F(16,5),-F(9,5))]
vals=[]
for p in (P,Q):
 out,ped=tangent_and_center_pedal(p,F(16),F(9));vals.append(area(out)*area(ped))
ck('excluded_period_four_varies',vals==[F(1152),F(1250)])

# Geometric and complex analytic diagnostics using parameter k^2 in mpmath.
import mpmath as mp
mp.mp.dps=90;maxerr=mp.mpf(0);families=0;stars=0;odd_families=0
def near(g,a,b):
 global maxerr
 err=abs(a-b)/max(mp.mpf(1),abs(a),abs(b));maxerr=max(maxerr,err)
 assert err<mp.mpf('1e-54'),(g,mp.nstr(err,12))
 D[g]+=1
for k in [mp.mpf('.31'),mp.mpf('.67'),mp.mpf('.89')]:
 par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Ki=mp.ellipk(1-par);al=mp.mpf('1.4');be=al*kp
 sn=lambda u:mp.ellipfun('sn',u,par);cn=lambda u:mp.ellipfun('cn',u,par);dn=lambda u:mp.ellipfun('dn',u,par)
 f=lambda z:sn(z)*cn(z)/dn(z)
 for N in [3,5,6,7,9,10,11,14]:
  for tau in range(1,(N+1)//2):
   if gcd(tau,N)!=1:continue
   families+=1;stars+=tau>1;odd_families+=N%2==1
   v=2*tau*K/N;step=2*v;a=al*dn(v)/cn(v);b=be/cn(v);w=K-v;cnw=cn(w)
   T=lambda z:sum(dn(z+j*step) for j in range(N));r=gcd(N,2);q=N//r
   U=lambda z:sum(dn(z+2*K*j/q) for j in range(q))
   P=lambda z:(-a*sn(z),b*cn(z));coeff=a*a*b**4*f(v)*(2*f(v)-f(2*v))/(4*al*be*cnw**2)
   product0=coeff*T(0)*T(K)
   for phase in [mp.mpf('.119'),mp.mpf('.467'),mp.mpf('.913')]:
    u=phase*K;p=[P(u+j*step) for j in range(N)];out,ped=tangent_and_center_pedal(p,a*a,b*b)
    A=area(p);Ap=area(out);Aq=area(ped)
    near('original_area_trace',A,a*b*f(v)*T(u))
    near('outer_area_trace',Ap,a*a*b*b/(al*be)*f(v)*T(u+v))
    near('outer_center_pedal_area_trace',Aq,b*b/(4*cnw**2)*(2*f(v)-f(2*v))*T(u+K-v))
    near('full_product_constancy',Ap*Aq,product0)
    near('trace_product_constancy',T(u)*T(u+K),T(0)*T(K))
    for j in range(N):
     z=u+j*step;R0=P(z+K-v);R1=P(z+K+v)
     pred=((b/a)*(R0[0]-R1[0])/(2*cnw),(R0[1]-R1[1])/(2*cnw))
     for i in range(2):near('pointwise_pedal_edge_map',ped[j][i],pred[i])
   z=mp.mpf('.173')*K+mp.mpf('.231')*1j*Ki
   near('trace_reduction_to_odd_subgroup',T(z),r*U(z))
   near('complex_trace_product',T(z)*T(z+K),T(0)*T(K))
   near('complex_imaginary_antiperiod',U(z+2j*Ki),-U(z))
   near('reflected_center_zero',U(K+1j*Ki),0)
   eps=mp.mpf('1e-9')*(1+mp.mpf('.2')*1j)
   near('near_pole_product_removable',T(1j*Ki+eps)*T(1j*Ki+eps+K),T(0)*T(K))

root=Path(__file__).resolve().parent
receipt={'status':'PASS','proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'precision_digits':90,'maximum_scaled_error':mp.nstr(maxerr,14),'primitive_families':families,'odd_period_families':odd_families,'star_families':stars,'exact_six_period_areas_and_product':six,'excluded_four_period_products':list(map(str,vals)),'limits':'Exact algebra and finite controls plus non-interval high-precision diagnostics. The analytic proof establishes the universal claim; numerical sampling does not.'}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
