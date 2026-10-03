#!/usr/bin/env python3
from fractions import Fraction as Q
import json,random
E=((Q(0),Q(0)),(Q(1),Q(1)))
def simplify(p):
 out=[]
 for z in p:
  out.append(z)
  while len(out)>=3:
   a,b,c=out[-3:]
   if (b[1]-a[1])*(c[0]-b[0])!=(c[1]-b[1])*(b[0]-a[0]):break
   out.pop(-2)
 return tuple(out)
def val(f,x):
 for (a,b),(c,d) in zip(f,f[1:]):
  if a<=x<=c:return b+(d-b)*(x-a)/(c-a)
 raise ValueError(x)
def inv(f):return tuple((y,x) for x,y in f)
def comp(f,g):
 gi=inv(g);xs={x for x,y in g}|{val(gi,x) for x,y in f}
 return simplify([(x,val(f,val(g,x))) for x in sorted(xs)])
def power(f,n):
 if n<0:return power(inv(f),-n)
 r=E
 for _ in range(n):r=comp(r,f)
 return r
def slope(f,left=True):
 a,b=f[:2] if left else f[-2:]
 return (b[1]-a[1])/(b[0]-a[0])
def bump(a,b):
 a,b=Q(a),Q(b);d=b-a
 pts=[(Q(0),Q(0))] if a>0 else []
 pts += [(a,a),(a+d/2,a+d/4),(a+3*d/4,a+d/2),(b,b)]
 if b<1:pts +=[(Q(1),Q(1))]
 return simplify(pts)
def support(f):
 cuts={x for x,y in f}
 for (a,b),(c,d) in zip(f,f[1:]):
  va,vb=b-a,d-c
  if va*vb<0:cuts.add(a+(c-a)*(-va)/(vb-va))
 cs=sorted(cuts);out=[]
 for a,b in zip(cs,cs[1:]):
  z=(a+b)/2
  if val(f,z)!=z:
   if out and out[-1][1]==a and val(f,a)!=a:out[-1]=(out[-1][0],b)
   else:out.append((a,b))
 return out
def run():
 n=0
 def ck(x):
  nonlocal n
  assert x;n+=1
 f=bump(0,1);a=bump(Q(1,4),Q(1,2));b=bump(Q(1,2),Q(3,4))
 rng=random.Random(3853);gs=[f,a,b,inv(f),inv(a),inv(b)];words=[E]
 for _ in range(160):
  w=E
  for _ in range(rng.randrange(1,9)):w=comp(w,rng.choice(gs))
  words.append(w)
 for w in words:
  ck(comp(w,inv(w))==E);ck(comp(inv(w),w)==E)
  for x in [Q(i,16) for i in range(17)]:ck(val(inv(w),val(w,x))==x)
  for g in gs:
   v=comp(w,g)
   ck(slope(v)==slope(w)*slope(g));ck(slope(v,False)==slope(w,False)*slope(g,False))
   c=comp(comp(comp(inv(w),inv(g)),w),g)
   ck(slope(c)==1);ck(slope(c,False)==1)
 for k in range(-12,13):
  t=power(f,k);c=comp(comp(inv(t),a),t)
  ck(support(c)==[(val(inv(t),Q(1,4)),val(inv(t),Q(1,2)))])
 ck(support(comp(a,b))==[(Q(1,4),Q(1,2)),(Q(1,2),Q(3,4))])
 ck(support(E)==[])
 return {'turn':4,'assertions':n,'word_samples':len(words),'scope':'exact rational PL diagnostics, conditional normality only'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
