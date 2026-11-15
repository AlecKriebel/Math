#!/usr/bin/env python3
"""Bounded NONINTERVAL diagnostics, independently coded; no source imports."""
import mpmath as m
from collections import Counter
import json,sys
sys.dont_write_bytecode=True;m.mp.dps=90;counts=Counter();worst=m.mpf(0)
def ck(t,name):
 counts[name]+=1
 if not t:raise RuntimeError(name)
def near(x,y,name,tol=m.mpf('1e-50')):
 global worst
 e=abs(x-y)/(1+abs(x)+abs(y));worst=max(worst,e);ck(e<tol,name)
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def foot(F,n,h=1):
 t=(h-dot(n,F))/dot(n,n);return F[0]+t*n[0],F[1]+t*n[1]
def main():
 ck(len(sys.argv)==1,'no overrides');families=0;realphases=0
 for ks in ['0.2','0.75']:
  k=m.mpf(ks);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);Kp=m.ellipk(1-k*k)
  def scd(u):return tuple(m.ellipfun(x,u,k*k) for x in ['sn','cn','dn'])
  for N,tau in [(3,1),(4,1),(5,2),(7,3),(10,3)]:
   v=2*K*tau/N;d=2*v;sv,cv,dv=scd(v);a=dv/cv;b=kp/cv;L=4*K/N
   def q(u):
    S,C,_=scd(u);return (k-S)/(1-k*S),kp*C/(1-k*S)
   def Q(u):
    S,C,_=scd(u);return a*(k-a*S)/(a-k*S),a*b*C/(a-k*S)
   def traces(w):return area([q(w+v+j*d) for j in range(N)]),area([Q(w+j*d) for j in range(N)])
   mult=[]
   for w in [K/13,4*K/7]:
    P=[(-a*S,b*C) for S,C,_ in [scd(w+j*d) for j in range(N)]];norm=[(x/(a*a),y/(b*b)) for x,y in P]
    tangentvertices=[]
    for j,n in enumerate(norm):
     nn=norm[(j+1)%N];dd=det(n,nn);ck(dd>0,'all star tangent increments positive');tangentvertices.append(((nn[1]-n[1])/dd,(n[0]-nn[0])/dd))
    aa=[];bb=[]
    for sign in [1,-1]:
     F=(sign*k,0);chord=[]
     for j,p in enumerate(P):
      edge=sub(P[(j+1)%N],p);n=(-edge[1],edge[0]);h=dot(n,p);chord.append(foot(F,n,h))
     af=area(chord);bf=area([foot(F,n) for n in norm]);ck(af>0 and bf>0,'both focal signed areas positive')
     expected=traces(w+(0 if sign==1 else 2*K));near(af,expected[0],'actual chord feet equal midpoint trace');near(bf,expected[1],'actual tangent feet equal trace')
     outer=[]
     for j,p in enumerate(tangentvertices):
      edge=sub(tangentvertices[(j+1)%N],p);n=(-edge[1],edge[0]);outer.append(foot(F,n,dot(n,p)))
     near(bf,area(outer),'actual outer polygon side agreement');aa.append(af);bb.append(bf)
    near(aa[0]*bb[1],aa[1]*bb[0],'common focal ratio equality');mult.extend([bb[j]/aa[j] for j in range(2)]);realphases+=1
   for c in mult[1:]:near(c,mult[0],'same phase-independent multiplier at both foci')
   w=K/7+m.j*Kp/5;A,B=traces(w);At,Bt=traces(w+L);Aa,Ba=traces(w+2*m.j*Kp)
   near(A,At,'complex reduced real period original');near(B,Bt,'complex reduced real period outer');near(A,-Aa,'complex imaginary antiperiod original');near(B,-Ba,'complex imaginary antiperiod outer');near(B,mult[0]*A,'complex multiplier agreement')
   pole=K-v+m.j*Kp;eps1=m.mpf('1e-12');eps2=m.mpf('1e-16');A1,B1=traces(pole+eps1);A2,B2=traces(pole+eps2)
   near(eps1*A1,eps2*A2,'simple original pole finite diagnostic',m.mpf('1e-9'));near(eps1*B1,eps2*B2,'simple outer pole finite diagnostic',m.mpf('1e-9'));near(B2,mult[0]*A2,'near-pole multiplier agreement',m.mpf('1e-40'));families+=1
 print(json.dumps({'assessment':'BOUNDED_COMPLEX_AND_DIRECT_PROJECTION_DIAGNOSTICS_AGREE','precision_digits':m.mp.dps,'families':families,'real_phases':realphases,'checks':dict(sorted(counts.items())),'total_checks':sum(counts.values()),'maximum_normalized_discrepancy':m.nstr(worst,16),'scope':'Finite high-precision NONINTERVAL diagnostics only; no certified error bound or universal theorem follows from these samples.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
