#!/usr/bin/env python3
"""Independent exact audit; no submitted checker, CAS, or nonstandard library.

Only source inputs are the two displayed vertex lists and the ellipse equations.
Outputs are symbolic rational/quadratic-field values; floats are cosmetic only.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json
import platform
import sys


class Q:
    """An exact element a+b*sqrt(d), with d=2 or 5."""
    def __init__(self, a=0, b=0, d=5):
        self.a, self.b, self.d = F(a), F(b), d
    def coerce(self, z):
        if isinstance(z, Q):
            if not (z.d == self.d):
                raise RuntimeError('Scientific guard failed at original source line 22')
            return z
        return Q(z, d=self.d)
    def __add__(self, z):
        z = self.coerce(z)
        return Q(self.a+z.a, self.b+z.b, self.d)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.a, -self.b, self.d)
    def __sub__(self, z):
        return self + (-self.coerce(z))
    def __rsub__(self, z):
        return self.coerce(z) - self
    def __mul__(self, z):
        z = self.coerce(z)
        return Q(self.a*z.a+self.d*self.b*z.b,
                 self.a*z.b+self.b*z.a, self.d)
    __rmul__ = __mul__
    def __truediv__(self, z):
        z = self.coerce(z)
        norm = z.a*z.a-self.d*z.b*z.b
        if not (norm):
            raise RuntimeError('Scientific guard failed at original source line 43')
        return self * Q(z.a/norm, -z.b/norm, self.d)
    def __rtruediv__(self, z):
        return self.coerce(z)/self
    def __pow__(self, n):
        if not (n >= 0):
            raise RuntimeError('Scientific guard failed at original source line 48')
        ans = Q(1, d=self.d)
        for _ in range(n):
            ans *= self
        return ans
    def __eq__(self, z):
        z = self.coerce(z)
        return (self.a, self.b) == (z.a, z.b)
    def sign(self):
        if self.b == 0:
            return (self.a > 0)-(self.a < 0)
        if self.a == 0:
            return (self.b > 0)-(self.b < 0)
        if self.a*self.b > 0:
            return (self.a > 0)-(self.a < 0)
        delta = self.a*self.a-self.d*self.b*self.b
        return ((delta > 0)-(delta < 0))*((self.a > 0)-(self.a < 0))
    def rational(self):
        if not (self.b == 0):
            raise RuntimeError('Scientific guard failed at original source line 66')
        return self.a
    def __str__(self):
        if not self.b:
            return str(self.a)
        if not self.a:
            return f"({self.b})*sqrt({self.d})"
        return f"({self.a})+({self.b})*sqrt({self.d})"


def sqrt_fraction(q):
    q = F(q)
    if not (q >= 0):
        raise RuntimeError('Scientific guard failed at original source line 78')
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    if not (n*n == q.numerator and d*d == q.denominator):
        raise RuntimeError('Scientific guard failed at original source line 80')
    return F(n, d)


def add(p, q): return tuple(a+b for a, b in zip(p, q))
def sub(p, q): return tuple(a-b for a, b in zip(p, q))
def scale(p, t): return tuple(a*t for a in p)
def dot(p, q): return sum(a*b for a, b in zip(p, q))
def cross(p, q): return p[0]*q[1]-p[1]*q[0]
def length(v): return sqrt_fraction(dot(v, v).rational())
def normal(p): return (p[0]/4, p[1])
def outer_residual(p): return p[0]**2/4+p[1]**2-1
def inner_residual(p): return p[0]**2/F(32,9)+p[1]**2/F(5,9)-1
def area(p): return sum(cross(p[i], p[(i+1)%len(p)]) for i in range(len(p)))/2
def coords(p): return [str(z) for z in p]


def audit_polygon(name, p):
    m = len(p)
    if not (m == 6):
        raise RuntimeError('Scientific guard failed at original source line 99')
    if not (all(outer_residual(x) == 0 for x in p)):
        raise RuntimeError('Scientific guard failed at original source line 100')
    if not (all(p[i] != p[j] for i in range(m) for j in range(i))):
        raise RuntimeError('Scientific guard failed at original source line 101')
    edges = [sub(p[(i+1)%m], p[i]) for i in range(m)]
    # Strong convexity certificate: every other vertex is strictly left of every edge.
    support_cross = []
    edge_evidence = []
    for i, v in enumerate(edges):
        support_cross.append([str(cross(v, sub(p[j], p[i])))
                              for j in range(m) if j not in (i, (i+1)%m)])
        if not (all(cross(v, sub(p[j], p[i])).sign() > 0
                   for j in range(m) if j not in (i, (i+1)%m))):
            raise RuntimeError('Scientific guard failed at original source line 109')
        if not (cross(edges[(i-1)%m], v).sign() > 0):
            raise RuntimeError('Scientific guard failed at original source line 111')
        # Independently use the quadratic obtained by restricting the caustic to
        # the actual finite segment p_i+t*v, not merely to its supporting line.
        alpha = v[0]**2/F(32,9)+v[1]**2/F(5,9)
        beta = 2*(p[i][0]*v[0]/F(32,9)+p[i][1]*v[1]/F(5,9))
        gamma = inner_residual(p[i])
        if not (alpha.sign() > 0 and beta**2-4*alpha*gamma == 0):
            raise RuntimeError('Scientific guard failed at original source line 117')
        t = -beta/(2*alpha)
        if not (t.sign() > 0 and (1-t).sign() > 0):
            raise RuntimeError('Scientific guard failed at original source line 119')
        c = add(p[i], scale(v, t))
        if not (inner_residual(c) == 0):
            raise RuntimeError('Scientific guard failed at original source line 121')
        n = (v[1], -v[0])  # outward/right normal for this CCW side
        h = dot(n, p[i])
        if not (h.sign() > 0):
            raise RuntimeError('Scientific guard failed at original source line 124')
        if not (dot(n, c) == h):
            raise RuntimeError('Scientific guard failed at original source line 125')
        if not (F(32,9)*n[0]**2+F(5,9)*n[1]**2 == h**2):
            raise RuntimeError('Scientific guard failed at original source line 126')
        support_contact = (F(32,9)*n[0]/h, F(5,9)*n[1]/h)
        if not (c == support_contact):
            raise RuntimeError('Scientific guard failed at original source line 128')
        edge_evidence.append({"edge":i, "length":str(length(v)),
                              "caustic_polynomial":[str(alpha),str(beta),str(gamma)],
                              "discriminant":"0", "contact_parameter":str(t),
                              "contact":coords(c), "outward_normal":coords(n),
                              "positive_support":str(h)})
    reflection, cosine, half_squared = [], [], []
    for i, x in enumerate(p):
        uin = scale(edges[(i-1)%m], 1/length(edges[(i-1)%m]))
        uout = scale(edges[i], 1/length(edges[i]))
        n = normal(x)
        inc, out = dot(uin, n), dot(uout, n)
        if not (inc.sign() > 0 and out.sign() < 0):
            raise RuntimeError('Scientific guard failed at original source line 140')
        if not (inc == F(1,3) and out == F(-1,3)):
            raise RuntimeError('Scientific guard failed at original source line 141')
        if not (uout == sub(uin, scale(n, 2*inc/dot(n,n)))):
            raise RuntimeError('Scientific guard failed at original source line 142')
        if not (dot(uin,uin) == 1 and dot(uout,uout) == 1):
            raise RuntimeError('Scientific guard failed at original source line 143')
        # Internal angle is between vectors FROM x to previous/next vertices.
        ci = -dot(uin, uout)
        hi = (1-ci)/2
        if not (hi.sign() > 0 and (1-hi).sign() > 0):
            raise RuntimeError('Scientific guard failed at original source line 147')
        cosine.append(ci.rational())
        half_squared.append(hi.rational())
        reflection.append({"vertex":i, "unit_incoming":coords(uin),
                           "unit_outgoing":coords(uout), "outward_normal":coords(n),
                           "positive_incident_normal_component":str(inc),
                           "negative_departing_normal_component":str(out),
                           "full_reflection_residual":["0","0"]})
    q, dets = [], []
    for i in range(m):
        a, b = normal(p[i]), normal(p[(i+1)%m])
        det = cross(a,b)
        if not (det.sign() > 0):
            raise RuntimeError('Scientific guard failed at original source line 159')
        z = ((b[1]-a[1])/det, (a[0]-b[0])/det)
        if not (dot(a,z) == 1 and dot(b,z) == 1):
            raise RuntimeError('Scientific guard failed at original source line 161')
        q.append(z)
        dets.append(str(det))
    if not (all(cross(sub(q[(i+1)%m],q[i]),sub(q[j],q[i])).sign() > 0
               for i in range(m) for j in range(m) if j not in (i,(i+1)%m))):
        raise RuntimeError('Scientific guard failed at original source line 164')
    a, ap = area(p), area(q)
    if not (a.sign() > 0 and ap.sign() > 0):
        raise RuntimeError('Scientific guard failed at original source line 167')
    product_squared = F(1)
    ext_squared = F(1)
    for h in half_squared:
        product_squared *= h
        ext_squared *= 1-h
    product = sqrt_fraction(product_squared)
    quotient = (ap/a).rational()/product
    ext_product = sqrt_fraction(ext_squared)
    reverse_area = area(list(reversed(p)))
    reverse_outer_area = area(list(reversed(q)))
    if not (reverse_area == -a and reverse_outer_area == -ap):
        raise RuntimeError('Scientific guard failed at original source line 178')
    if not (reverse_outer_area/reverse_area == ap/a):
        raise RuntimeError('Scientific guard failed at original source line 179')
    if not (sum(edge["length"] != "0" for edge in edge_evidence) == 6):
        raise RuntimeError('Scientific guard failed at original source line 180')
    return {"name":name, "vertices":[coords(z) for z in p],
            "all_vertices_on_outer_ellipse":True, "six_distinct_vertices":True,
            "strict_convex_support_crosses":support_cross,
            "finite_segment_tangency":edge_evidence, "reflection":reflection,
            "outer_tangent_vertices":[coords(z) for z in q],
            "outer_tangent_intersection_determinants":dets,
            "area":str(a), "outer_area":str(ap), "area_ratio":str(ap/a),
            "internal_angle_cosines":[str(c) for c in cosine],
            "internal_half_angle_sine_squared":[str(h) for h in half_squared],
            "positive_internal_half_angle_product":str(product),
            "k108":str(quotient), "k108_decimal_for_display":float(quotient),
            "perimeter":str(sum(length(v) for v in edges)),
            "Joachimsthal_incoming_normal_dot":"1/3",
            "area_product":str(a*ap),
            "orientation_reversal_preserves_quotient":True,
            "external_turning_half_angle_product":str(ext_product),
            "external_turning_angle_quotient":str((ap/a).rational()/ext_product)}


# Independent multivariate-polynomial arithmetic to check the direct map identity.
# Dictionary keys are exponents of (t,s), ordered lexicographically for division.
def poly_add(a,b):
    r = dict(a)
    for z,c in b.items():
        r[z] = r.get(z,F(0))+c
        if not r[z]: del r[z]
    return r
def poly_scale(a,c): return {z:x*c for z,x in a.items() if x*c}
def poly_sub(a,b): return poly_add(a,poly_scale(b,-1))
def poly_mul(a,b):
    r = {}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            z=(i+k,j+l)
            r[z] = r.get(z,F(0))+x*y
    return {z:x for z,x in r.items() if x}
def poly_divide(a,b):
    rem, out, rest = dict(a), {}, {}
    lead_b = max(b)
    while rem:
        lead_a = max(rem)
        if all(x>=y for x,y in zip(lead_a,lead_b)):
            term = {tuple(x-y for x,y in zip(lead_a,lead_b)):rem[lead_a]/b[lead_b]}
            out = poly_add(out,term)
            rem = poly_sub(rem,poly_mul(term,b))
        else:
            rest[lead_a] = rem.pop(lead_a)
    return out,rest
def poly_string(p):
    return " + ".join(f"({c})*t^{i}*s^{j}" for (i,j),c in sorted(p.items(),reverse=True)) or "0"


def check_direct_family_identity():
    one={(0,0):F(1)}; t={(1,0):F(1)}; s={(0,1):F(1)}
    t2=poly_mul(t,t); s2=poly_mul(s,s); ts=poly_mul(t,s)
    f=poly_sub(poly_add(poly_scale(poly_add(t2,s2),5),poly_scale(ts,-24)),
               poly_add(poly_mul(t2,s2),one))
    d=poly_sub(poly_scale(one,5),s2)
    k=poly_sub(poly_scale(s,24),poly_mul(t,d))
    denom=poly_sub(poly_scale(poly_mul(d,d),5),poly_mul(k,k))
    numerator=poly_add(poly_scale(poly_mul(poly_mul(t,k),d),24),
                       poly_mul(poly_sub(one,ts),denom))
    factor, remainder=poly_divide(numerator,f)
    if not (not remainder):
        raise RuntimeError('Scientific guard failed at original source line 244')
    if not (poly_mul(factor,f) == numerator):
        raise RuntimeError('Scientific guard failed at original source line 245')
    return {"tangency_biquadratic":poly_string(f),
            "recurrence":"r=24*s/(5-s*s)-t; w=24*r/(5-r*r)-s",
            "identity_numerator":poly_string(numerator),
            "factor_quotient":poly_string(factor), "exact_remainder":"0",
            "consequence":"T^3(t)=-1/t and T^6=id on the entire continuous left-caustic branch"}


def main():
    h=[(Q(2),Q(0)),(Q(F(4,3)),Q(0,F(1,3))),
       (Q(F(-4,3)),Q(0,F(1,3))),(Q(-2),Q(0)),
       (Q(F(-4,3)),Q(0,F(-1,3))),(Q(F(4,3)),Q(0,F(-1,3)))]
    v=[(Q(0,d=2),Q(1,d=2)),(Q(0,F(-4,3),2),Q(F(1,3),d=2)),
       (Q(0,F(-4,3),2),Q(F(-1,3),d=2)),(Q(0,d=2),Q(-1,d=2)),
       (Q(0,F(4,3),2),Q(F(-1,3),d=2)),(Q(0,F(4,3),2),Q(F(1,3),d=2))]
    if not (F(4)-F(32,9) == 1-F(5,9) == F(4,9)):
        raise RuntimeError('Scientific guard failed at original source line 260')
    results = {"scope":"independent mathematical geometry verification of original PR148",
               "original_effort":"1/5", "new_central_proof_search_turns":0,
               "submitted_checker_imports":[], "python":platform.python_version(),
               "PH":audit_polygon("PH",h), "PV":audit_polygon("PV",v),
               "direct_family_identity":check_direct_family_identity()}
    difference=F(results["PH"]["k108"])-F(results["PV"]["k108"])
    if not (difference > 0):
        raise RuntimeError('Scientific guard failed at original source line 267')
    if not (results["PH"]["area_product"] == results["PV"]["area_product"]):
        raise RuntimeError('Scientific guard failed at original source line 268')
    if not (results["PH"]["perimeter"] == results["PV"]["perimeter"]):
        raise RuntimeError('Scientific guard failed at original source line 269')
    results["exact_k108_difference"] = str(difference)
    results["verdict"] = "PASS: exact unequal values on the same primitive convex connected six-period branch"
    out = Path(__file__).resolve().parent/"independent_geometry_results.json"
    out.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"verdict":results["verdict"], "PH_k108":results["PH"]["k108"],
                      "PV_k108":results["PV"]["k108"], "difference":str(difference),
                      "direct_family_identity":results["direct_family_identity"]},indent=2))


if __name__ == "__main__": main()
