#!/usr/bin/env python3
"""Independent finite controls, standard library only; no theorem-by-enumeration claim.

Run in any directory. JSON is printed to stdout. This script changes no files.
"""
from itertools import product, combinations
import json


def pairs(vertices, adjacent):
    return [(u, v) for u in vertices for v in vertices if adjacent(u, v)]


def grid(sides):
    return list(product(*(range(m + 1) for m in sides)))


def near(u, v):
    return all(abs(x-y) <= 1 for x,y in zip(u,v))


def boundary(u, sides):
    return any(x in (0, m) for x,m in zip(u,sides))


def alpha(j, i):
    return i - (i > j)


def graph_targets(q):
    off = list(combinations(range(q), 2))
    for bits in product((0,1), repeat=len(off)):
        A = [[i == j for j in range(q)] for i in range(q)]
        for (i,j),yes in zip(off,bits):
            A[i][j] = A[j][i] = bool(yes)
        yield A


def contiguity_control(sides, max_q):
    V = grid(sides); index = {v:i for i,v in enumerate(V)}
    E = [(index[u],index[v]) for u,v in pairs(V,near)]
    maximal = [tuple(index[tuple(x+d for x,d in zip(lo,delta))]
                      for delta in product((0,1),repeat=len(sides)))
               for lo in product(*(range(m) for m in sides))]
    total = 0
    for q in range(1,max_q+1):
        for A in graph_targets(q):
            maps = [f for f in product(range(q),repeat=len(V))
                    if all(A[f[u]][f[v]] for u,v in E)]
            for f in maps:
                for g in maps:
                    strong = all(A[f[u]][g[v]] for u,v in E)
                    contiguous = True
                    for C in maximal:
                        labels = set(f[i] for i in C) | set(g[i] for i in C)
                        if not all(A[x][y] for x,y in combinations(labels,2)):
                            contiguous = False; break
                    assert strong == contiguous
                    total += 1
    return total


# Independently enumerate octahedral endomorphisms using adjacency-matrix indices.
V = tuple(range(6))
opp = (1,0,3,2,5,4)
A = [[j != opp[i] for j in V] for i in V]
E = [(i,j) for i in V for j in V if A[i][j]]
maps = [f for f in product(V,repeat=6) if f[1] == 1
        and all(A[f[i]][f[j]] for i,j in E)]
idmap = V
strong_neighbors = [f for f in maps if all(A[i][f[j]] for i,j in E)]
assert len(maps) == 1057 and strong_neighbors == [idmap]
h = (2,1,1,1,1,1); constant = (1,)*6
assert h in maps and constant in maps
assert all(A[i][h[i]] and A[h[i]][1] for i in V)
assert not A[0][h[3]] and A[0][3]
cliques = [s for k in range(1,7) for s in combinations(V,k)
           if all(A[i][j] for i,j in combinations(s,2))]
f_vector = [sum(len(s)==k for s in cliques) for k in range(1,5)]
assert f_vector == [6,12,8,0]
# Every maximal face makes one of two choices from each antipodal pair.
assert set(s for s in cliques if len(s)==3) == set(
    tuple(sorted(c)) for c in product((0,1),(2,3),(4,5)))

# Exhaustive one-dimensional cross-conditions, including the constant m=0 case.
collar_cases = 0
for m in range(81):
    for j in range(m):
        for u in range(m+2):
            for v in range(m+2):
                if abs(u-v)<=1:
                    assert abs(alpha(j,u)-alpha(j+1,v))<=1
                    collar_cases += 1
assert collar_cases == 534600

# Product equality: all elementary cube subsets in dimensions one to three.
cube_subsets = 0
for n in range(1,4):
    C = list(product((0,1),repeat=n))
    for mask in range(1 << len(C)):
        S = [C[i] for i in range(len(C)) if mask >> i & 1]
        categorical = all(len({p[k] for p in S}) <= 2 for k in range(n))
        flag = all(near(u,v) for u,v in combinations(S,2))
        assert categorical == flag
        cube_subsets += 1

# Include negative cases outside any unit cube, not only unit-cube subsets.
product_graph_subsets = 0
for n in range(1,4):
    W = grid((2,)*n)
    elementary = [set(tuple(a+d for a,d in zip(lo,delta))
                      for delta in product((0,1),repeat=n))
                  for lo in product((0,1),repeat=n)]
    sizes = range(len(W)+1) if n<3 else range(4)
    for size in sizes:
        for S in combinations(W,size):
            generated_simplex = any(set(S) <= C for C in elementary)
            flag_simplex = all(near(u,v) for u,v in combinations(S,2))
            assert generated_simplex == flag_simplex
            product_graph_subsets += 1
assert product_graph_subsets == 3824

# Strong maps versus contiguity, including genuine 2D and 3D grid domains.
contiguity_counts = {
    'I2_targets_up_to_4': contiguity_control((2,),4),
    'I1xI1_targets_up_to_4': contiguity_control((1,1),4),
    'I2xI1_targets_up_to_3': contiguity_control((2,1),3),
    'I1xI1xI1_targets_up_to_2': contiguity_control((1,1,1),2),
}
assert contiguity_counts['I2_targets_up_to_4'] == 61885

