#!/usr/bin/env python3
"""Rational controls for the focal polar reduction, not a sampled proof of periodicity."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json

checks=0;edges=0;angles=0
def ck(v):
 global checks
 assert v
 checks+=1
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(s,p):return (s*p[0],s*p[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def J(p):return (-p[1],p[0])
def pole(p,q):
 D=det(p,q)
 return ((q[1]-p[1])/D,(p[0]-q[0])/D)

positive=sorted(set(F(i,j) for i in range(1,9) for j in (1,2,4,8)))
params=[F(0)]+positive+[None]+[-t for t in reversed(positive)]
for a,b,c in [(5,3,4),(5,4,3),(13,5,12),(13,12,5),(17,8,15),(17,15,8)]:
 a,b,c=map(F,(a,b,c));ck(a*a-b*b==c*c)
 C=(c/(b*b),F(0));r=a/(b*b)
 P=[(-a,F(0)) if t is None else (a*(1-t*t)/(1+t*t),2*b*t/(1+t*t)) for t in params]
 p=[sub(v,(c,F(0))) for v in P]
 d=[a-c*v[0]/a for v in P]
 u=[mul(1/dd,v) for v,dd in zip(p,d)]
 for v,vv,dd,uu in zip(P,p,d,u):
  ck(v[0]**2/a**2+v[1]**2/b**2==1)
  ck(dd>0 and dot(vv,vv)==dd*dd)
  ck(dot(uu,uu)==1)
  ck(1-dot(C,vv)==r*dd)
  T=add(C,mul(r,uu));ck(dot(vv,T)==1)
 n=len(P)
 for step in range(1,8):
  for i in range(n):
   ids=[(i+h*step)%n for h in range(4)]
   if len(set(ids))<4:continue
   if not all(det(p[x],p[y])>0 and det(add(P[x],(c,F(0))),add(P[y],(c,F(0))))>0 for x,y in zip(ids,ids[1:])):continue
   Q=[]
   for x,y in zip(ids,ids[1:]):
    q=pole(p[x],p[y]);Q.append(q)
    ck(dot(q,p[x])==dot(q,p[y])==1)
    normal=(P[y][1]-P[x][1],P[x][0]-P[y][0]);h=dot(normal,P[x])
    lam=(a*a*normal[0]**2+b*b*normal[1]**2-h*h)/dot(normal,normal)
    ck(0<lam<b*b)
    ck((b*b-lam)*dot(q,q)-2*c*q[0]-1==0)
    cos=dot(u[x],u[y]);sin=det(u[x],u[y]);ck(sin>0 and cos*cos+sin*sin==1)
    T=add(C,mul(r,u[x]));ck(q==add(T,mul(r*sin/(1+cos),J(u[x]))))
    edges+=1
   x,y=ids[1:3]
   incoming=sub(Q[1],Q[0]);outgoing=sub(Q[2],Q[1])
   li=dot(incoming,J(u[x]));lo=dot(outgoing,J(u[y]))
   ck(li>0 and lo>0)
   ck(incoming==mul(li,J(u[x])) and outgoing==mul(lo,J(u[y])))
   ck(-dot(incoming,outgoing)/(li*lo)==-dot(u[x],u[y]))
   angles+=1

root=Path(__file__).resolve().parent
receipt={'status':'PASS','assertions':checks,'rational_local_edges':edges,'rational_local_angle_configurations':angles,'artifact_sha256':sha256((root/'SOURCE_STATUS.md').read_bytes()).hexdigest(),'scope':'Exact polar-coordinate, confocal tangency and ordinary-angle bridge controls; no assertion that arbitrary sampled chords are closed or share a caustic. All-N invariance uses the credited published bicentric theorem.'}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
