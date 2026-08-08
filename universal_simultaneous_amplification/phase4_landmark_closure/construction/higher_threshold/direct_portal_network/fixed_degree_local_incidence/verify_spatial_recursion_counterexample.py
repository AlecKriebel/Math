#!/usr/bin/env python3
"""Exact audit of the fixed-degree local recursion and cavity failure.

The true C4 subset resolvent is constructed from rational atomic rates.  Its
singleton transform is then substituted into the independent-descendant
quadratic inherited from the diffuse limit.  A nonzero exact residual proves
that this tempting local closure is false once portal edges retain order-one
weight.
"""

from __future__ import annotations

import sympy as sp


def checked_zero(expression, label, verbose=True):
    value = sp.factor(sp.cancel(expression))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    if verbose:
        print("PASS", label)


def exact_cycle_transform(rule, r, blade_load, portal_load, z, q=6):
    degree = 2
    edge = portal_load / degree
    total_degree = blade_load + portal_load
    states = (1 << q) - 1
    matrix = sp.zeros(states)
    rhs = sp.zeros(states, 1)

    def neighbors(a):
        return ((a - 1) % q, (a + 1) % q)

    for mask in range(1, 1 << q):
        row = mask - 1
        active = [a for a in range(q) if mask >> a & 1]
        transitions = []
        if rule == "Bd":
            for a in active:
                mutant_neighbors = sum(mask >> b & 1 for b in neighbors(a))
                transitions.append((
                    mask ^ (1 << a),
                    blade_load
                    + (degree - mutant_neighbors) * edge / total_degree,
                ))
            for b in range(q):
                if not (mask >> b & 1):
                    mutant_neighbors = sum(mask >> a & 1 for a in neighbors(b))
                    transitions.append((
                        mask | (1 << b),
                        r * mutant_neighbors * edge / total_degree,
                    ))
            killing = (
                len(active) * r**2 * blade_load
                / ((r + 1) * total_degree) * (1 - z)
            )
        elif rule == "dB":
            for a in active:
                mutant_neighbors = sum(mask >> b & 1 for b in neighbors(a))
                resident = blade_load + (degree - mutant_neighbors) * edge
                transitions.append((
                    mask ^ (1 << a),
                    resident / (resident + r * mutant_neighbors * edge),
                ))
            for b in range(q):
                if not (mask >> b & 1):
                    mutant_neighbors = sum(mask >> a & 1 for a in neighbors(b))
                    transitions.append((
                        mask | (1 << b),
                        r * mutant_neighbors * edge
                        / (blade_load + (degree - mutant_neighbors) * edge
                           + r * mutant_neighbors * edge),
                    ))
            killing = len(active) * r * blade_load / 2 * (1 - z)
        else:
            raise ValueError(rule)

        matrix[row, row] = killing + sum(rate for _, rate in transitions)
        rhs[row] = killing
        for nxt, rate in transitions:
            if nxt:
                matrix[row, nxt - 1] -= rate

        checked_zero(
            matrix[row, row]
            + sum(matrix[row, column] for column in range(states)
                  if column != row)
            - killing
            - sum(rate for nxt, rate in transitions if nxt == 0),
            f"{rule} C{q} row balance {mask}",
            verbose=False,
        )

    hitting = matrix.inv() * rhs
    transforms = [sp.factor(1 - hitting[(1 << a) - 1]) for a in range(q)]
    for value in transforms[1:]:
        checked_zero(value - transforms[0], f"{rule} C{q} singleton symmetry",
                     verbose=False)
    print("PASS", rule, f"C{q}", "all row balances and singleton symmetries")
    return transforms[0]


def main():
    blade_load = sp.Integer(1)
    portal_load = sp.Integer(1)
    total_degree = blade_load + portal_load
    failures = []

    # At the Bd test mark, a product ansatz r^(-|A|) has an exact residual
    # that exposes the knife edge d=B+H=1 on every regular portal graph.
    r_symbol, size, boundary, B_symbol, d_symbol = sp.symbols(
        "r size boundary B d", positive=True
    )
    candidate = 1 / r_symbol
    loss = size * B_symbol + boundary / d_symbol
    gain = r_symbol * boundary / d_symbol
    retained_child = size * (r_symbol - 1) * B_symbol / d_symbol
    product_residual = sp.factor(
        loss * (1 - 1 / candidate)
        + gain * (1 - candidate)
        + retained_child
    )
    checked_zero(
        product_residual
        - (r_symbol - 1) * size * B_symbol * (1 / d_symbol - 1),
        "universal Bd product residual",
    )
    checked_zero(product_residual.subs(d_symbol, 1),
                 "universal Bd degree-one product harmonicity")

    for r in (sp.Rational(3, 2), sp.Rational(31, 20)):
        for rule in ("Bd", "dB"):
            z = 1 / r**2 if rule == "Bd" else (2 - r) / r
            exact = exact_cycle_transform(
                rule, r, blade_load, portal_load, z
            )

            # The false cavity closure treats each portal infection as two
            # independent descendant portal lineages, using isolated-state
            # rates exactly as in the diffuse theorem.
            birth = r * portal_load / total_degree
            if rule == "Bd":
                death = blade_load + portal_load / total_degree
                child = r**2 * blade_load / ((r + 1) * total_degree)
            else:
                death = sp.Integer(1)
                child = r * blade_load / 2
            residual = sp.factor(
                birth * exact**2
                - (death + birth + child * (1 - z)) * exact
                + death
            )
            if residual == 0:
                raise AssertionError(f"false cavity closure accidentally held: {r} {rule}")
            failures.append((r, rule, exact, residual))
            print("PASS exact cavity counterexample", r, rule,
                  "F=", exact, "residual=", residual)

    if len(failures) != 4:
        raise AssertionError("missing cavity counterexample")
    print("ALL FIXED-DEGREE SPATIAL CHECKS PASS")


if __name__ == "__main__":
    main()
