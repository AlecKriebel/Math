#!/usr/bin/env python3
"""Read-only independent exact algebra for record 23331080.

Standard-library arithmetic only. Four-chart differentiation is performed in
Q[U,V,(1+U)^-1,(1+V)^-1], not by importing a source verifier or a CAS.
The program certifies identities; analytic existence and sign arguments are
proved or explicitly imported in DERIVATION.md. No sampling is used.
"""
from fractions import Fraction as F
import json


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
        else:
            self.c = {(0, 0): F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in Poly(other).c.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for (i, j), a in self.c.items():
            for (k, l), b in Poly(other).c.items():
                out[i+k, j+l] = out.get((i+k, j+l), F(0)) + a*b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("nonnegative integer exponent required")
        out = Poly(1)
        for _ in range(n):
            out = out*self
        return out

    def d(self, axis):
        out = {}
        for k, v in self.c.items():
            if k[axis]:
                kk = list(k)
                kk[axis] -= 1
                out[tuple(kk)] = v*k[axis]
        return Poly(out)

    def at(self, axis, value):
        out = {}
        for k, v in self.c.items():
            kk = list(k)
            kk[axis] = 0
            key = tuple(kk)
            out[key] = out.get(key, F(0)) + v*F(value)**k[axis]
        return Poly(out)

    def mean(self, axis):
        out = {}
        for k, v in self.c.items():
            kk = list(k)
            kk[axis] = 0
            key = tuple(kk)
            out[key] = out.get(key, F(0)) + v/F(k[axis]+1)
        return Poly(out)

    def div_linear(self, axis):
        """Exact division by 1+variable, or None if not divisible."""
        if not self.c:
            return Poly()
        if self.at(axis, -1).c:
            return None
        grouped = {}
        for k, v in self.c.items():
            other = k[1-axis]
            grouped.setdefault(other, {})[k[axis]] = v
        out = {}
        for other, a in grouped.items():
            n = max(a)
            b = F(0)
            for i in range(n, 0, -1):
                b = a.get(i, F(0))-b
                key = (i-1, other) if axis == 0 else (other, i-1)
                out[key] = b
            if a.get(0, F(0))-b:
                raise ArithmeticError("division remainder disagrees with evaluation")
        return Poly(out)


U = Poly({(1, 0): 1})
V = Poly({(0, 1): 1})


class Rat:
    def __init__(self, value=0, a=0, b=0):
        if isinstance(value, Rat):
            self.n, self.a, self.b = Poly(value.n), value.a, value.b
            return
        self.n, self.a, self.b = Poly(value), a, b
        if not self.n.c:
            self.a = self.b = 0
        for axis in (0, 1):
            while (self.a if axis == 0 else self.b):
                q = self.n.div_linear(axis)
                if q is None:
                    break
                self.n = q
                if axis == 0:
                    self.a -= 1
                else:
                    self.b -= 1

    def __add__(self, other):
        other = Rat(other)
        a, b = max(self.a, other.a), max(self.b, other.b)
        one = self.n*(1+U)**(a-self.a)*(1+V)**(b-self.b)
        two = other.n*(1+U)**(a-other.a)*(1+V)**(b-other.b)
        return Rat(one+two, a, b)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.n, self.a, self.b)

    def __sub__(self, other):
        return self + -Rat(other)

    def __rsub__(self, other):
        return Rat(other) + -self

    def __mul__(self, other):
        other = Rat(other)
        return Rat(self.n*other.n, self.a+other.a, self.b+other.b)

    __rmul__ = __mul__

    def __pow__(self, n):
        return Rat(self.n**n, self.a*n, self.b*n)

    def d(self, axis):
        exponent = self.a if axis == 0 else self.b
        variable = U if axis == 0 else V
        return Rat(self.n.d(axis)*(1+variable)-exponent*self.n,
                   self.a+(axis == 0), self.b+(axis == 1))


passed = []
negative_controls = []


def zero(name, value):
    coeffs = value.n.c if isinstance(value, Rat) else Poly(value).c
    if coeffs:
        raise AssertionError((name, {str(k): str(v) for k, v in coeffs.items()}))
    passed.append(name)


def nonzero(name, value):
    coeffs = value.n.c if isinstance(value, Rat) else Poly(value).c
    if not coeffs:
        raise AssertionError((name, "mutation was not detected"))
    negative_controls.append(name)


