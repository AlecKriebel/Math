from pathlib import Path
import json,hashlib,itertools
from fractions import Fraction as F
p=Path('/workspace/shared/math-30001202');n=0
for mf in ['FINAL_AUTHOR_MANIFEST.json','SOURCE_HASHES.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 for name,h in json.loads((p/mf).read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h;n+=1
S=set(range(3));sets=[{i for i in S if mask>>i&1} for mask in range(8)]
for f in itertools.product(range(3),repeat=3):
 for word in itertools.product(sets,repeat=3):
  paths=[(x,f[x],f[f[x]]) for x in S if x in word[0] and f[x] in word[1] and f[f[x]] in word[2]]
  A=[word[0]]
  for t in [1,2]:A.append({f[x] for x in A[-1]}&word[t])
  B=[None,None,word[2]]
  for t in [1,0]:B[t]={x for x in word[t] if f[x] in B[t+1]}
  Q=[A[t]&B[t] for t in range(3)]
  for t in range(3):assert Q[t]=={path[t] for path in paths};n+=1
  if paths:
   assert all(Q[t]==word[t] for t in range(3))==all({f[x] for x in word[t]}==word[t+1] for t in [0,1]);n+=1
for rho in [F(1,5),F(1,2),F(3,4)]:
 theta=(rho+1)/2;K=(1+rho*theta)/(theta-rho)+(theta+rho)/(1-rho*theta)
 for T in range(20):
  w=[theta**t+theta**(T-t) for t in range(T+1)]
  for t in range(T+1):
   value=sum(rho**(t-1-k)*w[k] for k in range(t))+sum(rho**(k-t+1)*w[k] for k in range(t,T))
   assert value<=K*w[t];n+=1
# Counterexample orbit coordinates and exact code-prefix separation.
for k in range(1,100):
 a=F(1,k+2);b=2+a
 assert a/(1-a)==F(1,k+1);n+=1
 assert 2+(b-2)/(3-b)==2+F(1,k+1);n+=1
 assert b-a==2;n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'integrity, arbitrary-subset marginal gluing, geometric-sum coefficients and boundary-orbit controls'},indent=2))
