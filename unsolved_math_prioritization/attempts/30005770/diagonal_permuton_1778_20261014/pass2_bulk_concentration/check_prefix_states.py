#!/usr/bin/env python3
"""Bounded exact checks of first-hit prefix-state continuation equality."""
from itertools import permutations,combinations
from functools import lru_cache
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent

def require(c,m):
 if not c:raise RuntimeError(m)
def st(s):
 ranks={v:i+1 for i,v in enumerate(sorted(s))}
 return tuple(ranks[v] for v in s)
@lru_cache(maxsize=None)
def has(p,a):
 return any(st(tuple(p[i] for i in I))==a for I in combinations(range(len(p)),len(a)))
@lru_cache(maxsize=None)
def lab(p,a):
 return next((j for j in range(len(a),len(p)+1) if has(p[:j],a)),len(p)+1)
def ins(p,k):return tuple(x+1 for x in p[:k])+(1,)+tuple(x+1 for x in p[k:])
@lru_cache(maxsize=None)
def sig(p,a,depth):
 L=lab(p,a)
 return (L,) if depth==0 else (L,tuple(sig(ins(p,k),a,depth-1) for k in range(L)))
counts={'classes':0,'present_prefix_checks':0,'absent_flag_checks':0,'scalar_counterexample_pairs':0}
for m in [2,3,4]:
 for alpha in permutations(range(1,m+1)):
  tau=tuple(x+1 for x in alpha)+(1,)
  counts['classes']+=1
  top=6 if m<=3 else 5
  for n in range(top+1):
   for p in permutations(range(1,n+1)):
    if has(p,tau):continue
    L=lab(p,alpha)
    if L<=n:
     q=st(p[:L])
     require(has(q,alpha),'present flag')
     require(lab(q,alpha)==len(q),'endpoint at end')
     require(sig(p,alpha,2)==sig(q,alpha,2),'entire depth2 continuation tree equality')
     counts['present_prefix_checks']+=1
    else:
     require(L==n+1 and not has(p,alpha),'absent sentinel')
     counts['absent_flag_checks']+=1
# Frozen exact pairs in the note, including both containing states.
pairs=[((1,3,2),(1,3,4,2),(2,1,4,3),(5,5,5,5),(3,5,5,5)),((3,1,2),(1,4,2,3),(2,4,1,3),(5,5,4,5),(5,4,4,5))]
for a,p,q,cp,cq in pairs:
 tau=tuple(x+1 for x in a)+(1,)
 require(not has(p,tau) and not has(q,tau),'pair belongs to target class')
 require(lab(p,a)==4 and lab(q,a)==4,'pair equal labels')
 require(tuple(lab(ins(p,k),a) for k in range(4))==cp,'first child list')
 require(tuple(lab(ins(q,k),a) for k in range(4))==cq,'second child list')
 require(sum(cp)!=sum(cq),'distinct D2')
 counts['scalar_counterexample_pairs']+=1
print(json.dumps({'status':'PASS','scope':'Finite exact prefix-state checks only; not an asymptotic proof.','python_optimization_level':sys.flags.optimize,'bounds':{'alpha_lengths':[2,3,4],'maximum_parent_size_by_alpha_length':{'2':6,'3':6,'4':5},'continuation_depth':2},'checks':counts,'proof_sha256':hashlib.sha256((P/'PREFIX_STATE_REDUCTION.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
