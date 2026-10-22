"""Independent real billiard construction and exact low-period checks.

All required checks use explicit exceptions and remain active under python -O.
No external files are written except the requested JSON output argument.
"""
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
RUNTIME = Path(__file__).resolve().parents[2] / 'pr200_5100007/math_algebra_family_01/runtime_packages'
sys.path.insert(0, str(RUNTIME))
import sympy as sp
import mpmath as mp


def require(ok, text):
    if not ok:
        raise RuntimeError(text)


def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]


def areas(vertices, clipped=False):
    n = len(vertices)
    A = sum(cross(vertices[i], vertices[(i+1) % n]) for i in range(n))/2
    feet = []
    for i in range(n):
        p, q = vertices[i], vertices[(i+1) % n]
        v = (q[0]-p[0], q[1]-p[1])
        s = -dot(p, v)/dot(v, v)
        if clipped:
            s = max(0, min(1, s))
        feet.append((p[0]+s*v[0], p[1]+s*v[1]))
    B = sum(cross(feet[i], feet[(i+1) % n]) for i in range(n))/2
    return A, B, A*B


def verify_exact_orbit(vertices, outer_x2, outer_y2, lam):
    n = len(vertices)
    for i, p in enumerate(vertices):
        q = vertices[(i+1) % n]
        prev = vertices[(i-1) % n]
        require(sp.simplify(p[0]**2/outer_x2+p[1]**2/outer_y2-1) == 0, 'exact vertex off outer ellipse')
        direction = (q[0]-p[0], q[1]-p[1])
        normal = (-direction[1], direction[0])
        support = dot(normal, p)
        require(sp.simplify(support**2-(outer_x2-lam)*normal[0]**2-(outer_y2-lam)*normal[1]**2) == 0, 'exact side not tangent')
        incoming = (p[0]-prev[0], p[1]-prev[1])
        incoming_len = sp.sqrt(dot(incoming, incoming))
        outgoing_len = sp.sqrt(dot(direction, direction))
        enormal = (p[0]/outer_x2, p[1]/outer_y2)
        coefficient = 2*dot(incoming, enormal)/(incoming_len*dot(enormal, enormal))
        for j in range(2):
            residue = direction[j]/outgoing_len-incoming[j]/incoming_len+coefficient*enormal[j]
            require(sp.simplify(residue) == 0, 'exact physical reflection failed')
    for i in range(n):
        for j in range(i+1, n):
            require(sp.simplify(dot((vertices[i][0]-vertices[j][0], vertices[i][1]-vertices[j][1]), (vertices[i][0]-vertices[j][0], vertices[i][1]-vertices[j][1]))) != 0, 'exact list has repeated vertex')


