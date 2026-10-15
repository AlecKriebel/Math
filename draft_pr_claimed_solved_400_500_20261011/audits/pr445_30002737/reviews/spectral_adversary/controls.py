#!/usr/bin/env python3
"""Independent exact finite controls. No imports from frozen author/audit scripts.

RS inputs are deterministic substitution/recursion values. Essential guards use
exceptions, so python -O does not disable verification. All writes stay next to
this script. Infinite claims are established in REPORT.md, not by finite tests.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
CASE = ROOT.parent.parent
SNAP = CASE / 'source_snapshot'
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
SLOTS = {'0': (0, 0), 'e': (3, 3), 'a': (10, 0), 'b': (0, 10)}
MEANS = {'0': F(1), 'e': F(1), 'a': F(1, 2), 'b': F(1, 2)}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def frozen_integrity():
    receipt = json.loads((CASE / 'SOURCE_RECEIPT.json').read_text())
    require(receipt['head_sha'] == HEAD, 'Wrong frozen head')
    rows = []
    for item in receipt['files']:
        data = (SNAP / item['path']).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        require(len(data) == item['bytes'], 'Frozen byte count mismatch: ' + item['path'])
        require(digest == item['sha256'], 'Frozen hash mismatch: ' + item['path'])
        rows.append({'path': item['path'], 'bytes': len(data), 'sha256': digest})
    return rows


@lru_cache(None)
def rs(n):
    # Primary Baake-Grimm two-sided recursion, not random signs.
    if n == 0:
        return 1
    if n == -1:
        return -1
    q, r = divmod(n, 4)
    return rs(q) if r < 2 else (-1 if (q + r) % 2 else 1) * rs(q)


def rs_controls():
    rho = {'a': 'ab', 'b': 'ac', 'c': 'db', 'd': 'dc'}
    rho2 = {a: ''.join(rho[b] for b in rho[a]) for a in rho}
    code = lambda a: 1 if a in 'ab' else -1
    left, right = 'c', 'a'
    for _ in range(7):
        left = ''.join(rho2[a] for a in left)
        right = ''.join(rho2[a] for a in right)
    for i, a in enumerate(left, -len(left)):
        require(code(a) == rs(i), 'Bilateral negative substitution mismatch')
    for i, a in enumerate(right):
        require(code(a) == rs(i), 'Bilateral positive substitution mismatch')
        require(code(a) == (-1 if (i & (i >> 1)).bit_count() % 2 else 1), 'Bit formula mismatch')
    diagnostics = []
    for length in (1024, 4096, 16384):
        values = [rs(i) for i in range(-length // 2, length // 2 + 65)]
        diagnostics.append({'length': length,
                            'mean': sum(values[:length]) / length,
                            'max_abs_nonzero_lag_correlation': max(abs(sum(values[i] * values[i+m] for i in range(length))) / length for m in range(1, 65))})
    return {'bilateral_sites_checked': len(left) + len(right), 'positive_bit_formula_sites': len(right), 'finite_diagnostics': diagnostics}


def occupancy(kind, i, j, ox, oy):
    if kind == 'a':
        return (1 + rs(i + ox)) // 2
    if kind == 'b':
        return (1 + rs(j + oy)) // 2
    return 1


def make_points(bounds, phase, ox, oy):
    xmin, xmax, ymin, ymax = bounds
    px, py = phase
    points = set()
    ranges = {}
    # Bounds and coordinates are in units of 1/30; half-open physical windows.
    for c, (cx, cy) in SLOTS.items():
        irange = tuple(i for i in range((xmin + px - cx) // 30 - 2, (xmax + px - cx) // 30 + 3) if xmin <= 30*i + cx - px < xmax)
        jrange = tuple(j for j in range((ymin + py - cy) // 30 - 2, (ymax + py - cy) // 30 + 3) if ymin <= 30*j + cy - py < ymax)
        ranges[c] = (irange, jrange)
        for i in irange:
            for j in jrange:
                if occupancy(c, i, j, ox, oy):
                    p = (30*i + cx - px, 30*j + cy - py)
                    require(p not in points, 'Coincident physical slots')
                    points.add(p)
    return points, ranges


def axis_occ(kind, i, axis, ox, oy):
    if kind == 'a' and axis == 0:
        return (1 + rs(i + ox)) // 2
    if kind == 'b' and axis == 1:
        return (1 + rs(i + oy)) // 2
    return 1


def exact_pairs(displacement, ranges, ox, oy):
    dx, dy = displacement
    total = 0
    for c, (cx, cy) in SLOTS.items():
        for d, (dxslot, dyslot) in SLOTS.items():
            mx, ny = dx - cx + dxslot, dy - cy + dyslot
            if mx % 30 or ny % 30:
                continue
            m, n = mx // 30, ny // 30
            ic, jc = ranges[c]
            idom, jdom = map(set, ranges[d])
            sx = sum(axis_occ(c, i, 0, ox, oy) * axis_occ(d, i-m, 0, ox, oy) for i in ic if i-m in idom)
            sy = sum(axis_occ(c, j, 1, ox, oy) * axis_occ(d, j-n, 1, ox, oy) for j in jc if j-n in jdom)
            total += sx * sy
    return total


def asymptotic_pairs(displacement):
    dx, dy = displacement
    total = F(0)
    for c, (cx, cy) in SLOTS.items():
        for d, (dxslot, dyslot) in SLOTS.items():
            mx, ny = dx - cx + dxslot, dy - cy + dyslot
            if mx % 30 or ny % 30:
                continue
            m, n = mx // 30, ny // 30
            total += MEANS[c] * MEANS[d]
            if c == d == 'a' and m == 0:
                total += F(1, 4)
            if c == d == 'b' and n == 0:
                total += F(1, 4)
    return total


def physical_controls():
    residues = defaultdict(list)
    for c, cp in SLOTS.items():
        for d, dp in SLOTS.items():
            residues[((cp[0]-dp[0]) % 30, (cp[1]-dp[1]) % 30)].append(c + '-' + d)
    require(len(residues) == 13, 'Unexpected residue collisions')
    require(residues[(0, 0)] == ['0-0', 'e-e', 'a-a', 'b-b'], 'Wrong zero-residue degeneracy')
    require(residues[(3, 3)] == ['e-0'], 'Marker orientation not unique')
    displacements = sorted({(30*m + cp[0]-dp[0], 30*n + cp[1]-dp[1])
                            for m in range(-2, 3) for n in range(-2, 3)
                            for cp in SLOTS.values() for dp in SLOTS.values()})
    records = []
    samples = [((-240, 240, -240, 240), (0, 0), 0, 0),
               ((-451, 449, -601, 599), (7, -11), -113, 97),
               ((-960, 960, -960, 960), (29, 0), 31, 31),
               ((-1920, 1920, -1920, 1920), (-31, 47), 0, 0)]
    for bounds, phase, ox, oy in samples:
        points, ranges = make_points(bounds, phase, ox, oy)
        max_error = F(0)
        area = F((bounds[1]-bounds[0]) * (bounds[3]-bounds[2]), 900)
        for z in displacements:
            direct = sum((p[0]-z[0], p[1]-z[1]) in points for p in points)
            expected = exact_pairs(z, ranges, ox, oy)
            require(direct == expected, f'Physical pair mismatch at {z}: {direct} != {expected}')
            max_error = max(max_error, abs(F(direct) / area - asymptotic_pairs(z)))
        # The same x/y offset specifically guards against assuming x and y are
        # independently chosen deterministic sequences.
        records.append({'bounds_units_1_over_30': bounds, 'phase_units_1_over_30': phase,
                        'rs_offsets': [ox, oy], 'points': len(points),
                        'displacements_checked': len(displacements),
                        'density': float(F(len(points)) / area),
                        'max_finite_asymptotic_error': float(max_error)})
    # Negative control: omitting variable-slot diagonal corrections is false.
    erroneous_origin = sum(v*v for v in MEANS.values())
    require(erroneous_origin == F(5, 2), 'Wrong negative-control setup')
    require(asymptotic_pairs((0, 0)) == 3 and erroneous_origin != 3,
            'Missing self-correlation negative control was not rejected')
    return {'residue_classes': [{'residue_units_1_over_30': list(k), 'ordered_slot_pairs': v} for k, v in sorted(residues.items())],
            'samples': records, 'pair_comparisons': len(displacements)*len(samples),
            'central_autocorrelation': 3, 'central_bragg_intensity': 9,
            'missing_self_correction_negative_control_rejected': True}


def component_1d(component, kind, index, axis, ox, oy):
    if component == 'P':
        return MEANS[kind] if axis == 0 else F(1)
    if component == 'A':
        if kind != 'a':
            return F(0)
        return F(rs(index + ox), 2) if axis == 0 else F(1)
    if component == 'B':
        if kind != 'b':
            return F(0)
        return F(1, 2) if axis == 0 else F(rs(index + oy))
    raise RuntimeError('Unknown component')


def cross_controls():
    # Direct signed-component cross convolutions versus separated finite sums.
    bounds, phase, ox, oy = (-481, 479, -541, 539), (11, -7), 13, -19
    _, ranges = make_points(bounds, phase, ox, oy)
    combs = {}
    for comp in ('P', 'A', 'B'):
        comb = {}
        for kind, (cx, cy) in SLOTS.items():
            ii, jj = ranges[kind]
            for i in ii:
                for j in jj:
                    w = component_1d(comp, kind, i, 0, ox, oy) * component_1d(comp, kind, j, 1, ox, oy)
                    if w:
                        comb[(30*i + cx-phase[0], 30*j + cy-phase[1])] = w
        combs[comp] = comb
    displacements = sorted({(30*m+cp[0]-dp[0], 30*n+cp[1]-dp[1]) for m in range(-1, 2) for n in range(-1, 2) for cp in SLOTS.values() for dp in SLOTS.values()})
    checks = 0
    maxima = {}
    area = F((bounds[1]-bounds[0])*(bounds[3]-bounds[2]), 900)
    for first in combs:
        for second in combs:
            max_abs = F(0)
            for z in displacements:
                direct = sum(w * combs[second].get((p[0]-z[0], p[1]-z[1]), F(0)) for p, w in combs[first].items())
                factored = F(0)
                for c, cp in SLOTS.items():
                    for d, dp in SLOTS.items():
                        mx, ny = z[0]-cp[0]+dp[0], z[1]-cp[1]+dp[1]
                        if mx % 30 or ny % 30:
                            continue
                        m, n = mx // 30, ny // 30
                        ii, jj = ranges[c]
                        idom, jdom = map(set, ranges[d])
                        sx = sum(component_1d(first,c,i,0,ox,oy)*component_1d(second,d,i-m,0,ox,oy) for i in ii if i-m in idom)
                        sy = sum(component_1d(first,c,j,1,ox,oy)*component_1d(second,d,j-n,1,ox,oy) for j in jj if j-n in jdom)
                        factored += sx*sy
                require(direct == factored, 'Component cross-correlation mismatch')
                max_abs = max(max_abs, abs(direct/area))
                checks += 1
            maxima[first+'-'+second] = float(max_abs)
    require(maxima['P-A'] > 0 and maxima['A-B'] > 0,
            'Control accidentally suppresses finite imbalance terms')
    return {'comparisons': checks, 'finite_normalized_maxima': maxima,
            'finite_cross_terms_retained': True}


def weighted_controls():
    checks = 0
    maxima = []
    for length, offsetx, offsety in ((16,0,0), (37,11,-17), (128,0,0)):
        ii = tuple(range(-length//2, -length//2 + length))
        jj = tuple(range(5, 5 + length + 7))
        iset, jset = set(ii), set(jj)
        weights = {(i,j):4+rs(i+offsetx)+2*rs(j+offsety) for i in ii for j in jj}
        require(set(weights.values()).issubset({1,3,5,7}), 'Positive weighted comb is wrong')
        max_error = F(0)
        for m in range(-4, 5):
            for n in range(-4, 5):
                ix, jy = tuple(i for i in ii if i-m in iset), tuple(j for j in jj if j-n in jset)
                lx, ly = len(ix), len(jy)
                x0, x1 = sum(rs(i+offsetx) for i in ix), sum(rs(i-m+offsetx) for i in ix)
                y0, y1 = sum(rs(j+offsety) for j in jy), sum(rs(j-n+offsety) for j in jy)
                xx = sum(rs(i+offsetx)*rs(i-m+offsetx) for i in ix)
                yy = sum(rs(j+offsety)*rs(j-n+offsety) for j in jy)
                expanded = 16*lx*ly + 4*(x0+x1)*ly + 8*(y0+y1)*lx + xx*ly + 4*yy*lx + 2*(x0*y1+x1*y0)
                direct = sum(w * weights.get((i-m,j-n),0) for (i,j),w in weights.items())
                require(direct == expanded, 'Weighted exact finite expansion mismatch')
                max_error = max(max_error, abs(F(direct,len(ii)*len(jj))-(16+(m==0)+4*(n==0))))
                checks += 1
        maxima.append({'horizontal_length':len(ii),'vertical_length':len(jj),'rs_offsets':[offsetx,offsety],'max_finite_asymptotic_error':float(max_error)})
    return {'comparisons':checks,'samples':maxima,'limiting_origin_coefficient':21,'limiting_density':4,'central_bragg_intensity':16}


def floor_fraction(value):
    return value.numerator // value.denominator


def exact_suspension(t):
    cuts = {F(0), F(1)}
    for n in range(floor_fraction(t)-2, floor_fraction(t)+4):
        if 0 < F(n)-t < 1:
            cuts.add(F(n)-t)
    cuts = sorted(cuts)
    return sum((hi-lo) for lo, hi in zip(cuts,cuts[1:]) if floor_fraction((lo+hi)/2+t) == 0)


def spectral_controls():
    times = sorted({F(p,q) for q in (1,2,3,5,7,17) for p in range(-5*q,5*q+1)})
    for t in times:
        require(exact_suspension(t) == max(F(0),F(1)-abs(t)), 'Suspension overlap failure')
    product_checks = 0
    for t1 in times[::13]:
        for t2 in times[::17]:
            exact = exact_suspension(t1)*exact_suspension(t2)
            expected = max(F(0),F(1)-abs(t1))*max(F(0),F(1)-abs(t2))
            require(exact == expected, 'Product suspension overlap failure')
            product_checks += 1
    require(exact_suspension(F(1)) != 1, 'Naive seam negative control not rejected')
    def sinc2(k):
        return 1.0 if k == 0 else (math.sin(math.pi*k)/(math.pi*k))**2
    transform_records = []
    # Composite Simpson quadrature on the smooth half-triangle, using symmetry.
    steps = 16384
    for k in (-17.25,-3,-1.125,-0.5,0,0.5,1,2.25,19.75):
        g = lambda t: 2*(1-t)*math.cos(2*math.pi*k*t)
        numeric = (g(0)+g(1)+4*sum(g(j/steps) for j in range(1,steps,2))+2*sum(g(j/steps) for j in range(2,steps,2)))/(3*steps)
        error = abs(numeric-sinc2(k))
        require(error < 1e-10, 'Triangle Fourier normalization failure')
        transform_records.append({'frequency':k,'quadrature':numeric,'sinc_squared':sinc2(k),'absolute_error':error})
    # This is a diagnostic check of an analytically proved Plancherel identity.
    masses=[]
    for radius in (1,4,16):
        steps = 16384*radius
        step = radius/steps
        mass = 2*step*(sinc2(0)+sinc2(radius)+4*sum(sinc2(j*step) for j in range(1,steps,2))+2*sum(sinc2(j*step) for j in range(2,steps,2)))/3
        bound = 2/(math.pi**2*radius)
        require(1-bound-1e-9 <= mass <= 1+1e-9, 'Sinc mass/tail bound failed')
        masses.append({'radius':radius,'truncated_mass':mass,'analytic_upper_tail_bound':bound})
    return {'rational_times_checked':len(times),'product_times_checked':product_checks,
            'integer_endpoints': {str(i): str(exact_suspension(F(i))) for i in range(-3,4)},
            'naive_seam_negative_control_rejected':True,'fourier_checks':transform_records,'mass_diagnostics':masses}


def main():
    before = frozen_integrity()
    result = {'frozen_head':HEAD,'method':'independent deterministic exact finite controls; no IID model',
              'rs':rs_controls(),'physical':physical_controls(),'cross':cross_controls(),
              'weighted':weighted_controls(),'spectral':spectral_controls()}
    after = frozen_integrity()
    require(before == after, 'Frozen source changed during controls')
    result['source_integrity_files'] = before
    result['status'] = 'PASS'
    (ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'physical_pairs':result['physical']['pair_comparisons'],
                      'cross_pairs':result['cross']['comparisons'],'weighted_pairs':result['weighted']['comparisons'],
                      'suspension_times':result['spectral']['rational_times_checked'],
                      'frozen_files_unchanged':len(before)},sort_keys=True))

if __name__ == '__main__':
    main()
