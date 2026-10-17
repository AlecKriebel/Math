"""Independent compact PR210 adversarial controls, authored 17 October 2026.

Only installed SymPy/mpmath and the standard library are used. No input files,
imports of candidate code, network, subprocesses, or filesystem writes. Results
are emitted on stdout. Finite exact checks and noninterval numerical diagnostics
do not establish the universal theorem by enumeration.
"""
import json
import math
import sys
from fractions import Fraction
import sympy as s
import mpmath as mp


def dot(x, y): return sum(a*b for a, b in zip(x, y))
def det(x, y): return x[0]*y[1]-x[1]*y[0]
def sub(x, y): return tuple(a-b for a, b in zip(x, y))
def area(p): return sum(det(p[j], p[(j+1) % len(p)]) for j in range(len(p)))/2
def clean(x): return s.factor(s.radsimp(s.simplify(x)))


exact = {}
def zero(label, expression):
    value = clean(expression)
    assert value == 0, (label, value)
    exact[label] = str(value)


def project(f, u, v):
    d = sub(v, u)
    scale = dot(sub(f, u), d)/dot(d, d)
    return tuple(u[t]+scale*d[t] for t in range(2))


def tangent_intersections(points, aa, bb):
    ns = [(p[0]/aa, p[1]/bb) for p in points]
    out = []
    for j, n in enumerate(ns):
        m = ns[(j+1) % len(ns)]
        cross = det(n, m)
        assert cross != 0
        out.append(((m[1]-n[1])/cross, (n[0]-m[0])/cross))
    return out


def exact_orbit(name, points, aa, bb, lam):
    outer = tangent_intersections(points, aa, bb)
    for j, p in enumerate(points):
        q = points[(j+1) % len(points)]
        zero(name+f'/boundary/{j}', p[0]**2/aa+p[1]**2/bb-1)
        incoming = sub(p, points[j-1]); outgoing = sub(q, p)
        incoming = tuple(x/s.sqrt(clean(dot(incoming, incoming))) for x in incoming)
        outgoing = tuple(x/s.sqrt(clean(dot(outgoing, outgoing))) for x in outgoing)
        n = (p[0]/aa, p[1]/bb)
        for t in range(2):
            zero(name+f'/reflection/{j}/{t}', incoming[t]-2*dot(incoming, n)*n[t]/dot(n, n)-outgoing[t])
        edge = sub(q, p); normal = (edge[1], -edge[0]); h = dot(normal, p)
        zero(name+f'/caustic/{j}', h*h-(aa-lam)*normal[0]**2-(bb-lam)*normal[1]**2)
    bvalues = []; dvalues = []; cvalues = []
    for sign in (1, -1):
        focus = (sign*s.sqrt(aa-bb), s.Integer(0))
        feet = [tuple(clean(x) for x in project(focus, outer[j-1], outer[j])) for j in range(len(points))]
        inv = [tuple(clean(x/dot(sub(p, focus), sub(p, focus))) for x in sub(p, focus)) for p in points]
        chords = [project(focus, p, points[(j+1) % len(points)]) for j, p in enumerate(points)]
        for j, (p, q) in enumerate(zip(points, feet)):
            n = (p[0]/aa, p[1]/bb)
            zero(name+f'/line/{sign}/{j}', dot(n, q)-1)
            zero(name+f'/perpendicular/{sign}/{j}', det(sub(q, focus), n))
            zero(name+f'/circle/{sign}/{j}', dot(q, q)-aa)
        B = clean(area(feet)); D = clean(area(inv)); C = clean(area(chords))
        bvalues.append(B); dvalues.append(D); cvalues.append(C)
        zero(name+f'/reversal/{sign}', area(list(reversed(feet)))+B)
        zero(name+f'/twice/{sign}', area(feet*2)-2*B)
    return {'outer_areas': list(map(str, bvalues)), 'outer_product': str(clean(bvalues[0]*bvalues[1])),
            'inverse_areas': list(map(str, dvalues)), 'inverse_product': str(clean(dvalues[0]*dvalues[1])),
            'chord_product': str(clean(cvalues[0]*cvalues[1]))}


