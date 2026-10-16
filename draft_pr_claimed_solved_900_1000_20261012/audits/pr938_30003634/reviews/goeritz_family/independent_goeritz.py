#!/usr/bin/env python3
"""Independent three-braid checkerboard audit, using only Python stdlib.

Construct an oriented planar rotation system first. Build faces and colors
from its edge pairing, not from the candidate's claimed cyclic matrix.
No author executable, certificate or historical audit is imported.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import datetime
import argparse
import sys


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def inverse(w):
    return [-x for x in reversed(w)]


def comm(x, y):
    return x + y + inverse(x) + inverse(y)


def reduce_free(w):
    s = []
    for x in w:
        if s and s[-1] == -x:
            s.pop()
        else:
            s.append(x)
    return s


def witness():
    a, b = [1, 1], [2, 2]
    c = comm(a, b)
    d = inverse(a) + c + a
    e = inverse(b) + c + b
    u, v = comm(c, d), comm(d, e)
    return reduce_free(comm(u, v))


def syllables(w):
    out = []
    for x in w:
        if out and abs(out[-1][0]) == abs(x):
            out[-1][1] += 1 if x > 0 else -1
        else:
            out.append([abs(x), 1 if x > 0 else -1])
    require(all(v for _, v in out), 'Check failed: all(v for _, v in out)')
    return out


def pairs(w):
    # The actual reduced word already starts in sigma1 and ends in sigma2;
    # no conjugation or silent cyclic change is used.
    s = syllables(w)
    require(s[0][0] == 1 and s[-1][0] == 2, 'Check failed: s[0][0] == 1 and s[-1][0] == 2')
    require(all(t[0] == 1 + i % 2 for i, t in enumerate(s)), 'Check failed: all(t[0] == 1 + i % 2 for i, t in enumerate(s))')
    return [(s[i][1], s[i + 1][1]) for i in range(0, len(s), 2)]


def oriented_closure(w):
    positions = [0, 1, 2]
    sums = {(0, 1): 0, (0, 2): 0, (1, 2): 0}
    for x in w:
        k = abs(x) - 1
        i, j = sorted(positions[k:k + 2])
        sums[i, j] += 1 if x > 0 else -1
        positions[k], positions[k + 1] = positions[k + 1], positions[k]
    return {'permutation': positions,
            'signed_pair_crossings': {str(k): v for k, v in sums.items()},
            'pairwise_linking': {str(k): str(F(v, 2)) for k, v in sums.items()}}


def diagram(w):
    """Port cyclic order is NW,NE,SE,SW (clockwise).

    Connect consecutive crossings at each horizontal position. Join bottom
    position k to top position k by its own exterior closure edge. This is
    the standard nested closure; its planar Euler characteristic is checked.
    At each crossing, strands connect NW-SE and NE-SW, regardless of sign.
    Face successor rotates clockwise after crossing an edge. Thus
    the face on the left of NW is the west sector, etc.
    """
    n = len(w)
    require(n > 0 and set(map(abs, w)) == {1, 2}, 'Check failed: n > 0 and set(map(abs, w)) == {1, 2}')
    edge = {}
    first = [None] * 3
    last = [None] * 3

    def join(a, b):
        require(a not in edge and b not in edge, 'Check failed: a not in edge and b not in edge')
        edge[a], edge[b] = b, a

    for v, x in enumerate(w):
        k = abs(x) - 1
        for pos, port_in, port_out in [(k, 0, 3), (k + 1, 1, 2)]:
            pin, pout = 4 * v + port_in, 4 * v + port_out
            if last[pos] is None:
                first[pos] = pin
            else:
                join(last[pos], pin)
            last[pos] = pout
    for pos in range(3):
        require(first[pos] is not None, 'Check failed: first[pos] is not None')
        join(last[pos], first[pos])
    require(len(edge) == 4 * n, 'Check failed: len(edge) == 4 * n')
    face_of, faces = {}, []
    for h in range(4 * n):
        if h in face_of:
            continue
        seq, a = [], h
        while a not in face_of:
            face_of[a] = len(faces)
            seq.append(a)
            b = edge[a]
            a = 4 * (b // 4) + (b % 4 + 1) % 4
        require(a == h, 'Check failed: a == h')
        faces.append(seq)
    require(n - 2 * n + len(faces) == 2, 'nonplanar or disconnected diagram')
    # West sector of any sigma1 crossing is unbounded.
    v1 = next(v for v, x in enumerate(w) if abs(x) == 1)
    outer = face_of[4 * v1]
    color = {outer: 0}
    q = deque([outer])
    adjacency = [set() for _ in faces]
    for a, b in edge.items():
        adjacency[face_of[a]].add(face_of[b])
    while q:
        a = q.popleft()
        for b in adjacency[a]:
            if b in color:
                require(color[b] != color[a], 'Check failed: color[b] != color[a]')
            else:
                color[b] = 1 - color[a]
                q.append(b)
    require(len(color) == len(faces), 'Check failed: len(color) == len(faces)')
    black = sorted(f for f, c in color.items() if c == 0 and f != outer)
    ix = {f: i for i, f in enumerate(black)}
    G = [[0 for _ in black] for _ in black]
    rows, mu = [], 0
    for v, x in enumerate(w):
        # Local sectors W,N,E,S are left of NW,NE,SE,SW.
        sectors = [face_of[4 * v + p] for p in range(4)]
        if abs(x) == 1:
            require(all(color[sectors[p]] == p % 2 for p in range(4)), 'Check failed: all(color[sectors[p]] == p % 2 for p in range(4))')
            a, b = sectors[0], sectors[2]
            require(outer in (a, b), 'Check failed: outer in (a, b)')
            theta, exceptional = (1 if x > 0 else -1), True
        else:
            require(all(color[sectors[p]] == 1 - p % 2 for p in range(4)), 'Check failed: all(color[sectors[p]] == 1 - p % 2 for p in range(4))')
            a, b = sectors[1], sectors[3]
            theta, exceptional = (-1 if x > 0 else 1), False
        # Erle puts theta=0 if the same alpha-region meets itself.
        if a == b:
            theta = 0
        if exceptional:
            mu += theta
        if a != b:
            for f in (a, b):
                if f != outer:
                    G[ix[f]][ix[f]] += theta
            if a != outer and b != outer:
                G[ix[a]][ix[b]] -= theta
                G[ix[b]][ix[a]] -= theta
        rows.append({'crossing': v, 'artin': x, 'sectors_WNES': sectors,
                     'black_faces': [a, b], 'theta': theta,
                     'exceptional': exceptional})
    return {'matrix': G, 'mu': mu, 'faces': faces, 'black_bounded': black,
            'outer': outer, 'crossings': rows, 'face_of': face_of}


def cycle_matrix(ab):
    N = sum(abs(b) for a, b in ab)
    G, t = [[0] * N for _ in range(N)], 0
    anchors = []
    for a, b in ab:
        anchors.append(t)
        G[t][t] += a
        for k in range(abs(b)):
            i, h = t + k, (t + k + 1) % N
            s = 1 if b > 0 else -1
            # Add -s (e_i-e_h)(e_i-e_h)^T, allowing coincident indices.
            for r, cr in [(i, 1), (h, -1)]:
                for c, cc in [(i, 1), (h, -1)]:
                    G[r][c] -= s * cr * cc
        t += abs(b)
    return G, anchors


def inertia(G):
    """Exact congruence, with 2x2 pivots when the diagonal is identically 0."""
    A = [[F(a) for a in row] for row in G]
    pos, neg, zero, det = 0, 0, 0, F(1)
    pivots = []
    while A:
        m = len(A)
        k = next((i for i in range(m) if A[i][i]), None)
        if k is not None:
            A[0], A[k] = A[k], A[0]
            for row in A:
                row[0], row[k] = row[k], row[0]
            p = A[0][0]
            pivots.append({'size': 1, 'swap_index': k, 'value': str(p)})
            pos += p > 0
            neg += p < 0
            det *= p
            A = [[A[i][j] - A[i][0] * A[0][j] / p
                  for j in range(1, m)] for i in range(1, m)]
            continue
        pair = next(((i, j) for i in range(m) for j in range(i + 1, m)
                     if A[i][j]), None)
        if pair is None:
            zero += m
            det = F(0)
            pivots.append({'size': m, 'zero_block': True})
            break
        i, j = pair
        order = [i, j] + [k for k in range(m) if k not in (i, j)]
        A = [[A[i][j] for j in order] for i in order]
        b = A[0][1]
        pivots.append({'size': 2, 'off_diagonal': str(b), 'order': order})
        pos += 1
        neg += 1
        det *= -b * b
        A = [[A[i][j] - (A[i][0] * A[1][j] + A[i][1] * A[0][j]) / b
              for j in range(2, m)] for i in range(2, m)]
    require(pos + neg + zero == len(G), 'Check failed: pos + neg + zero == len(G)')
    return {'inertia': [pos, neg, zero], 'determinant': str(det),
            'signature': pos - neg, 'pivots': pivots}


def bareiss(G):
    A = [r[:] for r in G]
    n, prev, sign = len(A), 1, 1
    if n == 0:
        return 1
    for k in range(n - 1):
        if A[k][k] == 0:
            i = next((i for i in range(k + 1, n) if A[i][k]), None)
            if i is None:
                return 0
            A[k], A[i] = A[i], A[k]
            sign *= -1
        p = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = A[i][j] * p - A[i][k] * A[k][j]
                require(numerator % prev == 0, 'Check failed: numerator % prev == 0')
                A[i][j] = numerator // prev
        prev = p
        for i in range(k + 1, n):
            A[i][k] = 0
    return sign * A[-1][-1]


def calculate(w):
    d = diagram(w)
    v = inertia(d['matrix'])
    return {**v, 'mu': d['mu'], 'link_signature': v['signature'] - d['mu'],
            'matrix': d['matrix']}


def literal_printed_off_diagonal(ab):
    """Deliberately follow the source's prior-block off-diagonal index."""
    g, _ = cycle_matrix(ab)
    n, t = len(g), 0
    require(n >= 3, 'Check failed: n >= 3')
    switching = [1]
    for j, (a, b) in enumerate(ab):
        curr = 1 if b > 0 else -1
        prev = 1 if ab[j - 1][1] > 0 else -1
        for k in range(abs(b)):
            i, h = t + k, (t + k + 1) % n
            g[i][h] += prev - curr
            g[h][i] += prev - curr
            switching.append(switching[-1] * prev * curr)
        t += abs(b)
    return g, switching


