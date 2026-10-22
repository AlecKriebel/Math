#!/usr/bin/env python3
"""Fresh exact plane-arrangement/triangle-simplex control; stdlib only.
No package checker or result is imported. Finite computations supplement proofs.
"""
from fractions import Fraction as Q
from math import comb,factorial
import argparse,json
C=0
def require(b,msg):
 global C; C+=1
 if not b: raise RuntimeError(msg)
def clip(poly,a,b,c):
 out=[]
 for u,v in zip(poly,poly[1:]+poly[:1]):
  fu=a*u[0]+b*u[1]+c;fv=a*v[0]+b*v[1]+c
  if fu>=0:out.append(u)
  if (fu<0<fv) or (fv<0<fu):
   t=fu/(fu-fv);out.append(tuple(u[i]+t*(v[i]-u[i]) for i in (0,1)))
 clean=[]
 for u in out:
  if not clean or clean[-1]!=u:clean.append(u)
 if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
 return clean

def area(poly):
 return abs(sum(u[0]*v[1]-v[0]*u[1] for u,v in zip(poly,poly[1:]+poly[:1])))/2 if len(poly)>2 else Q(0)
def partition(n):
 polys=[[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1))]]
 lines={(m,0,-k) for m in range(1,n) for k in range(1,m)}
 lines|={(j,1,-k) for j in range(n) for k in range(j+2)}
 for a,b,c in sorted(lines):
  new=[]
  for p in polys:
   cuts=[clip(p,a,b,c),clip(p,-a,-b,-c)]
   good=[q for q in cuts if area(q)>0]
   require(sum(map(area,good))==area(p),'split area conservation')
   new.extend(good)
  polys=new
 require(sum(map(area,polys))==1,'whole square area')
 return polys

def eval_aff(f,v):return f[0]*v[0]+f[1]*v[1]+f[2]
def affine_power_integral(f,m,tri):
 vals=[eval_aff(f,v) for v in tri]
 # Complete homogeneous symmetric polynomial from its defining generating function.
 h=[Q(0)]*(m+1);h[0]=Q(1)
 for value in vals:
  for degree in range(1,m+1):h[degree]+=value*h[degree-1]
 return 2*area(tri)*h[m]/((m+1)*(m+2))
def integrate(poly,f,m):
 return sum((affine_power_integral(f,m,[poly[0],poly[i],poly[i+1]]) for i in range(1,len(poly)-1)),Q(0))