def exact_controls():
    A, B, lam, X, Y = s.symbols('A B lam X Y', positive=True)
    c = s.sqrt(A-B); U = A-lam; V = B-lam
    ix = A*(X-c)/(A-c*X); iy = B*Y/(A-c*X)
    ax = A*A/U-c*c; by = B*B/V; ell = c*A*lam/U; C = -A*A*V/U
    zero('projectivity/image-conic', (ix*ix/U+iy*iy/V-1)*(A-c*X)**2-(ax*X*X+by*Y*Y-2*ell*X+C))
    matrix = s.Matrix([[ax, 0, -ell], [0, by, 0], [-ell, 0, C]])
    line = s.Matrix([X, Y, -A])
    dual = (line.T*matrix.adjugate()*line)[0]
    d = -c*lam/V; R2 = U*B*B/(V*V)
    zero('polarity/negative-center', dual/(by*C)-(X*X+Y*Y-2*d*X+d*d-R2))
    zero('image/focus-at-origin', ell*ell+C*(by-ax))
    zero('image/not-a-circle', by-ax-(A-B)*lam*lam/(U*V))
    # Laurent cancellation with a shared regular vertex: this is the N=3 case.
    e, rx, ry, ax0, ay0, bx0, by0, cx0, cy0 = s.symbols('e rx ry ax0 ay0 bx0 by0 cx0 cy0')
    R = (rx, ry); U0 = (ax0, ay0); V0 = (bx0, by0); W = (cx0, cy0)
    q0 = tuple(R[t]/e+U0[t] for t in range(2)); q1 = tuple(-R[t]/e+V0[t] for t in range(2))
    expr = s.expand(area([q0, q1, W]))
    zero('N3/no-double-pole', expr.coeff(e, -2))
    zero('N3/simple-coefficient', expr.coeff(e, -1)-det(R, tuple(U0[t]+V0[t]-2*W[t] for t in range(2)))/2)
    aa = s.Integer(21); bb = s.Integer(16); a = s.sqrt(aa)
    H = [(a, s.Integer(0)), (-3*a/5, s.Rational(16, 5)), (-3*a/5, -s.Rational(16, 5))]
    Vtri = [(s.Integer(0), s.Integer(4)), (-s.Rational(21, 5), -s.Rational(8, 5)), (s.Rational(21, 5), -s.Rational(8, 5))]
    rows = {name: exact_orbit(name, p, aa, bb, s.Rational(336, 25)) for name, p in [('H', H), ('V', Vtri)]}
    for name in ('H', 'V'):
        zero(name+'/outer-target', s.sympify(rows[name]['outer_product'])-s.Rational(12544, 25))
        for e in range(2):
            zero(name+f'/opposite-inverse/{e}', s.sympify(rows[name]['outer_areas'][e])-s.Rational(2016, 5)*s.sympify(rows[name]['inverse_areas'][1-e]))
    diamond = [(s.Integer(2), s.Integer(0)), (s.Integer(0), s.Integer(1)), (-s.Integer(2), s.Integer(0)), (s.Integer(0), -s.Integer(1))]
    rect = [(x/s.sqrt(5), y/s.sqrt(5)) for x, y in [(4, 1), (-4, 1), (-4, -1), (4, -1)]]
    rows['D'] = exact_orbit('D', diamond, s.Integer(4), s.Integer(1), s.Rational(4, 5))
    rows['C'] = exact_orbit('C', rect, s.Integer(4), s.Integer(1), s.Rational(4, 5))
    assert [rows[x]['outer_product'] for x in ('D', 'C')] == ['16', '25']
    return rows


