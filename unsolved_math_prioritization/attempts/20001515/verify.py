#!/usr/bin/env python3
"""Exact finite certificate checks for the rank-455 two-cube construction.

Standard library only. No search, network, external corpus, or floating point.
The proof still uses the standard cubical link/Cartan--Hadamard theorem.
"""
import itertools
import json
from pathlib import Path


def inv_word(word):
    return tuple(-x for x in reversed(word))


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
    return {w[k:] + w[:k] for w in (word, inv_word(word))
            for k in range(len(word))}


def links(vertices, edges, squares):
    """Edges are integer IDs -> (initial, terminal), faces are oriented IDs."""
    answer = {v: {"vertices": set(), "edges": set()} for v in vertices}
    for e, (u, v) in edges.items():
        answer[u]["vertices"].add(e)
        answer[v]["vertices"].add(-e)

    def ends(e):
        u, v = edges[abs(e)]
        return (u, v) if e > 0 else (v, u)

    for face in squares:
        assert len(face) == 4
        for incoming, outgoing in zip(face, face[1:] + face[:1]):
            assert ends(incoming)[1] == ends(outgoing)[0], "face not closed"
            v = ends(incoming)[1]
            pair = frozenset((-incoming, outgoing))
            assert len(pair) == 2, "loop in a link"
            assert pair not in answer[v]["edges"], "duplicate link edge"
            answer[v]["edges"].add(pair)
    return answer


def cliques(verts, edge_set, size):
    return {frozenset(c) for c in itertools.combinations(sorted(verts), size)
            if all(frozenset(p) in edge_set
                   for p in itertools.combinations(c, 2))}


# K generators 1=x, 2=y, 3=b.
K_EDGES = {1: (0, 0), 2: (0, 0), 3: (0, 0)}
K_FACES = [(1, 2, -1, -2), (3, 1, -3, -2)]
K_LINK = links([0], K_EDGES, K_FACES)[0]
assert len(K_LINK["vertices"]) == 6
assert len(K_LINK["edges"]) == 8
assert not cliques(K_LINK["vertices"], K_LINK["edges"], 3)

# Q edges 1=p, 2=q, 3=r, 4=s, 5=d, 6=e.
Q_EDGES = {1: ("B", "A"), 2: ("A", "C"), 3: ("D", "C"),
           4: ("B", "D"), 5: ("A", "B"), 6: ("C", "A")}
Q_FACES = [(1, 2, -3, -4), (5, 1, -6, -2)]
Q_LABELS = {1: 1, 2: 2, 3: 1, 4: 2, 5: 3, 6: 3}
Q_LINKS = links("ABCD", Q_EDGES, Q_FACES)
LAMBDA = {1: 2, 2: 1, 3: -3}


def on_letter(mapping, letter):
    return (1 if letter > 0 else -1) * mapping[abs(letter)]


def mapped_word(mapping, word):
    return tuple(on_letter(mapping, e) for e in word)


K_BOUNDARIES = set().union(*(dihedral_words(f) for f in K_FACES))
for face in K_FACES:
    assert mapped_word(LAMBDA, face) in K_BOUNDARIES
for e in K_EDGES:
    assert on_letter(LAMBDA, on_letter(LAMBDA, e)) == e
for face in Q_FACES:
    image = mapped_word(Q_LABELS, face)
    assert image in K_BOUNDARIES
    assert mapped_word(LAMBDA, image) in K_BOUNDARIES

EXPECTED_LINKS = {
    "A": {-3, -1, 2, 3}, "B": {-3, 1, 2},
    "C": {-1, -2, 3}, "D": {1, -2},
}
link_report = {}
for v, link in Q_LINKS.items():
    image_vertices = {on_letter(Q_LABELS, e) for e in link["vertices"]}
    image_edges = {frozenset(on_letter(Q_LABELS, e) for e in pair)
                   for pair in link["edges"]}
    assert len(image_vertices) == len(link["vertices"]), "link not injective"
    assert image_vertices == EXPECTED_LINKS[v]
    induced = {pair for pair in K_LINK["edges"] if pair <= image_vertices}
    assert image_edges == induced, "link image not full"
    link_report[v] = {"directions": sorted(image_vertices),
                      "edges": sorted(sorted(e) for e in image_edges)}

# Fundamental group of Q: collapse tree p,q,s. Relators become r^-1, d e^-1.
tree = {1, 2, 4}
collapsed = [reduce_word(e for e in face if abs(e) not in tree)
             for face in Q_FACES]
assert collapsed == [(-3,), (5, -6)]
assert mapped_word(Q_LABELS, (5, 1)) == (3, 1)
assert mapped_word(LAMBDA, (3, 1)) == (-3, 2)

