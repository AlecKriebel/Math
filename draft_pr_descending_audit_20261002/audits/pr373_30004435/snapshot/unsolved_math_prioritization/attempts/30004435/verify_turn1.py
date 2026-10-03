from fractions import Fraction as F
from itertools import combinations,product
from math import lcm
import random,json
from finite_markov import power,classes_phases
checks=0
def check(x):
 global checks
 assert x;checks+=1
rng=random.Random(30004435)
choices=[(1,1),(1,2),(1,3),(2,1),(2,2),(3,1),(3,2)]
specs=[(x,) for x in choices]+list(combinations(choices,2))+[tuple(choices[i:i+3]) for i in range(5)]
bridges=0
for spec in specs:
 size=sum(d*h for d,h in spec);P=[[F(0) for _ in range(size+1)] for _ in range(size+1)];pi=[F(0)]*(size+1);offset=0
 for d,h in spec:
  for phase in range(d):
   weights=[rng.randint(1,7) for _ in range(h)];total=sum(weights)
   for i in range(h):
    a=offset+phase*h+i;pi[a]=F(1,len(spec)*d*h)
    for j in range(h):P[a][offset+((phase+1)%d)*h+j]=F(weights[(j-i)%h],total)
  offset+=d*h
 P[size][0]=F(1) # A transient state of stationary mass0.
 check(all(sum(row)==1 for row in P));check(sum(pi)==1)
 check([sum(pi[i]*P[i][j] for i in range(size+1)) for j in range(size+1)]==pi)
 cp=classes_phases(P,pi);check([x['period'] for x in cp]==[x[0] for x in spec]);D=lcm(*(x['period'] for x in cp));Q=power(P,D)
 for C in cp:
  mass=sum(pi[i] for i in C['states'])
  for phase in C['phases']:
   h=len(phase);check(sum(pi[i] for i in phase)==mass/C['period'])
   epsilon=h*min(Q[i][j] for i in phase for j in phase);check(0<epsilon<=1)
   for k in [1,2,4,8]:
    A=power(P,k*D);B=power(P,2*k*D);delta=(1-epsilon)**k
    for i in phase:
     tv=sum(abs(A[i][j]-F(1,h)) for j in phase)/2;check(tv<=delta)
     for j in phase:
      bridge=[A[i][a]*A[a][j]/B[i][j] for a in range(size+1)]
      check(sum(bridge)==1);check(all(bridge[a]==0 for a in range(size+1) if a not in phase));bridges+=1
      tvb=sum(abs(bridge[a]-F(a in phase,h)) for a in range(size+1))/2
      if delta*delta<F(1,h):
       bound=((h+1)*delta+delta*delta)/(2*(F(1,h)-delta*delta));check(tvb<=bound)
# Periodic phase is genuine tail information even when invariant events are trivial.
P=[[F(0),F(1)],[F(1),F(0)]];cp=classes_phases(P,[F(1,2)]*2);check(cp[0]['period']==2);check(cp[0]['phases']==[[0],[1]])
# Shift-register finite truncations of the infinite-state counterexample mix exactly.
for length in range(1,6):
 n=2**length;P=[[F(0) for _ in range(n)] for _ in range(n)]
 for i in range(n):
  for b in [0,1]:P[i][((i<<1)|b)&(n-1)]+=F(1,2)
 R=power(P,length);check(all(x==F(1,n) for row in R for x in row));check(classes_phases(P,[F(1,n)]*n)[0]['period']==1)
# Tail discontinuity under weak convergence of fixed binary-state Markov laws.
weak=[]
for k in range(1,8):
 epsilon=F(1,2**k)
 for n in range(2,11):
  tv=F(0)
  for word in product(range(2),repeat=n):
   p=F(1,2)
   for a,b in zip(word,word[1:]):p*=1-epsilon if a==b else epsilon
   q=F(1,2) if len(set(word))==1 else F(0)
   tv+=abs(p-q)/2
  check(tv==1-(1-epsilon)**(n-1));check(tv<=(n-1)*epsilon)
 weak.append(dict(epsilon=str(epsilon),ten_block_tv=str(1-(1-epsilon)**9)))
print(json.dumps(dict(assertions=checks,chain_cases=len(specs),bridge_cases=bridges,weak_limit_controls=weak,scope='Finite exact controls for the phase/bridge proof and approximation barriers; no finite scan proves the general source method request.'),indent=2,sort_keys=True))
