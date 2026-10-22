#!/usr/bin/env python3
"""Independent exact algebra and finite boundary diagnostics; no ODE simulation."""
from fractions import Fraction as F
from pathlib import Path
import json,sys,hashlib,datetime
R=Path(__file__).resolve().parent;A=R.parent
# Sparse polynomials in ax,ay,bx,by,x,y,L. This checks the general identity,
# not only evaluations at a collection of points.
N=7;ZERO=(0,)*N
def add(a,b):
 d=dict(a)
 for m,c in b.items():d[m]=d.get(m,F(0))+c
 return {m:c for m,c in d.items() if c}
def scale(a,c):return {m:v*c for m,v in a.items() if v*c}
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
 d={}
 for m,c in a.items():
  for n,e in b.items():
   k=tuple(x+y for x,y in zip(m,n));d[k]=d.get(k,F(0))+c*e
 return {m:c for m,c in d.items() if c}
def sq(a):return mul(a,a)
def variable(i):return {tuple(int(j==i) for j in range(N)):F(1)}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dist(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def main():
 ax,ay,bx,by,x,y,L=[variable(i) for i in range(N)];one={ZERO:F(1)}
 da=add(sq(sub(x,ax)),sq(sub(y,ay)));db=add(sq(sub(x,bx)),sq(sub(y,by)))
 ff=sub(da,mul(L,db));d2=add(sq(sub(ax,bx)),sq(sub(ay,by)))
 gx=scale(sub(sub(x,ax),mul(L,sub(x,bx))),2);gy=scale(sub(sub(y,ay),mul(L,sub(y,by))),2)
 residual=sub(add(sq(gx),sq(gy)),scale(add(mul(sub(one,L),ff),mul(L,d2)),4))
 need(not residual,'general polynomial gradient identity')
 sites=[(F(1,5),F(1,4)),(F(3,4),F(1,3)),(F(2,5),F(4,5))]
 ds=[dist(sites[i],sites[j]) for i,j in [(0,1),(0,2),(1,2)]]
 need(ds==[F(557,1800),F(137,400),F(49,144)],'independent exact distances')
 det=(sites[1][0]-sites[0][0])*(sites[2][1]-sites[0][1])-(sites[1][1]-sites[0][1])*(sites[2][0]-sites[0][0])
 need(det==F(343,1200),'independent exact determinant')
 h=F(1,16);K=4*h*h;eta=K*K
 need(K==F(1,64) and eta==F(1,4096) and 1-2*eta==F(2047,2048),'independent exact constants')
 configurations=[('original',sites,h),('boundary_square_and_equal_separation',[(F(1,16),F(1,16)),(F(3,16),F(3,16))],h),('collinear_allowed',[(F(1,4),F(1,2)),(F(1,2),F(1,2)),(F(3,4),F(1,2))],h),('five_sites',[(F(1,5),F(1,5)),(F(4,5),F(1,5)),(F(1,5),F(4,5)),(F(4,5),F(4,5)),(F(1,2),F(1,2))],F(1,32))]
 checks=0;cases=[]
 for name,pts,hw in configurations:
  n=len(pts);need(all(hw<=c<=1-hw for pt in pts for c in pt),'contained square')
  need(all(dist(pts[i],pts[j])>=8*hw*hw for i in range(n) for j in range(i)),'separated square')
  for k in (3,4,8):
   for i in range(n):
    for s in (F(1,2),F(1,1000)):
     zi=s**k;other=[j for j in range(n) if j!=i]
     # One competitor takes nearly all remaining mass, testing the true max.
     z=[F(0)]*n;z[i]=zi
     for j in other[:-1]:z[j]=zi/F(n)
     z[other[-1]]=1-sum(z)
     need(sum(z)==1 and min(z)>0,'positive simplex diagnostic state')
     for dx in (-1,0,1):
      for dy in (-1,0,1):
       yy=(pts[i][0]+dx*hw*s,pts[i][1]+dy*hw*s)
       for j in other:
        need(zi**2*dist(yy,pts[j])**k>=z[j]**2*dist(yy,pts[i])**k,'actual all-competitor influence')
        checks+=1
  cases.append({'name':name,'n':n,'geometry':'PASS','finite_influence_diagnostics':'PASS'})
 exponents=[]
 for p in (F(1,1000000),F(1,3),F(1,2),F(999999,1000000)):
  r=1/(1-p)
  need(r*(1-p)==1 and r-1==p*r,'general scalar comparison exponent arithmetic')
  exponents.append(str(p))
 result={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'optimized' if sys.flags.optimize else 'normal','general_gradient_polynomial_residual_terms':len(residual),'distances':list(map(str,ds)),'determinant':str(det),'K':str(K),'lower':str(eta),'upper':str(1-2*eta),'cases':cases,'exact_influence_diagnostic_comparisons':checks,'scalar_exponent_cases':exponents,'limits':'Sparse-polynomial identity is exact algebra. Finite influence diagnostics are supporting checks, not an analytic all-state/all-time proof. No trajectory integration or conclusion for p>=1 is asserted.'}
 (R/('EXACT_CHECKS_OPTIMIZED.json' if sys.flags.optimize else 'EXACT_CHECKS_NORMAL.json')).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result))
if __name__=='__main__':main()
