#!/usr/bin/env python3
"""Exact/high-precision audit of the r=2 likelihood/Fisher route.

All Markov-chain data and the Green--collision quantities are constructed
independently over ``Fraction``.  Decimal logarithms are used only for the
reported entropy diagnostics; every algebraic identity asserted by the
program is exact.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations
from math import comb


def popcount(state: int) -> int:
    return state.bit_count()


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [
                aug[row][j] - scale * aug[col][j] for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def transition(weights):
    degree = [sum(row) for row in weights]
    return [
        [F(weights[v][u], degree[v]) for u in range(len(weights))]
        for v in range(len(weights))
    ]


def geometric_union_law(row):
    support = [u for u, value in enumerate(row) if value]
    law = {}
    for size in range(1, len(support) + 1):
        for chosen in combinations(support, size):
            probability = F(0)
            for subsize in range(size + 1):
                for subset in combinations(chosen, subsize):
                    mass = sum((row[u] for u in subset), F(0))
                    probability += (-1) ** (size - subsize) * (
                        mass / (2 - mass) if mass else F(0)
                    )
            if probability:
                law[sum(1 << u for u in chosen)] = probability
    assert sum(law.values(), F(0)) == 1
    return law


def proper_generator(P):
    n = len(P)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    laws = [geometric_union_law(P[v]) for v in range(n)]
    Q = [[F(0) for _ in states] for _ in states]
    for state in states:
        source = index[state]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                assert 0 < output < full
                if output != state:
                    Q[source][index[output]] += probability
                    Q[source][source] -= probability
    assert all(sum(row, F(0)) == 0 for row in Q)
    return states, Q


def event_kernel(P):
    """Uncentered dual event kernel, including events that leave A fixed.

    Its row sum at A is |A|.  Subtracting |A| from the diagonal recovers the
    continuous-time generator returned by ``proper_generator``.
    """
    n = len(P)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    laws = [geometric_union_law(P[v]) for v in range(n)]
    T = [[F(0) for _ in states] for _ in states]
    for state in states:
        source = index[state]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                assert 0 < output < full
                T[source][index[output]] += probability
        assert sum(T[source], F(0)) == popcount(state)
    return states, T


def stationary(Q):
    size = len(Q)
    matrix = [[Q[col][row] for col in range(size)] for row in range(size)]
    matrix[-1] = [F(1)] * size
    rhs = [F(0)] * size
    rhs[-1] = F(1)
    pi = solve(matrix, rhs)
    assert all(value > 0 for value in pi)
    assert sum(pi, F(0)) == 1
    assert all(
        sum(pi[row] * Q[row][col] for row in range(size)) == 0
        for col in range(size)
    )
    return pi


def complete_green_coefficients(n):
    denominator = 1 - F(1, 2) ** (n - 1)
    mu = [F(0)] * (n + 1)
    for k in range(1, n):
        mu[k] = (
            F(n + k, 2 * n) - F(2) ** (k - n)
        ) / (n * comb(n - 2, k - 1) * denominator)
    return [mu[k] + mu[k + 1] for k in range(n)]


def decimal(value: F) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def matvec(Q, vector):
    return [
        sum((Q[row][col] * vector[col] for col in range(len(vector))), F(0))
        for row in range(len(Q))
    ]


def green_data(weights, P, states, QK, pi):
    n = len(P)
    N = n - 1
    index = {state: row for row, state in enumerate(states)}
    coefficients = complete_green_coefficients(n)
    U = [F(0)] * n
    for holes in range(1, n):
        U[holes] = sum(
            (
                coefficients[k]
                * F(2 * N * N, (N + k) ** 2)
                * comb(holes - 1, k - 1)
                for k in range(1, holes + 1)
            ),
            F(0),
        )

    forcing = []
    conditional_V = []
    conditional_hit_gap = []
    for state in states:
        occupied = [v for v in range(n) if (state >> v) & 1]
        holes = [u for u in range(n) if not ((state >> u) & 1)]
        cut = sum((P[v][u] for v in occupied for u in holes), F(0))
        surplus = cut - F(len(occupied) * len(holes), N)
        forcing_value = U[len(holes)] * surplus
        forcing.append(forcing_value)

        value = F(0)
        hit_gap = F(0)
        for k in range(1, len(holes) + 1):
            baseline = F(k, N)
            factor = coefficients[k] * F(2) / (1 + baseline) ** 2
            baseline_hit = F(2) * baseline / (1 + baseline)
            for v in occupied:
                for subset in combinations(holes, k):
                    mass = sum((P[v][u] for u in subset), F(0))
                    atom = factor * (mass - baseline) ** 2 / (1 + mass)
                    hit = F(2) * mass / (1 + mass)

                    # If p=h(mass) and p_0=h(baseline), the tangent
                    # remainder has the exact one-sided chi-square form
                    #
                    #   D_{-h}(mass,baseline)
                    #       =(p-p_0)^2/(2-p).
                    #
                    # This is the cost naturally paired with the direct
                    # stationary-flow work; no logarithms or approximation
                    # enter the identity.
                    hit_chi = coefficients[k] * (hit - baseline_hit) ** 2 / (
                        2 - hit
                    )
                    assert atom == hit_chi
                    value += atom
                    hit_gap += coefficients[k] * (baseline_hit - hit)
        conditional_V.append(value)
        conditional_hit_gap.append(hit_gap)

        # The tangent identity h(x)-h(a)=linear-D gives a second, simpler
        # exact form of the direct residual at every dual state.
        assert value - forcing_value == hit_gap

    L = sum((pi[row] * forcing[row] for row in range(len(states))), F(0))
    V = sum((pi[row] * conditional_V[row] for row in range(len(states))), F(0))
    assert V - L == sum(
        (pi[row] * conditional_hit_gap[row] for row in range(len(states))),
        F(0),
    )

    # Solve Q_K psi = forcing with one gauge equation.  Because the forcing
    # has zero pi_K mean, replacing any one equation is legitimate.
    matrix = [row[:] for row in QK]
    rhs = forcing[:]
    matrix[-1] = [F(0)] * len(states)
    matrix[-1][0] = F(1)
    rhs[-1] = F(0)
    psi = solve(matrix, rhs)
    residual = matvec(QK, psi)
    assert residual == forcing
    return L, V, forcing, conditional_V, psi


def audit(label, weights, expected):
    n = len(weights)
    N = n - 1
    P = transition(weights)
    states, QP = proper_generator(P)
    complete_P = [
        [F(0) if u == v else F(1, N) for u in range(n)] for v in range(n)
    ]
    complete_states, QK = proper_generator(complete_P)
    assert states == complete_states
    pi = stationary(QP)
    piK = [
        F(n - popcount(state), n * (2 ** (n - 1) - 1)) for state in states
    ]
    assert sum(piK, F(0)) == 1
    assert all(
        sum(piK[row] * QK[row][col] for row in range(len(states))) == 0
        for col in range(len(states))
    )
    g = [pi[row] / piK[row] for row in range(len(states))]

    # Q_K is not generally reversible.  Record an exact detailed-balance
    # violation whenever one occurs.
    nonreversible = None
    for row, A in enumerate(states):
        for col, B in enumerate(states):
            if piK[row] * QK[row][col] != piK[col] * QK[col][row]:
                nonreversible = (
                    A,
                    B,
                    piK[row] * QK[row][col],
                    piK[col] * QK[col][row],
                )
                break
        if nonreversible:
            break
    assert nonreversible is not None

    L, V, forcing, conditional_V, psi = green_data(
        weights, P, states, QK, pi
    )
    # Exact covariance and Poisson representations of L.
    assert sum((piK[row] * forcing[row] for row in range(len(states))), F(0)) == 0
    assert L == sum(
        (piK[row] * (g[row] - 1) * forcing[row] for row in range(len(states))),
        F(0),
    )

    # Direct actual-flow compensation.  T_P and T_K include self-events and
    # have the same row mass |A|.  With r_AB=T_P/T_K, actual stationarity
    # cancels the r-weighted work exactly, leaving L as the (1-r)-work.
    event_states, TP = event_kernel(P)
    complete_event_states, TK = event_kernel(complete_P)
    assert event_states == complete_event_states == states
    for row, state in enumerate(states):
        size = popcount(state)
        for col in range(len(states)):
            assert QP[row][col] == TP[row][col] - (size if row == col else 0)
            assert QK[row][col] == TK[row][col] - (size if row == col else 0)
    direct_work = F(0)
    actual_work = F(0)
    event_pinsker_lower_bound = F(0)
    event_chi_square = F(0)
    for row in range(len(states)):
        ratio_mean = F(0)
        total_variation = F(0)
        for col in range(len(states)):
            if not TK[row][col]:
                assert not TP[row][col]
                continue
            ratio = TP[row][col] / TK[row][col]
            ratio_mean += TK[row][col] * ratio
            total_variation += abs(TP[row][col] - TK[row][col]) / 2
            event_chi_square += (
                pi[row] * (TP[row][col] - TK[row][col]) ** 2 / TK[row][col]
            )
            increment = psi[col] - psi[row]
            direct_work += (
                piK[row] * TK[row][col] * g[row] * (1 - ratio) * increment
            )
            actual_work += pi[row] * TP[row][col] * increment
        assert ratio_mean == popcount(states[row])
        # T_P/|A| and T_K/|A| are probability laws.  Pinsker therefore
        # gives a fully rational lower bound on their rowwise KL cost:
        # |A| KL(T_P/|A| || T_K/|A|) >= 2 TV(T_P,T_K)^2/|A|.
        event_pinsker_lower_bound += (
            pi[row] * F(2, popcount(states[row])) * total_variation**2
        )
    assert actual_work == 0
    assert direct_work == L
    assert V - L == sum(
        (pi[row] * conditional_V[row] for row in range(len(states))), F(0)
    ) - direct_work
    assert event_pinsker_lower_bound == expected["event_pinsker"]
    assert event_chi_square == expected["event_chi"]
    assert event_pinsker_lower_bound > V

    # The quadratic (chi-square) complete-chain Fisher information remains
    # exact without reversibility because the stationary directed flow is
    # balanced.  Compare the true Poisson pairing with its symmetric part;
    # their difference measures the nonreversible circulation obstruction.
    chi_fisher = -sum(
        (
            piK[row]
            * g[row]
            * sum(QK[row][col] * g[col] for col in range(len(states)))
            for row in range(len(states))
        ),
        F(0),
    )
    chi_flow = sum(
        (
            piK[row]
            * QK[row][col]
            * (g[col] - g[row]) ** 2
            for row in range(len(states))
            for col in range(len(states))
            if row != col
        ),
        F(0),
    ) / 2
    assert chi_fisher == chi_flow
    psi_energy = sum(
        (
            piK[row]
            * QK[row][col]
            * (psi[col] - psi[row]) ** 2
            for row in range(len(states))
            for col in range(len(states))
            if row != col
        ),
        F(0),
    ) / 2
    symmetric_pairing = -sum(
        (
            piK[row]
            * QK[row][col]
            * (g[col] - g[row])
            * (psi[col] - psi[row])
            for row in range(len(states))
            for col in range(len(states))
            if row != col
        ),
        F(0),
    ) / 2
    Qstar = [
        [piK[col] * QK[col][row] / piK[row] for col in range(len(states))]
        for row in range(len(states))
    ]
    Qs = [
        [(QK[row][col] + Qstar[row][col]) / 2 for col in range(len(states))]
        for row in range(len(states))
    ]
    symmetric_poisson = sum(
        (
            pi[row]
            * sum(
                ((Qs[row][col] - QP[row][col]) * psi[col]
                 for col in range(len(states))),
                F(0),
            )
            for row in range(len(states))
        ),
        F(0),
    )
    assert symmetric_pairing == symmetric_poisson

    # Same-rank complete transitions are exactly reversible.  Every
    # rank-changing transition is one-way, and summing its contribution gives
    # the exact antisymmetric-current formula L-S.
    circulation = F(0)
    for row, A in enumerate(states):
        for col, B in enumerate(states):
            if row == col or not QK[row][col]:
                continue
            forward_flow = piK[row] * QK[row][col]
            reverse_flow = piK[col] * QK[col][row]
            if popcount(A) == popcount(B):
                assert forward_flow == reverse_flow
            else:
                assert reverse_flow == 0
                circulation += (
                    forward_flow
                    * (g[row] + g[col])
                    * (psi[col] - psi[row])
                    / 2
                )
    assert L - symmetric_pairing == circulation

    statewise_symmetric_residual = []
    for row in range(len(states)):
        correction = sum(
            ((Qs[row][col] - QP[row][col]) * psi[col]
             for col in range(len(states))),
            F(0),
        )
        statewise_symmetric_residual.append(conditional_V[row] - correction)

    assert L == expected["L"]
    assert V == expected["V"]
    assert symmetric_pairing == expected["S"]
    for state, value in expected.get("symmetric_state_residuals", {}).items():
        assert statewise_symmetric_residual[states.index(state)] == value
    assert L == sum(
        (
            pi[row]
            * sum(
                ((QK[row][col] - QP[row][col]) * psi[col]
                 for col in range(len(states))),
                F(0),
            )
            for row in range(len(states))
        ),
        F(0),
    )

    with localcontext() as context:
        context.prec = 80
        logg = [decimal(value).ln() for value in g]

        # I=-<pi,Q_K log g>.  The second expression is its exact directed
        # Bregman representation; equality is checked to high precision.
        fisher = Decimal(0)
        bregman = Decimal(0)
        entropy_forcing = Decimal(0)
        for row in range(len(states)):
            for col in range(len(states)):
                if row == col or not QK[row][col]:
                    continue
                flow = decimal(piK[row] * QK[row][col])
                fisher -= decimal(pi[row] * QK[row][col]) * (
                    logg[col] - logg[row]
                )
                bregman += flow * (
                    decimal(g[row]) * (logg[row] - logg[col])
                    - decimal(g[row])
                    + decimal(g[col])
                )
                entropy_forcing += decimal(
                    pi[row] * (QP[row][col] - QK[row][col])
                ) * (logg[col] - logg[row])
        tolerance = Decimal(10) ** -65
        assert abs(fisher - bregman) < tolerance
        assert abs(fisher - entropy_forcing) < tolerance
        assert fisher >= 0

        # Sharp Fenchel--Young generator bound.  For every lambda>0,
        #   L=<g,Q_K psi>_K
        #     <= I/lambda + R(lambda)/lambda,
        # where R is the exponential directed-flow remainder below.
        # The sign convention uses Delta psi = psi_B-psi_A.
        def young_bound(lam: Decimal):
            remainder = Decimal(0)
            for row in range(len(states)):
                for col in range(len(states)):
                    if row == col or not QK[row][col]:
                        continue
                    flow = decimal(piK[row] * QK[row][col])
                    delta = decimal(psi[col] - psi[row])
                    remainder += flow * decimal(g[col]) * (
                        (lam * delta).exp() - 1
                    )
            return (fisher + remainder) / lam, remainder

        candidates = []
        # Dense deterministic scan is enough to determine whether the sharp
        # one-parameter Fenchel bound even reaches V on the exact witnesses.
        for numerator in range(1, 4097):
            lam = Decimal(numerator) / Decimal(64)
            bound, remainder = young_bound(lam)
            candidates.append((bound, lam, remainder))
        best_bound, best_lam, best_remainder = min(candidates)

        print(f"[{label}] n={n}")
        print(
            "  nonreversible edge A,B,forward,reverse = "
            f"{nonreversible}"
        )
        print(f"  L={L} ({decimal(L):.20E})")
        print(f"  V={V} ({decimal(V):.20E})")
        print(
            "  event Pinsker lower bound="
            f"{event_pinsker_lower_bound} "
            f"({decimal(event_pinsker_lower_bound):.20E}); "
            f"event chi-square={event_chi_square}"
        )
        print(f"  I_K(g)={fisher:.20E}")
        print(f"  chi-Fisher={chi_fisher} ({decimal(chi_fisher):.20E})")
        print(f"  psi-energy={psi_energy} ({decimal(psi_energy):.20E})")
        print(
            f"  symmetric pairing={symmetric_pairing} "
            f"({decimal(symmetric_pairing):.20E}); circulation L-sym="
            f"{L-symmetric_pairing}"
        )
        print(f"  L/I={decimal(L)/fisher:.20E}")
        print(f"  V/I={decimal(V)/fisher:.20E}")
        print(
            "  best sampled Young bound="
            f"{best_bound:.20E} at lambda={best_lam:.8E}; "
            f"remainder={best_remainder:.20E}"
        )
        print(f"  bound/V={best_bound/decimal(V):.20E}")


def audit_directed_counterexample():
    """An exact positive-support directed kernel with L>S.

    This does not lie in the undirected graph class.  It proves that the
    circulation sign cannot follow from subset-chain stationarity alone.
    """
    rows = [
        [0, 100, 300, 3, 30],
        [10, 0, 30, 30, 100],
        [100, 3, 0, 1000, 1000],
        [300, 1, 3, 0, 1],
        [3, 30, 3, 10, 0],
    ]
    n = len(rows)
    N = n - 1
    P = [
        [F(rows[v][u], sum(rows[v])) for u in range(n)] for v in range(n)
    ]
    states, QP = proper_generator(P)
    pi = stationary(QP)
    complete_P = [
        [F(0) if u == v else F(1, N) for u in range(n)] for v in range(n)
    ]
    _, QK = proper_generator(complete_P)
    piK = [
        F(n - popcount(state), n * (2 ** (n - 1) - 1)) for state in states
    ]
    g = [pi[row] / piK[row] for row in range(len(states))]
    L, V, _, _, psi = green_data(rows, P, states, QK, pi)
    S = -sum(
        (
            piK[row]
            * QK[row][col]
            * (g[col] - g[row])
            * (psi[col] - psi[row])
            for row in range(len(states))
            for col in range(len(states))
            if row != col
        ),
        F(0),
    ) / 2
    assert L - S > 0
    assert S < V
    print(
        "PASS: exact directed counterexample to L<=S; "
        f"L-S={L-S} (~{float(L-S):.8g})"
    )


def audit_rank_collapse():
    """Check the exact Green-coefficient rank identity in (20).

    The manuscript proof uses the complete count-chain Green equation.
    These rational checks are an independent finite replay of its explicit
    binomial form, not a proof for all n.
    """
    for n in range(3, 13):
        N = n - 1
        coefficients = complete_green_coefficients(n)
        rhoK = F((n - 1) * 2 ** (n - 2), n * (2 ** (n - 1) - 1))
        for size in range(1, n):
            holes = n - size
            complete_hits = sum(
                (
                    coefficients[k]
                    * F(2 * k, N + k)
                    * comb(holes, k)
                    for k in range(1, n)
                ),
                F(0),
            )
            stationary_elimination = sum(
                (
                    coefficients[k]
                    * sum(
                        (
                            F((-1) ** (k - 1 - j)) * comb(holes, j)
                            for j in range(k)
                        ),
                        F(0),
                    )
                    for k in range(1, n)
                ),
                F(0),
            )
            assert size * (complete_hits - stationary_elimination) == (
                rhoK - F(size, n)
            )
    print("PASS: exact Green-coefficient rank collapse for 3<=n<=12")


def audit_original_edge_decomposition():
    """Verify the pair-Poisson expansion and refute a termwise edge sign."""
    # Vertex 0 is the middle of the path; its incident weights are 1 and 4.
    weights = [[0, 1, 4], [1, 0, 0], [4, 0, 0]]
    n = len(weights)
    N = n - 1
    P = transition(weights)
    states, QP = proper_generator(P)
    pi = stationary(QP)
    complete_P = [
        [F(0) if u == v else F(1, N) for u in range(n)] for v in range(n)
    ]
    _, QK = proper_generator(complete_P)
    piK = [
        F(n - popcount(state), n * (2 ** (n - 1) - 1)) for state in states
    ]
    Qstar = [
        [piK[col] * QK[col][row] / piK[row] for col in range(len(states))]
        for row in range(len(states))
    ]
    Qa = [
        [(QK[row][col] - Qstar[row][col]) / 2 for col in range(len(states))]
        for row in range(len(states))
    ]
    coefficients = complete_green_coefficients(n)
    U = [F(0)] * n
    for holes in range(1, n):
        U[holes] = sum(
            (
                coefficients[k]
                * F(2 * N * N, (N + k) ** 2)
                * comb(holes - 1, k - 1)
                for k in range(1, holes + 1)
            ),
            F(0),
        )

    terms = {}
    for u in range(n):
        for v in range(u + 1, n):
            forcing = []
            for state in states:
                size = popcount(state)
                contains_pair = bool((state >> u) & 1 and (state >> v) & 1)
                forcing.append(
                    U[n - size]
                    * (F(int(contains_pair)) - F(size * (size - 1), n * N))
                )
            assert sum(
                (piK[row] * forcing[row] for row in range(len(states))), F(0)
            ) == 0
            matrix = [row[:] for row in QK]
            rhs = forcing[:]
            matrix[-1] = [F(0)] * len(states)
            matrix[-1][0] = F(1)
            rhs[-1] = F(0)
            eta = solve(matrix, rhs)
            assert matvec(QK, eta) == forcing
            observable = matvec(Qa, eta)
            theta = sum(
                (pi[row] * observable[row] for row in range(len(states))), F(0)
            )
            b = F(2, N) - P[u][v] - P[v][u]
            terms[(u, v)] = b * theta

    assert terms == {
        (0, 1): F(4, 13365),
        (0, 2): F(-64, 13365),
        (1, 2): F(-4, 891),
    }
    assert sum(terms.values(), F(0)) == F(-8, 891)
    assert terms[(0, 1)] > 0
    print(
        "PASS: original-pair circulation expansion; termwise sign is false "
        "on path (1,4)"
    )


def audit_undirected_split_counterexample():
    """Exact connected undirected counterexample to the auxiliary L<=S."""
    # Complete-support edge weights in lexicographic order
    # 01,02,03,04,05,12,13,14,15,23,24,25,34,35,45.
    edge_weights = [3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1]
    n = 6
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (u, v) in zip(edge_weights, combinations(range(n), 2)):
        weights[u][v] = weights[v][u] = value
    P = transition(weights)
    states, QP = proper_generator(P)
    pi = stationary(QP)
    N = n - 1
    complete_P = [
        [F(0) if u == v else F(1, N) for u in range(n)] for v in range(n)
    ]
    _, QK = proper_generator(complete_P)
    piK = [
        F(n - popcount(state), n * (2 ** (n - 1) - 1)) for state in states
    ]
    g = [pi[row] / piK[row] for row in range(len(states))]
    L, V, _, _, psi = green_data(weights, P, states, QK, pi)

    # A graph-independent scalar sandwich through the full event
    # chi-square cannot work either.  The regular K4 would require
    # alpha >= L_K4/Chi_K4, while this n=6 witness requires
    # alpha <= V_6/Chi_6.  The two exact rational bounds cross.
    _, TP = event_kernel(P)
    _, TK = event_kernel(complete_P)
    event_chi = sum(
        (
            pi[row] * (TP[row][col] - TK[row][col]) ** 2 / TK[row][col]
            for row in range(len(states))
            for col in range(len(states))
            if TK[row][col]
        ),
        F(0),
    )
    k4_required_alpha = F(207, 22960) / F(82543, 387450)
    n6_allowed_alpha = V / event_chi
    assert k4_required_alpha > n6_allowed_alpha
    S = -sum(
        (
            piK[row]
            * QK[row][col]
            * (g[col] - g[row])
            * (psi[col] - psi[row])
            for row in range(len(states))
            for col in range(len(states))
            if row != col
        ),
        F(0),
    ) / 2
    assert L - S > 0
    assert L - V < 0
    print(
        "PASS: exact undirected n=6 counterexample to L<=S; "
        f"L-S~{float(L-S):.8g}, while L-V~{float(L-V):.8g}"
    )
    print(
        "PASS: exact event-chi scalar sandwich obstruction; "
        f"K4 requires alpha>={float(k4_required_alpha):.8g}, "
        f"n6 requires alpha<={float(n6_allowed_alpha):.8g}"
    )


def main():
    audit_rank_collapse()
    audit(
        "weighted path (1,2)",
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        {
            "L": F(2, 135),
            "S": F(1, 45),
            "V": F(8, 135),
            "event_pinsker": F(8051, 18000),
            "event_chi": F(4293, 4000),
            "symmetric_state_residuals": {
                2: F(-13, 990),
                3: F(-4, 495),
            },
        },
    )
    audit(
        "regular weighted K4",
        [[0, 1, 1, 2], [1, 0, 2, 1], [1, 2, 0, 1], [2, 1, 1, 0]],
        {
            "L": F(207, 22960),
            "S": F(207, 22960),
            "V": F(247, 22960),
            "event_pinsker": F(65753, 774900),
            "event_chi": F(82543, 387450),
        },
    )
    audit_directed_counterexample()
    audit_original_edge_decomposition()
    audit_undirected_split_counterexample()
    print("PASS: exact likelihood/Fisher identities and witness diagnostics")


if __name__ == "__main__":
    main()
