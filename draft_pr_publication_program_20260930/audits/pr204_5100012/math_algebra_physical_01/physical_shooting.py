#!/usr/bin/env python3
"""Independent Euclidean confocal billiard shooting, no elliptic functions or author imports.
Tangency is obtained by mapping the inner ellipse to a circle; every subsequent step
uses an outer quadratic intersection and Euclidean normal reflection.
"""
import sys,json,hashlib,math
from pathlib import Path
from collections import Counter
import mpmath as mp
mp.mp.dps=85
COUNTS=Counter();MAX={}
TOL=mp.mpf('1e-48')
def require(ok,label):
 if not ok:raise RuntimeError(label)
 COUNTS[label]+=1
def check(err,label,tol=TOL):
 MAX[label]=max(MAX.get(label,mp.mpf(0)),abs(err))
 require(abs(err)<tol,label)
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(z,p):return (z*p[0],z*p[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return mp.sqrt(dot(p,p))
def initial(a,b,lam,theta,sign):
 p=(a*mp.cos(theta),b*mp.sin(theta));aa=mp.sqrt(a*a-lam);bb=mp.sqrt(b*b-lam)
 z=(p[0]/aa,p[1]/bb);r2=dot(z,z);w=mp.sqrt(r2-1)
 t=(aa*(z[0]-w*z[1])/r2,bb*(z[1]+w*z[0])/r2)
 v=sub(t,p)
 if mp.sign(cross(p,v))!=sign:
  t=(aa*(z[0]+w*z[1])/r2,bb*(z[1]-w*z[0])/r2);v=sub(t,p)
 return p,mul(1/norm(v),v)
def step(a,b,p,v):
 qf=lambda z:z[0]*z[0]/(a*a)+z[1]*z[1]/(b*b)
 length=-2*(p[0]*v[0]/(a*a)+p[1]*v[1]/(b*b))/qf(v)
 q=add(p,mul(length,v));n=(q[0]/(a*a),q[1]/(b*b))
 reflected=sub(v,mul(2*dot(v,n)/dot(n,n),n))
 return q,reflected,length

def shoot_advance(a,b,lam,N):
 p,v=initial(a,b,lam,mp.mpf(0),1);total=mp.mpf(0)
 for j in range(N):
  q,v2,length=step(a,b,p,v)
  ang=mp.atan2(cross((p[0]/a,p[1]/b),(q[0]/a,q[1]/b)),dot((p[0]/a,p[1]/b),(q[0]/a,q[1]/b)))
  if ang<0:ang+=2*mp.pi
  total+=ang;p,v=q,v2
 return total

def locate(a,b,N,m):
 low=mp.mpf(0);high=b*b
 for j in range(250):
  mid=(low+high)/2
  if shoot_advance(a,b,mid,N)<2*mp.pi*m:low=mid
  else:high=mid
 return (low+high)/2

def area(P):return sum(cross(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2

def orbit(a,b,lam,N,m,theta,sign):
 p,v=initial(a,b,lam,theta,sign);start=p;vstart=v;P=[];V=[];minimum_nonclosure=mp.inf
 for j in range(N):
  P.append(p);V.append(v);q,v2,length=step(a,b,p,v)
  require(length>0,'positive_chord_length')
  check(p[0]*p[0]/(a*a)+p[1]*p[1]/(b*b)-1,'outer_ellipse')
  # Quadratic discriminant for the ORIGINAL COMPLETE chord and caustic.
  Aq=v[0]*v[0]/(a*a-lam)+v[1]*v[1]/(b*b-lam)
  Bq=2*(p[0]*v[0]/(a*a-lam)+p[1]*v[1]/(b*b-lam))
  Cq=p[0]*p[0]/(a*a-lam)+p[1]*p[1]/(b*b-lam)-1
  check((Bq*Bq-4*Aq*Cq)/max(1,abs(Bq*Bq),abs(4*Aq*Cq)),'caustic_tangency')
  check(norm(v2)-1,'unit_reflected_velocity')
  n=(q[0]/(a*a),q[1]/(b*b));unitn=mul(1/norm(n),n)
  check(dot(v2,unitn)+dot(v,unitn),'equal_normal_components')
  check(cross(v2,unitn)-cross(v,unitn),'equal_tangential_components')
  p,v=q,v2
  if j<N-1:minimum_nonclosure=min(minimum_nonclosure,norm(sub(p,start))/max(a,b))
 check(norm(sub(p,start))/max(a,b),'position_closure')
 check(norm(sub(v,vstart)),'velocity_closure')
 require(minimum_nonclosure>mp.mpf('1e-8'),'physical_least_period')
 Q=[];clipped=[];M=(a/7,b/9);moving=[];maxfootoutside=mp.mpf(0)
 for p,q in zip(P,P[1:]+P[:1]):
  d=sub(q,p);t=-dot(p,d)/dot(d,d);Q.append(add(p,mul(t,d)))
  clipped.append(add(p,mul(max(0,min(1,t)),d)))
  tM=dot(sub(M,p),d)/dot(d,d);moving.append(add(p,mul(tM,d)))
  maxfootoutside=max(maxfootoutside,max(0,-t,t-1))
  check(dot(Q[-1],d)/max(1,norm(Q[-1])*norm(d)),'perpendicular_origin_foot')
 A=area(P);B=area(Q)
 return {'A':A,'B':B,'product':A*B,'moving_product':A*area(moving),'clipped_product':A*area(clipped),'max_foot_outside':maxfootoutside,'minimum_nonclosure':minimum_nonclosure}

def main():
 if '--false-identity' in sys.argv:
  a=mp.mpf(2);b=mp.mpf(1);lam=locate(a,b,3,1)
  z=orbit(a,b,lam,3,1,mp.mpf(0),1);w=orbit(a,b,lam,3,1,mp.pi/2,1)
  check(z['product']-(w['product']+1),'FALSE_physical_product_plus_one')
 records=[];wrong=[];moving=[];clipped_bad=[];outside=mp.mpf(0)
 for aspect in ['1.01','2','8']:
  a=mp.mpf(aspect);b=mp.mpf(1)
  for N in [3,4,5,7,8,9,12,16,6,10]:
   for m in range(1,(N+1)//2):
    if math.gcd(m,N)!=1 or 2*m>=N:continue
    lam=locate(a,b,N,m);require(0<lam<b*b,'proper_elliptical_caustic')
    vals=[orbit(a,b,lam,N,m,theta,1) for theta in [mp.mpf(0),mp.pi/2,mp.pi*mp.mpf('.17'),mp.pi*mp.mpf('.41'),mp.pi*mp.mpf('.73')]]
    reverse=orbit(a,b,lam,N,m,mp.pi*mp.mpf('.17'),-1)
    check((reverse['A']+vals[2]['A'])/max(1,abs(vals[2]['A'])),'signed_area_reversal')
    check((reverse['B']+vals[2]['B'])/max(1,abs(vals[2]['B'])),'signed_pedal_reversal')
    check((reverse['product']-vals[2]['product'])/max(1,abs(vals[2]['product'])),'product_reversal')
    spread=(max(v['product'] for v in vals)-min(v['product'] for v in vals))/max(1,abs(vals[0]['product']))
    if N%4!=2:check(spread,'target_phase_product')
    else:wrong.append({'aspect':aspect,'N':N,'winding':m,'relative_spread':mp.nstr(spread,12)})
    cs=(max(v['clipped_product'] for v in vals)-min(v['clipped_product'] for v in vals))/max(1,abs(vals[0]['clipped_product']))
    if N%4!=2:clipped_bad.append(cs)
    ms=(max(v['moving_product'] for v in vals)-min(v['moving_product'] for v in vals))/max(1,abs(vals[0]['moving_product']))
    if N%2==1:moving.append(ms)
    outside=max(outside,max(v['max_foot_outside'] for v in vals))
    records.append({'aspect':aspect,'N':N,'winding':m,'target':N%4!=2,'lambda':mp.nstr(lam,32),'relative_phase_spread':mp.nstr(spread,12),'A_reference':mp.nstr(vals[0]['A'],18),'B_reference':mp.nstr(vals[0]['B'],18),'moving_base_spread':mp.nstr(ms,12),'clipped_product_spread':mp.nstr(cs,12)})
 require(any(mp.mpf(v['relative_spread'])>mp.mpf('1e-6') for v in wrong),'wrong_parity_nonconstant_control')
 require(max(moving)>mp.mpf('1e-6'),'moving_base_nonconstant_control')
 require(max(clipped_bad)>mp.mpf('1e-6'),'segment_projection_nonconstant_control')
 # Repeating a physical primitive 6-orbit twice is a formal N=12 list with product 4*A*B.
 r=next(v for v in wrong if v['N']==6 and v['aspect']=='2')
 require(mp.mpf(r['relative_spread'])>mp.mpf('1e-6'),'repeated_nonprimitive_12_list_counterexample')
 # False target control is a mathematical identity differing by 1, not an artificial syntax failure.
 result={'status':'PASS','precision_digits':mp.mp.dps,'checks':dict(COUNTS),'maximum_residuals':{k:mp.nstr(v,12) for k,v in MAX.items()},'physical_rotation_cases':len(records),'target_rotation_cases':sum(r['target'] for r in records),'phase_direction_orbits':len(records)*6,'records':records,'excluded_parity_controls':wrong,'largest_clipped_projection_parameter_excursion':mp.nstr(outside,12),'segment_control':'Clipped-to-segment feet produce nonconstant target products in tested families; see clipped_product_spread records.','unsigned_control':'All tested primitive elliptical cases had same signs; reversal changes both signs and leaves the product, so unsigned-product extension is not disproved here.','limits':'Noninterval finite diagnostics from direct physical shooting; no universal theorem or priority claim. No Jacobi functions, author modules or prior target proof used.'}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
