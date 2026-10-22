"""Small exact consistency controls for a credited known boundedness consequence."""
from itertools import product
from math import comb,gcd
from pathlib import Path
import json,hashlib
checks=0;families={};examples=[]
def ck(x,label):
 global checks
 assert x,label
 checks+=1;families[label]=families.get(label,0)+1
for q in [3,5,7]:
 X=range(q)
 def op(a,b):return (2*b-a)%q
 for a in X:ck(op(a,a)==a,'quandle idempotence')
 for b in X:ck(len({op(a,b) for a in X})==q,'invertible right translation')
 for a,b,c in product(X,repeat=3):ck(op(op(a,b),c)==op(op(a,c),op(b,c)),'quandle self distributivity')
 states=list(product(X,repeat=2))
 def S(pair):a,b=pair;return (b,op(a,b))
 inv={S(x):x for x in states};ck(len(inv)==q*q,'braid coloring permutation')
 def power(x,k):
  for _ in range(abs(k)):x=S(x) if k>=0 else inv[x]
  return x
 for k in range(-11,12,2):
  h=sum(power(x,k)==x for x in states)
  ck(q<=h<=q*q,'two-braid coloring bound')
  ck(h==q*gcd(q,k),'dihedral odd two-braid count')
 examples.append({'q':q,'unknot_count':sum(S(x)==x for x in states),'T_2_q_count':sum(power(x,q)==x for x in states)})
 ck(examples[-1]['unknot_count']==q and examples[-1]['T_2_q_count']==q*q,'nonconstant example control')
for d in range(7):
 for n in range(-5,6):
  ck(sum((-1)**(d+1-j)*comb(d+1,j)*(n+j)**d for j in range(d+2))==0,'finite difference polynomial identity')
for m in range(1,8):
 ck(sum((-1)**(m-j)*comb(m,j) for j in range(m+1))==0,'constant additive shift')
p=Path(__file__).parent
r={'status':'pass','assertions':checks,'families':families,'examples':examples,'artifact_sha256':hashlib.sha256((p/'SOURCE_STATUS.md').read_bytes()).hexdigest(),'scope':'Finite exact quandle/braid and polynomial controls only; no numerical logarithm test or novelty assertion.'}
(p/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
