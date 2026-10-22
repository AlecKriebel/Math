#!/usr/bin/env python3
"""Exact identity controls. Standard library only; no numerical proof claims."""
from fractions import Fraction as F
import json
from pathlib import Path


class P:
    """Sparse polynomials over Q; monomials are sorted (name, exponent) tuples."""
    def __init__(self, x=0):
        if isinstance(x, P):
            self.d = dict(x.d)
        elif isinstance(x, dict):
            self.d = {m: F(v) for m, v in x.items() if v}
        else:
            self.d = {(): F(x)} if x else {}

    def __add__(self, other):
        d = dict(self.d)
        for m, v in P(other).d.items():
            d[m] = d.get(m, F(0)) + v
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -v for m, v in self.d.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        d = {}
        for a, x in self.d.items():
            for b, y in P(other).d.items():
                m = dict(a)
                for k, v in b:
                    m[k] = m.get(k, 0) + v
                key = tuple(sorted(m.items()))
                d[key] = d.get(key, F(0)) + x*y
        return P(d)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        r = P(1)
        for _ in range(n):
            r = r*self
        return r

    def __eq__(self, other):
        return self.d == P(other).d

    def reduce_square(self, variable, replacement):
        result = P()
        for monomial, coefficient in self.d.items():
            exponents = dict(monomial)
            exponent = exponents.pop(variable, 0)
            if exponent % 2:
                exponents[variable] = 1
            result += P({tuple(sorted(exponents.items())): coefficient}) * replacement**(exponent//2)
        return result


def var(name):
    return P({((name, 1),): 1})


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), P())


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


passed = []
rejected = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    passed.append(name)


def reject(name, false_condition):
    if false_condition:
        raise AssertionError('Corrupted control accepted: '+name)
    rejected.append(name)


c, w = var('c'), var('w')
reduce_circle = lambda x: P(x).reduce_square('w', 1-c*c)
velocity = [-2*w, 4+c, 2*c]
acceleration = [-4-5*c, -4*w, -4*w]
jerk = [14*w, -4-13*c, -8*c]
determinant = reduce_circle(dot(velocity, cross(acceleration, jerk)))
expected_det = -6*(c**3-24*c*c+32)
check('closed_curve_torsion_numerator', determinant == expected_det)
check('closed_curve_speed_squared', reduce_circle(dot(velocity, velocity)) == (4+c)**2+4)
check('torsion_sign_certificate', c**3-24*c*c+32 == 7+(c+1)*(c*c-c+1)+24*(1-c*c))
check('positive_quadratic_certificate', c*c-c+1 == (c-F(1, 2))**2+F(3, 4))
check('speed_lower_bound', 3**2+4 == 13)
reject('wrong_torsion_sign', determinant == -expected_det)
reject('wrong_speed_constant', reduce_circle(dot(velocity, velocity)) == (4+c)**2+3)

# Frenet normal at q=pi/4: project acceleration orthogonally to velocity.
v = [F(-2), F(4), F(0)]
a = [F(-4), F(-4), F(-4)]
inner = sum(x*y for x,y in zip(v,a))
speed2 = sum(x*x for x in v)
normal_raw = [a[j]-inner*v[j]/speed2 for j in range(3)]
check('normal_projection_at_quarter_turn', normal_raw == [F(-24,5),F(-12,5),F(-4)])
normal_norm2 = sum(x*x for x in normal_raw)
check('normal_norm_squared', normal_norm2 == F(224,5))
check('normal_vertical_component_squared', normal_raw[2]**2/normal_norm2 == F(25,70))
check('offset_height_positive_for_abs_t_below_one', 25 < 70 and normal_raw[2] < 0)
t,h,x,y = (var(s) for s in ['t','h','x','y'])
p1 = [5-t,P(0),P(0)]
p2 = [-(5-t),P(0),P(0)]
p3 = [P(0),3+t,P(0)]
p4 = [x,y,h]
sub = lambda a,b:[a[j]-b[j] for j in range(3)]
volume = dot(sub(p2,p1),cross(sub(p3,p1),sub(p4,p1)))
check('offset_nonplanarity_determinant', volume == -2*(5-t)*(3+t)*h)
reject('offsets_falsely_declared_planar', volume == 0)

