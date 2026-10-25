"""Executable incorrect formulas used as independent negative controls."""

from __future__ import annotations

import sympy as sp


def wrong_divided_difference(a: sp.Expr, b: sp.Expr, delta: sp.Expr) -> sp.Expr:
    return (sp.exp(-a * delta) - sp.exp(-b * delta)) / (a - b)


def unscaled_determinant_coordinate(joint: sp.Matrix) -> sp.Expr:
    return -sp.log(joint.det())


def literal_prefix_only(target: sp.Matrix, earlier_rows: list[sp.Matrix]) -> bool:
    return any(target == row for row in earlier_rows)


def omit_mixed_funnel_routes(gamma: sp.Expr) -> sp.Expr:
    return gamma**2 + (1 - gamma) ** 2


def wrong_scaled_hazard(rate: sp.Expr, time: sp.Expr, scale: sp.Expr) -> sp.Expr:
    return (rate * scale) * (time * scale)


def duplicate_vandermonde_node(nodes: list[sp.Expr]) -> list[sp.Expr]:
    return [nodes[0], nodes[0], *nodes[2:]]


def jacobian_kernel_is_exact_tangent() -> bool:
    x = sp.symbols("x")
    return sp.diff(x**2, x).subs(x, 0) == 0


def balanced_switch_requires_equal_suffixes(
    suffix_1: sp.Expr, suffix_2: sp.Expr
) -> bool:
    """Wrongly ignores equality of the actual posterior-weighted mixture."""
    return sp.simplify(suffix_1 - suffix_2) == 0


def cocycle_all_completions_only(residual: sp.Matrix) -> bool:
    """Wrongly accepts a column error whenever its total mass cancels."""
    return sp.simplify(sum(residual)) == 0


def cocycle_empty_word_only(empty_word_residual: sp.Matrix) -> bool:
    """Wrongly treats the no-merger word as the entire continuation test."""
    return empty_word_residual == sp.zeros(*empty_word_residual.shape)


def cocycle_aggregate_target_pairs(
    first_target_future: sp.Matrix,
    second_target_future: sp.Matrix,
) -> bool:
    """Wrongly discards the label of the first merger target pair."""
    return sp.simplify(sum(first_target_future) - sum(second_target_future)) == 0


def cocycle_check_sides_without_spanning(
    left_side_passes: bool,
    right_side_passes: bool,
) -> bool:
    """Wrongly infers gluing from separate one-sided checks."""
    return left_side_passes and right_side_passes


def cocycle_accept_physical_port_id(
    left_port_id: str,
    right_port_id: str,
) -> bool:
    """Wrongly substitutes a latent population identifier for a law test."""
    return left_port_id == right_port_id


def multicut_entry_is_product_of_port_marginals(
    joint_entry_table: sp.Matrix,
) -> bool:
    """Wrongly requires a joint entry mass to factor across incident ports."""
    return joint_entry_table.rank() == 1
