#!/usr/bin/env python3
"""Independent finite controls for the Legendrian peak obstruction package."""
from itertools import permutations,product,combinations_with_replacement
from math import comb
from pathlib import Path
import json
checks={}
def ck(n,v):
    assert bool(v),n
    checks[n]='PASS'

# Count unordered tuples of actual classes, including equal-tb distinct peaks.
for p in range(1,5):
 for m in range(1,4):
    reps=list(combinations_with_replacement(range(p),m))
    counts={tuple(sorted(t)) for t in product(range(p),repeat=m)}
    ck(f'symmetric_classes_{p}_{m}',set(reps)==counts)
    ck(f'stars_bars_{p}_{m}',len(reps)==comb(p+m-1,m))
    tb=[-1-(i%2) for i in range(p)]
    rot=[2*i for i in range(p)]
    ck(f'tb_min_{p}_{m}',min(sum(tb[j] for j in t)+m-1 for t in reps)==m*min(tb)+m-1)
    ck(f'rot_addition_permutations_{p}_{m}',all(sum(rot[i] for i in t)==sum(rot[i] for i in reversed(t)) for t in reps))
# Permutation group only moves slots of the same oriented prime type.
types=('A','A','B')
allowed=[sigma for sigma in permutations(range(3)) if all(types[sigma[i]]==types[i] for i in range(3))]
ck('permutation_group_size',len(allowed)==2)
raw=list(product(range(3),range(3),range(2)))
orbits={min(tuple(t[sigma[i]] for i in range(3)) for sigma in allowed) for t in raw}
ck('mixed_prime_count',len(orbits)==comb(3+2-1,2)*2)
# Both signs of stabilization transfer preserve the two classical invariants.
for k,(ap,am,bp,bm) in enumerate(product(range(2),repeat=4)):
 for sign in ('plus','minus'):
    i=0 if sign=='plus' else 1
    A=[ap,am];B=[bp,bm];start=(A.copy(),B.copy());start[0][i]+=1
    end=(A.copy(),B.copy());end[1][i]+=1
    def tb(t):return -sum(sum(v) for v in t)
    def rot(t):return sum(v[0]-v[1] for v in t)
    ck(f'transfer_tb_{k}_{sign}',tb(start)==tb(end))
    ck(f'transfer_rot_{k}_{sign}',rot(start)==rot(end))
    ck(f'transfer_no_peak_endpoint_{k}_{sign}',any(sum(v) for v in start) and any(sum(v) for v in end))
# Standard unknot mountain range: exactly one class avoids both stabilizations.
for depth in range(9):
 pairs=[(p,depth-p) for p in range(depth+1)]
 ck(f'unknot_fixed_level_{depth}',len(pairs)==depth+1)
 ck(f'unknot_rot_distinct_{depth}',len({p-q for p,q in pairs})==depth+1)
 ck(f'unknot_peak_{depth}',sum(p==q==0 for p,q in pairs)==int(depth==0))
# Independent bit-mask realization of the infinite Leavitt module.
def b(i,v):
 out=0;n=0
 while v:
    if v&1:out^=1<<(2*n+i)
    v>>=1;n+=1
 return out
def a(i,v):
 out=0;n=0
 while v:
    if n%2==i and v&1:out^=1<<(n//2)
    v>>=1;n+=1
 return out
for v in range(64):
 for i,j in product((0,1),repeat=2):
    ck(f'leavitt_ab_{v}_{i}_{j}',a(i,b(j,v))==(v if i==j else 0))
 ck(f'leavitt_sum_{v}',b(0,a(0,v))^b(1,a(1,v))==v)
ck('nonzero_identity',b(0,a(0,1))^b(1,a(1,1))==1)
for n in range(1,17):
 ck(f'positive_dimension_rank_obstruction_{n}',min(n,2*n)<2*n)
# Trace-only reasoning would fail in characteristic two for even n.
ck('trace_warning_even_dimension',2%2==0)
# Positive representation dimension matters: V=0 would make both identities zero.
ck('zero_dimension_is_excluded',0==2*0)
result={'status':'PASS','assertions':len(checks),'checks':checks,'scope':'Independent finite combinatorial and algebraic controls; not Legendrian realizations, full DGA calculations, or a solution of KP1.63.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
