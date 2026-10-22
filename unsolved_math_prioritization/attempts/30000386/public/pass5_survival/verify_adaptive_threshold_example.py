"""Independent absolute-coordinate replay of the frozen 24-pair example."""
from itertools import product
from collections import Counter
import json

MOVES = tuple(product((-1, 0, 1), repeat=2))
def add(p, q): return (p[0]+q[0], p[1]+q[1])
def N(p): return {add(p, d) for d in MOVES}
def A8(B):
    candidates = {add(p,d) for p in B for d in MOVES}
    return {q for q in candidates if len(N(q) & B) >= 8}

origin = (0, 0)
Q = set(product((0,1), repeat=2))
Cp = set(product(range(-1,3), repeat=2)) - set(product((-1,2),repeat=2))
C = Cp - {origin}
B = N(origin) - Q
A = N(origin) - {origin}
assert tuple(map(len,(A,B,C,Cp))) == (8,5,11,12)
assert A8(C) == set()
assert A8(Cp) == Q
assert A8(B | A8(C)) == set()

# All absolute three-move words, with the Devil reacting only after each move.
deaths = Counter()
for word in product(MOVES, repeat=3):
    a1 = word[0]
    if a1 in A:
        deaths[1] += 1
        continue
    assert a1 == origin
    terminal = C | {origin}  # announced after observing the first move
    a2 = add(a1, word[1])
    if a2 in B:
        deaths[2] += 1
        continue
    assert a2 in Q
    missing = N(a2) - terminal
    assert len(missing) == 1
    terminal |= missing  # announced after observing the second move
    a3 = add(a2, word[2])
    assert a3 in terminal
    deaths[3] += 1
assert sum(deaths.values()) == 9**3

# An arbitrary first new announcement can add at most one next-time site.
assert len(N(origin) - B) == 4

history = []
for r, p in enumerate(sorted(A), 1): history.append((r,p,25))
for r, p in enumerate(sorted(B), 9): history.append((r,p,26))
for r, p in enumerate(sorted(C),14): history.append((r,p,27))
assert len(history) == 24
assert {r for r,_,_ in history} == set(range(1,25))
assert all(1 <= t-r <= 24 and t>24 for r,p,t in history)
assert {(p,t-24) for r,p,t in history} == {(p,1) for p in A}|{(p,2) for p in B}|{(p,3) for p in C}
print(json.dumps({'words':9**3,'death_round_counts':dict(sorted(deaths.items())),
                  'preload_sizes':[8,5,11], 'dense_centers_before':[],
                  'dense_centers_after':sorted(map(list,Q)),
                  'history_rounds':len(history),'maximum_lead':max(t-r for r,p,t in history)},
                 sort_keys=True,indent=2))
