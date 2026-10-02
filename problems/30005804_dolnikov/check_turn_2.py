from exact_geometry import *
from itertools import combinations
import json
c=0;tested=0;stripsets=0

def ck(x):
 global c
 c+=1;assert x

def hull(P):
 P=sorted(set(P))
 def chain(P):
  C=[]
  for p in P:
   while len(C)>=2 and cross(sub(C[-1],C[-2]),sub(p,C[-1]))<=0:C.pop()
   C.append(p)
  return C
 return chain(P)[:-1]+chain(P[::-1])[:-1]
def section(P,y):
 xs=[]
 for a,b in zip(P,P[1:]+P[:1]):
  if a[1]==b[1]:
   if y==a[1]:xs.extend([a[0],b[0]])
  elif min(a[1],b[1])<=y<=max(a[1],b[1]):xs.append(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
 return (min(xs),max(xs)) if xs else None
shapes=[[(0,0),(2,0),(0,2)],[(0,0),(3,0),(2,2),(0,1)],[(0,0),(2,0),(3,1),(1,3),(0,2)],[(0,0),(2,0),(2,2),(0,2)]]
records=[]
for raw in shapes:
 K=list(map(pt,raw));D=hull([sub(a,b) for a in K for b in K]);ell=section(D,F(0))[1]
 lower=max((ell-x)/y for x,y in D if y<0);upper=min((ell-x)/y for x,y in D if y>0);ck(lower<=upper);beta=(lower+upper)/2
 phi=lambda p:p[0]+beta*p[1]
 ck(all(abs(phi(p))<=ell for p in D))
 L=hull([(-x,-y) for x,y in K]);best=max(((section(L,y)[1]-section(L,y)[0],y) for y in {p[1] for p in L}));ck(best[0]==ell)
 y=best[1];lo,hi=section(L,y);z=tuple(sum(p[j] for p in L)/len(L) for j in range(2));a=tuple(z[j]+F(3,4)*(pt((lo,y))[j]-z[j]) for j in range(2));bb=tuple(z[j]+F(3,4)*(pt((hi,y))[j]-z[j]) for j in range(2));v=(-beta,F(1))
 limits=[]
 for u,w in zip(L,L[1:]+L[:1]):
  edge=sub(w,u);den=abs(cross(edge,v))
  for p in (a,bb):
   slack=cross(edge,sub(p,u));ck(slack>0)
   if den:limits.append(slack/den)
 t=min(limits)/2;b=2*t;width=F(3,4)*ell
 P=[(a[0]-t*v[0],a[1]-t),(bb[0]-t*v[0],bb[1]-t),(bb[0]+t*v[0],bb[1]+t),(a[0]+t*v[0],a[1]+t)]
 ck(all(inside(p,L) for p in P));ck(max(map(phi,P))-min(map(phi,P))==width);ck(max(y for x,y in P)-min(y for x,y in P)==b)
 for h in range(-6,7):
  Y=F(h,6)*max(y for x,y in D);T=[]
  for y in [Y,Y+b/2,Y+b]:
   interval=section(D,y)
   if interval:
    low,high=interval
    T.extend((low+(high-low)*F(i,20),y) for i in range(21))
  if not T:continue
  stripsets+=1;x0=min(map(phi,T));y0=min(y for x,y in T);pmin=min(map(phi,P));pbot=min(y for x,y in P)
  Q=[]
  for j in range(3):
   qy=y0-pbot;qphi=x0+j*width-pmin;Q.append((qphi-beta*qy,qy))
  for center in T:ck(any(inside(sub(q,center),K) for q in Q));tested+=1
 for den in range(1,5):
  coords=[ell*F(i,den) for i in range(-3,4)]
  polys=[[(x+u,y) for x,y in K] for u in coords];cv=masks(polys)
  for S in range(1,1<<7):
   xs=[coords[i] for i in range(7) if S>>i&1];greedy=0
   while xs:
    cutoff=xs[0]+ell;xs=[x for x in xs if x>cutoff];greedy+=1
   ck(greedy==min_cover(S,cv))
 records.append({'vertices':len(K),'ell':str(ell),'beta':str(beta),'strip_width':str(b)})
print(json.dumps({'assertions':c,'verified_strip_incidences':tested,'strip_point_sets':stripsets,'polygon_parameters':records,'scope':'Exact rational constructions and finite controls; all-size strip theorem is proved in text'},indent=2,sort_keys=True))
