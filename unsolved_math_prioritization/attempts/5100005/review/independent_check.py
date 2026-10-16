#!/usr/bin/env python3
"""Independent exact k111 audit; contacts recovered as double roots on chords.
This does not use the author's polarity-map formula to construct the contacts.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
count=0
def ok(x):
 global count
 assert x
 count+=1

def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def mul(k,p):return tuple(k*x for x in p)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def norm(p):
 a=dot(p,p);n=isqrt(a.numerator);d=isqrt(a.denominator);ok(n*n==a.numerator and d*d==a.denominator);return F(n,d)
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
squared_outer=(F(16),F(9));squared_inner=(F(256,25),F(81,25))
diamond=[(F(4),F(0)),(F(0),F(3)),(F(-4),F(0)),(F(0),F(-3))]
rectangle=[(F(16,5),F(9,5)),(-F(16,5),F(9,5)),(-F(16,5),-F(9,5)),(F(16,5),-F(9,5))]
results=[]
for p in [diamond,rectangle]:
 q=[];t=[];vel=[]
 ok(len(set(p))==4)
 for i,x in enumerate(p):
  y=p[(i+1)%4];v=sub(y,x)
  ok(sum(x[j]**2/squared_outer[j] for j in range(2))==1)
  aa=sum(v[j]**2/squared_inner[j] for j in range(2))
  bb=2*sum(x[j]*v[j]/squared_inner[j] for j in range(2))
  cc=sum(x[j]**2/squared_inner[j] for j in range(2))-1
  ok(aa>0 and bb*bb-4*aa*cc==0)
  contact_t=-bb/(2*aa);ok(0<contact_t<1);z=add(x,mul(contact_t,v));q.append(z)
  ok(sum(z[j]**2/squared_inner[j] for j in range(2))==1)
  n=tuple(x[j]/squared_outer[j] for j in range(2));m=tuple(y[j]/squared_outer[j] for j in range(2));den=cross(n,m);ok(den!=0)
  w=((m[1]-n[1])/den,(n[0]-m[0])/den);t.append(w)
  ok(dot(n,w)==dot(m,w)==1)
  ok(z==(F(16,25)*w[0],F(9,25)*w[1]))
  vel.append(mul(1/norm(v),v))
 for i in range(4):
  n=tuple(p[i][j]/squared_outer[j] for j in range(2));incoming=vel[i-1]
  reflected=sub(incoming,mul(2*dot(incoming,n)/dot(n,n),n));ok(reflected==vel[i])
 ap=area(t);app=area(q);a=area(p);ok(a>0 and ap>0 and app>0)
 ok(app==F(144,625)*ap)
 for k in range(4):
  ok(area(t[k:]+t[:k])==ap);ok(area(q[k:]+q[:k])==app)
 ok(area(list(reversed(t)))*area(list(reversed(q)))==ap*app)
 results.append({'A':str(a),'Aprime':str(ap),'Asecond':str(app),'product':str(ap*app),'contact_points':[[str(z) for z in x] for x in q]})
x,y=map(lambda r:F(r['product']),results);ok(x==F(331776,625));ok(y==576);ok(y-x==F(28224,625));ok(x!=y)
ok(F(results[0]['A'])*F(results[0]['Asecond'])==F(results[1]['A'])*F(results[1]['Asecond'])==F(165888,625))
r={'status':'PASS','exact_assertions':count,'construction':'Caustic contacts independently reconstructed as double roots of the edge-parameter quadratic','results':results,'difference':str(y-x),'limits':'Exact checks of two previously known primitive four-period witnesses. General family membership also checked analytically against the pinned PR147 proof. No new discovery claimed.'}
print(json.dumps(r,indent=2));Path(__file__).with_name('independent_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
