"""Independent physical-vertex controls; stdlib only; stdout JSON only."""
from fractions import Fraction
import json

RAD = (2, 3, 5)


class K:
    def __init__(self, x=0):
        self.v = tuple(x) if isinstance(x, (tuple, list)) else (Fraction(x),) + (Fraction(0),) * 7

    def __add__(self, other):
        other = other if isinstance(other, K) else K(other)
        return K(tuple(a+b for a, b in zip(self.v, other.v)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-a for a in self.v))

    def __sub__(self, other):
        return self + (-other if isinstance(other, K) else -K(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, K) else K(other)
        z = [Fraction(0)] * 8
        for i, a in enumerate(self.v):
            for j, b in enumerate(other.v):
                factor = 1
                for k, rad in enumerate(RAD):
                    if i & j & (1 << k):
                        factor *= rad
                z[i ^ j] += a*b*factor
        return K(tuple(z))

    __rmul__ = __mul__

    def inverse(self):
        cols = [(self*K(tuple(Fraction(int(j == i)) for j in range(8)))).v for i in range(8)]
        rows = [[cols[j][i] for j in range(8)] + [Fraction(int(i == 0))] for i in range(8)]
        for j in range(8):
            pivot = next((i for i in range(j, 8) if rows[i][j]), None)
            if pivot is None:
                raise ZeroDivisionError("zero field element")
            rows[j], rows[pivot] = rows[pivot], rows[j]
            denom = rows[j][j]
            rows[j] = [x/denom for x in rows[j]]
            for i in range(8):
                if i != j:
                    factor = rows[i][j]
                    rows[i] = [a-factor*b for a, b in zip(rows[i], rows[j])]
        return K(tuple(rows[i][-1] for i in range(8)))

    def __truediv__(self, other):
        return self*(other if isinstance(other, K) else K(other)).inverse()

    def __eq__(self, other):
        other = other if isinstance(other, K) else K(other)
        return self.v == other.v

    def serial(self):
        return {str(i): str(v) for i, v in enumerate(self.v) if v}


def root(bit):
    return K(tuple(Fraction(int(i == 1 << bit)) for i in range(8)))


def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def invert(vertices, focus, rho=1):
    result = []
    for x, y in vertices:
        u, v = x-focus[0], y-focus[1]
        d = u*u+v*v
        result.append((rho*rho*u/d+focus[0], rho*rho*v/d+focus[1]))
    return result


def area(vertices):
    return sum((cross(p, vertices[(i+1) % len(vertices)]) for i, p in enumerate(vertices)), K())/2


def pair(vertices, c, rho=1):
    return [area(invert(vertices, (sign*c, K()), rho)) for sign in (1, -1)]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    s2, s3, s5 = root(0), root(1), root(2)
    h = [(2*s2, K()), (-4*s2/3, K(Fraction(5, 3))), (-4*s2/3, K(Fraction(-5, 3)))]
    v = [(K(), s5), (K(Fraction(-8, 3)), -s5/3), (K(Fraction(8, 3)), -s5/3)]
    results = {}
    for label, vertices in (("H", h), ("V", v)):
        for x, y in vertices:
            require(x*x/8+y*y/5 == 1, label+" outer ellipse")
        areas = pair(vertices, s3)
        require(areas[0]*areas[1] == Fraction(5, 256), label+" product")
        if label == "H":
            require(areas[0] == s2/10-s3/80, "H plus area")
            require(areas[1] == s2/10+s3/80, "H minus area")
        else:
            require(areas[0] == s5/16 and areas[1] == s5/16, "V areas")
        reverse = pair(list(reversed(vertices)), s3)
        require(reverse[0] == -areas[0] and reverse[1] == -areas[1], "reversal")
        for repeat in (2, 3, 4):
            repeated = pair(vertices*repeat, s3)
            require(repeated[0]*repeated[1] == areas[0]*areas[1]*(repeat*repeat), "repetition")
        scaled = pair([(3*x, 3*y) for x, y in vertices], 3*s3)
        require(scaled[0]*scaled[1] == areas[0]*areas[1]/81, "physical scaling")
        radius = pair(vertices, s3, rho=2)
        require(radius[0]*radius[1] == areas[0]*areas[1]*256, "radius scaling")
        results[label] = {"areas": [q.serial() for q in areas], "product": (areas[0]*areas[1]).serial()}
    print(json.dumps({"status": "pass", "field_basis": "sqrt(2)^i sqrt(3)^j sqrt(5)^k with bit mask i+2j+4k", "results": results, "covariance": {"reversal": True, "repeat": [2, 3, 4], "physical_scale": 3, "inversion_radius": 2}}, sort_keys=True))


if __name__ == "__main__":
    main()
