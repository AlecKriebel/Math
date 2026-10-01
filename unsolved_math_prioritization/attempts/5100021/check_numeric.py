"""Non-interval 95-digit diagnostics for the focal source constructions.
Direct line intersections and feet are compared with the analytic formulas.
No finite set of these diagnostics substitutes for the universal proof.
"""
from collections import Counter
from math import gcd
import json
import mpmath as mp

mp.mp.dps = 95
C = Counter()
worst = mp.mpf(0)


def close(x, y, family):
    global worst
    error = abs(x-y)/(1+abs(x)+abs(y))
    assert error < mp.mpf('1e-48'), (family, error)
    worst = max(worst, error)
    C[family] += 1


def dot(x, y):
    return x[0]*y[0]+x[1]*y[1]


def det(x, y):
    return x[0]*y[1]-x[1]*y[0]


def area(points):
    return sum(det(points[j], points[(j+1) % len(points)]) for j in range(len(points)))/2


cases = []
for N in [4, 8, 12, 20, 28]:
    for tau in sorted({1, 3, N//2-1}):
        if 2*tau >= N or gcd(tau, N) != 1:
            continue
        for kval in ['0.25', '0.63', '0.96']:
            k = mp.mpf(kval)
            kp = mp.sqrt(1-k*k)
            K, Kp = mp.ellipk(k*k), mp.ellipk(1-k*k)
            v, delta = 2*K*tau/N, 4*K*tau/N
            sn = lambda u: mp.ellipfun('sn', u, k*k)
            cn = lambda u: mp.ellipfun('cn', u, k*k)
            dn = lambda u: mp.ellipfun('dn', u, k*k)
            sv, cv, dv = sn(v), cn(v), dn(v)
            alpha = mp.mpf('1.4')
            a, b = alpha*dv/cv, alpha*kp/cv
            focus = (alpha*k, mp.mpf(0))
            H = 1-2*k*k*sv*sv+k*k*sv**4
            trace = lambda u: sum(dn(u+j*delta) for j in range(N))

            def explicit(x):
                S, CC = sn(x), cn(x)
                L = 1-k*k*sv*sv*S*S
                anti = (-alpha*(H*S+k*(cv*cv-dv*dv*S*S))/(cv*cv*L),
                        alpha*CC*(2*kp*kp-H*(1+k*S))/(kp*cv*cv*L))
                pedal = (alpha*(k-S)/(1-k*S), alpha*kp*CC/(1-k*S))
                return pedal, anti

            def direct(w, F=focus, compare=False):
                vertices = [(-a*sn(w+j*delta), b*cn(w+j*delta)) for j in range(N)]
                feet, anti = [], []
                for j, p in enumerate(vertices):
                    q = vertices[(j+1) % N]
                    edge = q[0]-p[0], q[1]-p[1]
                    parameter = dot((F[0]-p[0], F[1]-p[1]), edge)/dot(edge, edge)
                    feet.append((p[0]+parameter*edge[0], p[1]+parameter*edge[1]))
                    n, m = (p[0]-F[0], p[1]-F[1]), (q[0]-F[0], q[1]-F[1])
                    hh, gg = dot(n, p), dot(m, q)
                    denominator = det(n, m)
                    anti.append(((hh*m[1]-gg*n[1])/denominator,
                                 (n[0]*gg-m[0]*hh)/denominator))
                    if compare:
                        ef, ea = explicit(w+v+j*delta)
                        for coord in range(2):
                            close(feet[-1][coord], ef[coord], 'actual_chord_foot_formula')
                            close(anti[-1][coord], ea[coord], 'actual_antipedal_intersection_formula')
                return area(vertices), area(feet), area(anti)

            A0, F0, B0 = direct(mp.mpf(0), compare=True)
            cf, cb = F0/trace(K+v), B0/trace(0)
            constant = F0*B0
            for phase in ['0.137', '0.551', '1.183']:
                w = mp.mpf(phase)*K
                A, AF, BA = direct(w, compare=True)
                assert AF > 0 and A > 0
                C['real_positive_original_and_pedal_areas'] += 1
                close(AF*BA, constant, 'focal_product_all_real_phases')
                close(AF, cf*trace(w+K+v), 'focal_pedal_shifted_trace')
                close(BA, cb*trace(w), 'focal_antipedal_original_trace')
                close(A, a*b*sv*cv/dv*trace(w), 'original_area_trace')
                _, minusF, minusB = direct(w, (-focus[0], 0))
                close(AF, minusF, 'opposite_focal_pedal_area')
                close(BA, minusB, 'opposite_focal_antipedal_area')
                close(trace(w)*trace(w+2*K/N), trace(0)*trace(2*K/N),
                      'complementary_halfperiod_trace_product')
            for w in [mp.mpf('.23')*K+mp.mpf('.31')*1j*Kp,
                      mp.mpf('.71')*K+mp.mpf('1.27')*1j*Kp,
                      1j*Kp+mp.mpf('1e-12'), K+1j*Kp-v+mp.mpf('1e-12')]:
                _, AF, BA = direct(w)
                close(AF, cf*trace(w+K+v), 'complex_focal_pedal_trace')
                close(BA, cb*trace(w), 'complex_focal_antipedal_trace')
                close(AF*BA, constant, 'complex_focal_product')
            w = mp.mpf('.41')*K+mp.mpf('.19')*1j*Kp
            _, _, U = direct(w)
            _, _, Uminus = direct(-w)
            _, _, Uimag = direct(w+2j*Kp)
            close(U, Uminus, 'antipedal_exact_symmetry_diagnostic')
            close(Uimag, -U, 'antipedal_imaginary_antiperiod_diagnostic')
            if N == 4:
                close(B0, 2*A0, 'N4_antipedal_twice_original_control')
                close(constant, 16*alpha**4*kp**2, 'N4_product_value_control')
            cases.append({'N': N, 'tau': tau, 'modulus': kval,
                          'product': mp.nstr(constant, 25),
                          'antipedal_over_original': mp.nstr(B0/A0, 25)})

print(json.dumps({'status': 'PASS', 'diagnostic_assertions': sum(C.values()),
                  'families': dict(sorted(C.items())),
                  'maximum_scaled_error': mp.nstr(worst, 15),
                  'orbit_cases': cases,
                  'scope': '95-digit non-interval diagnostics using actual source-defined lines and perpendicular feet. Finite sampling does not establish universal pole cancellation or invariance; those are analytical claims in PROOF.md.'},
                 indent=2, sort_keys=True))