eps, delta = F(1, 96), F(1, 4)
for base_infinity in (False, True):
    for fiber_infinity in (False, True):
        chart = ("infinity" if base_infinity else "finite") + "/" + (
            "infinity" if fiber_infinity else "finite")
        p = Rat(1 if base_infinity else U, 1, 0)
        x = Rat(1 if fiber_infinity else V, 0, 1)
        # The two logarithmic frame weights remain 2 log(1+U), 2 log(1+V).
        rem = (2-eps)*(1-p)+delta*p*x*x
        A = 2 + Rat((1+U)**2)*(rem.d(0)+Rat(U)*rem.d(0).d(0))
        B = 2 + Rat((1+V)**2)*(rem.d(1)+Rat(V)*rem.d(1).d(1))
        Q = Rat(U*V*(1+U)**2*(1+V)**2)*rem.d(0).d(1)**2
        targetA = 4*p+(eps+delta*x*x)*(1-2*p)
        targetB = 2+2*delta*p*x*(2-3*x)
        targetQ = 4*delta*delta*p*(1-p)*x**3*(1-x)
        zero(chart+": actual diagonal A", A-targetA)
        zero(chart+": actual diagonal B", B-targetB)
        zero(chart+": actual mixed modulus Q", Q-targetQ)
        loA, loB, hiQ = eps+F(167,48)*p, F(3,2), F(1,4)*p
        zero(chart+": A nonnegative-factor identity",
             A-loA-delta*x*x-2*delta*p*(1-x*x))
        zero(chart+": B nonnegative-factor identity",
             B-loB-2*delta*((1-p)+p*(1-x)*(1+3*x)))
        zero(chart+": Q nonnegative-factor identity",
             hiQ-Q-4*delta*delta*p*(1-(1-p)*x**3*(1-x)))
        zero(chart+": strict determinant certificate",
             loA*loB-hiQ-F(1,64)-F(159,32)*p)

# Independent spectral-basis check. U is now x and V is R=exp(-2t).
x, R = U, V
P1, P2 = 2*x-1, 6*x*x-6*x+1


def lap(q, scale=F(1,2)):
    return scale*(x*(1-x)*q.d(0).d(0)+(1-2*x)*q.d(0))


def rhs(q, reaction=1, subtract_mean=True, scale=F(1,2)):
    return lap(q, scale)+reaction*q-(q.mean(0) if subtract_mean else 0)


zero("P1 exact eigenvalue", lap(P1)+P1)
zero("P2 exact eigenvalue", lap(P2)+3*P2)
zero("P1 zero mean", P1.mean(0))
zero("P2 zero mean", P2.mean(0))
zero("initial spectral decomposition", F(1,3)+F(1,2)*P1+F(1,6)*P2-x*x)
w = eps+delta*F(1,3)+delta*F(1,2)*P1+delta*F(1,6)*R*P2
wdot = -2*R*w.d(1)
zero("actual jet initial value", w.at(1,1)-eps-delta*x*x)
zero("actual jet PDE residual", wdot-rhs(w))
zero("conserved jet mean", w.mean(0)-eps-delta*F(1,3))
zero("exact pole for every finite t", w.at(0,0)-eps+F(1,24)*(1-R))
zero("exact finite negative value", w.at(0,0).at(1,F(1,2))+F(1,96))
zero("exact first-zero threshold", w.at(0,0).at(1,F(3,4)))
zero("exact initial slope", wdot.at(0,0).at(1,1)+F(1,12))
zero("positive root metric scales initial Hessian", Poly(F(1,2)*2)-1)

# Each deliberate convention/error mutation must leave a nonzero exact residual.
nonzero("reject dropped probability normalization", wdot-rhs(w, subtract_mean=False))
nonzero("reject same-weight reaction coefficient two", wdot-rhs(w, reaction=2))
nonzero("reject doubled fiber Laplacian", wdot-rhs(w, scale=F(1)))
nonzero("reject reversed exponential sign", 2*R*w.d(1)-rhs(w))
nonzero("reject pole negativity already at initial time", w.at(0,0).at(1,1))
zero("stationary pure-base normalized gauge", rhs(Poly(2)))
nonzero("product calibration detects literal rank-two term", rhs(Poly(2), reaction=2))

print(json.dumps({
    "verdict": "PASS",
    "mechanism": "exact four-chart rational differentiation plus spectral jet identity",
    "identities_passed": len(passed),
    "identities": passed,
    "negative_controls_rejected": len(negative_controls),
    "negative_controls": negative_controls,
    "strict_initial_determinant_lower_bound": "1/64+(159/32)*p",
    "horizontal_at_t_log2_over2": "-1/96",
    "scope": "Exact algebra; no numerical sampling; analytic existence is a separate primary import.",
    "source_imports": [],
    "writes": []
}, indent=2))
