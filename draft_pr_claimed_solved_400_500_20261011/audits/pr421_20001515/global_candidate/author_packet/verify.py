"""Exact finite certificate checks for the rank-455 two-cube construction.

Standard library only. No search, network, external corpus, or floating point.
The proof still uses the standard cubical link/Cartan--Hadamard theorem.
"""
import itertools
import json
from pathlib import Path

def inv_word(word):
    return tuple((-x for x in reversed(word)))

def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)

def dihedral_words(word):
    word = tuple(word)
    return {w[k:] + w[:k] for w in (word, inv_word(word)) for k in range(len(word))}

def links(vertices, edges, squares):
    """Edges are integer IDs -> (initial, terminal), faces are oriented IDs."""
    answer = {v: {'vertices': set(), 'edges': set()} for v in vertices}
    for e, (u, v) in edges.items():
        answer[u]['vertices'].add(e)
        answer[v]['vertices'].add(-e)

    def ends(e):
        u, v = edges[abs(e)]
        return (u, v) if e > 0 else (v, u)
    for face in squares:
        if not len(face) == 4:
            raise AssertionError()
        for incoming, outgoing in zip(face, face[1:] + face[:1]):
            if not ends(incoming)[1] == ends(outgoing)[0]:
                raise AssertionError('face not closed')
            v = ends(incoming)[1]
            pair = frozenset((-incoming, outgoing))
            if not len(pair) == 2:
                raise AssertionError('loop in a link')
            if not pair not in answer[v]['edges']:
                raise AssertionError('duplicate link edge')
            answer[v]['edges'].add(pair)
    return answer

def cliques(verts, edge_set, size):
    return {frozenset(c) for c in itertools.combinations(sorted(verts), size) if all((frozenset(p) in edge_set for p in itertools.combinations(c, 2)))}
K_EDGES = {1: (0, 0), 2: (0, 0), 3: (0, 0)}
K_FACES = [(1, 2, -1, -2), (3, 1, -3, -2)]
K_LINK = links([0], K_EDGES, K_FACES)[0]
if not len(K_LINK['vertices']) == 6:
    raise AssertionError()
if not len(K_LINK['edges']) == 8:
    raise AssertionError()
if not not cliques(K_LINK['vertices'], K_LINK['edges'], 3):
    raise AssertionError()
Q_EDGES = {1: ('B', 'A'), 2: ('A', 'C'), 3: ('D', 'C'), 4: ('B', 'D'), 5: ('A', 'B'), 6: ('C', 'A')}
Q_FACES = [(1, 2, -3, -4), (5, 1, -6, -2)]
Q_LABELS = {1: 1, 2: 2, 3: 1, 4: 2, 5: 3, 6: 3}
Q_LINKS = links('ABCD', Q_EDGES, Q_FACES)
LAMBDA = {1: 2, 2: 1, 3: -3}

def on_letter(mapping, letter):
    return (1 if letter > 0 else -1) * mapping[abs(letter)]

def mapped_word(mapping, word):
    return tuple((on_letter(mapping, e) for e in word))
K_BOUNDARIES = set().union(*(dihedral_words(f) for f in K_FACES))
for face in K_FACES:
    if not mapped_word(LAMBDA, face) in K_BOUNDARIES:
        raise AssertionError()
for e in K_EDGES:
    if not on_letter(LAMBDA, on_letter(LAMBDA, e)) == e:
        raise AssertionError()
for face in Q_FACES:
    image = mapped_word(Q_LABELS, face)
    if not image in K_BOUNDARIES:
        raise AssertionError()
    if not mapped_word(LAMBDA, image) in K_BOUNDARIES:
        raise AssertionError()
EXPECTED_LINKS = {'A': {-3, -1, 2, 3}, 'B': {-3, 1, 2}, 'C': {-1, -2, 3}, 'D': {1, -2}}
link_report = {}
for v, link in Q_LINKS.items():
    image_vertices = {on_letter(Q_LABELS, e) for e in link['vertices']}
    image_edges = {frozenset((on_letter(Q_LABELS, e) for e in pair)) for pair in link['edges']}
    if not len(image_vertices) == len(link['vertices']):
        raise AssertionError('link not injective')
    if not image_vertices == EXPECTED_LINKS[v]:
        raise AssertionError()
    induced = {pair for pair in K_LINK['edges'] if pair <= image_vertices}
    if not image_edges == induced:
        raise AssertionError('link image not full')
    link_report[v] = {'directions': sorted(image_vertices), 'edges': sorted((sorted(e) for e in image_edges))}
tree = {1, 2, 4}
collapsed = [reduce_word((e for e in face if abs(e) not in tree)) for face in Q_FACES]
if not collapsed == [(-3,), (5, -6)]:
    raise AssertionError()
if not mapped_word(Q_LABELS, (5, 1)) == (3, 1):
    raise AssertionError()
if not mapped_word(LAMBDA, (3, 1)) == (-3, 2):
    raise AssertionError()
