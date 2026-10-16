import sys,os,json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
sys.path.insert(0,os.environ['PR204_RUNTIME_PACKAGES'])
import sympy as s
import mpmath as mp
O=Path(__file__).resolve().parent
checks=[]
def require(t,label):
 if not bool(t):raise RuntimeError(label)
 checks.append(label)
def zero(x,label):require(s.simplify(x)==0,label)
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(v):return sum(det(p,v[(j+1)%len(v)]) for j,p in enumerate(v))/2
R=s.Rational
H=[(2,0),(R(4,3),s.sqrt(5)/3),(-R(4,3),s.sqrt(5)/3),(-2,0),(-R(4,3),-s.sqrt(5)/3),(R(4,3),-s.sqrt(5)/3)]
J=[(0,1),(-4*s.sqrt(2)/3,R(1,3)),(-4*s.sqrt(2)/3,-R(1,3)),(0,-1),(4*s.sqrt(2)/3,-R(1,3)),(4*s.sqrt(2)/3,R(1,3))]
H=[tuple(s.sympify(x) for x in p) for p in H]
J=[tuple(s.sympify(x) for x in p) for p in J]
rows=[]
for name,P,expect in [('H',H,(20*s.sqrt(5)/9,140*s.sqrt(5)/81,R(14000,729))),('J',J,(32*s.sqrt(2)/9,224*s.sqrt(2)/81,R(14336,729)))]:
 Q=[]
 require(len(set(P))==6,name+' six distinct vertices')
 for j,p in enumerate(P):
  q=P[(j+1)%6];before=P[(j-1)%6];d=sub(q,p);incoming=sub(p,before)
  zero(p[0]**2/4+p[1]**2-1,name+' outer '+str(j))
  aa=R(32,9);bb=R(5,9)
  Aq=d[0]**2/aa+d[1]**2/bb;Bq=2*(p[0]*d[0]/aa+p[1]*d[1]/bb);Cq=p[0]**2/aa+p[1]**2/bb-1
  zero(Bq**2-4*Aq*Cq,name+' caustic tangent '+str(j))
  t=s.simplify(-Bq/(2*Aq));require(0<t<1,name+' interior caustic contact '+str(j))
  v=tuple(s.simplify(x/s.sqrt(dot(incoming,incoming))) for x in incoming)
  out=tuple(s.simplify(x/s.sqrt(dot(d,d))) for x in d);n=(p[0]/4,p[1])
  for k in [0,1]:zero(out[k]-v[k]+2*dot(v,n)*n[k]/dot(n,n),name+' reflected unit direction '+str(j)+' '+str(k))
  foot_t=-dot(p,d)/dot(d,d);foot=tuple(s.simplify(p[k]+foot_t*d[k]) for k in [0,1]);Q.append(foot)
  zero(dot(foot,d),name+' complete-line perpendicular foot '+str(j))
 A=s.simplify(area(P));B=s.simplify(area(Q));AB=s.simplify(A*B)
 for v,e,lab in zip([A,B,AB],expect,['A','B','AB']):zero(v-e,name+' '+lab)
 zero(area(P+P)-2*A,name+' double traversal A');zero(area(Q+Q)-2*B,name+' double traversal B')
 rows.append({'orbit':name,'A':str(A),'B':str(B),'AB':str(AB),'twelve_entry_product':str(4*AB)})