# Nonzero degree witness: published generator labels (read bottom row upwards).
b = -1
rows = [(-1,)*5, (-1,3,3,-2,-1), (-1,2,1,-2,-1),
        (-1,2,-3,-3,-1), (-1,)*5]
T = {(x,y): rows[y][x] for x,y in grid((4,4))}
adj = lambda x,y: x != -y
assert all(adj(T[u],T[v]) for u,v in pairs(grid((4,4)),near))
assert all(T[u] == b for u in T if boundary(u,(4,4)))

def degree(f, sides):
    count = 0
    for x in range(sides[0]):
        for y in range(sides[1]):
            for triangle in (((x,y),(x+1,y),(x+1,y+1)),
                             ((x,y),(x+1,y+1),(x,y+1))):
                labels = tuple(f[p] for p in triangle)
                if set(labels) == {1,2,3}:
                    inv = sum(labels[i] > labels[j] for i in range(3) for j in range(i+1,3))
                    count += (-1)**inv
    return count
assert degree(T,(4,4)) == 1
inverse = {(x,y):T[(4-x,y)] for x,y in T}
assert degree(inverse,(4,4)) == -1

# Check every step in the collar homotopy on this nontrivial representative.
multidimensional_steps = 0
for axis in (0,1):
    new_sides = [4,4]; new_sides[axis] += 1
    U = grid(new_sides); EE = pairs(U,near)
    slices = []
    for j in range(4,-1,-1):
        f = {}
        for u in U:
            v = list(u); v[axis] = alpha(j,v[axis]); f[u] = T[tuple(v)]
        assert all(f[u] == b for u in U if boundary(u,new_sides))
        assert degree(f,new_sides) == 1
        slices.append(f)
    for f,g in zip(slices,slices[1:]):
        assert all(adj(f[u],g[v]) for u,v in EE)
        multidimensional_steps += 1

# Concatenation, diagonal product, reflection and zero extension control degree.
side_by_side = {(x,y): T[(x,y)] if x<=4 else T[(x-5,y)]
                for x,y in grid((9,4))}
diagonal = {(x,y): T[(x,y)] if x<=4 and y<=4 else
             T[(x-5,y-5)] if x>=5 and y>=5 else b
             for x,y in grid((9,9))}
for f,sides in ((side_by_side,(9,4)),(diagonal,(9,9))):
    assert all(adj(f[u],f[v]) for u,v in pairs(grid(sides),near))
    assert degree(f,sides) == 2
# Slide the right block through five rows, using actual alpha chains in a
# disjoint slab. Every intermediate map satisfies the strong cross-condition.
previous = diagonal
local_slide_steps = 0
for shift in range(5,0,-1):
    small = {(x,y): T[(x,y-(shift-1))] if shift-1<=y<=shift+3 else b
             for x,y in grid((4,8))}
    slices = []
    for j in range(9):
        current = {(x,y): T[(x,y)] if x<=4 and y<=4 else
                   small[(x-5,alpha(j,y))] if x>=5 else b
                   for x,y in grid((9,9))}
        assert all(current[u]==b for u in current if boundary(u,(9,9)))
        assert degree(current,(9,9)) == 2
        slices.append(current)
    assert slices[0] == previous
    for f,g in zip(slices,slices[1:]):
        assert all(adj(f[u],g[v]) for u,v in pairs(grid((9,9)),near))
        local_slide_steps += 1
    previous = slices[-1]
assert all(previous[(x,y)] == side_by_side[(x,y)] for x,y in side_by_side)
assert all(previous[(x,y)] == b for x,y in previous if y>4)

# Uniform k-subdivision is a string of allowed repeated-coordinate moves.
subdivision_degrees = {}
for k in (2,3):
    m = 5*k-1
    f = {(x,y):T[(x//k,y//k)] for x,y in grid((m,m))}
    assert all(adj(f[u],f[v]) for u,v in pairs(grid((m,m)),near))
    assert all(f[u]==b for u in f if boundary(u,(m,m)))
    subdivision_degrees[str(k)] = degree(f,(m,m))
    assert subdivision_degrees[str(k)] == 1

result = {
    'result':'PASS',
    'scope':'Supplemental finite controls only; the all-dimensional theorem is justified by the source and symbolic bridge audit.',
    'octahedral_based_endomorphisms':len(maps),
    'octahedral_strong_identity_neighbors':len(strong_neighbors),
    'octahedral_clique_f_vector':f_vector,
    'two_step_based_box_contraction':True,
    'collar_cross_conditions':collar_cases,
    'elementary_cube_subsets':cube_subsets,
    'product_graph_subsets_including_negative_cases':product_graph_subsets,
    'strong_contiguity_comparisons':contiguity_counts,
    'nonzero_generator_degree':degree(T,(4,4)),
    'reflection_degree':degree(inverse,(4,4)),
    'collar_steps_on_nonzero_generator':multidimensional_steps,
    'horizontal_product_degree':degree(side_by_side,(9,4)),
    'strong_local_slide_steps':local_slide_steps,
    'diagonal_product_degree':degree(diagonal,(9,9)),
    'subdivision_degrees':subdivision_degrees,
}
print(json.dumps(result,indent=2,sort_keys=True))
