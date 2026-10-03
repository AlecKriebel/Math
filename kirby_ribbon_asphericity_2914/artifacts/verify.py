#!/usr/bin/env python3
"""Small exact checks for the partial results, not an asphericity decision procedure."""
import itertools
import json


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(p, q):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, 0) + c
    return clean(r)


def mul(p, q):
    r = {}
    for e, c in p.items():
        for f, d in q.items():
            r[e + f] = r.get(e + f, 0) + c * d
    return clean(r)


def det(a):
    n = len(a)
    out = {}
    for perm in itertools.permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        v = {0: (-1) ** inv}
        for i, j in enumerate(perm):
            v = mul(v, a[i][j])
        out = add(out, v)
    return out


def relator(edge):
    s, t, label = edge
    return [(s, 1), (label, 1), (t, -1), (label, -1)]


def abelian_fox(word, n):
    row = [{} for _ in range(n)]
    height = 0
    for g, sign in word:
        if sign == 1:
            row[g] = add(row[g], {height: 1})
            height += 1
        else:
            height -= 1
            row[g] = add(row[g], {height: -1})
    assert height == 0
    return row


def predicted(edge, n):
    s, t, label = edge
    row = [{} for _ in range(n)]
    row[s] = add(row[s], {0: 1})
    row[t] = add(row[t], {1: -1})
    row[label] = add(row[label], {1: 1, 0: -1})
    return row


def forest(edges, n):
    parent = list(range(n))

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for a, b in edges:
        a, b = root(a), root(b)
        if a == b:
            return False
        parent[a] = b
    return True


def actual_links(words):
    positive, negative = [], []
    for word in words:
        for (g, sg), (h, sh) in zip(word, word[1:] + word[:1]):
            # End direction of the first letter and start direction of the next.
            x, y = (g, -sg), (h, sh)
            if x[1] == y[1] == 1:
                positive.append((g, h))
            elif x[1] == y[1] == -1:
                negative.append((g, h))
    return positive, negative


def reduced_word(word):
    stack = []
    for a in word:
        if stack and stack[-1] == -a:
            stack.pop()
        else:
            stack.append(a)
    return tuple(stack)


def ring_add(a, b):
    out = dict(a)
    for word, c in b.items():
        out[word] = out.get(word, 0) + c
    return {w: c for w, c in out.items() if c}


def ring_mul(a, b):
    out = {}
    for x, c in a.items():
        for y, d in b.items():
            word = reduced_word(x + y)
            out[word] = out.get(word, 0) + c * d
    return {w: c for w, c in out.items() if c}


def main():
    n = 5
    edges = [(0, 1, 2), (1, 2, 4), (2, 3, 0), (3, 4, 2)]
    fox_cases = 0
    for s, t, label in itertools.product(range(n), repeat=3):
        if s == t:
            continue
        edge = (s, t, label)
        assert abelian_fox(relator(edge), n) == predicted(edge, n)
        fox_cases += 1
    matrix = [abelian_fox(relator(edge), n) for edge in edges]
    determinants = []
    for root in range(n):
        minor = [[v for j, v in enumerate(row) if j != root] for row in matrix]
        value = det(minor)
        expected = {1: (-1) ** root, 2: -(-1) ** root, 3: (-1) ** root}
        assert value == expected
        assert sum(value.values()) == (-1) ** root
        determinants.append(value)
    assert det([]) == {0: 1}
    # Compressed, boundary reduced, interior reduced.
    assert all(label not in (s, t) for s, t, label in edges)
    labels = [e[2] for e in edges]
    assert 0 in labels and 4 in labels
    assert all(edges[i][2] != edges[i + 1][2] for i in range(3))
    assert len(set(labels)) < len(labels)
    proper_intervals = 0
    for left in range(n):
        for right in range(left + 1, n):
            if (left, right) == (0, n - 1):
                continue
            subedges = edges[left:right]
            assert any(label < left or label > right for _, _, label in subedges)
            proper_intervals += 1
    assert proper_intervals == 9
    # Direct link computation from signed relators, including inversions of
    # generators that occur only as endpoints.
    inversion_passes = []
    for mask in range(1 << n):
        words = [[(g, -sign if mask & (1 << g) else sign) for g, sign in relator(e)]
                 for e in edges]
        pos, neg = actual_links(words)
        if forest(pos, n) and forest(neg, n):
            inversion_passes.append(mask)
    assert inversion_passes == []
    # Check the hand table using all eight effective label choices.
    witnesses = [('+', [(0, 2), (0, 2)]),
                 ('+', [(1, 2), (2, 4), (1, 4)]),
                 ('+', [(0, 2), (0, 2)]),
                 ('+', [(2, 4), (2, 4)]),
                 ('-', [(2, 4), (2, 4)]),
                 ('-', [(0, 2), (0, 2)]),
                 ('+', [(0, 2), (2, 3), (0, 3)]),
                 ('+', [(2, 4), (2, 4)])]
    for (a, e, c), (kind, witness) in zip(itertools.product((0, 1), repeat=3), witnesses):
        bits = (c, e, a, c)
        oriented = [(t, s, label) if bit else (s, t, label)
                    for bit, (s, t, label) in zip(bits, edges)]
        pos, neg = actual_links([relator(edge) for edge in oriented])
        remaining = [tuple(sorted(x)) for x in (pos if kind == '+' else neg)]
        for pair in witness:
            remaining.remove(tuple(sorted(pair)))
    orientation_passes = []
    for bits in itertools.product((0, 1), repeat=4):
        oriented = [(t, s, label) if bit else (s, t, label)
                    for bit, (s, t, label) in zip(bits, edges)]
        pos, neg = actual_links([relator(edge) for edge in oriented])
        if forest(pos, n) and forest(neg, n):
            orientation_passes.append(bits)
    assert orientation_passes == [(0, 0, 1, 1), (1, 1, 0, 0)]
    assert all(bits[0] != bits[3] for bits in orientation_passes)
    # Free-group ring identity used in the augmentation-ideal lemma.
    lhs = {(1, 2, -1, -2): 1, (): -1}
    uv_minus_vu = {(1, 2): 1, (2, 1): -1}
    assert ring_mul(uv_minus_vu, {(-1, -2): 1}) == lhs
    u_minus_one = {(1,): 1, (): -1}
    v_minus_one = {(2,): 1, (): -1}
    v_u_negative = {w: -c for w, c in ring_mul(v_minus_one, u_minus_one).items()}
    assert ring_add(ring_mul(u_minus_one, v_minus_one), v_u_negative) == uv_minus_vu
    print(json.dumps({
        'problem': '2914 / KP-4.38',
        'result': 'PASS',
        'scope': 'Finite exact algebra and graph checks only; not a solution of asphericity.',
        'fox_triples_checked': fox_cases,
        'root_minor_determinants_by_exponent': determinants,
        'proper_intervals_checked': proper_intervals,
        'generator_inversion_subsets_checked': 32,
        'generator_inversion_forest_passes': inversion_passes,
        'independent_edge_orientations_checked': 16,
        'independent_edge_orientation_forest_passes': orientation_passes,
        'hand_table_cycle_witnesses_checked': 8,
        'free_group_ring_identities_checked': 2,
        'general_proof_status': 'unresolved'
    }, indent=2))


if __name__ == '__main__':
    main()