zero(4*(R(14336,729)-R(14000,729))-R(448,243),'exact repeated12 product gap')
# Independent symbolic derivative from Jacobi ODE, not a package script.
x,c,d,k,al=s.symbols('x c d k al')
q=-al*k*c/(1+d)
qp=s.diff(q,c)*(-x*d)+s.diff(q,d)*(-k*k*x*c)
zero(s.factor((qp-al*k*x*(d+1-k*k)/(1+d)**2)*(1+d)**2).subs(c*c,1-x*x).subs(d*d,1-k*k*x*x),'explicit trace coefficient derivative')
# Exhaustive integer arithmetic proof diagnostics, finite evidence only.
from fractions import Fraction as F
integer_cases=0
for N in range(3,501):
 for t in range(1,(N+1)//2):
  if math.gcd(N,t)!=1 or 2*t>=N:continue
  m=N if N%2 else N//2;g=2*t if N%2 else t
  require(math.gcd(g,m)==1,'generator '+str((N,t)))
  h=F(N+2*t,2) if N%2 else F(m+t,2)
  require(h%1==(0 if N%4==2 else F(1,2)),'parity '+str((N,t)))
  integer_cases+=1
mp.mp.dps=85
num=[]
for mod in ['0.000001','0.63','0.9999']:
 k=mp.mpf(mod);par=k*k;kp=mp.sqrt(1-par);K=mp.ellipk(par);Kp=mp.ellipk(1-par)
 sn=lambda x:mp.ellipfun('sn',x,par)
 cn=lambda x:mp.ellipfun('cn',x,par)
 dn=lambda x:mp.ellipfun('dn',x,par)
 for N,t in [(3,1),(4,1),(5,2),(6,1),(7,3),(8,3),(9,4),(12,5)]:
  v=2*K*t/N;delta=2*v;m=N if N%2 else N//2;ell=2*K/m
  a=dn(v)/cn(v);b=kp/cn(v);CA=a*b*sn(v)*cn(v)/dn(v)
  CT=sn(delta)*(dn(delta)+kp*kp)/(1+dn(delta))**2
  P=lambda w:(-a*sn(w),b*cn(w))
  Q=lambda u:(-kp*kp*sn(u)/dn(u)**2,kp*cn(u)/dn(u)**2)
  S=lambda w:sum(dn(w+j*delta) for j in range(N))
  T=lambda u:area([Q(u+j*delta) for j in range(N)])
  errs=[];products=[]
  for w in [K/13,K/3,mp.mpf('1.17')*K]:
   pv=[P(w+j*delta) for j in range(N)];qv=[]
   for j,p in enumerate(pv):
    d=sub(pv[(j+1)%N],p);z=-dot(p,d)/dot(d,d);qv.append(tuple(p[h]+z*d[h] for h in [0,1]))
   A=area(pv);B=area(qv);products.append(A*B)
   errs.extend([abs(A-CA*S(w))/max(1,abs(A)),abs(B-CT*S(w+v+K))/max(1,abs(B))])
  z=K/mp.mpf('7.1')+mp.j*Kp/mp.mpf('3.3')
  errs.append(abs(S(z)*S(z+ell/2)-S(K/13)*S(K/13+ell/2))/max(1,abs(S(K/13)*S(K/13+ell/2))))
  eps=mp.mpf('1e-14');r=K+mp.j*Kp
  # Finite pole test challenges sign, multiplicity, and cancellation; it is not a proof.
  residue=eps*T(r+eps);expected=-mp.j*(N/m)*CT
  poleerr=abs(residue-expected)/max(1,abs(expected))
  require(mp.isfinite(poleerr) and poleerr<mp.mpf('1e-10'),'numeric simple-pole coefficient '+str((mod,N,t)))
  require(all(mp.isfinite(e) and e<mp.mpf('1e-55') for e in errs),'numeric trace identity '+str((mod,N,t)))
  spread=(max(products)-min(products))/max(1,abs(products[0]))
  if N%4!=2:require(spread<mp.mpf('1e-55'),'target constancy diagnostic '+str((mod,N,t)))
  num.append({'k':mod,'N':N,'winding':t,'max_identity_residual':mp.nstr(max(errs),15),'pole_residue_error':mp.nstr(poleerr,15),'phase_spread':mp.nstr(spread,15)})
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_six_orbits':rows,'integer_diagnostic_cases':integer_cases,'checks_total':len(checks),'numeric_configurations':num,'runtime':{'sympy':s.__version__,'mpmath':mp.__version__,'bytecode_disabled':sys.dont_write_bytecode},'limits':'Finite exact controls and noninterval numerical diagnostics, separate from analytic proof; no universal proof or priority certificate.'}
(O/'INDEPENDENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
