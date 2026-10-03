#!/usr/bin/env python3
"""Independent exact graph controls. No candidate code is imported.
Finite checks supplement the separately reconstructed unbounded proof.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import random, json, datetime

HERE=Path(__file__).resolve().parent
rng=random.Random(20261003383)
counts={'graphs':0,'laminar_graphs':0,'disjoint_maximal_nonlaminar_graphs':0,'qualifying_graph_k_pairs':0,'boundary_negative_graphs':0,'deletion_cases':0,'uncrossing_four_neighbor_reassignments':0}
examples=[]

def weight(raw):
 s=sum(raw); return tuple(Q(a,s) for a in raw)
def maxima(S):
 return tuple(sorted({s for s in S if s and not any(s<t for t in S)},key=lambda z:tuple(sorted(z))))
def disjoint_max(S):
 return all(not a&b for a,b in combinations(maxima(S),2))
def laminar(S):
 return all(not a&b or a<=b or b<=a for a,b in combinations(S,2))
def inspect(alpha,beta,gamma,S,T,ks=range(1,13),structural=True):
 assert sum(alpha)==sum(beta)==sum(gamma)==1
 assert all(v>0 for v in alpha+beta+gamma)
 n=len(alpha); assert len(S)==len(beta)==len(T)
 assert all(s<=set(range(n)) for s in S)
 assert all(t<=set(range(len(gamma))) for t in T)
 x=min(sum(b for b,s in zip(beta,S) if a in s) for a in range(n))
 y=min(sum(gamma[c] for c in t) for t in T)
 reach=tuple(frozenset().union(*(s for s,t in zip(S,T) if c in t)) for c in range(len(gamma)))
 mass=tuple(sum(alpha[a] for a in r) for r in reach)
 assert x>0 and y>0
 if structural: assert disjoint_max(S)
 counts['graphs']+=1
 if structural:
  counts['laminar_graphs' if laminar(S) else 'disjoint_maximal_nonlaminar_graphs']+=1
  for k in ks:
   if x+k*y>1 and k*x+y>=1:
    counts['qualifying_graph_k_pairs']+=1
    assert max(mass)>=Q(1,k), (alpha,beta,gamma,S,T,k)
 return {'x':x,'y':y,'max_reach':max(mass),'reach_sets':reach,'m':len(maxima(S))}

def serial(obj):
 if isinstance(obj,Q):return str(obj)
 if isinstance(obj,(set,frozenset)):return sorted(obj)
 if isinstance(obj,tuple):return [serial(a) for a in obj]
 if isinstance(obj,list):return [serial(a) for a in obj]
 if isinstance(obj,dict):return {k:serial(v) for k,v in obj.items()}
 return obj

# Actual finite graphs with arbitrary, sharply unequal weights. Maximal blocks
# occur as middle types; chains give laminar controls, crossing subsets within
# one block give the strictly broader disjoint-maximal class.
for trial in range(2400):
 n=rng.randrange(3,13); m=rng.randrange(1,min(5,n)+1)
 order=list(range(n));rng.shuffle(order)
 cuts=sorted(rng.sample(range(1,n),m-1));ends=[0]+cuts+[n]
 blocks=[frozenset(order[ends[i]:ends[i+1]]) for i in range(m)]
 S=[]
 for block in blocks:
  S.append(block)
  if trial%2:
   seq=list(block);rng.shuffle(seq)
   for size in range(1,len(seq)):S.append(frozenset(seq[:size]))
  else:
   for repeat in range(rng.randrange(1,5)):
    S.append(frozenset(a for a in block if rng.randrange(2)))
 if trial%3==0:S.append(frozenset())
 q=rng.randrange(2,8)
 T=[]
 for s in S:
  t=frozenset(c for c in range(q) if rng.randrange(10)<(3+trial%6))
  T.append(t or frozenset({rng.randrange(q)}))
 raw_a=[rng.randrange(1,1001) for a in range(n)]
 raw_a[trial%n]=10**12+trial
 alpha=weight(raw_a)
 beta=weight([rng.randrange(1,1001) for s in S])
 gamma=weight([rng.randrange(1,1001) for c in range(q)])
 r=inspect(alpha,beta,gamma,S,T)
 if trial in [0,1,27,799]:examples.append({'kind':'generated actual graph','alpha':alpha,'beta':beta,'gamma':gamma,'S':S,'T':T,'result':r})

# A non-laminar family inside disjoint maximal triples; zero reverse degree
# is intentional. This uses distinct A mass, not equally weighted A.
alpha=weight([497,1,2,1,498,1]);S=[frozenset([0,1,2]),frozenset([0,1]),frozenset([1,2]),frozenset([3,4,5]),frozenset([3,4]),frozenset([4,5]),frozenset()]
beta=weight([40,3,3,40,3,3,8]);gamma=weight([45,55]);T=[frozenset([0])]*3+[frozenset([1])]*3+[frozenset([0])]
assert disjoint_max(S) and not laminar(S)
r=inspect(alpha,beta,gamma,S,T)
assert r['x']==Q(43,100) and r['y']==Q(45,100) and r['max_reach']==Q(1,2)
examples.append({'kind':'nonlaminar disjoint maximal, exact half reach','alpha':alpha,'beta':beta,'gamma':gamma,'S':S,'T':T,'result':r})

# Highly asymmetric actual graphs at the weak kx+y=1 boundary, all k finite
# but including a k much larger than any author enumeration. Useful B type
# sees all A; empty B type violates any invented reverse A degree condition.
for k in [2,3,7,149,100003]:
 x=Q(1,10**12);y=1-k*x
 r=inspect(weight([1,10**15]),(x,1-x),(y,1-y),[frozenset([0,1]),frozenset()],[frozenset([0]),frozenset([0])],ks=[k])
 assert r['x']==x and r['y']==y and x+k*y>1 and k*x+y==1
 examples.append({'kind':'extreme x, weak boundary','k':k,'result':r})
k=1000003;y=Q(1,1000000);x=(1-y)/k
r=inspect(weight([10**18,1]),(x,1-x),(y,1-y),[frozenset([0,1]),frozenset()],[frozenset([0]),frozenset([0])],ks=[k])
assert x+k*y>1 and k*x+y==1
examples.append({'kind':'extreme y, large k weak boundary','k':k,'result':r})

# Strict inequality cannot be replaced by equality: ordinary disjoint paths.
for k in [1,2,3,7,19]:
 n=k+1;alpha=beta=gamma=tuple(Q(1,n) for _ in range(n));S=[frozenset([a]) for a in range(n)];T=[frozenset([a]) for a in range(n)]
 r=inspect(alpha,beta,gamma,S,T,ks=[k]);assert r['x']+k*r['y']==1 and k*r['x']+r['y']==1 and r['max_reach']<Q(1,k)
 counts['boundary_negative_graphs']+=1
 examples.append({'kind':'strict boundary negative, ordinary paths','k':k,'result':r})

# Direct exceptional-middle deletion in an actual non-laminar graph.
alpha=weight([1,399,100,500]);beta=(Q(2,5),Q(2,5),Q(1,5));gamma=(Q(2,5),Q(2,5),Q(1,5))
S=[frozenset([0,1]),frozenset([2,3]),frozenset([1,2])];T=[frozenset([0,1]),frozenset([1,2]),frozenset([0,2])]
r=inspect(alpha,beta,gamma,S,T,structural=False);eps=beta[-1];k=2;x=r['x'];y=r['y']
assert not disjoint_max(S)
assert eps<x and eps<(x+k*y-1)/(k*y) and eps<=(k*x+y-1)/(k+y-1)
xp=(x-eps)/(1-eps);rr=inspect(alpha,tuple(b/(1-eps) for b in beta[:-1]),gamma,S[:-1],T[:-1],ks=[2])
assert rr['x']>=xp and xp+2*y>1 and 2*xp+y>=1 and rr['max_reach']<=r['max_reach']
examples.append({'kind':'actual exceptional deletion','epsilon':eps,'guaranteed_x_prime':xp,'original':r,'remaining':rr})

# Exact neighborhood of both algebraic boundaries, with independent rational
# cross multiplication. The side conditions epsilon<x and epsilon<1 are kept.
delta=Q(1,10**9)
for k,x,y,e0 in [(2,Q(1,2),Q(3,10),Q(1,6)),(2,Q(2,5),Q(2,5),Q(1,7)),(2,Q(3,10),Q(2,5),Q(0)),(100003,Q(1,10**12),1-Q(100003,10**12),Q(0))]:
 for e in [e0-delta,e0,e0+delta]:
  if not 0<=e<x:continue
  xp=(x-e)/(1-e)
  assert (xp+k*y>1)==(e*k*y<x+k*y-1)
  assert (k*xp+y>=1)==(e*(k+y-1)<=k*x+y-1)
  counts['deletion_cases']+=1
  examples.append({'kind':'deletion boundary','k':k,'x':x,'y':y,'epsilon':e,'strict_condition':xp+k*y>1,'weak_condition':k*xp+y>=1})
for trial in range(10000):
 k=rng.randrange(2,1001);d=rng.randrange(2,10001);a=rng.randrange(1,d+1);b=rng.randrange(1,d+1);e=rng.randrange(a)
 x=Q(a,d);y=Q(b,d);epsilon=Q(e,d);xp=(x-epsilon)/(1-epsilon)
 assert (xp+k*y>1)==(epsilon*k*y<x+k*y-1)
 assert (k*xp+y>=1)==(epsilon*(k+y-1)<=k*x+y-1)
 counts['deletion_cases']+=1

# Raw graph reconstruction, then Boolean union reach (not path counting).
A=tuple(map(frozenset,combinations(range(11),9)));B=tuple(map(frozenset,combinations(range(11),4)))
S=tuple(frozenset(i for i,a in enumerate(A) if b<=a) for b in B);T=B
alpha=tuple(Q(1,55) for a in A);beta=tuple(Q(1,330) for b in B);gamma=tuple(Q(1,11) for c in range(11))
r=inspect(alpha,beta,gamma,S,T,ks=[2],structural=False)
assert len(A)+len(B)+11==396 and r['x']==Q(21,55)>=Q(4,11) and r['y']==Q(4,11)
assert all(len(s)==45 for s in r['reach_sets']) and r['max_reach']==Q(9,11)
assert not laminar(S) and not disjoint_max(S)
path_counts=[sum(len(s) for s,t in zip(S,T) if c in t) for c in range(11)]
assert set(path_counts)=={2520} and set(map(len,r['reach_sets']))=={45}
p=B.index(frozenset(range(4)));q=B.index(frozenset(range(4,8)))
s1,s2=S[p],S[q];union=s1|s2;inter=s1&s2
assert [len(s1),len(s2),len(inter),len(union)]==[21,21,3,39]
old_degree=[sum(beta[j] for j,s in enumerate(S) if a in s) for a in range(55)]
newS=list(S);newS[p]=union;newS[q]=inter
assert old_degree==[sum(beta[j] for j,s in enumerate(newS) if a in s) for a in range(55)]
remaining=tuple(frozenset().union(*(s for j,(s,t) in enumerate(zip(S,T)) if j not in [p,q] and c in t)) for c in range(11))
assert remaining==r['reach_sets']
with_union=[len(s|union) for s in remaining];with_inter=[len(s|inter) for s in remaining];with_both=[len(s|union|inter) for s in remaining]
assert with_union==[51]*8+[55]*3 and with_inter==[45]*8+[47]*3
# Enumerate every minimal legal reassignment for BOTH changed vertices.
# More than four neighbors can only increase reach, so four-neighbor choices
# certify the exact optimum among all legal choices of at least four neighbors.
choices=tuple(map(frozenset,combinations(range(11),4)));best=55;witness=None
for u in choices:
 for v in choices:
  z=max(with_both[c] if c in u and c in v else with_union[c] if c in u else with_inter[c] if c in v else len(remaining[c]) for c in range(11))
  counts['uncrossing_four_neighbor_reassignments']+=1
  if z<best:best=z;witness=[sorted(u),sorted(v)]
assert best==51 and counts['uncrossing_four_neighbor_reassignments']==108900
examples.append({'kind':'raw overlap graph and exact local reassignment optimum','part_sizes':[55,330,11],'result':r,'per_C_path_counts':path_counts,'per_C_distinct_reach_counts':[45]*11,'uncrossed_sizes':[21,21,3,39],'union_reach_counts':with_union,'intersection_reach_counts':with_inter,'minimum_legal_max_reach':Q(best,55),'minimizing_reassignment':witness,'fixed_remaining_middle_vertices':328})

out={'status':'PASS','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independence':'No author or earlier reviewer code imported; own adjacency/Boolean reach/Fraction implementation. Primary sources reconstructed first.','counts':counts,'examples':serial(examples),'scope':'Finite controls are not the original universal proof, do not imply universal laminarization/support reduction, and do not certify novelty.'}
(HERE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'counts':counts,'uncrossing_minimum_legal_max_reach':'51/55'},indent=2))
