"""Own source-first finite Cartesian controls. No project/native imports or file writes."""
from datetime import datetime,timezone
import json
import sympy as s
import mpmath as mp


def simp(x):return s.simplify(x)
def dot(x,y):return (x.T*y)[0]
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def norm(x):return s.sqrt(simp(dot(x,x)))
def area(points):return simp(sum(det(points[i],points[(i+1)%len(points)]) for i in range(len(points)))/2)
def scalar(x):return str(simp(x))
def exact_case(name,points,a2,b2,lam,R=None,center=None):
 R=s.eye(2) if R is None else R
 center=s.zeros(2,1) if center is None else center
 G=R*s.diag(1/a2,1/b2)*R.T
 Gc=R*s.diag(1/(a2-lam),1/(b2-lam))*R.T
 ps=[s.Matrix(p) for p in points];N=len(ps);c=s.sqrt(a2-b2)
 normals=[G*(p-center) for p in ps]
 outer=[];fail=[];zero=[]
 for i,p in enumerate(ps):
  zero.append(simp(dot(p-center,G*(p-center))-1))
  q=ps[(i+1)%N];direction=q-p;A=s.Matrix([direction[1],-direction[0]])
  C=dot(A,p-center)
  # Support function of the caustic in actual Cartesian normal coordinates.
  zero.append(simp(C*C-dot(A,Gc.inv()*A)))
  previous=ps[(i-1)%N];incoming=(p-previous)/norm(p-previous);outgoing=(q-p)/norm(q-p);n=normals[i]
  residual=incoming-2*dot(incoming,n)/dot(n,n)*n-outgoing
  zero.extend(simp(x) for x in residual)
  rows=s.Matrix.vstack(normals[i].T,normals[(i+1)%N].T)
  if simp(rows.det())==0:fail.append('parallel outer tangents')
  rhs=s.Matrix([1+dot(normals[i],center),1+dot(normals[(i+1)%N],center)])
  outer.append(rows.inv()*rhs)
 Bs=[]
 for sign in [1,-1]:
  focus=center+R*s.Matrix([sign*c,0]);feet=[]
  for i,p in enumerate(ps):
   A=outer[(i-1)%N];B=outer[i];d=B-A;n=s.Matrix([d[1],-d[0]])
   foot=focus-dot(focus-A,n)/dot(n,n)*n
   foot=s.simplify(foot)
   # Distinct direct tangent-normal construction; this does not use source Q(w).
   direct=focus+(1-dot(normals[i],focus-center))/dot(normals[i],normals[i])*normals[i]
   zero.extend(simp(x) for x in foot-direct)
   zero.append(simp(dot(foot-center,foot-center)-a2))
   zero.append(simp(dot(foot-A,n)))
   zero.append(simp(det(foot-focus,n)))
   feet.append(foot)
  Bs.append(area(feet))
 fail += ['nonzero exact residual '+str(x) for x in zero if x!=0]
 return {'name':name,'N':N,'areas':[scalar(x) for x in Bs],'product':scalar(Bs[0]*Bs[1]),'exact_zero_residuals':len(zero),'failures':fail},Bs

A=s.Integer(8);B=s.Integer(3);lam=s.Rational(72,25);a=s.sqrt(A);b=s.sqrt(B)
H=[(a,0),(-4*a/5,3*b/5),(-4*a/5,-3*b/5)]
V=[(0,b),(-8*s.sqrt(3)/5,-b/5),(8*s.sqrt(3)/5,-b/5)]
D=[(a,0),(0,b),(-a,0),(0,-b)]
C=[(8/s.sqrt(11),3/s.sqrt(11)),(-8/s.sqrt(11),3/s.sqrt(11)),(-8/s.sqrt(11),-3/s.sqrt(11)),(8/s.sqrt(11),-3/s.sqrt(11))]
records=[];fail=[]
rec,BH=exact_case('new_triangle_H_A8_B3',H,A,B,lam);records.append(rec)
rec,BV=exact_case('new_triangle_V_same_caustic',V,A,B,lam);records.append(rec)
if simp(BH[0]*BH[1]-BV[0]*BV[1])!=0:fail.append('odd product differs across exact phases')
rec,BR=exact_case('H_reversed',list(reversed(H)),A,B,lam);records.append(rec)
if any(simp(BR[i]+BH[i])!=0 for i in [0,1]):fail.append('reversal area sign')
rec,B2=exact_case('H_twice_total_period6',H+H,A,B,lam);records.append(rec)
if any(simp(B2[i]-2*BH[i])!=0 for i in [0,1]):fail.append('repetition area scaling')
scale=s.Rational(7,3);R=s.Matrix([[0,-1],[1,0]]);center=s.Matrix([3,-4])
transformed=[center+scale*R*s.Matrix(p) for p in V]
rec,BS=exact_case('V_similarity_scale7over3_rotate_translate',transformed,scale**2*A,scale**2*B,scale**2*lam,R,center);records.append(rec)
if any(simp(BS[i]-scale**2*BV[i])!=0 for i in [0,1]):fail.append('similarity area dimensions')
rec,BD=exact_case('primitive_even_diamond',D,A,B,s.Rational(24,11));records.append(rec)
rec,BC=exact_case('primitive_even_rectangle_same_caustic',C,A,B,s.Rational(24,11));records.append(rec)
if simp(BD[0]*BD[1]-BC[0]*BC[1])==0:fail.append('even negative control failed to distinguish products')
fail += [str(rec['name'])+':'+x for rec in records for x in rec['failures']]

