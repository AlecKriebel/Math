"""Fresh exact controls for the pinned upstream proof, not a PDE proof.

Standard library only. No packaged manuscript checks or reviewer outputs used.
The dual-number check differentiates the signed primitive independently of the
displayed residual. Fractions avoid numerical cancellation at narrow angles.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import json
import random


class Dual:
    def __init__(self, v, t=0):
        self.v, self.t = F(v), F(t)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, x):
        x = self.coerce(x)
        return Dual(self.v + x.v, self.t + x.t)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.v, -self.t)

    def __sub__(self, x):
        return self + -self.coerce(x)

    def __rsub__(self, x):
        return self.coerce(x) + -self

    def __mul__(self, x):
        x = self.coerce(x)
        return Dual(self.v * x.v, self.t * x.v + self.v * x.t)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.coerce(x)
        return Dual(self.v / x.v, (self.t * x.v - self.v * x.t) / x.v**2)

    def __rtruediv__(self, x):
        return self.coerce(x) / self


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(t, v):
    return [t * x for x in v]


def unit(s, t):
    den = 1 + s*s + t*t
    return [2*s/den, 2*t/den, (1-s*s-t*t)/den]


def check_identity(n, a, u, b, at, r):
    d, D, e = 1-dot(n, u), 1-dot(n, a), 1-dot(a, u)
    assert dot(n, n) == 1 and dot(a, a) < 1 and dot(u, u) < 1
    rp = d/D-1
    np = scale(1/r, add(scale(d/D, add(a, scale(-1, n))), add(n, scale(-1, u))))
    assert dot(n, np) == 0
    # Automatic directional derivative along the retarded branch.
    rd = Dual(r, rp)
    nd = [Dual(x, y) for x, y in zip(n, np)]
    ud = [Dual(x, y) for x, y in zip(u, b)]
    ad = [Dual(x, y*d/D) for x, y in zip(a, at)]
    dd, DD, ed = 1-dot(nd, ud), 1-dot(nd, ad), 1-dot(ad, ud)
    k0d = add(ud, scale(-ed/DD, nd))
    primitive = scale(1/(rd*dd), k0d)
    fp = [x.t for x in primitive]
    k0 = add(u, scale(-e/D, n))
    g = scale(1/d, add(u, scale(-1, n)))
    gu = add(scale(1/d, b), scale(dot(n, b)/d**2, add(u, scale(-1, n))))

    def H(v):
        return add(v, scale(dot(a, v)/D, n))

    lhs = add(scale(-1/r, H(gu)), scale(-(1-dot(u, u))/(r*r*d), H(g)))
    residual = scale(e/(r*r*D*D), add(scale((1-dot(a, a))/D, n), scale(-1, a)))
    receiver = scale(dot(at, k0)/(r*D*D), n)
    rhs = add(scale(-1, fp), add(residual, receiver))
    assert lhs == rhs
    # Negative controls: terms essential to the identity must matter.
    no_transport = scale(-1/r, H(gu))
    no_receiver = add(scale(-1, fp), residual)
    return no_transport != rhs, no_receiver != lhs


def main():
    rng = random.Random(23203334)
    counts = {'general_rational': 0, 'near_parallel_high_momentum': 0,
              'transport_omission_detected': 0, 'receiver_omission_detected': 0}
    for _ in range(80):
        n = unit(F(rng.randint(-8, 8), 5), F(rng.randint(-8, 8), 7))
        a = [F(rng.randint(-4, 4), 9) for _ in range(3)]
        u = [F(rng.randint(-4, 4), 9) for _ in range(3)]
        b = [F(rng.randint(-8, 8), 7) for _ in range(3)]
        at = [F(rng.randint(-8, 8), 11) for _ in range(3)]
        neg1, neg2 = check_identity(n, a, u, b, at, F(rng.randint(1, 12), 5))
        counts['general_rational'] += 1
        counts['transport_omission_detected'] += int(neg1)
        counts['receiver_omission_detected'] += int(neg2)
    # Exact rational subluminal velocities with deficits down to 2^-80.
    for k in range(2, 42, 2):
        n = [F(0), F(0), F(1)]
        ua = unit(F(1, 2**(k+2)), F(0))
        aa = unit(F(1, 2**(k//2)), F(1, 2**(k//2+1)))
        u = scale(1-F(1, 2**(2*k)), ua)
        a = scale(1-F(1, 2**(2*k)), aa)
        neg1, neg2 = check_identity(n, a, u, [F(1, 3), F(-2, 7), F(1, 5)],
                                   [F(3, 11), F(1, 13), F(-2, 9)], F(1, 2**k))
        counts['near_parallel_high_momentum'] += 1
        counts['transport_omission_detected'] += int(neg1)
        counts['receiver_omission_detected'] += int(neg2)
    assert counts['transport_omission_detected'] == 100
    assert counts['receiver_omission_detected'] == 100

    eps, beta, delta_bound = F(1, 100000), F(29, 25), F(1, 1000)
    exact_delta_ratio = 4*eps/(1-5*eps)
    assert exact_delta_ratio == F(4, 99995) < delta_bound
    # Combine near, unsafe-first, and improved-far inequalities after
    # dropping nonnegative alpha and min(alpha,c). All constants exact.
    h_lower = F(1, 2)-4*delta_bound
    h_upper = (beta*(1+delta_bound)/2-F(1, 3)+8*delta_bound/3)/(F(1, 3)+beta/4)
    assert h_lower == F(62, 125)
    assert h_upper == F(37487, 93500) < h_lower
    beta_threshold = (F(1, 3)+h_lower/3-8*delta_bound/3)/((1+delta_bound)/2-h_lower/4)
    assert beta_threshold == F(992, 753) > beta

    # Explicit normalized exponent witness: baseline bounds alone do not
    # force a safe coefficient. It must fail the improved far selection.
    alpha, c, z, Hh, y, b = F(0), F(0), F(1), F(3, 5), F(3, 10), F(29, 50)
    delta = eps*(alpha+b+y+Hh)
    witness = {
        'near_selection': 2*alpha+Hh/2+2*y < z+delta,
        'far_energy_selection': b < Hh-c-alpha+delta,
        'unsafe_first': b > 2*Hh/3+z/6-delta/3,
        'unsafe_second': b < Hh+2*y-z/2+delta,
        'far_actual_relaxation': b < Hh/2-min(alpha,c)+y+F(2,1000)*z,
        'improved_window': F(16,100)*max(z,1-alpha) < y < F(49,100)*min(z,1-alpha),
        'improved_far_selection': b < Hh/2-min(alpha,c)+beta*y/2+delta,
    }
    assert all(v for k, v in witness.items() if k != 'improved_far_selection')
    assert not witness['improved_far_selection']

    # Boundary exponents needed for summability and constant absorption.
    margins = {
        'radial_transition_theta_exponent': (1-4*eps)/(1-2*eps),
        'radial_transition_small_x_power': (1-2*eps)/(1+2*eps),
        'time_weight_h_power': 1-6*eps/(1-eps),
        'time_weight_phi_power': 3-4*eps/(1-eps),
        'occupation_log_absorption_power': F(7,10)*F(16,100)*(beta-1),
    }
    assert all(v > 0 for v in margins.values())
    assert margins['occupation_log_absorption_power'] == F(56,3125)

    result = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Exact finite cancellation checks and exact rational exponent implications; not a numerical or formal proof of the global PDE theorem.',
        'cancellation': counts,
        'selection': {
            'epsilon': str(eps), 'beta': str(beta),
            'delta_over_z_strict_upper': str(exact_delta_ratio),
            'unsafe_H_over_z_strict_lower': str(h_lower),
            'improved_H_over_z_strict_upper': str(h_upper),
            'contradiction_margin': str(h_lower-h_upper),
            'sufficient_beta_threshold_for_this_relaxed_combination': str(beta_threshold),
            'baseline_unsafe_witness': {k:str(v) for k,v in dict(alpha=alpha,c=c,z=z,H=Hh,y=y,b=b,delta=delta).items()},
            'witness_checks': witness,
        },
        'positive_boundary_exponents': {k:str(v) for k,v in margins.items()},
        'all_checks_passed': True,
    }
    Path(__file__).with_name('independent-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
