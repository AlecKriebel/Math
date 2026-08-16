"""High-precision discovery probe for K2P/K3P tangent spaces.

This script is explicitly a numerical discovery aid.  It evaluates exact
symbolic Jacobians at the inherited JC common point, lifted diagonally into the
richer models, and reports singular values.  The final theorem must replace
any conclusion suggested here by exact certificates.
"""

from __future__ import annotations

import argparse
from typing import Dict

import mpmath as mp
import sympy as sp

from fourier_models import source_parameterization, target_parameterization


def beta_value() -> mp.mpf:
    mp.mp.dps = 80
    a = mp.mpf(43337075)
    b = mp.mpf(-36083110)
    c = mp.mpf(7336259)
    return (-b - mp.sqrt(b * b - 4 * a * c)) / (2 * a)


def jc_position_values(side: str) -> Dict[str, mp.mpf]:
    b = beta_value()
    common = {
        "rA": mp.mpf(2) / 3,
        "rC": mp.mpf(3) / 4,
        "BC": mp.mpf(1) / 2,
        "pD": mp.mpf(1) / 2,
    }
    if side == "source":
        common.update(
            {
                "AB": mp.mpf(3) / 5,
                "CD": mp.mpf(9) / 20,
                "DE": mp.mpf(2) / 5,
                "AF": mp.mpf(1) / 2,
                "EF": mp.mpf(1) / 3,
                "pB": mp.mpf(1) / 5,
                "pF": mp.mpf(1) / 2,
                "pE": mp.mpf(3) / 8,
            }
        )
    elif side == "target":
        common.update(
            {
                "AB": mp.mpf(24835) * b / (mp.mpf(20678) - mp.mpf(24835) * b),
                "CD": mp.mpf(9934) / 12215,
                "DE": mp.mpf(171) / 775,
                "AF": mp.mpf(10339) / (mp.mpf(53010) * b),
                "EF": mp.mpf(1) / 2,
                "pB": mp.mpf(3) / (mp.mpf(20) * b),
                "pF": mp.mpf(1767) / 4832,
                "pE": mp.mpf(31) / 190,
            }
        )
    else:
        raise ValueError(side)
    return common


def substitution(parameters, model: str, side: str):
    values = jc_position_values(side)
    result = {}
    for parameter in parameters:
        name = str(parameter)
        if name.endswith("lambda_C") or name.endswith("lambda_F"):
            result[parameter] = mp.mpf(1) / 2
            continue
        edge = name.split("_", 2)[-1]
        # Prefixes are s_ or t_; the next token is x/s/t/x1/x2/x3.
        if edge not in values:
            edge = name.rsplit("_", 1)[-1]
        if edge not in values:
            raise KeyError(name)
        result[parameter] = values[edge]
    return result


def evaluate_jacobian(model: str, side: str):
    build = source_parameterization if side == "source" else target_parameterization
    coordinates, parameters = build(model, prefix=("s_" if side == "source" else "t_"))
    rows = [coordinates[g] for g in coordinates if g != (0, 0, 0, 0)]
    jacobian = sp.Matrix(rows).jacobian(parameters)
    sub = substitution(parameters, model, side)
    numeric = mp.matrix(
        [[mp.mpf(str(sp.N(entry.subs(sub), 80))) for entry in row] for row in jacobian.tolist()]
    )
    return numeric


def singular_values(matrix: mp.matrix):
    _u, values, _v = mp.svd(matrix)
    return [values[i] for i in range(values.rows)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=("K2P", "K3P"))
    args = parser.parse_args()
    mp.mp.dps = 80
    source = evaluate_jacobian(args.model, "source")
    target = evaluate_jacobian(args.model, "target")
    combined = mp.matrix(source.rows, source.cols + target.cols)
    for i in range(source.rows):
        for j in range(source.cols):
            combined[i, j] = source[i, j]
        for j in range(target.cols):
            combined[i, source.cols + j] = target[i, j]

    for name, matrix in (("source", source), ("target", target), ("combined", combined)):
        values = singular_values(matrix)
        print(name, matrix.rows, matrix.cols)
        for i, value in enumerate(values):
            print(i + 1, mp.nstr(value, 18))


if __name__ == "__main__":
    main()