def lattice_controls():
    cases = phases = 0
    for n in range(3, 56):
        for tau in range(1, (n+1)//2):
            if math.gcd(n, tau) != 1: continue
            for cut in range(n):
                singular = [j for j in range(n) if ((j-cut)*tau) % n in (0, tau)]
                assert set(singular) == {cut, (cut+1) % n}
                phases += 1
            inv = pow(tau, -1, n)
            assert Fraction(inv*tau, n)-(inv*tau-1)//n == Fraction(1, n)
            assert Fraction(n, 2) % 1 == (Fraction(1, 2) if n % 2 else 0)
            cases += 1
    # A repeated six-entry triangular walk is not primitive N=6.
    assert len({j*2 % 6 for j in range(6)}) == 3
    return {'N_max': 55, 'primitive_cases': cases, 'all_cyclic_cut_checks': phases, 'noncoprime_mutant_detected': True}


def numeric_case(ks, n, tau):
    k = mp.mpf(ks); m = k*k; K = mp.ellipk(m); Kp = mp.ellipk(1-m)
    v = 2*K*tau/n; delta = 2*v; L = 4*K/n; p = 1j*Kp
    jac = lambda kind, z: mp.ellipfun(kind, z, m)
    a = jac('dn', v)/jac('cn', v); b = mp.sqrt(1-m)/jac('cn', v); c = k
    lam = a*a-1; mb = 4*k/(1+k)**2; Kb = mp.ellipk(mb)
    db = -c*lam/(1-m); Rb = b*b/(1-m); tM = mp.sqrt((Rb-db)**2-a*a)
    q = lambda z: (a*(c-a*jac('sn', z))/(a-c*jac('sn', z)), a*b*jac('cn', z)/(a-c*jac('sn', z)))
    T = lambda z: area([q(z+j*delta) for j in range(n)])
    errors = {}
    def near(label, x, y, floor=1):
        err = abs(x-y)/max(mp.mpf(floor), abs(x), abs(y))
        errors[label] = max(errors.get(label, mp.mpf(0)), err)
    products = []
    for fraction in ('0.071', '0.337', '0.823'):
        w = K*mp.mpf(fraction)
        pts = [(-a*jac('sn', w+j*delta), b*jac('cn', w+j*delta)) for j in range(n)]
        out = tangent_intersections(pts, a*a, b*b)
        pedals = [[project((sign*c, 0), out[j-1], out[j]) for j in range(n)] for sign in (1, -1)]
        ap, am = [area(x) for x in pedals]; products.append(ap*am/a**4)
        near('actual-outer-feet', ap, T(w)); near('focus-shift', am, T(w+2*K))
        for j, pt in enumerate(pts):
            inc = sub(pt, pts[j-1]); outg = sub(pts[(j+1) % n], pt)
            inc = tuple(x/mp.sqrt(dot(inc, inc)) for x in inc)
            outg = tuple(x/mp.sqrt(dot(outg, outg)) for x in outg)
            normal = (pt[0]/a**2, pt[1]/b**2)
            for t in range(2): near('reflection', inc[t]-2*dot(inc, normal)*normal[t]/dot(normal, normal), outg[t])
            line = (pts[(j+1) % n][1]-pt[1], pt[0]-pts[(j+1) % n][0])
            near('confocal-tangency', dot(line, pt)**2, line[0]**2+(1-m)*line[1]**2)
        # Independent construction of contact/bicentric geometry, then dn bridge.
        R = tangent_intersections(pedals[0], a*a, a*a)
        near('contact-area-ratio', ap/area(R), a*a/(Rb*Rb-db*db))
        u = (1+k)*(w+v-K)/2
        total = mp.fsum(mp.ellipfun('dn', u+2*j*Kb*tau/n, mb) for j in range(n))
        near('area-dn-trace', ap, a**3*tM/(Rb*Rb-db*db)*total)
        for r in R: near('bicentric-circle', (r[0]-db)**2+r[1]**2, Rb*Rb)
    z = (K-v)+mp.mpf('.27')*L+mp.mpf('.31')*p
    near('reduced-period', T(z+L), T(z)); near('imaginary-antiperiod', T(z+2*p), -T(z))
    near('reflection-evenness', T(2*(K-v)-z), T(z))
    near('complementary-zero', T(K-v+p+L/2)/a**2, 0)
    reference = T(K*mp.mpf('.071'))*T(K*mp.mpf('.071')+L/2)/a**4
    near('complex-halfshift-product', T(z)*T(z+L/2)/a**4, reference)
    if n % 2: near('odd-focus-halfshift', reference, products[0])
    eps = mp.mpf('1e-24')*(mp.mpf('.6')+mp.mpf('.8')*1j)
    rm, rp = q(K+p-v+eps), q(K+p+v+eps)
    pole_error = max(abs(eps*(rm[t]+rp[t]))/a for t in range(2))
    double_error = abs(eps*eps*det(rm, rp))/a**2
    assert max(pole_error, double_error) < mp.mpf('1e-18')
    assert max(errors.values()) < mp.mpf('1e-65'), (ks, n, tau, errors)
    span = max(products)-min(products)
    if n % 2: assert abs(span) < mp.mpf('1e-65')
    else: assert span > mp.mpf('1e-8')
    return {'k': ks, 'N': n, 'tau': tau, 'max_errors': {k: mp.nstr(x, 20) for k, x in errors.items()},
            'product_samples_over_a4': [mp.nstr(x, 25) for x in products], 'product_span': mp.nstr(span, 20),
            'finite_epsilon_opposite_residue_error': mp.nstr(pole_error, 20), 'double_coefficient_error': mp.nstr(double_error, 20)}


def main():
    assert __debug__
    mp.mp.dps = 100
    rows = exact_controls(); lattice = lattice_controls()
    specs = [('.00001', 3, 1), ('.63', 5, 2), ('.91', 7, 3), ('.9999', 11, 5), ('.63', 4, 1)]
    numerical = [numeric_case(*x) for x in specs]
    print(json.dumps({'python': sys.version, 'sympy': s.__version__, 'mpmath': mp.__version__,
                      'exact_zero_count': len(exact), 'exact_zero_checks': exact, 'exact_orbits': rows,
                      'finite_lattice': lattice, 'numerical_precision': mp.mp.dps, 'numerical_cases': numerical,
                      'all_assertions_passed': True, 'limitations': 'Finite exact identities and cases; noninterval numerical diagnostics; no universal enumeration, priority certificate, or formal proof.'}, indent=2))


if __name__ == '__main__': main()
