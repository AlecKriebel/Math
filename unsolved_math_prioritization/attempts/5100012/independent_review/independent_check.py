#!/usr/bin/env python3
"""Independent review controls: direct Euclidean feet and complex pole cancellation."""
from math import gcd
from fractions import Fraction as F
import json
import mpmath as m
m.mp.dps=95
exact=0;rotations=0
for n in range(3,151):
 for t in range(1,(n+1)//2):
  if gcd(n,t)!=1: continue
  step=F(2*t,n);order=step.denominator
  orbit={(j*step)%1 for j in range(n)}
  assert len(orbit)==order;exact+=1
  multiplicities=[sum((j*step)%1==q for j in range(n)) for q in orbit]
  assert all(v==n//order for v in multiplicities);exact+=1
  phase=order*(F(1,2)+step/2)
  assert phase%1==(F(0) if n%4==2 else F(1,2));exact+=1
  assert step%1!=0;exact+=1
  rotations+=1
count=0;maxerr=m.mpf(0);wrong=[];pole_records=[]
def assert_close(a,b,label,tol='1e-75'):
 global count,maxerr
 e=abs(a-b)/max(1,abs(a),abs(b))
 assert e<m.mpf(tol),(label,str(e))
 count+=1;maxerr=max(maxerr,e)
def shoelace(points):
 return sum(points[j][0]*points[(j+1)%len(points)][1]-points[j][1]*points[(j+1)%len(points)][0] for j in range(len(points)))/2
for k in map(m.mpf,['0.17','0.63','0.91']):
 par=k*k;kp=m.sqrt(1-par);K=m.ellipk(par);Kc=m.ellipk(1-par)
 sn=lambda u:m.ellipfun('sn',u,par)
 cn=lambda u:m.ellipfun('cn',u,par)
 dn=lambda u:m.ellipfun('dn',u,par)
 for n,t in [(3,1),(4,1),(5,1),(5,2),(7,2),(7,3),(8,3),(9,4),(12,5),(16,7),(6,1),(10,3),(14,5)]:
  v=2*K*t/n;step=2*v;aa=dn(v)/cn(v);bb=kp/cn(v)
  def geometric_areas(w):
   points=[(-aa*sn(w+j*step),bb*cn(w+j*step)) for j in range(n)]
   feet=[]
   for p,q in zip(points,points[1:]+points[:1]):
    dx,dy=q[0]-p[0],q[1]-p[1]
    cross=p[0]*dy-p[1]*dx
    # Closest point to the origin on the chord, using its perpendicular normal.
    feet.append((cross*dy/(dx*dx+dy*dy),-cross*dx/(dx*dx+dy*dy)))
   return shoelace(points),shoelace(feet)
  vals=[geometric_areas(K*q) for q in map(m.mpf,['0.071','0.413','1.119','2.237'])]
  products=[a*b for a,b in vals]
  if n%4!=2:
   for prod in products[1:]:assert_close(prod,products[0],f'area product {n}/{t}')
  else:
   wrong.append(float(max(products)-min(products)))
  for a0,b0 in vals:
   assert a0>0 and b0>0;count+=1
  # Independent complex continuation of the pedal map; only real geometry above
  # is used for the invariant checks.
  def Q(u):return (-(kp*kp)*sn(u)/(dn(u)**2),kp*cn(u)/(dn(u)**2))
  def T(u):return shoelace([Q(u+j*step) for j in range(n)])
  S=lambda w:sum(dn(w+j*step) for j in range(n))
  c=T(K*m.mpf('.231'))/S(K*m.mpf('.231')+K)
  for zz in [K*m.mpf('.37')+m.j*Kc*m.mpf('.29'), K*m.mpf('1.11')+m.j*Kc*m.mpf('.57')]:
   assert_close(T(zz),c*S(zz+K),f'complex meromorphic proportionality {n}/{t}')
  if (n,t) in [(3,1),(4,1),(5,2),(8,3)]:
   r=K+m.j*Kc
   e1=m.mpf('1e-17');e2=m.mpf('1e-22')
   res1=e1*T(r+e1);res2=e2*T(r+e2)
   assert_close(res1,res2,f'simple pole residue {n}/{t}',tol='1e-15')
   assert abs(e2*res2)<m.mpf('1e-18');count+=1
   pole_records.append({'N':n,'turning':t,'modulus':str(k),'residue_nonzero':abs(res2)>m.mpf('1e-20')})
assert any(abs(x)>1e-7 for x in wrong)
print(json.dumps({'status':'PASS','exact_lattice_assertions':exact,'primitive_rotations':rotations,
 'high_precision_diagnostics':count,'precision_digits':95,'maximum_scaled_diagnostic_error':m.nstr(maxerr,10),
 'wrong_parity_nonconstant_examples':len(wrong),'pole_diagnostics':pole_records,
 'limits':'Finite exact lattice controls and non-certified high-precision diagnostics. Written analytic audit establishes the universal result; no author modules imported.'},indent=2))
