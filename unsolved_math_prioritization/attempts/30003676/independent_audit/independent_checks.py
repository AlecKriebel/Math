#!/usr/bin/env python3
"""Independent SIS audit. No author imports; standard library; exact tests separated from diagnostics."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
from math import lcm, log, log1p, exp, sqrt, isfinite
import json

counts = Counter()

def require(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] += 1

def determinant(a):
    """Integer fraction-free Bareiss elimination, including pivot sign."""
    a = [row[:] for row in a]
    n = len(a)
    if not n:
        return 1
    previous, sign = 1, 1
    for k in range(n - 1):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * value - a[i][k] * a[k][j]
                assert num % previous == 0
                a[i][j] = num // previous
            a[i][k] = 0
        previous = value
    return sign * a[-1][-1]

def det_fraction(a):
    scale = lcm(*(x.denominator for row in a for x in row))
    return F(determinant([[int(x * scale) for x in row] for row in a]), scale ** len(a))

def cramers(a, b):
    d = det_fraction(a)
    assert d
    ans = []
    for j in range(len(b)):
        aa = [row[:] for row in a]
        for i in range(len(b)):
            aa[i][j] = b[i]
        ans.append(det_fraction(aa) / d)
    return ans

def states(n):
    return [frozenset(c) for k in range(n + 1) for c in combinations(range(n), k)]

def chain(w, mu, theta, epsilon):
    """w[target][source]; generate transitions by sets, not the author's bit enumeration."""
    ss = states(len(mu))
    loc = {s: i for i, s in enumerate(ss)}
    q = [[F(0) for _ in ss] for _ in ss]
    for i, s in enumerate(ss):
        for v in range(len(mu)):
            if v in s:
                t, rate = s - {v}, mu[v]
            else:
                t = s | {v}
                rate = epsilon + theta * sum((w[v][u] for u in s), F(0))
            q[i][loc[t]] = rate
        q[i][i] = -sum(q[i])
    return ss, q

def invariant(q):
    """Markov-chain tree/cofactor weights, independently of balance-equation solving."""
    scale = lcm(*(x.denominator for row in q for x in row))
    lap = [[int(-scale * x) for x in row] for row in q]
    cof = [determinant([[lap[i][j] for j in range(len(q)) if j != k]
                        for i in range(len(q)) if i != k]) for k in range(len(q))]
    require('cofactor_weights_nonnegative', min(cof) >= 0 and sum(cof) > 0)
    p = [F(x, sum(cof)) for x in cof]
    require('cofactor_full_balance', all(sum(p[i] * q[i][j] for i in range(len(q))) == 0
                                        for j in range(len(q))))
    return p

def residual(p, q):
    return [sum(p[i] * q[i][j] for i in range(len(q))) for j in range(len(q))]

def susceptible(ss, p, subset):
    return sum((p[i] for i, s in enumerate(ss) if not s & subset), F(0))

def upper_sets(ss):
    for choice in product([False, True], repeat=len(ss)):
        if all(not choice[i] or choice[j] for i, a in enumerate(ss)
               for j, b in enumerate(ss) if a <= b):
            yield [i for i in range(len(ss)) if choice[i]]

def symmetric(n, edges):
    w = [[F(0) for _ in range(n)] for _ in range(n)]
    for u, v, rate in edges:
        w[u][v] = w[v][u] = F(rate)
    return w

