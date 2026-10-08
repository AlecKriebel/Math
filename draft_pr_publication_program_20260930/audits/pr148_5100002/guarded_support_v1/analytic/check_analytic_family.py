#!/usr/bin/env python3
"""Independent exact check of tangent-map and support-area derivations.

No author checker, edge velocity reconstruction, or outer-intersection list is used.
Only standard-library rational arithmetic is required. Run from any directory.
"""
from fractions import Fraction as R
import json


class Q:
    """Exact a+b*sqrt(d), restricted to one quadratic field per calculation."""
    def __init__(self, a=0, b=0, d=5):
        self.a, self.b, self.d = R(a), R(b), d
    def coerce(self, value):
        if isinstance(value, Q):
            if not (self.d == value.d):
                raise RuntimeError('Scientific guard failed at original source line 17')
            return value
        return Q(value, d=self.d)
    def __add__(self, value):
        v = self.coerce(value)
        return Q(self.a+v.a, self.b+v.b, self.d)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.a, -self.b, self.d)
    def __sub__(self, value):
        return self + -self.coerce(value)
    def __rsub__(self, value):
        return self.coerce(value) - self
    def __mul__(self, value):
        v = self.coerce(value)
        return Q(self.a*v.a+self.d*self.b*v.b,
                 self.a*v.b+self.b*v.a, self.d)
    __rmul__ = __mul__
    def __truediv__(self, value):
        v = self.coerce(value)
        norm = v.a*v.a-self.d*v.b*v.b
        if not (norm != 0):
            raise RuntimeError('Scientific guard failed at original source line 38')
        return self * Q(v.a/norm, -v.b/norm, self.d)
    def __rtruediv__(self, value):
        return self.coerce(value) / self
    def __pow__(self, power):
        if not (isinstance(power, int) and power >= 0):
            raise RuntimeError('Scientific guard failed at original source line 43')
        result = Q(1, d=self.d)
        for _ in range(power):
            result = result * self
        return result
    def __eq__(self, value):
        v = self.coerce(value)
        return self.a == v.a and self.b == v.b
    def positive(self):
        if self.b == 0:
            return self.a > 0
        if self.a >= 0 and self.b > 0:
            return True
        if self.a <= 0 and self.b < 0:
            return False
        if self.a > 0:
            return self.a*self.a > self.d*self.b*self.b
        return self.d*self.b*self.b > self.a*self.a
    def rational(self):
        if not (self.b == 0):
            raise RuntimeError('Scientific guard failed at original source line 62')
        return self.a
    def record(self):
        return {"a": str(self.a), "b": str(self.b), "radicand": self.d}


def padd(*terms):
    out = {}
    for term in terms:
        for monomial, coefficient in term.items():
            out[monomial] = out.get(monomial, 0)+coefficient
    return {m: c for m, c in out.items() if c}


def pmul(left, right):
    out = {}
    for (i, j), a in left.items():
        for (k, l), b in right.items():
            m = (i+k, j+l)
            out[m] = out.get(m, 0)+a*b
    return {m: c for m, c in out.items() if c}


def scale(poly, scalar):
    return {m: c*scalar for m, c in poly.items() if c*scalar}


one, t, u = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
t2, u2 = pmul(t, t), pmul(u, u)
ap = padd(scale(one, 5), scale(u2, -1))
bp = padd(scale(u2, 5), scale(one, -1))
fp = padd(pmul(ap, t2), scale(pmul(t, u), -24), bp)
left = padd(pmul(padd(scale(t, 5), scale(u, -1)), pmul(bp, bp)),
            pmul(pmul(padd(scale(u, 5), scale(t, -1)), pmul(ap, ap)), t2))
right = pmul(padd(scale(pmul(ap, t), -1), scale(pmul(u, bp), -1)), fp)
if not (left == right):
    raise RuntimeError("Third-step antipodality polynomial identity failed")


def homogeneous_F(point, next_point):
    r, s = point
    v, w = next_point
    return 5*r*r*w*w+5*v*v*s*s-24*r*v*s*w-r*r*v*v-s*s*w*w


