#!/usr/bin/env python3
"""Portable k601 calibration: physical billiards and classical Landen traces.
Finite noninterval diagnostics, not a universal proof or a novelty claim.
Python >=3.10; mpmath==1.3.0. No files, services, or repository are required.
"""
import argparse
import json
import math
import sys
import mpmath as mp

class VerificationError(RuntimeError):
    pass

def require(ok, message):
    if not ok:
        raise VerificationError(message)

def real(x):
    require(not isinstance(x, bool), 'Boolean is not a real input')
    try:
        y = mp.mpf(x)
    except (TypeError, ValueError) as exc:
        raise VerificationError('Expected a real scalar') from exc
    require(mp.isfinite(y), 'Nonfinite scalar')
    return y

def total(xs):
    values = [real(x) for x in xs]  # Validate BEFORE any reduction.
    require(bool(values), 'Empty sum')
    return real(mp.fsum(values))

def largest(xs):
    values = [real(x) for x in xs]  # NaN must not disappear inside max().
    require(bool(values), 'Empty maximum')
    return max(values)

def dot(p, q): return total([real(p[0])*real(q[0]), real(p[1])*real(q[1])])
def cross(p, q): return real(real(p[0])*real(q[1])-real(p[1])*real(q[0]))
def add(p, q): return (real(p[0]+q[0]), real(p[1]+q[1]))
def sub(p, q): return (real(p[0]-q[0]), real(p[1]-q[1]))
def scale(k, p): return (real(k*p[0]), real(k*p[1]))
def norm(p): return real(mp.sqrt(dot(p, p)))
def unit(p):
    length = norm(p)
    require(length > 0, 'Zero direction')
    return scale(1/length, p)

def close(actual, expected, tol, label):
    actual, expected, tol = map(real, (actual, expected, tol))
    require(tol > 0, 'Nonpositive tolerance')
    error = real(abs(actual-expected)/largest([1, abs(expected)]))
    require(error < tol, label+' mismatch')
    return error

def period(N, winding, odd=True):
    require(type(N) is int and type(winding) is int, 'Integer period/winding required')
    require(N >= 3 and (not odd or N % 2 == 1), 'Odd period >=3 required')
    require(0 < winding < N/2 and math.gcd(N, winding) == 1,
            'Primitive coprime winding required')

def geometry(a, b, s):
    a, b, s = map(real, (a, b, s))
    require(a >= b > 0 and 0 < s < 1, 'Improper ellipse/caustic input')
    lam = s*b*b
    alpha, beta = real(mp.sqrt(a*a-lam)), real(mp.sqrt(b*b-lam))
    c = real(mp.sqrt(a*a-b*b))
    require(alpha >= beta > 0 and a > alpha and b > beta, 'Nonproper caustic')
    return a, b, alpha, beta, c

def initial(g, phase, direction):
    require(type(direction) is int and direction in (-1, 1), 'Direction must be +/-1')
    a, b, alpha, beta, _ = g
    phase = real(phase)
    p = (real(a*mp.cos(phase)), real(b*mp.sin(phase)))
    w = (p[0]/alpha, p[1]/beta)
    r2 = dot(w, w)
    require(r2 > 1, 'Initial point not outside caustic')
    rot = (-w[1], w[0])
    for sign in (1, -1):
        z = add(scale(1/r2, w), scale(sign*mp.sqrt(r2-1)/r2, rot))
        v = unit(sub((alpha*z[0], beta*z[1]), p))
        if direction*cross(p, v) > 0:
            return p, v
    raise VerificationError('Tangent direction selection failed')

def propagate(g, phase, count, direction=1):
    require(type(count) is int and count >= 3, 'Invalid traversal length')
    a, b, _, _, _ = g
    p, v = initial(g, phase, direction)
    points, velocities, angles = [p], [v], []
    for _ in range(count):
        aa = total([v[0]**2/a**2, v[1]**2/b**2])
        bb = 2*total([p[0]*v[0]/a**2, p[1]*v[1]/b**2])
        require(aa > 0 and bb < 0, 'No forward ellipse intersection')
        q = add(p, scale(real(-bb/aa), v))
        n = unit((q[0]/a**2, q[1]/b**2))
        new_v = sub(v, scale(2*dot(v, n), n))
        u, z = (p[0]/a, p[1]/b), (q[0]/a, q[1]/b)
        angle = real(mp.atan2(cross(u, z), dot(u, z)))
        require(0 < direction*angle < mp.pi, 'Incorrect angle lift')
        angles.append(angle)
        points.append(q)
        velocities.append(new_v)
        p, v = q, new_v
    return points, velocities, total(angles)

