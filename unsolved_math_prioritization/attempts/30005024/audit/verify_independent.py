#!/usr/bin/env python3
"""Independent exact diagnostics. No import or execution of author code.

The 9,093 original test cases are reconstructed with a subset-insertion dynamic
program, fraction-free integer determinants, and weighted two-by-two transfers.
Additional tests have a separately reported count. These are finite diagnostics,
not formal proofs, novelty certification, or a solution of the original problem.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import cache
from itertools import product
from math import factorial, lcm, prod
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parent
counts = Counter()
extra = Counter()
def demand(name, value, bucket=counts):
    if not value:
        raise AssertionError(name)
    bucket[name] += 1

def canonical(word):
    labels = {}
    return tuple(labels.setdefault(x, len(labels)) for x in word)

@cache
def insertions(word):
    """Count insertion histories on position subsets, rather than deleting words."""
    n = len(word)
    if n > 7:
        # Every long word used below is alternating. The only possible last
        # insertions are its endpoints; shorter cases use the subset algorithm.
        if not all(word[j] != word[j+1] for j in range(n-1)):
            return 0
        if not all(word[j] == word[j+2] for j in range(n-2)):
            raise ValueError('long non-alternating word is outside test scope')
        return insertions(canonical(word[1:])) + insertions(canonical(word[:-1]))
    ways = [0] * (1 << n)
    ways[0] = 1
    for mask in range(1, 1 << n):
        present = [i for i in range(n) if mask >> i & 1]
        if any(word[i] == word[j] for i,j in zip(present,present[1:])):
            continue
        ways[mask] = sum(ways[mask ^ (1 << i)] for i in present)
    return ways[-1]

def probability(q, word):
    n = len(word)
    b = insertions(canonical(word))
    return Q(b, (1 << n)*factorial(n+1)) if q == 4 else Q(2*b, factorial(n+2))

def bareiss_det(matrix):
    """Clear denominators rowwise, then fraction-free Bareiss elimination."""
    scales = [lcm(*(v.denominator for v in row)) for row in matrix]
    a = [[int(v*s) for v in row] for row,s in zip(matrix,scales)]
    sign, previous = 1, 1
    for k in range(len(a)-1):
        pivot_row = next((r for r in range(k,len(a)) if a[r][k]), None)
        if pivot_row is None:
            return Q(0)
        if pivot_row != k:
            a[k],a[pivot_row] = a[pivot_row],a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numer = pivot*a[i][j] - a[i][k]*a[k][j]
                quotient, rem = divmod(numer,previous)
                if rem:
                    raise AssertionError('non-exact Bareiss division')
                a[i][j] = quotient
            a[i][k] = 0
        previous = pivot
    return Q(sign*a[-1][-1],prod(scales))

def determinant_formula(q,s):
    vandermonde = prod(factorial(i) for i in range(1,s))
    sign = (-1)**(s*(s-1)//2)
    if q == 4:
        return Q(sign * 2**(s*(s-1)//2) * vandermonde,
                 2**s * prod(factorial(2*i+s) for i in range(1,s+1)))
    return Q(sign * 2**(2*s*s) * vandermonde,
             prod(factorial(2*i+s+1) for i in range(1,s+1)))

minors=[]
for q,gap in ((4,1),(3,2)):
    for length in range(6):
        mass=Q(0)
        for word in product(range(q), repeat=length):
            p=probability(q,word)
            mass += p
            demand('nonnegative', p >= 0)
            demand('left_consistency', sum(probability(q,(x,)+word) for x in range(q)) == p)
            demand('right_consistency', sum(probability(q,word+(x,)) for x in range(q)) == p)
        demand('cylinder_normalization',mass == 1)
    for left_length,right_length in product((1,2),repeat=2):
        for left in product(range(q),repeat=left_length):
            for right in product(range(q),repeat=right_length):
                mass=sum(probability(q,left+middle+right) for middle in product(range(q),repeat=gap))
                demand('separated_blocks',mass == probability(q,left)*probability(q,right))
    for n in range(1,25):
        word=tuple(i%2 for i in range(n))
        p=probability(q,word)
        expected=Q(1,2*factorial(n+1)) if q==4 else Q(2**n,factorial(n+2))
        demand('alternating_word_law',p == expected)
        demand('alternating_continuation', probability(q,word+(n%2,))/p == (Q(1,n+2) if q==4 else Q(2,n+3)))
    for s in range(1,13):
        h=[[probability(q,(0,1)*i+tuple(t%2 for t in range(j))) for j in range(s)] for i in range(1,s+1)]
        value=bareiss_det(h)
        bucket=counts if s<=8 else extra
        demand('hankel_minor_formula',value == determinant_formula(q,s) and value != 0,bucket)
        if s<=8:minors.append({'colors':q,'size':s,'determinant':str(value)})

for choices in product(range(5),repeat=5):
    # Group by bit-index; different indices cannot collide. Within each group,
    # distinct sites remain distinct after adding the common index.
    groups={n:[i+n for i,x in enumerate(choices) if x==n] for n in set(choices)}
    demand('heavy_delay_injective',all(len(v)==len(set(v)) for v in groups.values()))
partial=Q(1,2)
for r in range(1,100):
    partial += Q(1,r+1)-Q(1,r+2)
    demand('heavy_delay_tail',1-partial == Q(1,r+2))

# Matrix-style transfer over U0,U1,... while accumulating X0=1. Interior
# observations are 1, followed by either boundary value. No full bit strings.
conditional=[]
p=Q(1,3)
bernoulli=(1-p,p)
for m in range(1,6):
    n=2*m
    values=[]
    for boundary in (0,1):
        state={(u,first): bernoulli[u]*bernoulli[first] for u in (0,1) for first in (0,1)}
        # State is (U0,current Uj), start at j=1.
        for j in range(1,n+1):
            wanted=1 if j<n else boundary
            nxt=Counter()
            for (origin,old),weight in state.items():
                for new in (0,1):
                    if old^new == wanted:
                        nxt[(origin,new)] += weight*bernoulli[new]
            state=nxt
        # For n even, U1 is recovered as U[n+1] XOR boundary XOR 1.
        total=sum(state.values())
        one=sum(weight for (origin,last),weight in state.items() if origin != (last^boundary^1))
        values.append(one/total)
    demand('conditional_bridge',values == [Q(5,9),Q(4,9)])
    conditional.append({'m':m,'conditional_probabilities':list(map(str,values))})

P=((Q(1,2),Q(1,2),Q(0)),(Q(0),Q(1,2),Q(1,2)),(Q(1,2),Q(0),Q(1,2)))
word=((0,1,0),(1,1,2))
demand('sync_no_single_step',not any(all(row[j] for row in P) for j in range(3)))
image=list(range(3));delta=Q(1)
for f in word:
    image=[f[x] for x in image]
    for x,y in enumerate(f):
        demand('sync_supported',P[x][y]>0)
        delta*=P[x][y]
demand('sync_word',len(set(image))==1)
demand('sync_probability',delta==Q(1,64))

# Exhaust all 3-state directed supports (including loops). Iterate Boolean
# powers until full positivity or an exactly repeated power. Repetition makes
# all subsequent powers periodic, so no untested exponent bound is needed.
primitive=0
for bits in product((0,1),repeat=9):
    adj=[bits[3*i:3*i+3] for i in range(3)]
    if not all(any(row) for row in adj):continue
    power=[[int(i==j) for j in range(3)] for i in range(3)]
    L=None
    seen=set()
    length=0
    while True:
        fingerprint=tuple(tuple(row) for row in power)
        if fingerprint in seen:break
        seen.add(fingerprint)
        length+=1
        power=[[int(any(power[i][k] and adj[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
        if all(all(row) for row in power):L=length;break
    if L is None:continue
    primitive+=1
    for terminal in range(3):
        pred=[{terminal}]
        for t in range(L):pred.append({i for i in range(3) if any(adj[i][j] and j in pred[-1] for j in range(3))})
        current=list(range(3))
        for remaining in range(L,0,-1):
            f=[]
            for i in range(3):
                options=[j for j in range(3) if adj[i][j] and (i not in pred[remaining] or j in pred[remaining-1])]
                demand('primitive_supported_choice',bool(options),extra)
                f.append(min(options))
            current=[f[i] for i in current]
        demand('primitive_synchronizes',set(current)=={terminal},extra)

recorded=json.loads((ROOT/'author/results.json').read_text())
demand('original_count_is_9093',sum(counts.values())==9093,extra)
demand('all_original_counts_match',dict(counts)==recorded['checks'],extra)
demand('all_original_minors_match',minors==recorded['hankel_minors'],extra)
demand('all_original_bridges_match',conditional==recorded['conditional_bridge'],extra)
demand('original_sync_probability_matches',str(delta)==recorded['sync_word_probability'],extra)
result={
 'status':'PASS_INDEPENDENT_REBUILD',
 'original_cases_rebuilt':sum(counts.values()),
 'original_case_counts':dict(sorted(counts.items())),
 'recorded_author_results_match':True,
 'additional_exact_checks':sum(extra.values()),
 'additional_check_counts':dict(sorted(extra.items())),
 'hankel_minor_sizes_checked_per_law':12,
 'primitive_three_state_supports_checked':primitive,
 'original_hankel_minors':minors,
 'conditional_bridge':conditional,
 'sync_word_probability':str(delta),
 'limitations':['Finite diagnostics are not formal verification of the analytical arguments.',
                'No test establishes an infinite-mean lower bound for all representations.',
                'Countably infinite hidden-state spaces remain outside the Hankel exclusion.',
                'The primitive-support enumeration is finite and does not replace the general proof.']}
serialized=json.dumps(result,indent=2,sort_keys=True)+'\n'
parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
path=ROOT/'INDEPENDENT_RESULTS.json'
if args.write:path.write_text(serialized)
else:
    if path.read_text()!=serialized:raise AssertionError('independent recorded results differ')
print(json.dumps({k:result[k] for k in ('status','original_cases_rebuilt','additional_exact_checks','primitive_three_state_supports_checked','recorded_author_results_match')}))
