#!/usr/bin/env python3
"""Independent exact audit of a corrected partial packet, not a global solver."""
import argparse
import ast
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, floor
import os
from pathlib import Path
from random import Random
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
MUTANT = None


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def solve(matrix, rhs):
    """Rational Gauss-Jordan elimination; None means singular."""
    a = [[F(x) for x in row] + [F(v)] for row, v in zip(matrix, rhs)]
    n = len(a)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for r in range(n):
            if r != col:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[col])]
    return [row[-1] for row in a]


def barycentric(triangle, point):
    return solve([[p[0] for p in triangle], [p[1] for p in triangle], [1, 1, 1]],
                 [point[0], point[1], 1])


def residual(a, b, p):
    # Canonical line equation, rather than the original orientation routine.
    if a[0] == b[0]:
        return F(p[0]) - a[0]
    slope = F(b[1] - a[1]) / (b[0] - a[0])
    return F(p[1]) - a[1] - slope * (p[0] - a[0])


def intersection(a, b, c, d):
    parameters = solve([[b[0]-a[0], c[0]-d[0]],
                        [b[1]-a[1], c[1]-d[1]]],
                       [c[0]-a[0], c[1]-a[1]])
    if parameters is None or not all(0 < t < 1 for t in parameters):
        return None
    t = parameters[0]
    return (F(a[0])+t*(b[0]-a[0]), F(a[1])+t*(b[1]-a[1]))


