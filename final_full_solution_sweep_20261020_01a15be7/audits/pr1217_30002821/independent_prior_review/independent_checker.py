"""Independent supplementary checks of PR1217, without executing source programs.

Universal statements remain proved in the written audit. This checker uses a
small polynomial/rational-function algebra, exact Fraction geometry, independent
mediant recursion, and Decimal diagnostics. No assert statement is used.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from math import gcd, factorial, comb
from pathlib import Path
import hashlib
import json

COUNTS = {}


def check(test, family):
    COUNTS[family] = COUNTS.get(family, 0) + 1
    if not test:
        raise ArithmeticError("failed: " + family)


class Poly:
    """Four-variable polynomial (q,x,E,X), rational coefficients."""
    def __init__(self, v=0):
        if isinstance(v, dict):
            self.terms = {k: F(c) for k, c in v.items() if c}
        elif isinstance(v, Poly):
            self.terms = dict(v.terms)
        else:
            self.terms = {(0, 0, 0, 0): F(v)} if v else {}

    def __add__(self, v):
        out = dict(self.terms)
        for k, c in Poly(v).terms.items():
            out[k] = out.get(k, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -c for k, c in self.terms.items()})

    def __sub__(self, v):
        return self + -Poly(v)

    def __rsub__(self, v):
        return Poly(v) + -self

    def __mul__(self, v):
        out = {}
        for a, c in self.terms.items():
            for b, d in Poly(v).terms.items():
                k = tuple(i + j for i, j in zip(a, b))
                out[k] = out.get(k, F(0)) + c*d
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = Poly(1)
        for _ in range(n):
            out = out*self
        return out

    def dq(self):
        # dE/dq=E; x and X are constant under this derivative.
        out = Poly()
        for (q, x, e, z), c in self.terms.items():
            if q:
                out += Poly({(q-1, x, e, z): c*q})
            if e:
                out += Poly({(q, x, e, z): c*e})
        return out

    def zero(self):
        return not self.terms


class Rat:
    def __init__(self, p=0, q=1):
        if isinstance(p, Rat):
            self.p, self.q = p.p, p.q
        else:
            self.p, self.q = Poly(p), Poly(q)

    def __add__(self, v):
        v = Rat(v)
        return Rat(self.p*v.q+v.p*self.q, self.q*v.q)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.p, self.q)

    def __sub__(self, v):
        return self + -Rat(v)

    def __rsub__(self, v):
        return Rat(v) + -self

    def __mul__(self, v):
        v = Rat(v)
        return Rat(self.p*v.p, self.q*v.q)

    __rmul__ = __mul__

    def __pow__(self, n):
        return Rat(self.p**n, self.q**n)

    def ds(self):
        return Rat(-q**2*(self.p.dq()*self.q-self.p*self.q.dq()), self.q**2)

    def same(self, v):
        v = Rat(v)
        return (self.p*v.q-v.p*self.q).zero()


q, x, E, X = [Poly({tuple(int(i == j) for i in range(4)): 1}) for j in range(4)]
w = Rat(1, E-1)
dw = w.ds()
ddw = dw.ds()
check(dw.same(Rat(q**2*E, (E-1)**2)), "derivatives")
check(ddw.same(Rat(q**3*E*(q*(E+1)-2*(E-1)), (E-1)**3)), "derivatives")
psi = (1+w+Rat(1, X-1))*(dw+Rat(q+x, q*x)*ddw)-Rat(q+x, q*x)*dw**2
P = x*(E-1)+(q+x)*(q*(E+1)-2*(E-1))
omega = (E*(X-1)+E-1)*P-q*(q+x)*E*(X-1)
check(psi.same(Rat(q**2*E*omega, x*(X-1)*(E-1)**4)), "omega_identity")
u1 = q*E**2-E**2+E
u2 = q**2*E**2-2*q*E**2+2*q*E
u3 = q*E**2-E**2+2*E-q-1
u4 = q**2*E**2-2*q*E**2+4*q*E-q**2-2*q
check((omega-(x*(X-1)*u1+(X-1)*u2+x*u3+u4)).zero(), "omega_identity")


def falling(m, a):
    if m < a:
        return 0
    out = 1
    for j in range(a):
        out *= m-j
    return out


def coefficient(poly, m, n):
    # m! n! times coefficient after E=exp(q), X=exp(x).
    return sum(c*falling(m, a)*k**(m-a)*falling(n, b)*l**(n-b)
               for (a, b, k, l), c in poly.terms.items() if m >= a and n >= b)


for m in range(257):
    uc = [coefficient(u, m, 0) for u in (u1, u2, u3, u4)]
    if m >= 2:
        check(uc[0] == (m-2)*2**(m-1)+1, "coefficient_formula")
        check(uc[1] == m*((m-5)*2**(m-2)+2), "coefficient_formula")
        check(uc[2] == (m-2)*2**(m-1)+2, "coefficient_formula")
        check(uc[3] == (m*((m-5)*2**(m-2)+4) if m >= 3 else 0), "coefficient_formula")
    else:
        check(uc == [0]*4, "coefficient_formula")
    for n in range(257):
        c = coefficient(omega, m, n)
        expected = uc[3] if n == 0 else (uc[1]+uc[2] if n == 1 else n*uc[0]+uc[1])
        check(c == expected and c >= 0, "double_coefficient")
check(coefficient(omega, 5, 0) == 20, "strict_positive_anchor")
# Detect a deliberately false sign in the key factorization.
check(not (omega-(x*(X-1)*u1+(X-1)*u2-x*u3+u4)).zero(), "negative_control")

# Exact chain objective bookkeeping with independently assigned formal weights.
for k in range(2, 14):
    for i in range(k+2):
        for j in range(i+2, k+2):
            if (i, j) == (0, k+1):
                continue
            inner = j-i-1
            outer = k-j+i+1
            check(1 <= inner < k and 1 <= outer < k, "split_parameters")
            weights = [F((l+2)**2, l+3) for l in range(k+2)]
            def objective(ids):
                return sum((weights[l] for l in ids[1:-1]), F(0))+sum((weights[a]*weights[b] for a, b in zip(ids, ids[1:])), F(0))
            lhs = objective(list(range(k+2)))
            rhs = objective(list(range(i+1))+list(range(j,k+2)))+objective(list(range(i,j+1)))-weights[i]*weights[j]
            check(lhs == rhs, "split_bookkeeping")


def mediants(cap):
    stack = [((1, 0), (0, 1))]
    out = set()
    while stack:
        a, b = stack.pop()
        v = tuple(i+j for i,j in zip(a,b))
        if sum(v) > cap:
            continue
        check(v not in out, "mediant_unique")
        out.add(v)
        stack.extend([(a,v),(v,b)])
    return out


cap = 32
tree = mediants(cap)
primitive = {(m,n) for m in range(1,cap) for n in range(1,cap-m+1) if gcd(m,n)==1}
check(tree == primitive, "mediant_completeness_finite")
gaps = [(F(1),F(1)),(F(1,11),F(17,3)),(F(13,2),F(1,5)),(F(19,7),F(8,13)),(F(50),F(29)),(F(1,40),F(1,13))]
geometry_counts = []
for a,b in gaps:
    vertices = [(1,0),(0,1),*sorted(tree)]
    disks = []
    for m,n in vertices:
        size = 1/(m/a+n/b)
        base = 2*a*n*size
        disks.append((m,n,size,base))
        if m*n:
            check(0 < base < 2*a*b and size <= a*b/(a+b), "boundary_geometry")
    count = 0
    for i,(m,n,s,z) in enumerate(disks):
        for M,N,t,y in disks[i+1:]:
            det = m*N-M*n
            check(y-z == 2*det*s*t, "determinant_geometry")
            check(abs(y-z) >= 2*s*t, "nonoverlap_geometry")
            count += 1
    geometry_counts.append(count)
# Determinant orientation control is not vacuous.
check(2*F(1,2)*F(1,3) != -2*F(1,2)*F(1,3), "negative_control")

# Unit-gap k=2 deformation: y=exp(theta), 4/3 <= y <= 3/2.
for y in [F(4,3),F(7,5),F(3,2)]:
    s1,s2=y-1,2/y-1
    f02=s1+s1*s2-s2
    f13=s1*s2+s2-s1
    check(f02 == 3-4/y and f13 == 3-2*y and f02 >= 0 and f13 >= 0, "k2_deformation")
    check(s1+s1*s2+s2 == 1, "k2_deformation")
check(3-4/F(1) < 0 and 3-2*F(2) < 0, "k2_endpoint_exclusion")
check(3-4/F(5,4) < 0 and 3-2*F(7,4) < 0, "negative_control")

# The additive constant in h must be kept; the threshold weight is not covered.
for vals in [(F(1,3),F(5,7),F(7,4),F(2,5)),(F(3),F(8),F(2),F(11))]:
    a,b,c,d=vals
    h=b+c+a*b+b*c+c*d
    check(h == (1+b+d)*(1+c+a)-(1+a)*(1+d), "objective_factorization")
    check(h != (1+b+d)*(1+c+a), "negative_control")
counter = [(-F(1,3),F(1,3)),(-F(1,9),F(1,3)),(F(1,9),F(1,3)),(F(1,3),F(1,3))]
for i,(z,s) in enumerate(counter):
    check(z+1 >= 2*s and 1-z >= 2*s, "weight_counterexample")
    for y,t in counter[i+1:]:
        check(y-z >= 2*s*t, "weight_counterexample")
check(sum(1 for m,n in primitive if m+n <= 3) == 3 < len(counter), "weight_counterexample")

# Decimal checks use stable exp(-1/s), never float exp or source software.
diagnostics = []
with localcontext() as ctx:
    ctx.prec = 600
    def wd(s):
        z=(-1/s).exp()
        return z/(1-z)
    for s,r in [(D('0.001'),D('0.001')),(D('0.0032'),D('0.001')),(D('0.1'),D('100')),(D('1'),D('1')),(D('100'),D('0.1')),(D('10000'),D('10000'))]:
        Q,T=1/s,1/r
        EE,XX=Q.exp(),T.exp()
        PP=T*(EE-1)+(Q+T)*(Q*(EE+1)-2*(EE-1))
        OO=(EE*(XX-1)+EE-1)*PP-Q*(Q+T)*EE*(XX-1)
        check(OO >= Q**5/6, "decimal_omega_bound")
        deriv1=Q**2*EE/(EE-1)**2
        deriv2=Q**3*EE*(Q*(EE+1)-2*(EE-1))/(EE-1)**3
        ff=1+wd(s)+wd(r)
        curvature=(s+r)*((ff*(deriv1+(s+r)*deriv2)-(s+r)*deriv1**2))/ff**2
        lam=(s+r).ln()
        step=min(D('1e-35'),(1+s/r).ln()/100)
        def logf(t):
            return (1+wd(t.exp()-r)+wd(r)).ln()
        finite=(logf(lam+step)-2*logf(lam)+logf(lam-step))/step**2
        check(curvature > 0 and finite > 0 and abs(finite/curvature-1) < D('1e-60'), "decimal_logconvexity")
        diagnostics.append({'s':str(s),'rho':str(r),'curvature':format(curvature,'.15E'),'finite_difference':format(finite,'.15E')})

out = {'verdict':'PASS','counts':COUNTS,'checks':sum(COUNTS.values()),'coefficient_grid':[256,256],
       'primitive_disks_per_gap':len(tree),'gaps':[[str(a),str(b)] for a,b in gaps],
       'pair_counts':geometry_counts,'decimal_precision':600,'decimal_diagnostics':diagnostics,
       'author_programs_executed':False,'universal_scope':'Written proof; finite diagnostics are supplementary.',
       'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,sort_keys=True,indent=2))
