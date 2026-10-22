"""Fresh review checks organized independently of the supplied verifiers.
Finite numeric tests are diagnostics; exact algebra checks are not the analytic proof.
"""
from pathlib import Path
import json,math,datetime,hashlib
import sympy as s
import mpmath as mp
O=Path(__file__).resolve().parent.parent
exact=[]
def zero(name,e,ring=None):
 n=s.together(e).as_numer_denom()[0]
 if ring:n=ring.reduce(s.expand(n))[1]
 n=s.factor(n)
 if n!=0:raise RuntimeError(name+': '+str(n))
 exact.append(name)
# Derive the circle chord tangency criterion, including its excluded zero chord.
X,Y,U1,V1=s.symbols('X Y U1 V1')
ring=s.groebner([X*X+Y*Y-1,U1*U1+V1*V1-1],X,Y,U1,V1)
normal=(Y-V1,U1-X);support=Y*U1-X*V1
conic=s.Rational(4,9)*normal[0]**2+s.Rational(1,9)*normal[1]**2-support**2
zero('circle_chord_tangency_factorization',conic+s.Rational(2,9)*(1-X*U1-Y*V1)*(3*X*U1+6*Y*V1+2),ring)
# Independently form the physical local identity coefficients and compare the 3 polynomial coefficients.
r,t,x=s.symbols('r t x');q=1-t
U=1-2*r*t+r*t*t;V=1-2*t+r*t*t;W=1-r*t*t
H=U*U-r*V*V*x
Lambda=U*(r*r*t**3+r*r*t*t-5*r*t+r+2)/(2*(1-r)**2*W**3)
a0=q/(U-V)**2;a1=(Lambda-a0)/2
# 4 r h cv dv V a2 equals this expression, cancelling the positive real factors.
dcoef=r*V*(V*V-U*U*t)/((U*U-r*V*V)*(U-V))
res=(1-r*t*x)*(U*U+r*V*(V+2*U)*x)-a0*H**2-2*W*U*a1*(1-r*x)*H-dcoef*(1-r*x)*(U*U+(r*V*V-2*U*U)*x)
respoly=s.Poly(s.together(res).as_numer_denom()[0],x)
for i in range(3):zero('direct_physical_local_coefficient_'+str(i),respoly.nth(i))
zero('positive_Lambda_bracket',r*r*t**3+r*r*t*t-5*r*t+r+2-(2*(1-r)**2+5*r*(1-r)*q+r*r*q*q*(4-q)))
# m=N/2 halfgrid and exhaustive finite collision congruences, including nontrivial star windings.
closure_count=0
for N in range(4,257,4):
 m=N//2
 for tau in range(1,N//2):
  if math.gcd(N,tau)!=1:continue
  if sorted((j*tau)%m for j in range(m))!=list(range(m)):raise RuntimeError('grid not permutation')
  if (m+tau)%2!=1:raise RuntimeError('shift is not halfintegral')
  if any((N+2*tau*(2*j+1))%(2*N)==0 for j in range(N)):raise RuntimeError('singular real collision')
  closure_count+=1
mp.mp.dps=150
numeric=[];maximum=mp.mpf(0)
def check(error,label):
 global maximum
 if not mp.isfinite(error) or error>mp.mpf('1e-90'):raise RuntimeError(label+': '+str(error))
 maximum=max(maximum,error)
def rel(a,b):return abs(a-b)/max(1,abs(a),abs(b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
for ks in ['0.001','0.2','0.7','0.99','0.999999999999']:
 k=mp.mpf(ks);par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par)
 sn=lambda z:mp.ellipfun('sn',z,par)
 cn=lambda z:mp.ellipfun('cn',z,par)
 dn=lambda z:mp.ellipfun('dn',z,par)
 F=lambda z:1/dn(z)
 Fp=lambda z:par*sn(z)*cn(z)/dn(z)**2
 for fraction in ['0.01','0.25','0.5','0.75','0.99']:
  v=K*mp.mpf(fraction);delta=2*v;h=sn(v);cv=cn(v);dv=dn(v);t=h*h;q=cv*cv
  a=dv/cv;b=kp/cv;C0=b*h*dv*cv**4
  U=1-2*par*t+par*t*t;V=1-2*t+par*t*t;W=1-par*t*t
  L=U*(par**2*t**3+par**2*t*t-5*par*t+par+2)/(2*kp**4*W**3)
  a0=q/(U-V)**2;a1=(L-a0)/2;a2=(V*V-U*U*t)/(4*h*cv*dv*(U*U-par*V*V)*(U-V))
  def point(u):return (-a*sn(u),b*cn(u))
  def inv(p):
   z=(p[0]-k,p[1]);d=z[0]**2+z[1]**2
   return (z[0]/d,z[1]/d)
  def E(u):return det(inv(point(u-v)),inv(point(u+v)))/2
  for phase in ['-1.9','-0.4','0','0.21','1.3','2.4']:
   u=K*mp.mpf(phase);z=sn(u)
   pair=E(u)+E(u+2*K)
   formula=2*C0*(1-par*t*z*z)*(U*U+par*V*(V+2*U)*z*z)/(dn(u)*(U*U-par*V*V*z*z)**2)
   local=2*C0*(a0*F(u)+a1*(F(u+delta)+F(u-delta))+a2*(Fp(u+delta)-Fp(u-delta)))
   check(rel(pair,formula),'direct Euclidean pair')
   check(rel(pair,local),'direct local identity')
  numeric.append({'k':ks,'v_over_K':fraction,'samples':6})
# Independent finite Fourier/Landen comparison and complex residue checks.
complex_checks=[]
for ks in ['0.1','0.7','0.999']:
 k=mp.mpf(ks);par=k*k;K=mp.ellipk(par);Kp=mp.ellipk(1-par);nome=mp.exp(-mp.pi*Kp/K)
 for m in [2,4,6,10,32]:
  Q=nome**m;theta3=mp.jtheta(3,0,Q);kappa=(mp.jtheta(2,0,Q)/theta3)**2;Km=mp.pi*theta3**2/2;lam=m*Km/K;kapr=(mp.jtheta(4,0,Q)/theta3)**2
  S=lambda w:mp.fsum(mp.ellipfun('dn',w+2*K*j/m,par) for j in range(m))
  for phase in ['0','0.137','0.73']:
   w=K*mp.mpf(phase)
   check(rel(S(w),lam*mp.ellipfun('dn',lam*w,kappa*kappa)),'Landen scale')
   check(rel(S(w)*S(w+K/m),lam*lam*kapr),'halfgrid product')
  eps=mp.mpf('1e-50');pole=1j*Kp
  check(abs(eps*S(pole+eps)+1j),'reduced dn residue -i')
  check(abs(eps*S(3*pole+eps)-1j),'reduced dn residue +i')
  complex_checks.append({'k':ks,'m':m})
# Recompute the complete connected triangle path with actual physical rays/reflection and direct inversions.
triangle_checks=[]
max_reflect=mp.mpf(0);min_orientation=mp.inf;min_contact=mp.inf
products=[]
for index in range(101):
 theta=mp.pi*index/100;X=mp.cos(theta);Y=mp.sin(theta);n=(3*X,6*Y);D=n[0]**2+n[1]**2;root=mp.sqrt(D-4);Jn=(-n[1],n[0])
 neigh=[((-2*n[0]+sign*root*Jn[0])/D,(-2*n[1]+sign*root*Jn[1])/D) for sign in [1,-1]]
 pts=[(2*mp.sqrt(2)*x,mp.sqrt(5)*y) for x,y in [(X,Y),*neigh]]
 for j,p in enumerate(pts):
  before=pts[(j-1)%3];after=pts[(j+1)%3]
  incoming=(p[0]-before[0],p[1]-before[1]);outgoing=(after[0]-p[0],after[1]-p[1])
  norm=lambda z:mp.sqrt(z[0]**2+z[1]**2)
  incoming=tuple(z/norm(incoming) for z in incoming);outgoing=tuple(z/norm(outgoing) for z in outgoing)
  normal=(p[0]/8,p[1]/5);dot=lambda x,y:x[0]*y[0]+x[1]*y[1]
  reflected=tuple(incoming[d]-2*dot(incoming,normal)*normal[d]/dot(normal,normal) for d in [0,1])
  err=norm(tuple(outgoing[d]-reflected[d] for d in [0,1]));check(err,'connected physical reflection');max_reflect=max(max_reflect,err)
  nv=(after[1]-p[1],p[0]-after[0]);J=dot(nv,p);contact=(mp.mpf(32)/9*nv[0]/J,mp.mpf(5)/9*nv[1]/J)
  step=tuple(after[d]-p[d] for d in [0,1]);fraction=dot(tuple(contact[d]-p[d] for d in [0,1]),step)/dot(step,step)
  if not 0<fraction<1:raise RuntimeError('noninternal tangent contact')
  min_contact=min(min_contact,fraction,1-fraction)
 orientation=mp.fsum(det(p,pts[(j+1)%3]) for j,p in enumerate(pts))/2
 if orientation<=0:raise RuntimeError('triangle orientation lost')
 min_orientation=min(min_orientation,orientation)
 inv=[]
 for p in pts:
  z=(p[0]-mp.sqrt(3),p[1]);d=z[0]**2+z[1]**2;inv.append((z[0]/d,z[1]/d))
 invarea=mp.fsum(det(p,inv[(j+1)%3]) for j,p in enumerate(inv))/2
 products.append(orientation*invarea)
check(rel(16*(products[0]-products[-1]),-20*mp.sqrt(6)/9),'independent repeated triangle difference')
result={'schema':'fresh-independent-mathematical-checks-v1','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','sympy':s.__version__,'mpmath':mp.__version__,'precision_dps':mp.mp.dps,'exact_checks':exact,'coprime_lattice_cases_through_N256':closure_count,'local_numeric_cases':numeric,'complex_grid_cases':complex_checks,'maximum_normalized_error':mp.nstr(maximum,40),'connected_triangle_path_points':101,'minimum_contact_margin':mp.nstr(min_contact,40),'minimum_positive_area':mp.nstr(min_orientation,40),'maximum_physical_reflection_error':mp.nstr(max_reflect,40),'repeated_difference':mp.nstr(16*(products[0]-products[-1]),40),'scope':'Finite independent algebra/congruence/numerical checks. No interval or universal analytic certificate, novelty or priority claim.'}
(O/'INDEPENDENT_MATH_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('local_numeric_cases','complex_grid_cases')},indent=2))
