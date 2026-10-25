from fractions import Fraction as F
from functools import reduce

# Exact polynomial ring in a,b,c,d; no external dependencies.
class P:
    def __init__(self, t=0):
        pairs = t.items() if isinstance(t, dict) else [((0, 0, 0, 0), t)]
        self.t = {k: F(v) for k, v in pairs if v}

    def __add__(self, o):
        o = o if isinstance(o, P) else P(o)
        r = self.t.copy()
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return P(r)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        o = o if isinstance(o, P) else P(o)
        r = {}
        for k, v in self.t.items():
            for l, w in o.t.items():
                m = tuple(x + y for x, y in zip(k, l))
                r[m] = r.get(m, 0) + v * w
        return P(r)

    __rmul__ = __mul__

    def __eq__(self, o):
        return self.t == (o.t if isinstance(o, P) else P(o).t)

    def __repr__(self):
        return str(sorted((k, str(v)) for k, v in self.t.items()))


def var(i):
    return P({tuple(int(j == i) for j in range(4)): 1})


a, b, c, d = [var(i) for i in range(4)]
delta = a * d - b * c
# sl2 basis H,E,F; source H,E,Z with [H,E]=2E.
# j1(H,E,Z)=(H,E,0); j2(H,E,Z)=(0,0,F).
# p=[[a,b],[c,d]], delta=1. Columns are the left-trivialized fields.
B = [[a * d + b * c, c * d, P(0)],
     [2 * b * d, d * d, P(0)],
     [-2 * a * c, -c * c, P(-1)]]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


f = det3(B)
print('determinant polynomial (a,b,c,d exponents; coefficient): ' + repr(f))
assert f + delta * d * d == P(0)
print('PASS exact polynomial identity det(B)=-d^2*(ad-bc); on SL2, det(B)=-d^2')


def add(A, B):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(A, B))


def scale(k, A):
    return tuple(tuple(k * x for x in row) for row in A)


def mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def comm(A, B):
    return add(mul(A, B), scale(-1, mul(B, A)))


H = ((1, 0), (0, -1))
E = ((0, 1), (0, 0))
FF = ((0, 0), (1, 0))
O = ((0, 0), (0, 0))
j1, j2 = [H, E, O], [O, O, FF]
for j in [j1, j2]:
    for i in range(3):
        for k in range(3):
            rhs = (scale(2, j[1]) if (i, k) == (0, 1)
                   else scale(-2, j[1]) if (i, k) == (1, 0) else O)
            assert comm(j[i], j[k]) == rhs
print('PASS both maps are Lie homomorphisms on all basis pairs')
print('source_trace_ad_H=2; source is nonunimodular')


def ev(p, vals):
    return sum(v * reduce(lambda x, y: x * y,
                          (F(z) ** k for z, k in zip(vals, key)), F(1))
               for key, v in p.t.items())


identity, weyl = (1, 0, 0, 1), (0, -1, 1, 0)
assert ev(delta, identity) == 1 and ev(delta, weyl) == 1
assert ev(f, identity) == -1 and ev(f, weyl) == 0
print('PASS f(identity)=-1 but f(Weyl)=0 for actual SL2 points')
print('VERIFIED DROPPED-HYPOTHESIS EXAMPLE: initial transversality need not be global without unimodularity')
print('This checks the mechanism; it is not a counterexample under the target hypotheses.')
