#!/usr/bin/env python3
"""Independent exact red-team implementation of row-segment realization."""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "independent_verifier"))
from network_parser import parse_network  # noqa: E402
from mass_action_jacobian import factorized_jacobian  # noqa: E402


def lcm_denominators(values: list[sp.Rational]) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, int(sp.denom(value)))
    return result


def nonnegative_base(vectors: list[list[int]], row: int) -> list[int]:
    p = len(vectors[0])
    base = [0] * p
    for j in range(p):
        base[j] = max([0] + [-vector[j] for vector in vectors]) + (1 if j == row else 0)
    return base


def construct_rows(fixed: list[sp.Matrix], variable: list[tuple[sp.Matrix, sp.Matrix]]) -> tuple[dict, list[dict]]:
    p = len(fixed) + len(variable)
    reactions: list[dict] = []
    metadata: list[dict] = []
    row_index = 0
    for a in fixed:
        values = [sp.Rational(x) for x in a]
        c = lcm_denominators(values)
        delta = [int(c * x) for x in values]
        y0 = nonnegative_base([delta], row_index)
        yp = [y0[j] + delta[j] for j in range(p)]
        target_plus = yp.copy(); target_plus[row_index] += 1
        target_minus = y0.copy(); target_minus[row_index] -= 1
        start = len(reactions)
        reactions.extend([{"source": yp, "target": target_plus}, {"source": y0, "target": target_minus}])
        metadata.append({"kind": "fixed", "row": row_index, "c": c, "indices": [start, start + 1]})
        row_index += 1
    for a, b in variable:
        apb = [sp.Rational(a[j] + b[j]) for j in range(p)]
        amb = [sp.Rational(a[j] - b[j]) for j in range(p)]
        c = lcm_denominators(apb + amb)
        plus_delta = [int(c * x) for x in apb]
        minus_delta = [int(c * x) for x in amb]
        y0 = nonnegative_base([plus_delta, minus_delta], row_index)
        yp = [y0[j] + plus_delta[j] for j in range(p)]
        ym = [y0[j] + minus_delta[j] for j in range(p)]
        tp = yp.copy(); tp[row_index] += 1
        tm = ym.copy(); tm[row_index] += 1
        td = y0.copy(); td[row_index] -= 1
        start = len(reactions)
        reactions.extend([
            {"source": yp, "target": tp},
            {"source": ym, "target": tm},
            {"source": y0, "target": td},
        ])
        metadata.append({"kind": "variable", "row": row_index, "c": c, "indices": [start, start + 1, start + 2]})
        row_index += 1
    raw = {"species": [f"X{i+1}" for i in range(p)], "reactions": reactions}
    return raw, metadata


def random_row(rng: random.Random, p: int) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(p)]])


def main() -> int:
    rng = random.Random(20260813)
    instances = 0
    sampled_fluxes = 0
    zero_entries = 0
    repeated_sources = 0
    for p in range(1, 8):
        for _ in range(70):
            fixed_count = rng.randint(0, p)
            variable_count = p - fixed_count
            fixed = [random_row(rng, p) for _ in range(fixed_count)]
            variable = [(random_row(rng, p), random_row(rng, p)) for _ in range(variable_count)]
            # Inject degenerate rows regularly.
            if fixed and instances % 9 == 0:
                fixed[0] = sp.zeros(1, p)
            if variable and instances % 11 == 0:
                variable[0] = (variable[0][0], sp.zeros(1, p))
            raw, metadata = construct_rows(fixed, variable)
            network = parse_network(raw)
            Gamma = network.stoichiometric_matrix()
            Y = network.source_matrix()
            if Gamma.rank() != p:
                raise AssertionError("constructed stoichiometric matrix is not full row rank")
            if any(min(r.source) < 0 or min(r.target) < 0 for r in network.reactions):
                raise AssertionError("negative complex entry")
            if any(r.source == r.target for r in network.reactions):
                raise AssertionError("identity reaction")
            source_list = [r.source for r in network.reactions]
            repeated_sources += len(source_list) - len(set(source_list))

            for _sample in range(6):
                flux = [sp.Integer(0)] * network.m
                target_rows: list[sp.Matrix] = []
                rho_values: list[sp.Rational] = []
                q_values: list[sp.Rational | None] = []
                fixed_cursor = 0
                variable_cursor = 0
                for item in metadata:
                    c = sp.Integer(item["c"])
                    if item["kind"] == "fixed":
                        s = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
                        i1, i2 = item["indices"]
                        flux[i1] = s; flux[i2] = s
                        rho = c * s
                        a = fixed[fixed_cursor]
                        fixed_cursor += 1
                        target_rows.append(rho * a)
                        rho_values.append(rho); q_values.append(None)
                    else:
                        u = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
                        w = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
                        i1, i2, i3 = item["indices"]
                        flux[i1] = u; flux[i2] = w; flux[i3] = u + w
                        rho = c * (u + w)
                        q = sp.simplify((u - w) / (u + w))
                        a, b = variable[variable_cursor]
                        variable_cursor += 1
                        if not (-1 < q < 1):
                            raise AssertionError("q left the open interval")
                        target_rows.append(rho * (a + q * b))
                        rho_values.append(rho); q_values.append(q)
                v = sp.Matrix(flux)
                if any(value <= 0 for value in v):
                    raise AssertionError("nonpositive flux")
                if Gamma * v != sp.zeros(p, 1):
                    raise AssertionError("hidden or missing steady-flux equation")
                A = Gamma * sp.diag(*flux) * Y.T
                expected = sp.Matrix.vstack(*target_rows)
                if sp.simplify(A - expected) != sp.zeros(p):
                    raise AssertionError("row image mismatch")
                J = factorized_jacobian(network, flux, [1] * p)
                if J != A:
                    raise AssertionError("mass-action Jacobian factor mismatch")
                zero_entries += sum(1 for entry in A if entry == 0)
                sampled_fluxes += 1
            instances += 1

    print(json.dumps({
        "status": "PASS",
        "independent_row_families": instances,
        "strict_positive_flux_samples": sampled_fluxes,
        "zero_matrix_entries_exercised": zero_entries,
        "repeated_source_occurrences": repeated_sources,
        "counterexample_found": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
