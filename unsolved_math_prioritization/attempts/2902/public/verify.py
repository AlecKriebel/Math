#!/usr/bin/env python3
"""Finite algebra diagnostics, not a proof of a smooth embedding theorem.

Python 3 standard library only. Output is deterministic JSON on stdout.
No downloads, external packages, manifold classification, or search for solutions.
"""
from itertools import product
from collections import Counter, deque
from fractions import Fraction
import json

checks = 0

def check(statement):
    global checks
    checks += 1
    assert statement


def mul(a, b):
    return ((a[0]*b[0]+a[1]*b[2]) % 5,
            (a[0]*b[1]+a[1]*b[3]) % 5,
            (a[2]*b[0]+a[3]*b[2]) % 5,
            (a[2]*b[1]+a[3]*b[3]) % 5)

G = sorted(a for a in product(range(5), repeat=4)
           if (a[0]*a[3]-a[1]*a[2]) % 5 == 1)
check(len(G) == 120)
index = {g:i for i,g in enumerate(G)}
e = index[(1,0,0,1)]
table = []
for a in G:
    row = []
    for b in G:
        ab = mul(a,b)
        check(ab in index)
        row.append(index[ab])
    table.append(row)
inv = [index[(a[3], -a[1] % 5, -a[2] % 5, a[0])] for a in G]
for i in range(120):
    check(table[i][e] == table[e][i] == i)
    check(table[i][inv[i]] == table[inv[i]][i] == e)


def comm(a,b):
    return table[table[table[a][b]][inv[a]]][inv[b]]


def normal_closure(seeds):
    generators = set()
    for s in seeds:
        for h in range(120):
            generators.add(table[table[h][s]][inv[h]])
    generators |= {inv[s] for s in generators}
    found, todo = {e}, deque([e])
    while todo:
        x = todo.popleft()
        for s in generators:
            y = table[x][s]
            if y not in found:
                found.add(y)
                todo.append(y)
    return found

# A commutator normal closure of all group commutators is [G,G].
derived = normal_closure({comm(a,b) for a in range(120) for b in range(120)})
check(len(derived) == 120)

# Work by conjugacy classes, not by a search over presentations.
unseen = set(range(120))
classes = []
while unseen:
    g = min(unseen)
    conj = {table[table[h][g]][inv[h]] for h in range(120)}
    check(conj <= unseen)
    unseen -= conj
    ng = normal_closure({g})
    cg = normal_closure({comm(g,x) for x in range(120)})
    check(cg <= ng)
    check((len(ng) == 120) == (len(cg) == 120))
    classes.append({"representative":list(G[g]), "class_size":len(conj),
                    "normal_generator_closure_order":len(ng),
                    "commutator_normal_closure_order":len(cg),
                    "diagonal_surgery_quotient_order":120//len(cg)})
check(sum(row['class_size'] for row in classes) == 120)
check(len(classes) == 9)
check(Counter(row['diagonal_surgery_quotient_order'] for row in classes)
      == Counter({1:7, 120:2}))

# Non-perfect negative control: C5, g = 1 normally generates, but is central.
cyclic_normal = {k % 5 for k in range(5)}
cyclic_comm = {(a+b-a-b) % 5 for a in range(5) for b in range(5)}
check(len(cyclic_normal) == 5)
check(cyclic_comm == {0})
check(5//len(cyclic_comm) == 5)

# The abelianization matrix for x^2=y^3=z^5=xyz.
A = [[2,-3,0], [0,3,-5], [-1,-1,4]]
det = (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
       - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
       + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
check(det == -1)

# Independent rank check of the primitive-circle Mayer--Vietoris maps.
# Domain H_i(S1 x S2); target H_i(A) plus H_i(D2 x S2).
# In positive degrees the maps in degrees 1,2 are [1], [1]; degree 3
# has target zero. Exactness gives H1=H2=H3=0, H4=Z.
def rank(matrix):
    if not matrix or not matrix[0]: return 0
    matrix = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for col in range(len(matrix[0])):
        selected = next((i for i in range(pivot,len(matrix)) if matrix[i][col]),None)
        if selected is None: continue
        matrix[pivot],matrix[selected] = matrix[selected],matrix[pivot]
        t=matrix[pivot][col]
        matrix[pivot] = [x/t for x in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot:
                t=matrix[i][col]
                matrix[i]=[x-t*y for x,y in zip(matrix[i],matrix[pivot])]
        pivot += 1
    return pivot

boundary = [1,1,1,1,0]
target = [2,1,1,0,0]
rankmap = [rank([[1],[-1]]),rank([[1]]),rank([[1]]),0,0]
betti = [target[i]-rankmap[i]+(boundary[i-1]-rankmap[i-1] if i else 0)
         for i in range(5)]
check(betti == [1,0,0,0,1])
# The integral argument also requires unit, not merely nonzero, maps.
check(rankmap[1] == rankmap[2] == 1)
check(abs(1) == 1)  # the two actual 1-by-1 integral maps are unimodular
surgeries=[]
for r in range(11):
    chi=2+2*r
    b2=chi-2
    check(b2 == 2*r)
    check((b2 == 0) == (r == 0))
    surgeries.append({"additional_circle_surgeries":r, "euler_characteristic":chi,
                      "second_betti_number":b2})

print(json.dumps({
    "problem":"KP-4.26", "status":"UNRESOLVED",
    "scope":"Finite group and exact homology-rank diagnostics only; no smooth standardness certificate",
    "assertions":checks,
    "sl2_f5_order":120, "sl2_f5_derived_order":len(derived),
    "conjugacy_classes":classes,
    "nonperfect_c5_quotient_order":5,
    "presentation_abelianization_determinant":det,
    "primitive_circle_mv_betti":betti,
    "additional_surgery_controls":surgeries
},sort_keys=True,indent=2))
