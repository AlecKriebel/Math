"""Independent direct reflection and perpendicular-projection sampler.
High precision NONINTERVAL evidence, not a universal proof. Frozen before author access.
"""
from pathlib import Path
import json,math
import mpmath as mp
mp.mp.dps=100
Z=mp.mpf(0);O=mp.mpf(1)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def scale(t,p):return tuple(t*x for x in p)
def area(P):return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def n_at(p,a,b):return (p[0]/a**2,p[1]/b**2)
def reflect(v,n):return sub(v,scale(2*dot(v,n)/dot(n,n),n))
def initial(p,a,b,lam):
 n=n_at(p,a,b);nn=dot(n,n);J=mp.sqrt(lam)/(a*b);tau=(-n[1],n[0]);rad=1-J**2/nn
 if rad<=0:raise ArithmeticError('No elliptic initial tangent')
 return add(scale(-J/nn,n),scale(mp.sqrt(rad/nn),tau))
def step(p,v,a,b):
 tt=-2*(p[0]*v[0]/a**2+p[1]*v[1]/b**2)/(v[0]**2/a**2+v[1]**2/b**2)
 if tt<=0:raise ArithmeticError('Nonpositive outgoing step')
 q=add(p,scale(tt,v));w=reflect(v,n_at(q,a,b));return q,w,tt

def orbit(a,b,lam,N,r=Z):
 p=(a*(1-r*r)/(1+r*r),b*2*r/(1+r*r));v=initial(p,a,b,lam);P=[p];V=[v];L=[]
 for i in range(N):
  p,v,t=step(p,v,a,b);P.append(p);V.append(v);L.append(t)
 return P,V,L

def rotation_endpoint(a,b,lam,N):
 P,_,_=orbit(a,b,lam,N);angs=[mp.atan2(p[1]/b,p[0]/a) for p in P];total=Z
 for i in range(N):
  d=angs[i+1]-angs[i]
  if d<0:d+=2*mp.pi
  total+=d
 return total

def periodic_lambda(a,b,N,m):
 lo=b*b*mp.mpf('1e-90');hi=b*b*(1-mp.mpf('1e-90'));target=2*mp.pi*m
 for it in range(335):
  mid=(lo+hi)/2
  if rotation_endpoint(a,b,mid,N)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2

def foot(f,p,q):
 d=sub(q,p);return add(p,scale(dot(sub(f,p),d)/dot(d,d),d))
def tfoot(f,n):return add(f,scale((1-dot(n,f))/dot(n,n),n))
def intersection(n,m):
 den=cross(n,m);return ((m[1]-n[1])/den,(n[0]-m[0])/den)
