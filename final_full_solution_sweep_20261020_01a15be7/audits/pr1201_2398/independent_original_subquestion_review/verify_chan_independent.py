#!/usr/bin/env python3
"""Independent exact exhaustive verifier of Chan's finite graph.

Author programs/certificates are not imported or executed. The graph is rebuilt
from its mathematical Cayley description. Optional inert public edge-list and
graph6 inputs must match. The whole proper-three-colouring space of G-0 is
enumerated, modulo global colour permutation, with no time/node cutoff.
"""
import argparse
import hashlib
import json
from pathlib import Path

N = 60
GENERATORS = ((1, 0), (11, 0), (5, 1), (7, 2), (6, 0), (6, 3))
EDGE_SHA = '85914250312a4fe8d1a67d747fea2ee1772c9762796af90095efa61fb4c0400c'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def mul(a, b):
    e, i = divmod(a, 5)
    f, j = divmod(b, 5)
    return 5*((e+f) % 12)+(i+pow(2, e, 5)*j) % 5


def rebuild():
    edges = set()
    for u in range(N):
        for e, i in GENERATORS:
            v = mul(u, 5*e+i)
            require(u != v, 'Loop in mathematical construction')
            edges.add(tuple(sorted((u, v))))
    require(len(edges) == 180, 'Unexpected constructed size')
    return sorted(edges)


def parse_edges(raw):
    rows = []
    for line in raw.decode('ascii').splitlines():
        words = line.split()
        require(len(words) == 2, 'Edge row not a pair')
        u, v = map(int, words)
        require(0 <= u < v < N, 'Invalid ordered edge')
        rows.append((u, v))
    require(len(rows) == len(set(rows)) == 180, 'Duplicate or wrong edge count')
    return sorted(rows)


def parse_graph6(raw):
    data = raw.strip()
    require(len(data) == 296 and data[0]-63 == N, 'Unexpected graph6 order/length')
    values = [x-63 for x in data[1:]]
    require(all(0 <= x < 64 for x in values), 'Invalid graph6 character')
    bits = [(v >> shift) & 1 for v in values for shift in range(5, -1, -1)]
    edges = []; at = 0
    for v in range(1, N):
        for u in range(v):
            if bits[at]:
                edges.append((u, v))
            at += 1
    require(not any(bits[at:]), 'Nonzero graph6 padding')
    return sorted(edges)


def proper(edges, colours, omitted=None):
    require(len(colours) == N, 'Colouring dimension')
    require(all(c in range(3) for v, c in enumerate(colours) if v != omitted),
            'Invalid puncture colour')
    return all(u == omitted or v == omitted or colours[u] != colours[v] for u, v in edges)


