from fractions import Fraction as F
from itertools import product
from finite_markov import classes_phases,power
from observable_space import matrices,mv,dot,basis,observable_basis
import json,random
checks=0;cases=0;pathchecks=0;dimensions={}
def check(x):
 global checks
 assert x;checks+=1
rng=random.Random(443502)
specs=[(n,) for n in range(1,8)]+[(2,3),(3,3),(1,2,3)]
for spec in specs:
 n=sum(spec);P=[[F(0)]*n for _ in range(n)];pi=[F(0)]*n;off=0
 for d in spec:
  for i in range(d):P[off+i][off+(i+1)%d]=F(1);pi[off+i]=F(1,len(spec)*d)
  off+=d
 labelings=list(product(range(2),repeat=n)) if n<=5 else [tuple(rng.randrange(2) for _ in range(n)) for j in range(30)]
 for labels in labelings:
  cases+=1;M=matrices(P,labels);B,dims=observable_basis(M);check(len(dims)<=n);check(len(B)<=n);dimensions[len(B)]=dimensions.get(len(B),0)+1
  for A in M.values():
   for v in B:check(len(basis(B+[mv(A,v)]))==len(B))
  cp=classes_phases(P,pi);alphas=[]
  for C in cp:
   for phase in C['phases']:
    mass=sum(pi[i] for i in phase);alphas.append(tuple(pi[i]/mass if i in phase else F(0) for i in range(n)))
  words=[()];cols={():tuple([F(1)]*n)}
  for length in range(1,n+3):
   for w in product(M,repeat=length):cols[w]=mv(M[w[0]],cols[w[1:]])
  for a in alphas:
   for length in range(1,min(4,n+2)):
    check(sum(dot(a,v) for w,v in cols.items() if len(w)==length)==1)
    for w in product(M,repeat=length):
     # Independently sum probabilities of all hidden paths of this length.
     prob=F(0)
     for path in product(range(n),repeat=length):
      if any(labels[i]!=x for i,x in zip(path,w)):continue
      t=a[path[0]]
      for i,j in zip(path,path[1:]):t*=P[i][j]
      prob+=t
     check(prob==dot(a,cols[w]));pathchecks+=1
  for i,a in enumerate(alphas):
   for b in alphas[:i+1]:
    delta=tuple(x-y for x,y in zip(a,b));short=all(not dot(delta,v) for w,v in cols.items() if len(w)<=n-1)
    full=all(not dot(delta,v) for v in B);long=all(not dot(delta,v) for v in cols.values());check(short==full==long)
# Nontrivial cyclic quotient:001001 has three, not six, observable phases.
P=[[F(j==(i+1)%6) for j in range(6)] for i in range(6)];M=matrices(P,[0,0,1,0,0,1]);B,_=observable_basis(M)
profiles=[tuple(v[i] for v in B) for i in range(6)];check(len(set(profiles))==3);check(all(profiles[i]==profiles[i+3] for i in range(3)))
# Two iid classes: same bias collapses, different bias survives.
for p,q in [(F(1,3),F(1,3)),(F(1,3),F(2,3))]:
 P=[[1-p,p,0,0],[1-p,p,0,0],[0,0,1-q,q],[0,0,1-q,q]];M=matrices(P,[0,1,0,1]);B,_=observable_basis(M);a=(1-p,p,0,0);b=(0,0,1-q,q)
 check(all(dot(a,v)==dot(b,v) for v in B)==(p==q))
print(json.dumps(dict(assertions=checks,observation_cases=cases,independent_path_probability_checks=pathchecks,observable_dimensions=dimensions,scope='Exact finite controls; the tail and finite-word theorems are proved in TURN_2.md.'),indent=2,sort_keys=True))
