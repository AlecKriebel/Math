"""Independent exact SIC triple audit using polynomial-field determinants."""
import itertools,json
def require(condition):
 if not condition: raise RuntimeError("Independent exact audit failed")
# Q[z]/(z^2+z+1); all entries here integral.
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def mul(x,y):
 a,b=x;c,d=y
 return (a*c-b*d,a*d+b*c-b*d)
def det3(cols):
 out=(0,0)
 for p in itertools.permutations(range(3)):
  parity=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
  term=(1,0)
  for i in range(3):term=mul(term,cols[p[i]][i])
  out=add(out,neg(term) if parity else term)
 return out
zero=(0,0);one=(1,0);minus=(-1,0);z=(0,1);mz=(0,-1);mz2=(1,1)
cols=[(zero,one,minus),(zero,one,mz),(zero,one,mz2),(minus,zero,one),(mz,zero,one),(mz2,zero,one),(one,minus,zero),(one,mz,zero),(one,mz2,zero)]
def conj(x): return (x[0]-x[1],-x[1])
def dot(x,y):
 out=zero
 for a,b in zip(x,y):out=add(out,mul(conj(a),b))
 return out
require(all(dot(c,c)==(2,0) for c in cols))
require(all(mul(dot(cols[i],cols[j]),conj(dot(cols[i],cols[j])))==one for i in range(9) for j in range(i)))
for i in range(3):
 for j in range(3):
  v=zero
  for c in cols:v=add(v,mul(c[i],conj(c[j])))
  require(v==((6,0) if i==j else zero))
triples=[t for t in itertools.combinations(range(9),3) if det3([cols[i] for i in t])==zero]
# Pairwise coherence squared 1/4 implies no two columns proportional; every
# dependent triple has rank 2. Its eigenvalues satisfy equality in trace CS:
# trace=3, trace(square)=9/2, rank=2, hence both nonzero eigenvalues=3/2.
expected=json.load(open('exact_results.json'))
require(triples==[tuple(t) for t in expected['proper_nonsingleton_tight_blocks_zero_based']])
counts={}
for k in range(1,4):
 counts[str(k)]=sum(len(set(sum((list(t) for t in combo),[])))==3*k for combo in itertools.combinations(triples,k))
require(counts==expected['partitions_with_remaining_singletons'])
require(sum(counts.values())==expected['total_nontrivial_partitions'])
require(expected['parameters']=={'n':9,'d':3,'q':'1/4'})
result={'method':'Independent exact polynomial quotient arithmetic and determinant/rank test','dependent_triples':len(triples),'partitions_by_nonsingleton_block_count':counts,'matches_primary_enumeration':True}
print(json.dumps(result,indent=2))
open('independent_audit_results.json','w').write(json.dumps(result,indent=2)+'\n')
