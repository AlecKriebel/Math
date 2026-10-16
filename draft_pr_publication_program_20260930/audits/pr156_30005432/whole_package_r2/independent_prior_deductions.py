#!/usr/bin/env python3
"""Independent reconstruction of July/September implications and source-map control."""
import itertools,json,sys
counts={}
def ck(ok,name):
 if not ok:raise RuntimeError(name)
 counts[name]=counts.get(name,0)+1
Q=range(16)
def bits(x):return [(x>>i)&1 for i in range(4)]
def label(a):return sum((a[i]%2)<<i for i in range(4))
def chi(x):
 a,b,c,d=bits(x);return(b+c+d+c*d)%2
def lf(x,y):
 a,b,c,d=bits(x);u,v,w,z=bits(y)
 return label([u+z*(b+c+d+c*d),v+d*w+z*(c+b*d),w+z*(b+c+c*d),z])
def cf(x,y):return x^lf(x,y)
for x,y in itertools.product(Q,repeat=2):
 ck(chi(cf(x,y))==(chi(x)+chi(y))%2,'July character')
 for z in Q:
  ck(cf(cf(x,y),z)==cf(x,cf(y,z)),'July finite associativity')
  ck(lf(x,y^z)==lf(x,y)^lf(x,z),'July lambda additive')
  ck(lf(cf(x,y),z)==lf(x,lf(y,z)),'July action')
K=[x for x in Q if chi(x)==0];ck(K==[0,1,6,7,10,11,14,15],'July kernel')
ck(6^10==12 and chi(12)==1,'July additive failure');ck(lf(8,6)==4 and chi(4)==1,'July lambda failure')
july=[]
for x,want in [(6,(2,2)),(10,(4,8))]:
 H=[g for g in Q if lf(x,g)==g];T=[g for g in Q if lf(g,x)==x and cf(g,x)==cf(x,g)]
 ck((16//len(H),16//len(T))==want,'July exact indices')
 for L,op in [(H,lambda a,b:a^b),(T,cf)]:ck(0 in L and all(op(a,b) in L for a,b in itertools.product(L,repeat=2)),'July subgroup')
 july.append({'witness':x,'indices':want,'H':H,'K':T})
# Generic Z-by-finite-factor proof: negative actor gives -2m and positive actor
# leaves only finitely many finite-factor values. This is written in derivation.
# MSTY: formal U-coordinate coefficient triples over F7, finite factor F3^2 x F3.
actors=list(itertools.product(range(3),repeat=3));V=[(1,0,0),(0,1,0),(0,0,1)];zero=((0,0,0),(0,0),0)
def vplus(a,b):return tuple((x+y)%7 for x,y in zip(a,b))
def vscl(k,a):return tuple(k*x%7 for x in a)
def beta(v,w):return(v[0]*w[1]-v[1]*w[0])%3
def vv(v,w):return tuple((a+b)%3 for a,b in zip(v,w))
def plus(a,b):return(vplus(a[0],b[0]),vv(a[1],b[1]),(a[2]+b[2]+beta(a[1],b[1]))%3)
def neg(a):return(vscl(-1,a[0]),tuple(-x%3 for x in a[1]),-a[2]%3)
def sub(a,b):return plus(a,neg(b))
def circ(a,b):return(vplus(a[0],vscl(pow(2,a[2],7),b[0])),vv(a[1],b[1]),(a[2]+b[2])%3)
def inv(a):return(vscl(-pow(2,(-a[2])%3,7),a[0]),tuple(-x%3 for x in a[1]),-a[2]%3)
def lam(a,b):return plus(neg(a),circ(a,b))
def star(a,b):return sub(lam(a,b),b)
for q,r,t in itertools.product(actors,repeat=3):
 a=(V[0],q[:2],q[2]);b=(V[1],r[:2],r[2]);e=(V[2],t[:2],t[2])
 ck(plus(plus(a,b),e)==plus(a,plus(b,e)),'MSTY formal additive associativity')
 ck(circ(circ(a,b),e)==circ(a,circ(b,e)),'MSTY formal circle associativity')
 ck(circ(a,plus(b,e))==plus(sub(circ(a,b),a),circ(a,e)),'MSTY formal brace law')
 ck(lam(a,b)==(vscl(pow(2,a[2],7),b[0]),b[1],(b[2]-beta(a[1],b[1]))%3),'MSTY formal lambda')
 ck(star(a,b)==(vscl(pow(2,a[2],7)-1,b[0]),(0,0),-beta(a[1],b[1])%3),'MSTY formal star')
 ck(circ(circ(b,a),inv(b))==(vplus(vscl(pow(2,b[2],7),a[0]),vscl(1-pow(2,a[2],7),b[0])),a[1],a[2]),'MSTY formal conjugation')
 ck(plus(plus(b,a),neg(b))==(a[0],a[1],(a[2]+2*beta(b[1],a[1]))%3),'MSTY formal additive conjugation')
msty=[]
for v in [(1,0),(0,1)]:
 x=((0,0,0),v,0);H=[];T=[]
 for w1,w2,t in actors:
  g=(V[1],(w1,w2),t)
  h=star(x,g)==zero and plus(x,g)==plus(g,x)
  k=star(g,x)==zero and circ(x,g)==circ(g,x)
  ck(h==(beta(v,(w1,w2))==0),'MSTY H witness')
  ck(k==(beta(v,(w1,w2))==0),'MSTY K witness')
  if h:H.append((w1,w2,t))
  if k:T.append((w1,w2,t))
 ck((27//len(H),27//len(T))==(3,3),'MSTY exact witness indices');msty.append({'v':v,'indices':[3,3]})
x=((0,0,0),(1,0),0);y=((0,0,0),(0,1),0);s=plus(x,y)
ck(s==((0,0,0),(1,1),1),'MSTY sum actor')
ck(star(s,(V[1],(0,0),0))[0]==V[1],'MSTY infinite injective coefficient')
ck(lam(y,x)[2]==1,'MSTY lambda failure')
# Independent finite source-map test; original B3 is global(S) because it is finite.
B=list(itertools.product(range(3),range(4)))
def eps(c):return 1 if c<2 else -1
def pb(a,b):return((a[0]+b[0])%3,(a[1]+b[1])%4)
def nb(a):return(-a[0]%3,-a[1]%4)
def cb(a,b):return((a[0]+eps(a[1])*b[0])%3,a[1]^b[1])
def sb(a,b):return pb(pb(nb(a),cb(a,b)),nb(b))
ann=[a for a in B if all(sb(a,b)==sb(b,a)==(0,0) and cb(a,b)==cb(b,a) for b in B)]
ck(ann==([(0,0),(1,0)] if '--corrupt-ann' in sys.argv else [(0,0)]),'source-map annihilator')
gens=[(1,0),(0,1)]
data=lambda b:tuple(sb(b,g) for g in gens)+tuple(sb(g,b) for g in gens)
ck(data((1,0))==data((0,0)),'source-map unequal annihilator cosets collide')
ck((1,0) not in ann,'source-map distinct cosets')
print(json.dumps({'status':'PASS_INDEPENDENT_PRIOR_DEDUCTIONS_AND_SOURCE_MAP','checks':sum(counts.values()),'categories':counts,'July':july,'MSTY':msty,'source_map_finite_Ann':ann,'universal_scope':'July group finite factor reconstructed from primary formulas; Z is not truncated. MSTY first coordinate is an arbitrary-U coefficient vector over F7, so equality certifies any F7-vector space. Infinity follows from independent basis vectors in the written derivation.'},indent=2))
