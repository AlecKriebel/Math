import sys,json,math
import sympy as S
import mpmath as mp
from datetime import datetime,timezone

# All computations are independent; no candidate checker or inherited review is imported.
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def exact_foot(p,q,f):
 d=q-p;t=S.simplify((f-p).dot(d)/d.dot(d));return S.simplify(p+t*d)
def exact_area(q):return S.simplify(sum(det(q[i],q[(i+1)%len(q)]) for i in range(len(q)))/2)
def exact_outer(P,a2,b2):
 O=[]
 for i in range(len(P)):
  u=P[i];v=P[(i+1)%len(P)]
  O.append(S.simplify(S.Matrix([[u[0]/a2,u[1]/b2],[v[0]/a2,v[1]/b2]]).inv()*S.ones(2,1)))
 return O

t=S.symbols('t',positive=True)
r=t*(2-t)/(1-t*t)
# Independent isosceles reflection-equation derivation: squared lengths agree.
reflection_residual=S.factor(r*(1+t)**2+(1-t*t)-(1-t*t)*(r*(1+t)/t-1)**2)
assert reflection_residual==0
exact=[]
for a2,b2,tt in [(S.Integer(8),S.Integer(5),S.Rational(2,3)),(S.Integer(21),S.Integer(16),S.Rational(3,5))]:
 a=S.sqrt(a2);b=S.sqrt(b2);c=S.sqrt(a2-b2)
 assert S.simplify(a2/b2-r.subs(t,tt))==0
 P=[S.Matrix([a,0]),S.Matrix([-a*tt,b*S.sqrt(1-tt*tt)]),S.Matrix([-a*tt,-b*S.sqrt(1-tt*tt)])]
 alpha2=a2*tt**2;beta2=alpha2-c*c
 assert alpha2>0 and beta2>0
 O=exact_outer(P,a2,b2)
 for i in range(3):
  prev=P[(i-1)%3];x=P[i];nxt=P[(i+1)%3]
  incoming=(x-prev)/S.sqrt((x-prev).dot(x-prev));outgoing=(nxt-x)/S.sqrt((nxt-x).dot(nxt-x))
  normal=S.Matrix([x[0]/a2,x[1]/b2])
  assert S.simplify(det(incoming-outgoing,normal))==0
  d=nxt-x;normal_line=S.Matrix([d[1],-d[0]]);h=normal_line.dot(x)
  assert S.simplify(alpha2*normal_line[0]**2+beta2*normal_line[1]**2-h*h)==0
 for reverse in [False,True]:
  for repeat in [1,2,3]:
   pp=(P if not reverse else list(reversed(P)))*repeat
   oo=(O if not reverse else list(reversed(O)))*repeat
   vals=[]
   for poly in [pp,oo]:
    for sign in [1,-1]:
     f=S.Matrix([sign*c,0]);vals.append(exact_area([exact_foot(poly[i],poly[(i+1)%len(poly)],f) for i in range(len(poly))]))
   assert S.simplify(vals[0]*vals[3]-vals[1]*vals[2])==0
   assert S.simplify(vals[2]/vals[0]-vals[3]/vals[1])==0
   exact.append({'a2':str(a2),'b2':str(b2),'t':str(tt),'reverse':reverse,'repeat':repeat,'areas':list(map(str,vals)),'C':str(S.simplify(vals[2]/vals[0])),'ratio':str(S.simplify(vals[0]/vals[1]))})

mp.mp.dps=100
sn=lambda u,k:mp.ellipfun('sn',u,k*k)
cn=lambda u,k:mp.ellipfun('cn',u,k*k)
dn=lambda u,k:mp.ellipfun('dn',u,k*k)
def foot(p,q,f):
 d=(q[0]-p[0],q[1]-p[1]);den=d[0]**2+d[1]**2
 t=((f[0]-p[0])*d[0]+(f[1]-p[1])*d[1])/den
 return(p[0]+t*d[0],p[1]+t*d[1])
def area(q):return mp.fsum(det(q[i],q[(i+1)%len(q)]) for i in range(len(q)))/2
def outer(P,a,b):
 O=[]
 for i in range(len(P)):
  u=(P[i][0]/a**2,P[i][1]/b**2);v=(P[(i+1)%len(P)][0]/a**2,P[(i+1)%len(P)][1]/b**2)
  dd=det(u,v);O.append(((v[1]-u[1])/dd,(u[0]-v[0])/dd))
 return O

