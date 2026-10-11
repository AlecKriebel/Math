#!/usr/bin/env python3
"""Independent exact directed-edge audit; does not import the author's checker.

Standard library only. Polynomials use ascending powers of h=1/log(2).
Adjacency is constructed by pairwise Hamming distance, not by label swaps.
Finite controls supplement the analytic audit; they are not an all-density proof.
"""
from fractions import Fraction as F
from itertools import permutations
from functools import lru_cache
from decimal import Decimal, localcontext
import json

CHECKS = []
NEGATIVES = []

def require(condition, label):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)

def reject(condition, label):
    require(not condition, 'negative: ' + label)
    NEGATIVES.append(label)

def poly(*a):
    a = tuple(map(F, a))
    while len(a) > 1 and a[-1] == 0:
        a = a[:-1]
    return a or (F(0),)

def add(a, b):
    return poly(*( (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                   for i in range(max(len(a), len(b))) ))

def scale(a, b):
    return poly(*(x*b for x in a))

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return poly(*c)

def pw(k):
    return F(2)**k

def mean_data(aexp, bexp, density_scale=F(1)):
    """Quotient-rule derivatives in the common formal variable h=1/log(2)."""
    if aexp == bexp:
        return poly(density_scale*pw(aexp)), poly(F(1, 2)), poly(F(1, 2))
    a, b = pw(aexp), pw(bexp)
    z = aexp-bexp
    mean = poly(0, density_scale*(a-b)/z)
    da = poly(0, F(1, z), -(a-b)/(a*z*z))
    db = poly(0, -F(1, z), (a-b)/(b*z*z))
    return mean, da, db

@lru_cache(None)
def cayley(n):
    states = tuple(permutations(range(n)))
    adjacency = tuple(tuple(j for j, t in enumerate(states)
                            if sum(x != y for x, y in zip(s, t)) == 2)
                      for s in states)
    return states, adjacency

def complete(n):
    return tuple(tuple(j for j in range(n) if i != j) for i in range(n))

def directed_forms(adjacency, exponents, potential, rate, density_scale=F(1),
                   derivative_factor=F(1), antisymmetry_factor=F(1)):
    """Use ordered edges and the source's 1/4 and 1/2 factors directly.

    The returned final two forms separate density-derivative and gradient terms.
    diagonal is obtained by retaining the reverse jump in each directed edge.
    """
    size = len(adjacency)
    mu = F(1, size)
    density = [density_scale*pw(k) for k in exponents]
    psi = list(map(F, potential))
    density_drift = [sum((rate*(density[j]-density[i]) for j in row), F(0))
                     for i, row in enumerate(adjacency)]
    psi_drift = [sum((rate*(psi[j]-psi[i]) for j in row), F(0))
                 for i, row in enumerate(adjacency)]
    action, density_term, gradient_term, diagonal = [poly(0) for _ in range(4)]
    for x, row in enumerate(adjacency):
        for y in row:
            m, dx, dy = mean_data(exponents[x], exponents[y], density_scale)
            g = psi[y]-psi[x]
            w = mu*rate
            action = add(action, scale(m, w*g*g/2))
            dm = add(scale(dx, density_drift[x]), scale(dy, density_drift[y]))
            density_term = add(density_term, scale(dm, w*g*g/4))
            gradient_term = add(gradient_term,
                                scale(m, -w*g*(psi_drift[y]-psi_drift[x])/2))
            local_dm = scale(sub(dx, dy), rate*(density[y]-density[x]))
            diagonal = add(diagonal, add(scale(local_dm, w*g*g/4),
                                         scale(m, w*rate*g*g)))
    hessian = add(scale(density_term, derivative_factor),
                  scale(gradient_term, antisymmetry_factor))
    return action, hessian, diagonal, density_term, gradient_term

def log2_interval(terms=36):
    # Integrate the geometric series for 1/(1-x^2) between 0 and 1/3.
    lower = sum((F(2, (2*j+1)*3**(2*j+1)) for j in range(terms)), F(0))
    tail = F(2, (2*terms+1)*3**(2*terms+1))*F(9, 8)
    return lower, lower+tail

def interval_polynomial(a, low, high):
    # h lies in a positive interval. Coefficient signs give rigorous bounds.
    result = [F(0), F(0)]
    for k, c in enumerate(a):
        terms = (c*low**k, c*high**k)
        result[0] += min(terms)
        result[1] += max(terms)
    return tuple(result)

def interval_ratio(a, b, low, high):
    al, ah = interval_polynomial(a, low, high)
    bl, bh = interval_polynomial(b, low, high)
    if not (al > 0 and bl > 0):
        raise AssertionError('ratio denominator/numerator interval not positive')
    return bl/ah, bh/al

def decimal_string(x):
    with localcontext() as context:
        context.prec = 35
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def run():
    L0, L1 = log2_interval()
    h0, h1 = 1/L1, 1/L0
    require(L0 > F(2, 3), 'positive strict rational log2 lower endpoint')
    require(L1-L0 < F(1, 10**35), 'rigorous log2 interval width')
    graphs, total_states = [], 0
    for n in range(2, 7):
        states, adj = cayley(n)
        N, degree = len(states), n*(n-1)//2
        total_states += N
        q = F(1, degree)
        require(all(len(row) == degree and len(set(row)) == degree for row in adj),
                f'S{n}: regular degree')
        require(all(i != j and i in adj[j] for i, row in enumerate(adj) for j in row),
                f'S{n}: no loops and reversibility')
        reached, frontier = {0}, [0]
        while frontier:
            i = frontier.pop()
            for j in adj[i]:
                if j not in reached:
                    reached.add(j); frontier.append(j)
        require(len(reached) == N, f'S{n}: irreducibility')
        require(q*degree == 1, f'S{n}: total rate one')
        require(all(sum(states[j][0] == z for j in adj[i]) ==
                    (1 if z != s[0] else degree-(n-1))
                    for i, s in enumerate(states) for z in range(n)),
                f'S{n}: one-card fiber multiplicities')
        f = [int(s[0] == 0) for s in states]
        A, B, _, _, _ = directed_forms(adj, [0]*N, f, q)
        require(B == scale(A, n*q), f'S{n}: constant-density upper test')
        for k in (-3, -1, 0, 1, 2, 5):
            exponents = [k if s[0] == 0 else 0 for s in states]
            A, B, _, _, _ = directed_forms(adj, exponents, f, q)
            t = pw(k)
            R = poly(n*q) if k == 0 else poly(n*q/2,
                        q*(t+n-2-F(n-1)/t)/(2*k))
            require(B == mul(A, R), f'S{n}: one-card exact t=2^{k}')
            require(interval_polynomial(A, h0, h1)[0] > 0,
                    f'S{n}: positive one-card action t=2^{k}')
        # These tests have arbitrary, multi-level quotient densities and potentials.
        exponents_q = [((5*i+2) % 7)-3 for i in range(n)]
        potential_q = [i*i-3*i+1 for i in range(n)]
        exponents = [exponents_q[s[0]] for s in states]
        potential = [potential_q[s[0]] for s in states]
        full = directed_forms(adj, exponents, potential, q)
        quotient = directed_forms(complete(n), exponents_q, potential_q, q)
        require(full[0:2] == quotient[0:2], f'S{n}: full and arbitrary one-card quotient forms')
        scaled = directed_forms(adj, exponents, potential, q*F(7, 11))
        require(scaled[0] == scale(full[0], F(7, 11)) and
                scaled[1] == scale(full[1], F(49, 121)), f'S{n}: time scaling')
        hom = directed_forms(adj, exponents, potential, q, density_scale=F(11, 13))
        require(hom[0] == scale(full[0], F(11, 13)) and
                hom[1] == scale(full[1], F(11, 13)), f'S{n}: density homogeneity')
        shifted = directed_forms(adj, exponents, [x+17 for x in potential], q)
        require(shifted == full, f'S{n}: potential constant-shift invariance')
        parity = [sum(s[i] > s[j] for i in range(n) for j in range(i+1, n)) % 2
                  for s in states]
        require(all(parity[i] != parity[j] for i, row in enumerate(adj) for j in row),
                f'S{n}: parity quotient has rate one')
        exponents_p = [-2 if p == 0 else 3 for p in parity]
        fa = directed_forms(adj, exponents_p, parity, q)
        fq = directed_forms(((1,), (0,)), [-2, 3], [0, 1], F(1))
        require(fa[:2] == fq[:2], f'S{n}: parity quotient forms')
        require(interval_polynomial(sub(fa[1], scale(fa[0], 2)), h0, h1)[0] > 0,
                f'S{n}: nonuniform parity test exceeds two')
        graphs.append({'n': n, 'states': N, 'undirected_edges': N*degree//2})
    states, adj = cayley(3)
    exponents, potential = [0, 0, 4, 4, 0, 0], [5, -5, 8, -8, 5, -5]
    A, B, diagonal, density_term, gradient_term = directed_forms(adj, exponents, potential, F(1, 3))
    require(A == poly(F(2248, 9), F(15, 2)), 'witness A exact coefficients')
    require(B == poly(F(1964, 9), F(5, 12), F(675, 128)), 'witness B exact coefficients')
    gap = sub(scale(A, F(9, 10)), B)
    require(interval_polynomial(gap, h0, h1)[0] > 0, 'witness rigorous 9/10 gap')
    witness_interval = interval_ratio(A, B, h0, h1)
    require(F(881815, 1000000) < witness_interval[0] < witness_interval[1] < F(881816, 1000000),
            'witness enclosing six-decimal rational interval')
    normalized = directed_forms(adj, exponents, potential, F(1, 3), density_scale=F(1, 6))
    require(normalized[0] == scale(A, F(1, 6)) and normalized[1] == scale(B, F(1, 6)),
            'witness density normalization leaves quotient unchanged')
    require(sum(pw(k) for k in exponents)/6 == 6, 'witness density mean is six')
    require(F(37888)*F(2, 3)**2+F(36480)*F(2, 3)-30375 == F(97057, 9),
            'witness elementary lower-end polynomial certificate')
    reject(B == gradient_term, 'omit density derivative')
    reject(B == add(scale(density_term, 2), gradient_term), 'drop Hessian one-half')
    reject(B == add(density_term, scale(gradient_term, -1)), 'reverse gradient-term sign')
    reject(A == scale(A, 2), 'count directed edges without one-half')
    unnormalized = directed_forms(adj, exponents, potential, F(1))
    require(unnormalized[0] == scale(A, 3) and unnormalized[1] == scale(B, 9),
            'unnormalized transposition generator scales curvature by three at n=3')
    reject(mul(unnormalized[1], A) == mul(B, unnormalized[0]), 'wrong time normalization same quotient')
    reject(B == A, 'uniform density optimum claimed for S3')
    reject(B == scale(A, F(2, 3)), 'witness attains known lower bound')
    reject(interval_polynomial(sub(B, scale(A, 2)), h0, h1)[0] >= 0,
           'reverse parity-quotient lower bound')
    local_intervals = []
    bipartite = tuple(tuple(range(3, 6)) if i < 3 else tuple(range(3)) for i in range(6))
    for k in (1, 3, 7, 15, 31):
        e = pw(-k)
        ex = [-k]*3 + [0, -2*k, -2*k]
        ps = [1]*3 + [0, 2, 2]
        a, b, on, _, _ = directed_forms(bipartite, ex, ps, F(1, 3))
        # Express the expected quotients as polynomials in h=1/log2.
        on_ratio = poly(F(1, 3), (1-e*e)/(6*e*k))
        off_ratio = poly(2*e/(3*(1+2*e)), (1-e*e)/(3*k*(1+2*e)))
        require(a == poly(0, (1-e)*(1+2*e)/(6*k)), f'local S3 action k={k}')
        require(on == mul(a, on_ratio), f'local S3 diagonal identity k={k}')
        require(sub(b, on) == mul(a, off_ratio), f'local S3 off-diagonal identity k={k}')
        require(b == mul(a, add(on_ratio, off_ratio)), f'local S3 full identity k={k}')
        full_i = interval_ratio(a, b, h0, h1)
        off_i = interval_ratio(a, sub(b, on), h0, h1)
        local_intervals.append({'epsilon_power_of_two': -k,
                                'full_ratio_decimal': list(map(decimal_string, full_i)),
                                'off_ratio_decimal': list(map(decimal_string, off_i))})
        if k == 31:
            require(full_i[0] > 10000000 and off_i[1] < F(1, 50),
                    'local divergent full quotient and small off-diagonal quotient')
            reject(full_i[1] < 1, 'off-diagonal obstruction is full-curvature sharpness')
    # Matrix construction checked by coefficients for every pair of S3 basis vectors.
    q = F(1, 3); N = 6
    LM = [[q if j in adj[i] else (-1 if i == j else 0) for j in range(N)] for i in range(N)]
    rho = list(map(pw, exponents))
    lr = [sum(LM[i][j]*rho[j] for j in range(N)) for i in range(N)]
    AM = [[poly(0) for _ in range(N)] for _ in range(N)]
    DM = [[poly(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in adj[i]:
            if i >= j: continue
            th, da, db = mean_data(exponents[i], exponents[j])
            hh = add(scale(da, lr[i]), scale(db, lr[j]))
            for r, sr in ((i, -1), (j, 1)):
                for s, ss in ((i, -1), (j, 1)):
                    AM[r][s] = add(AM[r][s], scale(th, F(sr*ss, 18)))
                    DM[r][s] = add(DM[r][s], scale(hh, F(sr*ss, 36)))
    BM = [[sub(DM[i][j], scale(add(
                sum_poly(scale(AM[i][k], LM[k][j]) for k in range(N)),
                sum_poly(scale(AM[k][j], LM[i][k]) for k in range(N))), F(1, 2)))
           for j in range(N)] for i in range(N)]
    require(all(sum_poly(row) == poly(0) for row in AM+BM), 'matrix constant nullspace')
    for i in range(N):
        for j in range(i, N):
            v = [int(k == i)+int(k == j) for k in range(N)]
            aa, bb, *_ = directed_forms(adj, exponents, v, q)
            aq = sum_poly(scale(AM[r][s], v[r]*v[s]) for r in range(N) for s in range(N))
            bq = sum_poly(scale(BM[r][s], v[r]*v[s]) for r in range(N) for s in range(N))
            require(aa == aq and bb == bq, f'fixed-density matrix identity directions {i},{j}')
    return {'status': 'passed', 'exact_assertions': len(CHECKS),
            'checks': CHECKS, 'negative_controls': NEGATIVES, 'graphs': graphs,
            'distinct_permutation_states': total_states,
            'witness_ratio_rational_interval': list(map(str, witness_interval)),
            'witness_ratio_decimal_for_orientation_only': list(map(decimal_string, witness_interval)),
            'log2_rational_interval': list(map(str, (L0, L1))),
            'local_obstruction_controls': local_intervals,
            'all_density_or_all_n_optimum_certified': False,
            'dependencies': 'Python standard library',
            'author_code_imported': False}

def sum_poly(terms):
    result = poly(0)
    for term in terms:
        result = add(result, term)
    return result

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