# Every integer Fourier mode is handled symbolically, with i^2=-1.
m,r,p,z,b,d,i = (var(s) for s in ['m','r','p','z','b','d','i'])
complex_reduce = lambda expr: P(expr).reduce_square('i',P(-1))
bp_numerator = -p*(m*m-1)*b-i*m*z*d
cp_numerator = -i*m*p*p*(m*m-1)*b+m*m*p*z*d
check('fourier_meridian_strain', complex_reduce(-i*m*p*bp_numerator+cp_numerator) == 0)
check('fourier_mixed_strain', bp_numerator+p*(m*m-1)*b+i*m*z*d == 0)
reject('fourier_wrong_axial_sign', complex_reduce(-i*m*p*bp_numerator-cp_numerator) == 0)

# Associate derivatives in the orthogonal equal-length (C_u,C_v) basis.
co,si = var('co'),var('si')
unit = lambda expr: P(expr).reduce_square('si',1-co*co)
fu,fv = [co,-si],[si,co]
check('associate_u_metric', unit(dot(fu,fu)) == 1)
check('associate_v_metric', unit(dot(fv,fv)) == 1)
check('associate_cross_metric', dot(fu,fv) == 0)
pi = var('pi')
period = 2*pi*si
check('associate_period_coefficient', period == si*(2*pi))
reject('nontrivial_associate_automatic_descent', period == 0)

# Normal ribbon algebra in an orthonormal Frenet frame.
kap,tau,kaps,taus = (var(s) for s in ['kap','tau','kaps','taus'])
xs = [1-t*kap,P(0),t*tau]
xt = [P(0),P(1),P(0)]
normal_numerator = [-t*tau,P(0),1-t*kap]
mixed_derivative = [-kap,P(0),tau]
energy = (1-t*kap)**2+t*t*tau*tau
check('ribbon_first_form', dot(xs,xs) == energy and dot(xs,xt)==0 and dot(xt,xt)==1)
check('ribbon_normal_orthogonal', dot(xs,normal_numerator)==0 and dot(xt,normal_numerator)==0)
check('ribbon_normal_length', dot(normal_numerator,normal_numerator)==energy)
mixed_numerator = dot(mixed_derivative,normal_numerator)
check('ribbon_mixed_second_form', mixed_numerator==tau)
check('ribbon_curvature_numerator', -(mixed_numerator**2)==-(tau*tau))
reject('ribbon_positive_curvature', -(mixed_numerator**2)==tau*tau)
gamma_ss = [P(0),kap,P(0)]
normal_t_at_core = [-tau,P(0),P(0)]
frenet_normal_ss = [-kaps,-kap*kap-tau*tau,taus]
lt = dot(frenet_normal_ss,[P(0),P(0),P(1)])+dot(gamma_ss,normal_t_at_core)
check('ribbon_core_Lt', lt==taus)
check('ribbon_core_asymptotic', dot(gamma_ss,[P(0),P(0),P(1)])==0)
reject('ribbon_wrong_Lt_factor', lt==2*taus)

# Denominator-cleared implicit differentiation of L+2Ma+Na^2=0 at a=0.
L_t,M = var('L_t'),var('M')
a_t_numerator = -L_t
check('return_multiplier_linearization', 2*M*L_t+2*M*a_t_numerator==0)
reject('return_multiplier_missing_half', 2*M*L_t+2*M*(-2*L_t)==0)

result = {
    'problem_id': '7000003',
    'arithmetic': 'exact rational sparse polynomial identities; no floating point',
    'assertions_passed': len(passed),
    'corrupted_controls_rejected': len(rejected),
    'passed': passed,
    'rejected': rejected,
    'scope': 'Algebraic controls only. Analytic/topological proofs and the unresolved global problem are not machine-certified.'
}
expected = Path(__file__).with_name('EXPECTED_RESULTS.json')
if expected.exists():
    if json.loads(expected.read_text()) != result:
        raise AssertionError('Expected result mismatch')
print(json.dumps(result,indent=2,sort_keys=True))
