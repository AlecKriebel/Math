"""Independently authored geometric/elliptic falsification controls, no archived checker imports."""
from pathlib import Path
from datetime import datetime,timezone
from math import gcd
import hashlib,json,sys
import mpmath as m
import sympy as s
H=Path(__file__).parent
m.mp.dps=110

def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def crosslines(n,t):
 d=det(n,t);return((t[1]-n[1])/d,(n[0]-t[0])/d)
def foot(f,x,y):
 d=sub(y,x);rho=dot(sub(f,x),d)/dot(d,d);return(x[0]+rho*d[0],x[1]+rho*d[1])
def area(v):return sum(det(v[j],v[(j+1)%len(v)]) for j in range(len(v)))/2
def txt(v):return m.nstr(v,32)

def exact():
 a=s.Integer(2);b=s.Integer(1);c=s.sqrt(3);S=s.simplify
 phases=[[(2,0),(0,1),(-2,0),(0,-1)],[(4/s.sqrt(5),1/s.sqrt(5)),(-4/s.sqrt(5),1/s.sqrt(5)),(-4/s.sqrt(5),-1/s.sqrt(5)),(4/s.sqrt(5),-1/s.sqrt(5))]]
 rows=[]
 for pts in phases:
  pts=[tuple(map(s.sympify,p)) for p in pts]
  normals=[(x/4,y) for x,y in pts];outer=[crosslines(normals[j],normals[(j+1)%4]) for j in range(4)]
  ar=[]
  for e in [1,-1]:
   qs=[foot((e*c,0),outer[(j-1)%4],outer[j]) for j in range(4)];ar.append(S(area(qs)))
  for j in range(4):
   p=pts[j];q=pts[(j+1)%4];assert S(p[0]**2/4+p[1]**2-1)==0;n=(q[1]-p[1],p[0]-q[0]);z=dot(n,p)
   assert S(z*z-(4-s.Rational(4,5))*n[0]**2-(1-s.Rational(4,5))*n[1]**2)==0
  for j in range(4):
   p=pts[j];q=pts[(j+1)%4];prev=pts[(j-1)%4];ni=(p[0]/4,p[1]);inc=sub(p,prev);out=sub(q,p)
   inc=tuple(S(x/s.sqrt(dot(inc,inc))) for x in inc);out=tuple(S(x/s.sqrt(dot(out,out))) for x in out)
   assert S(det(sub(inc,out),ni))==0
  rows.append({'all_exact_reflection_and_common_caustic_checks_zero':True,'areas':[str(v) for v in ar],'product':str(S(ar[0]*ar[1]))})
 assert rows[0]['product']!=rows[1]['product']
 # A different nonconfocal homothetic Poncelet triangle: linear image of regular triangles.
 def nc(theta):
  pts=[(s.Integer(3)*s.cos(theta+2*j*s.pi/3),s.sin(theta+2*j*s.pi/3)) for j in range(3)]
  normals=[(x/9,y) for x,y in pts];vs=[crosslines(normals[j],normals[(j+1)%3]) for j in range(3)]
  Bs=[S(area([foot((e*s.sqrt(8),0),vs[(j-1)%3],vs[j]) for j in range(3)])) for e in [1,-1]]
  return str(S(Bs[0]*Bs[1]))
 ncprod=[nc(0),nc(s.pi/6)];assert ncprod[0]!=ncprod[1]
 circle=[(s.Integer(2),s.Integer(0)),(-s.Integer(1),s.sqrt(3)),(-s.Integer(1),-s.sqrt(3))]
 assert S(area(circle)**2)==27
 printed=(2/s.sqrt(5),2/s.sqrt(5));qprinted=(-2/s.sqrt(5),2/s.sqrt(5));nn=(qprinted[1]-printed[1],printed[0]-qprinted[0]);hh=dot(nn,printed)
 bad=S(hh*hh-s.Rational(16,5)*nn[0]**2-s.Rational(1,5)*nn[1]**2)
 assert bad!=0
 return {'0062_printed_wrong_rectangle_tangency_residual':str(bad),'even_four_period_common_caustic_negative_control':rows,'nonconfocal_homothetic_triangle_products':ncprod,'circle_radius_two_triangle_foot_product':'27'}