def exact_checks():
    rt2, rt5, rt13 = sp.sqrt(2), sp.sqrt(5), sp.sqrt(13)
    n3 = [
        [(2*rt2, 0), (-4*rt2/3, 5*sp.S.One/3), (-4*rt2/3, -5*sp.S.One/3)],
        [(0, -rt5), (8*sp.S.One/3, rt5/3), (-8*sp.S.One/3, rt5/3)],
    ]
    lam3 = 40*sp.S.One/9
    c3 = 7*lam3**3/40  # sqrt(8^2-8*5+5^2)=7
    n4 = [
        [(2*rt2, 0), (0, rt5), (-2*rt2, 0), (0, -rt5)],
        [(8/rt13, 5/rt13), (-8/rt13, 5/rt13), (-8/rt13, -5/rt13), (8/rt13, -5/rt13)],
    ]
    lam4 = 40*sp.S.One/13
    records = []
    for N, families, lam, target in [(3, n3, lam3, c3), (4, n4, lam4, 8*lam4**2)]:
        for phase, v in enumerate(families):
            A, B, product = map(sp.simplify, areas(v))
            require(sp.simplify(product-target) == 0, 'exact low-period product failed')
            verify_exact_orbit(v, sp.S(8), sp.S(5), lam)
            ar, br, pr = map(sp.simplify, areas(list(reversed(v))))
            require(sp.simplify(ar+A) == 0 and sp.simplify(br+B) == 0 and sp.simplify(pr-product) == 0, 'exact reversal failed')
            records.append({'N': N, 'phase': phase, 'A': str(A), 'B': str(B), 'product': str(product), 'target': str(target)})
    # The algebraic triangular closure condition has exactly r+s=1 in the proper domain.
    r, s = sp.symbols('r s', positive=True)
    require(sp.expand((1-2*r*r-2*s*s)+(r*r-s*s)**2 + ((r+s)**2-1)*(1-(r-s)**2)) == 0, 'triangle factorization failed')
    # Reject a real false identity through the same nonremovable guard.
    rejected = False
    try:
        require(sp.simplify(1-sp.Rational(1000000001, 1000000000)) == 0, 'intentional false identity')
    except RuntimeError:
        rejected = True
    require(rejected, 'false identity accepted')
    # Independent exact expansion of the classical signed pedal-area identity.
    x, u, v, h, j = sp.symbols('x u v h j', nonzero=True, real=True)
    shifted = [(-h, -j), (x-h, -j), (u-h, v-j)]
    triangle_A, pedal_B, _ = areas(shifted)
    center_y = (u*u+v*v-x*u)/(2*v)
    R2 = x*x/4+center_y*center_y
    power = (h-x/2)**2+(j-center_y)**2-R2
    require(sp.factor(sp.together(pedal_B+triangle_A*power/(4*R2))) == 0, 'classical pedal identity expansion failed')
    sixes = [
        [(sp.S(2), 0), (sp.Rational(4, 3), rt5/3), (-sp.Rational(4, 3), rt5/3), (-sp.S(2), 0), (-sp.Rational(4, 3), -rt5/3), (sp.Rational(4, 3), -rt5/3)],
        [(0, sp.S(1)), (-4*rt2/3, sp.Rational(1, 3)), (-4*rt2/3, -sp.Rational(1, 3)), (0, -sp.S(1)), (4*rt2/3, -sp.Rational(1, 3)), (4*rt2/3, sp.Rational(1, 3))],
    ]
    six_products, repeat_products = [], []
    for v in sixes:
        verify_exact_orbit(v, sp.S(4), sp.S(1), sp.Rational(4, 9))
        six_products.append(sp.simplify(areas(v)[2]))
        repeat_products.append(sp.simplify(areas(v+v)[2]))
        require(sp.simplify(repeat_products[-1]-4*six_products[-1]) == 0, 'repeat scaling failed')
    require(sp.simplify(six_products[1]-six_products[0]) != 0, 'exact least6 countercontrol failed')
    return {'low_periods': records, 'false_identity_rejected': rejected,
            'exact_least6_products': [str(p) for p in six_products],
            'exact_repeated_list_N12_products': [str(p) for p in repeat_products],
            'exact_repeated_list_counterexample_difference': str(sp.simplify(repeat_products[1]-repeat_products[0])),
            'exact_reflection_and_distinct_vertex_checks': True,
            'symbolic_classical_pedal_area_identity_checked': True}


mp.mp.dps = 75
A2 = mp.mpf(8)
B2 = mp.mpf(5)
a = mp.sqrt(A2)
b = mp.sqrt(B2)


def next_t(t, lam):
    ct, st = mp.cos(t), mp.sin(t)
    D = ct*ct/A2+st*st/B2
    H = (1/B2-1/A2)*st*ct
    disc = mp.sqrt(lam*(D-lam/(A2*B2)))
    v = lam*D/(disc-lam*H)
    return t+2*mp.atan(v)


def closure(lam, N, w):
    t = mp.mpf(0)
    for _ in range(N):
        t = next_t(t, lam)
    return t-2*mp.pi*w


def parameter(N, w):
    require(math.gcd(N, w) == 1 and 0 < 2*w < N, 'nonprimitive star request')
    lo, hi = mp.mpf('1e-70'), B2*(1-mp.mpf('1e-65'))
    require(closure(lo, N, w) < 0 and closure(hi, N, w) > 0, 'closure bracket failed')
    for _ in range(260):
        mid = (lo+hi)/2
        if closure(mid, N, w) < 0:
            lo = mid
        else:
            hi = mid
    lam = (lo+hi)/2
    require(abs(closure(lam, N, w)) < mp.mpf('1e-60'), 'least-period closure solve failed')
    return lam