def enumerate_puncture(adjacency):
    """All proper colourings of vertices1..59, modulo colour renaming.

    Unassigned vertices are selected by (number of distinct coloured neighbour
    colours, number of unassigned neighbours, degree, smallest label). Those
    criteria are invariant under colour renaming. Already introduced colours
    are all tried; of unused colours only the next label is tried. Every global
    colour-permutation orbit consequently has one retained first-use labelling.
    Zero available colours closes exactly that inconsistent branch.
    """
    colours = [-1]*N
    classes = [0, 0, 0]
    all_unassigned = ((1 << N)-1) ^ 1
    stats = {'nodes': 0, 'dead_ends': 0, 'leaves': 0, 'unbalanced_leaves': 0}
    digest = hashlib.sha256()
    first = None

    def visit(unassigned, used):
        nonlocal first
        stats['nodes'] += 1
        if unassigned == 0:
            stats['leaves'] += 1
            split = tuple((adjacency[0] & classes[c]).bit_count() for c in range(3))
            digest.update(bytes(colours[1:]))
            if first is None:
                first = colours.copy()
            if split != (2, 2, 2):
                stats['unbalanced_leaves'] += 1
                raise RuntimeError('COUNTEREXAMPLE: '+json.dumps({'colours':colours,'split':split}))
            return
        best = None; chosen = -1; forbidden = 0
        todo = unassigned
        while todo:
            bit = todo & -todo; todo ^= bit; v = bit.bit_length()-1
            mask = sum((1 << c) for c in range(3) if adjacency[v] & classes[c])
            if mask == 7:
                stats['dead_ends'] += 1
                return
            rank = (mask.bit_count(), (adjacency[v] & unassigned).bit_count(),
                    adjacency[v].bit_count(), -v)
            if best is None or rank > best:
                best, chosen, forbidden = rank, v, mask
        bit = 1 << chosen
        for c in range(min(used+1, 3)):
            if forbidden & (1 << c):
                continue
            colours[chosen] = c; classes[c] |= bit
            visit(unassigned ^ bit, max(used, c+1))
            classes[c] ^= bit; colours[chosen] = -1

    visit(all_unassigned, 0)
    require(first is not None and stats['leaves'] > 0, 'No puncture colouring')
    stats['ordered_leaf_colourings_sha256'] = digest.hexdigest()
    return stats, first


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edgelist', type=Path)
    parser.add_argument('--graph6', type=Path)
    args = parser.parse_args()
    edges = rebuild(); canonical = ''.join(f'{u} {v}\n' for u,v in edges).encode()
    require(hashlib.sha256(canonical).hexdigest() == EDGE_SHA, 'Constructed canonical source mismatch')
    inputs = {}
    if args.edgelist:
        raw = args.edgelist.read_bytes()
        require(parse_edges(raw) == edges and hashlib.sha256(raw).hexdigest() == EDGE_SHA,
                'Public edge list differs from independent construction')
        inputs['edgelist_sha256'] = hashlib.sha256(raw).hexdigest()
    if args.graph6:
        raw = args.graph6.read_bytes()
        require(parse_graph6(raw) == edges, 'Graph6 differs from independent construction')
        inputs['graph6_sha256'] = hashlib.sha256(raw).hexdigest()
    adjacency = [0]*N
    for u, v in edges:
        adjacency[u] |= 1 << v; adjacency[v] |= 1 << u
    require(all(x.bit_count() == 6 for x in adjacency), 'Not six-regular')
    edge_set = set(edges); automorphisms = []
    for g in range(N):
        perm = [mul(g, v) for v in range(N)]
        require(sorted(perm) == list(range(N)) and perm[0] == g, 'Not transitive permutations')
        require({tuple(sorted((perm[u],perm[v]))) for u,v in edges} == edge_set,
                'Left translation not an explicit graph automorphism')
        automorphisms.append(perm)
    stats, first = enumerate_puncture(adjacency)
    require(proper(edges, first, 0), 'Independent puncture witness invalid')
    witnesses = []
    for g, perm in enumerate(automorphisms):
        witness = [-1]*N
        for v in range(1, N):
            witness[perm[v]] = first[v]
        require(proper(edges, witness, g), 'Transported puncture witness invalid')
        witnesses.append(witness)
    four = first.copy(); four[0] = 3
    require(all(four[u] != four[v] for u,v in edges), 'Four-colouring witness invalid')
    defect = first.copy(); defect[0] = 0
    monochromatic = [[u,v] for u,v in edges if defect[u] == defect[v]]
    require(len(monochromatic) == 2, 'Exact upper defect witness invalid')
    # Meaningful rejection controls for the graph parsers and witness validator.
    rejected = []
    for label, bad in [('duplicate_edge', canonical+canonical.splitlines(keepends=True)[0]),
                       ('loop', b'0 0\n'+canonical.split(b'\n',1)[1]),
                       ('out_of_range', b'0 60\n'+canonical.split(b'\n',1)[1])]:
        try:
            parse_edges(bad)
        except (RuntimeError, ValueError):
            rejected.append(label)
        else:
            raise RuntimeError('Failed parser rejection control: '+label)
    bad = first.copy(); u,v = next((u,v) for u,v in edges if u and v); bad[v] = bad[u]
    require(not proper(edges,bad,0), 'Failed monochromatic witness rejection')
    rejected.append('monochromatic_puncture_witness')
    print(json.dumps({'graph_order':N,'graph_size':len(edges),'degree':6,
       'canonical_edge_sha256':EDGE_SHA,'inputs':inputs,
       'explicit_vertex_transitive_automorphisms_checked':len(automorphisms),
       'exhaustive_root_puncture':stats,
       'balanced_neighbour_colour_counts':[2,2,2],
       'all_vertex_puncture_witnesses':witnesses,
       'proper_four_colouring':four,'three_colour_defect_witness':defect,
       'defect_witness_monochromatic_edges':monochromatic,
       'exact_three_colour_defect':2,'chromatic_number':4,
       'all_vertex_deletions_chromatic_number':3,'all_edge_deletions_chromatic_number':4,
       'rejected_controls':rejected,
       'logical_bridge':'Any <=1-defect three-colouring becomes proper after deleting an incident vertex; an explicit automorphism sends it to G-0, where exhaustive balance forces two conflicts on reinsertion. Thus defect>=2. Proper4 and all proper puncture3 witnesses establish exact criticality.',
       'scope':'Fresh independent conventional finite proof; no Lean replay or infinite-family certification.'},indent=2))


if __name__ == '__main__':
    main()
