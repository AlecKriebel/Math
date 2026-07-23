#!/usr/bin/env python3
"""Mechanically check the reduction of the fixed-q repair to empty TU(41).

This script verifies the new, elementary part of the obstruction:

* the exact edge decomposition induced by Eliahou's fixed q;
* the product-parity telescope forcing the reversal signs of X and Y;
* the decimation identity producing a Turyn base sequence in BS(42, 41).

It does not re-run the published exhaustive classification that excludes
TU(41).  That literature dependency is cited in FIXED_Q_OBSTRUCTION.md.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Sequence

from seed import ELIAHOU_Q, fixed_q_edges


Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]
SignedVariable = tuple[int, str]


class ParityUnionFind:
    """Union-find for constraints value(left) XOR value(right) = parity."""

    def __init__(self, names: Iterable[str]) -> None:
        self.parent = {name: name for name in names}
        self.rank = {name: 0 for name in names}
        self.xor_to_parent = {name: 0 for name in names}

    def find(self, name: str) -> tuple[str, int]:
        parent = self.parent[name]
        if parent == name:
            return name, 0
        root, parent_parity = self.find(parent)
        parity = self.xor_to_parent[name] ^ parent_parity
        self.parent[name] = root
        self.xor_to_parent[name] = parity
        return root, parity

    def constrain(self, left: str, right: str, parity: int) -> None:
        left_root, left_parity = self.find(left)
        right_root, right_parity = self.find(right)
        if left_root == right_root:
            if left_parity ^ right_parity != parity:
                raise AssertionError("inconsistent parity constraints")
            return

        link_parity = left_parity ^ right_parity ^ parity
        if self.rank[left_root] < self.rank[right_root]:
            self.parent[left_root] = right_root
            self.xor_to_parent[left_root] = link_parity
        else:
            self.parent[right_root] = left_root
            self.xor_to_parent[right_root] = link_parity
            if self.rank[left_root] == self.rank[right_root]:
                self.rank[left_root] += 1

    def parity_between(self, left: str, right: str) -> int:
        left_root, left_parity = self.find(left)
        right_root, right_parity = self.find(right)
        if left_root != right_root:
            raise AssertionError(f"{left} and {right} are not connected")
        return left_parity ^ right_parity


def expected_fixed_q_edges(lag: int) -> tuple[tuple[int, int], ...]:
    edges: list[tuple[int, int]] = []
    if lag < 83:
        edges.extend((index, index + lag) for index in range(83 - lag))
    if lag < 81:
        edges.extend((85 + index, 85 + index + lag) for index in range(81 - lag))
    if lag == 82:
        edges.append((84, 166))
    return tuple(edges)


def verify_edge_decomposition() -> None:
    for lag in range(1, 167):
        actual = fixed_q_edges(lag, ELIAHOU_Q)
        expected = expected_fixed_q_edges(lag)
        if actual != expected:
            raise AssertionError(f"fixed-q edge mismatch at lag {lag}")


def lag_product_mask(length: int, lag: int, offset: int) -> int:
    """Product of every correlation term, represented modulo squares."""

    mask = 0
    if lag >= length:
        return mask
    for index in range(length - lag):
        mask ^= 1 << (offset + index)
        mask ^= 1 << (offset + index + lag)
    return mask


def verify_product_telescope() -> None:
    # P_k is the product of every individual term in c_k(X)+c_k(Y), with
    # the Y product empty at k=81.  A zero sum at lag k has 82-k negative
    # terms, so sign(P_k)=(-1)^k for 1 <= k <= 81; P_0=+1 as well.
    masks = [
        lag_product_mask(83, lag, 0) ^ lag_product_mask(81, lag, 83)
        for lag in range(82)
    ]
    for lag in range(82):
        term_count = max(83 - lag, 0) + max(81 - lag, 0)
        if term_count != 2 * (82 - lag):
            raise AssertionError(f"wrong term count at lag {lag}")
        product_sign_bit = 0 if lag == 0 else (term_count // 2) % 2
        if product_sign_bit != lag % 2:
            raise AssertionError(f"wrong product parity at lag {lag}")

    # P_{i+1}/P_i contains only the four reflected endpoint variables.
    for index in range(81):
        expected = (
            (1 << index)
            ^ (1 << (82 - index))
            ^ (1 << (83 + index))
            ^ (1 << (83 + 80 - index))
        )
        if masks[index] ^ masks[index + 1] != expected:
            raise AssertionError(f"telescope support mismatch at index {index}")


def verify_forced_reversal_signs() -> None:
    names = (
        ["constant"]
        + [f"r_{index}" for index in range(83)]
        + [f"t_{index}" for index in range(81)]
    )
    system = ParityUnionFind(names)

    # r_i=x_i*x_{82-i}, t_i=y_i*y_{80-i}.  Bit 1 denotes a negative sign.
    for index in range(83):
        system.constrain(f"r_{index}", f"r_{82 - index}", 0)
    for index in range(81):
        system.constrain(f"t_{index}", f"t_{80 - index}", 0)
        system.constrain(f"r_{index}", f"t_{index}", 1)

    # The two central reflected products are squares.
    system.constrain("r_41", "constant", 0)
    system.constrain("t_40", "constant", 0)

    for index in range(83):
        expected = (index + 1) % 2  # r_i=(-1)^(i+1)
        actual = system.parity_between(f"r_{index}", "constant")
        if actual != expected:
            raise AssertionError(f"wrong forced sign for r_{index}")
    for index in range(81):
        expected = index % 2  # t_i=(-1)^i
        actual = system.parity_between(f"t_{index}", "constant")
        if actual != expected:
            raise AssertionError(f"wrong forced sign for t_{index}")


def multiply(left: SignedVariable, right: SignedVariable) -> tuple[int, Monomial]:
    coefficient = left[0] * right[0]
    if left[1] == right[1]:
        return coefficient, ()
    return coefficient, tuple(sorted((left[1], right[1])))


def correlation_polynomial(sequence: Sequence[SignedVariable], lag: int) -> Polynomial:
    result: defaultdict[Monomial, int] = defaultdict(int)
    for index in range(len(sequence) - lag):
        coefficient, monomial = multiply(sequence[index], sequence[index + lag])
        result[monomial] += coefficient
    return {monomial: value for monomial, value in result.items() if value}


def add_polynomials(*polynomials: Polynomial) -> Polynomial:
    result: defaultdict[Monomial, int] = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {monomial: value for monomial, value in result.items() if value}


def generic_reversal_sequences() -> tuple[
    list[SignedVariable],
    list[SignedVariable],
    SignedVariable,
    SignedVariable,
]:
    x: list[SignedVariable] = [(0, "") for _ in range(83)]
    for index in range(42):
        x[index] = (1, f"x_{index}")
    for index in range(42, 83):
        mirror = 82 - index
        x[index] = ((-1) ** (mirror + 1), f"x_{mirror}")

    y: list[SignedVariable] = [(0, "") for _ in range(81)]
    for index in range(41):
        y[index] = (1, f"y_{index}")
    for index in range(41, 81):
        mirror = 80 - index
        y[index] = ((-1) ** mirror, f"y_{mirror}")

    u = (1, "u")
    v = (1, "u")  # u*v=+1, hence v=u for signs.
    return x, y, u, v


def negate(variable: SignedVariable) -> SignedVariable:
    return -variable[0], variable[1]


def verify_decimation_to_turyn() -> None:
    x, y, u, v = generic_reversal_sequences()
    e = x[0::2]
    o = x[1::2]
    p = y[0::2]
    q = y[1::2]
    b = [u, *q, v]

    if len(e) != 42 or len(b) != 42 or len(o) != 41 or len(p) != 41:
        raise AssertionError("wrong BS(42,41) sequence lengths")
    if list(reversed(e)) != [negate(value) for value in e]:
        raise AssertionError("E is not symbolically skew-symmetric")
    if list(reversed(o)) != o or list(reversed(p)) != p:
        raise AssertionError("O and P are not symbolically symmetric")

    # For lags 1..40, the base-sequence correlation sum is exactly the
    # even-lag fixed-q equation c_{2k}(X)+c_{2k}(Y).
    for lag in range(1, 41):
        base = add_polynomials(
            correlation_polynomial(e, lag),
            correlation_polynomial(b, lag),
            correlation_polynomial(o, lag),
            correlation_polynomial(p, lag),
        )
        original = add_polynomials(
            correlation_polynomial(x, 2 * lag),
            correlation_polynomial(y, 2 * lag),
        )
        if base != original:
            raise AssertionError(f"decimation identity failed at lag {lag}")

    # At lag 41, only E and B contribute, reproducing x_0*x_82+u*v.
    base_41 = add_polynomials(
        correlation_polynomial(e, 41), correlation_polynomial(b, 41)
    )
    original_82 = add_polynomials(
        correlation_polynomial(x, 82),
        correlation_polynomial([u, v], 1),
    )
    if base_41 != original_82:
        raise AssertionError("endpoint identity failed at lag 41")


def main() -> int:
    verify_edge_decomposition()
    print("PASS fixed-q edge decomposition")
    verify_product_telescope()
    print("PASS product-parity telescope")
    verify_forced_reversal_signs()
    print("PASS forced reversal signs")
    verify_decimation_to_turyn()
    print("PASS symbolic reduction to TU(41) in BS(42,41)")
    print("PASS mechanically checkable reduction to TU(41)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
