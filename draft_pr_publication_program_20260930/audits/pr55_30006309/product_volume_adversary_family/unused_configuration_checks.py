"""Explicit full lattice configurations with strictly unused product columns."""
from pathlib import Path
import hashlib
import json
import random
from independent_product_checks import lower_hull, closure, lattice_volume

HERE = Path(__file__).resolve().parent

def main():
    rng = random.Random(3000630955)
    records = []
    for kind in ('square', 'triangle'):
        for scale in (2, 3):
            # Triangle scale 3 has ten lattice points; square scale 3 sixteen.
            # Only scale 2 square is enumerated to keep exact controls compact.
            if kind == 'square' and scale == 3:
                continue
            corners = [(0, 0), (scale, 0), (scale, scale), (0, scale)] if kind == 'square' else [(0, 0), (scale, 0), (0, scale)]
            A = [(x, y) for x in range(scale + 1) for y in range(scale + 1)
                 if kind == 'square' or x + y <= scale]
            points = [a + (b,) for a in A for b in (0, 1)]
            for sign in (-1, 1):
                w = [0, sign, 0, sign] if kind == 'square' else [0, 0, 0]
                h = []
                for a in A:
                    for _ in (0, 1):
                        h.append(1000000 * w[corners.index(a)] + rng.randrange(-1000, 1001)
                                 if a in corners else 1000000000 + rng.randrange(-1000, 1001))
                facets = lower_hull(points, h)
                assert facets is not None
                used = {i // 2 for tau in facets for i in tau}
                assert used == {A.index(a) for a in corners}
                desired_volume = 6 * scale * scale if kind == 'square' else 3 * scale * scale
                assert sum(lattice_volume([points[i] for i in tau]) for tau in facets) == desired_volume
                projected = [0] * len(A)
                for face in closure(facets):
                    ps = [points[i] for i in face]
                    k = len(face) - 1
                    if kind == 'square':
                        fixed = sum(len({p[c] for p in ps}) == 1 and ps[0][c] in (0, scale) for c in (0, 1))
                    else:
                        fixed = int(all(p[0] == 0 for p in ps)) + int(all(p[1] == 0 for p in ps)) + int(all(p[0] + p[1] == scale for p in ps))
                    fixed += int(len({p[2] for p in ps}) == 1)
                    if k != 3 - fixed:
                        continue
                    v = lattice_volume(ps)
                    for i in face:
                        projected[i // 2] += (-1) ** (3 - k) * v
                assert all(projected[i] == 0 for i, a in enumerate(A) if a not in corners)
                expected = [0] * len(A)
                cells = [(0, 1, 2), (0, 2, 3)] if kind == 'square' and sign > 0 else ([(0, 1, 3), (1, 2, 3)] if kind == 'square' else [(0, 1, 2)])
                for cell in cells:
                    v = lattice_volume([corners[i] for i in cell])
                    for i in cell:
                        expected[A.index(corners[i])] += 2 * v
                for i, a in enumerate(corners):
                    edge_pairs = [(j, (j + 1) % len(corners)) for j in range(len(corners))]
                    expected[A.index(a)] -= sum(lattice_volume([corners[u], corners[v]]) for u, v in edge_pairs if i in (u, v))
                assert projected == expected
                records.append({'kind': kind, 'scale': scale, 'A_complete': A, 'heights_B': h,
                                'lower_hull_facets': facets, 'unused_A_points': [a for a in A if a not in corners],
                                'projected_massive_vector': projected, 'expected_Hurwitz_vector': expected,
                                'normalized_volume': desired_volume})
    result = {'status': 'PASS_EXPLICIT_COMPLETE_CONFIGURATIONS_WITH_UNUSED_COLUMNS', 'configurations': len(records),
              'records': records, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'independent_math_code_sha256': hashlib.sha256((HERE / 'independent_product_checks.py').read_bytes()).hexdigest(),
              'limits': 'Finite full configurations supplement the universal generic-height proof; no old code imported.'}
    (HERE / 'UNUSED_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))

if __name__ == '__main__':
    main()
