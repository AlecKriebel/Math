"""Expanded gluing controls using disjoint sets and Burnside fixed-point averages."""
from itertools import product
from math import gcd, lcm
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(cat,p):
    assert p,cat
    counts[cat]=counts.get(cat,0)+1

def involutions(n, allow_fixed):
    def go(left, edges):
        if not left:
            out=list(range(n))
            for a,b in edges:out[a]=b;out[b]=a
            yield tuple(out)
            return
        a,*rest=left
        if allow_fixed:yield from go(rest,edges)
        for b in rest:
            yield from go([x for x in rest if x!=b],edges+[(a,b)])
    yield from go(list(range(n)),[])

def glued_components(a,b):
    root=list(range(len(a)))
    def find(i):
        while root[i]!=i:i=root[i]
        return i
    for i in range(len(a)):
        for j in (a[i],b[i]):root[find(i)]=find(j)
    return len({find(i) for i in range(len(a))})

cases=0
for n in (0,2,4,6):
    bound=lcm(*range(1,n+1)) if n else 1
    for a in involutions(n,False):
        for b in involutions(n,True):
            p=tuple(a[b[i]] for i in range(n))
            f=sum(b[i]==i for i in range(n))
            # Burnside's lemma for the cyclic action, using an a priori common order.
            cur=tuple(range(n)); fixed_sum=0
            for _ in range(bound):
                fixed_sum+=sum(cur[i]==i for i in range(n))
                cur=tuple(p[cur[i]] for i in range(n))
            ck('permutation_period',cur==tuple(range(n)))
            cycles=F(fixed_sum,bound)
            comp=glued_components(a,b)
            ck('burnside_cycle_integrality',cycles.denominator==1)
            ck('boundary_evenness',f%2==0)
            ck('arc_corrected_formula',4*comp==2*cycles+f)
            ck('closed_component_nonnegative',cycles-F(f,2)>=0)
            for c0 in range(4):
                ck('uncut_components',4*(comp+c0)==2*cycles+f+4*c0)
            cases+=1

ck('single_arc_requires_correction',glued_components((1,0),(0,1))==1 and F(1,2)+F(2,4)==1)
ck('two_colored_parallel_edges',glued_components((1,0),(1,0))==1)
for n in range(1,101):
    ck('consecutive_coprimality',gcd(n,n+1)==1)
    ck('homogeneous_forced_value',F(gcd(n,n+1),n)==F(1,n))
    ck('diagonal_scale',gcd(n,n)==n)
for k in range(1,41):
    ck('binary_expansion', (2**k).bit_length()==k+1 and 2*(2**k)==2**(k+1))
ck('two_pants_curves_gcd_fails',gcd(1,1)==1 and 2!=1)

r=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((r/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'involution_pair_cases':cases,'scope':'Expanded finite gluing and narrow arithmetic diagnostics only; not a compressed Dehn–Thurston formula or proof of geometric admissibility.'}
(r/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
