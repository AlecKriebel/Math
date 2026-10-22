#!/usr/bin/env python3
"""Exact finite checks for the authored partial-result packet. No assert statements."""
import argparse
from fractions import Fraction
from itertools import combinations
import json
import math
import os
from pathlib import Path
import sys
import hashlib

class CheckFailure(Exception):
    pass

COUNTS = {}

def check(condition, message):
    if not condition:
        raise CheckFailure(message)

def bump(name, value=1):
    COUNTS[name] = COUNTS.get(name, 0) + value

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
    p = sorted(set(points))
    if len(p) <= 1:
        return p
    lo = []
    for x in p:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], x) <= 0:
            lo.pop()
        lo.append(x)
    hi = []
    for x in reversed(p):
        while len(hi) >= 2 and orient(hi[-2], hi[-1], x) <= 0:
            hi.pop()
        hi.append(x)
    return lo[:-1] + hi[:-1]

def in_closed_hull(p, poly):
    if not poly:
        return False
    if len(poly) == 1:
        return p == poly[0]
    if len(poly) == 2:
        a, b = poly
        return orient(a, b, p) == 0 and all(min(a[i], b[i]) <= p[i] <= max(a[i], b[i]) for i in (0, 1))
    return all(orient(poly[i], poly[(i+1) % len(poly)], p) >= 0 for i in range(len(poly)))

def in_interior(p, poly):
    return len(poly) >= 3 and all(orient(poly[i], poly[(i+1) % len(poly)], p) > 0 for i in range(len(poly)))

def strict(points):
    return len(points) >= 3 and len(set(points)) == len(points) and len(hull(points)) == len(points)

def is_hole(P, S, k=6):
    if len(S) != k or not set(S).issubset(P) or not strict(S):
        return False
    poly = hull(S)
    return all(p in S or not in_closed_hull(p, poly) for p in P)

def find_hole(P, k=6):
    for S in combinations(P, k):
        if is_hole(P, S, k):
            return list(S)
    return None

def max_line(P):
    if len(P) < 2:
        return len(P)
    return max(sum(orient(a, b, c) == 0 for c in P) for a, b in combinations(P, 2))

def area2(poly):
    return abs(sum(poly[i][0]*poly[(i+1) % len(poly)][1]-poly[i][1]*poly[(i+1) % len(poly)][0] for i in range(len(poly))))

def boundary_cleanup(P, S):
    check(strict(S), 'cleanup requires strict input')
    K = hull(S)
    check(not any(in_interior(p, K) for p in P), 'cleanup requires interior emptiness')
    inside = [p for p in P if in_closed_hull(p, K)]
    choices = [hull(T) for T in combinations(inside, len(S)) if strict(T)]
    check(bool(choices), 'cleanup candidate family absent')
    T = min(choices, key=lambda T: (area2(T), T))
    check(is_hole(P, T, len(S)), 'minimum-area cleanup was not closed-empty')
    return T

def extension_regions(S, q):
    H = hull(S)
    values = [orient(H[i], H[(i+1) % len(H)], q) for i in range(len(H))]
    return [i for i, v in enumerate(values) if v < 0 and all(w > 0 for j, w in enumerate(values) if j != i)]

def nearest_ear(P, S, i):
    H = hull(S)
    candidates = [q for q in P if i in extension_regions(S, q)]
    check(bool(candidates), 'ear region is empty')
    q = min(candidates, key=lambda q: (-orient(H[i], H[(i+1) % len(H)], q), q))
    check(is_hole(P, list(S)+[q], len(S)+1), 'nearest-ear conclusion failed')
    return q

def affine(P):
    # Integer invertible map with negative determinant.
    return [(3*x+2*y+7, x-y-11) for x, y in P]

