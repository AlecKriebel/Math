"""Independent rational and character-histogram audit, not a conjecture proof."""
from fractions import Fraction as F
from itertools import product,permutations
from collections import Counter
from math import isqrt,comb
import random,json
rng=random.Random(1816)
checks=0
for p in (5,7,11,13):
 for trial in range(20):
  c=[rng.randrange(4) for _ in range(p)]; n=[c.count(i) for i in range(4)]; a=[F(v,p) for v in n]
  count=Counter();pairs=triples=mono=walsh=0
  for x in range(p):
   for d in range(1,p):
    v=[c[(x+j*d)%p] for j in range(4)]
    count[tuple(sorted(Counter(v).values()))]+=1
    pairs+=sum(v[i]==v[j] and v[k]==v[l] for i,j,k,l in [(0,1,2,3),(0,2,1,3),(0,3,1,2)])
    triples+=sum(len(set(v[:j]+v[j+1:]))==1 for j in range(4))
    mono+=len(set(v))==1
    walsh+=sum((-1)**sum((z&mask).bit_count() for z in v) for mask in (1,2,3))
  R=count[(1,1,1,1)];D=sum(v*(v-1) for v in n)
  assert R==p*(p-1)-6*D+pairs+2*triples-6*mono
  assert 4*R==p*(p-1)+walsh-4*pairs+8*mono
  # Check the exact two-term telescoping identity for all 24 color orders.
  for colors in permutations(range(4)):
   lhs=F(0);rhs=F(0)
   i,j,k,l=colors
   for x in range(p):
    for d in range(p):
     b=[int(c[(x+h*d)%p]==col) for h,col in enumerate(colors)]
     lhs+=b[0]*b[1]*b[2]*b[3]
     rhs+=(b[0]-a[i])*b[1]*b[2]*b[3]+a[i]*(b[1]-a[j])*b[2]*b[3]
   assert lhs/p**2-a[i]*a[j]*a[k]*a[l]==rhs/p**2
  checks+=1
ks=[k for k in product(range(5),repeat=4) if sum(k)==4 and k!=(1,1,1,1)]
types={(0,1,1,2):F(59,100),(0,0,2,2):F(35,100),(0,0,1,3):F(5,100),(0,0,0,4):F(1,100)}
base={k:types[tuple(sorted(k))]/sum(sorted(l)==sorted(k) for l in ks) for k in ks}
pair_checks=0
for p in list(range(10001,10022,2))+[65537,1000003]:
 for n in set(permutations([p//4+int(i<p%4) for i in range(4)])):
  Q=[[F(n[i]*(n[j]-int(i==j)),p*(p-1)) for j in range(4)] for i in range(4)]
  delta=[[v-F(1,16) for v in row] for row in Q]; w=base.copy()
  for i in range(4):
   for j in range(i+1,4):w[tuple(3*int(h==i)+int(h==j) for h in range(4))]+=4*delta[i][j]
   w[tuple(4*int(h==i) for h in range(4))]+=delta[i][i]-2*sum(delta[i][j] for j in range(i+1,4))
  assert min(w.values())>0 and sum(w.values())==1
  for i in range(4):
   for j in range(4):assert sum(v*F(k[i]*(k[j]-int(i==j)),12) for k,v in w.items())==Q[i][j]
  pair_checks+=1
assert sum(comb(4,s)*3**s*(s-1) for s in range(1,5))==513
assert sum(comb(4,s)*3**s*(4-s) for s in range(1,5))==252
assert (263681-256)**2-513**2*263681==65536
prime=lambda p:all(p%d for d in range(2,isqrt(p)+1))
p=263681
while not prime(p):p+=4
factors=[];z=p-1
for q in range(2,isqrt(z)+1):
 if z%q==0:
  factors.append(q)
  while z%q==0:z//=q
if z>1:factors.append(z)
g=next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in factors))
chi=[None]*p;x=1
for e in range(p-1):chi[x]=e%4;x=x*g%p
hist=Counter(tuple(chi[(t+j)%p] for j in range(4)) for t in range(p) if all((t+j)%p for j in range(4)))
assert len(hist)==256 and min(hist.values())>0
print(json.dumps({'random_colorings_exact_identities_and_all_permutation_telescoping':checks,'exact_pair_laws_all_balance_permutations':pair_checks,'quartic_threshold_integer_check':'passed','quartic_histogram_prime':p,'primitive_root':g,'patterns_present':len(hist),'minimum_pattern_count':min(hist.values())},indent=2))
