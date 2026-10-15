"""Finite base-complex checks only; no explicit completion Q is used."""
from itertools import combinations
from collections import Counter

BOUNDARIES = ('xyXY', 'bxBY')
INVERSE = dict(zip('xybXYB', 'XYBxyb'))
LAMBDA = dict(zip('xybXYB', 'yxBYXb'))

def corners(word):
    return [tuple(sorted((INVERSE[word[i-1]], word[i]))) for i in range(len(word))]

def dihedral_words(word):
    inverse = ''.join(INVERSE[c] for c in word[::-1])
    return {w[i:] + w[:i] for w in (word, inverse) for i in range(len(w))}

edge_counts = Counter(edge for w in BOUNDARIES for edge in corners(w))
assert all(a != b for a, b in edge_counts)
assert all(count == 1 for count in edge_counts.values())
vertices = set(INVERSE)
triangles = [triple for triple in combinations(vertices, 3)
             if all(tuple(sorted(pair)) in edge_counts for pair in combinations(triple, 2))]
assert not triangles
assert all(LAMBDA[LAMBDA[c]] == c for c in vertices)
for w in BOUNDARIES:
    assert ''.join(LAMBDA[c] for c in w) in dihedral_words(w)
# The uncompleted bx circle fails local fullness at its intermediate vertex.
assert tuple(sorted(('B', 'x'))) in edge_counts
print({'base_link_vertices': len(vertices), 'base_link_edges': len(edge_counts),
       'duplicate_edges': False, 'triangles': triangles,
       'lambda_involutive': True, 'lambda_preserves_square_boundaries': True,
       'uncompleted_bx_circle_not_local_isometry': True})