def geometric_metrics(points):
    n = len(points)
    need(n >= 3 and len(set(points)) == n, 'distinct points required')
    for triple in combinations(points, 3):
        need(barycentric(triple, (0, 0)) is not None, 'general position failed')
    e = [0] * ((n-2)//2+1)
    for i, j in combinations(range(n), 2):
        sides = [residual(points[i], points[j], points[k])
                 for k in range(n) if k not in (i, j)]
        need(all(sides), 'line contains third point')
        positive = sum(s > 0 for s in sides)
        e[min(positive, n-2-positive)] += 1
    segment_count = affine_count = 0
    locations = set()
    for a, b, c, d in combinations(points, 4):
        hits = [intersection(*pair) for pair in ((a,b,c,d),(a,c,b,d),(a,d,b,c))]
        actual = [p for p in hits if p is not None]
        need(len(actual) in (0, 1), 'multiple crossing pairs in a four-set')
        segment_count += len(actual)
        locations.update(actual)
        relation = barycentric((a, b, c), d) + [F(-1)]
        need(all(relation), 'zero affine-dependence coefficient')
        affine_count += sum(v > 0 for v in relation) == 2
    if MUTANT == 'count_locations':
        segment_count = len(locations)
    need(segment_count == affine_count, 'pair crossings disagree with affine dependence')
    hull = 0
    for i, p in enumerate(points):
        inside = any(all(v > 0 for v in barycentric(tri, p))
                     for tri in combinations(points[:i]+points[i+1:], 3))
        hull += not inside
    need(e[0] == hull, 'supporting pairs disagree with triangle-containment hull')
    return dict(n=n, crossings=segment_count, halving=e[-1], edges=e,
                hull=hull, distinct_intersection_locations=len(locations))


def profile_checks(z):
    n, c, e = z['n'], z['crossings'], z['edges']
    m = len(e)-1
    offset = 3 if MUTANT == 'wrong_weight' else 2
    w = [j*(n-offset-j) for j in range(m+1)]
    need(sum(e) == comb(n,2), 'edge partition')
    need(c+sum(x*y for x,y in zip(w,e)) == 3*comb(n,4), 'weighted identity')
    if m:
        E = [sum(e[:k+1]) for k in range(m)]
        a = [n-3-2*k for k in range(m)]
        need(all(v > 0 for v in a), 'positive coefficients')
        need(c == 3*comb(n,4)-w[m]*comb(n,2)+sum(x*y for x,y in zip(a,E)), 'cumulative identity')
        need(e[-1] == comb(n,2)-E[-1], 'halving complement')
        last = 1 if MUTANT == 'parity_blind_last' else (1 if n%2 == 0 else 2)
        need(a[-1] == last, 'last coefficient parity')
    if n <= 5:
        need((c,e[-1]) == (0,3) if n == 3 else c+(n-3)*e[-1] == 3*comb(n,4), 'small-order identity')
    if e[0] == 3 and n in (6,7):
        need(c+(1 if n==6 else 2)*e[-1] == (9 if n==6 else 33), 'triangular small-order identity')
    if e[0] == 3 and n == 8:
        need(c == -15+4*e[1]+e[2], 'triangular eight-point identity')
        term = 0 if MUTANT == 'omit_e1_parameter' else 3*e[1]
        need(e[-1] == 10-c+term, 'eight-point independent profile parameter')


OUTER = [(0,0),(1000,0),(0,1000)]
WITNESSES = {
    'P': (OUTER+[(578,36),(72,693),(201,510),(52,473),(56,41)], [3,6,13,6],22,6),
    'Q': (OUTER+[(171,780),(189,153),(17,28),(421,229),(171,510)], [3,7,9,9],22,9),
    'R': (OUTER+[(81,398),(957,30),(78,650),(288,498),(77,202)], [3,6,10,9],19,9)
}


def deletions(points, z):
    n = len(points)
    rows = []
    for i in range(n):
        sub = geometric_metrics(points[:i]+points[i+1:])
        profile_checks(sub)
        rows.append(sub)
    factor = n-3 if MUTANT == 'wrong_crossing_deletion' else n-4
    need(sum(r['crossings'] for r in rows) == factor*z['crossings'], 'crossing deletion coefficient')
    if n%2:
        r = (n-1)//2
        factor = r-1 if MUTANT == 'wrong_odd_deletion' else r
        expected = factor*z['halving']
    else:
        extra = 0 if MUTANT == 'omit_adjacent_even' else n//2*z['edges'][n//2-2]
        expected = (n-2)*z['halving']+extra
    need(sum(r['halving'] for r in rows) == expected, 'parity-specific halving deletion')
    return rows


def sign_signature(points):
    # Canonical residual changes sign exactly for the triple at the mutation;
    # the first two points never exchange x order in these fixtures.
    return {(i,j,k): residual(points[i],points[j],points[k]) > 0
            for i,j,k in combinations(range(len(points)),3)}


def mutation_checks():
    rng = Random(802671033)
    receipts = []
    for n in range(3,13):
        for k in range(n-2):
            for attempt in range(100):
                rest = [(rng.randrange(-251,252), (1 if i<k else -1)*rng.randrange(31,311))
                        for i in range(n-3)]
                a = [(0,F(1,10**8)),(-7,0),(11,0)]+rest
                b = [(0,F(-1,10**8)),(-7,0),(11,0)]+rest
                try:
                    za, zb = geometric_metrics(a), geometric_metrics(b)
                except RuntimeError as exc:
                    if str(exc) in ('distinct points required','general position failed','line contains third point'):
                        continue
                    raise
                sa, sb = sign_signature(a), sign_signature(b)
                if [t for t in sa if sa[t] != sb[t]] == [(0,1,2)]:
                    break
            else:
                raise RuntimeError('independent mutation fixture exhaustion')
            profile_checks(za); profile_checks(zb)
            dc = zb['crossings']-za['crossings']
            formula = n-3-2*k if MUTANT == 'reverse_mutation_sign' else 2*k-n+3
            need(dc == formula, 'mutation crossing sign')
            delta = [v-u for u,v in zip(za['edges'],zb['edges'])]
            expected = [0]*len(delta)
            if 2*k < n-3:
                expected[k], expected[k+1] = -1,1
            elif 2*k > n-3:
                mirror = n-3-k
                expected[mirror], expected[mirror+1] = 1,-1
            if MUTANT == 'reverse_profile_transfer':
                expected = [-v for v in expected]
            need(delta == expected, 'entire mutation profile transfer')
            if dc < 0:
                need(zb['halving'] >= za['halving'], 'mutation halving monotonicity')
            if dc == 0:
                need(n%2 == 1 and delta == [0]*len(delta), 'zero-cost mutation invariance')
            receipts.append(dict(n=n,k=k,delta_crossings=dc,delta_edges=delta))
    return receipts


def rounding_checks():
    p = [(0,0),(6,0),(0,6),(1,1)]
    z = geometric_metrics(p)
    need(z['crossings'] == 0 and z['edges'][0] == 3, 'rounding counterexample geometry')
    lower, U, A, coefficient = F(5,2),0,-3,1
    slack = F(z['edges'][0])-lower
    budget = F(U-A)-lower
    old_right = floor(budget/coefficient)
    corrected_right = floor(lower+budget/coefficient)-lower
    need(slack > old_right, 'known original floor defect not reproduced')
    need(slack <= corrected_right, 'general corrected floor bound')
    if MUTANT == 'unqualified_floor_slack':
        need(slack <= old_right, 'unqualified floor-slack inequality is false')
    # Bounded algebraic regression, including nonintegral valid lower bounds.
    cases = 0
    for n in range(4,31):
        m = (n-2)//2
        weights = [n-3-2*k for k in range(m)]
        last = weights[-1]
        for shift in (F(0),F(1,2),F(2,3)):
            E = [3+k*(k+1) for k in range(m)]
            L = [F(v)-shift for v in E]
            total_slack = sum(a*(x-y) for a,x,y in zip(weights,E,L))
            need(E[-1]-L[-1] <= floor(L[-1]+total_slack/last)-L[-1], 'general rounding regression')
            if L[-1].denominator == 1:
                need(E[-1]-L[-1] <= floor(total_slack/last), 'integral rounding regression')
            cases += 1
    return dict(counterexample=dict(n=4,E0=3,L0='5/2',U=0,slack='1/2',old_rhs=0,corrected_rhs='1/2'), algebra_cases=cases)


def mathematics():
    concurrence = [(-2,0),(-1,-2),(1,-2),(2,0),(1,2),(-1,2)]
    concurrent = geometric_metrics(concurrence)
    need(concurrent['crossings'] == 15 and concurrent['distinct_intersection_locations'] < 15, 'crossing multiplicity fixture')
    records, deletion_records = {}, {}
    for name, (p,e,c,h) in WITNESSES.items():
        z = geometric_metrics(p)
        profile_checks(z)
        need((z['edges'],z['crossings'],z['halving']) == (e,c,h), 'authored witness '+name)
        need(all(all(v>0 for v in barycentric(OUTER,point)) for point in p[3:]), 'outer triangle containment')
        records[name] = z
        deletion_records[name] = deletions(p,z)
    need(records['P']['crossings'] == records['Q']['crossings'] > records['R']['crossings'], 'nonoptimal witness certificate')
    need(records['P']['halving'] < records['Q']['halving'], 'equal crossing unequal halving')
    rng = Random(518902)
    fixtures = []
    for n in range(3,11):
        for sample in range(3):
            for attempt in range(100):
                p = [(rng.randrange(-131,132),rng.randrange(-131,132)) for _ in range(n)]
                try:
                    z = geometric_metrics(p)
                    break
                except RuntimeError as exc:
                    if str(exc) not in ('distinct points required','general position failed','line contains third point'):
                        raise
            else:
                raise RuntimeError('independent fixture exhaustion')
            profile_checks(z)
            if n>=4:
                deletions(p,z)
            fixtures.append(z)
    return dict(witnesses=records,witness_deletions=deletion_records,concurrence=concurrent,
                auxiliary_fixtures=fixtures,mutations=mutation_checks(),rounding=rounding_checks())


MUTANTS = ['count_locations','wrong_weight','parity_blind_last','omit_e1_parameter',
           'wrong_crossing_deletion','wrong_odd_deletion','omit_adjacent_even',
           'reverse_mutation_sign','reverse_profile_transfer','unqualified_floor_slack']


def verify_manifest(directory, filename):
    rows = json.loads((directory/filename).read_text())['files']
    need(len({r['path'] for r in rows}) == len(rows), 'duplicate pin')
    for r in rows:
        p = directory/r['path']
        need(p.parent == directory and p.is_file() and not p.is_symlink(), 'invalid pin path')
        raw = p.read_bytes()
        need(len(raw) == r['bytes'] and sha256(raw).hexdigest() == r['sha256'], 'pin mismatch '+r['path'])
    need({p.name for p in directory.iterdir()} == {r['path'] for r in rows}|{filename}, 'unexpected pinned directory entry')
    return len(rows)


def readonly(directory):
    need(os.geteuid() == 1000, 'read-only audit requires UID 1000')
    need(not os.access(directory,os.W_OK), 'directory writable')
    probe = directory/('.independent_write_probe_'+str(os.getpid()))
    try:
        fd = os.open(probe,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except PermissionError:
        pass
    else:
        os.close(fd);probe.unlink();raise RuntimeError('directory create succeeded')
    denied = []
    for p in sorted(directory.iterdir()):
        need(p.is_file() and not p.is_symlink() and not os.access(p,os.W_OK), 'file writable or unexpected')
        try:
            fd = os.open(p,os.O_WRONLY)
        except PermissionError:
            denied.append(p.name)
        else:
            os.close(fd);raise RuntimeError('write-open succeeded')
    return dict(directory_create_denied=True,existing_file_write_open_denials=denied)


def main():
    global MUTANT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,default=BASE.parent/'current')
    parser.add_argument('--require-readonly',action='store_true')
    parser.add_argument('--mutant',choices=MUTANTS)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    MUTANT = args.mutant
    packet = args.packet.resolve()
    output = args.output.resolve() if args.output else None
    if output:
        need(not output.exists(), 'output already exists')
        need(all(output!=d and d not in output.parents for d in (BASE,packet)), 'output must be external')
    own_pins = verify_manifest(BASE,'AUDIT_PINS.json')
    current_pins = verify_manifest(packet,'PAYLOAD_PINS.json')
    need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(Path(__file__).read_text()))), 'assert node present')
    report = (packet/'REPORT.md').read_text()
    need('L_{m−1} is an integer' in report and '(4R)' in report and '1/2≤0' in report, 'rounding correction missing')
    status = json.loads((packet/'STATUS.json').read_text())
    need(status['full_target_resolved'] is False and status['outcome']=='exhausted' and status['substantive_proof_search_approaches']==5, 'status overclaim')
    ro = {name:readonly(d) for name,d in (('audit',BASE),('current',packet))} if args.require_readonly else None
    result = dict(status='passed',uid=os.geteuid(),optimization=sys.flags.optimize,
                  audit_pins=own_pins,current_pins=current_pins,readonly=ro,
                  original_defect_explicitly_reproduced=True,mathematics=mathematics(),
                  limits='Independent bounded exact regression; proofs and source quantifiers are reviewed in AUDIT.md. No global optimizer enumeration.')
    data = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if output:
        with output.open('x') as f:
            f.write(data)
    else:
        sys.stdout.write(data)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        sys.stderr.write(type(exc).__name__+': '+str(exc)+'\n')
        sys.exit(1)