def shoot(a, b, N, winding):
    period(N, winding)
    eps = mp.power(10, -mp.mp.dps+12)
    lo, hi = eps, 1-eps
    def error(s):
        return real(propagate(geometry(a, b, s), '0.137', N)[2]-2*mp.pi*winding)
    require(error(lo) < 0 < error(hi), 'Closure root not bracketed')
    for _ in range(int(mp.mp.dps*mp.log(10)/mp.log(2))+8):
        mid = (lo+hi)/2
        if error(mid) > 0: hi = mid
        else: lo = mid
    return real((lo+hi)/2)

def measure(g, orbit, winding, tol, primitive=True):
    points, velocities, angle = orbit
    a, b, alpha, beta, c = g
    N = len(points)-1
    angle = real(angle)
    direction = 1 if angle > 0 else -1
    require(type(winding) is int and 0 < winding < N/2, 'Invalid traversal winding')
    if primitive: period(N, winding, odd=False)
    residuals = {'closure': largest([norm(sub(points[-1], points[0]))/a,
                                      norm(sub(velocities[-1], velocities[0]))]),
                 'winding': abs(real(angle)-direction*2*mp.pi*winding)}
    tangency, reflection, boundary, focal = [], [], [], []
    plus, minus, segment_plus, segment_minus = [], [], [], []
    for i in range(N):
        p, q = points[i], points[i+1]
        v = unit(sub(q, p)); n = (-v[1], v[0]); h = dot(n, p)
        tangency.append(abs(real(h*h-alpha**2*n[0]**2-beta**2*n[1]**2))/a**2)
        boundary.append(abs(real(p[0]**2/a**2+p[1]**2/b**2-1)))
        outgoing = unit(sub(points[i+2], q)) if i+2 <= N else velocities[-1]
        nn = unit((q[0]/a**2, q[1]/b**2))
        reflection.append(norm(sub(sub(v, scale(2*dot(v, nn), nn)), outgoing)))
        distances = []
        for focus, segment in [((c, 0), segment_plus), ((-c, 0), segment_minus)]:
            fp = sub(focus, p)
            distances.append(abs(cross(v, fp)))  # COMPLETE original support line.
            projection = real(dot(fp, sub(q, p))/dot(sub(q, p), sub(q, p)))
            clamped = min(real(1), max(real(0), projection))
            segment.append(norm(sub(focus, add(p, scale(clamped, sub(q, p))))))
        require(all(real(x) > 0 for x in distances), 'Nonpositive focal line distance')
        plus.append(real(distances[0])); minus.append(real(distances[1]))
        focal.append(abs(real(distances[0]*distances[1]-beta**2))/a**2)
    residuals.update(tangency=largest(tangency), reflection=largest(reflection),
                     boundary=largest(boundary), focal_product=largest(focal))
    for key, value in residuals.items():
        require(real(value) < real(tol), key+' validation failed')
    if primitive:
        for k in range(1, N):
            require(norm(sub(points[k], points[0]))/a > mp.sqrt(real(tol)),
                    'Unexpected shorter geometric period')
    return real(total(plus)*total(minus)), real(total(segment_plus)*total(segment_minus)), residuals

def normalized_value(m, N):
    period(N, 1)
    m = real(m)
    require(0 < m < 1, 'Landen parameter must be in (0,1)')
    K = real(mp.ellipk(m))
    q = real(mp.exp(-mp.pi*mp.ellipk(1-m)/K)); Q = real(q**N)
    theta2, theta3 = real(mp.jtheta(2, 0, Q)), real(mp.jtheta(3, 0, Q))
    M = real((theta2/theta3)**4); KM = real(mp.pi*theta3**2/2)
    gamma = real(K/(N*KM))
    require(0 < M < 1 and gamma > 0, 'Invalid transformed parameter/scale')
    return real((1-M)/gamma**2), K, gamma, M