rows=[]
for ks,n,tau in [('0.000003',3,1),('0.31',7,3),('0.81',11,2),('0.985',17,8),('0.9999999',5,2),('0.71',51,25),('0.61',8,3)]:
 assert gcd(n,tau)==1
 k=m.mpf(ks);K=m.ellipk(k*k);Kp=m.ellipk(1-k*k);v=2*K*tau/n;delta=2*v;L=4*K/n
 sn=lambda z:m.ellipfun('sn',z,k*k)
 cn=lambda z:m.ellipfun('cn',z,k*k)
 dn=lambda z:m.ellipfun('dn',z,k*k)
 a=dn(v)/cn(v);b=m.sqrt(1-k*k)/cn(v);c=k;beta2=1-k*k;lam=b*b-beta2
 rb=a;db=-c*lam/beta2;Rb=b*b/beta2;tM=m.sqrt((Rb+abs(db))**2-rb*rb)
 mb=4*k/(1+k)**2;Kb=m.ellipk(mb);Kbp=m.ellipk(1-mb);qb=m.exp(-m.pi*Kbp/Kb)
 qn=qb**n;mn=(m.jtheta(2,0,qn)/m.jtheta(3,0,qn))**4;Kn=m.pi*m.jtheta(3,0,qn)**2/2;scale=n*Kn/Kb
 errs={x:m.mpf(0) for x in ['common_caustic','reflection','outer_sides','bicentric_circle','positive_tangent_length_dn','contact_area_ratio','dn_sum_area','KS_dn_sum','inverse_opposite_ratio_variation','imaginary_character','quarter_shift','simple_pole_scaling','forced_zero']}
 products=[];ratios=[]
 for phi in ['.093','.281','.637','1.019']:
  w=m.mpf(phi)*K;ps=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(n)]
  normals=[(x/(a*a),y/(b*b)) for x,y in ps]
  vs=[crosslines(normals[j],normals[(j+1)%n]) for j in range(n)]
  feet=[[foot((e*c,m.mpf(0)),vs[(j-1)%n],vs[j]) for j in range(n)] for e in [1,-1]]
  B=[area(qs) for qs in feet];products.append(B[0]*B[1]/a**4)
  inverses=[]
  for e in [1,-1]:
   vec=[sub(p,(e*c,m.mpf(0))) for p in ps];inverses.append(area([(x/dot(t,t),y/dot(t,t)) for t in vec for x,y in [t]]))
  ratios.append(B[0]/inverses[1])
  R=[(a*a*(x+c)/(a*a+c*x),a*a*y/(a*a+c*x)) for x,y in vs]
  AR=area(R)
  errs['contact_area_ratio']=max(errs['contact_area_ratio'],abs(B[0]/AR-rb*rb/(Rb*Rb-db*db)))
  u=(1+k)*(w+v-K)/2
  dns=[m.ellipfun('dn',u+2*j*Kb*tau/n,mb) for j in range(n)]
  errs['dn_sum_area']=max(errs['dn_sum_area'],abs(B[0]-rb**3*tM/(Rb*Rb-db*db)*sum(dns))/a**2)
  errs['KS_dn_sum']=max(errs['KS_dn_sum'],abs(sum(dns)-scale*m.ellipfun('dn',scale*u,mn))/n)
  for j in range(n):
   p=ps[j];q=ps[(j+1)%n];nn=(q[1]-p[1],p[0]-q[0]);h=dot(nn,p)
   errs['common_caustic']=max(errs['common_caustic'],abs(h*h-nn[0]**2-beta2*nn[1]**2)/max(1,dot(nn,nn)))
   inc=sub(p,ps[(j-1)%n]);out=sub(q,p);inc=tuple(x/m.sqrt(dot(inc,inc)) for x in inc);out=tuple(x/m.sqrt(dot(out,out)) for x in out)
   errs['reflection']=max(errs['reflection'],abs(det(sub(inc,out),normals[j]))/m.sqrt(dot(normals[j],normals[j])))
   errs['outer_sides']=max(errs['outer_sides'],abs(dot(normals[j],vs[(j-1)%n])-1),abs(dot(normals[j],vs[j])-1))
   errs['bicentric_circle']=max(errs['bicentric_circle'],abs((R[j][0]-db)**2+R[j][1]**2-Rb*Rb)/(Rb*Rb))
   actual=m.sqrt(dot(R[j],R[j])-rb*rb);errs['positive_tangent_length_dn']=max(errs['positive_tangent_length_dn'],abs(actual-tM*dns[j])/a)
   assert det(feet[0][j],feet[0][(j+1)%n])>0
 def Q(z):
  return(a*(c-a*sn(z))/(a-c*sn(z)),a*b*cn(z)/(a-c*sn(z)))
 def T(z):return area([Q(z+j*delta) for j in range(n)])
 z=m.mpf('.17')*K+m.j*m.mpf('.13')*Kp;q=Q(z);qq=Q(z+2*m.j*Kp)
 errs['imaginary_character']=max(abs(qq[0]-q[0]),abs(qq[1]+q[1]))/a
 r=K+m.j*Kp
 errs['quarter_shift']=max(abs(sn(r+z)-dn(z)/(k*cn(z))),abs(cn(r+z)+m.j*m.sqrt(1-k*k)/(k*cn(z))),abs(dn(r+z)-m.j*m.sqrt(1-k*k)*sn(z)/cn(z)))
 zero=T(K-v+m.j*Kp+L/2)/a**2;errs['forced_zero']=abs(zero)
 eps=m.mpf('1e-27')*(1+m.j);errs['simple_pole_scaling']=abs(eps**2*T(r-v+eps))/a**2
 errs['inverse_opposite_ratio_variation']=max(abs(x-ratios[0])/abs(ratios[0]) for x in ratios)
 spread=max(abs(x-products[0]) for x in products)
 assert all(x<m.mpf('1e-70') for key,x in errs.items() if key!='simple_pole_scaling'),(ks,n,tau,errs)
 assert errs['simple_pole_scaling']<m.mpf('1e-20')
 if n%2:assert spread<m.mpf('1e-70')
 else:assert spread>m.mpf('1e-10')
 rows.append({'k':ks,'N':n,'tau':tau,'phase_count':4,'normalized_product_samples':list(map(txt,products)),'normalized_product_spread':txt(spread),'errors':{key:txt(x) for key,x in errs.items()}})
 print('PASS',ks,n,tau,flush=True)
result={'utc':datetime.now(timezone.utc).isoformat(),'completion_percent':65,'python':sys.version,'sympy':s.__version__,'mpmath':m.__version__,'precision_digits':m.mp.dps,'interval_certification':False,'archived_scientific_code_imported':False,'exact':exact(),'families':rows,'all_pass':True}
(H/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_pass':True,'families':len(rows),'phases':sum(r['phase_count'] for r in rows),'exact':result['exact']},indent=2))
