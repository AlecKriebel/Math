"""Independent integer-polynomial Gram-square census, no triangle criterion."""
import itertools,json
from collections import Counter
from fractions import Fraction
def require(c):
 if not c:raise RuntimeError('Independent harmonic audit failed')
# Phi_15 = x^8-x^7+x^5-x^4+x^3-x+1.
phi=[1,-1,0,1,-1,1,0,-1,1]
def red(p):
 p=list(p)+[0]*max(0,8-len(p))
 for k in range(len(p)-1,7,-1):
  c=p[k]
  for j in range(9):p[k-8+j]-=c*phi[j]
 return tuple(p[:8])
def mul(a,b):
 p=[0]*15
 for i,x in enumerate(a):
  for j,y in enumerate(b):p[i+j]+=x*y
 return red(p)
D=[0,1,2,3,5,7,8,11]
counts=Counter((a-b)%15 for a in D for b in D if a!=b)
require(counts==Counter({i:4 for i in range(1,15)}))
g=[]
for a in range(15):
 p=[0]*15
 for k in D:p[(k*a)%15]+=1
 g.append(red(p))
products={(a,b):mul(g[a],g[b]) for a in range(15) for b in range(15)}
# Independently validate squared coherence for normalized Gram K/8.
require(all(products[a,(-a)%15]==(4,0,0,0,0,0,0,0) for a in range(1,15)))
# Orthogonality of distinct Fourier rows proves full frame tightness.
admissible=[m for m in range(2,8) if Fraction(m,1+Fraction(m-1,16)).denominator==1]
require(admissible==[5])
def tight(t):
 for i in t:
  for j in t:
   vals=[products[(k-i)%15,(j-k)%15] for k in t]
   if tuple(sum(v[l] for v in vals) for l in range(8))!=tuple(10*v for v in g[(j-i)%15]):return False
 return True
blocks=[t for t in itertools.combinations(range(15),5) if tight(t)]
expected=json.load(open('harmonic_exact_results.json'))
require(blocks==[tuple(t) for t in expected['proper_tight_blocks_zero_based']])
counts={str(k):sum(len(set(sum((list(t) for t in p),[])))==5*k for p in itertools.combinations(blocks,k)) for k in range(1,4)}
require(counts==expected['partition_counts_with_remaining_singletons'])
res={'method':'Independent integer polynomial arithmetic modulo explicit Phi15 and full Gram square test on all3003 five-subsets','blocks':blocks,'partition_counts':counts,'total_nontrivial_partitions':sum(counts.values()),'matches_primary_census':True}
print(json.dumps(res,indent=2))
open('independent_harmonic_results.json','w').write(json.dumps(res,indent=2)+'\n')
