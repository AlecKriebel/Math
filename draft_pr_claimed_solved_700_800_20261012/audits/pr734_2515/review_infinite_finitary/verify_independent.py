#!/usr/bin/env python3
"""Independent standard-library checks; computations do not prove the infinite union."""
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib, json, platform, random, sys

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT.parent / 'original/unsolved_math_prioritization/attempts/2515/author/PROOFS.md'

def comp(a, b):
    return tuple(a[b[x]] for x in range(len(a)))

def inv(a):
    r = [0] * len(a)
    for x, y in enumerate(a): r[y] = x
    return tuple(r)

def perm(f, t):
    return tuple(2 * (v ^ t) + (e ^ ((f >> (v ^ t)) & 1)) for v in range(4) for e in range(2))

def tau(f, t):
    return sum(((f >> (v ^ t)) & 1) << v for v in range(4))

pairs = [(f,t) for t in range(4) for f in range(16) if f.bit_count() % 2 == t % 2]
P = tuple(perm(f,t) for f,t in pairs)
assert len(set(P)) == len(P) == 32
pair_index = {pair:i for i,pair in enumerate(pairs)}
perm_index = {p:i for i,p in enumerate(P)}
identity = perm_index[tuple(range(8))]
M = tuple(tuple(perm_index[comp(a,b)] for b in P) for a in P)
for i,(f,t) in enumerate(pairs):
    for j,(g,u) in enumerate(pairs):
        assert M[i][j] == pair_index[(f ^ tau(g,t), t ^ u)]
    assert inv(P[i]) == perm(tau(f,t), t)

# Generate finite subgroups from the multiplication table, independently of parity derivation.
def extend(H, x):
    generators = tuple(H) + (x,)
    reached = {identity}
    todo = [identity]
    while todo:
        y = todo.pop()
        for g in generators:
            z = M[g][y]
            if z not in reached:
                reached.add(z); todo.append(z)
    return frozenset(reached)

subgroups = {frozenset((identity,))}
todo = list(subgroups)
while todo:
    H = todo.pop()
    for x in range(32):
        if x not in H:
            Q = extend(H, x)
            if Q not in subgroups: subgroups.add(Q); todo.append(Q)
transitive = [H for H in subgroups if {P[g][0] for g in H} == set(range(8))]
assert transitive == [frozenset(range(32))]

# Test all choices that the minimal-transitivity proof permits, including commutator formula.
lifts1 = [pair_index[f,1] for f in range(16) if f.bit_count() % 2 == 1]
lifts2 = [pair_index[g,2] for g in range(16) if g.bit_count() % 2 == 0]
for i,j in product(lifts1,lifts2):
    assert len(extend(extend(frozenset((identity,)), i), j)) == 32
    f,t = pairs[i]; g,u = pairs[j]
    square = comp(P[i],P[i])
    h = f ^ tau(f,1)
    assert square == perm(h,0)
    c = (f ^ tau(f,2)) ^ (g ^ tau(g,1))
    assert comp(comp(comp(P[i],P[j]),inv(P[i])),inv(P[j])) == perm(c,0)
    assert c ^ tau(c,1) == 15

b = perm(0,2)
z = perm((1<<1) | (1<<2),0)
C = frozenset((0,4))
assert frozenset(b[x] for x in C) == C
assert frozenset(z[x] for x in C) == frozenset((0,5))
assert len(C & frozenset(z[x] for x in C)) == 1

def cycles(p):
    seen = set()
    out = []
    for x in range(len(p)):
        if x not in seen:
            c = []
            while x not in seen:
                seen.add(x); c.append(x); x = p[x]
            out.append(frozenset(c))
    return out

def has_cycle_blocks(elements):
    for p in elements:
        for c in cycles(p):
            for q in elements:
                qc = frozenset(q[x] for x in c)
                if qc != c and qc & c: return False
    return True
assert not has_cycle_blocks(P)

# Complete first extension, tuple implementation independent of a tree implementation below.
def wreath_perm(a,b,swap):
    return tuple((a[x] + 8*swap) if x<8 else (b[x-8] + 8*(1-swap)) for x in range(16))
W = tuple(wreath_perm(a,b,s) for a,b,s in product(P,P,(0,1)))
assert len(set(W)) == 2048
B = frozenset(range(8))
W_B = [w for w in W if frozenset(w[x] for x in B)==B]
assert len(W_B)==1024
assert {tuple(w[x] for x in range(8)) for w in W_B} == set(P)
for w in W:
    image = frozenset(w[x] for x in B)
    assert image == B or not image & B