# Link of Z from product-cell incidences. Directions for its four new edges
# are +/-4,...,+/-7. At each end product-square corners give cone edges;
# product-cube corners give cone triangles.
Z_VERTS = set(K_LINK["vertices"])
Z_EDGES = set(K_LINK["edges"])
Z_TRIANGLES = set()
for k, v in enumerate("ABCD", 4):
    for end in (0, 1):
        apex = k if end == 0 else -k
        Z_VERTS.add(apex)
        label_map = Q_LABELS if end == 0 else {
            e: on_letter(LAMBDA, a) for e, a in Q_LABELS.items()}
        for direction in Q_LINKS[v]["vertices"]:
            pair = frozenset((apex, on_letter(label_map, direction)))
            assert pair not in Z_EDGES
            Z_EDGES.add(pair)
        for pair in Q_LINKS[v]["edges"]:
            triangle = frozenset([apex] + [on_letter(label_map, d) for d in pair])
            assert len(triangle) == 3 and triangle not in Z_TRIANGLES
            Z_TRIANGLES.add(triangle)
assert (len(Z_VERTS), len(Z_EDGES), len(Z_TRIANGLES)) == (14, 32, 16)
assert cliques(Z_VERTS, Z_EDGES, 3) == Z_TRIANGLES, "missing triangle"
assert not cliques(Z_VERTS, Z_EDGES, 4), "missing higher simplex"
cell_counts = [1, len(K_EDGES) + 4, len(K_FACES) + len(Q_EDGES), len(Q_FACES)]
assert cell_counts == [1, 7, 8, 2]
assert sum((-1)**i * n for i, n in enumerate(cell_counts)) == 0

# Independent group-word evaluation in the exact target F(a,b,c) semidirect Z.
# Pairs represent f t^n, and multiplication is (f,n)(g,m)=(f phi^n(g),n+m).
PHI = {1: (1,), 2: (1, 2), 3: (2, 3, 2)}
PHI_INV = {1: (1,), 2: (-1, 2), 3: (-2, 1, 3, -2, 1)}


def substitute(word, mapping):
    out = ()
    for e in word:
        w = mapping[abs(e)]
        out = reduce_word(out + (w if e > 0 else inv_word(w)))
    return out


for e in (1, 2, 3):
    assert substitute(PHI[e], PHI_INV) == (e,)
    assert substitute(PHI_INV[e], PHI) == (e,)


def phi_power(word, n):
    for _ in range(abs(n)):
        word = substitute(word, PHI if n >= 0 else PHI_INV)
    return word


def mult(a, b):
    return reduce_word(a[0] + phi_power(b[0], a[1])), a[1] + b[1]


def inverse(a):
    return phi_power(inv_word(a[0]), -a[1]), -a[1]


identity = ((), 0)
gens = {1: ((), 1), 2: ((-1,), 1), 3: ((2,), 0), 4: ((-3,), -1)}
# x=t, y=a^-1 t, b=b, z=c^-1 t^-1.


def eval_word(word):
    out = identity
    for e in word:
        out = mult(out, gens[abs(e)] if e > 0 else inverse(gens[abs(e)]))
    return out


hnn_relator = (-4, 3, 1, 4, -2, 3)
for rel in K_FACES + [hnn_relator]:
    assert eval_word(rel) == identity
# Vertical generators solved using the p,q,s spanning-tree relations.
vertical = {"A": (4,), "B": (1, 4, -2), "C": (-2, 4, 1),
            "D": (-2, 1, 4, -2, 1)}
product_relators = {}
for e, (u, v) in Q_EDGES.items():
    bottom = Q_LABELS[e]
    top = on_letter(LAMBDA, bottom)
    rel = (bottom,) + vertical[v] + (-top,) + inv_word(vertical[u])
    assert eval_word(rel) == identity
    product_relators[str(e)] = list(rel)
# Recover the original a,b,c,t from the new generators exactly.
assert eval_word((1, -2)) == ((1,), 0)     # a=x y^-1
assert eval_word((3,)) == ((2,), 0)       # b=b
assert eval_word((-1, -4)) == ((3,), 0)   # c=(z x)^-1
assert eval_word((1,)) == ((), 1)         # t=x

# Falsification controls: wrong b-sign destroys the cubical symmetry;
# deleting any triangle destroys flagness of the 3-dimensional construction.
wrong_lambda = {1: 2, 2: 1, 3: 3}
assert mapped_word(wrong_lambda, K_FACES[1]) not in K_BOUNDARIES
for triangle in Z_TRIANGLES:
    assert cliques(Z_VERTS, Z_EDGES, 3) != Z_TRIANGLES - {triangle}

report = {
    "status": "PASS", "method": "exact finite incidence and free-word checks",
    "K_link": {"vertices": 6, "edges": 8, "triangles": 0},
    "Q_link_images": link_report,
    "Q_tree_collapsed_relators": [list(r) for r in collapsed],
    "Z_cells_by_dimension": cell_counts,
    "Z_link": {"vertices": 14, "edges": 32, "triangles": 16,
               "four_vertex_cliques": 0, "flag": True},
    "product_square_relators_after_tree_elimination": product_relators,
    "exact_target_relators_verified": len(K_FACES) + 1 + len(Q_EDGES),
    "original_generators_recovered": 4,
    "negative_controls": 17,
    "limitation": "Finite certificate checks supplement the written proof; standard cubical link and Cartan-Hadamard theorems supply the global CAT(0) conclusion. Historical novelty and live source identity are not certified by this script.",
}
print(json.dumps(report, indent=2, sort_keys=True))