graphs = [
    (symmetric(1, []), [F(2, 3)]),
    (symmetric(2, [(0, 1, F(5, 7))]), [F(1, 3), F(4, 5)]),
    (symmetric(3, [(0, 1, F(2, 3)), (1, 2, F(3, 2))]), [F(1), F(7, 4), F(2, 5)]),
    (symmetric(3, [(0, 1, F(1)), (0, 2, F(1, 8)), (1, 2, F(11, 6))]),
     [F(3, 4), F(1, 2), F(2)]),
]
for w, mu in graphs:
    n = len(mu)
    for theta, epsilon in [(F(0), F(1, 9)), (F(1, 10), F(2, 7)), (F(8, 3), F(1, 31))]:
        ss, q = chain(w, mu, theta, epsilon)
        p = invariant(q)
        _, q0 = chain(w, mu, theta, F(0))
        hh = [susceptible(ss, p, s) for s in ss]
        require('dual_empty_boundary', hh[0] == 1)
        for i, s in enumerate(ss[1:], 1):
            require('dual_killed_equation_all_subsets',
                    sum(q0[i][j] * hh[j] for j in range(len(ss))) == epsilon * len(s) * hh[i])
        for u, v in combinations(range(n), 2):
            pu = 1 - susceptible(ss, p, {u})
            pv = 1 - susceptible(ss, p, {v})
            both = sum((p[i] for i, s in enumerate(ss) if {u, v} <= s), F(0))
            require('joint_ancestry_covariance', both - pu * pv ==
                    susceptible(ss, p, {u, v}) - susceptible(ss, p, {u}) * susceptible(ss, p, {v}))
        for parameter in ['theta', 'epsilon', 'recoveries', 'weights']:
            wt = [[x * (2 if parameter == 'weights' else 1) for x in row] for row in w]
            mt = [x / (2 if parameter == 'recoveries' else 1) for x in mu]
            tt = theta + (F(1, 3) if parameter == 'theta' else 0)
            et = epsilon + (F(1, 5) if parameter == 'epsilon' else 0)
            _, qp = chain(wt, mt, tt, et)
            pp = invariant(qp)
            for event in upper_sets(ss):
                require('all_upper_events_monotonic_' + parameter,
                        sum(p[i] for i in event) <= sum(pp[i] for i in event))
        # A genuinely nonconstant positive vector, not only a_v=1.
        av = [F(i + 2, i + 1) for i in range(n)]
        small_theta = F(1, 100)
        margin = min(mu[u] - small_theta * sum(w[u][v] * av[v] for v in range(n)) / av[u]
                     for u in range(n))
        ss, qs = chain(w, mu, small_theta, epsilon)
        ps = invariant(qs)
        H = [sum((av[v] for v in s), F(0)) for s in ss]
        for i in range(len(ss)):
            require('nonconstant_positive_vector_drift',
                    sum(qs[i][j] * H[j] for j in range(len(ss))) <= epsilon * sum(av) - margin * H[i])
        require('nonconstant_positive_vector_stationary_bound',
                sum(ps[i] * len(s) for i, s in enumerate(ss)) <= epsilon * sum(av) / (margin * min(av)))
        M = [[(mu[i] if i == j else F(0)) - small_theta * w[i][j] for j in range(n)] for i in range(n)]
        bound = cramers(M, [epsilon] * n)
        for i in range(n):
            require('resolvent_marginal_certificate', 1 - susceptible(ss, ps, {i}) <= bound[i])
    ss, q = chain(w, mu, F(7, 2), F(0))
    p = invariant(q)
    require('zero_immigration_exact_stationary_empty', p == [F(1)] + [F(0)] * (len(ss) - 1))

for N in range(1, 5):
    for theta in [F(0), F(2, 3), F(9, 2)]:
        a, mu, epsilon = F(5, 4), F(7, 6), F(1, 17)
        beta = theta * a
        w = symmetric(N, [(i, j, a / N) for i, j in combinations(range(N), 2)])
        ss, q = chain(w, [mu] * N, theta, epsilon)
        p = invariant(q)
        weights = [F(1)]
        for k in range(N):
            weights.append(weights[-1] * (N - k) * (epsilon + beta * F(k, N)) / (mu * (k + 1)))
        total = sum(weights)
        for k in range(N + 1):
            require('clique_count_law_from_cofactors',
                    sum((p[i] for i, s in enumerate(ss) if len(s) == k), F(0)) == weights[k] / total)
            if k and beta:
                r = N * epsilon / (mu * k) * (beta / mu) ** (k - 1)
                for j in range(1, k):
                    r *= (1 - F(j, N)) * (1 + N * epsilon / (beta * j))
                require('clique_closed_product', r == weights[k])
        if not theta:
            for i, s in enumerate(ss):
                x = epsilon / (mu + epsilon)
                require('theta_zero_independent_product', p[i] == x ** len(s) * (1 - x) ** (N - len(s)))

