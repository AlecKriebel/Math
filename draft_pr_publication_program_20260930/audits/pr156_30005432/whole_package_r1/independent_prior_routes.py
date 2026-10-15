"""Independent verification of the two prior-construction deductions cited in the package."""
from itertools import product
from pathlib import Path
import json
P=Path(__file__).resolve().parent
def ck(c,m):
 if not c:raise RuntimeError(m)
F=list(product(range(2),repeat=4))
def ap(x,y):return tuple(a^b for a,b in zip(x,y))
def chi(x):
 a,b,c,d=x;return b^c^d^(c*d)
def lf(x,y):
 a,b,c,d=x;u,v,w,z=y
 return u^(z*chi(x)),v^(d*w)^(z*(c^(b*d))),w^(z*(b^c^(c*d))),z

def cf(x,y):return ap(x,lf(x,y))
def sf(x,y):return ap(lf(x,y),y)
zero=(0,0,0,0);count=0
for x,y,z in product(F,repeat=3):
 ck(cf(cf(x,y),z)==cf(x,cf(y,z)),'July finite associativity')
 ck(lf(cf(x,y),z)==lf(x,lf(y,z)),'July lambda homomorphism')
 count+=2
for x,y in product(F,repeat=2):
 ck(chi(cf(x,y))==chi(x)^chi(y),'July character');count+=1
labels=lambda x:x[0]+2*x[1]+4*x[2]+8*x[3]
K={labels(x) for x in F if chi(x)==0}
ck(K=={0,1,6,7,10,11,14,15},'July exact finite kernel')
results=[]
for label in (6,10,12):
 x=next(v for v in F if labels(v)==label)
 H=[v for v in F if sf(x,v)==zero]
 T=[v for v in F if sf(v,x)==zero and cf(v,x)==cf(x,v)]
 results.append({'label':label,'H_order':len(H),'K_order':len(T),'sign':(-1)**chi(x),'indices':[16//len(H),16//len(T)] if chi(x)==0 else ['infinite','infinite']})
ck(results[0]['indices']==[2,2] and results[1]['indices']==[4,8] and results[2]['sign']==-1,'July witness indices')
x6=next(x for x in F if labels(x)==6);x10=next(x for x in F if labels(x)==10);x8=next(x for x in F if labels(x)==8)
ck(labels(ap(x6,x10))==12 and labels(lf(x8,x6))==4,'July closure and lambda obstruction')
# MSTY: exact formal coefficients for an arbitrary F7-vector space U.
# Every U-coordinate is a formal linear combination of three independent U variables.
def up(a,b):return tuple((x+y)%7 for x,y in zip(a,b))
def us(k,a):return tuple(k*x%7 for x in a)
def beta(v,w):return (v[0]*w[1]-v[1]*w[0])%3
def vp(v,w):return tuple((a+b)%3 for a,b in zip(v,w))
def uneg(v):return tuple(-a%3 for a in v)
V=list(product(range(3),repeat=2));actors=list(product(V,range(3)))
Uvars=[tuple(int(i==j) for i in range(3)) for j in range(3)]
def ba(x,y):
 u,v,z=x;a,w,t=y
 return up(u,a),vp(v,w),(z+t+beta(v,w))%3

def bn(x):return us(-1,x[0]),uneg(x[1]),-x[2]%3

def bc(x,y):
 u,v,z=x;a,w,t=y
 return up(u,us(pow(2,z,7),a)),vp(v,w),(z+t)%3

def bi(x):return us(-pow(pow(2,x[2],7),-1,7),x[0]),uneg(x[1]),-x[2]%3

def bl(x,y):return ba(bn(x),bc(x,y))
def bs(x,y):return ba(bl(x,y),bn(y))
for a,b,c in product(actors,repeat=3):
 x=(Uvars[0],*a);y=(Uvars[1],*b);z=(Uvars[2],*c)
 ck(ba(ba(x,y),z)==ba(x,ba(y,z)),'MSTY universal additive associativity')
 ck(bc(bc(x,y),z)==bc(x,bc(y,z)),'MSTY universal circle associativity')
 ck(bc(x,ba(y,z))==ba(ba(bc(x,y),bn(x)),bc(x,z)),'MSTY universal brace identity')
 count+=3
for a,b in product(actors,repeat=2):
 x=(Uvars[0],*a);g=(Uvars[1],*b)
 ck(bs(x,g)==(us(pow(2,x[2],7)-1,Uvars[1]),(0,0),-beta(x[1],g[1])%3),'MSTY universal right star')
 ck(bc(bc(g,x),bi(g))==(up(us(pow(2,g[2],7),Uvars[0]),us(1-pow(2,x[2],7),Uvars[1])),x[1],x[2]),'MSTY universal conjugation')
 count+=2
ck(pow(2,1,7)-1!=0 and pow(2,2,7)-1!=0,'MSTY nonzero scalar automorphisms')
x=((0,0,0),(1,0),0);y=((0,0,0),(0,1),0)
ck(ba(x,y)[2]==1,'MSTY additive failure actor')
# At actor z=0, all four relevant families vary only over finite actor/scalar choices.
# At z=1,2, (2^z-1) acts injectively on an infinite F7-vector space, giving distinct basis cosets.
for z in (x,y):
 H=[a for a in actors if beta(z[1],a[0])==0]
 ck(len(H)==9,'MSTY witness actor subgroup order')
 ck(all(bc(z,((0,0,0),*a))==bc(((0,0,0),*a),z) for a in H),'MSTY witness circle centrality')
result={'status':'PASS_PRIOR_DEDUCTION_AUDIT','checks':count,'July_finite_kernel':sorted(K),'July_indices':results,'MSTY_witness_indices':[3,3],'MSTY_infinite_certificate':'Choose independent basis vectors e_j of U=direct sum F7. For actor z=1,2, (2^z-1)e_j are distinct because the scalar is nonzero. Exact star/conjugation coefficients were compared for all finite actor triples, independent of dimension of U.','scope':'These are independently derived infinite variations, not statements printed as property-(s) counterexamples in the prior sources.'}
(P/'INDEPENDENT_PRIOR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':count,'July_indices':results},indent=2))
