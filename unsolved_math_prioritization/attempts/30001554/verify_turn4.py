from itertools import product
from word_tools import parameters,theta_borders,theta_word
import json
checks=0

def check(x):
 global checks
 assert x;checks+=1
out=[]
for theta,N in [((1,0),13),((1,0,2),9),((1,0,3,2),7),((0,1),10)]:
 ct=saturated=gap=0
 for n in range(1,N+1):
  for w in product(range(len(theta)),repeat=n):
   t,p=parameters(w,theta);ct+=1
   if n>=2*p-1:
    saturated+=1;u=w[:p];fixed=all(theta[a]==a for a in u)
    U=u if fixed else u+theta_word(u,theta);d=len(U)
    check(all(U!=U[:k]*(d//k) for k in range(1,d) if d%k==0))
    i=min(range(d),key=lambda j:U[j:]+U[:j]);R=U[i:]+U[:i]
    check(not any(R[:k]==R[-k:] for k in range(1,d)))
    j=i%p;f=w[j:j+p]
    check(len(f)==p and not theta_borders(f,theta));check(t==p)
   if t<p:
    gap+=1;check(n<=2*p-2)
    B=theta_borders(w,theta);check(bool(B));check(all(2*k<=n-2 for k in B))
 out.append(dict(theta=list(theta),maximum_length=N,words=ct,saturation_instances=saturated,gap_instances=gap))
print(json.dumps(dict(assertions=checks,cases=out,scope='Finite controls for the all-alphabet saturation and witness theorem proved in TURN_4.md.'),indent=2,sort_keys=True))
