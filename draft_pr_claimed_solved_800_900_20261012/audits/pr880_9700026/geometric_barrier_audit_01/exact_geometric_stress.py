#!/usr/bin/env python3
"""Independent finite exact-arithmetic stress; no author verifier is imported.

These checks test the stated geometric constants and selected rational points.
The continuum inclusion and the all-time result require the analytical proof.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def need(value, message):
    if not value:
        raise RuntimeError(message)


def d2(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def wins(zi, zj, di2, dj2, a, b):
    """q=a/b: compare the hard-max influence after positive integer powers."""
    return zi**(2*a) * dj2**b >= zj**(2*a) * di2**b


def geometry(points, h):
    need(h > 0, 'h must be positive')
    for i, x in enumerate(points):
        need(len(x) == 2 and all(h <= v <= 1-h for v in x), 'domain failure')
        for y in points[:i]:
            need(d2(x, y) >= 8*h*h, 'all-competitor separation failure')


def witness():
    data = json.loads((AUDIT/'source/author/certificate.json').read_text())
    x = [tuple(map(F, row)) for row in data['cities']]
    z = list(map(F, data['initial_weights']))
    h = F(data['square_halfwidth'])
    alpha, beta = F(data['alpha']), F(data['beta'])
    geometry(x, h)
    need(alpha > 1 and beta > 2*alpha, 'incorrect literal refutation parameters')
    need(all(w > 0 for w in z) and sum(z) == 1, 'invalid probability vector')
    q, p, k = alpha/beta, 2*alpha/beta, 4*h*h
    need(q == F(1, 4) and p == F(1, 2), 'wrong exponents')
    lower = k*k
    upper = 1-(len(x)-1)*lower
    need(k == F(1, 64) and lower == F(1, 4096), 'wrong derived constants')
    need(all(w >= lower for w in z), 'initial state below claimed fixed barrier')
    need(upper == F(2047, 2048), 'wrong simplex upper bound')
    for key, value in [('claimed_p', p), ('claimed_K', k),
                       ('claimed_lower_bound', lower), ('claimed_upper_bound', upper)]:
        need(F(data[key]) == value, 'certificate field disagrees with independent arithmetic')
    determinant = ((x[1][0]-x[0][0])*(x[2][1]-x[0][1])
                   -(x[1][1]-x[0][1])*(x[2][0]-x[0][0]))
    distances = [d2(x[i], x[j]) for i in range(len(x)) for j in range(i)]
    need(determinant != 0 and len(set(distances)) == 3, 'special triangle degeneracy')
    return {
        'q': str(q), 'p': str(p), 'K': str(k),
        'all_time_lower': str(lower), 'all_time_upper': str(upper),
        'pairwise_squared_distances': list(map(str, distances)),
        'separation_margins': [str(v-8*h*h) for v in distances],
        'boundary_margin': str(min(min(v, 1-v) for row in x for v in row)-h),
        'triangle_determinant': str(determinant),
    }


def stress():
    geometries = [
        ('separation_equality', [(F(1,4),F(1,4)), (F(1,2),F(1,2))], F(1,8)),
        ('boundary_square_contact', [(F(1,8),F(1,8)), (F(3,4),F(3,4))], F(1,8)),
        ('near_coincident_sites', [(F(1,2),F(1,2)),
                                   (F(1,2)+F(1,2**20),F(1,2))], F(1,2**23)),
        ('asymmetric_three', [(F(1,5),F(1,4)), (F(3,4),F(1,3)),
                              (F(2,5),F(4,5))], F(1,16)),
        ('eight_competitors', [(F(i,5),F(j,3)) for i in range(1,5)
                              for j in range(1,3)], F(1,40)),
    ]
    exponents = [(1,3), (1,4), (2,5), (3,7), (1,25)]
    samples = (F(1,2), F(1,3), F(1,17), F(1,997))
    offsets = (F(-1), F(-1,2), F(0), F(1,2), F(1))
    count = 0
    by_geometry = {}
    for label, points, h in geometries:
        geometry(points, h)
        start = count
        n = len(points)
        for a, b in exponents:
            need(0 < 2*a < b, 'stress exponent outside persistence range')
            for i in range(n):
                others = [j for j in range(n) if j != i]
                for s in samples:
                    # zi=s^b makes zi^(a/b)=s^a rational exactly.
                    z = [F(0)]*n
                    z[i] = s**b
                    masses = [F(10**rank) for rank in range(len(others))]
                    total = sum(masses)
                    for j, mass in zip(others, masses):
                        z[j] = (1-z[i])*mass/total
                    need(all(w > 0 for w in z) and sum(z) == 1, 'bad stress state')
                    for u in offsets:
                        for v in offsets:
                            y = (points[i][0]+h*s**a*u, points[i][1]+h*s**a*v)
                            need(all(0 <= c <= 1 for c in y), 'capture point outside square')
                            for j in others:
                                need(wins(z[i], z[j], d2(y, points[i]),
                                          d2(y, points[j]), a, b), 'capture square lost a point')
                                count += 1
        by_geometry[label] = count-start
    return {'exact_comparisons': count, 'by_geometry': by_geometry,
            'q_values': [str(F(a,b)) for a,b in exponents],
            'smallest_target_weight': str(F(1,997)**25),
            'grid_points_per_square': 25}


def negative_controls():
    controls = []
    points = [(F(1,4),F(1,4)), (F(1,2),F(1,2))]
    h = F(1,8)
    geometry(points, h)
    zi, zj = F(1,16), F(16)
    y = (F(5,16),F(5,16))
    need(not wins(zi,zj,d2(y,points[0]),d2(y,points[1]),1,4),
         'normalization-negative control did not lose')
    controls.append('Without probability normalization a stated capture point loses to a weight > 1.')

    y = (F(3,8),F(3,8))
    need(not wins(F(1,16),F(15,16),d2(y,points[0]),d2(y,points[1]),1,4),
         'oversized square control did not lose')
    controls.append('Doubling h past the separation hypothesis loses a normalized capture point.')

    points3 = [(F(1,4),F(1,4)), (F(3,4),F(3,4)), (F(3,8),F(1,4))]
    y = (F(5,16),F(1,4))
    need(d2(points3[0],points3[1]) >= 8*h*h, 'far-only geometry should pass')
    need(not wins(F(1,16),F(7,8),d2(y,points3[0]),d2(y,points3[2]),1,4),
         'omitted competitor control did not lose')
    controls.append('Checking only a distant competitor misses a nearer dominant third city.')

    k, z = F(1,64), F(1,4096)
    need(k*z-z < 0 and k*z*z-z < 0, 'critical/supercritical derivative controls')
    controls.append('At area powers p=1 and p=2 the same small-z scalar bound points downward.')

    lower = k*k
    for s in [k/F(10), k/F(2), k, k*2]:
        derivative = k*s-s*s  # z=s^2, p=1/2 exactly.
        need((derivative > 0) == (s < k), 'subthreshold comparison sign error')
        need((derivative == 0) == (s == k), 'threshold equality error')
    controls.append('The p=1/2 scalar bound has the correct upward/equality/downward threshold signs.')
    need(F(1,1000000) < lower, 'small-start control not small')
    u0 = F(1,1000)
    for v in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        bracket = k+(u0-k)*v
        need(bracket > 0 and bracket**2 >= min(u0*u0,lower),
             'below-threshold initial condition comparison failed')
    controls.append('A positive initial coordinate below K^2 keeps the smaller valid all-time bound.')
    return controls


def algebra():
    count = 0
    for a,b in [(1,3),(1,4),(2,5),(3,7),(1,25)]:
        p = F(2*a,b)
        r = 1/(1-p)
        need(r*(1-p) == 1 and p*r == r-1, 'comparison power identities')
        count += 2
    return {'exact_power_identities': count,
            'meaning': 'Finite identities support, but do not replace, the chain-rule proof.'}


def main():
    pins = {}
    for name in ['SOURCE_MANIFEST.json','source/author/PROOF.md',
                 'source/author/certificate.json','source/author/verify.py']:
        payload = (AUDIT/name).read_bytes()
        pins[name] = {'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
    need(pins['SOURCE_MANIFEST.json']['sha256'] ==
         'b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b',
         'wrong frozen source manifest')
    need(pins['source/author/PROOF.md']['sha256'] ==
         '8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767',
         'wrong frozen proof')
    result = {'status': 'PASS', 'scope': 'Independent exact finite stress, not continuum/time proof',
              'pins': pins, 'witness': witness(), 'stress': stress(),
              'controls': negative_controls(), 'comparison_algebra': algebra()}
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    (HERE/'EXACT_STRESS_RESULTS.json').write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
