"""Independent, optimization-safe finite checks for the local-action counterexample.

These check exact rational and Artinian-ring identities only. The proof of the
power-series module, cohomology, and naturality claims is in INDEPENDENT_AUDIT.md.
No third-party packages, floating point, network, or external writes are used.
"""
import argparse
import json
import sys


def require(ok, label):
    if not ok:
        raise ValueError(label)


def gf_mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7  # u^2 + u + 1
    return c


def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return tuple(a) if a else (0,)


def pa(a, b):
    return trim((a[i] if i < len(a) else 0) ^
                (b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))


def pm(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] ^= gf_mul(x, y)
    return trim(c)


def pp(a, n):
    c = (1,)
    for _ in range(n):
        c = pm(c, a)
    return c


def pd(a):
    return trim(a[i] if i & 1 else 0 for i in range(1, len(a)))


class Rat:
    """Exact rational function over F4; equality by polynomial cross products."""
    def __init__(self, n=(0,), d=(1,)):
        self.n, self.d = trim(n), trim(d)
        require(self.d != (0,), "zero denominator")

    def __add__(self, other):
        return Rat(pa(pm(self.n, other.d), pm(other.n, self.d)),
                   pm(self.d, other.d))

    def __mul__(self, other):
        return Rat(pm(self.n, other.n), pm(self.d, other.d))

    def __truediv__(self, other):
        return Rat(pm(self.n, other.d), pm(self.d, other.n))

    def __pow__(self, n):
        return Rat(pp(self.n, n), pp(self.d, n))

    def __eq__(self, other):
        return pm(self.n, other.d) == pm(other.n, self.d)

    def sub(self, other):
        def evaluate(p):
            r = Rat()
            for x in reversed(p):
                r = r * other + Rat((x,))
            return r
        return evaluate(self.n) / evaluate(self.d)

    def derivative(self):
        return Rat(pa(pm(pd(self.n), self.d), pm(self.n, pd(self.d))),
                   pp(self.d, 2))


def aa(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def am(a, b):
    c = [0, 0, 0]
    for i in range(3):
        for j in range(3-i):
            c[i+j] ^= gf_mul(a[i], b[j])
    return tuple(c)


def mm(a, b):
    return [[aa(am(a[i][0], b[0][j]), am(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def sm(s, a):
    return [[am(s, x) for x in r] for r in a]


def verify(mutant):
    records = []
    one, x = Rat((1,)), Rat((0, 1))
    u = 2
    require(gf_mul(u, u ^ 1) == 1, "F4 defining relation")
    for a in range(4):
        for b in range(4):
            ra = x / (one + Rat((a,)) * x)
            rb = x / (one + Rat((b,)) * x)
            rab = x / (one + Rat((a ^ b,)) * x)
            require(ra.sub(rb) == rab, "faithful additive-action composition")
    records.append("all 16 group-composition identities")
    y = x**2 / (one+x)
    rho1 = x / (one+x)
    rhou = x / (one+Rat((u,))*x)
    require(y.sub(rho1) == y, "N-invariance of quotient coordinate")
    claimed = y if mutant == "quotient_action" else y/(one+y)
    require(y.sub(rhou) == claimed, "induced Q-action")
    require(y.derivative() == x**2 / ((one+x)**2), "quotient derivative")
    records.append("quotient invariance, induced action, derivative")
    sigma = x/(one+x)
    z = x**2/(one+x)
    require(z.sub(sigma) == z, "second quotient invariant")
    weight = one+x if mutant == "derivation_weight" else (one+x)**2
    require(weight * x.sub(sigma) + x == x**2, "coboundary of y")
    for n in range(9):
        h = z**n
        require(weight * (x*h).sub(sigma) + x*h == x**2*h,
                "exact rational coboundary identity, monomial " + str(n))
        require(weight * (x**2*h).sub(sigma) == x**2*h,
                "exact rational invariant identity, monomial " + str(n))
    records.append("exact rational invariant and coboundary identities for z^0 through z^8")
    zero, one_a, e, e2 = (0,0,0), (1,0,0), (0,1,0), (0,0,1)
    m = [[one_a, e], [one_a, one_a]]
    target = e if mutant == "parameter_shift" else aa(e,e2)
    mp = [[one_a, target], [one_a, one_a]]
    c = [[aa(one_a,e), zero if mutant == "conjugator_translation" else e],
         [zero,one_a]]
    scale = one_a if mutant == "projective_scalar" else aa(one_a,e)
    require(mm(mp,c) == sm(scale, mm(c,m)), "projective conjugacy")
    require(mm(m,m) == sm(aa(one_a,e), [[one_a,zero],[zero,one_a]]),
            "involution")
    records.append("conjugacy and involution in F4[e]/e^3")
    def j(a):
        # e -> e+e^2 fixes coefficients; j(c0+c1 e+c2 e^2)
        return a if mutant == "fixed_ring" else (a[0], a[1], a[2]^a[1])
    fixed = []
    for a0 in range(4):
        for a1 in range(4):
            for a2 in range(4):
                a = (a0,a1,a2)
                require(j(j(a)) == a, "j involutive")
                require((j(a) == a) == (a1 == 0), "j fixed-ring linear coefficient")
                if j(a) == a:
                    fixed.append(a)
    require(len(fixed) == 16, "fixed-ring cardinality")
    records.append("all 64 elements: j-fixed iff linear coefficient is zero")
    return {"ok": True, "optimization_level": sys.flags.optimize,
            "mutant": mutant, "checks": records,
            "limitation": "Finite identities support but do not prove the formal power-series or functor arguments."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutant", choices=["none", "quotient_action", "derivation_weight",
                        "parameter_shift", "conjugator_translation", "projective_scalar", "fixed_ring"],
                        default="none")
    args = parser.parse_args()
    try:
        result = verify(args.mutant)
    except ValueError as exc:
        print(json.dumps({"ok": False, "optimization_level": sys.flags.optimize,
                          "mutant": args.mutant, "failure": str(exc)}))
        sys.exit(1)
    print(json.dumps(result, indent=2))