def classical_checks(g, N, tol):
    _, _, alpha, beta, c = g
    m = real(c*c/alpha**2)  # parameter m=k^2, not modulus k.
    if m == 0:
        return real(N*N*beta**2), real(0)
    normalized, K, gamma, _ = normalized_value(m, N)
    errors = []
    dn = lambda u: real(mp.ellipfun('dn', u, m))
    cn = lambda u: real(mp.ellipfun('cn', u, m))
    dn2 = total([dn(2*K*j/N) for j in range(N)])
    errors.append(close(gamma, 1/dn2, tol, 'dn 2K normalization'))
    reciprocal = real(beta**2*total([1/dn(4*K*j/N) for j in range(N)])**2)
    value = real(alpha**2*normalized)
    errors.append(close(value, reciprocal, tol, 'reciprocal-dn value'))
    for phase in map(real, ['0', '.37', '1.1']):
        D = total([dn(phase+4*K*j/N) for j in range(N)])
        C = total([cn(phase+4*K*j/N) for j in range(N)])
        errors.append(close(real(D*D-m*C*C), normalized, tol, 'Landen trace'))
        errors.append(close(D, total([dn(phase+2*K*j/N) for j in range(N)]), tol,
                            'odd dn grid permutation'))
    return value, largest(errors)

