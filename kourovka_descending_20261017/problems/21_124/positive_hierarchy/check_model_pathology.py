#!/usr/bin/env python3
"""Exact w=ab direct-self-osculation witnesses; model-specific, not group obstruction."""
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from check_one_twist import original_complex, cover


def analyze(complex_):
    parallel = defaultdict(list)
    corners = defaultdict(set)
    for square in complex_.squares:
        for a, b in ((square[0], square[2]), (square[1], square[3])):
            multiplier = -(1 if a > 0 else -1) * (1 if b > 0 else -1)
            parallel[abs(a)].append((abs(b), multiplier))
            parallel[abs(b)].append((abs(a), multiplier))
        for previous, current in zip(square[-1:] + square[:-1], square):
            v = complex_.ends(current)[0]
            corners[v].add(tuple(sorted((-previous, current))))
    root, orientation = {}, {}
    for initial in range(1, len(complex_.edges) + 1):
        if initial in root:
            continue
        root[initial], orientation[initial] = initial, 1
        pending = [initial]
        while pending:
            edge = pending.pop()
            for neighbour, multiplier in parallel[edge]:
                value = orientation[edge] * multiplier
                if neighbour not in root:
                    root[neighbour], orientation[neighbour] = initial, value
                    pending.append(neighbour)
                else:
                    assert root[neighbour] == initial
                    assert orientation[neighbour] == value
    c_components = defaultdict(list)
    for eid, edge in enumerate(complex_.edges, 1):
        if edge[3] == 'c':
            c_components[root[eid]].append(eid)
    witnesses = []
    for component, edges in c_components.items():
        assert len(edges) == 2
        a, b = edges
        assert a != b and orientation[a] == orientation[b]
        head_a, head_b = complex_.edges[a-1][1], complex_.edges[b-1][1]
        assert head_a == head_b
        assert tuple(sorted((-a, -b))) not in corners[head_a]
        assert all(complex_.edges[eid-1][3] == 'c' for eid, r in root.items() if r == component)
        witnesses.append({'hyperplane_root': component, 'edges': [a, b],
                          'common_terminal_vertex': repr(head_a),
                          'coorientation': orientation[a], 'missing_square_corner': [-a, -b]})
    return witnesses


def main():
    _, original = original_complex((1, 2), rank=2, k=1, chi=(1, 0))
    original.check_npc()
    voltages = {eid: int(edge[3] == 'c') for eid, edge in enumerate(original.edges, 1)}
    cases = []
    for degree in range(1, 33):
        lifted, _ = cover(original, degree, voltages)
        lifted.check_npc()
        witnesses = analyze(lifted)
        assert len(witnesses) == degree
        cases.append({'degree': degree, 'witness_count': len(witnesses),
                      'first_witness': witnesses[0]})
    here = Path(__file__).resolve().parent
    payload = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
               'word': [1, 2], 'case_count': len(cases),
               'scope': 'Specific displayed models and c-only covers; no group nonembedding claim',
               'cases': cases,
               'proof_sha256': hashlib.sha256((here/'MODEL_PATHOLOGY_CONTROL.md').read_bytes()).hexdigest(),
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'constructor_sha256': hashlib.sha256((here/'check_one_twist.py').read_bytes()).hexdigest()}
    (here/'model_pathology_certificate.json').write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
