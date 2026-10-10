#!/usr/bin/env python3
"""Author exploratory numerical probe; not a proof certificate."""
import mpmath as mp
mp.mp.dps=50
m=mp.mpf('0.6');par=m*m;ac=mp.mpf(1);bc=mp.sqrt(1-par);K=mp.ellipk(par)
def sn(u):return mp.ellipfun('sn',u,par)
def cn(u):return mp.ellipfun('cn',u,par)
def dn(u):return mp.ellipfun('dn',u,par)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
for N in [3,4,5,6,7,8,9,10,12]:
 s=2*K/N;a=ac*dn(s)/cn(s);b=bc/cn(s);vals=[]
 for phase in ['0.017','0.137','0.371','0.777']:
  u=mp.mpf(phase)*4*K;P=[(-a*sn(u+2*i*s),b*cn(u+2*i*s)) for i in range(N)];norm=[(x/a**2,y/b**2) for x,y in P]
  outer=[];pedal=[]
  for i,n in enumerate(norm):
   nn=norm[(i+1)%N];d=det(n,nn)
   outer.append(((nn[1]-n[1])/d,(n[0]-nn[0])/d));pedal.append((n[0]/(n[0]**2+n[1]**2),n[1]/(n[0]**2+n[1]**2)))
  vals.append(area(outer)*area(pedal))
 print(N,[mp.nstr(v,20) for v in vals], 'relative_range',mp.nstr((max(vals)-min(vals))/max(map(abs,vals)),7))
