#!/usr/bin/env python3
"""Exact independent finite controls. Standard library only; no original imports.

These checks test formulas and detect selected mutations. They do not prove
smooth global existence, which is established in FULL_REPORT.md.
"""
from fractions import Fraction as F
from itertools import product, permutations
import json


class P:
    def __init__(self, n, terms=None):
        self.n = n
        self.t = {tuple(a): F(c) for a, c in (terms or {}).items() if c}

    @staticmethod
    def const(n, c):
        return P(n, {(0,) * n: c})

    @staticmethod
    def var(n, i):
        a = [0] * n
        a[i] = 1
        return P(n, {tuple(a): 1})

    def __add__(self, other):
        if not isinstance(other, P):
            other = P.const(self.n, other)
        assert self.n == other.n
        d = dict(self.t)
        for a, c in other.t.items():
            d[a] = d.get(a, F(0)) + c
        return P(self.n, d)

    __radd__ = __add__

    def __neg__(self):
        return P(self.n, {a: -c for a, c in self.t.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, P):
            return P(self.n, {a: c * other for a, c in self.t.items()})
        assert self.n == other.n
        d = {}
        for a, c in self.t.items():
            for b, e in other.t.items():
                k = tuple(i + j for i, j in zip(a, b))
                d[k] = d.get(k, F(0)) + c * e
        return P(self.n, d)

    __rmul__ = __mul__

    def __pow__(self, k):
        ans = P.const(self.n, 1)
        for _ in range(k):
            ans = ans * self
        return ans

    def d(self, i):
        out = {}
        for a, c in self.t.items():
            if a[i]:
                b = list(a)
                b[i] -= 1
                out[tuple(b)] = c * a[i]
        return P(self.n, out)

    def at(self, point):
        return sum(c * product_numbers(v ** k for v, k in zip(point, a))
                   for a, c in self.t.items())

    def compose(self, ps):
        assert len(ps) == self.n
        out = P.const(ps[0].n, 0)
        for a, c in self.t.items():
            term = P.const(ps[0].n, c)
            for q, k in zip(ps, a):
                term = term * q ** k
            out = out + term
        return out

    def derivative_at(self, indices, point=None):
        out = self
        for i in indices:
            out = out.d(i)
        return out.at(point or (F(0),) * self.n)

    def zero(self):
        return not self.t


def product_numbers(seq):
    ans = F(1)
    for a in seq:
        ans *= a
    return ans


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [v / z for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [u - z * v for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** c * a[0][c] * determinant([
        row[:c] + row[c+1:] for row in a[1:]]) for c in range(len(a)))


def solve(a, b):
    m = [[F(v) for v in row] + [F(z)] for row, z in zip(a, b)]
    n = len(m)
    for j in range(n):
        k = next(i for i in range(j, n) if m[i][j])
        m[j], m[k] = m[k], m[j]
        z = m[j][j]
        m[j] = [v/z for v in m[j]]
        for i in range(n):
            if i != j:
                z = m[i][j]
                m[i] = [u-z*v for u,v in zip(m[i],m[j])]
    return [row[-1] for row in m]


checks = {}
u, v = P.var(2, 0), P.var(2, 1)
lam = 2 + u + 2*v + u*u + v*v
g = [[lam if i == j else P.const(2, 0) for j in range(2)] for i in range(2)]
Cval = {0: F(2), 1: F(-1), 2: F(3), 3: F(-4)}
C = lambda i,j,k: Cval[i+j+k]
G0 = [[p.at((0,0)) for p in row] for row in g]
dg = lambda k,i,j: g[i][j].derivative_at((k,))
L = lambda i,j,k: (dg(i,j,k)+dg(j,i,k)-dg(k,i,j))/2
Gamma = lambda i,j,k: L(i,j,k)-C(i,j,k)/2
Gamma_star = lambda i,j,k: L(i,j,k)+C(i,j,k)/2
Q = lambda i,j,k: dg(k,i,j)+Gamma(i,j,k)
triples = list(product(range(2), repeat=3))
assert all(Q(*a) == Q(*b) for a in triples for b in permutations(a))
assert all(dg(i,j,k) == Gamma(i,j,k)+Gamma_star(i,k,j) for i,j,k in triples)
assert all(dg(i,j,k)-Gamma(i,j,k)-Gamma(i,k,j) == C(i,j,k) for i,j,k in triples)
checks['connection_algebra'] = {'ordered_triples': 8, 'pass': True,
    'curved_metric': 'g=(2+u+2v+u^2+v^2)(du^2+dv^2)',
    'Gaussian_curvature_at_origin': '-3/16'}

# A nonlinear chart change with nonzero second and third derivatives.
X = [2*u+v+u*u+2*u*v-v*v+u**3,
     -u+v+3*u*u-u*v+v*v+2*u*u*v]
A = [[X[i].derivative_at((a,)) for a in range(2)] for i in range(2)]
assert determinant(A) == 3
qx = P.const(2,0)
for i,j in product(range(2),repeat=2):
    qx += F(1,2)*G0[i][j]*[u,v][i]*[u,v][j]
for i,j,k in triples:
    qx += F(1,6)*Q(i,j,k)*[u,v][i]*[u,v][j]*[u,v][k]
qy = qx.compose(X)
gy = [[sum(X[i].d(a)*X[j].d(b)*g[i][j].compose(X)
           for i,j in product(range(2),repeat=2)) for b in range(2)] for a in range(2)]
def gamma_y(a,b,c):
    return (sum(A[i][a]*A[j][b]*A[k][c]*Gamma(i,j,k) for i,j,k in triples)
        +sum(G0[i][k]*X[i].derivative_at((a,b))*A[k][c]
             for i,k in product(range(2),repeat=2)))
assert qy.at((0,0)) == 0
assert all(qy.derivative_at((a,)) == 0 for a in range(2))
assert all(qy.derivative_at((a,b)) == gy[a][b].at((0,0))
           for a,b in product(range(2),repeat=2))
assert all(qy.derivative_at((a,b,c)) == gy[a][b].derivative_at((c,))+gamma_y(a,b,c)
           for a,b,c in triples)
# Omitting the inhomogeneous connection transformation must be detected.
assert any(qy.derivative_at((a,b,c)) != gy[a][b].derivative_at((c,))+
           sum(A[i][a]*A[j][b]*A[k][c]*Gamma(i,j,k) for i,j,k in triples)
           for a,b,c in triples)
checks['nonlinear_coordinate_compatibility'] = {'pass': True, 'Jacobian_determinant': '3',
    'ordered_third_derivatives_checked': 8, 'omitted_connection_term_rejected': True}

# Normal-coordinate cubic: -C(v,v,v)/12 gives third derivative -C/2.
normal_cubic = sum(-F(1,12)*C(i,j,k)*[u,v][i]*[u,v][j]*[u,v][k]
                   for i,j,k in triples)
assert all(normal_cubic.derivative_at(a) == -C(*a)/2 for a in triples)
wrong_cubic = normal_cubic*2
assert any(wrong_cubic.derivative_at(a) != -C(*a)/2 for a in triples)
checks['normal_cubic_factor'] = {'pass': True, 'factor_2_mutation_rejected': True}

# Scalar jet feature ranks. All calculations use exact rational arithmetic.
def indices(n, degree):
    return sorted((a for a in product(range(degree+1), repeat=n) if sum(a)<=degree),
                  key=lambda a:(sum(a),a))
features_exp = indices(5,3)
jet_exp = indices(2,3)
e = [u, v, u*u+v*v, u*v, u**3+v**3]
def monomial(coords, alpha):
    out=P.const(coords[0].n,1)
    for p,k in zip(coords,alpha):
        out=out*p**k
    return out
features=[monomial(e,a) for a in features_exp]
def jet_matrix(fs, point):
    return [[p.derivative_at(tuple(i for i,k in enumerate(a) for _ in range(k)),point)
             for p in fs] for a in jet_exp]
ranks=[]
for point in [(F(0),F(0)),(F(1,2),F(-1,3)),(F(5),F(-7))]:
    z=rank(jet_matrix(features,point)); assert z==10
    ranks.append({'point':[str(x) for x in point],'rank':z})
linear_e=[u,v,P.const(2,0),P.const(2,0),P.const(2,0)]
quadratic_features=[monomial(linear_e,a) for a in indices(5,2)]
assert rank(jet_matrix(quadratic_features,(F(0),F(0))))==6
assert rank(jet_matrix(features[1:],(F(0),F(0))))==9
checks['scalar_3jet_feature_rank']={'pass':True,'ambient_K':5,'N':len(features),
    'jet_dimension':len(jet_exp),'ranks':ranks,
    'degree_2_linear_embedding_rank':6,'constant_removed_origin_rank':9}

# An exact smooth one-dimensional Lauritzen pair, checked as polynomial identities.
t=P.var(1,0); one=P.const(1,1)
metric=one+t*t; cubic=2+2*t**3
gamma=metric.d(0)*F(1,2)-cubic*F(1,2)
qq=metric.d(0)+gamma
a=[metric*t*t*F(1,2)-qq*t**3*F(1,6),
   -metric*t+qq*t*t*F(1,2), metric*F(1,2)-qq*t*F(1,2),qq*F(1,6)]
phi=[-p for p in a]; f=[one,t,t*t,t**3]
dot=lambda p,q:sum(x*y for x,y in zip(p,q))
assert dot(a,f).zero()
assert dot(a,[p.d(0) for p in f]).zero()
assert (dot(a,[p.d(0).d(0) for p in f])-metric).zero()
assert (dot(a,[p.d(0).d(0).d(0) for p in f])-qq).zero()
assert (dot([p.d(0) for p in f],[p.d(0) for p in phi])-metric).zero()
assert (dot([p.d(0).d(0) for p in f],[p.d(0) for p in phi])-gamma).zero()
assert not (dot([p.d(0) for p in f],[p.d(0) for p in a])-metric).zero()
checks['differentiated_pair_identities']={'pass':True,'g':'1+t^2','C':'2+2t^3',
    'Gamma_lower':'t-1-t^3','phi_sign_mutation_rejected':True}

# Explicit local Hessian extension at a nontrivial point, independent of tubular code.
x=[P.var(4,i) for i in range(4)]
phi_x=[p.compose([x[1]]) for p in phi]
v0=x[0]-1; v2=x[2]-x[1]**2; v3=x[3]-x[1]**3
Psi=phi_x[0]*v0+phi_x[2]*v2+phi_x[3]*v3+10*(v0*v0+v2*v2+v3*v3)
base=(F(1),F(0),F(0),F(0))
H=[[Psi.derivative_at((i,j),base) for j in range(4)] for i in range(4)]
minors=[determinant([row[:k] for row in H[:k]]) for k in range(1,5)]
assert all(z>0 for z in minors)
F1=[F(0),F(1),F(0),F(0)]; F2=[F(0),F(0),F(2),F(0)]
pair=lambda b,c:sum(b[i]*H[i][j]*c[j] for i,j in product(range(4),repeat=2))
T11=[Psi.derivative_at((1,1,i),base) for i in range(4)]
star_acceleration=[b+c for b,c in zip(F2,solve(H,T11))]
induced=pair(F2,F1); induced_star=pair(star_acceleration,F1)
assert pair(F1,F1)==1 and induced==-1 and induced_star==1
assert induced_star != induced
checks['ordered_ambient_connection_projection']={'pass':True,
    'Sylvester_leading_minors':[str(z) for z in minors],
    'pullback_metric':'1','D_induced_Gamma_lower':str(induced),
    'Dstar_induced_Gamma_lower':str(induced_star),'swapped_order_rejected':True,
    'ambient_Psi_111':str(T11[1])}

print(json.dumps({'all_pass':True,'arithmetic':'exact fractions, no external packages',
    'limitations':'Finite controls detect formula errors; global proof is in FULL_REPORT.md.',
    'checks':checks},indent=2))
