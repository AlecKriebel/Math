#!/usr/bin/env python3
"""Independent exact three-port replay with no Python ``assert`` statements.

This is intentionally separate from the frozen continuation-2 script.  Every
qualification condition is an explicit exception-producing check, so the
mathematics is not erased by Python optimization.  The top-level release
harness nevertheless rejects ``python -O`` to keep one execution policy for
all imported historical programs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


A, C, G, T = range(4)
XOR = ((0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0))


class ReplayFailure(RuntimeError):
    """A load-bearing exact check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def determinant(matrix: list[list[object]]) -> F:
    work = [list(map(F, row)) for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "matrix is not square")
    answer = F(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        require(pivot is not None, f"singular matrix at column {column}")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for index in range(column, size):
            work[column][index] /= value
        for row in range(column + 1, size):
            value = work[row][column]
            if value:
                for index in range(column, size):
                    work[row][index] -= value * work[column][index]
    return answer


def edge_vector(s_value: F, g_value: F) -> tuple[F, F, F, F]:
    return (F(1), s_value, g_value, s_value)


def sunlet_coordinate(labels: tuple[int, int, int], retic_leaf: int) -> F:
    rho, theta, kappa, delta = F(1, 2), F(1, 3), F(1, 2), F(1, 2)
    a = b = c = edge_vector(rho, rho)
    f = edge_vector(theta, theta)
    d = e = edge_vector(kappa, kappa)
    permutation = [index for index in range(3) if index != retic_leaf]
    permutation.append(retic_leaf)
    inverse_labels = [0, 0, 0]
    for index, image in enumerate(permutation):
        inverse_labels[index] = labels[image]
    x_value, y_value, z_value = inverse_labels
    if XOR[XOR[x_value][y_value]][z_value] != A:
        return F(0)
    return (
        a[x_value]
        * b[y_value]
        * c[z_value]
        * (
            delta * f[y_value] * d[z_value]
            + (1 - delta) * f[x_value] * e[z_value]
        )
    )


def transition(s_value: F, g_value: F) -> tuple[F, F, F, F]:
    return (
        (1 + 2 * s_value + g_value) / 4,
        (1 - g_value) / 4,
        (1 - 2 * s_value + g_value) / 4,
        (1 - g_value) / 4,
    )


def build_certificate() -> dict[str, object]:
    physical_rows = []
    for s_value, g_value in ((F(1, 2), F(1, 2)), (F(1, 3), F(1, 3))):
        probabilities = transition(s_value, g_value)
        require(all(value > 0 for value in probabilities), "non-strict edge")
        require(
            0 < s_value < 1 and s_value * s_value < g_value < 1,
            "edge is outside the strict continuous-time cone",
        )
        physical_rows.append(
            {
                "s": str(s_value),
                "g": str(g_value),
                "transition": [str(value) for value in probabilities],
            }
        )

    tensors = []
    for retic_leaf in range(3):
        tensor = {
            labels: sunlet_coordinate(labels, retic_leaf)
            for labels in product(range(4), repeat=3)
        }
        tensors.append(tensor)
    require(tensors[0] == tensors[1] == tensors[2], "triangle tensors differ")
    tensor = tensors[0]
    pair_values, triple_values = [], []
    for labels, value in tensor.items():
        if value == 0 or labels == (A, A, A):
            continue
        nonzero = sum(character != A for character in labels)
        (pair_values if nonzero == 2 else triple_values).append(value)
    require(len(pair_values) == 9, "pair-coordinate census changed")
    require(len(triple_values) == 6, "triple-coordinate census changed")
    require(set(pair_values) == {F(1, 12)}, "pair-coordinate value changed")
    require(set(triple_values) == {F(1, 48)}, "triple-coordinate value changed")

    character_index = {character: index for index, character in enumerate("ACGT")}

    def coordinate(word: str) -> F:
        return tensor[tuple(character_index[character] for character in word)]

    x_s, x_g = coordinate("CCA"), coordinate("GGA")
    y_s, y_g = coordinate("CAC"), coordinate("GAG")
    z_s, z_g = coordinate("ACC"), coordinate("AGG")
    u_value, v_value, w_value = (
        coordinate("CGT"),
        coordinate("CTG"),
        coordinate("GCT"),
    )
    invariants = (
        u_value * u_value * y_g - y_s * y_s * x_g * z_g,
        v_value * v_value * x_g - x_s * x_s * y_g * z_g,
        w_value * w_value * z_g - z_s * z_s * x_g * y_g,
    )
    require(invariants == (F(-1, 82944),) * 3, "tree equations changed")

    jc_block = [
        [1, 1, 0, 1],
        [1, 0, 1, F(1, 4)],
        [0, 1, 1, F(1, 4)],
        [1, 1, 1, 1],
    ]
    anisotropy_block = [
        [1, 1, 0, 0, 1],
        [1, 0, 1, F(3, 4), F(1, 4)],
        [0, 1, 1, F(1, 4), F(1, 4)],
        [-1, 1, 0, 0, 0],
        [-1, 0, 1, F(1, 2), F(-1, 2)],
    ]
    jc_determinant = determinant(jc_block)
    anisotropy_determinant = determinant(anisotropy_block)
    require(jc_determinant == F(-1, 2), "JC block determinant changed")
    require(
        anisotropy_determinant == F(-1, 4),
        "anisotropy block determinant changed",
    )
    require(
        jc_determinant * anisotropy_determinant == F(1, 8),
        "rank-nine split determinant changed",
    )

    try:
        import sympy as sp
    except Exception as exc:  # pragma: no cover - environment qualification
        raise ReplayFailure("SymPy is required for the symbolic factor gate") from exc
    d_symbol, e_symbol, f_symbol, delta_symbol = sp.symbols("D E f delta")
    complement = 1 - delta_symbol
    n_value = delta_symbol * d_symbol + complement * e_symbol
    l_value = delta_symbol * d_symbol + complement * f_symbol * e_symbol
    m_value = delta_symbol * f_symbol * d_symbol + complement * e_symbol
    identity = sp.expand(
        f_symbol * n_value**2
        - l_value * m_value
        + delta_symbol
        * complement
        * d_symbol
        * e_symbol
        * (1 - f_symbol) ** 2
    )
    require(identity == 0, "tree-sunlet symbolic factor identity failed")

    a_s, a_g = F(2, 5), F(1, 3)
    b_s, b_g = F(3, 7), F(2, 7)
    c_s, c_g = F(4, 9), F(1, 4)
    f_s, f_g = F(2, 5), F(3, 8)
    d_s, d_g = F(1, 3), F(2, 9)
    e_s, e_g = F(1, 5), F(3, 10)
    del a_g, b_g, c_s, d_s, e_s
    delta_value = F(2, 5)
    complement_value = 1 - delta_value
    q_cca = a_s * b_s * f_s
    q_gga = F(1, 3) * F(2, 7) * f_g
    q_gag = F(1, 3) * c_g * (
        delta_value * d_g + complement_value * f_g * e_g
    )
    q_agg = F(2, 7) * c_g * (
        delta_value * f_g * d_g + complement_value * e_g
    )
    q_ctg = a_s * b_s * c_g * f_s * (
        delta_value * d_g + complement_value * e_g
    )
    observed = q_ctg * q_ctg * q_gga - q_cca * q_cca * q_gag * q_agg
    factored = -(
        (a_s**2)
        * (b_s**2)
        * F(1, 3)
        * F(2, 7)
        * (c_g**2)
        * (f_s**2)
        * delta_value
        * complement_value
        * d_g
        * e_g
        * ((1 - f_g) ** 2)
    )
    require(observed == factored, "strict sign factor evaluation changed")
    require(factored < 0, "strict sign is not negative")

    payload: dict[str, object] = {
        "schema": "k2p-three-port-geometry-no-assert-v1",
        "status": "PASS",
        "qualification_style": "explicit require checks; no Python assert statements",
        "physical_ct_rows": physical_rows,
        "common_triangle_tensor": {
            "orientations": 3,
            "nonzero_pair_coordinates": 9,
            "nonzero_triple_coordinates": 6,
            "pair_value": "1/12",
            "triple_value": "1/48",
            "canonical_tensor_sha256": sha_object(
                [
                    [list(labels), str(value)]
                    for labels, value in sorted(tensor.items())
                ]
            ),
        },
        "tree_equation_values": [str(value) for value in invariants],
        "rank_nine_split": {
            "jc_rank": 4,
            "anisotropy_rank": 5,
            "jc_determinant": str(jc_determinant),
            "anisotropy_determinant": str(anisotropy_determinant),
            "product": str(jc_determinant * anisotropy_determinant),
        },
        "tree_sunlet_factor": {
            "symbolic_identity_zero": True,
            "strict_observed_value": str(observed),
            "strict_factored_value": str(factored),
            "strict_sign": "negative",
        },
    }
    payload["payload_sha256"] = sha_object(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("K2P_THREE_PORT_NO_ASSERT_REPLAY_PASS")
    print(json.dumps(certificate, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReplayFailure as error:
        raise SystemExit(f"K2P_THREE_PORT_NO_ASSERT_REPLAY_FAIL:{error}") from error