def main(expected_signature=-2, output=None):
    w = witness()
    ab = pairs(w)
    d = diagram(w)
    # Reading alpha_N at each sigma2 crossing is a geometric cyclic ordering.
    order_faces = [r['sectors_WNES'][1] for r in d['crossings']
                   if abs(r['artin']) == 2]
    require(len(order_faces) == len(set(order_faces)) == len(d['black_bounded']), "Check failed: len(order_faces) == len(set(order_faces)) == len(d['black_bounded'])")
    ix = {f: i for i, f in enumerate(d['black_bounded'])}
    order = [ix[f] for f in order_faces]
    G = [[d['matrix'][i][j] for j in order] for i in order]
    predicted, anchors = cycle_matrix(ab)
    require(G == predicted, 'Check failed: G == predicted')
    # Every sigma2 lower alpha equals the next upper alpha, including the
    # exterior-closing-arcs seam. Every sigma1 meets outer + expected anchor.
    b_rows = [r for r in d['crossings'] if abs(r['artin']) == 2]
    for i, row in enumerate(b_rows):
        require(row['sectors_WNES'][3] == order_faces[(i + 1) % len(order_faces)], "Check failed: row['sectors_WNES'][3] == order_faces[(i + 1) % len(order_faces)]")
    # Avoid indexing repeated pairs: validate anchors by running block index.
    cursor = 0
    for j, (a, b) in enumerate(ab):
        for row in d['crossings'][cursor:cursor + abs(a)]:
            require(set(row['black_faces']) == {d['outer'], order_faces[anchors[j]]}, "Check failed: set(row['black_faces']) == {d['outer'], order_faces[anchors[j]]}")
        cursor += abs(a) + abs(b)
    exact = inertia(G)
    require(int(exact['determinant']) == bareiss(G), "Check failed: int(exact['determinant']) == bareiss(G)")
    mirror = calculate([-x for x in w])
    require(mirror['link_signature'] == -(exact['signature'] - d['mu']), "Check failed: mirror['link_signature'] == -(exact['signature'] - d['mu'])")
    require(mirror['matrix'] == [[-x for x in row] for row in d['matrix']], "Check failed: mirror['matrix'] == [[-x for x in row] for row in d['matrix']]")
    controls = [
        ('unknot positive stabilization', [1, 2], 0),
        ('unknot mixed stabilization', [1, -2], 0),
        ('positive Hopf stabilized', [1, 1, 2], -1),
        ('negative Hopf mirror', [-1, -1, -2], 1),
        ('positive trefoil stabilized', [1, 1, 1, 2], -2),
        ('negative trefoil mirror', [-1, -1, -1, -2], 2),
        ('three component unlink RII', [1, -1, 2, -2], 0),
        ('two component unlink RII', [1, 2, -2], 0),
        ('Borromean standard braid', [1, -2] * 3, 0),
        ('Borromean mirror', [-1, 2] * 3, 0),
        ('positive T(3,3)', [1, 2] * 3, -4),
        ('negative T(3,3)', [-1, -2] * 3, 4),
        ('q=1 two vertices parallel edges', [1, 1, 2, 2], -2),
        ('q=1 three vertices', [1, 1, 2, 2, 2], -3),
    ]
    control_results = []
    for name, word, expected in controls:
        row = calculate(word)
        require(row['link_signature'] == expected, (name, row))
        control_results.append({'name': name, 'word': word,
                                'expected_signature': expected, **row})
    # Additional sampled checks vary signs, block lengths, q and degeneracy.
    # These do not substitute for the symbolic diagram derivation.
    import itertools
    samples = []
    for vals in itertools.product([-2, -1, 1, 2], repeat=4):
        p = [(vals[0], vals[1]), (vals[2], vals[3])]
        ww = [g * (1 if power > 0 else -1)
              for a, b in p for g, power in [(1, a), (2, b)]
              for _ in range(abs(power))]
        dg = diagram(ww)
        of = [r['sectors_WNES'][1] for r in dg['crossings'] if abs(r['artin']) == 2]
        old = {f: i for i, f in enumerate(dg['black_bounded'])}
        pg = [[dg['matrix'][old[i]][old[j]] for j in of] for i in of]
        require(pg == cycle_matrix(p)[0], 'Check failed: pg == cycle_matrix(p)[0]')
        rr = inertia(pg)
        require(int(rr['determinant']) == bareiss(pg), "Check failed: int(rr['determinant']) == bareiss(pg)")
        require(dg['mu'] == vals[0] + vals[2], "Check failed: dg['mu'] == vals[0] + vals[2]")
        samples.append({'powers': vals, 'inertia': rr['inertia'], 'mu': dg['mu']})
    literal, switches = literal_printed_off_diagonal(ab)
    require(switches[-1] == switches[0], 'Check failed: switches[-1] == switches[0]')
    require(literal == [[switches[i] * G[i][j] * switches[j]
                        for j in range(len(G))] for i in range(len(G))], 'Check failed: literal == [[switches[i] * G[i][j] * switches[j]                         for j in range(len(G))] for i in range(len(G))]')
    typo_control_pairs = [(1, 2), (1, -1)]
    repaired, _ = cycle_matrix(typo_control_pairs)
    wrong, _ = literal_printed_off_diagonal(typo_control_pairs)
    require(inertia(repaired)['inertia'] == [2, 1, 0], "Check failed: inertia(repaired)['inertia'] == [2, 1, 0]")
    require(inertia(wrong)['inertia'] == [1, 1, 1], "Check failed: inertia(wrong)['inertia'] == [1, 1, 1]")
    require(len(w) == 104 and len(ab) == 23, 'Wrong witness length or pair count')
    require(sum(a for a, b in ab) == sum(b for a, b in ab) == 0,
            'Nonzero witness exponent sum')
    closure = oriented_closure(w)
    require(closure['permutation'] == [0, 1, 2], 'Witness is not pure')
    require(set(closure['pairwise_linking'].values()) == {'0'},
            'Witness linking numbers are not all zero')
    require(exact['inertia'] == [23, 25, 0], 'Wrong witness inertia')
    require(exact['determinant'] == '-7154819319988224', 'Wrong witness determinant')
    require(d['mu'] == 0, 'Wrong exceptional-crossing correction')
    require(exact['signature'] - d['mu'] == expected_signature,
            f'Wrong numerical expectation: signature {expected_signature}, '
            f'computed {exact["signature"] - d["mu"]}')
    out = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python_optimization': sys.flags.optimize,
        'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'reduced_word': w, 'word_length': len(w), 'cyclic_conjugation': False,
        'pairs': ab, 'A': [a for a, b in ab], 'B': [b for a, b in ab],
        'sum_A': sum(a for a, b in ab), 'sum_B': sum(b for a, b in ab),
        'closure': closure, 'bounded_black_faces': len(order_faces),
        'all_faces': len(d['faces']), 'outer_face': d['outer'],
        'region_order': order_faces, 'region_permutation': order,
        'anchors': anchors, 'crossings': d['crossings'],
        'matrix': G, 'matrix_in_face_order': d['matrix'],
        'mu': d['mu'], **exact,
        'link_signature': exact['signature'] - d['mu'],
        'bareiss_determinant': bareiss(G),
        'mirror_inertia': mirror['inertia'], 'mirror_signature': mirror['link_signature'],
        'source_typo_control': {
            'pairs': typo_control_pairs, 'geometric_matrix': repaired,
            'geometric_inertia': inertia(repaired)['inertia'],
            'literal_printed_matrix': wrong,
            'literal_printed_inertia': inertia(wrong)['inertia'],
            'witness_literal_inertia': inertia(literal)['inertia'],
            'witness_diagonal_switching': switches[:-1],
            'witness_switching_closes': True,
            'warning': 'Even B-block lengths make the wrong off-diagonal index '
                       'sign-congruent for this witness; its inertia cannot '
                       'by itself validate the source correction.'},
        'controls': control_results, 'sampled_two_pair_checks': samples,
        'artificial_exact_congruence_edge_cases': [
            {'matrix': z, **inertia(z)} for z in [[], [[0]], [[0, 2], [2, 0]],
                                                [[0, 0], [0, 0]], [[0, 0], [0, 3]]]],
    }
    serialized = json.dumps(out, indent=2) + '\n'
    if output:
        Path(output).write_text(serialized)
        print(json.dumps({k: out[k] for k in ['word_length', 'inertia',
                        'bareiss_determinant', 'mu', 'link_signature', 'mirror_signature']}))
    else:
        print(serialized, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Explicit output file; default emits JSON to stdout only')
    parser.add_argument('--expect-signature', type=int, default=-2,
                        help='Expected numerical signature; wrong values fail closed')
    args = parser.parse_args()
    main(args.expect_signature, args.output)