Z_VERTS = set(K_LINK['vertices'])
Z_EDGES = set(K_LINK['edges'])
Z_TRIANGLES = set()
for k, v in enumerate('ABCD', 4):
    for end in (0, 1):
        apex = k if end == 0 else -k
        Z_VERTS.add(apex)
        label_map = Q_LABELS if end == 0 else {e: on_letter(LAMBDA, a) for e, a in Q_LABELS.items()}
        for direction in Q_LINKS[v]['vertices']:
            pair = frozenset((apex, on_letter(label_map, direction)))
            if not pair not in Z_EDGES:
                raise AssertionError()
            Z_EDGES.add(pair)
        for pair in Q_LINKS[v]['edges']:
            triangle = frozenset([apex] + [on_letter(label_map, d) for d in pair])
            if not (len(triangle) == 3 and triangle not in Z_TRIANGLES):
                raise AssertionError()
            Z_TRIANGLES.add(triangle)
if not (len(Z_VERTS), len(Z_EDGES), len(Z_TRIANGLES)) == (14, 32, 16):
    raise AssertionError()
if not cliques(Z_VERTS, Z_EDGES, 3) == Z_TRIANGLES:
    raise AssertionError('missing triangle')
if not not cliques(Z_VERTS, Z_EDGES, 4):
    raise AssertionError('missing higher simplex')
cell_counts = [1, len(K_EDGES) + 4, len(K_FACES) + len(Q_EDGES), len(Q_FACES)]
if not cell_counts == [1, 7, 8, 2]:
    raise AssertionError()
if not sum(((-1) ** i * n for i, n in enumerate(cell_counts))) == 0:
    raise AssertionError()
PHI = {1: (1,), 2: (1, 2), 3: (2, 3, 2)}
PHI_INV = {1: (1,), 2: (-1, 2), 3: (-2, 1, 3, -2, 1)}

def substitute(word, mapping):
    out = ()
    for e in word:
        w = mapping[abs(e)]
        out = reduce_word(out + (w if e > 0 else inv_word(w)))
    return out
for e in (1, 2, 3):
    if not substitute(PHI[e], PHI_INV) == (e,):
        raise AssertionError()
    if not substitute(PHI_INV[e], PHI) == (e,):
        raise AssertionError()

def phi_power(word, n):
    for _ in range(abs(n)):
        word = substitute(word, PHI if n >= 0 else PHI_INV)
    return word

def mult(a, b):
    return (reduce_word(a[0] + phi_power(b[0], a[1])), a[1] + b[1])

def inverse(a):
    return (phi_power(inv_word(a[0]), -a[1]), -a[1])
identity = ((), 0)
gens = {1: ((), 1), 2: ((-1,), 1), 3: ((2,), 0), 4: ((-3,), -1)}

def eval_word(word):
    out = identity
    for e in word:
        out = mult(out, gens[abs(e)] if e > 0 else inverse(gens[abs(e)]))
    return out
hnn_relator = (-4, 3, 1, 4, -2, 3)
for rel in K_FACES + [hnn_relator]:
    if not eval_word(rel) == identity:
        raise AssertionError()
vertical = {'A': (4,), 'B': (1, 4, -2), 'C': (-2, 4, 1), 'D': (-2, 1, 4, -2, 1)}
product_relators = {}
for e, (u, v) in Q_EDGES.items():
    bottom = Q_LABELS[e]
    top = on_letter(LAMBDA, bottom)
    rel = (bottom,) + vertical[v] + (-top,) + inv_word(vertical[u])
    if not eval_word(rel) == identity:
        raise AssertionError()
    product_relators[str(e)] = list(rel)
if not eval_word((1, -2)) == ((1,), 0):
    raise AssertionError()
if not eval_word((3,)) == ((2,), 0):
    raise AssertionError()
if not eval_word((-1, -4)) == ((3,), 0):
    raise AssertionError()
if not eval_word((1,)) == ((), 1):
    raise AssertionError()
wrong_lambda = {1: 2, 2: 1, 3: 3}
if not mapped_word(wrong_lambda, K_FACES[1]) not in K_BOUNDARIES:
    raise AssertionError()
for triangle in Z_TRIANGLES:
    if not cliques(Z_VERTS, Z_EDGES, 3) != Z_TRIANGLES - {triangle}:
        raise AssertionError()
report = {'status': 'PASS', 'method': 'exact finite incidence and free-word checks', 'K_link': {'vertices': 6, 'edges': 8, 'triangles': 0}, 'Q_link_images': link_report, 'Q_tree_collapsed_relators': [list(r) for r in collapsed], 'Z_cells_by_dimension': cell_counts, 'Z_link': {'vertices': 14, 'edges': 32, 'triangles': 16, 'four_vertex_cliques': 0, 'flag': True}, 'product_square_relators_after_tree_elimination': product_relators, 'exact_target_relators_verified': len(K_FACES) + 1 + len(Q_EDGES), 'original_generators_recovered': 4, 'negative_controls': 17, 'limitation': 'Finite certificate checks supplement the written proof; standard cubical link and Cartan-Hadamard theorems supply the global CAT(0) conclusion. Historical novelty and live source identity are not certified by this script.'}
print(json.dumps(report, indent=2, sort_keys=True))
