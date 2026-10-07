"""Independent, exact audit of the bowtie periodic tube/face calculations.
No source file is executed or modified. Run from the repository directory.
"""
from collections import Counter, defaultdict
from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'nonnegative_critical_varieties_30004938'
N = 5
# Endpoint-interlacing reconstruction of crossings from Definition 2.4.
fbar = [3,1,5,2,4]
inv = {p:s for s,p in enumerate(fbar,1)}
crossings = []
for p,q in combinations(range(1,N+1),2):
    a,b = 2*inv[p]-1, 2*p-2
    c,d = 2*inv[q]-1, 2*q-2
    if (0 < (c-a)%(2*N) < (b-a)%(2*N)) != (0 < (d-a)%(2*N) < (b-a)%(2*N)):
        crossings.append((p,q))
assert crossings == [(1,2),(1,3),(2,3),(2,4),(2,5),(4,5)]
# Reduced covers of the two given chains, expressed as residue/period edges.
EDGES = [(1,2,0), (2,3,0), (3,1,1), (2,4,0), (4,5,0), (5,2,1)]
INF = 1000
dist = [[0 if i == j else INF for j in range(N)] for i in range(N)]
for a,b,k in EDGES:
    dist[a-1][b-1] = min(dist[a-1][b-1], k)
for k in range(N):
    for i in range(N):
        for j in range(N):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

def decode(x):
    t, r0 = divmod(x-1, N)
    return r0+1, t

def less(x,y):
    r,t = decode(x); s,u = decode(y)
    return x != y and u-t >= dist[r-1][s-1]

def neighbors(x):
    r,t = decode(x)
    for a,b,k in EDGES:
        if a == r: yield b + N*(t+k)
        if b == r: yield a + N*(t-k)

def convex(S):
    for a,b in combinations(sorted(S),2):
        if less(a,b):
            for c in range(a+1,b):
                if less(a,c) and less(c,b) and c not in S: return False
    return True

# Independently enumerate connected sets, extending along covers rather than
# enumerating all bounded integer subsets and testing comparability connectivity.
found = set()
for m in range(1,N+1):
    frontier = {frozenset([m])}
    for size in range(2,N+1):
        nxt = set()
        for S in frontier:
            for a in S:
                for b in neighbors(a):
                    if b >= m and b not in S and all((b-c)%N for c in S):
                        nxt.add(S | {b})
        frontier = nxt
        found.update(S for S in frontier if convex(S))
tubes = sorted(found,key=lambda S:(min(S),len(S),tuple(sorted(S))))
original = {frozenset(S) for S in json.loads((SOURCE/'checks/bowtie_tubes.json').read_text())['tubes']}
assert found == original, (found-original, original-found)

