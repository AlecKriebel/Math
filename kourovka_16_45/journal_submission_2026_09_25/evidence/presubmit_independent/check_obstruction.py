"""Fresh presubmission falsification checks; no project verifier imports.

Run with Python 3. Uses exact arithmetic and independently constructs H,
all H-subgroups, line stabilizers, and the affine size-three witness.
"""
from collections import Counter, deque
from itertools import combinations
import json

p = 29
I = (1, 0, 0, 1)
minus = (28, 0, 0, 28)
A = (0, 28, 1, 0)
B = (2, 7, 12, 28)
R2 = (12, 24, 0, 17)
R3 = (25, 3, 4, 4)

def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g)%p, (a*f+b*h)%p,
            (c*e+d*g)%p, (c*f+d*h)%p)

def mv(h, v):
    a, b, c, d = h
    x, y = v
    return ((a*x+b*y)%p, (c*x+d*y)%p)

def closure(gens):
    out, queue = {I}, deque([I])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mul(x, g)
            if y not in out:
                out.add(y)
                queue.append(y)
    return frozenset(out)

H = closure([A, B])
assert len(H) == 120
assert all((x[0]*x[3]-x[1]*x[2])%p == 1 for x in H)
assert [x for x in H if x != I and mul(x, x) == I] == [minus]

# Enumerate subgroups by repeatedly adjoining one element. The stored tuple
# is an independently known generating set, not an external subgroup list.
gens = {frozenset([I]): ()}
todo = deque(gens)
while todo:
    J = todo.popleft()
    for x in H-J:
        K = closure(gens[J]+(x,))
        if K not in gens:
            gens[K] = gens[J]+(x,)
            todo.append(K)
subs = list(gens)
odd = [J for J in subs if len(J)%2]
assert {len(J) for J in odd} == {1, 3, 5}
assert all(minus in J for J in subs if len(J)%2 == 0)

# Every putative irredundant triple with trivial bottom is tested directly.
faithful_triples = 0
normal_bottom_triple = None
for J, K, L in combinations(subs, 3):
    bottom = J & K & L
    if (J & K) > bottom and (J & L) > bottom and (K & L) > bottom:
        if len(bottom) == 1:
            faithful_triples += 1
        if bottom == frozenset([I, minus]):
            normal_bottom_triple = (len(J), len(K), len(L))
assert faithful_triples == 0
assert normal_bottom_triple is not None

line_reps = [(1, t) for t in range(p)] + [(0, 1)]
def same_line(v, w):
    return (v[0]*w[1]-v[1]*w[0])%p == 0

line_stabilizers = [frozenset(h for h in H if same_line(mv(h, v), v))
                    for v in line_reps]
assert all(len(J) == 4 for J in line_stabilizers)
assert all(any(closure([h]) == J for h in J) for J in line_stabilizers)
assert all(all(h == I or mv(h, v) != v for h in J)
           for J, v in zip(line_stabilizers, line_reps))

pair23, pair13, pair12 = (closure(pair) for pair in
                        [(R2, R3), (A, R3), (A, R2)])
assert [len(pair23), len(pair13), len(pair12)] == [8, 12, 20]
assert closure([A, R2, R3]) == H
assert pair23 & pair13 & pair12 == frozenset([I, minus])
for J in [pair23, pair13, pair12]:
    orbit = {mv(h, (1, 0)) for h in J}
    assert any(not same_line(x, (1, 0)) for x in orbit)

# Affine elements use a translation vector and an exact 2x2 matrix.
def amul(x, y):
    v, h = x
    w, k = y
    hw = mv(h, w)
    return (((v[0]+hw[0])%p, (v[1]+hw[1])%p), mul(h, k))

identity = ((0, 0), I)
def aclosure(gs):
    out, queue = {identity}, deque([identity])
    while queue:
        x = queue.popleft()
        for g in gs:
            y = amul(x, g)
            if y not in out:
                out.add(y)
                queue.append(y)
    return frozenset(out)

L1 = aclosure([((1, 0), I), ((0, 0), minus)])
L2 = aclosure([((0, 1), I), ((0, 0), minus)])
L3 = aclosure([((1, 1), I), ((2, 0), minus)])
assert [len(L1), len(L2), len(L3)] == [58, 58, 58]
assert L1 & L2 == frozenset([identity, ((0, 0), minus)])
assert L1 & L3 == frozenset([identity, ((2, 0), minus)])
assert L2 & L3 == frozenset([identity, ((0, 27), minus)])
assert L1 & L2 & L3 == frozenset([identity])

# Four independent generators and the resulting nonnormal bottom.
S = [((1, 0), I), ((0, 0), A), ((0, 0), R2), ((0, 0), R3)]
M = [aclosure(S[:i]+S[i+1:]) for i in range(4)]
assert all(S[i] not in M[i] and all(S[j] in M[i] for j in range(4) if j != i)
           for i in range(4))
Z0 = frozenset([identity, ((0, 0), minus)])
assert frozenset.intersection(*M) == Z0
conjugate = amul(amul(((1, 0), I), ((0, 0), minus)), ((28, 0), I))
assert conjugate == ((2, 0), minus) and conjugate not in Z0

# Witnesses certify all 16 distinct images, and pairwise intersection is
# precisely the meet operation on their Boolean index sets.
whole = frozenset(((a, b), h) for a in range(p) for b in range(p) for h in H)
def meet_image(mask):
    ans = whole
    for i in range(4):
        if not (mask & (1 << i)):
            ans = ans & M[i]
    return ans
images = [meet_image(mask) for mask in range(16)]
assert len(set(images)) == 16
assert all(images[i] & images[j] == images[i & j]
           for i in range(16) for j in range(16))
assert images[0] == Z0 and images[15] == whole

print(json.dumps({
    "H_order": len(H),
    "H_subgroups_by_order": dict(sorted(Counter(map(len, subs)).items())),
    "H_odd_subgroup_orders": sorted({len(J) for J in odd}),
    "H_irredundant_trivial_bottom_triples": faithful_triples,
    "H_example_irredundant_Z_bottom_triple_orders": normal_bottom_triple,
    "line_stabilizers_by_order": dict(Counter(map(len, line_stabilizers))),
    "affine_three_subgroup_orders": list(map(len, [L1, L2, L3])),
    "affine_coset_union_degree": sum(len(whole)//len(J) for J in [L1, L2, L3]),
    "four_witness_omission_subgroup_orders": list(map(len, M)),
    "four_witness_intersection_order": len(frozenset.intersection(*M)),
    "Boolean_rank4_distinct_images": len(set(images)),
    "status": "all assertions passed"
}, indent=2))