def verify_member(points, expected_A, expected_outer_A, expected_S):
    d = points[0][0].d
    zero, one = Q(0, d=d), Q(1, d=d)
    area, outer_area = zero, zero
    squared_internal_product, squared_exterior_product = one, one
    cosine_sum, inverse_normal_sum = zero, zero
    positive_angular_half_tangents = []
    for i, (r, s) in enumerate(points):
        v, w = points[(i+1) % 6]
        if not (homogeneous_F((r, s), (v, w)) == 0):
            raise RuntimeError('Scientific guard failed at original source line 115')
        r3, s3 = points[(i+3) % 6]
        if not (r*r3+s*s3 == 0):
            raise RuntimeError("Third vertex is not the antipode")
        h = (v*s-r*w)/(s*w+r*v)
        if not (h.positive()):
            raise RuntimeError("Half angular increment not strictly positive")
        positive_angular_half_tangents.append(h.record())
        area += 2*h/(1+h*h)
        outer_area += 2*h
        ellipse_x = 2*(s*s-r*r)/(s*s+r*r)
        normal2 = 1-R(3, 16)*ellipse_x*ellipse_x
        if not (normal2.positive()):
            raise RuntimeError('Scientific guard failed at original source line 125')
        cosine_half2 = R(1, 9)/normal2
        sine_half2 = 1-cosine_half2
        if not (sine_half2.positive()):
            raise RuntimeError('Scientific guard failed at original source line 128')
        squared_internal_product *= sine_half2
        squared_exterior_product *= cosine_half2
        cosine_sum += 2*cosine_half2-1
        inverse_normal_sum += 1/normal2
    if not (area == expected_A):
        raise RuntimeError('Scientific guard failed at original source line 133')
    if not (outer_area == expected_outer_A):
        raise RuntimeError('Scientific guard failed at original source line 134')
    if not (squared_internal_product == expected_S*expected_S):
        raise RuntimeError('Scientific guard failed at original source line 135')
    if not (squared_exterior_product == R(1, 81)**2):
        raise RuntimeError('Scientific guard failed at original source line 136')
    if not (cosine_sum == R(-26, 9)):
        raise RuntimeError('Scientific guard failed at original source line 137')
    if not (inverse_normal_sum == 14):
        raise RuntimeError('Scientific guard failed at original source line 138')
    ratio = (outer_area/area).rational()
    return {
        "area": area.record(), "outer_area": outer_area.record(),
        "ratio": str(ratio), "positive_half_angle_product": str(expected_S),
        "k108": str(ratio/expected_S),
        "half_angular_increment_tangents": positive_angular_half_tangents,
        "cosine_sum": str(cosine_sum.rational()),
        "perimeter_from_normal_identity": "28/3",
        "exterior_half_angle_product": "1/81"
    }


h0, h1, hr = Q(0), Q(1), Q(0, 1)
H = [(h0, h1), (h1, hr), (hr, h1), (h1, h0), (-hr, h1), (-h1, hr)]
v0, v1, vr = Q(0, d=2), Q(1, d=2), Q(0, 1, 2)
V = [(v1, v1), (3+2*vr, v1), (-3-2*vr, v1), (-v1, v1),
     (-3+2*vr, v1), (3-2*vr, v1)]
H_result = verify_member(H, R(20, 9)*hr, R(16, 5)*hr, R(125, 324))
V_result = verify_member(V, R(32, 9)*vr, 5*vr, R(32, 81))
difference = R(H_result["k108"])-R(V_result["k108"])
if not (difference == R(553311, 3200000) and difference > 0):
    raise RuntimeError('Scientific guard failed at original source line 159')
if not (R(H_result["ratio"])*R(125, 324) == R(5, 9)):
    raise RuntimeError('Scientific guard failed at original source line 160')
if not (R(V_result["ratio"])*R(32, 81) == R(5, 9)):
    raise RuntimeError('Scientific guard failed at original source line 161')
print(json.dumps({"status": "PASS", "return_map_polynomial_identity": True,
                  "H": H_result, "V": V_result,
                  "exact_k108_difference": str(difference)}, indent=2))