def run_tests(fixtures):
    check(fixtures.get('schema') == 1, 'unexpected fixture schema')
    F = {name: [tuple(p) for p in value] for name, value in fixtures['point_sets'].items()}
    required = {'degenerate_six','hexagon','boundary_blocker','pentagon','ear_candidates','two_edge_point','sparse_triples'}
    check(set(F) == required, 'missing or unexpected point-set fixtures')
    for name, P in F.items():
        check(len(P) == len(set(P)), 'duplicate fixture points: '+name)
        check(all(len(p) == 2 and all(type(v) is int for v in p) for p in P), 'noninteger fixture coordinate')
        bump('fixture_sets')
    # Definition boundaries: no floating point and no ignoring edge blockers.
    H = F['hexagon']
    check(is_hole(H, H), 'six convex vertices should be a hole')
    P = H + F['boundary_blocker']
    check(not is_hole(P, H), 'closed edge blocker was ignored')
    check(not any(in_interior(p, hull(H)) for p in P), 'boundary fixture has an interior blocker')
    T = boundary_cleanup(P, H)
    check(area2(hull(T)) < area2(hull(H)), 'cleanup did not reduce area')
    check(is_hole(affine(P), affine(T)), 'affine/reflection invariance failed')
    for k in range(3, 7):
        S = H[:k]
        if strict(S) and not any(in_interior(p, hull(S)) for p in P):
            boundary_cleanup(P, S)
            bump('cleanup_sizes')
    for invalid in ([], [(0,0)], [(0,0),(1,0)], [(0,0),(1,0),(2,0)]):
        check(not strict(invalid), 'degenerate strictness accepted')
        check(not is_hole(invalid, invalid), 'degenerate hexagon accepted')
        bump('degenerate_rejections')
    check(in_closed_hull((1,0), [(0,0),(2,0)]), 'segment midpoint missing')
    check(not in_closed_hull((3,0), [(0,0),(2,0)]), 'segment extension accepted')
    check(not in_interior((1,0), [(0,0),(2,0)]), 'segment has plane interior')
    # Exact perturbation degeneracy at eight rational scales.
    W = F['degenerate_six']
    check(max_line(W) == 3 and len(hull(W)) == 3, 'weak-six fixture wrong')
    check(not is_hole(W, W), 'weak six incorrectly called strict hexagon')
    for power in range(1, 9):
        e = Fraction(1, 2**power)
        R = [(0,0),(2,-e),(4,0),(2+e,2+e),(0,4),(-e,2)]
        check(is_hole(R, R), 'perturbed six not an empty strict hexagon')
        bump('perturbation_scales')
    # Full finite parity/grid enumeration; this is not the universal proof.
    for m in (2, 3, 4):
        G = [(x,y) for x in range(m) for y in range(m)]
        check(max_line(G) == m, 'grid collinearity mismatch')
        for k in (5, 6):
            for S in combinations(G, k):
                bump('grid_subsets_'+str(k))
                check(not is_hole(G, S, k), 'grid hole found')
                if strict(S):
                    same = next(((a,b) for a,b in combinations(S,2) if (a[0]-b[0]) % 2 == 0 and (a[1]-b[1]) % 2 == 0), None)
                    check(same is not None, 'parity pair absent')
                    a,b = same
                    c = ((a[0]+b[0])//2, (a[1]+b[1])//2)
                    check(c in G and c not in S and in_closed_hull(c,hull(S)), 'midpoint blocker certificate invalid')
                    bump('parity_blocker_certificates')
    check(COUNTS.get('grid_subsets_5') == 4494, 'wrong 5-grid enumeration count')
    check(COUNTS.get('grid_subsets_6') == 8092, 'wrong 6-grid enumeration count')
    # Ambient versus subset holes and the d=1, n=61 slab construction.
    Q = [(i,i*i) for i in range(60)]
    D = [(2,7)]
    check(max_line(Q) == 2, 'parabola was not general position')
    left,right = Q[:6],Q[30:36]
    check(is_hole(Q,left) and is_hole(Q,right), 'block holes invalid relative to Q')
    check(not is_hole(Q+D,left), 'ambient blocker was ignored')
    check(is_hole(Q+D,right), 'clean slab hexagon blocked')
    check(len(Q+D) == 31*len(D)+30, 'slab threshold fixture wrong')
    bump('slab_threshold_instances')
    # Six independently specified collinear triples, and no cross triple.
    R = F['sparse_triples']
    check(len(R) == 18, 'sparse triple fixture wrong size')
    actual = {tuple(ids) for ids in combinations(range(18),3) if orient(*(R[i] for i in ids)) == 0}
    intended = {tuple(range(3*i,3*i+3)) for i in range(6)}
    check(actual == intended, 'unexpected collinearity among sparse triples')
    check(max_line(R) == 3, 'sparse fixture has four collinear')
    Q2 = [p for i,p in enumerate(R) if i % 3 != 1]
    check(max_line(Q2) == 2, 'one-per-triple deletion did not give general position')
    bump('sparse_disjoint_triples', 6)
    # Check the maximal-GP extraction inequality on every subset of the 3x3 grid.
    pool = [(x,y) for x in range(3) for y in range(3)]
    for mask in range(1, 1 << len(pool)):
        P0 = [p for i,p in enumerate(pool) if mask >> i & 1]
        A = []
        for p in P0:
            if all(orient(a,b,p) != 0 for a,b in combinations(A,2)):
                A.append(p)
        ell = max(3, max_line(P0)+1)
        bound = len(A)+(ell-3)*math.comb(len(A),2)
        check(len(P0) <= bound, 'maximal-GP extraction inequality failed')
        bump('maximal_gp_instances')
    # Boundary-only theorem on every subset of a six-corner boundary with one
    # edge-interior point per side. Applicability is counted, not assumed.
    B = list(H)
    for i,a in enumerate(H):
        b = H[(i+1) % len(H)]
        B.append(((a[0]+b[0])//2,(a[1]+b[1])//2))
    check(len(set(B)) == 12, 'boundary pool duplicate')
    for mask in range(1, 1 << 12):
        P0 = [p for i,p in enumerate(B) if mask >> i & 1]
        K = hull(P0)
        check(not any(in_interior(p,K) for p in P0), 'boundary pool was not weakly convex')
        ell = max(3,max_line(P0)+1)
        if len(P0) > 5*(ell-2):
            check(find_hole(P0) is not None, 'boundary-only theorem finite instance failed')
            bump('boundary_theorem_applicable_instances')
        bump('boundary_subsets')
    check(COUNTS.get('boundary_theorem_applicable_instances',0) > 0, 'boundary theorem tests were vacuous')
    # Ear regions: a farther candidate is edge-blocked; the nearest works.
    S = F['pentagon']
    C = F['ear_candidates']
    check(is_hole(S+C,S,5), 'ear base pentagon is not empty')
    check(not is_hole(S+C,S+[(2,-2)]), 'far ear side blockers ignored')
    region = extension_regions(S,C[0])
    check(len(region) == 1, 'ear region classification failed')
    nearest_ear(S+C,S,region[0])
    bump('ear_extensions')
    P0 = S+F['two_edge_point']
    q = F['two_edge_point'][0]
    check(is_hole(P0,S,5) and max_line(P0) == 2, 'two-edge example assumptions failed')
    check(len(hull(P0)) == 5 and not is_hole(P0,P0), 'two-edge hull conclusion failed')
    check(not extension_regions(S,q), 'two-edge point lies in an ear region')
    bump('ear_occupancy_obstructions')
    # Exhaustive rational ear candidates in a bounded integer box, each checked
    # as a finite instance of the minimizing argument, never as universal proof.
    candidates = [(x,y) for x in range(-3,8) for y in range(-3,8) if (x,y) not in S]
    for i in range(5):
        E = [q for q in candidates if i in extension_regions(S,q)]
        if E:
            P0 = S+E
            check(is_hole(P0,S,5), 'region candidates invaded base pentagon')
            nearest_ear(P0,S,i)
            bump('ear_region_grid_instances')
            bump('ear_region_grid_points',len(E))
    check(COUNTS.get('ear_region_grid_instances') == 5, 'not all five ear regions exercised')
    return COUNTS

def check_readonly(root):
    check(os.getuid() == 1000, 'readonly trial requires actual UID 1000')
    check(os.geteuid() == 1000, 'readonly trial requires effective UID 1000')
    check(root.stat().st_mode & 0o222 == 0, 'packet root is writable by mode')
    for p in root.iterdir():
        check(p.is_file() and not p.is_symlink(), 'unexpected packet entry')
        check(p.stat().st_mode & 0o222 == 0, 'packet file writable by mode: '+p.name)
    probes=[]
    for target,mode in ((root/'README.md','r+'),(root/'.forbidden-write-probe','x')):
        try:
            f=target.open(mode)
        except PermissionError:
            probes.append({'target':target.name,'operation':mode,'result':'PermissionError'})
        else:
            f.close()
            if mode == 'x':
                target.unlink()
            raise CheckFailure('write probe unexpectedly succeeded: '+target.name)
    return probes

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fixtures',type=Path,default=Path(__file__).resolve().parent/'fixtures.json')
    ap.add_argument('--readonly',action='store_true')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    try:
        check(args.fixtures.is_file(), 'required fixture input missing: '+str(args.fixtures))
        data=args.fixtures.read_bytes()
        fixtures=json.loads(data)
        probes=check_readonly(root) if args.readonly else []
        counts=run_tests(fixtures)
        output={'status':'PASS','scope':'exact finite fixture checks only; not a universal proof',
                'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,
                'python':sys.version.split()[0], 'counts':counts,'write_probes':probes,
                'fixtures_sha256':hashlib.sha256(data).hexdigest(),
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        print(json.dumps(output,sort_keys=True,indent=2))
        return 0
    except (CheckFailure,OSError,ValueError,TypeError,KeyError) as e:
        print(json.dumps({'status':'FAIL','error':str(e),'optimization':sys.flags.optimize},sort_keys=True))
        return 2

if __name__ == '__main__':
    sys.exit(main())
