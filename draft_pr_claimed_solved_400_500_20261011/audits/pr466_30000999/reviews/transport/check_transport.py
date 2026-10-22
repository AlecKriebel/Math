#!/usr/bin/env python3
"""Independent finite checks; the analytical report, not this script, proves universality.

Standard library only. Writes only numerical_checks.json beside this script.
No source proof/check scripts are imported or executed.
"""
from fractions import Fraction
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parent


def clean(a):
    return {i: v for i, v in a.items() if v}


def add(a, b):
    c = dict(a)
    for i, v in b.items():
        c[i] = c.get(i, 0) + v
    return clean(c)


def scale(a, c):
    return clean({i: c*v for i, v in a.items()})


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (h, l), w in b.items():
            ind = (i+h, j+l)
            c[ind] = c.get(ind, 0) + v*w
    return clean(c)


def derivative(a, axis):
    c = {}
    for ind, v in a.items():
        if ind[axis]:
            new = list(ind)
            new[axis] -= 1
            c[tuple(new)] = v * ind[axis]
    return c


def power(a, k):
    out = {(0, 0): 1}
    for _ in range(k):
        out = mul(out, a)
    return out


def harmonic(k):
    return {(k-2*j, 2*j): (-1)**j * math.comb(k, 2*j)
            for j in range(k//2+1)}


def eigenvalue(n, k):
    out = Fraction((-1)**(k//2), 1)
    for j in range(k//2):
        out *= Fraction(2*j+1, n-1+2*j)
    return out


def log_moment(n, q):
    alpha = (n-2)/2
    return (math.lgamma(alpha+1) + math.lgamma(q/2+1)
            - math.lgamma(q/2+alpha+1))


def log_lambda(n, k):
    alpha = (n-2)/2
    m = k/2
    return (math.lgamma(alpha+0.5) - 0.5*math.log(math.pi)
            + math.lgamma(m+0.5) - math.lgamma(m+alpha+0.5))


def log_ratio_bound(n, p, a, k):
    return (math.log((k+n-2)/(2*k)) + (1-1/p)*math.log(1-a)
            + log_moment(n, 2*k) - log_lambda(n, k)
            - log_moment(n, p*(k-1))/p)


def log_asymptotic_constant(n, p, a):
    alpha = (n-2)/2
    return (0.5*math.log(math.pi) + (1-1/p)*math.lgamma(alpha+1)
            + alpha*math.log(p)/p + (1-1/p)*math.log(1-a)
            - (1+alpha+alpha/p)*math.log(2) - math.lgamma(alpha+0.5))


exact = []
for k in (2, 4, 6, 8, 12, 16):
    h = harmonic(k)
    hx = derivative(h, 0)
    hy = derivative(h, 1)
    lap = add(derivative(hx, 0), derivative(hy, 1))
    euler = add(mul({(1, 0): 1}, hx), mul({(0, 1): 1}, hy))
    gradient_square = add(mul(hx, hx), mul(hy, hy))
    gradient_target = scale(power({(2, 0): 1, (0, 2): 1}, k-1), k*k)
    assert not lap
    assert euler == scale(h, k)
    assert gradient_square == gradient_target
    exact.append({'k': k, 'laplacian_zero': True,
                  'euler_identity': True, 'gradient_square_identity': True})

moment_checks = []
for n in (3, 4, 5, 10):
    alpha = Fraction(n-2, 2)
    for ell in (0, 1, 2, 8, 32):
        rational = Fraction(math.factorial(ell), 1)
        for j in range(1, ell+1):
            rational /= alpha+j
        gamma = math.exp(log_moment(n, 2*ell))
        relative_error = abs(gamma/float(rational)-1)
        assert relative_error < 1e-12
        moment_checks.append({'n': n, 'q': 2*ell,
                              'exact_moment': str(rational),
                              'gamma_relative_error': relative_error})
    for k in (2, 4, 8, 32, 128):
        value = float(abs(eigenvalue(n, k)))
        relative_error = abs(math.exp(log_lambda(n, k))/value-1)
        assert relative_error < 1e-12
        moment_checks.append({'n': n, 'k': k,
                              'exact_abs_lambda': str(abs(eigenvalue(n, k))),
                              'gamma_relative_error': relative_error})

asymptotic = []
for n in (3, 4, 5, 10):
    alpha = (n-2)/2
    for p in (1.0, 1.25, math.sqrt(2), math.pi, 31.5):
        for a in (0.5, 0.999):
            seq = []
            for k in (16, 256, 4096, 65536):
                log_bound = log_ratio_bound(n, p, a, k)
                log_scale = log_asymptotic_constant(n, p, a) + alpha*math.log(k)/p
                normalized = math.exp(log_bound-log_scale)
                seq.append({'k': k, 'lower_ratio_bound': math.exp(log_bound),
                            'bound_over_predicted_asymptotic': normalized})
            assert abs(seq[-1]['bound_over_predicted_asymptotic']-1) < 0.002
            asymptotic.append({'n': n, 'p': p, 'a': a,
                               'exponent': alpha/p, 'sequence': seq})


def velocity_data(n, k, b, t, x):
    z = complex(x[0], x[1])
    h = (z**k).real
    zprev = z**(k-1)
    ambient = [k*zprev.real, -k*zprev.imag] + [0.0]*(n-2)
    grad = [ambient[j]-k*h*x[j] for j in range(n)]
    eta = 1+t*b*h
    L = k*(k+n-2)
    grad2 = sum(g*g for g in grad)
    v = [b*g/(L*eta) for g in grad]
    div_v = -b*h/eta - t*b*b*grad2/(L*eta*eta)
    return v, div_v, eta


def integrate(n, k, b, initial, ps, steps=512):
    # State = position, log-Jacobian, trajectory actions for each real p.
    state = initial[:] + [0.0]*(1+len(ps))
    dt = 1/steps
    def rhs(t, s):
        v, div_v, _ = velocity_data(n, k, b, t, s[:n])
        speed = math.sqrt(sum(vj*vj for vj in v))
        return v + [div_v] + [speed**p for p in ps]
    def shifted(s, ds, amount):
        return [sj+amount*dj for sj, dj in zip(s, ds)]
    for j in range(steps):
        t = j*dt
        f1 = rhs(t, state)
        f2 = rhs(t+dt/2, shifted(state, f1, dt/2))
        f3 = rhs(t+dt/2, shifted(state, f2, dt/2))
        f4 = rhs(t+dt, shifted(state, f3, dt))
        state = [sj+dt*(v1+2*v2+2*v3+v4)/6
                 for sj, v1, v2, v3, v4 in zip(state, f1, f2, f3, f4)]
    x = state[:n]
    _, _, eta = velocity_data(n, k, b, 1.0, x)
    jacobian_error = abs(eta*math.exp(state[n])-1)
    sphere_error = abs(sum(xj*xj for xj in x)-1)
    cosine = sum(xj*yj for xj, yj in zip(initial, x))
    distance = math.acos(min(1.0, max(-1.0, cosine)))
    cost_checks = []
    for p, action in zip(ps, state[n+1:]):
        endpoint = distance**p
        # For stationary trajectories acos can amplify a last-bit dot error.
        assert endpoint <= action + 1e-9
        cost_checks.append({'p': p, 'endpoint_cost': endpoint,
                            'trajectory_p_action': action})
    assert jacobian_error < 1e-9
    assert sphere_error < 1e-9
    return {'jacobian_identity_absolute_error': jacobian_error,
            'sphere_norm_absolute_error': sphere_error,
            'cost_checks': cost_checks}

flow_checks = []
ps = (1.0, 1.5, math.pi, 31.5)
for n in (3, 5):
    starts = [[0.6, 0.0, 0.8]+[0.0]*(n-3),
              [0.48, 0.64, 0.6]+[0.0]*(n-3),
              [1/math.sqrt(n)]*n,
              [math.cos(0.37), math.sin(0.37)]+[0.0]*(n-2),
              [0.0, 0.0, 1.0]+[0.0]*(n-3)]
    for k in (2, 4, 8):
        for a in (0.8, 0.999):
            b = a*float(eigenvalue(n, k))
            for j, x in enumerate(starts):
                check = integrate(n, k, b, x, ps)
                flow_checks.append({'n': n, 'k': k, 'a': a, 'b': b,
                                    'start_index': j, **check})

result = {
 'status': 'passed',
 'interpretation': 'Finite checks only; universal proof is in ANALYTICAL_REPORT.md.',
 'independence': 'No frozen author check code or results imported, read, or executed.',
 'exact_polynomial_checks': exact,
 'normalization_and_gamma_crosschecks': moment_checks,
 'asymptotic_checks_for_real_p': asymptotic,
 'smooth_flow_checks': flow_checks,
 'summary': {
   'polynomial_cases': len(exact),
   'moment_and_eigenvalue_cases': len(moment_checks),
   'real_p_asymptotic_parameter_cases': len(asymptotic),
   'flow_trajectories': len(flow_checks),
   'real_p_trajectory_cost_checks': len(flow_checks)*len(ps),
   'max_jacobian_error': max(c['jacobian_identity_absolute_error'] for c in flow_checks),
   'max_sphere_norm_error': max(c['sphere_norm_absolute_error'] for c in flow_checks),
 }
}
(ROOT/'numerical_checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result['summary'], indent=2))