def obstruction(n):
    m = n // 4
    N, eta = 2 * m, F(1, n * n)
    edges = [(i, j, F(1, 4 * m)) for i, j in combinations(range(N), 2)]
    blocks = [list(range(N))] + [[N + 2 * i, N + 2 * i + 1] for i in range(m)]
    edges += [(block[0], block[1], F(1)) for block in blocks[1:]]
    base = symmetric(n, edges)
    bridges = [(left[-1], right[0], eta) for left, right in zip(blocks, blocks[1:])]
    extra_chain = [blocks[-1][-1]] + list(range(4 * m, n))
    bridges += [(x, y, eta) for x, y in zip(extra_chain, extra_chain[1:])]
    weak = symmetric(n, bridges)
    full = [[base[i][j] + weak[i][j] for j in range(n)] for i in range(n)]
    return full, base, weak, N

for n in range(4, 37):
    w, base, weak, N = obstruction(n)
    reached = {0}
    for _ in range(n):
        reached |= {v for u in reached for v in range(n) if w[u][v]}
    require('all_integer_sizes_connected', len(reached) == n)
    require('all_integer_sizes_weak_row_bound', max(map(sum, weak)) <= F(2, n * n))
    require('all_integer_sizes_base_spectral_upper', max(map(sum, base)) == 1)
    require('all_integer_sizes_dimer_rayleigh_lower', w[N][N + 1] == 1)
    require('all_integer_sizes_fixed_clique_a', base[0][1] == F(1, 2) / N)

# Independently certify the actual connected-chain stochastic sandwich at n=4.
w, base, weak, N = obstruction(4)
ss, q = chain(w, [F(1)] * 4, F(3), F(1, 13))
p = invariant(q)
_, qlo = chain(base, [F(1)] * 4, F(3), F(1, 13))
_, qhi = chain(base, [F(1)] * 4, F(3), F(1, 13) + 2 * F(3, 16))
plo, phi = invariant(qlo), invariant(qhi)
for event in upper_sets(ss):
    require('connected_sandwich_all_upper_events',
            sum(plo[i] for i in event) <= sum(p[i] for i in event) <= sum(phi[i] for i in event))

# Deliberately wrong models/formulas are required to fail.
w = symmetric(2, [(0, 1, 1)])
ss, q = chain(w, [F(1), F(1)], F(2), F(1, 5))
p = invariant(q)
for name, wrong_q in [
    ('missing_immigration', chain(w, [F(1)] * 2, F(2), F(0))[1]),
    ('theta_scaled_recovery', chain(w, [F(2)] * 2, F(2), F(1, 5))[1]),
    ('global_instead_of_per_vertex_seeding', chain(w, [F(1)] * 2, F(2), F(1, 10))[1]),
    ('incorrect_edge_normalization', chain([[2*x for x in row] for row in w], [F(1)]*2, F(2), F(1,5))[1]),
]:
    require('REJECT_' + name, any(residual(p, wrong_q)))
_, qmf = chain(w, [F(1)] * 2, F(1), F(1, 2))
require('REJECT_meanfield_independent_stationary_law', any(residual([F(1,4)] * 4, qmf)))
hh = [susceptible(ss, p, s) for s in ss]
_, q0 = chain(w, [F(1)] * 2, F(2), F(0))
require('REJECT_missing_dual_cardinality', sum(q0[-1][j] * hh[j] for j in range(len(ss))) != F(1,5) * hh[-1])
h, t = F(1, 5), F(2)
claimed_dimer = h * (1 + h + t) / ((1 + h) ** 2 + h * t)
require('dimer_formula_cofactor_check', 1 - hh[1] == claimed_dimer)
require('REJECT_missing_susceptible_birth_factor', p[1] + p[2] != h/(1 + h + h*(h+t)/2))

