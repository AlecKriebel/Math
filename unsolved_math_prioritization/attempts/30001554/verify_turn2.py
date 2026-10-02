from itertools import product
from math import gcd
from word_tools import negative_periods,tau_theta
import json,pathlib
checks=0
def check(x):
 global checks
 assert x;checks+=1
# Signed constraint graph: store parity to one root; an odd closed walk fixes it.
for p in range(1,31):
 for q in range(1,31):
  for n in [p+q,p+q+1]:
   graph=[[] for _ in range(n)]
   for k in [p,q]:
    for i in range(n-k):graph[i].append(i+k);graph[i+k].append(i)
   component=[-1]*n;parity=[0]*n;fixed=[]
   for root in range(n):
    if component[root]>=0:continue
    c=len(fixed);fixed.append(False);component[root]=c;todo=[root]
    for x in todo:
     for y in graph[x]:
      if component[y]<0:component[y]=c;parity[y]=parity[x]^1;todo.append(y)
      elif parity[y]==parity[x]:fixed[c]=True
   g=gcd(p,q)
   for i in range(n-g):check(component[i]==component[i+g] and (parity[i]!=parity[i+g] or fixed[component[i]]))
# Separate literal finite-window check with a fixed explicit alphabet and involution.
# Full Cartesian generation, no canonical pruning or author search engine import.
finite=[]
for t,theta in [(1,(1,0,2)),(2,(1,0,2)),(3,(1,0))]:
 n=3*t;accepted=0
 for w in product(range(len(theta)),repeat=n):
  if tau_theta(w,theta)<=t:
   accepted+=1;check(min(negative_periods(w,theta))<=t)
 finite.append(dict(t=t,theta=list(theta),accepted=accepted))
# Literal signed-period gluing for all binary words through length10.
gluings=0
for n in range(3,11):
 for w in product(range(2),repeat=n):
  for split in range(1,n):
   X=w[:-1];Y=w[split:];Z=w[split:-1]
   for p in negative_periods(X,(1,0)):
    for q in negative_periods(Y,(1,0)):
     if len(Z)>=p+q:
      check(gcd(p,q) in negative_periods(w,(1,0)));gluings+=1
# Insufficient ordinary Fine-Wilf threshold control.
w=(0,0,1,1);check(negative_periods(w,(1,0))==[2,3,4])
r=json.loads((pathlib.Path(__file__).parent/'TURN_2_ENUMERATION.json').read_text())
check([x['t'] for x in r]==list(range(1,8)))
check([x['leaves'] for x in r]==[2,8,37,199,1196,8026,59814])
for x in r:check(x['nonperiodic_by_length'][-1]==0 and x['bad']==[])
print(json.dumps(dict(assertions=checks,explicit_alphabet_controls=finite,literal_gluings=gluings,canonical_leaf_counts=[x['leaves'] for x in r],scope='Replay finite_window.py --max-t7 separately; this checker does not substitute for its exhaustive canonical enumeration.'),indent=2,sort_keys=True))
