#!/usr/bin/env python3
"""Independent exact replay of Rizzoli--Thomas's degree-19683 example.

Generator DATA credited to alunik/common-neighbour-conjecture,
counterexamples/degree_19683.g at b2c0a8f95aa4dca76a034a0e769a8c8249f38ae2.
This verifier was written afresh. No GAP/IRREDSOL output is trusted.
Requires Python 3 and NumPy; all arithmetic is exact integral arithmetic.
"""
import hashlib
import json
from collections import Counter, deque
from pathlib import Path
import numpy as np

P = [
    (0, 2, 1, 6, 8, 7, 3, 5, 4),
    (4, 5, 3, 6, 7, 8, 1, 2, 0),
    tuple(range(9)),
]
S = [(1,) * 9, (1,) * 9, (1, 1, 1, 1, 1, 1, 2, 1, 2)]
GENS = list(zip(P, S))
IDENTITY = (tuple(range(9)), (1,) * 9)

def compose(g, h):
    """Row action: first g, then h. e_i maps to s_i e_{p_i}."""
    p, s = g
    q, t = h
    return (tuple(q[p[i]] for i in range(9)),
            tuple(s[i] * t[p[i]] % 3 for i in range(9)))

def main():
    for p, s in GENS:
        assert sorted(p) == list(range(9)) and set(s) <= {1, 2}
    H = {IDENTITY}
    todo = deque([IDENTITY])
    while todo:
        g = todo.popleft()
        for h in GENS:
            gh = compose(g, h)
            if gh not in H:
                H.add(gh)
                todo.append(gh)
    H = sorted(H)
    assert len(H) == 1152
    D = [s for p, s in H if p == tuple(range(9))]
    signatures = [tuple(s[i] for s in D) for i in range(9)]
    assert len(D) == 64 and len(set(signatures)) == 9
    assert len({p for p, s in H}) == 18
    coord_orbit = {p[0] for p, s in H}
    assert coord_orbit == set(range(9))
    # The diagonal subgroup D has nine distinct F_3-valued characters.
    # Since 3 does not divide |D|, its invariant subspaces are sums of
    # their one-dimensional coordinate eigenspaces. Transitivity on the
    # coordinate axes then proves that H is irreducible.

    n = 3 ** 9
    powers = 3 ** np.arange(9, dtype=np.int64)
    V = (np.arange(n, dtype=np.int64)[:, None] // powers) % 3
    assert np.array_equal(V @ powers, np.arange(n))
    def act(g, vv):
        p, s = g
        out = np.zeros_like(vv)
        out[:, list(p)] = (vv * np.array(s, dtype=np.int64)) % 3
        return out
    maps = [act(g, V) @ powers for g in GENS]
    seen = set()
    orbits = []
    for k in range(n):
        if k in seen:
            continue
        orbit = {k}
        todo = deque([k])
        while todo:
            v = todo.popleft()
            for f in maps:
                w = int(f[v])
                if w not in orbit:
                    orbit.add(w)
                    todo.append(w)
        assert seen.isdisjoint(orbit)
        seen.update(orbit)
        orbits.append(sorted(orbit))
    assert len(seen) == n
    regular = [o for o in orbits if len(o) == len(H)]
    assert len(regular) == 1
    R = regular[0]

    # Separate direct stabilizer count over all vectors and all H elements.
    stabilizers = np.zeros(n, dtype=np.int64)
    for g in H:
        stabilizers += np.all(act(g, V) == V, axis=1)
    assert np.flatnonzero(stabilizers == 1).tolist() == R
    for o in orbits:
        assert np.all(stabilizers[o] * len(o) == len(H))

    rv = V[R]
    in_R = np.zeros(n, dtype=bool)
    in_R[R] = True
    assert np.all(in_R[((-rv) % 3) @ powers])
    in_two = np.zeros(n, dtype=bool)
    for r in rv:
        in_two[((rv + r) % 3) @ powers] = True
    holes = np.flatnonzero(~in_two)
    assert len(holes) == 96 and np.all(in_two[R])
    zcode = int(holes[0])
    z = V[zcode]
    assert zcode != 0 and not in_R[zcode]
    # Exhaustively test all 19683 potential common neighbors w:
    # w ~ 0 iff w in R; w ~ z iff w-z in R.
    in_shifted_R = in_R[((V - z) % 3) @ powers]
    common = np.flatnonzero(in_R & in_shifted_R)
    assert len(common) == 0
    # Since |holes| < |R|, every translate v-R meets R+R, so 3R = V.
    assert len(holes) < len(R)
    # Also check 3R membership directly for every exceptional vector.
    for h in holes:
        assert np.any(in_two[((V[h] - rv) % 3) @ powers])
    result = {
        'source': 'Rizzoli--Thomas, arXiv:2609.01367v1, Section 7, Table 2, first row',
        'source_code_commit': 'b2c0a8f95aa4dca76a034a0e769a8c8249f38ae2',
        'source_code_file': 'counterexamples/degree_19683.g',
        'scope': 'credited reproduction; no novelty claim; not a Lean replay',
        'field': 3, 'dimension': 9, 'degree': n,
        'coordinate_convention': 'row vectors; e_i -> signs[i] e_images[i]; base-3 code uses coordinate 0 as least significant',
        'generators': [{'images': list(p), 'signs': list(s)} for p, s in GENS],
        'point_stabilizer_order': len(H),
        'affine_group_order': n * len(H),
        'diagonal_subgroup_order': len(D),
        'distinct_diagonal_coordinate_characters': len(set(signatures)),
        'coordinate_permutation_image_order': len({p for p, s in H}),
        'coordinate_action_transitive': True,
        'irreducibility_certificate': 'distinct diagonal characters and transitive coordinate permutation action',
        'orbit_size_histogram': dict(sorted(Counter(map(len, orbits)).items())),
        'orbits': len(orbits), 'regular_orbits': len(regular),
        'regular_vectors': len(R), 'base_size': 2,
        'stabilizer_size_histogram': {int(k): int(v) for k, v in sorted(Counter(stabilizers).items())},
        'regular_vector_codes_sha256': hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest(),
        'twoR_size': int(in_two.sum()), 'holes': len(holes),
        'hole_vectors': V[holes].tolist(),
        'witness_zero': [0] * 9,
        'witness_z': z.tolist(), 'witness_z_code': zcode,
        'witness_z_stabilizer_order': int(stabilizers[zcode]),
        'witness_pair_adjacent': False,
        'witness_pair_common_neighbors': len(common),
        'common_neighbor_candidates_exhausted': n,
        'diameter': 3,
        'all_checks_passed': True,
    }
    Path(__file__).with_name('SMALL_COUNTEREXAMPLE_REPLAY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'hole_vectors'}, indent=2))

if __name__ == '__main__':
    main()
