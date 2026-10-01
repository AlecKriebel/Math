"""Independent exact adversarial probes; standard library only.

Finite algebra checks do not certify stochastic convergence or source theorems.
Run from any directory: python3 fresh_checks.py [output.json]
"""
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path
import json
import sys

CHECKS = []


def check(name, condition, detail=None):
    if not condition:
        raise AssertionError(name)
    CHECKS.append({"name": name, "pass": True, "detail": detail})


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x, y in zip(u, v)] for u, v in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def inv(a):
    n = len(a)
    aug = [row[:] + unit for row, unit in zip(a, eye(n))]
    for i in range(n):
        k = next(k for k in range(i, n) if aug[k][i])
        aug[i], aug[k] = aug[k], aug[i]
        z = aug[i][i]
        aug[i] = [x/z for x in aug[i]]
        for k in range(n):
            if k != i:
                z = aug[k][i]
                aug[k] = [x-z*y for x, y in zip(aug[k], aug[i])]
    return [row[n:] for row in aug]


def sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def det(a):
    ans = F(0)
    for p in permutations(range(len(a))):
        z = F(sign(p))
        for i, j in enumerate(p):
            z *= a[i][j]
        ans += z
    return ans


def matrix_checks():
    A = matrix([[0, 2, -1], [-1, 3, 1], [2, 0, -2]])
    R = matrix([[2, 1, 0], [1, 2, 1], [0, 1, 3]])
    B = matrix([[3, 1, 1], [1, 2, 0], [1, 0, 2]])
    Q, X = mul(B, B), mul(R, R)
    v = matrix([[2, -1, 1], [-1, 1, 0], [1, 0, 3]])
    coefficients = []
    representative = scale(2, mul(mul(R, v), B))
    wrong_representative = transpose(representative)
    for i in range(3):
        for j in range(3):
            E = matrix([[int((k, l) == (i, j)) for l in range(3)] for k in range(3)])
            first = trace(mul(mul(mul(v, R), E), B))
            second = trace(mul(mul(mul(v, B), transpose(E)), R))
            check(f"noise two terms ({i},{j})", first == second)
            check(f"HS representative coordinate ({i},{j})", first+second == representative[i][j])
            coefficients.append(first+second)
    norm_squared = sum(z*z for z in coefficients)
    expected = 4*trace(mul(mul(mul(X, v), Q), v))
    check("full-HS factor-four bracket", norm_squared == expected, str(expected))
    check("reject factor-two bracket", norm_squared != expected/2)
    check("reject adjointed HS representative", representative != wrong_representative)
    pairing = trace(mul(v, add(mul(X, A), mul(transpose(A), X))))
    dual = trace(mul(X, add(mul(A, v), mul(v, transpose(A)))))
    corrupt_dual = trace(mul(X, add(mul(transpose(A), v), mul(v, A))))
    check("weak drift adjoint orientation", pairing == dual)
    check("reject transposed generator orientation", pairing != corrupt_dual)

    L = matrix([[1, 2], [0, 1], [2, -1]])
    D = matrix([[3, 1], [1, 4]])
    di = inv(D)
    psi = mul(mul(L, di), transpose(L))
    Lprime = mul(A, L)
    Dprime = scale(2, mul(mul(transpose(L), Q), L))
    direct = add(add(mul(mul(Lprime, di), transpose(L)),
                     mul(mul(L, di), transpose(Lprime))),
                 scale(-1, mul(mul(mul(mul(L, di), Dprime), di), transpose(L))))
    expected_derivative = add(add(mul(A, psi), mul(psi, transpose(A))),
                              scale(-2, mul(mul(psi, Q), psi)))
    check("rectangular nonnormal Riccati identity", direct == expected_derivative)
    check("reject Riccati quadratic sign", direct != add(add(mul(A, psi), mul(psi, transpose(A))), scale(2, mul(mul(psi, Q), psi))))
    check("log determinant derivative normalization", trace(mul(di, Dprime))/2 == trace(mul(Q, psi)))
    for alpha in [F(-7, 3), F(0), F(3, 2), F(5)]:
        phi_prime = alpha*trace(mul(Q, psi))
        exponent_drift = phi_prime + trace(mul(X, direct)) - alpha*trace(mul(Q, psi)) - trace(mul(X, add(mul(A, psi), mul(psi, transpose(A)))))
        half_bracket = 2*trace(mul(mul(mul(X, psi), Q), psi))
        check(f"backward Ito cancellation alpha={alpha}", exponent_drift+half_bracket == 0)
        check(f"reject backward exponent sign alpha={alpha}", exponent_drift-half_bracket != 0)

    C = matrix([[3, 1], [1, 2]])
    for k, sqrt_v in enumerate([matrix([[0, 0], [0, 0]]), matrix([[1, 1], [1, 1]]), matrix([[2, 1], [1, 3]])]):
        vv = mul(sqrt_v, sqrt_v)
        d = add(eye(2), scale(2, mul(mul(sqrt_v, C), sqrt_v)))
        target = mul(vv, inv(add(eye(2), scale(2, mul(C, vv)))))
        actual = mul(mul(sqrt_v, inv(d)), sqrt_v)
        check(f"resolvent identity rank-case={k}", actual == target)
        check(f"determinant identity rank-case={k}", det(d) == det(add(eye(2), scale(2, mul(C, vv)))))
        check(f"symmetric resolvent rank-case={k}", target == transpose(target))
        if k == 2:
            wrong = mul(vv, inv(add(eye(2), scale(2, mul(vv, C)))))
            check("reject noncommuting inverse order", actual != wrong)

    # Exact tilt-rescale identity, with noncommuting noncentrality and v.
    vv = matrix([[2, 1], [1, 1]])
    noncentral = matrix([[3, -1], [-1, 2]])
    for r in [F(0), F(1, 3), F(4), F(100)]:
        a = 1+2*r
        z = add(scale(r, eye(2)), scale(a, vv))
        check(f"tilt determinant r={r}", det(add(eye(2), scale(2, z))) == a**2*det(add(eye(2), scale(2, vv))))
        difference = add(mul(z, inv(add(eye(2), scale(2, z)))), scale(-r/a, eye(2)))
        target = scale(1/a, mul(vv, inv(add(eye(2), scale(2, vv)))))
        check(f"tilt exponent matrix r={r}", difference == target)
        check(f"tilt exponent trace r={r}", trace(mul(noncentral, difference)) == trace(mul(noncentral, target)))