def compatible(A,B):
    # Only these shifts can intersect; all other shifts are disjoint.
    shifts = {(a-b)//N for a in A for b in B if (a-b)%N == 0}
    for d in shifts:
        C = frozenset(b+N*d for b in B)
        if A & C and not (A <= C or C <= A): return False
    return True

def min_edge_shift(A,B):
    # A strictly smaller shift puts every element of B+dN below every element
    # of A in the integer order and cannot furnish an increasing relation.
    d = (min(A)-max(B))//N + 1
    while True:
        C = frozenset(b+N*d for b in B)
        if not A&C and any(less(a,b) for a in A for b in C): return d
        d += 1

weights = {(i,j):min_edge_shift(A,B) for i,A in enumerate(tubes) for j,B in enumerate(tubes)}
assert all(weights[i,i] == 1 for i in range(len(tubes)))
compat = {(i,j):compatible(tubes[i],tubes[j]) for i in range(len(tubes)) for j in range(i+1,len(tubes))}

def exact_acyclic(ids):
    # Each tube has an edge to its +N translate. Thus a negative closed walk
    # can be closed by +1 self edges, and a zero walk already closes in the
    # infinite lift. Conversely an infinite-lift cycle projects to a closed
    # quotient walk of total shift zero. It suffices to check simple cycles:
    # every quotient closed walk decomposes into those.
    for k in range(1,len(ids)+1):
        for sub in combinations(ids,k):
            start = min(sub)
            for tail in permutations(i for i in sub if i != start):
                cyc = (start,)+tail
                if sum(weights[cyc[t],cyc[(t+1)%k]] for t in range(k)) <= 0:
                    return False
    return True

# Reproduce the original five-translate graph but use independent exact order.
def window_acyclic(ids):
    V = [frozenset(x+N*t for x in tubes[i]) for i in ids for t in range(-2,3)]
    E = [{j for j,B in enumerate(V) if i != j and not A&B and any(less(a,b) for a in A for b in B)} for i,A in enumerate(V)]
    indeg = [sum(j in adj for adj in E) for j in range(len(V))]
    todo = [i for i,k in enumerate(indeg) if k == 0]
    count = 0
    while todo:
        i = todo.pop(); count += 1
        for j in E[i]:
            indeg[j] -= 1
            if indeg[j] == 0: todo.append(j)
    return count == len(V)

# Minimal containing tube: normalize by fixing the representative of R[0].
# Every container for all three has a translate containing R[0].
def image_type(ids,R):
    allts = []
    for i in ids:
        for x in tubes[i]:
            if (x-R[0])%N == 0:
                d = (R[0]-x)//N
                allts.append(frozenset(y+N*d for y in tubes[i]))
    candidates = [T for T in allts if all(any((x-r)%N == 0 for x in T) for r in R)]
    if candidates:
        container = min(candidates,key=len)
        lifts = [next(x for x in container if (x-r)%N == 0) for r in R]
        for a,b in combinations(range(3),2):
            for i in ids:
                for x in tubes[i]:
                    if (x-lifts[a])%N == 0:
                        d = (lifts[a]-x)//N
                        U = frozenset(y+N*d for y in tubes[i])
                        if U < container and lifts[b] in U:
                            return ('v',tuple(sorted((R[a],R[b]))))
        order = sorted(range(3),key=lambda a:lifts[a])
        return ('e',tuple(sorted((R[order[0]],R[order[-1]]))))
    for a,b in combinations(R,2):
        if any(any((x-a)%N == 0 for x in tubes[i]) and any((x-b)%N == 0 for x in tubes[i]) for i in ids):
            return ('v',(a,b))
    return ('int',)

levels={0:[()]}; differences=[]; candidates_count={}; allimages=defaultdict(list)
for size in range(1,5):
    candidate = [ids for ids in combinations(range(len(tubes)),size) if all(compat[i,j] for i,j in combinations(ids,2))]
    candidates_count[size] = len(candidate)
    levels[size] = []
    for ids in candidate:
        exact = exact_acyclic(ids)
        finite = window_acyclic(ids)
        if exact != finite: differences.append({'ids':ids,'exact':exact,'window':finite})
        if exact: levels[size].append(ids)
    print('codimension',size,'nested/disjoint candidates',len(candidate),'exact faces',len(levels[size]),flush=True)
for size,rows in levels.items():
    for ids in rows:
        key = str((image_type(ids,(1,2,3)),image_type(ids,(2,4,5))))
        allimages[key].append(ids)

# Verify each reported original label and retained face, translating its indices.
original_order = [frozenset(S) for S in json.loads((SOURCE/'checks/bowtie_tubes.json').read_text())['tubes']]
indexmap = {i:tubes.index(S) for i,S in enumerate(original_order)}
original_faces = json.loads((SOURCE/'checks/bowtie_faces_exploratory.json').read_text())
original_set = set(); label_errors=[]
for key,rows in original_faces['images'].items():
    for ids in rows:
        normalized = tuple(sorted(indexmap[i] for i in ids))
        original_set.add(normalized)
        actual = str((image_type(normalized,(1,2,3)),image_type(normalized,(2,4,5))))
        if key != actual: label_errors.append({'ids':ids,'original':key,'exact':actual})
exact_set = set(ids for rows in levels.values() for ids in rows)
result = {
    'crossings': crossings,
    'tube_counts': dict(sorted(Counter(map(len,tubes)).items())),
    'tube_count': len(tubes),
    'tube_set_matches_original': found == original,
    'max_tube_span': max(max(S)-min(S) for S in tubes),
    'tubes': [sorted(S) for S in tubes],
    'residue_minimum_shift_matrix':dist,
    'nested_disjoint_candidate_counts':candidates_count,
    'exact_codimension_counts':{s:len(rows) for s,rows in levels.items()},
    'window_exact_differences':differences,
    'original_exact_face_sets_match':original_set == exact_set,
    'original_image_label_errors':label_errors,
    'exact_product_face_type_count':len(allimages),
    'images':allimages,
}
(OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['tubes','images']},indent=2))
