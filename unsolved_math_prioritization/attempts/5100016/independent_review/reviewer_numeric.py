"""Independent 85-digit diagnostics using actual tangent intersections.
These are non-interval diagnostics; none replaces the analytic proof.
"""
import json
import mpmath as mp
from collections import Counter

mp.mp.dps = 85
C = Counter()
worst = mp.mpf(0)


def close(a, b, label):
    global worst
    error = abs(a-b)/(1+abs(a)+abs(b))
    assert error < mp.mpf('1e-48'), (label, error)
    worst = max(worst, error)
    C[label] += 1


def det(x, y):
    return x[0]*y[1]-x[1]*y[0]


def dot(x, y):
    return x[0]*y[0]+x[1]*y[1]


def area(points):
    return sum(det(points[i], points[(i+1) % len(points)]) for i in range(len(points)))/2


families = []
pole_edges = 0
star = None
for N in [4, 8, 12, 20]:
    for tau in sorted({1, N//2-1}):
        for kval in ['0.25', '0.57', '0.88']:
            k = mp.mpf(kval)
            parameter = k*k
            kp = mp.sqrt(1-parameter)
            K, Kp = mp.ellipk(parameter), mp.ellipk(1-parameter)
            v, delta = 2*K*tau/N, 4*K*tau/N
            alpha = mp.mpf(7)/5
            beta = alpha*kp
            sn = lambda u: mp.ellipfun('sn', u, parameter)
            cn = lambda u: mp.ellipfun('cn', u, parameter)
            dn = lambda u: mp.ellipfun('dn', u, parameter)
            a, b = alpha*dn(v)/cn(v), beta/cn(v)
            normal = lambda u: (-sn(u)/a, cn(u)/b)
            trace = lambda u: sum(dn(u+j*delta) for j in range(N))

            def geometry(phase):
                normals = [normal(phase+j*delta) for j in range(N)]
                outer = []
                for i, left in enumerate(normals):
                    right = normals[(i+1) % N]
                    den = det(left, right)
                    outer.append(((right[1]-left[1])/den, (left[0]-right[0])/den))
                return normals, outer

            def actual_pedal(outer, M):
                feet = []
                for i, right in enumerate(outer):
                    left = outer[i-1]
                    edge = right[0]-left[0], right[1]-left[1]
                    fraction = dot((M[0]-left[0], M[1]-left[1]), edge)/dot(edge, edge)
                    feet.append((left[0]+fraction*edge[0], left[1]+fraction*edge[1]))
                return feet

            normals, outer = geometry(0)
            A0 = area(outer)
            B0 = area(actual_pedal(outer, (0, 0)))
            B1 = area(actual_pedal(outer, (1, 0)))
            c0, c2 = B0/A0, (B1-B0)/A0
            assert A0 > 0 and c0 > 0
            C['positive_outer_and_center_pedal'] += 1
            for phase in [mp.mpf(0), mp.mpf('0.273')*K, mp.mpf('1.179')*K]:
                normals, outer = geometry(phase)
                Aphase = area(outer)
                for i, point in enumerate(outer):
                    u = phase+v+i*delta
                    expected = (-a*a/alpha*sn(u), b*b/beta*cn(u))
                    close(point[0], expected[0], 'outer_vertices_from_actual_tangent_intersection')
                    close(point[1], expected[1], 'outer_vertices_from_actual_tangent_intersection')
                for M in [(0, 0), (2, -3), (mp.mpf('0.31'), mp.mpf('1.23')), (1, 0), (0, 1)]:
                    Bphase = area(actual_pedal(outer, M))
                    close(Bphase, Aphase*(c0+c2*dot(M, M)), 'direct_side_line_pedal_ratio')
                factor = a*a*b*b/(alpha*beta)*sn(v)*cn(v)/dn(v)
                close(Aphase, factor*trace(phase+v), 'independent_outer_trace_check')
            if tau == 1 and N > 4:
                assert c2 > 0
                C['convex_positive_coefficient_diagnostic'] += 1
            if N == 4:
                close(c0, mp.mpf('0.5'), 'N4_exact_value_diagnostic')
                close(c2, 0, 'N4_M_independence_diagnostic')

            M = (mp.mpf('.37'), mp.mpf('-.82'))
            Z, W = M[0]+1j*M[1], M[0]-1j*M[1]

            def complex_foot(u):
                nx, ny = normal(u)
                plus, minus = nx+1j*ny, nx-1j*ny
                qplus = Z/2+(1-plus*W/2)/minus
                qminus = W/2+(1-minus*Z/2)/plus
                return ((qplus+qminus)/2, (qplus-qminus)/(2j))

            def complex_points(u):
                return [complex_foot(u+j*delta) for j in range(N)]

            scalar = (c0+c2*dot(M, M))*A0/trace(v)
            for u in [mp.mpf('.347')*K+mp.mpf('.219')*1j*Kp,
                      mp.mpf('.713')*K+mp.mpf('1.271')*1j*Kp,
                      K-v+1j*Kp+mp.mpf('1e-14')]:
                value = area(complex_points(u))
                close(value, scalar*trace(u+v), 'isotropic_complex_foot_trace_diagnostic')
            # Extract each possible double-pole principal coefficient by
            # symmetric sampling. It is O(epsilon^2) after cancellation.
            pole = K-v+1j*Kp
            epsilon = mp.mpf('1e-15')
            plus_pts = complex_points(pole+epsilon)
            minus_pts = complex_points(pole-epsilon)
            singular = {0, 1, N//2, N//2+1}
            for i in range(N):
                j = (i+1) % N
                if i not in singular or j not in singular:
                    continue
                coefficient = epsilon**2*(det(plus_pts[i], plus_pts[j])+
                                          det(minus_pts[i], minus_pts[j]))/2
                assert abs(coefficient) < mp.mpf('1e-20'), (N, tau, kval, i, coefficient)
                pole_edges += 1
                C['adjacent_double_pole_zero_diagnostic'] += 1
            if N == 8 and tau == 3 and kval == '0.25':
                assert c2 < 0
                rho = mp.sqrt(-c0/c2)
                for phase in [mp.mpf('.11')*K, mp.mpf('.83')*K, mp.mpf('1.52')*K]:
                    _, outer = geometry(phase)
                    for angle in [0, mp.pi/3, mp.pi/2]:
                        point = rho*mp.cos(angle), rho*mp.sin(angle)
                        close(area(actual_pedal(outer, point)), 0, 'actual_star_side_foot_zero_circle')
                star = {'scale_alpha': str(alpha), 'rho_squared': mp.nstr(rho*rho, 32),
                        'rho_squared_over_alpha_squared': mp.nstr(rho*rho/(alpha*alpha), 32)}
            families.append({'N': N, 'tau': tau, 'k': kval,
                             'c0': mp.nstr(c0, 20), 'c2': mp.nstr(c2, 20)})

print(json.dumps({'status': 'PASS', 'diagnostic_assertions': sum(C.values()),
                  'families_of_checks': dict(sorted(C.items())),
                  'tested_orbit_families': families, 'adjacent_complex_edges': pole_edges,
                  'maximum_scaled_error': mp.nstr(worst, 14), 'star_scale_check': star,
                  'scope': '85-digit non-interval diagnostics using tangent-line intersections and projections onto their actual sides. Complex-pole tests support, but do not replace, the exact analytic review.'},
                 indent=2, sort_keys=True))