all_b_lifts = [w for w in W_B if tuple(w[x] for x in range(8)) == b]
all_z_lifts = [w for w in W_B if tuple(w[x] for x in range(8)) == z]
for hb,hz in product(all_b_lifts,all_z_lifts):
    assert C in cycles(hb)
    image = frozenset(hz[x] for x in C)
    assert image != C and len(image & C)==1

# A transitive proper subgroup without the original first-factor copy: diagonal P x C2.
J = tuple(wreath_perm(a,a,s) for a,s in product(P,(0,1)))
assert len(set(J)) == 64
assert {j[0] for j in J} == set(range(16))
assert not set(wreath_perm(a,P[identity],0) for a in P).issubset(set(J))
assert not has_cycle_blocks(J)
assert {tuple(j[x] for x in range(8)) for j in J if j[0]<8}==set(P)

# Controls. Full untwisted group has a regular elementary-abelian subgroup.
regular = tuple(perm(f,t) for f,t in product((0,15),range(4)))
assert len(set(regular))==8
assert {p[0] for p in regular}==set(range(8))
assert all(len({p[x] for p in regular})==8 for x in range(8))
assert has_cycle_blocks(regular)
assert C == frozenset(P[identity][x] for x in C)

# Symbolic recursive tree: leaves are P; internal nodes act as source-half swap.
def eval_tree(tree, x, n):
    if n==0: return tree[x]
    left,right,swap = tree
    half = 8*(1<<(n-1))
    side,local = divmod(x,half)
    image = eval_tree(right if side else left,local,n-1)
    return image + half*(side ^ swap)

def identity_tree(n):
    if n==0:return P[identity]
    child = identity_tree(n-1)
    return (child,child,0)

def random_tree(n,rng):
    if n==0:return P[rng.randrange(32)]
    return (random_tree(n-1,rng),random_tree(n-1,rng),rng.randrange(2))

def first_embed(tree,n):
    return (tree,identity_tree(n),0)

rng = random.Random(7342515)
random_counts = {}
for n in (0,1,2,3,6,9):
    count = 8 if n==9 else 24
    size = 8*(1<<n)
    for _ in range(count):
        tree = random_tree(n,rng)
        p = tuple(eval_tree(tree,x,n) for x in range(size))
        assert set(p)==set(range(size))
        for k in range(n+1):
            width=8*(1<<k)
            for start in range(0,size,width):
                image={p[x] for x in range(start,start+width)}
                lo=min(image)
                assert lo%width==0 and image==set(range(lo,lo+width))
        for leaf in range(1<<n):
            restricted=tuple(p[8*leaf+x]%8 for x in range(8))
            assert restricted in set(P)
        embedded=first_embed(tree,n)
        assert all(eval_tree(embedded,x,n+1)==p[x] for x in range(size))
        assert all(eval_tree(embedded,x,n+1)==x for x in range(size,2*size))
    random_counts[str(n)]=count

receipt = {
    'scope':'finite and bounded recursive controls; infinite statements independently deduced in report.md',
    'runtime':{'python_version':platform.python_version(),'executable':sys.executable,'third_party_math_libraries_used':False},
    'candidate_sha256':hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
    'P_order':len(P),
    'subgroup_count':len(subgroups),
    'subgroup_order_histogram':{str(k):v for k,v in sorted(Counter(map(len,subgroups)).items())},
    'transitive_subgroup_count':len(transitive),
    'all_lift_pairs_generating_P':len(lifts1)*len(lifts2),
    'crossing_witness_one_based':{'cycle':[1,5],'z_image':[1,6],'intersection':[1]},
    'first_wreath_order':len(W),
    'first_wreath_bottom_stabilizer_order':len(W_B),
    'all_arbitrary_outside_lift_pairs_checked':len(all_b_lifts)*len(all_z_lifts),
    'proper_transitive_diagonal_control_order':len(J),
    'diagonal_control_contains_first_factor_P':False,
    'regular_untwisted_control_has_cycle_blocks':True,
    'identity_translate_control_does_not_cross':True,
    'recursive_random_seed':7342515,
    'recursive_random_samples_by_level':random_counts,
    'status':'PASS'
}
(ROOT/'control_receipts.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
