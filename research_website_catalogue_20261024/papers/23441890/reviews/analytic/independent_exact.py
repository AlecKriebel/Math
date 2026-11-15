#!/usr/bin/env python3
"""Read-only exact finite construction diagnostics; no deposited-code imports.
Canonical piecewise-affine maps are composed on all pieces, not merely sampled.
Infinite components, perfectness and arbitrary embeddings require the proof.
"""
from fractions import Fraction as F
from bisect import bisect_right
from pathlib import Path
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
counts=Counter();negative=[]
def ck(t,label):
 counts[label]+=1
 if not t:raise RuntimeError(label)
def p2(k):return F(2**k) if k>=0 else F(1,2**(-k))
def isdyadicpower(r):
 def power2(n):return n>0 and n&(n-1)==0
 return r>0 and power2(r.numerator) and power2(r.denominator)
class PL:
 def __init__(self,xy):
  a=[(F(x),F(y)) for x,y in xy];ck(len(a)>=2,'PL input has endpoints')
  ck(all(x<X and y<Y for (x,y),(X,Y) in zip(a,a[1:])),'PL strictly increasing')
  ck(a[0][0]==a[0][1] and a[-1][0]==a[-1][1],'PL outer endpoints fixed')
  out=[]
  for z in a:
   out.append(z)
   while len(out)>=3:
    (x,y),(X,Y),(u,v)=out[-3:]
    if (Y-y)*(u-X)!=(v-Y)*(X-x):break
    out.pop(-2)
  self.xy=tuple(out);self.x=tuple(x for x,y in out)
 def __call__(self,x):
  x=F(x)
  if x<=self.x[0] or x>=self.x[-1]:return x
  i=bisect_right(self.x,x)-1;(a,b),(c,d)=self.xy[i:i+2]
  return b+(d-b)*(x-a)/(c-a)
 def inverse(self):return PL([(y,x) for x,y in self.xy])
 def compose(self,g):
  gi=g.inverse();knots=sorted(set(g.x)|{gi(x) for x in self.x})
  return PL([(x,self(g(x))) for x in knots])
 def same(self,g):return self.xy==g.xy
 def power(self,n):
  b=self if n>=0 else self.inverse();ans=identity()
  for _ in range(abs(n)):ans=b.compose(ans)
  return ans
 def slopes(self):return [(Y-y)/(X-x) for (x,y),(X,Y) in zip(self.xy,self.xy[1:])]
 def support(self):
  intervals=[]
  for (x,y),(X,Y) in zip(self.xy,self.xy[1:]):
   a,b=y-x,Y-X
   if a==b==0:continue
   pts=[x,X]
   if a*b<0:pts.insert(1,x-a*(X-x)/(b-a))
   for u,v in zip(pts,pts[1:]):
    if self((u+v)/2)==(u+v)/2:continue
    if intervals and intervals[-1][1]==u and self(u)!=u:intervals[-1]=(intervals[-1][0],v)
    else:intervals.append((u,v))
  return intervals
 def first_germ(self):
  a=self.support()[0][0];i=bisect_right(self.x,a)-1;(x,y),(X,Y)=self.xy[i:i+2]
  return a,(Y-y)/(X-x)
def identity():return PL([(0,0),(1,1)])
def bump(a,b):
 a,b=F(a),F(b);d=b-a
 return PL([(0,0),(a,a),(a+d/3,a+2*d/3),(b,b),(1,1)])
def split(x,X,y,Y):
 # Independent dual algorithm: bracket target ratio from ABOVE, permitting
 # zero lower-piece length at exact upper powers, then omit zero pieces.
 ratio=(Y-y)/(X-x);up=F(1)
 while up<ratio:up*=2
 while up/2>=ratio:up/=2
 lo=up/2;length=(X-x)*(up-ratio)/(up-lo)
 rows=[(x,y)]
 if length:rows.append((x+length,y+lo*length))
 rows.append((X,Y));return rows
def interpolate(xs,ys):
 xs=list(map(F,xs));ys=list(map(F,ys));c=min(xs+ys)/3;d=(max(xs+ys)+2)/3
 a,b=[c]+xs+[d],[c]+ys+[d];out=[(F(0),F(0)),(c,c)]
 for x,X,y,Y in zip(a,a[1:],b,b[1:]):out.extend(split(x,X,y,Y)[1:])
 out.append((F(1),F(1)));return PL(out)
def alpha(h,f):return h.inverse().compose(f.compose(h))
def chart(n,f):
 left=-p2(-n);width=p2(-n-1)
 return [(left+width*x,left+width*y) for x,y in f.xy]