def data(n,p):
 if n<1 or p<2 or p%2:raise ValueError('positive n and positive even exponent required')
 polys=partition(n);result=Q(0);rows=[]
 for poly in polys:
  witness=tuple(sum(v[i] for v in poly)/len(poly) for i in (0,1))
  floors=[(j*witness[0]+witness[1]).numerator//(j*witness[0]+witness[1]).denominator for j in range(n)]
  funcs=[(Q(j),Q(1),Q(-floors[j])) for j in range(n)]
  perm=sorted(range(n),key=lambda j:eval_aff(funcs[j],witness))
  ordered=[(Q(0),Q(0),Q(0))]+[funcs[j] for j in perm]+[(Q(0),Q(0),Q(1))]
  for vertex in poly:
   values=[eval_aff(f,vertex) for f in ordered]
   require(all(0<=v<=1 for v in values),'valid modular affine values')
   require(values==sorted(values),'fixed order throughout convex cell')
  val=Q(0)
  for k in range(n+1):
   f,g=ordered[k],ordered[k+1]
   left=(f[0],f[1],f[2]-Q(k,n));right=(g[0],g[1],g[2]-Q(k,n))
   val+=(integrate(poly,right,p+1)-integrate(poly,left,p+1))/(p+1)
  require(val>=0,'nonnegative complete cell integral');result+=val
  rows.append({'area':str(area(poly)),'moment':str(val),'floors':floors,'order':perm})
 return result,rows

def iid(n,p):
 # Entire Binomial distribution followed by exact integer beta integrals.
 return sum((Q(comb(n,k)*comb(p,a)*(-1)**a)*Q(k,n)**(p-a)*Q(factorial(k+a)*factorial(n-k),factorial(n+a+1)) for k in range(n+1) for a in range(p+1)),Q(0))
def point_moment(pts,p):
 n=len(pts);s=[Q(0)]+sorted(pts)+[Q(1)]
 return sum(((s[k+1]-Q(k,n))**(p+1)-(s[k]-Q(k,n))**(p+1) for k in range(n+1)),Q(0))/(p+1)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--force-failure',action='store_true');args=parser.parse_args()
 # Primitive controls do not use target answers.
 tri=[(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1))]
 for a in range(8):
  require(affine_power_integral((1,0,0),a,tri)==Q(1,(a+1)*(a+2)),'simplex primitive')
  require(affine_power_integral((0,0,1),a,tri)==Q(1,2),'constant primitive')
 moments={};full={}
 for n in range(1,6):
  for p in (2,4,6):
   value,rows=data(n,p);ind=iid(n,p)
   if p==2:require(value==Q(1,6*n),'second moment')
   if n<=2:require(value==ind,'complete law small-n control')
   if p==4:require(ind==Q(3*n-1,30*n**3),'iid formula')
   moments[f'{n},{p}']={'lattice':str(value),'iid':str(ind),'cells':len(rows)}
   if p==4:full[str(n)]=rows
 require(Q(moments['3,4']['lattice'])==Q(19,1620),'three-point value')
 require(Q(moments['4,4']['lattice'])==Q(139,17280),'four-point value')
 require(Q(moments['3,4']['lattice'])-iid(3,4)==Q(1,540),'strict gap')
 require(Q(moments['3,4']['lattice'])/iid(3,4)==Q(19,16),'ratio')
 # Independent simplex derivation of empty tails; no fitting or numerical quadrature.
 tails={}
 for n in (2,3,4,5,10,234,1000):
  up=[(Q(0),Q(0)),(Q(0),Q(1)),(Q(1,n-1),Q(0))]
  one=(integrate(up,(0,1,0),5)+integrate(up,(-(n-1),-1,1),5))/5
  require(one==Q(1,105*(n-1)),'unconditional triangle contribution')
  tails[str(n)]=str(2*one-iid(n,4))
  if n>=4:require(2*one>iid(n,4),'tail reversal')
 require(Q(tails['3'])<0,'tail bound insufficient n3')
 # Reconstruct the all-n positivity certificate from expansion.
 for t in range(100):
  n=t+4;require(4*n**3-21*n**2+28*n-7==25+52*t+27*t*t+4*t**3,'polynomial identity')
 adverse=[]
 def reject(name,b):require(b,name);adverse.append(name)
 reject('deleted positive cell loses exact moment',sum(Q(r['moment']) for r in full['3'][1:])!=Q(19,1620))
 reject('one no-wrap region cannot replace full ensemble',Q(full['3'][0]['moment'])!=Q(19,1620))
 reject('discarding normalization changes comparison',Q(19,1620)*3**4!=Q(19,1620))
 reject('substituting triple iid erases true gap',iid(3,4)!=Q(19,1620))
 reject('fixed zero generator cannot replace uniform generator',point_moment([Q(1,2)]*3,4)!=Q(19,1620))
 reject('three-point tail cannot prove strict reversal',Q(2,210)<iid(3,4))
 reject('double-counting regions would contradict small-n law',4*Q(1,105)>iid(2,4))
 for badn,badp in [(0,4),(3,3)]:
  try:data(badn,badp)
  except ValueError:adverse.append(f'domain rejection {badn},{badp}')
  else:raise RuntimeError('domain rejection inactive')
 if args.force_failure:require(False,'explicit forced failure remains active under -O')
 print(json.dumps({'status':'PASS','requirements':C,'method':'generic affine plane arrangement, convex-cell validation, triangle-simplex power integration','moments':moments,'fourth_cells':full,'tail_lower_bound_margins':tails,'adverse_controls':adverse,'universal_claims_require_written_proofs':True},indent=2,sort_keys=True))
if __name__=='__main__':main()
