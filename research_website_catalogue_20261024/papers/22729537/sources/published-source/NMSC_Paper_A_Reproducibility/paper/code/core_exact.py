from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence
import sympy as sp


def moment_of_atoms(weights: Sequence[sp.Rational], atoms: Sequence[sp.Rational], k: int) -> sp.Expr:
    return sp.simplify(sum(w * a**k for w, a in zip(weights, atoms)))


def lower_moment_from_length_L(words: dict[tuple[int, ...], sp.Expr], prefix: tuple[int, ...], alphabet_size: int, L: int) -> sp.Expr:
    if len(prefix) > L:
        raise ValueError("prefix longer than L")
    total = sp.Integer(0)
    tail_len = L - len(prefix)
    if tail_len == 0:
        return words[prefix]
    from itertools import product
    for tail in product(range(alphabet_size), repeat=tail_len):
        total += words[prefix + tail]
    return sp.simplify(total)


def prefix_state(s: sp.Expr) -> sp.Matrix:
    """Row state (1,s) from exp([[0,1],[0,0]] s) and an identity mark."""
    return sp.Matrix([[1, s]])


def span_coefficients_for_later() -> tuple[sp.Rational, sp.Rational]:
    a, b = sp.symbols("a b")
    sol = sp.solve([
        sp.Eq(a + b, 1),
        sp.Eq(sp.Rational(1, 4) * a + sp.Rational(3, 4) * b, sp.Rational(3, 2)),
    ], [a, b], dict=True)[0]
    return sp.Rational(sol[a]), sp.Rational(sol[b])


def divided_difference_two(A: sp.Expr, B: sp.Expr, Delta: sp.Expr) -> sp.Expr:
    if sp.simplify(A - B) == 0:
        return sp.simplify(Delta * sp.exp(-A * Delta))
    return sp.simplify((sp.exp(-B * Delta) - sp.exp(-A * Delta)) / (A - B))


def simplex_equal_rate(m: int, A: sp.Expr, Delta: sp.Expr) -> sp.Expr:
    return sp.simplify(Delta**m / sp.factorial(m) * sp.exp(-A * Delta))


def biunary_kernel(gamma: sp.Expr, lam: sp.Expr, Delta: sp.Expr) -> sp.Matrix:
    e = sp.exp(-lam * Delta)
    return sp.Matrix([[1 - gamma + gamma * e, gamma * (1 - e)], [0, 1]])


def pair_port_survival(
    gamma: sp.Expr,
    lambda_1: sp.Expr,
    lambda_2: sp.Expr,
    time: sp.Expr,
) -> sp.Expr:
    """Two independently routed surviving blocks on a first parent chamber."""
    return sp.expand(
        2 * gamma * (1 - gamma)
        + gamma**2 * sp.exp(-lambda_1 * time)
        + (1 - gamma) ** 2 * sp.exp(-lambda_2 * time)
    )