def main():
 ck(len(sys.argv)==1,'no overrides')
 root=Path(__file__).resolve().parents[2]
 for name,d in {'sources/SOURCE_READY.json':'61f1a6961c0255fd94bc9789fb468b7baded2a37f988ef0b3000a272306b77cf','sources/paper.pdf':'e4f442fada2f0203678eb5344ce420875947cca02506b2c19df255947e614fe7','sources/published-source/kourovka-21-149/main.tex':'edb1b5751a57f51477efd03cb3a6b5fb4f6485d7a51c3234f064ccac819bcd57','reviews/analytic/INITIAL_SEAL.json':'3eb58109fb69edb448cbaaa69d96d3ac574a7f0ced867e6a1d1458ea3e2b3611'}.items():ck(hashlib.sha256((root/name).read_bytes()).hexdigest()==d,'exact source binding')
 ratios=[F(p,q) for p in range(1,18) for q in range(1,20)]+[p2(k) for k in range(-40,41)]
 for r in ratios:
  xy=split(F(2,7),F(11,7),F(-4,9),F(-4,9)+r*F(9,7))
  ck(xy[0]==(F(2,7),F(-4,9)) and xy[-1][1]==F(-4,9)+r*F(9,7),'segment endpoints')
  ss=[(Y-y)/(X-x) for (x,y),(X,Y) in zip(xy,xy[1:])]
  ck(all(isdyadicpower(s) for s in ss),'segment dyadic slopes')
 tuples=[([F(1,9),F(2,9),F(5,9),F(7,9)],[F(1,17),F(9,17),F(12,17),F(16,17)]),([F(1,10000),F(1,3),F(3,5),F(9999,10000)],[F(1,13),F(3,13),F(9,13),F(12,13)])]
 maps=[]
 for xs,ys in tuples:
  for a,b in [(xs,ys),(ys,xs)]:
   f=interpolate(a,b);maps.append(f)
   ck(all(f(x)==y for x,y in zip(a,b)),'all prescribed tuple coordinates')
   ck(all(isdyadicpower(s) for s in f.slopes()),'full tuple-map slopes')
   ck(f.inverse().compose(f).same(identity()),'full-piece inverse identity')
 for m in range(48):
  b=p2(-2*m-2);a=b/2
  for u,v in [(a,b),(1-b,1-a)]:
   h=bump(u,v);d=v-u;f=bump(u+d/3,u+d/2);af=alpha(h,f)
   ck(h.support()==[(u,v)] and h.first_germ()[1]==2,'exact bump support and first germ')
   ck(af.support()==[(h.inverse()(u+d/3),h.inverse()(u+d/2))],'conjugated full support preimage')
   ck(af.first_germ()[1]==f.first_germ()[1],'conjugated earliest slope')
   ck(not af.same(f) and af.support()[0][1]<f.support()[0][0],'local nonidentity via disjoint support')
   ck(alpha(h.inverse(),af).same(f),'full-piece conjugation inverse')
  ck(p2(-2*(m+1)-2)<a,'left-tail strict gap')
  ck(1-a<1-p2(-2*(m+1)-2),'right-tail strict gap')
 # Positive cone and homomorphism identities on exact full PL maps.
 fs=[bump(F(1,8),F(3,8)),bump(F(1,4),F(3,4)),bump(F(1,8),F(7,8))]
 h=bump(F(1,10),F(9,10))
 for f in fs:
  for g in fs:
   fg=f.compose(g)
   ck(fg.first_germ()[1]>1,'positive-cone product first slope')
   ck(alpha(h,fg).same(alpha(h,f).compose(alpha(h,g))),'full-piece automorphism multiplication')
   ck(f.inverse().first_germ()[1]==1/f.first_germ()[1],'inverse earliest slope reciprocal')
 # Bilateral shift diagram on whole finite-piece cell maps, positive/negative n.
 f=bump(F(2,5),F(3,5));beta_f=alpha(h,f)
 for n in range(-7,8):
  hn=h.power(n);hn1=h.power(n+1)
  left=chart(n,alpha(hn,beta_f))
  right=[(2*x,2*y) for x,y in chart(n+1,alpha(hn1,f))]
  ck(left==right,'exact bilateral next-cell conjugation diagram')
  ck(-p2(-n)/2==-p2(-(n+1)),'cell left endpoint halving')
 # Deliberately false generic construction identities.
 tests={
  'wrong conjugation direction':not alpha(h,f).same(alpha(h.inverse(),f)),
  'wrong bilateral beta index':not alpha(h.power(2),f).same(alpha(h.power(1),f)),
  'bump formulas meet with wrong slope':F(1,3)*2 != F(1)+F(2)*(F(1,3)-1),
  'right-only tail claimed descending':not (1-F(1,16)<1-F(1,4)),
  'uncancelled conjugating germ':F(3,2)*F(2)!=F(2),
 }
 for name,ok in tests.items():ck(ok,'false-identity rejection');negative.append(name)
 def mul(a,b):return a[0]*b[0],a[0]*b[1]+a[1]
 def inv(a):return 1/a[0],-a[1]/a[0]
 def comm(a,b):return mul(mul(mul(inv(a),inv(b)),a),b)
 for s in [F(1,3),F(2),F(5,2)]:
  for t in [F(-7,3),F(0),F(11,5)]:
   for u in [F(1,4),F(3),F(7,2)]:
    c=comm((s,t),(u,F(1,7)));d=comm((u,F(2,9)),(s,F(-3,4)))
    ck(c[0]==d[0]==1 and comm(c,d)==(1,0),'affine derived group abelian')
 print(json.dumps({'assessment':'INDEPENDENT_EXACT_FINITE_CONSTRUCTIONS_SUPPORTED','checks':dict(sorted(counts.items())),'total_controls':sum(counts.values()),'false_identities_rejected':negative,'scope':'Finite exact PL whole-piece identities only; independent handwritten proof handles all infinite/universal assertions. No source code import or file write.','optimized':not __debug__},sort_keys=True,indent=2))
if __name__=='__main__':main()
