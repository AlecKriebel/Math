"""Audit control: exact construction separation, not a general constancy proof.

Standard library only. No submitted candidate code or meromorphic identities.
Arithmetic is Q(sqrt(5), sqrt(21)); basis is 1,sqrt(5),sqrt(21),sqrt(105).
"""
from fractions import Fraction as F
from pathlib import Path
import json


class K:
    def __init__(self, x=0):
        self.c = x.c if isinstance(x, K) else ((F(x), F(0), F(0), F(0)) if not isinstance(x, tuple) else tuple(map(F, x)))

    def __add__(self, y):
        y = K(y)
        return K(tuple(a+b for a, b in zip(self.c, y.c)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-a for a in self.c))

    def __sub__(self, y):
        return self + -K(y)

    def __rsub__(self, y):
        return K(y) + -self

    def __mul__(self, y):
        y = K(y)
        out = [F(0)]*4
        for i in range(4):
            for j in range(4):
                common = i & j
                factor = (5 if common & 1 else 1)*(21 if common & 2 else 1)
                out[i ^ j] += self.c[i]*y.c[j]*factor
        return K(tuple(out))

    __rmul__ = __mul__

    def conj(self, mask):
        return K(tuple((-a if (i & mask).bit_count() % 2 else a) for i, a in enumerate(self.c)))

    def inv(self):
        other = self.conj(1)*self.conj(2)*self.conj(3)
        norm = self*other
        assert not any(norm.c[1:]) and norm.c[0]
        return K(tuple(x/norm.c[0] for x in other.c))

    def __truediv__(self, y):
        return self*K(y).inv()

    def __rtruediv__(self, y):
        return K(y)*self.inv()

    def __pow__(self, n):
        assert n >= 0
        out = K(1)
        for _ in range(n):
            out *= self
        return out

    def __eq__(self, y):
        return self.c == K(y).c

    def record(self):
        return [str(x) for x in self.c]


def sub(p, q):
    return tuple(x-y for x, y in zip(p, q))


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def dot(p, q):
    return sum(x*y for x, y in zip(p, q))


def tangent_intersection(p, q):
    # Tangent to x^2/21+y^2/16=1: p_x*x/21+p_y*y/16=1.
    a, b, c, d = p[0]/21, p[1]/16, q[0]/21, q[1]/16
    delta = a*d-b*c
    assert delta != 0
    return ((d-b)/delta, (a-c)/delta)


def area(vertices):
    return sum(det(p, vertices[(i+1) % len(vertices)]) for i, p in enumerate(vertices))/2


def inverse_area(vertices, focus):
    points = []
    for p in vertices:
        v = sub(p, focus)
        distance2 = dot(v, v)
        assert distance2 != 0
        points.append(tuple(x/distance2 for x in v))
    return area(points)  # Translation by the focus does not change area.


def verify_family(vertices, lengths):
    caustic_a2, caustic_b2 = F(189, 25), F(64, 25)
    outer = []
    for i, p in enumerate(vertices):
        q, prev = vertices[(i+1) % 3], vertices[(i-1) % 3]
        assert p[0]**2/21+p[1]**2/16 == 1
        edge = sub(q, p)
        assert dot(edge, edge) == lengths[i]**2
        normal = (p[0]/21, p[1]/16)
        incoming = tuple(x/lengths[(i-1) % 3] for x in sub(p, prev))
        outgoing = tuple(x/lengths[i] for x in edge)
        assert det(sub(incoming, outgoing), normal) == 0
        line_a, line_b = -edge[1], edge[0]
        line_c = line_a*p[0]+line_b*p[1]
        assert caustic_a2*line_a**2+caustic_b2*line_b**2 == line_c**2
        outer.append(tangent_intersection(p, q))
    for q in outer:
        assert q[0]**2/F(175, 3)+q[1]**2/100 == 1
    return outer


def main():
    sqrt5, sqrt21 = K((0, 1, 0, 0)), K((0, 0, 1, 0))
    horizontal = [(sqrt21, K(0)), (-F(3, 5)*sqrt21, K(F(16, 5))), (-F(3, 5)*sqrt21, K(-F(16, 5)))]
    vertical = [(K(0), K(4)), (K(-F(21, 5)), K(-F(8, 5))), (K(F(21, 5)), K(-F(8, 5)))]
    cases = []
    for name, vertices, lengths in [('H', horizontal, [F(8), F(32, 5), F(8)]), ('V', vertical, [F(7), F(42, 5), F(7)])]:
        outer = verify_family(vertices, lengths)
        original_areas = [inverse_area(vertices, (e*sqrt5, K(0))) for e in [1, -1]]
        outer_areas = [inverse_area(outer, (e*sqrt5, K(0))) for e in [1, -1]]
        assert original_areas[0]*original_areas[1] == F(1, 324)
        assert outer_areas[0]*outer_areas[1] == F(1, 3600)
        assert all(o == F(3, 10)*a for o, a in zip(outer_areas, original_areas))
        assert original_areas[0]*original_areas[1] != outer_areas[0]*outer_areas[1]
        cases.append({'phase': name, 'outer_vertices': [[x.record(), y.record()] for x, y in outer], 'original_inverse_areas': [x.record() for x in original_areas], 'outer_inverse_areas': [x.record() for x in outer_areas], 'original_product': '1/324', 'outer_product': '1/3600', 'outer_over_original_ratio_in_these_two_phases': '3/10'})
    out = {'status': 'all exact assertions passed', 'arithmetic': 'Q(sqrt(5),sqrt(21)), coefficient basis 1,sqrt(5),sqrt(21),sqrt(105)', 'ellipse_squared_axes': ['21', '16'], 'caustic_squared_axes': ['189/25', '64/25'], 'lambda': '336/25', 'outer_squared_axes': ['175/3', '100'], 'outer_axis_difference': '-125/3', 'original_focus_c_squared': '5', 'cases': cases, 'limitation': 'Two exact phases separate constructions; they are not a proof of constancy of the ratio or either product over a family, and not a prior literature theorem.'}
    Path(__file__).with_name('EXACT_SCOPE_SEPARATION.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
