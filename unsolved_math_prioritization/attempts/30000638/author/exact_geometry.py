"""Small exact-integer geometry engine; no floating point or external packages."""
from itertools import combinations, product
from math import gcd, comb, factorial
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def det3(a, b, c):
    return dot(a, cross(b, c))


def checked_vertices(raw):
    require(type(raw) is list and 6 <= len(raw) <= 32, 'vertex-list shape')
    require(all(type(v) is list and len(v) == 3 and
                all(type(t) is int and -4 <= t <= 4 for t in v)
                for v in raw), 'integer 3D vertices in declared box')
    vs = [tuple(v) for v in raw]
    require(vs == sorted(set(vs)), 'canonical distinct points')
    require(all(tuple(-x for x in v) in vs for v in vs), 'origin symmetry')
    require(any(det3(*v) != 0 for v in combinations(vs, 3)), 'full dimension')
    return vs


def facets(vs):
    """Every 3D facet contains three affinely independent generating points."""
    result = {}
    for p, q, r in combinations(vs, 3):
        a = cross(sub(q, p), sub(r, p))
        if a == (0, 0, 0):
            continue
        b = dot(a, p)
        if b == 0:
            continue
        if b < 0:
            a, b = tuple(-x for x in a), -b
        g = gcd(gcd(abs(a[0]), abs(a[1])), abs(a[2]))
        require(b % g == 0, 'lattice plane normalization')
        a, b = tuple(x//g for x in a), b//g
        if all(dot(a, v) <= b for v in vs):
            result[a+(b,)] = [v for v in vs if dot(a, v) == b]
    require(len(result) >= 4, 'missing facets')
    return result


def planar_hull(points):
    """Return boundary vertices of a 2D convex hull, omitting collinear points."""
    pts = sorted(set(points))
    def orient(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    low, high = [], []
    for p in pts:
        while len(low) >= 2 and orient(low[-2], low[-1], p) <= 0:
            low.pop()
        low.append(p)
    for p in reversed(pts):
        while len(high) >= 2 and orient(high[-2], high[-1], p) <= 0:
            high.pop()
        high.append(p)
    return low[:-1]+high[:-1]


def facet_cycle(plane, points):
    # Dropping a coordinate with nonzero normal is an affine bijection of plane.
    drop = next(i for i in range(3) if plane[i] != 0)
    keep = [i for i in range(3) if i != drop]
    lookup = {tuple(v[i] for i in keep): v for v in points}
    return [lookup[p] for p in planar_hull(list(lookup))]


def exact_case(vertices):
    vs = checked_vertices(vertices)
    fs = facets(vs)
    volume6 = 0
    for plane, pts in fs.items():
        poly = facet_cycle(plane, pts)
        require(len(poly) >= 3, 'facet polygon')
        for i in range(1, len(poly)-1):
            value = abs(det3(poly[0], poly[i], poly[i+1]))
            require(value > 0, 'nondegenerate origin cone')
            volume6 += value
    bounds = [(min(v[i] for v in vs), max(v[i] for v in vs)) for i in range(3)]
    def count(k, strict=False):
        return sum(all(dot(plane[:3], p) < k*plane[3] if strict else
                       dot(plane[:3], p) <= k*plane[3] for plane in fs)
                   for p in product(*(range(k*lo, k*hi+1) for lo, hi in bounds)))
    interior = count(1, True)
    counts = [1]+[count(k) for k in range(1, 4)]
    hstar = [sum((-1)**j*comb(4, j)*counts[i-j] for j in range(i+1))
             for i in range(4)]
    require(interior % 2 == 1, 'odd interior count')
    require(hstar[3] == interior and sum(hstar) == volume6, 'Ehrhart-volume cross-check')
    require(all(h >= 0 for h in hstar), 'nonnegative hstar')
    return {'vertices': vertices, 'facet_count': len(fs), 'volume_normalized': volume6,
            'interior_count': interior, 'closed_counts_k0_to_k3': counts,
            'hstar': hstar, 'volume_gap': volume6-4*(interior+1),
            'strong_hstar_gaps': [hstar[i]-comb(3, i)-
                                  (comb(2, i-1) if 1 <= i <= 3 else 0)*(interior-1)
                                  for i in range(4)]}


def paired(points):
    return [list(v) for v in sorted(set(tuple(p) for p in points) |
                                   set(tuple(-x for x in p) for p in points))]


def canonical_inputs():
    """Deterministic bounded stress suite, not a classification."""
    cases = {}
    # Exact extremizers for 1 <= l <= 4; boxes and noncrosspolytopal examples.
    for l in range(1, 5):
        cases[f'cross_stretch_{l}'] = paired([(l,0,0),(0,1,0),(0,0,1)])
        cases[f'box_stretch_{l}'] = [list(v) for v in product((-l,l),(-1,1),(-1,1))]
    cases['hexagon_bipyramid'] = paired([(1,0,0),(0,1,0),(1,1,0),(0,0,1)])
    cases['cube_scale_2'] = [list(v) for v in product((-2,2), repeat=3)]
    cases['cross_scale_2'] = paired([(2,0,0),(0,2,0),(0,0,2)])
    cases['cross_skew_1'] = paired([(2,0,0),(1,2,0),(0,1,1)])
    cases['cross_skew_2'] = paired([(3,1,0),(1,2,1),(0,1,2)])
    # Fixed integer recurrence avoids dependence on random module implementations.
    state = 30000638
    for j in range(24):
        pts = {(1,0,0),(0,1,0),(0,0,1)}
        while len(pts) < 4+j%5:
            xyz = []
            for _ in range(3):
                state = (1664525*state+1013904223) % (2**32)
                xyz.append((state >> 9) % 7-3)
            if any(xyz):
                pts.add(tuple(xyz))
        cases[f'stress_{j:02d}'] = paired(pts)
    return dict(sorted(cases.items()))


def barrier_checks():
    # A coefficient vector satisfying only the expressly listed necessary tests.
    h = [1,11,11,7]
    I, n = h[-1], 3
    require(all(h[i] >= comb(n,i) for i in range(n+1)), 'binomial floor')
    require(all(h[i] >= h[1] for i in range(1,n)), 'Hibi floors')
    require(h[1] >= I+n-1, 'at least 2n boundary points')
    require(all((h[i]-comb(n,i)) % 2 == 0 for i in range(n+1)), 'parity test')
    require(sum(h) == 30 and 4*(I+1) == 32, 'formal gap')
    # Minkowski sufficient criterion misses the actual cube, not the conjecture.
    require(27+1 > 2*8, 'successive-minima obstruction')
    # An embedded crosspolytope has 7 interior points; its containing cube has 27.
    require(7 < 27 and 4*(7+1) < 4*(27+1), 'monotonicity obstruction')
    return {'formal_hstar': h, 'formal_gap': -2,
            'cube_I': 27, 'cube_lambda_product_numerator': 1,
            'cube_lambda_product_denominator': 8,
            'contained_2_crosspolytope_I': 7}


def residue_certificate(columns):
    a,b,c = [tuple(v) for v in columns]
    signed_D = det3(a,b,c)
    D = abs(signed_D)
    require(D > 0, 'nonsingular crosspolytope')
    adjrows = (cross(b,c),cross(c,a),cross(a,b))
    vs = [tuple(v) for v in paired(columns)]
    bounds = [(min(v[i] for v in vs),max(v[i] for v in vs)) for i in range(3)]
    buckets = {}
    for p in product(*(range(lo,hi+1) for lo,hi in bounds)):
        numerators = tuple(dot(r,p) for r in adjrows)
        if sum(abs(t) for t in numerators) < D:
            key = tuple(t % D for t in numerators)
            buckets.setdefault(key,[]).append(list(p))
    require(buckets.get((0,0,0)) == [[0,0,0]], 'zero coset unique')
    require(all(len(ps) <= 2 for ps in buckets.values()), 'coset capacity')
    I = sum(len(ps) for ps in buckets.values())
    require(I <= 2*D-1, 'crosspolytope theorem')
    return {'columns':columns,'determinant_absolute':D,'interior_count':I,
            'occupied_cosets':len(buckets),'maximum_coset_occupancy':max(map(len,buckets.values())),
            'normalized_volume':8*D,'theorem_gap':8*D-4*(I+1)}


def arithmetic_checks():
    # Eq. (2.4) in Henze: two independently expanded equal expressions.
    rows=[]
    for n in range(1,21):
        laguerre = sum((Fraction(comb(n,k)*2**k,factorial(k)) for k in range(n+1)),Fraction())
        davenport = sum((Fraction(comb(n,k)**2*factorial(k),2**k) for k in range(n+1)),Fraction())
        require(davenport == Fraction(factorial(n),2**n)*laguerre, 'Laguerre identity')
        rows.append({'n':n,'L_plus_at_2':[laguerre.numerator,laguerre.denominator]})
    for n,m in product(range(1,8),repeat=2):
        for I,J in product(range(1,20,2),repeat=2):
            gap=comb(n+m,n)*(I+1)*(J+1)-2*(I*J+1)
            require(gap>0,'Cartesian-product inequality')
    residue_inputs=[[[l,0,0],[0,1,0],[0,0,1]] for l in range(1,5)]
    residue_inputs += [[[2,0,0],[0,2,0],[0,0,2]],
                       [[2,0,0],[1,2,0],[0,1,1]],
                       [[3,1,0],[1,2,1],[0,1,2]]]
    return {'laguerre_rows':rows,'residue_cases':[residue_certificate(c) for c in residue_inputs],
            'product_parameter_checks':4900}


def expected_results():
    out = {'status':'PARTIAL_UNSOLVED',
           'finite_scope':'37 specified origin-symmetric 3D lattice hulls, not an exhaustive classification',
           'cases':{name:exact_case(v) for name,v in canonical_inputs().items()},
           'barriers':barrier_checks(),'arithmetic':arithmetic_checks()}
    require(len(out['cases']) == 37, 'declared scope')
    require(all(v['volume_gap'] >= 0 for v in out['cases'].values()), 'finite volume failure')
    require(all(min(v['strong_hstar_gaps']) >= 0 for v in out['cases'].values()), 'finite coefficient failure')
    return out
