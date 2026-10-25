"""Independent analytic-lane integer-polynomial reconstruction.

Written before any deposited checker or prior audit was inspected. Standard
library only; no deposited code is imported or executed, and no network used.
Polynomials use the two indeterminates s,t with integer coefficients.
"""
from datetime import datetime, timezone
import json


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            self.d = dict(terms.d)
        elif isinstance(terms, int):
            self.d = {(0, 0): terms} if terms else {}
        else:
            self.d = {k: v for k, v in terms.items() if v}

    def __add__(self, other):
        out = dict(self.d)
        for k, v in Poly(other).d.items():
            out[k] = out.get(k, 0) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        out = {}
        for (i, j), a in self.d.items():
            for (k, l), b in Poly(other).d.items():
                term = (i + k, j + l)
                out[term] = out.get(term, 0) + a * b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert n >= 0 and isinstance(n, int)
        out = Poly(1)
        for _ in range(n):
            out = out * self
        return out

    def evaluate(self, s_value, t_value):
        return sum(a * s_value**i * t_value**j for (i, j), a in self.d.items())


s = Poly({(1, 0): 1})
t = Poly({(0, 1): 1})
r = s + 1
checks = []


def equal(name, left, right):
    residual = Poly(left) - Poly(right)
    if residual.d:
        raise AssertionError((name, residual.d))
    checks.append(name)


def det(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


# For p=xy^2-z^3, at (r,1,1): n=grad p, B=Hess p.
# A=Dp[h], b=Hess(p)h, C=D(Hess p)[h], h=(t^3,1,t).
# Direct chain rule for -log p-log z gives this M=-s^3 D^3 f[h].
n = [Poly(1), 2*r, Poly(-3)]
B = [[0, 2, 0], [2, 2*r, 0], [0, 0, -6]]
A = t**3 + 2*r - 3*t
b = [Poly(2), 2*t**3 + 2*r, -6*t]
C = [[0, 2, 0], [2, 2*t**3, 0], [0, 0, -6*t]]
M = [[2*A*n[i]*n[j] - s*(b[i]*n[j]+n[i]*b[j]+A*B[i][j])
      +s**2*C[i][j]+(2*s**3*t if i == j == 2 else 0)
      for j in range(3)] for i in range(3)]
literal = [
    [2*(t-1)**2*(t+2),
     2*(t-1)*(2*t**2+2*t-1-3*r),
     6*(t-1)*(r-t**2-t+1)],
    [None, 4*r**3+12*r**2-18*r**2*t+6*r*t**3-6*r*t+2*t**3,
     12*r**2*t-18*r**2-6*r*t**3+24*r*t-6*r-6*t**3],
    [None, None, 6*(r+2)*t**3+2*(r**3-6*r**2-18*r-4)*t+12*r*(r+2)],
]
for i in range(3):
    for j in range(i, 3):
        equal(f"M{i+1}{j+1} direct chain rule", M[i][j], literal[i][j])
        equal(f"M{i+1}{j+1} symmetry", M[i][j], M[j][i])
P = 2*(t+2)*s**2-3*(t-1)*(3*t+5)*s+3*(t-1)**2*(t+2)**2
R = (t+2)*(2*t*s**2-3*(t-1)*(3*t+1)*s+3*(t-1)**2*(t**2+4*t+1))
equal("second leading minor", M[0][0]*M[1][1]-M[0][1]**2, 4*s*(t-1)**2*P)
equal("determinant", det(M), 8*s**4*(t-1)**2*R)
equal("P square identity", 8*(t+2)*P,
      (4*(t+2)*s-3*(t-1)*(3*t+5))**2+3*(t-1)**2*(8*t**3+21*t**2+6*t-11))
equal("R square identity without division", 8*t*R,
      (t+2)*((4*t*s-3*(t-1)*(3*t+1))**2+3*(t-1)**3*(8*t**2+13*t+3)))
equal("P remainder shift", 8*(t+1)**3+21*(t+1)**2+6*(t+1)-11,
      8*t**3+45*t**2+72*t+24)
# t=1 endpoint checked as a polynomial in s, by replacing t exponents.
def at_t(poly, value):
    out = {}
    for (i, j), a in Poly(poly).d.items():
        out[(i, 0)] = out.get((i, 0), 0) + a*value**j
    return Poly(out)
endpoint = [[0,0,0],[0,2*s**2*(2*r+1),-6*s**2],[0,-6*s**2,2*s**2*(r+2)]]
for i in range(3):
    for j in range(3):
        equal(f"t=1 entry {i},{j}", at_t(M[i][j], 1), endpoint[i][j])
equal("t=1 lower block determinant", (2*r+1)*(r+2)-9, s*(2*r+7))
# Separate h=e_x chain-rule construction, no t->infinity assumption.
ae = [1,2,-3]
be = [0,1,-1]
bx = [0,2,0]
Cx = [[0,0,0],[0,2,0],[0,0,0]]
Mx = [[2*n[i]*n[j]-s*(bx[i]*n[j]+n[i]*bx[j]+B[i][j])+s**2*Cx[i][j]
       for j in range(3)] for i in range(3)]
for i in range(3):
    for j in range(3):
        equal(f"e_x Gram entry {i},{j}", Mx[i][j], 2*ae[i]*ae[j]+6*s*be[i]*be[j])
M0 = [[entry for entry in row] for row in M]
M0[2][2] = M0[2][2]-2*s**3*t
assert det(M0).evaluate(4, 2) == -24576
checks.append("unaugmented -log p counterexample determinant exact")

# Nonhyperbolicity quadratic discriminant, with s=a,t=b here.
equal("nonhyperbolicity quadratic discriminant", (s+2*t)**2-4*(s**2+s*t+t**2), -3*s**2)
print(json.dumps({"utc": datetime.now(timezone.utc).isoformat(),
                  "method": "independently written sparse integer polynomial arithmetic",
                  "all_passed": True, "count": len(checks), "checks": checks}, indent=2))
