"""Fresh audit: spanning-tree homology computation, without author/root imports.

The covering graph and phi are rebuilt here.  We reduce to a 17-dimensional
integral fundamental-cycle basis before computing monodromy fixed spaces.
This checks finite covers only, not boundedness over all finite-index groups.
"""
from collections import deque
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import subprocess


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def power(a, k):
    result = eye(len(a))
    for _ in range(k):
        result = multiply(result, a)
    return result


def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        chosen = next((i for i in range(r, len(a)) if a[i][j]), None)
        if chosen is None:
            continue
        a[r], a[chosen] = a[chosen], a[r]
        lead = a[r][j]
        a[r] = [x/lead for x in a[r]]
        for i in range(r+1, len(a)):
            lead = a[i][j]
            a[i] = [x-lead*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def inverse_word(word):
    return [-x for x in word[::-1]]


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def substitute(word, images):
    out = []
    for x in word:
        w = images[abs(x)-1]
        out.extend(w if x > 0 else inverse_word(w))
    return reduce_word(out)


def main():
    images = [[2], [3], [1, 2]]
    inverse = [[3, -1], [1], [2]]
    for generator in range(1, 4):
        assert substitute(substitute([generator], images), inverse) == [generator]
        assert substitute(substitute([generator], inverse), images) == [generator]

    # Vertex v has binary coordinates for a,b,c. Edges are (v,letter).
    vertices = list(range(8))
    edges = [(v, letter) for v in vertices for letter in range(3)]
    edge_index = {e: i for i, e in enumerate(edges)}
    end = lambda v, letter: v ^ (1 << letter)
    boundary = [[0 for _ in edges] for _ in vertices]
    for j, (v, letter) in enumerate(edges):
        boundary[v][j] -= 1
        boundary[end(v, letter)][j] += 1

    # Build one spanning tree. Its paths define an integral basis of H_1.
    paths = {0: [0]*len(edges)}
    queue = deque([0])
    tree_edges = []
    while queue:
        v = queue.popleft()
        for letter in range(3):
            w = end(v, letter)
            if w in paths:
                continue
            j = edge_index[v, letter]
            paths[w] = paths[v].copy()
            paths[w][j] += 1
            tree_edges.append(j)
            queue.append(w)
    assert len(paths) == 8 and len(tree_edges) == 7
    nontree = [j for j in range(len(edges)) if j not in tree_edges]
    cycles = []
    for j in nontree:
        v, letter = edges[j]
        cycle = [x-y for x, y in zip(paths[v], paths[end(v, letter)])]
        cycle[j] += 1
        cycles.append(cycle)
    basis = [list(row) for row in zip(*cycles)]
    assert multiply(boundary, basis) == [[0]*17 for _ in vertices]
    assert [basis[j] for j in nontree] == eye(17)
    assert rank(boundary) == 7 and rank(basis) == 17

    # The phi lift sends vertices by M mod 2, and is based at 0.
    def vertex_image(v):
        out = 0
        for bit, word in enumerate(images):
            if v & (1 << bit):
                for generator in word:
                    out ^= 1 << (generator-1)
        return out

    chain = [[0 for _ in edges] for _ in edges]
    for j, (v, letter) in enumerate(edges):
        cursor = vertex_image(v)
        for generator in images[letter]:
            k = generator-1
            chain[edge_index[cursor, k]][j] += 1
            cursor = end(cursor, k)
        assert cursor == vertex_image(end(v, letter))
    vertex_map = [[int(i == vertex_image(j)) for j in vertices] for i in vertices]
    assert multiply(boundary, chain) == multiply(vertex_map, boundary)

    fixed_spaces = []
    for n in (1, 2, 7, 14):
        chain_n = power(chain, n)
        image_cycles = multiply(chain_n, basis)
        homology_map = [image_cycles[j] for j in nontree]
        assert multiply(basis, homology_map) == image_cycles
        difference = [[homology_map[i][j]-int(i == j) for j in range(17)]
                      for i in range(17)]
        chain_difference = [[chain_n[i][j]-int(i == j) for j in range(24)]
                            for i in range(24)]
        h_rank = rank(difference)
        stacked_rank = rank(boundary+chain_difference)
        assert 17-h_rank == 24-stacked_rank
        expected = {1: 0, 2: 1, 7: 0, 14: 7}[n]
        assert 17-h_rank == expected
        fixed_spaces.append({'monodromy_power': n, 'subgroup_index': 8*n,
                             'rank_on_H1_minus_I': h_rank,
                             'stacked_chain_rank': stacked_rank,
                             'b2': 17-h_rank,
                             'H1_monodromy_integer_matrix': homology_map})

    base = Path(__file__).resolve().parents[1]
    root_script = base/'root_artifacts/verify_mod2_cover.py'
    root_result = json.loads(subprocess.run(['python3', str(root_script)],
                                          text=True, capture_output=True,
                                          check=True).stdout)
    assert root_result['second_betti'] == 7
    assert root_result['rank_lower_certificate']['determinant'] == -4096

    output = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'method': 'Independent spanning-tree integral H1 basis; exact Fraction ranks',
              'scope': 'Selected finite covers only; no all-cover upper bound or novelty claim',
              'automorphism_and_inverse_checked': True,
              'cover_vertices': 8, 'cover_edges': 24,
              'H1_rank': 17, 'tree_edge_indices': tree_edges,
              'nontree_edge_indices': nontree,
              'fundamental_cycle_basis_24_by_17': basis,
              'covers': fixed_spaces,
              'root_certificate_rerun_passed': True,
              'root_script_sha256': sha256(root_script.read_bytes()).hexdigest()}
    path = Path(__file__).with_name('partial_adversary01_checks.json')
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k: output[k] for k in ('checked_at_utc', 'method', 'scope')}))
    print(json.dumps([{k:v for k,v in row.items() if k != 'H1_monodromy_integer_matrix'}
                      for row in fixed_spaces], indent=2))


if __name__ == '__main__':
    main()
