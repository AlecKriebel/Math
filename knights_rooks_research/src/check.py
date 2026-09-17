#!/usr/bin/env python3
"""Direct finite-coordinate verifier. Python standard library only.

Knights: pairwise coordinate differences. Rooks: nearest occupied point
in each open orthogonal ray. No search-library imports or board assumptions.
"""
import argparse
import json
from pathlib import Path


def coordinates(values, label):
    if not isinstance(values, list) or not values:
        raise ValueError(f'{label} must be a nonempty list')
    for p in values:
        if not isinstance(p, (list, tuple)) or len(p) != 2 or any(type(z) is not int for z in p):
            raise ValueError(f'{label}: expected integer-coordinate pairs')
    out = [tuple(p) for p in values]
    if len(set(out)) != len(out):
        raise ValueError(f'{label}: repeated coordinate')
    return set(out)


def inspect(data, n=4, m=2):
    K, R = coordinates(data['knights'], 'knights'), coordinates(data['rooks'], 'rooks')
    if K & R:
        raise ValueError('Knights and rooks overlap')
    occupied = K | R
    attacks, errors = [], []
    for p in sorted(K):
        seen = sorted(q for q in occupied if sorted((abs(q[0]-p[0]), abs(q[1]-p[1]))) == [1, 2])
        kr, kk = [q for q in seen if q in R], [q for q in seen if q in K]
        attacks.append({'piece': 'K', 'at': p, 'attacks_rooks': kr, 'attacks_knights': kk})
        if len(kr) != n or kk:
            errors.append(f'Knight {p}: {len(kr)} rook targets, {len(kk)} knight targets')
    for p in sorted(R):
        rays = {}
        for name, dx, dy in [('E', 1, 0), ('W', -1, 0), ('N', 0, 1), ('S', 0, -1)]:
            candidates = []
            for q in occupied:
                vx, vy = q[0]-p[0], q[1]-p[1]
                distance = vx*dx + vy*dy
                if distance > 0 and vx*dy-vy*dx == 0:
                    candidates.append((distance, q))
            rays[name] = min(candidates)[1] if candidates else None
        seen = [q for q in rays.values() if q is not None]
        rk, rr = sorted(q for q in seen if q in K), sorted(q for q in seen if q in R)
        attacks.append({'piece': 'R', 'at': p, 'rays': rays, 'attacks_knights': rk, 'attacks_rooks': rr})
        if len(rk) != m or rr:
            errors.append(f'Rook {p}: {len(rk)} knight targets, {len(rr)} rook targets')
    return {'valid': not errors, 'knight_outdegree_required': n, 'rook_outdegree_required': m,
            'knight_count': len(K), 'rook_count': len(R),
            'bounding_box': [min(x for x,y in occupied), min(y for x,y in occupied),
                             max(x for x,y in occupied), max(y for x,y in occupied)],
            'errors': errors, 'attacks': attacks}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('coordinates', type=Path)
    p.add_argument('--knight-degree', type=int, default=4)
    p.add_argument('--rook-degree', type=int, default=2)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    try:
        result = inspect(json.loads(a.coordinates.read_text()), a.knight_degree, a.rook_degree)
    except (ValueError, KeyError, OSError) as e:
        p.exit(2, f'Invalid input: {e}\n')
    text = json.dumps(result, indent=2)
    if a.output:
        a.output.write_text(text+'\n')
    print(text)
    raise SystemExit(0 if result['valid'] else 1)

if __name__ == '__main__':
    main()