def balanced_suffix_responses(
    gamma: sp.Expr,
    boundary_base: sp.Expr,
    first_rates: tuple[sp.Expr, sp.Expr],
    suffix_rates: tuple[sp.Expr, sp.Expr],
    suffix_base: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    """Survival/density before and after exchanging two continuation words."""
    a, b = first_rates
    c, d = suffix_rates
    w_1 = sp.simplify(gamma**2 * boundary_base**a)
    w_2 = sp.simplify((1 - gamma) ** 2 * boundary_base**b)
    split = 2 * gamma * (1 - gamma)
    survival = sp.expand(split + w_1 * suffix_base**c + w_2 * suffix_base**d)
    swapped_survival = sp.expand(
        split + w_1 * suffix_base**d + w_2 * suffix_base**c
    )
    density = sp.expand(w_1 * c * suffix_base**c + w_2 * d * suffix_base**d)
    swapped_density = sp.expand(
        w_1 * d * suffix_base**d + w_2 * c * suffix_base**c
    )
    return survival, swapped_survival, density, swapped_density


def normalize_rank_one_kernel(
    kernel: sp.Matrix,
    completion_weights: Sequence[sp.Expr] | None = None,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return the canonical entry column and all-completions-normalized future row.

    Columns are observable suffix cylinders.  ``completion_weights`` specifies
    their all-completions union and defaults to the columnwise sum.  No latent
    state or physical-port identifier enters the normalization.
    """
    if kernel.rows == 0 or kernel.cols == 0:
        raise ValueError("kernel must be nonempty")
    if kernel.rank() != 1:
        raise ValueError("kernel must have rank one")
    if completion_weights is None:
        weights = sp.ones(kernel.cols, 1)
    else:
        if len(completion_weights) != kernel.cols:
            raise ValueError("one completion weight is required per column")
        weights = sp.Matrix([sp.sympify(value) for value in completion_weights])
    alpha = (kernel * weights).applyfunc(sp.simplify)
    pivot = next(
        (row for row in range(kernel.rows) if sp.simplify(alpha[row]) != 0),
        None,
    )
    if pivot is None:
        raise ValueError("all-completions mass must be nonzero")
    beta = (kernel.row(pivot) / alpha[pivot]).applyfunc(sp.simplify)
    residual = (kernel - alpha * beta).applyfunc(sp.simplify)
    if residual != sp.zeros(kernel.rows, kernel.cols):
        raise ValueError("rank-one reconstruction failed")
    if sp.simplify((beta * weights)[0] - 1) != 0:
        raise ValueError("future factor is not normalized")
    return alpha, beta


def piecewise_rate_integral(
    rate_segments: Sequence[tuple[sp.Expr, sp.Expr, sp.Expr]],
    start: sp.Expr,
    end: sp.Expr,
) -> sp.Expr:
    """Integrate an exact piecewise-constant rate over a covered interval."""
    start = sp.sympify(start)
    end = sp.sympify(end)
    if not bool(end >= start):
        raise ValueError("end must not precede start")
    total = sp.Integer(0)
    covered = sp.Integer(0)
    for raw_left, raw_right, raw_rate in rate_segments:
        left = sp.sympify(raw_left)
        right = sp.sympify(raw_right)
        rate = sp.sympify(raw_rate)
        overlap_left = max(start, left)
        overlap_right = min(end, right)
        if bool(overlap_right > overlap_left):
            width = overlap_right - overlap_left
            total += rate * width
            covered += width
    if sp.simplify(covered - (end - start)) != 0:
        raise ValueError("rate segments must cover the requested interval")
    return sp.simplify(total)


def rate_at(
    rate_segments: Sequence[tuple[sp.Expr, sp.Expr, sp.Expr]],
    time: sp.Expr,
) -> sp.Expr:
    """Return the right-continuous exact rate at an interior merger time."""
    time = sp.sympify(time)
    for raw_left, raw_right, raw_rate in rate_segments:
        left = sp.sympify(raw_left)
        right = sp.sympify(raw_right)
        if bool(left <= time < right):
            return sp.sympify(raw_rate)
    raise ValueError("merger time is outside the rate word")


def kingman_word_density(
    rate_segments: Sequence[tuple[sp.Expr, sp.Expr, sp.Expr]],
    start: sp.Expr,
    end: sp.Expr,
    merger_times: Sequence[sp.Expr],
    initial_block_count: int,
) -> sp.Expr:
    """Density of one specified labelled Kingman merger word.

    The survival exponent uses all current pairs, while each specified target
    pair contributes one instantaneous pair-rate factor.
    """
    if initial_block_count < 1:
        raise ValueError("initial_block_count must be positive")
    times = [sp.sympify(value) for value in merger_times]
    start = sp.sympify(start)
    end = sp.sympify(end)
    if len(times) >= initial_block_count:
        raise ValueError("too many mergers for the initial partition")
    if any(not bool(start < value < end) for value in times):
        raise ValueError("merger times must be strictly interior")
    if any(not bool(left < right) for left, right in zip(times, times[1:])):
        raise ValueError("merger times must be strictly ordered")

    density = sp.Integer(1)
    block_count = initial_block_count
    previous = start
    for event_time in [*times, end]:
        integrated = piecewise_rate_integral(rate_segments, previous, event_time)
        density *= sp.exp(-sp.binomial(block_count, 2) * integrated)
        if event_time != end:
            density *= rate_at(rate_segments, event_time)
            block_count -= 1
        previous = event_time
    return sp.simplify(density)


def continuation_cocycle_residual(
    observed_word_future: sp.Matrix,
    kingman_density: sp.Expr,
    terminal_future: sp.Matrix,
) -> sp.Matrix:
    """Observable residual for beta_s(word A)=K beta_t(A)."""
    if observed_word_future.shape != terminal_future.shape:
        raise ValueError("future columns must have the same shape")
    return (
        observed_word_future - sp.sympify(kingman_density) * terminal_future
    ).applyfunc(sp.simplify)


def spanning_cocycle_residual(
    left_word_density: sp.Expr,
    right_word_density: sp.Expr,
    spanning_word_density: sp.Expr,
) -> sp.Expr:
    """Residual that detects omission of a cross-boundary word check."""
    return sp.simplify(
        sp.sympify(spanning_word_density)
        - sp.sympify(left_word_density) * sp.sympify(right_word_density)
    )


def gauge_invariants(tau: sp.Expr, lam: sp.Expr, Q: sp.Matrix, c: sp.Expr) -> tuple[sp.Matrix, sp.Expr]:
    tau2, lam2, Q2 = c * tau, lam / c, Q / c
    return sp.simplify(Q2 * tau2), sp.simplify(lam2 * tau2)


def reachable_observable_reduction(A: sp.Matrix, alpha: sp.Matrix, beta: sp.Matrix) -> tuple[int, int, int]:
    """Return ambient, reachable rank, Hankel rank for a single-type linear system."""
    n = A.rows
    rows = [alpha * (A**k) for k in range(n)]
    cols = [(A**k) * beta for k in range(n)]
    R = sp.Matrix.vstack(*rows).rank()
    O = sp.Matrix.hstack(*cols).rank()
    H = sp.Matrix([[sp.simplify((rows[i] * cols[j])[0]) for j in range(n)] for i in range(n)]).rank()
    return n, R, H


def determinant_distance(Q: sp.Matrix, pi: Sequence[sp.Expr], u: sp.Expr, w: sp.Expr) -> sp.Expr:
    D = sp.diag(*pi)
    J = (Q.T * u).exp() * D * (Q * w).exp()
    return sp.simplify(-sp.log(sp.det(D.inv() * J)))


def moment_tensor_probability(v: Sequence[sp.Expr], word: Sequence[int]) -> sp.Expr:
    out = sp.Integer(1)
    for i in word:
        out *= v[i]
    return sp.expand(out)