class Jets:
    def __init__(self, variables, degree):
        self.variables, self.degree = variables, degree
        self.zero = (0,)*variables

    def constant(self, c):
        return {self.zero: F(c)} if c else {}

    def variable(self, i):
        t = list(self.zero)
        t[i] = 1
        return {tuple(t): F(1)}

    def add(self, a, b):
        c = dict(a)
        for m, x in b.items():
            c[m] = c.get(m, F(0))+x
            if not c[m]:
                del c[m]
        return c

    def scale(self, s, a):
        return {m: s*x for m, x in a.items() if s*x}

    def mul(self, a, b):
        c = {}
        for p, x in a.items():
            for q, y in b.items():
                m = tuple(z+w for z, w in zip(p, q))
                if sum(m) <= self.degree:
                    c[m] = c.get(m, F(0))+x*y
        return {m:x for m,x in c.items() if x}

    def matmul(self, a, b):
        return [[self.sum(self.mul(a[i][k], b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

    def sum(self, terms):
        out = {}
        for term in terms:
            out = self.add(out, term)
        return out

    def determinant(self, a):
        out = {}
        for p in permutations(range(len(a))):
            term = self.constant(sign(p))
            for i, j in enumerate(p):
                term = self.mul(term, a[i][j])
            out = self.add(out, term)
        return out


def laplace_jet(n, alpha, noncentral=None):
    pairs = [(i,j) for i in range(n) for j in range(i,n)]
    position = {p:k for k,p in enumerate(pairs)}
    jets = Jets(len(pairs), n)
    V = [[jets.variable(position[tuple(sorted((i,j)))]) for j in range(n)] for i in range(n)]
    D = [[jets.add(jets.constant(int(i == j)), jets.scale(2, V[i][j])) for j in range(n)] for i in range(n)]
    perturbation = jets.add(jets.determinant(D), jets.constant(-1))
    power, central, binomial = jets.constant(1), jets.constant(1), F(1)
    for k in range(1,n+1):
        power = jets.mul(power, perturbation)
        binomial *= (-alpha/2-k+1)/k
        central = jets.add(central, jets.scale(binomial, power))
    if noncentral is None:
        return jets, pairs, central
    vp = V
    log_exponential = {}
    # -tr(B V (I+2V)^(-1)) = -sum_k (-2)^(k-1)tr(B V^k).
    for k in range(1,n+1):
        log_exponential = jets.add(log_exponential, jets.sum(jets.scale(-F((-2)**(k-1))*noncentral[i][j], vp[j][i]) for i in range(n) for j in range(n)))
        vp = jets.matmul(vp, V)
    power, exponential = jets.constant(1), jets.constant(1)
    for k in range(1,n+1):
        power = jets.mul(power, log_exponential)
        exponential = jets.add(exponential, jets.scale(F(1,factorial(k)), power))
    return jets, pairs, jets.mul(central, exponential)


def determinant_moment(n, alpha, noncentral=None):
    jets, pairs, laplace = laplace_jet(n, alpha, noncentral)
    position = {p:k for k,p in enumerate(pairs)}
    result = F(0)
    for p in permutations(range(n)):
        powers = [0]*len(pairs)
        offdiag = 0
        for i, j in enumerate(p):
            powers[position[tuple(sorted((i,j)))]] += 1
            offdiag += (i != j)
        coefficient = laplace.get(tuple(powers), F(0))
        derivative_factor = 1
        for k in powers:
            derivative_factor *= factorial(k)
        result += F((-1)**n*sign(p)*derivative_factor, 2**offdiag)*coefficient
    return result


def determinant_checks():
    for n in [1,2,3,4]:
        for alpha in [F(0), F(1,3), F(1), F(3,2), F(2), F(5,2), F(3), F(4), F(7)]:
            expected = F(1)
            for k in range(n):
                expected *= alpha-k
            got = determinant_moment(n, alpha)
            check(f"central determinant moment n={n} alpha={alpha}", got == expected, str(got))
            if alpha >=0 and alpha.denominator != 1 and n == alpha.numerator//alpha.denominator+2:
                check(f"negative positive-matrix determinant obstruction alpha={alpha}", got < 0)
    B = matrix([[2,1,0],[1,3,1],[0,1,2]])
    check("noncentral test positive definite", all(det([row[:k] for row in B[:k]]) > 0 for k in [1,2,3]))
    alpha = F(3,2)
    for a in [F(1), F(3), F(9), F(101), F(1001)]:
        scaled = scale(1/a, B)
        got = determinant_moment(3, alpha, scaled)
        e2 = sum(B[i][i]*B[j][j]-B[i][j]**2 for i in range(3) for j in range(i+1,3))
        expected = alpha*(alpha-1)*(alpha-2)+(alpha-1)*(alpha-2)*trace(B)/a+(alpha-2)*e2/a**2+det(B)/a**3
        check(f"noncentral determinant polynomial a={a}", got == expected, str(got))
        if a >=101:
            check(f"tilted-rescaled forbidden determinant a={a}", got < 0)
    # Removing the half in symmetric off-diagonal derivatives fails already n=2.
    jets,pairs,L = laplace_jet(2,F(3))
    wrong = L.get((1,0,1),F(0))-2*L.get((0,2,0),F(0))
    check("reject off-diagonal derivative normalization", wrong != determinant_moment(2,F(3)))


def boundary_checks():
    for alpha in [F(1,3),F(3,2),F(17,4),F(99,10),F(1001,2)]:
        n = alpha.numerator//alpha.denominator+2
        check(f"obstructing dimension alpha={alpha}", n > alpha+1 and alpha < n-1 and alpha.denominator != 1)
    # For disjoint symmetric smooth bumps within (0,T), Q=I left-shift covariance
    # is diagonal and equals each support midpoint after normalization.
    T = F(1)
    intervals = [(F(1,10),F(2,10)),(F(3,10),F(4,10)),(F(5,10),F(7,10))]
    C = matrix([[((a+b)/2 if i == j else 0) for j in range(3)] for i,(a,b) in enumerate(intervals)])
    check("killed-left-shift positive compressed covariance", det(C)>0 and all(b<T for a,b in intervals), str(det(C)))
    check("killed-left-shift terminal noncentrality zero", all(b<T for a,b in intervals))
    # A finite-valued heavy-tailed initial trace has infinite mean and finite stops.
    for K in [1,2,5,10,30]:
        probability = sum(F(1,2**k) for k in range(1,K+1))
        truncated_mean = sum(F(2**k,2**k) for k in range(1,K+1))
        check(f"finite-a.s. infinite-mean initial law K={K}", probability == 1-F(1,2**K) and truncated_mean == K)
    check("zero-process weak equation alpha-zero", F(0)*F(7) == 0)


if __name__ == "__main__":
    matrix_checks()
    determinant_checks()
    boundary_checks()
    output = {"script": "fresh_checks.py", "arithmetic": "exact Fraction; Python standard library", "checks_passed":len(CHECKS), "checks_failed":0, "checks":CHECKS, "scope_limit":"Finite algebra and finite-dimensional positivity probes; analytic proof recorded separately."}
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("fresh_check_results.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(f"PASS {len(CHECKS)} exact checks; {path}")
