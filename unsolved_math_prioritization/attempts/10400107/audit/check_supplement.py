#!/usr/bin/env python3
"""Independent bounded audit controls. Exact arithmetic; standard library only.
The reduction implementation uses closed-branch elementary contractions, rather
than the submitted floor-and-carry implementation. These tests are NOT a proof
of the arbitrary-quandle CW/cohomology statement.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import json

D = 3
COUNTS = Counter()
A5 = tuple(tuple((2*x-y)%5 for y in range(5)) for x in range(5))
R4 = tuple(tuple((2*y-x)%4 for y in range(4)) for x in range(4))
T2 = ((0,0),(1,1))
T1 = ((0,),)

def normalizer(table):
    def prefix_action(prefix, a):
        return tuple((t, table[x][a]) for t,x in prefix)
    @lru_cache(None)
    def nf(word):
        choices=[]
        for i,(t,a) in enumerate(word):
            if t == 0:
                choices.append(word[:i]+word[i+1:])
            if t == D:
                choices.append(prefix_action(word[:i],a)+word[i+1:])
        for i in range(len(word)-1):
            t,a=word[i]; u,b=word[i+1]
            if a != b:
                continue
            if t+u <= D:
                choices.append(word[:i]+((t+u,a),)+word[i+2:])
            if t+u >= D:
                choices.append(prefix_action(word[:i],a)+((t+u-D,a),)+word[i+2:])
        if not choices:
            assert all(0<t<D for t,a in word)
            assert all(a!=b for (_,a),(_,b) in zip(word,word[1:]))
            return word
        targets={nf(child) for child in choices}
        assert len(targets)==1, (table,word,targets)
        COUNTS['independent_reduction_states']+=1
        return targets.pop()
    return nf

nf_a5=normalizer(A5)
# Right translations here have order four, unlike all of the original
# geometric controls, whose nontrivial translations are involutions.
for b in range(5):
    for a in range(5):
        z=a
        for k in range(4):z=A5[z][b]
        assert z==a
assert A5[A5[0][1]][1] != 0
COUNTS['noninvolutive_translation_witnesses']=1

alphabet=tuple(product(range(D+1),range(5)))
for n in range(5):
    for word in product(alphabet,repeat=n):
        normal=nf_a5(word)
        COUNTS['A5_all_third_grid_words_degree_le_4']+=1
        for i in range(n-1):
            t,a=word[i];u,b=word[i+1]
            if a!=b:continue
            for r in range(D+1):
                s=t+u-r
                if 0<=s<=D:
                    changed=word[:i]+((r,a),(s,a))+word[i+2:]
                    assert nf_a5(changed)==normal
                    COUNTS['A5_equal_sum_fibers']+=1

# Two disjoint merges with a nonempty prefix, testing noncommuting carries.
for p,a,b in product(range(5),repeat=3):
    for ts in product(range(D+1),repeat=5):
        word=tuple(zip(ts,(p,a,a,b,b)))
        nf_a5(word)
        COUNTS['A5_disjoint_merge_roots_degree_5']+=1

# Non-injective homomorphisms on coordinates, not merely on chains.
def check_geometric_naturality(source,target,f,max_degree):
    assert all(f[source[a][b]]==target[f[a]][f[b]]
               for a,b in product(range(len(source)),repeat=2))
    ns,nt=normalizer(source),normalizer(target)
    alpha=tuple(product(range(D+1),range(len(source))))
    for n in range(max_degree+1):
        for word in product(alpha,repeat=n):
            mapped=tuple((t,f[a]) for t,a in word)
            mapped_normal=tuple((t,f[a]) for t,a in ns(word))
            assert nt(mapped)==nt(mapped_normal)
            COUNTS['geometric_noninjective_naturality']+=1
            if len(nt(mapped))<len(ns(word)):
                COUNTS['geometric_naturality_dimension_drops']+=1
check_geometric_naturality(R4,T2,(0,1,0,1),4)
check_geometric_naturality(A5,T1,(0,0,0,0,0),3)

# Closed-branch seam: the low branch leaves coordinate 1, the high branch
# leaves 0 and acts on the prefix. The quotient identifies the two.
for p,a in product(range(5),repeat=2):
    for s,t in product(range(D+1),repeat=2):
        prefix=((s,p),)
        low=prefix+((D,a),)
        high=tuple((r,A5[x][a]) for r,x in prefix)+((0,a),)
        seam_word=prefix+((t,a),(D-t,a))
        assert nf_a5(low)==nf_a5(high)==nf_a5(seam_word)
        COUNTS['closed_branch_seam_checks']+=1

print(json.dumps({'result':'PASS','counts':dict(sorted(COUNTS.items())),
 'arithmetic':'Exact integers representing thirds; no network, randomness, or external libraries',
 'additional_coverage':['Non-involutive Alexander quandle A5, right translation order four',
 'All A5 words through degree four on {0,1/3,2/3,1}',
 'All prefixed disjoint-pair degree-five A5 words on that grid',
 'Geometric naturality for R4 to T2 parity and A5 to singleton',
 'Closed-piece seam at adjacent-coordinate sum one'],
 'limits':'Finite regression evidence only; does not replace the general termination/confluence, CW weak-topology, or cochain proofs.'},indent=2,sort_keys=True))