def fmt(x): return mp.nstr(real(x), 24)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--digits', type=int, default=60,
                        help='requested decimal digits, 50..160; 40 guard digits added')
    args = parser.parse_args()
    require(sys.version_info >= (3, 10), 'Python 3.10+ required')
    require(mp.__version__ == '1.3.0', 'mpmath 1.3.0 required')
    require(50 <= args.digits <= 160, 'digits outside 50..160')
    mp.mp.dps = args.digits+40
    tol = real(mp.power(10, -args.digits+20))
    configurations = [(2, 3, 1), (2, 5, 1), (2, 5, 2), (2, 7, 1),
                      (2, 7, 2), (2, 7, 3), ('1.01', 5, 2), (10, 7, 3)]
    rows, errors, orbit_count = [], [], 0
    worst = {key: real(0) for key in ['closure', 'winding', 'tangency', 'reflection',
                                     'boundary', 'focal_product']}
    for aspect, N, winding in configurations:
        s = shoot(aspect, 1, N, winding); g = geometry(aspect, 1, s)
        value, analytic_error = classical_checks(g, N, tol)
        errors.append(analytic_error)
        observed = []
        for phase in ['0', '.37', '1.1']:
            for direction in (1, -1):
                I, _, residuals = measure(g, propagate(g, phase, N, direction), winding, tol)
                errors.append(close(I, value, tol, 'physical/Landen value'))
                observed.append(real(I)); orbit_count += 1
                for key in worst: worst[key] = largest([worst[key], residuals[key]])
        for repetition in (3, 5):
            I, _, residuals = measure(g, propagate(g, '.37', repetition*N),
                                      repetition*winding, tol, primitive=False)
            errors.append(close(I, repetition**2*value, tol, 'repetition r^2'))
            orbit_count += 1
            for key in worst: worst[key] = largest([worst[key], residuals[key]])
        rows.append({'a_over_b': str(aspect), 'primitive_N': N, 'winding': winding,
                     'lambda_over_b2': fmt(s), 'I': fmt(value),
                     'phase_relative_spread': fmt((largest(observed)-min(observed))/value)})
    # Circular limit: regular star, exact q_i=beta and I=N^2*beta^2.
    for N, winding in [(3, 1), (5, 2)]:
        s = real(mp.sin(mp.pi*winding/N)**2); g = geometry(2, 2, s)
        for direction in (1, -1):
            I, _, _ = measure(g, propagate(g, '.37', N, direction), winding, tol)
            errors.append(close(I, N*N*g[3]**2, tol, 'circular exact value'))
            orbit_count += 1
    # Exact manuscript N4 pair: a=sqrt(3/2),b=sqrt(3)/2; alpha=1,beta=1/2.
    # Diamond I=8; axis-aligned rectangle (+/-1,+/-1/2) gives I=9.
    g4 = geometry(mp.sqrt(mp.mpf(3)/2), mp.sqrt(3)/2, mp.mpf(2)/3)
    I0, _, _ = measure(g4, propagate(g4, 0, 4), 1, tol)
    I1, _, _ = measure(g4, propagate(g4, mp.atan(1/mp.sqrt(2)), 4), 1, tol)
    errors.append(close(I0, 8, tol, 'exact N4 diamond'))
    errors.append(close(I1, 9, tol, 'exact N4 rectangle'))
    require(abs(real(I0-I1)) > mp.mpf('.5'), 'Even-period counterexample not distinguished')
    orbit_count += 2
    # Real rejection controls, executed identically under ordinary Python and -O.
    controls = []
    def reject(label, call):
        try: call()
        except VerificationError: controls.append(label); return
        raise VerificationError('Negative control unexpectedly accepted: '+label)
    for bad in [mp.nan, mp.inf, -mp.inf]:
        reject('nonfinite maximum '+str(bad), lambda bad=bad: largest([1, bad]))
        reject('nonfinite sum '+str(bad), lambda bad=bad: total([1, bad]))
        reject('nonfinite comparison '+str(bad), lambda bad=bad: close(bad, 1, tol, 'injected'))
    reject('complex scalar', lambda: real(mp.mpc(1, 1)))
    for bad in [(0, 1, '.5'), (2, 1, 0), (2, 1, 1), (mp.nan, 1, '.5')]:
        reject('bad geometry '+str(bad), lambda bad=bad: geometry(*bad))
    for bad in [(4, 1), (9, 3), (True, 1), (5, 0)]:
        reject('bad primitive period '+str(bad), lambda bad=bad: period(*bad))
    for bad in [0, 1, mp.inf]:
        reject('bad Landen parameter '+str(bad), lambda bad=bad: normalized_value(bad, 5))
    normalized, K, _, _ = normalized_value(mp.mpf('.5'), 5)
    wrong_C = total([real(mp.ellipfun('cn', 2*K*j/5, mp.mpf('.5'))) for j in range(5)])
    D = total([real(mp.ellipfun('dn', 4*K*j/5, mp.mpf('.5'))) for j in range(5)])
    reject('wrong cn 2K grid identity', lambda: close(D*D-mp.mpf('.5')*wrong_C**2,
                                                    normalized, tol, 'wrong grid'))
    g = geometry(2, 1, shoot(2, 1, 3, 1))
    orbit = propagate(g, '.37', 3); I, segment_I, _ = measure(g, orbit, 1, tol)
    reject('wrong finite value identity', lambda: close(I, I*mp.mpf('1.01'), tol, 'wrong identity'))
    reject('segment distances substituted for complete lines',
           lambda: close(segment_I, I, tol, 'segment semantics'))
    points, velocities, angle = orbit
    damaged_points = list(points); damaged_points[1] = add(points[1], (mp.mpf('1e-5'), 0))
    reject('corrupted physical orbit', lambda: measure(g, (damaged_points, velocities, angle), 1, tol))
    print(json.dumps({'status': 'PASS', 'kind': 'finite noninterval calibration; not a universal proof',
                      'python': '.'.join(map(str, sys.version_info[:3])), 'mpmath': mp.__version__,
                      'optimized': bool(sys.flags.optimize), 'requested_digits': args.digits,
                      'working_digits': mp.mp.dps, 'tolerance': fmt(tol),
                      'configuration_count': len(rows), 'validated_orbits': orbit_count,
                      'max_scaled_comparison_error': fmt(largest(errors)),
                      'worst_physical_residuals': {k: fmt(v) for k, v in worst.items()},
                      'exact_N4_values': [fmt(I0), fmt(I1)],
                      'negative_controls_rejected': len(controls), 'negative_controls': controls,
                      'configurations': rows}, indent=2, allow_nan=False))

if __name__ == '__main__':
    main()
