#!/usr/bin/env python3
"""Independent exact audit of frozen Dolnikov packet. Python standard library.

The lattice and diamond verifiers do not import any author geometry/cover code.
The final comparison section calls author routines only as implementations under
test; its oracle is independently computed intersection half-plane feasibility.
Run: python -B reviewer_checks.py [path/to/dolnikov_30005804]
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations, product
from functools import lru_cache
import hashlib
import importlib.util
import json
import random
import sys

PACKET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
checks = 0

def require(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)

def maximal_masks(masks):
    masks = set(masks) - {0}
    return sorted(m for m in masks if not any(m != n and m & n == m for n in masks))

def cover_table(n, masks):
    # Bottom-up recurrence: all residual states are numerically smaller.
    by_point = [[m for m in masks if m & (1 << i)] for i in range(n)]
    out = [0] * (1 << n)
    for s in range(1, 1 << n):
        i = (s & -s).bit_length() - 1
        out[s] = 1 + min(out[s & ~m] for m in by_point[i])
    return out

def audit_integrity():
    raw = (PACKET / 'TURN_5_MANIFEST.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == '4c77bd766217a50903162ab441416b2a3d5f003f1af6b13ca3db982d82d33b1d', 'pinned manifest digest')
    manifest = json.loads(raw)
    for entry in manifest['files']:
        data = (PACKET / entry['path']).read_bytes()
        require(len(data) == entry['bytes'], 'bytes: ' + entry['path'])
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'hash: ' + entry['path'])
    receipt = json.loads((PACKET / 'TURN_5_REMOTE_RECEIPT.json').read_text())
    require(receipt['head'] == '08e3f30b26bb9cd7487ad7f6db8373a4e796a343', 'receipt head')
    for entry in receipt['files']:
        data = (PACKET / entry['path']).read_bytes()
        git_hash = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(git_hash == entry['sha'] and len(data) == entry['size'], 'receipt blob: ' + entry['path'])
    return {'manifest_entries': len(manifest['files']), 'checkpoint_files_including_manifest': len(manifest['files']) + 1,
            'receipt_git_blobs_verified_locally': len(receipt['files']), 'remote_ref_independently_fetched': False,
            'extra_local_receipt': 'TURN_5_REMOTE_RECEIPT.json', 'pinned_manifest_sha256': hashlib.sha256(raw).hexdigest()}

def trap_contains(m, point, center):
    x, y = point[0] - center[0], point[1] - center[1]
    return 0 <= y <= 1 and x >= 0 and x + (m - 1) * y <= m

def trap_common(m, centers):
    # For K_m+t, x>=t_x, y>=t_y, y<=t_y+1,
    # x+(m-1)y<=m+t_x+(m-1)t_y. The lower-left corner is feasible iff any point is.
    x = max(t[0] for t in centers)
    y = max(t[1] for t in centers)
    return all(trap_contains(m, (x, y), t) for t in centers)

def audit_lattice():
    saved = json.loads((PACKET / 'LATTICE_CERTIFICATE.json').read_text())
    results = []
    for record in saved:
        m = record['m']
        # Generate D lattice points by direct intersection of two trapezoids,
        # never by an author hull or point-in-polygon routine.
        U = [(x, y) for x in range(-m, m + 1) for y in range(-1, 2)
             if trap_common(m, [(0, 0), (x, y)])]
        V = [(x, y) for x in range(-2*m, 2*m + 1) for y in range(-2, 3)
             if trap_common(m, [(0, 0), (Q(x, 2), Q(y, 2))])]
        require(list(map(list, U)) == record['U'], f'U_{m}')
        require(list(map(list, V)) == record['V'], f'V_{m}')
        # Every nonempty common intersection contains (max t_x,max t_y).
        # Thus this Cartesian set is complete and unrelated to edge arrangements.
        candidates = product(sorted({x for x, y in U}), sorted({y for x, y in U}))
        masks = maximal_masks(sum(1 << i for i, t in enumerate(U) if trap_contains(m, p, t)) for p in candidates)
        values = cover_table(len(U), masks)
        critical = []
        bad = []
        common_checks = 0
        for s in range(1, 1 << len(U)):
            chosen = [t for i, t in enumerate(U) if s & (1 << i)]
            # Independent common-intersection predicate validates every state.
            require((values[s] == 1) == trap_common(m, chosen), f'one-point test m={m}, mask={s}')
            if values[s] <= 3:
                continue
            bad.append(s)
            if any(values[s ^ (1 << i)] > 3 for i in range(len(U)) if s & (1 << i)):
                continue
            require(values[s] == 4, 'critical piercing number')
            neighbors = [v for v in V if all(trap_common(m, [t, v]) for t in chosen)]
            common_checks += len(V)
            require(neighbors == [(0, 0)], f'singleton common neighbors m={m}, mask={s}')
            critical.append({'mask': s, 'common_neighbors': list(map(list, neighbors))})
        require(critical == record['critical'], f'all critical certificate entries m={m}')
        for s in bad:
            require(any(s & e['mask'] == e['mask'] for e in critical), 'all bad subsets have saved critical core')
        results.append({'m': m, 'U_size': len(U), 'V_size': len(V), 'subsets': len(values),
                        'bad_subsets': len(bad), 'critical_subsets': len(critical),
                        'direct_coverage_masks': len(masks), 'common_neighbor_tests': common_checks})
    return results

def audit_diamond():
    saved = json.loads((PACKET / 'SQUARE_COVER_BARRIER.json').read_text())
    T = [tuple(map(Q, p)) for p in saved['boundary_points']]
    expected = sorted({(Q(i, 4), Q(j, 4)) for i in range(5) for j in range(5) if i in (0, 4) or j in (0, 4)})
    require(T == expected, '16 boundary points')
    # |dx|+|dy|<=1/2 iff max(|du|,|dv|)<=1/2,
    # u=x+y, v=x-y. Covering becomes unit axis-parallel square covering.
    Z = [(x+y, x-y) for x, y in T]
    masks = maximal_masks(sum(1 << i for i, (u, v) in enumerate(Z)
                              if u0 <= u <= u0+1 and v0 <= v <= v0+1)
                          for u0, v0 in product({p[0] for p in Z}, {p[1] for p in Z}))
    require(masks == [e['mask'] for e in saved['maximal_coverage_masks']], 'all maximal diamond masks')
    full = (1 << len(T)) - 1
    triple_tests = 0
    for c in combinations(masks, 3):
        triple_tests += 1
        require(c[0] | c[1] | c[2] != full, 'three translated diamonds never cover witness')
    values = cover_table(len(T), masks)
    require(values[full] == saved['minimum_cover_number'] == 4, 'exact diamond optimum')
    for entry in saved['maximal_coverage_masks']:
        x, y = map(Q, entry['point'])
        direct = sum(1 << i for i, (a, b) in enumerate(T) if abs(x-a)+abs(y-b) <= Q(1, 2))
        require(direct == entry['mask'], 'saved diamond witness incidence')
    points = [tuple(map(Q, p)) for p in saved['optimal_cover']]
    require(len(points) == 4, 'four-point upper certificate')
    require(all(any(abs(x-a)+abs(y-b) <= Q(1, 2) for x, y in points) for a, b in T), 'all boundary points covered')
    require(abs(Q(1))+abs(Q(1)) > 1, '(1,1) outside D, forbids repeated square color set')
    return {'points': len(T), 'maximal_masks': len(masks), 'all_distinct_triples_refuted': triple_tests,
            'minimum_cover_number': values[full], 'independent_method': 'L1-to-Linf linear change and complete Cartesian cover candidates'}

def inequalities(poly):
    # a*x+b*y<=c, with no hull routine or edge-segment intersections.
    out = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        a, b = q[1]-p[1], p[0]-q[0]
        out.append((a, b, a*p[0]+b*p[1]))
    return out

def common_halfplanes(H, centers):
    if not centers:
        return True
    C = [(a, b, min(c+a*x+b*y for x, y in centers)) for a, b, c in H]
    for (a, b, c), (d, e, f) in combinations(C, 2):
        det = a*e-b*d
        if det == 0:
            continue
        x, y = Q(c*e-b*f, det), Q(a*f-c*d, det)
        if all(A*x+B*y <= R for A, B, R in C):
            return True
    return False

def audit_geometry_implementation():
    # The author's geometry is the system under test, not the feasibility oracle.
    spec = importlib.util.spec_from_file_location('author_exact_geometry', PACKET/'exact_geometry.py')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    shapes = [list(map(lambda p: tuple(map(Q, p)), p)) for p in [
        [(0,0),(1,0),(1,1),(0,1)], [(0,0),(2,0),(0,2)],
        [(0,0),(3,0),(1,1),(0,1)], [(0,0),(2,0),(3,1),(1,3),(0,2)],
        [(0,0),(3,1),(4,3),(1,2)]]]
    # Includes exact same edges, segment intersections, singleton intersections,
    # positive-area intersections and rational offsets, plus affine shears.
    offsets = [(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)),(Q(1),Q(1)),
               (Q(-1),Q(0)),(Q(1,2),Q(1,2)),(Q(0),Q(0))]
    subset_tests = 0
    coverage_tests = 0
    for poly in shapes:
        for shear in (Q(0), Q(2,3)):
            P = [(x+shear*y, y) for x, y in poly]
            T = [(x+shear*y, y) for x, y in offsets]
            H = inequalities(P)
            polygons = [[(x+a,y+b) for x,y in P] for a,b in T]
            coverage = author.masks(polygons)
            feasible = [True]
            for s in range(1, 1 << len(T)):
                yes = common_halfplanes(H, [t for i,t in enumerate(T) if s & (1 << i)])
                feasible.append(yes)
                require(yes == any(m & s == s for m in coverage), 'arrangement candidate completeness vs independent halfplanes')
                subset_tests += 1
            # Independent exact partitioning into feasible common-intersection
            # classes. This does not compute Helly edges using author masks.
            dp = [0] * len(feasible)
            for s in range(1, len(feasible)):
                pivot = s & -s
                best = s.bit_count()
                t = s
                while t:
                    if t & pivot and feasible[t]:
                        best = min(best, 1 + dp[s ^ t])
                    t = (t - 1) & s
                dp[s] = best
                require(best == author.min_cover(s, coverage), 'exact cover vs independent partition oracle')
                require(best == author.hypergraph_chromatic(s, coverage), 'Helly coloring vs independent partition oracle')
                coverage_tests += 1
    return {'families': len(shapes)*2, 'common_intersection_subset_tests': subset_tests,
            'cover_and_Helly_subset_comparisons': coverage_tests, 'arithmetic': 'Fraction; all inequalities closed'}

def audit_constructions():
    # Independent half-plane oracle checks the author's construction interfaces.
    sys.path.insert(0, str(PACKET))
    from row_geometry import row_piercing
    from margin_geometry import normalize, rectangle, margin_piercing
    rng = random.Random(8403001)
    det = lambda a,b: a[0]*b[1]-a[1]*b[0]
    shapes = [list(map(lambda p: tuple(map(Q, p)), p)) for p in [
        [(0,0),(1,0),(1,1),(0,1)], [(0,0),(2,0),(0,2)],
        [(0,0),(3,0),(1,1),(0,1)], [(0,0),(2,0),(3,1),(1,3),(0,2)],
        [(0,0),(3,1),(4,3),(1,2)]]]
    branches = [0,0]
    row_cases = margin_cases = 0
    for raw in shapes:
        for shear in (Q(0), Q(2,3)):
            K = [(x+shear*y+Q(2,7), y-Q(3,5)) for x,y in raw]
            H = inequalities(K)
            N,f,g,(u,v) = normalize(K)
            diffs = [(a[0]-b[0],a[1]-b[1]) for a,b in product(K,K)]
            delta = max(abs(det(a,b)) for a,b in product(diffs,diffs))
            require(det(u,v) == delta > 0, 'normalization reaches independent global determinant maximum')
            require(all(g(f(p)) == p for p in K), 'normalization inverse')
            require(max(p[0] for p in N)-min(p[0] for p in N) == 1, 'normalized x projection width')
            require(max(p[1] for p in N)-min(p[1] for p in N) == 1, 'normalized y projection width')
            reflected_H = inequalities([(-x,-y) for x,y in N])
            for lam in (Q(1,100),Q(1,2),Q(3,4),Q(99,100)):
                lower,R = rectangle(N,lam)
                require(all(all(a*x+b*y <= c for a,b,c in reflected_H) for x,y in R), 'closed inscribed rectangle')
                require(max(x for x,y in R)-min(x for x,y in R) == lam, 'rectangle width')
                require(max(y for x,y in R)-min(y for x,y in R) == 1-lam, 'rectangle height')
                if lam > Q(3,4):
                    continue
                # Each center is in (lam/2)D; cross differences are in lam D.
                Z = [(lam*x/2,lam*y/2) for x,y in diffs]
                colors = [rng.sample(Z, min(9,len(Z))) for _ in range(3)]
                require(all(common_halfplanes(H,[(a[0]/lam,a[1]/lam),(b[0]/lam,b[1]/lam)])
                            for i in range(3) for j in range(i) for a in colors[i] for b in colors[j]), 'margin premise via independent intersection')
                selected,points,_ = margin_piercing(K,colors,lam)
                require(len(points) <= 3, 'margin output cardinality')
                require(all(any(all(a*(q[0]-t[0])+b*(q[1]-t[1]) <= c for a,b,c in H) for q in points)
                            for t in colors[selected]), 'margin output incidence via independent inequalities')
                margin_cases += 1
            grid = [(Q(x,2),Q(y,2)) for x in range(-4,5) for y in range(-2,3)]
            U = [p for p in grid if common_halfplanes(H,[(0,0),p])]
            for _ in range(15):
                heights = rng.sample(sorted({y for x,y in U}),min(3,len({y for x,y in U})))
                pool = [p for p in U if p[1] in heights]
                A = rng.sample(pool,min(6,len(pool)))
                Bpool = [b for b in grid if all(common_halfplanes(H,[a,b]) for a in A)]
                require((0,0) in Bpool, 'row common-neighbor nonempty')
                heights = rng.sample(sorted({y for x,y in Bpool}),min(3,len({y for x,y in Bpool})))
                B = [p for p in Bpool if p[1] in heights]
                selected,points = row_piercing(K,A,B)
                branches[selected] += 1
                require(len(points) <= len({y for x,y in (A,B)[selected]}) <= 3, 'row output cardinality')
                require(all(any(all(a*(q[0]-t[0])+b*(q[1]-t[1]) <= c for a,b,c in H) for q in points)
                            for t in (A,B)[selected]), 'row output incidence via independent inequalities')
                row_cases += 1
    require(all(branches), 'both row branches exercised')
    return {'normalized_polygons': 10, 'rectangle_parameters': ['1/100','1/2','3/4','99/100'],
            'row_cases': row_cases, 'row_branches': branches, 'margin_cases': margin_cases,
            'scope': 'Finite implementation controls, not a proof over all convex bodies'}

def main():
    result = {'status': 'PASS_SCOPED', 'integrity': audit_integrity(), 'lattice': audit_lattice(),
              'diamond': audit_diamond(), 'geometry_implementation': audit_geometry_implementation(),
              'construction_controls': audit_constructions()}
    result['reviewer_require_calls'] = checks
    result['scope'] = 'Finite exact certificate verification and implementation controls; universal analytic theorems audited separately in REVIEW.md. Original unresolved.'
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