mp.mp.dps=90

def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(t,p):return(t*p[0],t*p[1])
def mdot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def munit(p):return mul(1/mp.sqrt(mdot(p,p)),p)
def launch(P,a,b,lam):
 alpha=mp.sqrt(a*a-lam);beta=mp.sqrt(b*b-lam);z=(P[0]/alpha,P[1]/beta);r2=mdot(z,z);coef=mp.sqrt(r2-1)
 for sign in [1,-1]:
  u=((z[0]-sign*coef*z[1])/r2,(z[1]+sign*coef*z[0])/r2)
  U=(alpha*u[0],beta*u[1]);d=munit(sub(U,P))
  if cross(P,d)>0:return d
 raise ValueError('no positively oriented tangent launch')
def trace(a,b,lam,N,phase=mp.mpf(0)):
 P=(a*mp.cos(phase),b*mp.sin(phase));initial=P;d=launch(P,a,b,lam);ps=[];angle=mp.mpf(0)
 for j in range(N):
  ps.append(P);den=d[0]**2/(a*a)+d[1]**2/(b*b);t=-2*(P[0]*d[0]/(a*a)+P[1]*d[1]/(b*b))/den
  Q=add(P,mul(t,d));x=(P[0]/a,P[1]/b);y=(Q[0]/a,Q[1]/b);inc=mp.atan2(cross(x,y),mdot(x,y))
  if inc<=0:inc+=2*mp.pi
  angle+=inc;n=(Q[0]/(a*a),Q[1]/(b*b));d=sub(d,mul(2*mdot(d,n)/mdot(n,n),n));P=Q
 return ps,P,initial,angle

def numeric_areas(ps,a,b):
 N=len(ps);outer=[]
 for i,p in enumerate(ps):
  q=ps[(i+1)%N];n=(p[0]/(a*a),p[1]/(b*b));m=(q[0]/(a*a),q[1]/(b*b));D=cross(n,m)
  outer.append(((m[1]-n[1])/D,(n[0]-m[0])/D))
 areas=[];aux=mp.mpf(0)
 for sign in [1,-1]:
  focus=(sign*mp.sqrt(a*a-b*b),mp.mpf(0));feet=[]
  for i,p in enumerate(ps):
   A=outer[(i-1)%N];B=outer[i];v=sub(B,A);n=(v[1],-v[0]);f=sub(focus,mul(mdot(sub(focus,A),n)/mdot(n,n),n));feet.append(f);aux=max(aux,abs(mdot(f,f)-a*a))
  areas.append(sum(cross(feet[i],feet[(i+1)%N]) for i in range(N))/2)
 return areas,aux
numeric=[]
for name,aa,bb,N,tau in [('moderate_primitive5_star','2','1',5,2),('near_circle_primitive5_star','1.0001','1',5,2),('thin_primitive7_star','5','1',7,3)]:
 aa=mp.mpf(aa);bb=mp.mpf(bb);low=mp.mpf(0);high=bb*bb;target=2*mp.pi*tau
 for _ in range(260):
  mid=(low+high)/2;angle=trace(aa,bb,mid,N)[3]
  if angle<target:low=mid
  else:high=mid
 lamnum=(low+high)/2;cases=[];products=[]
 for phase in [mp.mpf(0),mp.mpf('0.37'),mp.mpf('1.11')]:
  ps,end,start,angle=trace(aa,bb,lamnum,N,phase);areas,aux=numeric_areas(ps,aa,bb);prod=areas[0]*areas[1];products.append(prod)
  closure=mp.sqrt(mdot(sub(end,start),sub(end,start)));res=max(closure/(1+aa),abs(angle-target),aux/(1+aa*aa))
  cases.append({'eccentric_anomaly_start':mp.nstr(phase,6),'areas':[mp.nstr(x,60) for x in areas],'product':mp.nstr(prod,60),'relative_max_closure_angle_auxcircle_residual':mp.nstr(res,8)})
  if res>mp.mpf('1e-60'):fail.append(name+' numerical geometry residual')
 spread=max(abs(x-products[0]) for x in products)/(1+abs(products[0]))
 if spread>mp.mpf('1e-60'):fail.append(name+' numerical product spread')
 numeric.append({'name':name,'a':str(aa),'b':str(bb),'primitive_period':N,'winding':tau,'lambda':mp.nstr(lamnum,75),'positive_caustic_minor_square':mp.nstr(bb*bb-lamnum,20),'phases':cases,'relative_product_spread':mp.nstr(spread,8),'interval_certified':False})
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','source_only':True,'source_native_or_project_imports':0,'exact_cases':records,'new_exact_odd_common_product':scalar(BH[0]*BH[1]),'even_general_family_prediction':'4*a^2*b^2 versus (a^2+b^2)^2; gap (a^2-b^2)^2','numeric_method':'Cartesian caustic contact launch, straight chord quadratic intersection, Euclidean unit-normal reflection, actual tangent intersections and perpendicular projections; no Jacobi functions','mpmath_dps':mp.mp.dps,'numeric_selected_cases':numeric,'finite_evidence_not_universal_proof':True,'numeric_interval_certification':False,'failures':fail},indent=2))
raise SystemExit(1 if fail else 0)
