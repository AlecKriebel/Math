"""Third whole-review controls, independent of archived scientific implementations.
Finite exact checks and uncertified high-precision diagnostics only.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,math,sys
import sympy as s
import mpmath as m
O=Path(__file__).resolve().parent
m.mp.dps=115
D=lambda x,y:x[0]*y[1]-x[1]*y[0]
A=lambda qs:sum(D(qs[j],qs[(j+1)%len(qs)]) for j in range(len(qs)))/2
sub=lambda x,y:(x[0]-y[0],x[1]-y[1])
dot=lambda x,y:x[0]*y[0]+x[1]*y[1]
unit=lambda x:tuple(z/m.sqrt(dot(x,x)) for z in x)
err=lambda x,y=0,scale=1:abs(x-y)/max(m.mpf(scale),abs(x),abs(y))
num=lambda x:m.nstr(x,35)

def exact_fixture():
 a=s.sqrt(10);b=s.Integer(2);c=s.sqrt(6);lam=s.Rational(20,7);aa=a*a-lam;bb=b*b-lam
 phases={'axis_diamond':[(a,0),(0,b),(-a,0),(0,-b)],'correct_rectangle':[(10/s.sqrt(14),4/s.sqrt(14)),(-10/s.sqrt(14),4/s.sqrt(14)),(-10/s.sqrt(14),-4/s.sqrt(14)),(10/s.sqrt(14),-4/s.sqrt(14))]}
 out={};count=0
 def zero(x):
  nonlocal count
  z=s.simplify(x);assert z==0,z;count+=1
 for name,ps in phases.items():
  ns=[(x/(a*a),y/(b*b)) for x,y in ps];vs=[]
  for j,p in enumerate(ps):
   zero(p[0]**2/a**2+p[1]**2/b**2-1)
   vin=sub(p,ps[j-1]);vout=sub(ps[(j+1)%4],p)
   vi=tuple(x/s.sqrt(dot(vin,vin)) for x in vin);vo=tuple(x/s.sqrt(dot(vout,vout)) for x in vout)
   for h in range(2):zero(vo[h]-vi[h]+2*dot(vi,ns[j])*ns[j][h]/dot(ns[j],ns[j]))
   n=(vout[1],-vout[0]);zero(aa*n[0]**2+bb*n[1]**2-dot(n,p)**2)
   n0=ns[j];n1=ns[(j+1)%4];dd=D(n0,n1)
   vs.append(((n1[1]-n0[1])/dd,(n0[0]-n1[0])/dd))
  areas=[];inverse=[]
  for e in [1,-1]:
   fs=[];iv=[]
   for j,p in enumerate(ps):
    n=ns[j];q=(e*c+(1-e*c*n[0])*n[0]/dot(n,n),(1-e*c*n[0])*n[1]/dot(n,n));q=tuple(s.simplify(x) for x in q);fs.append(q)
    edge=sub(vs[j],vs[j-1]);zero(dot(sub((e*c,0),q),edge));zero(dot(n,q)-1)
    zero(dot(q,q)-a*a)
    v=sub(p,(e*c,0));iv.append(tuple(x/dot(v,v) for x in v))
   areas.append(s.simplify(A(fs)));inverse.append(s.simplify(A(iv)))
  out[name]={'outer_areas':[str(x) for x in areas],'outer_product':str(s.simplify(areas[0]*areas[1])),'inverse_areas':[str(x) for x in inverse]}
 assert [out[z]['outer_product'] for z in phases]==['160','196']
 # A genuinely noncollinear adjacent residue mutant must create a double pole.
 r1,r2,t=s.symbols('r1 r2 t',nonzero=True)
 R=(r1,s.I*r1);S=(-r1,-s.I*r1);mut=(-r1,s.I*r1)
 assert s.simplify(D(R,S))==0 and s.simplify(D(R,mut))==2*s.I*r1*r1
 return {'ellipse_axes_squared':['10','4'],'lambda':'20/7','zero_residuals':count,'phases':out,'noncollinear_residue_mutant_double_coefficient':str(s.simplify(D(R,mut)))}

def lattice():
 cases=0;phases=0;cut=0
 ns=list(range(3,44))+[101,127,221]
 for n in ns:
  ts=range(1,(n+1)//2) if n<44 else [t for t in [1,2,3,(n-1)//2] if math.gcd(t,n)==1]
  for tau in ts:
   if math.gcd(tau,n)!=1:continue
   assert m.mpf(tau)/n<m.mpf('.5')
   for base in range(n):
    hits=[]
    for j in range(n):
     val=(4*tau*(j-base))%(4*n)
     if val==0:hits.append((j,'minus'))
     if val==(4*tau)%(4*n):hits.append((j,'plus'))
    assert sorted(hits)==sorted([(base,'minus'),((base+1)%n,'plus')])
    phases+=1
   inv=pow(tau,-1,n);assert inv*tau-((inv*tau-1)//n)*n==1
   assert (2*n)%(4)==(2 if n%2 else 0)
   cases+=1;cut+=1
 return {'N_small_range':[3,43],'additional_large_N':[101,127,221],'primitive_pairs':cases,'phase_cases':phases,'cyclic_cut_cases':cut,'all_passed':True}

class Family:
 def __init__(self,n,tau,k):
  self.n=n;self.tau=tau;self.k=m.mpf(k);self.mm=self.k**2;self.beta=m.sqrt(1-self.mm);self.K=m.ellipk(self.mm);self.Kp=m.ellipk(1-self.mm);self.v=2*self.K*tau/n;self.h=2*self.v;self.L=4*self.K/n;self.p=m.j*self.Kp;self.r=self.K+self.p;self.b0=self.K-self.v
  self.a=self.j('dn',self.v)/self.j('cn',self.v);self.b=self.beta/self.j('cn',self.v);self.c=self.k;self.lam=self.b**2-self.beta**2
 def j(self,name,w):return m.ellipfun(name,w,self.mm)
 def P(self,w):return (-self.a*self.j('sn',w),self.b*self.j('cn',w))
 def Q(self,w):
  sn=self.j('sn',w);cn=self.j('cn',w);den=self.a-self.c*sn
  return (self.a*(self.c-self.a*sn)/den,self.a*self.b*cn/den)
 def trace(self,w):return A([self.Q(w+j*self.h) for j in range(self.n)])
 def inverse(self,w,e):
  out=[]
  for j in range(self.n):
   v=sub(self.P(w+j*self.h),(e*self.c,0));out.append(tuple(x/dot(v,v) for x in v))
  return A(out)
 def projectivity(self,q):
  den=self.a*self.a+self.c*q[0]
  return (self.a*self.a*(q[0]+self.c)/den,self.a*self.a*q[1]/den)

def numeric():
 specs=[(3,1,'.4319'),(11,5,'.91437'),(21,8,'.006731'),(35,17,'.99631'),(103,51,'.99999991'),(9,2,'.00000000000000317'),(12,5,'.71391')]
 rows=[]
 for n,tau,k in specs:
  f=Family(n,tau,k);maxima={};products=[];ratios=[]
  def add(label,x,y=0,scale=1):maxima[label]=max(maxima.get(label,m.mpf(0)),err(x,y,scale))
  mb=4*f.k/(1+f.k)**2;Kb=(1+f.k)*f.K;db=-f.c*f.lam/f.beta**2;Rb=f.b*f.b/f.beta**2;r=f.a;tm=m.sqrt((Rb+abs(db))**2-r*r)
  qb=m.exp(-m.pi*f.Kp/(2*f.K));qn=qb**n;theta=m.jtheta(3,0,qn);mn=(m.jtheta(2,0,qn)/theta)**4;Kn=m.pi*theta**2/2;scale=n*Kn/Kb
  add('theta_nome_complete_integral',Kn,m.ellipk(mn))
  for phase in ['.0379','.2713','.8471']:
   w=m.mpf(phase)*f.K;ps=[f.P(w+j*f.h) for j in range(n)];ns=[(p[0]/f.a**2,p[1]/f.b**2) for p in ps];vs=[]
   for j,p in enumerate(ps):
    add('boundary',p[0]**2/f.a**2+p[1]**2/f.b**2,1)
    vi=unit(sub(p,ps[j-1]));vo=unit(sub(ps[(j+1)%n],p));nn=ns[j]
    for h in [0,1]:add('unit_reflection',vo[h],vi[h]-2*dot(vi,nn)*nn[h]/dot(nn,nn))
    edge=sub(ps[(j+1)%n],p);normal=(edge[1],-edge[0]);add('caustic_line_tangency',normal[0]**2+f.beta**2*normal[1]**2,dot(normal,p)**2,f.a**2*dot(normal,normal))
    n0=ns[j];n1=ns[(j+1)%n];dd=D(n0,n1);assert abs(dd)>m.mpf('1e-80')
    vs.append(((n1[1]-n0[1])/dd,(n0[0]-n1[0])/dd))
   areas=[]
   for e in [1,-1]:
    feet=[]
    for j in range(n):
     x=vs[j-1];edge=sub(vs[j],x);t=dot(sub((e*f.c,0),x),edge)/dot(edge,edge);q=(x[0]+t*edge[0],x[1]+t*edge[1]);feet.append(q)
     explicit=f.Q(w+j*f.h+(0 if e==1 else 2*f.K));explicit=explicit if e==1 else tuple(-h for h in explicit)
     for h in [0,1]:add('actual_outer_side_projection',q[h],explicit[h],f.a)
    areas.append(A(feet))
   products.append(areas[0]*areas[1]/f.a**4);ratios.append(areas[0]/f.inverse(w,-1))
   R=[f.projectivity(v) for v in vs];AR=A(R);Bp=areas[0];add('bicentric_contact_area_ratio',Bp*(Rb*Rb-db*db),AR*r*r,max(1,abs(AR*r*r)))
   u=(1+f.k)*(w+f.v-f.K)/2;ds=[m.ellipfun('dn',u+2*j*Kb*tau/n,mb) for j in range(n)]
   for j,v in enumerate(R):
    add('negative_center_polar_circle',(v[0]-db)**2+v[1]**2,Rb*Rb,Rb*Rb)
    add('positive_tangent_length_squared',dot(v,v)-r*r,tm*tm*ds[j]**2,tm*tm)
    assert D(f.Q(w+j*f.h),f.Q(w+(j+1)*f.h))>0
   add('bicentric_dn_area',Bp,r**3*tm/(Rb*Rb-db*db)*sum(ds),r*r)
   add('old_arbitrary_order_dn_sum',sum(ds),scale*m.ellipfun('dn',scale*u,mn),n)
   add('dn_halfperiod_focus_shift',sum(m.ellipfun('dn',u+Kb+2*j*Kb*tau/n,mb) for j in range(n)),sum(m.ellipfun('dn',u+2*j*Kb*tau/n,mb) for j in range(n)) if n%2==0 else scale*m.ellipfun('dn',scale*u+Kn,mn),n)
  add('opposite_inverse_proportionality',max(ratios),min(ratios),max(abs(x) for x in ratios))
  span=max(products)-min(products)
  if n%2:add('odd_product_span',span)
  else:assert span>m.mpf('1e-10')
  z=m.mpf('.217')*f.L+m.mpf('.091')*f.p
  add('trace_reduced_period',f.trace(z+f.L),f.trace(z),r*r);add('trace_reflection',f.trace(2*f.K-z),f.trace(z),r*r);add('trace_imaginary_antiperiod',f.trace(z+2*f.p),-f.trace(z),r*r)
  add('complementary_zero_row1',f.trace(f.b0+f.p+f.L/2),0,r*r);add('complementary_zero_row2',f.trace(f.b0+3*f.p+f.L/2),0,r*r)
  residue=-f.a/(f.k*f.j('sn',f.v));eps=m.mpf('1e-23')*(m.mpf('.8')+m.mpf('.6')*m.j);pole=[]
  for im in [1,3]:
   qm=f.Q(f.K+im*f.p-f.v+eps);qp=f.Q(f.K+im*f.p+f.v+eps);R=(residue,(1 if im==1 else -1)*m.j*residue)
   pole.append({'row':im,'residue_error':num(max(err(eps*qm[h],R[h],r) for h in [0,1])),'opposite_error':num(max(err(eps*qp[h],-R[h],r) for h in [0,1])),'epsilon_squared_trace':num(abs(eps*eps*f.trace(f.K+im*f.p-f.v+eps))/(r*r))})
   assert max(m.mpf(pole[-1][h]) for h in ['residue_error','opposite_error','epsilon_squared_trace'])<m.mpf('1e-17')
  wrong_cn=abs(f.j('cn',z+2*f.p)-f.j('cn',z))/abs(f.j('cn',z));assert wrong_cn>m.mpf('1.999')
  assert all(v<m.mpf('1e-75') for v in maxima.values()),(n,k,{h:num(v) for h,v in maxima.items() if v>=m.mpf('1e-75')})
  rows.append({'N':n,'tau':tau,'k':k,'phase_count':3,'max_normalized_errors':{h:num(v) for h,v in maxima.items()},'product_over_a4':[num(v) for v in products],'span':num(span),'complex_pole_rows':pole,'wrong_cn_period_control':num(wrong_cn)})
  print('PASS fresh family',n,tau,k,flush=True)
 return {'precision_digits':m.mp.dps,'interval_certification':False,'families':rows}
if __name__=='__main__':
 start=datetime.now(timezone.utc).isoformat();result={'utc_start':start,'python':sys.version,'sympy':s.__version__,'mpmath':m.__version__,'exact_fixture':exact_fixture(),'finite_lattice':lattice(),'numerical':numeric(),'universal_proof_from_finite_checks':False,'utc_end':datetime.now(timezone.utc).isoformat()}
 (O/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print('ALL FRESH CONTROLS PASS')
