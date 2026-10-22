from itertools import product
from pathlib import Path
import json,hashlib,math
R=list(product(range(2),repeat=4));Z=(0,0,0,0);I=(1,0,0,1);B=(0,1,0,0);E21=(0,0,1,0);checks=0
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def mul(a,b):return ((a[0]*b[0]+a[1]*b[2])%2,(a[0]*b[1]+a[1]*b[3])%2,(a[2]*b[0]+a[3]*b[2])%2,(a[2]*b[1]+a[3]*b[3])%2)
def ck(v):
 global checks
 assert v;checks+=1
ann={x for x in R if x[0]==x[2]==0};ck({mul(x,B) for x in R}==ann)
for a in R:
 # Relations (B,0) and (a,I); subtraction equals addition in F2.
 N={(add(mul(x,B),mul(y,a)),y) for x in R for y in R}
 direct={(x,y) for x in R for y in R if add(x,mul(y,a)) in ann}
 ck(N==direct)
 ck(len(N)==64)
 for x,y in product(R,repeat=2):
  T=add(x,mul(y,a));ck(((x,y) in N)==(T in ann))
  for z in R:
   ck(add(mul(z,x),mul(mul(z,y),a))==mul(z,T))
 # Images of old relations are B and zero, exactly the annihilator.
 ck(add(a,mul(I,a))==Z)
 ck({mul(x,B) for x in R}==ann)
# Reversed substitution sends a genuine relation to a non-annihilator.
a=E21;s=B;r=(mul(s,a),s)
ck(add(r[0],mul(r[1],a))==Z)
wrong=add(r[0],mul(a,r[1]));ck(wrong==I);ck(wrong not in ann)
ck(math.gcd(6,8)==2);ck(6!=2)
# Many integer consistency tests with M=Z/d, c a unit mod d,
# and a chosen inverse mod d: gcd(d*a,1-c*a)=d.
for d in range(2,20):
 for c in range(1,40):
  if math.gcd(c,d)!=1:continue
  for a in range(1,40):
   if (1-c*a)%d==0:ck(math.gcd(d*a,1-c*a)==d)
here=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':checks,'artifact_sha256':hashlib.sha256((here/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),'coverage':'Noncommutative M2(F2) relation kernels for all16 substitution choices, exact left-linearity on all matrices, reversed-order negative control, integer consistency examples. No surface mapping-class relations computed.'}
(here/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