# Directed-graph control: symmetry cannot silently be removed from self-duality.
directed = [[F(0), F(1, 4)], [F(3), F(0)]]
ss, q = chain(directed, [F(1), F(2)], F(3, 2), F(1, 7))
p = invariant(q)
hh = [susceptible(ss, p, s) for s in ss]
_, wrong_dual = chain(directed, [F(1), F(2)], F(3, 2), F(0))
_, right_dual = chain(list(map(list, zip(*directed))), [F(1), F(2)], F(3, 2), F(0))
require('REJECT_untransposed_directed_dual', any(sum(wrong_dual[i][j]*hh[j] for j in range(len(ss))) !=
                                              F(1,7)*len(s)*hh[i] for i,s in enumerate(ss[1:],1)))
for i, s in enumerate(ss[1:],1):
    require('transposed_directed_dual_control', sum(right_dual[i][j]*hh[j] for j in range(len(ss))) ==
                                             F(1,7)*len(s)*hh[i])

def logadd(x, y):
    z = max(x,y)
    return z + log1p(exp(min(x,y)-z))

def logweights(N, beta, mu, logepsilon):
    rr = [0.0]
    for k in range(N):
        birth_inner = logepsilon if not k else logadd(logepsilon, log(beta*k/N))
        rr.append(rr[-1] + log(N-k) + birth_inner - log(mu*(k+1)))
    return rr

# Diagnostics, explicitly not exact tests or a proof of any n -> infinity limit.
diagnostics = []
for N in [25,100,400,1600,6400]:
    for R in [0.8,1.0,1.2,3.0]:
        for schedule in ['exp_minus_sqrt_n','n_minus_2','inverse_log_n']:
            le = {'exp_minus_sqrt_n':-sqrt(N),'n_minus_2':-2*log(N),
                  'inverse_log_n':-log(log(N+2))}[schedule]
            rr = logweights(N,R,1.0,le)
            Fvalues = [(k/N)*log(R) - k/N - ((1-k/N)*log1p(-k/N) if k<N else 0.0)
                       for k in range(N+1)]
            error = max(abs(rr[k]/N - Fvalues[k]) for k in range(N+1))
            q = exp(le)/R
            envelope = (abs(le)+2*log(N)+abs(log(R))+1)/N + log1p(q)+q*log1p(1/q)
            assert error <= envelope + 1e-11
            top = max(rr)
            masses = [exp(x-top) for x in rr]
            mean = sum((k/N)*x for k,x in enumerate(masses))/sum(masses)
            diagnostics.append({'N':N,'R':R,'schedule':schedule,'uniform_log_error':error,
                                'proved_error_envelope':envelope,'mean_density':mean})
fast = []
for N in [20,40,80]:
    rr = logweights(N,3.0,1.0,-N*N)
    top = max(rr[1:])
    lm = top + log(sum(exp(x-top) for x in rr[1:]))
    bound = 2*log(N)-N*N+(N-1)*log(4*N)
    assert lm <= bound + 1e-10 and lm < -100
    fast.append({'N':N,'log_nonempty_unnormalized_mass':lm,'analytic_log_upper_bound':bound})

print(json.dumps({'status':'PASS','exact_arithmetic':'Fraction plus integer Bareiss determinant cofactors',
                  'author_code_imported':False,'exact_check_groups':dict(sorted(counts.items())),
                  'exact_checks':sum(counts.values()),
                  'wrong_model_rejections':sum(v for k,v in counts.items() if k.startswith('REJECT_')),
                  'floating_diagnostics_not_proofs':diagnostics,'fast_immigration_diagnostics_not_proofs':fast,
                  'scope_limit':'No finite calculation proves an asymptotic theorem or resolves the general conjecture.'},
                 indent=2,sort_keys=True))
