#!/usr/bin/env python3
"""Independent direct-geometry diagnostics, not interval or universal certificates."""
from math import gcd
import mpmath as m,json
m.mp.dps=85
count=0;cases=0;maxerror=m.mpf(0)
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
def difference(x,y):return [x[0]-y[0],x[1]-y[1]]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def signed(P):return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def projection(x,y,f):
 d=difference(y,x);q=dot(difference(f,x),d)/dot(d,d)
 return [x[0]+q*d[0],x[1]+q*d[1]]
def areas(P,a,b,k):
 normals=[[x/a**2,y/b**2] for x,y in P]
 vertices=[]
 for i,p in enumerate(normals):
  q=normals[(i+1)%len(P)];dd=cross(p,q)
  vertices.append([(q[1]-p[1])/dd,(p[0]-q[0])/dd])
 ans=[]
 for f in ([k,0],[-k,0]):
  ans.append([signed([projection(W[i],W[(i+1)%len(W)],f) for i in range(len(W))]) for W in [P,vertices]])
 return ans
for kk in [m.mpf('0.19'),m.mpf('0.61'),m.mpf('0.91')]:
 K=m.ellipk(kk*kk);kp=m.sqrt(1-kk*kk)
 for N in range(3,20):
  for turn in range(1,(N+1)//2):
   if gcd(N,turn)!=1:continue
   v=2*K*turn/N
   a=m.ellipfun('dn',v,kk*kk)/m.ellipfun('cn',v,kk*kk)
   b=kp/m.ellipfun('cn',v,kk*kk)
   reference=None
   for phi in [m.mpf('0.173'),m.mpf('0.527'),m.mpf('1.319')]:
    P=[[-a*m.ellipfun('sn',phi*K+2*i*v,kk*kk),b*m.ellipfun('cn',phi*K+2*i*v,kk*kk)] for i in range(N)]
    x=areas(P,a,b,kk)
    assert all(z>0 for pair in x for z in pair);count+=4
    error=abs(x[0][0]*x[1][1]-x[1][0]*x[0][1])/(1+abs(x[0][0]*x[1][1])+abs(x[1][0]*x[0][1]))
    assert error<m.mpf('1e-65');count+=1;maxerror=max(maxerror,error)
    C=x[0][1]/x[0][0]
    if reference is None:reference=C
    else:
     error=abs(C-reference)/(1+abs(C)+abs(reference));assert error<m.mpf('1e-65');count+=1;maxerror=max(maxerror,error)
    if phi==m.mpf('0.527'):
     z=areas(list(reversed(P)),a,b,kk)
     for i in range(2):
      for j in range(2):
       error=abs(x[i][j]+z[i][j])/(1+abs(x[i][j])+abs(z[i][j]));assert error<m.mpf('1e-65');count+=1;maxerror=max(maxerror,error)
    cases+=1
print(json.dumps({'status':'PASS','precision_decimal_digits':m.mp.dps,'diagnostic_checks':count,'real_cases':cases,'least_periods':[3,19], 'moduli':['0.19','0.61','0.91'],'max_relative_error':m.nstr(maxerror,15),'scope':'New direct chord/tangent-intersection/Euclidean-foot computations, including stars and reversal. No author code imported. Diagnostics are not universal or interval proofs.'},indent=2))
