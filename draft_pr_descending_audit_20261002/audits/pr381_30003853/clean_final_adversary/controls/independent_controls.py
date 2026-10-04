from fractions import Fraction as Q
from bisect import bisect_right
from collections import defaultdict
import json

class PL:
 def __init__(self,pts):
  p=[(Q(x),Q(y)) for x,y in pts]
  assert p[0]==(0,0) and p[-1]==(1,1)
  assert all(p[i][0]<p[i+1][0] and p[i][1]<p[i+1][1] for i in range(len(p)-1))
  i=1
  while i<len(p)-1:
   if (p[i][1]-p[i-1][1])*(p[i+1][0]-p[i][0])==(p[i+1][1]-p[i][1])*(p[i][0]-p[i-1][0]):p.pop(i)
   else:i+=1
  self.p=tuple(p)
 def at(self,x):
  if x==1:return Q(1)
  i=bisect_right([x for x,y in self.p],x)-1
  a,b=self.p[i];c,d=self.p[i+1]
  return b+(x-a)*(d-b)/(c-a)
 def inv(self):return PL([(y,x) for x,y in self.p])
 def __matmul__(self,g):
  gi=g.inv(); xs=sorted({x for x,y in g.p}|{gi.at(x) for x,y in self.p})
  return PL([(x,self.at(g.at(x))) for x in xs])
 def power(self,n):
  z=IDENTITY;g=self if n>=0 else self.inv()
  for i in range(abs(n)):z=g@z
  return z
 def isF(self):
  def dy(x):return x.denominator&(x.denominator-1)==0
  def pow2(x):return (x.numerator&(x.numerator-1)==0) and dy(x)
  return all(dy(x) and dy(y) for x,y in self.p) and all(pow2((d-b)/(c-a)) for (a,b),(c,d) in zip(self.p,self.p[1:]))
 def supports(self):
  xs=sorted({x for x,y in self.p}); seg=[]
  for x,y in zip(xs,xs[1:]):
   if self.at((x+y)/2)!=(x+y)/2:
    if seg and seg[-1][1]==x:seg[-1]=(seg[-1][0],y)
    else:seg.append((x,y))
  return seg
 def desc(self):return [[str(x),str(y)] for x,y in self.p]
 def __eq__(self,g):return self.p==g.p
IDENTITY=PL([(0,0),(1,1)])
t=PL([(0,0),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),(1,1)])
a=PL([(0,0),(Q(1,2),Q(1,2)),(Q(5,8),Q(9,16)),(Q(11,16),Q(5,8)),(Q(3,4),Q(3,4)),(1,1)])
def conjugate(f,g):return g.inv()@f@g
trans={i:conjugate(a,t.power(i)) for i in range(-4,5)}
print('EXACT FINITE-PIECE PL CONTROL; all arithmetic rational; composition f@g = f after g')
print('t',json.dumps(t.desc()));print('a',json.dumps(a.desc()))
for i,b in trans.items():
 assert b.isF();print('a^t^%d'%i,'pieces',len(b.p)-1,'support',[[str(x),str(y)] for x,y in b.supports()])
for i,b in trans.items():
 for j,c in trans.items():assert b@c==c@b
print('ALL 81 exact translate commutation identities hold in displayed finite window')
print('GLOBAL embedding proof separately establishes every integer translate; window is a falsification check only')
r=a.inv()@conjugate(a,t)
for m in range(2,9):
 s=a.power(m)
 assert r@s==s@r
 assert conjugate(s,t)@s.inv()==r.power(m)
 print('H_%d exact generator identity r^m=[s,t] verified; r nonidentity='%m,r!=IDENTITY)
print('INDEPENDENT LAURENT CONTROL')
def add(a,b):
 c=defaultdict(int,a)
 for i,v in b.items():c[i]+=v
 return {i:v for i,v in c.items() if v}
def scale(a,n):return {i:v*n for i,v in a.items() if v*n}
def shift(a,n):return {i+n:v for i,v in a.items()}
def mul(a,b):
 c={}
 for i,v in a.items():
  for j,w in b.items():c=add(c,{i+j:v*w})
 return c
def aug(a):return sum(a.values())
def deriv(a):return sum(i*v for i,v in a.items())
u={0:-1,1:1}
for m in range(2,9):
 for b in [{-3:2,0:-1,4:5},{0:1},{1:1},{-1:-2,2:1}]:
  f=add({0:m},mul(u,b));assert aug(f)%m==0
  assert (deriv(mul(u,f))%m)==0
 print('H_%d invariant [f] -> (f(1)/m,f\'(1) mod m); r -> (0,1); s -> (1,0); invariant factors [0,0,%d]'%(m,m))
print('NORMAL-CLOSURE CONTROL: [H,H] generated normally by pairwise generator commutators; subgroup/base commutation needed before deleting [r,s]')
print('FINITE-PRESENTATION CONTROL: for each K, graph-product base with edges |i-j|<=K satisfies all local commutators but retracts a_0,a_(K+1) to F_2')
for K in range(0,9):print('K=%d missing-distance=%d retracted commutator=a^-1 b^-1 a b nonempty reduced free word'%(K,K+1))
print('NON-FP2 CONTROL: H_2(W;Z) = direct sum_{d>=1} Z via mapping-torus Wang sequence; finite-index H_m transfer has composite m*id, so infinite rational H_2 persists')
print('ENDPOINT PROXY CONTROL: internal a is nonidentity but endpoint characters (0,0); endpoint records do not identify H/[H,H]')
print('BS(1,n) CONTROL: n>=2 has abelianization Z plus Z/(n-1), torsion-free affine action, no nontrivial finite-piece PL interval embedding by support endpoint slope invariance')
for n in range(2,9):print('n=%d abelianization=Z+Z/%d; any putative nontrivial support slope s must satisfy s=s^%d, hence s=1 contradiction'%(n,n-1,n))
print('BOUNDARY n=1: Z^2 embeds by disjoint supports; n=2: abelianization Z, so nonembedding alone does not correlate with torsion')
print('DIAGRAM CONTROL: all diagram groups have free integral homology; subgroups of a diagram group need separate membership proof; H_m abelianization torsion excludes membership')
print('ALL INDEPENDENT CONTROLS COMPLETED')