def case(N,tau,k):
 K=mp.ellipk(k*k);Kp=mp.ellipk(1-k*k);v=2*K*tau/N;delta=2*v;kp=mp.sqrt(1-k*k)
 a=dn(v,k)/cn(v,k);b=kp/cn(v,k);L=4*K/N
 def q(u):
  ss=sn(u,k);cc=cn(u,k)
  return((k-ss)/(1-k*ss),kp*cc/(1-k*ss))
 def Q(u):
  ss=sn(u,k);cc=cn(u,k)
  return(a*(k-a*ss)/(a-k*ss),a*b*cc/(a-k*ss))
 def traces(w):
  return(area([q(w+v+i*delta) for i in range(N)]),area([Q(w+i*delta) for i in range(N)]))
 real_errors=[];positives=[];Cs=[]
 for phase in [mp.mpf('.173'),mp.mpf('.681'),mp.mpf('1.192')]:
  w=phase*K
  P=[(-a*sn(w+i*delta,k),b*cn(w+i*delta,k)) for i in range(N)]
  O=outer(P,a,b)
  geom=[]
  for poly in [P,O]:
   for sign in [1,-1]:
    f=(sign*k,mp.mpf(0));geom.append(area([foot(poly[i],poly[(i+1)%N],f) for i in range(N)]))
  AA,BB=traces(w);Am,Bm=traces(w+2*K)
  real_errors.extend([abs(AA-geom[0]),abs(Am-geom[1]),abs(BB-geom[2]),abs(Bm-geom[3])])
  real_errors.append(abs(geom[0]*geom[3]-geom[1]*geom[2])/max(1,abs(geom[0]*geom[3])))
  assert min(geom)>0;positives.extend(geom);Cs.append(BB/AA)
 C=Cs[0]
 assert max(abs(cc-C) for cc in Cs)<mp.mpf('1e-75')*max(1,abs(C))
 w=mp.mpc('.213','.317')*K
 AA,BB=traces(w);AL,BL=traces(w+L);Ai,Bi=traces(w+2j*Kp)
 errors={'geometry_and_target':max(real_errors),'periodL':max(abs(AL-AA),abs(BL-BB)),'anti2iKp':max(abs(Ai+AA),abs(Bi+BB)),'complex_proportion':abs(BB-C*AA)}
 assert max(errors.values())<mp.mpf('1e-65')*max(1,abs(AA),abs(BB))
 residue=[];rr=K+1j*Kp;pole=rr-v
 for es in ['1e-8','1e-12','1e-16']:
  eps=mp.mpf(es)
  qq=q(rr+eps);germ=max(abs(eps**2*qq[0]-2/k),abs(eps**2*qq[1]-2j/k))
  R=a/(k*sn(v,k));qp=Q(rr+v+eps);qm=Q(rr-v+eps)
  rg=max(abs(eps*qp[0]-R),abs(eps*qp[1]-1j*R),abs(eps*qm[0]+R),abs(eps*qm[1]+1j*R))
  ap,bp=traces(pole+eps);an,bn=traces(pole-eps)
  ra=eps*(ap-an)/2;rb=eps*(bp-bn)/2
  residue.append({'eps':es,'q_germ_error':mp.nstr(germ,8),'outer_residue_error':mp.nstr(rg,8),'trace_residue_A':mp.nstr(ra,30),'trace_residue_B':mp.nstr(rb,30),'residue_proportion_error':mp.nstr(abs(rb-C*ra),8),'z2_trace_norm':mp.nstr(eps**2*max(abs(ap),abs(bp)),8)})
 assert mp.mpf(residue[-1]['q_germ_error'])<mp.mpf('1e-26')
 assert mp.mpf(residue[-1]['outer_residue_error'])<mp.mpf('1e-9')*max(1,abs(R))
 assert abs(ra)>0 and abs(rb)>0
 return{'N':N,'tau':tau,'k':str(k),'C':mp.nstr(C,35),'minimum_real_area':mp.nstr(min(positives),15),'errors':{z:mp.nstr(e,8) for z,e in errors.items()},'residues':residue}

cases=[]
for N,tau in [(3,1),(4,1),(5,1),(5,2),(6,1),(7,2),(7,3),(8,3),(9,4),(10,3),(11,5)]:
 for kval in ['.05','.6','.95']:
  cases.append(case(N,tau,mp.mpf(kval)))
# Extreme eccentricity approaching an excluded degenerate-caustic boundary.
cases.append(case(5,2,mp.mpf('.9999')))
output={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'sympy_version':S.__version__,'mpmath_version':mp.__version__,'dps':mp.mp.dps,'interpretation':'Exact controls are algebraic certificates; mpmath outputs are non-interval diagnostics only.','isosceles_reflection_identity':str(reflection_residual),'exact':exact,'numeric':cases}
print(json.dumps(output,indent=2))