def orbit(t, lam, N, w):
    ts = []
    t0 = t
    for _ in range(N):
        ts.append(t)
        t = next_t(t, lam)
    require(abs(t-t0-2*mp.pi*w) < mp.mpf('1e-57'), 'phase closure failed')
    for j in range(1, N):
        require(abs(mp.sin((ts[j]-ts[0])/2)) > mp.mpf('1e-40'), 'smaller physical period encountered')
    vertices = [(a*mp.cos(x), b*mp.sin(x)) for x in ts]
    for i, p in enumerate(vertices):
        q, prev = vertices[(i+1) % N], vertices[(i-1) % N]
        incoming = (p[0]-prev[0], p[1]-prev[1])
        outgoing = (q[0]-p[0], q[1]-p[1])
        il, ol = mp.sqrt(dot(incoming, incoming)), mp.sqrt(dot(outgoing, outgoing))
        normal = (p[0]/A2, p[1]/B2)
        coefficient = 2*dot(incoming, normal)/(il*dot(normal, normal))
        residues = [outgoing[j]/ol-incoming[j]/il+coefficient*normal[j] for j in range(2)]
        require(sum(abs(x) for x in residues) < mp.mpf('1e-55'), 'numerical physical reflection failed')
    return ts, vertices


def diagnostic(N, w):
    lam = parameter(N, w)
    values, clips, min_B = [], [], mp.inf
    scalar_errors = []
    for phase in ['0', '0.137', '0.619', '1.123', '2.017']:
        ts, v = orbit(mp.mpf(phase), lam, N, w)
        A, B, product = areas(v)
        min_B = min(min_B, B)
        ar, br, pr = areas(list(reversed(v)))
        require(abs(ar+A)+abs(br+B)+abs(pr-product) < mp.mpf('1e-60'), 'numerical reversal failed')
        ds = [(ts[i+1]-ts[i])/2 if i+1 < N else (ts[0]+2*mp.pi*w-ts[i])/2 for i in range(N)]
        us = [mp.cot(d) for d in ds]
        As = a*b*sum(u/(1+u*u) for u in us)
        Bs = lam**2/(2*a*b)*sum(us[i]*us[(i+1) % N]*(us[i]+us[(i+1) % N]) for i in range(N))
        err = abs(A-As)+abs(B-Bs)
        require(err < mp.mpf('1e-56'), 'independent scalar reduction failed')
        scalar_errors.append(err)
        values.append(product)
        clips.append(areas(v, clipped=True)[2])
    spread = max(values)-min(values)
    eligible = N % 2 == 1 or N % 4 == 0
    if eligible:
        require(spread < mp.mpf('1e-54'), 'target product diagnostic failed')
    return {
        'N': N, 'winding': w, 'eligible': eligible,
        'lambda': mp.nstr(lam, 45), 'product_phase0': mp.nstr(values[0], 45),
        'phase_spread': mp.nstr(spread, 8), 'scalar_reduction_error': mp.nstr(max(scalar_errors), 8),
        'minimum_positive_B': mp.nstr(min_B, 12),
        'clipped_product_phase_spread': mp.nstr(max(clips)-min(clips), 12),
        'clipped_disagreement': mp.nstr(max(abs(x-y) for x, y in zip(values, clips)), 12),
        'repeat_twice_product_spread': mp.nstr(4*spread, 12) if N == 6 else None,
    }


def nonconfocal_control():
    products = []
    for phase in [mp.mpf('0'), mp.mpf('.137'), mp.mpf('.619'), mp.mpf('1.123')]:
        vertices = [(a*mp.cos(phase+2*mp.pi*i/3), b*mp.sin(phase+2*mp.pi*i/3)) for i in range(3)]
        products.append(areas(vertices)[2])
    spread = max(products)-min(products)
    require(spread > mp.mpf('1e-5'), 'nonconfocal countercontrol failed')
    return {'family': 'affine regular triangles; caustic semiaxes a/2,b/2, nonconfocal', 'product_spread': mp.nstr(spread, 30)}


out = {'exact': exact_checks(), 'diagnostic_precision_decimal_digits': mp.mp.dps,
       'diagnostic_not_interval_certificate': True,
       'families': [diagnostic(N, w) for N, w in [(3, 1), (4, 1), (5, 1), (5, 2), (7, 2), (8, 1), (8, 3), (9, 4), (12, 5), (20, 1), (6, 1)]],
       'nonconfocal_control': nonconfocal_control(),
       'optimized_mode': not __debug__}
payload = json.dumps(out, indent=2)+'\n'
if len(sys.argv) == 2:
    Path(sys.argv[1]).write_text(payload)
else:
    print(payload)
