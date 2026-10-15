"""Independent exact controls; the all-real and all-time proofs are in REPORT.md.

Uses only the standard library. Writes no files and invokes no subprocess.
Both normal Python and -O perform the same explicitly enforced checks.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
import datetime
import hashlib
import json
import os

CHECKS = 0

def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(label)

def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def neg(a):
    return [-x for x in a]

def sub(a, b):
    return add(a, neg(b))

def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)

def scale(a, b):
    return trim([b*x for x in a])

def derivative(a):
    return trim([i*a[i] for i in range(1, len(a))] or [0])

def f(s):
    return -(s-1)*(s-4)/(1+s*s)

def fp(s):
    return (5+6*s-5*s*s)/(1+s*s)**2

# Exact polynomial identities; there is no floating-point inequality oracle.
numerator = list(map(Q, [-4, 5, -1]))
denominator = list(map(Q, [1, 0, 1]))
derivative_numerator = sub(mul(derivative(numerator), denominator),
                           mul(numerator, derivative(denominator)))
check(derivative_numerator == list(map(Q, [5, 6, -5])), "f derivative")
check(add(numerator, scale(denominator, Q(4))) == list(map(Q, [0, 5, 3])),
      "lower f certificate")
check(sub(scale(denominator, Q(3, 2)), numerator) ==
      add(scale(mul([-1, 1], [-1, 1]), Q(5, 2)), [3]),
      "upper f positive square certificate")

# div(single Cartesian oscillator) = 2f + 2s f'.
div_numerator = scale(add(mul(numerator, denominator),
                         mul([0, 1], derivative_numerator)), Q(2))
check(div_numerator == list(map(Q, [-8, 20, 2, 0, -2])),
      "single-block divergence polynomial")
check(sub(scale(mul(denominator, denominator), Q(11)), div_numerator) ==
      add([14, 0, 0, 0, 13], scale(mul([Q(-1, 2), 1],
                                      [Q(-1, 2), 1]), Q(20))),
      "strict divergence positive-square certificate")

class Dual:
    """Two-variable exact forward automatic differentiation."""
    def __init__(self, value, dx=0, dy=0):
        self.value, self.dx, self.dy = Q(value), Q(dx), Q(dy)
    @staticmethod
    def coerce(other):
        return other if isinstance(other, Dual) else Dual(other)
    def __add__(self, other):
        o = self.coerce(other)
        return Dual(self.value+o.value, self.dx+o.dx, self.dy+o.dy)
    __radd__ = __add__
    def __neg__(self):
        return Dual(-self.value, -self.dx, -self.dy)
    def __sub__(self, other):
        return self + (-self.coerce(other))
    def __rsub__(self, other):
        return self.coerce(other) + (-self)
    def __mul__(self, other):
        o = self.coerce(other)
        return Dual(self.value*o.value, self.dx*o.value+self.value*o.dx,
                    self.dy*o.value+self.value*o.dy)
    __rmul__ = __mul__
    def __truediv__(self, other):
        o = self.coerce(other)
        return Dual(self.value/o.value,
                    (self.dx*o.value-self.value*o.dx)/(o.value*o.value),
                    (self.dy*o.value-self.value*o.dy)/(o.value*o.value))

for xnum in range(-8, 9):
    for ynum in range(-8, 9):
        x, y = Q(xnum, 3), Q(ynum, 5)
        s = x*x+y*y
        for omega in (Q(1), Q(7, 5), Q(-3)):
            X, Y = Dual(x, 1, 0), Dual(y, 0, 1)
            S = X*X+Y*Y
            F = -(S-1)*(S-4)/(1+S*S)
            Vx, Vy = F*X-omega*Y, F*Y+omega*X
            jacobian = ((Vx.dx, Vx.dy), (Vy.dx, Vy.dy))
            check(jacobian == ((f(s)+2*x*x*fp(s),
                                2*x*y*fp(s)-omega),
                               (2*x*y*fp(s)+omega,
                                f(s)+2*y*y*fp(s))),
                  "Cartesian AD Jacobian")
            # In the frame rotating with the trajectory, subtract omega J.
            corotating = ((Vx.dx, Vx.dy+omega), (Vy.dx-omega, Vy.dy))
            check(corotating == ((f(s)+2*x*x*fp(s), 2*x*y*fp(s)),
                                (2*x*y*fp(s), f(s)+2*y*y*fp(s))),
                  "no hidden radial/angular shear")
            if s:
                z, jz = (x, y), (-y, x)
                action_z = tuple(sum(corotating[i][j]*z[j]
                                     for j in range(2)) for i in range(2))
                action_jz = tuple(sum(corotating[i][j]*jz[j]
                                      for j in range(2)) for i in range(2))
                check(action_z == tuple((f(s)+2*s*fp(s))*v for v in z),
                      "radial eigendirection")
                check(action_jz == tuple(f(s)*v for v in jz),
                      "angular eigendirection")
        check(Q(-4) <= f(s) <= Q(3, 2), "rational growth control")
        check(2*f(s)+2*s*fp(s) < 11, "rational divergence control")

radial_rates = {Q(0): f(Q(0)), Q(1): f(Q(1))+2*fp(Q(1)),
                Q(2): f(Q(4))+8*fp(Q(4))}
check(radial_rates == {Q(0): Q(-4), Q(1): Q(3), Q(2): Q(-24, 17)},
      "exact limiting radial rates")
for r in (Q(1,100), Q(1,2), Q(99,100), Q(101,100), Q(3,2),
          Q(199,100), Q(201,100), Q(3), Q(1000000)):
    velocity = r*f(r*r)
    expected_sign = -1 if 0 < r < 1 or r > 2 else 1
    check(expected_sign*velocity > 0, "radial sign controls")

def ky(spectrum):
    ordered = sorted(spectrum, reverse=True)
    prefix, j = Q(0), 0
    for k, value in enumerate(ordered, start=1):
        prefix += value
        if prefix >= 0:
            j = k
    if j == 0:
        return Q(0)
    if j == len(ordered):
        return Q(j)
    return Q(j)+sum(ordered[:j])/(-ordered[j])

types = {'O': (Q(-4), Q(-4)), 'U': (Q(3), Q(0)),
         'S': (Q(0), Q(-24,17))}
expected = {'OO':Q(0),'OU':Q(11,4),'OS':Q(1),
            'UU':Q(203,50),'US':Q(4)+Q(27,1700),'SS':Q(2)}
rows = {}
for a, b in combinations_with_replacement(types, 2):
    pair = a+b
    spectrum = sorted(types[a]+types[b]+(Q(-100),), reverse=True)
    sums = [sum(spectrum[:k]) for k in range(1,6)]
    dim = ky(spectrum)
    check(dim == expected[pair], "exact dimension "+pair)
    rows[pair] = {'spectrum':list(map(str,spectrum)),
                  'prefix_sums':list(map(str,sums)),
                  'pointwise_KY':str(dim),
                  'fixed_index4':str(Q(4)+sums[3]/100)}
maxima = [max(sum(sorted(types[a]+types[b]+(Q(-100),), reverse=True)[:k])
              for a,b in combinations_with_replacement(types,2))
          for k in range(1,6)]
check(maxima == list(map(Q,[3,6,6,6,-94])), "all local prefix maxima")
check(max(expected, key=expected.get) == 'UU', "unique maximizing stratum")

# Substantive scope controls: rationalizing the two frequencies destroys the
# claimed exclusion; decreasing w contraction destroys volume dissipation.
# Altering the angular zero convention destroys the published dimension table.
mutants_rejected = []
ratio = Q(7, 5)
first_turns, second_turns = Q(ratio.denominator), ratio*ratio.denominator
check(first_turns.denominator == second_turns.denominator == 1,
      "rational-frequency control has genuine common angular period")
for mutant, condition in (
    ('make_frequency_ratio_rational', second_turns.denominator != 1),
    ('remove_w_contraction', Q(3)+Q(3) < 0),
    ('suppress_zero_exponents', ky([Q(3),Q(3),Q(-100)]) == Q(203,50)),
    ('reverse_radial_stability_at_r1', -radial_rates[Q(1)] == Q(3)),
    ('replace_attractor_by_outer_torus', Q(0) == Q(2)),
    ('equilibrium_has_unstable_spectrum', ky(types['O']+types['O']+(Q(-100),)) == Q(203,50)),
):
    check(not condition, "mutant was not rejected: "+mutant)
    mutants_rejected.append(mutant)

source = Path(__file__).resolve().parent.parent/'original_head_authentication_20261006'
source_pins = []
for name in ('SOURCE_STATEMENT.json','PRIOR_REPORT.md','ORIGINAL_AUTHENTICATION.json',
             'original_attempt/COUNTEREXAMPLE.md','original_attempt/README.md',
             'original_attempt/source_manifest.json'):
    body = (source/name).read_bytes()
    source_pins.append({'path':name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
authentication = json.loads((source/'ORIGINAL_AUTHENTICATION.json').read_bytes())
check(authentication['original_head'] == '8a7270989d7064a4b97badecaa4b311db5e6d49f',
      'original immutable head binding')
check(authentication['literal_original_status'] == 'claimed_solved', 'original status binding')
check(authentication['original_effort'] == '2/5', 'original effort binding')
check(json.loads((source/'SOURCE_STATEMENT.json').read_bytes())['id'] == 4900006,
      'problem statement identity')
original_counterexample_pin = next(x for x in authentication['all_original_files']
                                  if x['path'] == 'COUNTEREXAMPLE.md')
actual_counterexample_pin = next(x for x in source_pins
                                if x['path'] == 'original_attempt/COUNTEREXAMPLE.md')
check(all(original_counterexample_pin[k] == actual_counterexample_pin[k]
          for k in ('bytes', 'sha256')), 'original counterexample full-body authentication')
repaired_path = source.parent/'repaired_diagnostics_v1'/'COUNTEREXAMPLE.md'
repaired_body = repaired_path.read_bytes()
repaired_pin = {'path':'../repaired_diagnostics_v1/COUNTEREXAMPLE.md',
                'bytes':len(repaired_body), 'sha256':hashlib.sha256(repaired_body).hexdigest()}
check(repaired_pin['sha256'] == '4943f2c38effe24e0aa049242f035091df100c1089612cd2ae4c585abc161ddb',
      'full repaired statement binding')
source_pins.append(repaired_pin)
print(json.dumps({'schema':'pr111-independent-global-flow-controls/v1',
                  'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'actual_PID':os.getpid(), 'checks':CHECKS,
                  'original_head':'8a7270989d7064a4b97badecaa4b311db5e6d49f',
                  'all_checks_passed':True,'rows':rows,
                  'prefix_maxima':list(map(str,maxima)),
                  'mutants_rejected':mutants_rejected,
                  'source_pins':source_pins,
                  'limitations':'Finite controls do not prove all-real, all-time, irrationality, attraction, or priority; see analytic report.'},
                 sort_keys=True,indent=2))
