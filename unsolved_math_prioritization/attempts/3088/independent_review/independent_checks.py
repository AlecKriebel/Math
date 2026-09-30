"""Independent exact certificate and elementary-identity controls for 3088."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
from collections import Counter
import json,math,hashlib
P=Path(__file__).parent; data=json.loads((P/'author_replay/finite_coloring.json').read_text())
V=[tuple(v) for v in data['vectors']];colors=data['colors'];checks=0;families={}
def check(v,name):
 global checks
 assert v,name
 checks+=1;families[name]=families.get(name,0)+1
def ray(v):
 first=next(x for x in v if x)
 return tuple(F(x,first) for x in v)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
# Regenerate projective classes by rational affine normalization rather than gcd
# filtering and primitive sign conventions used by the submitted verifier.
all_rays={ray(v) for v in product(range(-3,4),repeat=3) if any(v)}
check({ray(v) for v in V}==all_rays and len(V)==len(all_rays)==145,'independent grid generation')
check(len(colors)==len(V) and set(colors)=={0,1,2,3},'four nonempty colors')
G=[[dot(v,w) for w in V] for v in V]
monochromatic=0
for color in range(4):
 indices=[i for i,c in enumerate(colors) if c==color]
 for i,j,k in combinations(indices,3):
  check(G[i][j]*G[j][k]*G[k][i]>=0,'independent monochromatic triple')
  monochromatic+=1
negative=sum(G[i][j]*G[j][k]*G[k][i]<0 for i,j,k in combinations(range(145),3))
check(negative==125614,'all negative hyperedges recounted')
A=[(1,1,0),(1,-1,0),(1,0,1),(1,0,-1)]
check(all(colors[V.index(v)]==0 for v in A),'prescribed witness color')
H=[[dot(v,w) for w in A] for v in A]
check(H==[[2,0,1,1],[0,2,1,1],[1,1,2,0],[1,1,0,2]],'witness Gram matrix')
for triple in combinations(range(4),3):
 i,j,k=triple; val=H[i][j]*H[j][k]*H[k][i]
 for signs in product([-1,1],repeat=3):
  a,b,c=signs
  check((a*b*H[i][j])*(a*c*H[i][k])*(b*c*H[j][k])==val>=0,'representative sign invariance')
# Every sign assignment that makes all witness pair-products nonnegative is global.
consistent=[]
for sig in product([-1,1],repeat=4):
 if all(sig[i]*sig[j]*H[i][j]>=0 for i,j in combinations(range(4),2)):consistent.append(sig)
check(consistent==[(-1,-1,-1,-1),(1,1,1,1)],'global sign forced')
# Exhaust all nonempty support patterns in three coordinates. The needed two
# orthogonal pairs and four positive cross-pairs cannot coexist.
support_patterns=0;feasible=[]
for a,b,c,d in product(range(1,8),repeat=4):
 support_patterns+=1
 if a&b==0 and c&d==0 and all(x&y for x,y in [(a,c),(a,d),(b,c),(b,d)]):feasible.append((a,b,c,d))
check(not feasible,'support obstruction in dimension three')
a,b,c,d=3,12,5,10
check(a&b==0 and c&d==0 and all(x&y for x,y in [(a,c),(a,d),(b,c),(b,d)]),'four-coordinate control')
# Interior-point perpendicular obstruction, exactly in rational coordinates.
p=(F(1),F(0),F(0));x=(F(0),F(1),F(0))
for t in [F(1,2),F(1,3),F(1,10),F(1,100)]:
 u=tuple(pj+t*xj for pj,xj in zip(p,x));v=tuple(pj-t*xj for pj,xj in zip(p,x))
 check(dot(x,u)*dot(x,v)*dot(u,v)==-t*t*(1-t*t)<0,'interior perpendicular obstruction')
# Negative extreme vectors plus their sum create distinct forbidden lines.
for t in [F(1,2),F(1,3),F(2,3),F(3,4)]:
 c=-(1-t*t)/(1+t*t);d=2*t/(1+t*t)
 a=(F(1),F(0),F(0));b=(c,d,F(0));z=tuple(u+v for u,v in zip(a,b))
 check(dot(b,b)==1 and -1<c<0,'rational unit extreme pair')
 check(dot(a,b)*dot(a,z)*dot(b,z)==c*(1+c)**2<0,'sign-cone obstruction')
 check(len({ray(a),ray(b),ray(z)})==3,'three distinct projective lines')
sha=hashlib.sha256((P/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()
assert sha=='f53af31e3e4745f6894d6e8874e400cf44046fbaf8a676aa052ec76ad02dc183'
r={'status':'pass','assertions':checks,'families':families,'directions':145,'color_sizes':dict(sorted(Counter(colors).items())),'monochromatic_triples_checked':monochromatic,'negative_triples_recounted':negative,'support_patterns_examined':support_patterns,'artifact_sha256':sha,'scope':'Finite certificate and elementary exact controls only; no continuum extension asserted.'}
(P/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
