"""Independent necessary-invariant stress tests; imports no publication checker.
Fox-coloring fixed-space dimensions over F3/F5 and ordered classical crossings
are computed directly from displayed even schemes. This is not a proof oracle.
"""
from itertools import product, permutations
from collections import Counter
from functools import lru_cache
import datetime as dt
import json
import os
import sys

def words(k, length):
    letters = tuple((i, e) for i in range(1, k+1) for e in (-1, 0, 1))
    return [w for n in range(length+1) for w in product(letters, repeat=n)]
def inverse(w):
    return tuple((i, -e) for i, e in reversed(w))
def up(w):
    return tuple((i+1, e) for i, e in w)
def dimension(n, word, p):
    matrix = [[int(i == j) for j in range(n)] for i in range(n)]
    for i, e in word:
        assert 1 <= i < n and e in (-1, 0, 1)
        x, y = matrix[i-1][:], matrix[i][:]
        if e == 0:
            matrix[i-1], matrix[i] = y, x
        elif e == 1:
            matrix[i-1], matrix[i] = [(2*a-b) % p for a, b in zip(x,y)], x
        else:
            matrix[i-1], matrix[i] = y, [(2*b-a) % p for a, b in zip(x,y)]
    equations = [[(entry-int(i == j)) % p for j, entry in enumerate(row)]
                 for i, row in enumerate(matrix)]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank,n) if equations[i][col]), None)
        if pivot is None:
            continue
        equations[rank], equations[pivot] = equations[pivot], equations[rank]
        z = pow(equations[rank][col], -1, p)
        equations[rank] = [v*z % p for v in equations[rank]]
        for i in range(n):
            if i != rank:
                factor = equations[i][col]
                equations[i] = [(v-factor*w) % p for v,w in zip(equations[i],equations[rank])]
        rank += 1
    return n-rank
def ordered(n, word):
    labels = list(range(n))
    for i,e in word:
        labels[i-1], labels[i] = labels[i], labels[i-1]
    membership = {}
    count = 0
    for start in range(n):
        current = start
        while current not in membership:
            membership[current] = count
            current = labels[current]
        if membership[start] == count:
            count += 1
    matrix = [[0]*count for _ in range(count)]
    labels = list(range(n))
    for i,e in word:
        left, right = labels[i-1], labels[i]
        if e:
            over, under = (left,right) if e == 1 else (right,left)
            a,b = membership[over], membership[under]
            if a != b:
                matrix[a][b] += e
        labels[i-1], labels[i] = right,left
    return tuple(map(tuple,matrix))
@lru_cache(maxsize=None)
def canonical(matrix):
    n = len(matrix)
    return min(tuple(matrix[i][j] for i in perm for j in perm) for perm in permutations(range(n)))
counts = Counter()
comparisons = 0
def check(family, n1, w1, n2, w2):
    global comparisons
    for p in (3,5):
        assert dimension(n1,w1,p) == dimension(n2,w2,p), (family,n1,w1,n2,w2,p)
        comparisons += 1
    m1,m2 = ordered(n1,w1), ordered(n2,w2)
    assert len(m1) == len(m2) and canonical(m1) == canonical(m2), (family,w1,w2,m1,m2)
    comparisons += 1
    counts[family] += 1
for n in (2,4,6):
    for a in words(n-1,1):
        for b in words(n-1,1):
            check("C", n,b,n,a+b+inverse(a))
    for a in words(n-2,1):
        for b in words(n-2,1):
            check("BC",n,b+((n-1,1),),n,a+b+inverse(a)+((n-1,1),))
    for b in words(n-2,2):
        for g in (-1,0,1):
            check("T",n,b+((n-1,1),),n,b+((n-1,g),))
    for b in words(n-1,2):
        for g in (-1,0,1):
            check("D",n,b,n+2,b+((n,g),(n+1,1)))
for m in range(2,6):
    n = m if m % 2 == 0 else m+1
    tail = ((m,1),) if m % 2 else ()
    for a in words(m-2,2):
        for b in words(m-2,2):
            check("R" if m % 2 == 0 else "BR",n,
                  a+((m-1,-1),)+b+((m-1,1),)+tail,n,
                  a+((m-1,0),)+b+((m-1,0),)+tail)
            check("L" if m % 2 == 0 else "BL",n,
                  up(a)+((1,-1),)+up(b)+((1,1),)+tail,n,
                  up(a)+((1,0),)+up(b)+((1,0),)+tail)
assert dimension(2,((1,1),)*3,3) == 2
assert dimension(2,((1,1),),3) == 1
first = ordered(2,((1,1),(1,1)))
second = ordered(2,((1,1),(1,0),(1,1),(1,0)))
assert first == ((0,1),(1,0)) and second == ((0,2),(0,0))
assert canonical(first) != canonical(second)
false_left = ((1,1),(1,-1),(1,1),(1,1))
false_right = ((1,1),(1,0),(1,1),(1,0))
assert len(ordered(4,false_left)) == len(ordered(4,false_right)) == 4
assert canonical(ordered(4,false_left)) != canonical(ordered(4,false_right))
print(json.dumps({"status":"PASS_INDEPENDENT_NECESSARY_INVARIANT_STRESS",
    "child_self_pid":os.getpid(),"completed_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
    "python":sys.version,"scheme_cases":dict(sorted(counts.items())),
    "total_scheme_cases":sum(counts.values()),"necessary_invariant_comparisons":comparisons,
    "fields":[3,5],"exchange_block_scope":"All virtual words of lengths0,1,2 at total unrestricted counts2,3,4,5",
    "other_scope":"C/BC all blocks length0,1; T/D all prefix words length0,1,2; even counts2,4,6",
    "false_T_R_zero_shift_controls_distinguished":True,
    "author_checker_imported":False,
    "limits":["Necessary finite invariants, not a link-equivalence or proof oracle",
              "Universal proof and imported Markov theorems require separate mathematical review",
              "No historical priority, human peer review, formal certification or publication assertion"]},indent=2))
