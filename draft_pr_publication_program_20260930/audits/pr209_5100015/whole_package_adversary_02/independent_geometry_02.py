"""Owned finite diagnostics; direct Cartesian geometry independent of inherited scripts.
Run with Python 3.11 -E -S -B -P; no network, inherited execution or source writes.
"""
from pathlib import Path
import sys,json,math,datetime,hashlib
sys.path.insert(0,'/Users/alec/Library/Python/3.11/lib/python/site-packages')
import mpmath as mp
mp.mp.dps=70
M=mp.mpf
checks=0
maxerr=M(0)
def eq(x,y,tag,tol=M('1e-52')):
 global checks,maxerr
 err=abs(x-y)/max(M(1),abs(x),abs(y));maxerr=max(maxerr,err);checks+=1
 if err>tol:raise AssertionError((tag,mp.nstr(err,10)))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def scale(c,x):return tuple(c*a for a in x)
def unit(x):return scale(1/mp.sqrt(dot(x,x)),x)
def area(ps):return sum(det(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
def solve(n,m):
 d=det(n,m)
 return ((m[1]-n[1])/d,(n[0]-m[0])/d)
def physical(ps,a,b,alpha,beta,tag):
 ns=[(p[0]/a**2,p[1]/b**2) for p in ps]
 rs=[solve(ns[j],ns[(j+1)%len(ps)]) for j in range(len(ps))]
 qs=[scale(1/dot(n,n),n) for n in ns]
 for j,p in enumerate(ps):
  eq((p[0]/a)**2+(p[1]/b)**2,1,tag+'boundary')
  incoming=unit(sub(p,ps[j-1]));outgoing=unit(sub(ps[(j+1)%len(ps)],p));n=unit(ns[j])
  reflection=sub(incoming,scale(2*dot(incoming,n),n))
  for x,y in zip(outgoing,reflection):eq(x,y,tag+'reflection')
  e=sub(ps[(j+1)%len(ps)],p);h=(-e[1],e[0]);c=dot(h,p)
  eq(c*c,alpha**2*h[0]**2+beta**2*h[1]**2,tag+'caustic')
  eq(dot(ns[j],qs[j]),1,tag+'foot-on-line')
  eq(det(ns[j],qs[j]),0,tag+'foot-normal')
  eq(dot(ns[j],rs[j]),1,tag+'outer-on-line')
  eq(dot(ns[(j+1)%len(ps)],rs[j]),1,tag+'outer-on-next')
 return area(rs),area(qs),ps,rs,qs
cases=[]
for kstring in ['0.02','0.4','0.91','0.999']:
 k=M(kstring);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m)
 sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m);dn=lambda z:mp.ellipfun('dn',z,m)
 f=lambda z:sn(z)*cn(z)/dn(z)
 for N in [3,5,6,7,9,10,11,14]:
  for tau in range(1,(N+1)//2):
   if math.gcd(tau,N)>1:continue
   v=2*tau*K/N;a=dn(v)/cn(v);b=kp/cn(v);q=N//math.gcd(N,2);r=N//q
   C=mp.fprod((cn(2*K*j/q)/sn(2*K*j/q))**2 for j in range(1,(q+1)//2))
   expected=a*a*b**4*f(v)*(2*f(v)-f(2*v))/(4*kp*cn(K-v)**2)*r*r*kp**q/(C*C)
   products=[]
   for frac in ['0.013','0.277','0.731']:
    u=M(frac)*K;ps=[(-a*sn(u+2*j*v),b*cn(u+2*j*v)) for j in range(N)]
    A,B,ps,rs,qs=physical(ps,a,b,M(1),kp,f'{kstring}/{N}/{tau}/')
    eq(A*B,expected,'product-formula');products.append(A*B)
    T=lambda z:sum(dn(z+2*j*v) for j in range(N))
    eq(A,a*a*b*b/kp*f(v)*T(u+v),'outer-formula')
    eq(B,b*b/(4*cn(K-v)**2)*(2*f(v)-f(2*v))*T(u+K-v),'pedal-formula')
    w=K-v
    for j,Q in enumerate(qs):
     z=u+2*j*v
     edge=(a*(-sn(z+K-v)+sn(z+K+v)),b*(cn(z+K-v)-cn(z+K+v)))
     eq(Q[0],b/a/(2*cn(w))*edge[0],'foot-edge-x')
     eq(Q[1],edge[1]/(2*cn(w)),'foot-edge-y')
    eq(area(list(reversed(rs))),-A,'reverse-outer');eq(area(list(reversed(qs))),-B,'reverse-feet')
    if N==3:
     for d in [2,3,5]:eq(area(rs*d)*area(qs*d),d*d*A*B,'repeat')
     eq(area([scale(3,x) for x in rs])*area([scale(3,x) for x in qs]),81*A*B,'scale-fourth')
   for p in products[1:]:eq(p,products[0],'phase-constancy')
   cases.append({'k':kstring,'N':N,'tau':tau,'phases':3,'product':mp.nstr(products[0],20)})
# Independent complex global identity diagnostics, including close approaches to poles.
complex_tests=0
for k in [M('.2'),M('.8'),M('.999')]:
 m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);Ki=mp.ellipk(1-m)
 dn=lambda z:mp.ellipfun('dn',z,m);sn=lambda z:mp.ellipfun('sn',z,m);cn=lambda z:mp.ellipfun('cn',z,m)
 for q in [1,3,5,7,11,17]:
  C=mp.fprod((cn(2*K*j/q)/sn(2*K*j/q))**2 for j in range(1,(q+1)//2))
  for z in [K*M('.13')+1j*Ki*M('.37'),K*M('.61')-1j*Ki*M('.23'),1j*Ki+M('1e-10')]:
   U=lambda t:sum(dn(t+2*K*j/q) for j in range(q))
   V=mp.fprod(dn(z+2*K*j/q) for j in range(q))
   eq(V,C*U(z),'complex-product-sum',M('1e-46'))
   eq(U(z)*U(z+K),kp**q/C**2,'complex-trace',M('1e-46'));complex_tests+=1
# Exact rational+radical period-four check with independently reconstructed Cartesian maps.
import sympy as sp
checks_exact=0
def exacteq(x,y):
 global checks_exact
 assert sp.simplify(x-y)==0,(x,y)
 checks_exact+=1
def exactarea(ps):return sum(det(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
for ps,A0,B0 in [([(sp.Integer(2),0),(0,sp.Integer(1)),(-sp.Integer(2),0),(0,-sp.Integer(1))],8,4), ([(4/sp.sqrt(5),1/sp.sqrt(5)),(-4/sp.sqrt(5),1/sp.sqrt(5)),(-4/sp.sqrt(5),-1/sp.sqrt(5)),(4/sp.sqrt(5),-1/sp.sqrt(5))],10,5)]:
 ps=[tuple(map(sp.sympify,p)) for p in ps]
 ns=[(p[0]/4,p[1]) for p in ps];rs=[solve(ns[j],ns[(j+1)%4]) for j in range(4)];qs=[scale(1/dot(n,n),n) for n in ns]
 exacteq(exactarea(rs),A0);exacteq(exactarea(qs),B0)
 for j,p in enumerate(ps):
  exacteq(p[0]**2/4+p[1]**2,1)
  e=sub(ps[(j+1)%4],p);h=(-e[1],e[0]);c=dot(h,p)
  exacteq(c*c,sp.Rational(16,5)*h[0]**2+sp.Rational(1,5)*h[1]**2)
  ei=sub(p,ps[j-1]);eo=e;ei=scale(1/sp.sqrt(dot(ei,ei)),ei);eo=scale(1/sp.sqrt(dot(eo,eo)),eo);n=ns[j]
  er=sub(ei,scale(2*dot(ei,n)/dot(n,n),n))
  for x,y in zip(er,eo):exacteq(x,y)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','owned_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'mpmath':mp.__version__,'sympy':sp.__version__,'precision_decimal':70,'numerical_assertions':checks,'exact_assertions':checks_exact,'primitive_families':len(cases),'complex_trace_tests':complex_tests,'maximum_scaled_error':mp.nstr(maxerr,10),'families':cases,'limits':'Finite non-interval diagnostics support but do not prove the universal theorem. No inherited scientific program executed.'}
Path('OWNED_GEOMETRY_RESULTS_02.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='families'},indent=2))