def mstr(x):return mp.nstr(x,85)
def sample(a,b,N,m,r,lam):
 P,V,L=orbit(a,b,lam,N,r);P0=P[:-1];c=mp.sqrt(a*a-b*b);Ns=[n_at(p,a,b) for p in P0]
 Ts=[intersection(Ns[i],Ns[(i+1)%N]) for i in range(N)]
 checks={'closure':mp.sqrt(dot(sub(P[-1],P[0]),sub(P[-1],P[0]))),'ellipse':max(abs(p[0]**2/a**2+p[1]**2/b**2-1) for p in P),'unit':max(abs(dot(v,v)-1) for v in V),'reflection':Z,'caustic_tangency':Z,'projection_incidence':Z,'projection_perpendicular':Z,'circle_foot_locus':Z,'outer_side':Z,'outer_projection_agreement':Z,'min_outer_det':min(abs(cross(Ns[i],Ns[(i+1)%N])) for i in range(N))}
 for i in range(N):
  d=sub(P[i+1],P[i]);n=(-d[1],d[0]);h=dot(n,P[i]);res=h*h-(a*a-lam)*n[0]**2-(b*b-lam)*n[1]**2
  checks['caustic_tangency']=max(checks['caustic_tangency'],abs(res)/(1+abs(h*h)))
  checks['reflection']=max(checks['reflection'],mp.sqrt(dot(sub(reflect(V[i],n_at(P[i+1],a,b)),V[i+1]),sub(reflect(V[i],n_at(P[i+1],a,b)),V[i+1]))))
  checks['outer_side']=max(checks['outer_side'],abs(dot(Ns[i],Ts[(i-1)%N])-1),abs(dot(Ns[i],Ts[i])-1))
 A=[]
 for sigma in [1,-1]:
  f=(sigma*c,Z);Q=[foot(f,P0[i],P0[(i+1)%N]) for i in range(N)];Qp=[tfoot(f,n) for n in Ns]
  for i in range(N):
   d=sub(P0[(i+1)%N],P0[i]);n=(-d[1],d[0]);h=dot(n,P0[i]);
   checks['projection_incidence']=max(checks['projection_incidence'],abs(dot(n,Q[i])-h),abs(dot(Ns[i],Qp[i])-1))
   checks['projection_perpendicular']=max(checks['projection_perpendicular'],abs(dot(sub(Q[i],f),d)),abs(dot(sub(Qp[i],f),(-Ns[i][1],Ns[i][0]))))
   checks['circle_foot_locus']=max(checks['circle_foot_locus'],abs(dot(Q[i],Q[i])-(a*a-lam)),abs(dot(Qp[i],Qp[i])-a*a))
   qptest=foot(f,Ts[(i-1)%N],Ts[i]);checks['outer_projection_agreement']=max(checks['outer_projection_agreement'],mp.sqrt(dot(sub(qptest,Qp[i]),sub(qptest,Qp[i]))))
  A.extend([area(Q),area(Qp)])
 target=A[0]*A[3]-A[2]*A[1]
 checks['target_cross_product']=abs(target)/(1+abs(A[0]*A[3])+abs(A[2]*A[1]))
 checks['reversal']=max(abs(area(list(reversed(poly)))+area(poly)) for poly in [P0,Ts])
 checks['repetition']=max(abs(area(poly*3)-3*area(poly)) for poly in [P0,Ts])
 # source target and common-scale quotient, each independently measured
 return {'a':mstr(a),'b':mstr(b),'N':N,'winding':m,'primitive':math.gcd(N,m)==1,'r_phase':mstr(r),'lambda':mstr(lam),'alpha_squared':mstr(a*a-lam),'beta_squared':mstr(b*b-lam),'signed_areas_Aplus_Aprimeplus_Aminus_Aprimeminus':[mstr(x) for x in A],'ratios':{'target_original':mstr(A[0]/A[2]),'target_outer':mstr(A[1]/A[3]),'prime_to_original_plus':mstr(A[1]/A[0]),'prime_to_original_minus':mstr(A[3]/A[2])},'checks':{k:mstr(v) for k,v in checks.items()},'vertices':[[mstr(x) for x in p] for p in P0]}
if __name__=='__main__':
 results=[]
 families=[(3,1),(4,1),(5,1),(5,2),(6,1),(7,1),(7,2),(7,3),(8,1),(8,3),(9,2),(9,4),(11,5)]
 for aa in ['1.0001','2','10']:
  a=mp.mpf(aa);b=O
  for N,m in families:
   lam=periodic_lambda(a,b,N,m)
   for r in [Z,mp.mpf('0.2'),mp.mpf('1.3')]:
    out=sample(a,b,N,m,r,lam);results.append(out)
   print('completed family',aa,N,m,'lambda',mp.nstr(lam,22),'max target residual',mp.nstr(max(mp.mpf(x['checks']['target_cross_product']) for x in results[-3:]),6),flush=True)
 output={'precision_dps':100,'evidence':'Finite high-precision NONINTERVAL computations, not a universal proof. Direct reflection; canonical elliptic identities not used.','results':results}
 Path(__file__).with_name('independent_billiard_results.json').write_text(json.dumps(output,indent=2)+'\n')
 checknames=[k for k in results[0]['checks'] if k!='min_outer_det']
 print(json.dumps({'samples':len(results),'families':len(results)//3,'max_residuals':{k:mstr(max(mp.mpf(x['checks'][k]) for x in results)) for k in checknames},'minimum_absolute_signed_area':mstr(min(abs(mp.mpf(v)) for x in results for v in x['signed_areas_Aplus_Aprimeplus_Aminus_Aprimeminus'])),'minimum_outer_determinant':mstr(min(mp.mpf(x['checks']['min_outer_det']) for x in results))},indent=2))
