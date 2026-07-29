"""Discovery probe for the Hodge determinant tensor on balanced graph codes.

Floating-point calculations in this file are only used to locate exact
examples or counterexamples.
"""

from __future__ import annotations

import itertools
import math
import numpy as np


def digits(code: int, n: int = 4) -> tuple[int, ...]:
    out = []
    for _ in range(n):
        out.append(code % 3)
        code //= 3
    return tuple(out)


WORDS = [digits(i) for i in range(81)]
ZETA = np.exp(2j * np.pi / 3)
L = np.zeros((3, 3, 3), dtype=complex)
for k, a, b in itertools.permutations(range(3), 3):
    inversions = sum(x > y for i, x in enumerate((k, a, b))
                     for y in (k, a, b)[i + 1 :])
    L[k, a, b] = -1 if inversions % 2 else 1


def graph_frame(graph: int, syndrome: tuple[int, ...]) -> np.ndarray:
    adjacency = np.zeros((4, 4), dtype=int)
    code = graph
    for i in range(4):
        for j in range(i + 1, 4):
            adjacency[i, j] = adjacency[j, i] = code % 3
            code //= 3
    u = np.empty(81, dtype=complex)
    v = np.empty(81, dtype=complex)
    for index, word in enumerate(WORDS):
        phase = sum(adjacency[i, j] * word[i] * word[j]
                    for i in range(4) for j in range(i + 1, 4)) % 3
        shift = sum(syndrome[i] * word[i] for i in range(4)) % 3
        u[index] = ZETA**phase / 9
        v[index] = ZETA ** (phase + shift) / 9
    return np.column_stack((u, v))


def trace_replace(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape((3,) * 8)
    # Trace the row/column indices at site, then reinsert an identity.
    reduced = np.trace(tensor, axis1=site, axis2=site + 4)
    out = np.zeros((3,) * 8, dtype=complex)
    for value in range(3):
        selector = [slice(None)] * 8
        selector[site] = value
        selector[site + 4] = value
        out[tuple(selector)] = reduced
    return out.reshape(81, 81)


def moments(frame: np.ndarray) -> np.ndarray:
    p = frame @ frame.conj().T
    maps = [None] * 16
    maps[0] = p
    for mask in range(1, 16):
        bit = (mask & -mask).bit_length() - 1
        maps[mask] = trace_replace(maps[mask ^ (1 << bit)], bit)
    return np.array([np.vdot(p, maps[15 ^ mask]).real for mask in range(16)])


def determinant_sum(frame: np.ndarray) -> float:
    tensor = frame.reshape(3, 3, 3, 3, 2)
    total = 0.0
    for labels in itertools.product(range(3), repeat=4):
        transformed = np.einsum(
            "aA,bB,cC,dD,ABCDq->abcdq",
            L[labels[0]], L[labels[1]], L[labels[2]], L[labels[3]],
            tensor,
        )
        s = np.einsum("abcdp,abcdq->pq", tensor, transformed)
        total += abs(np.linalg.det(s))
    return total


def main() -> None:
    count = 0
    minimum = float("inf")
    maximum = 0.0
    min_witness = None
    max_witness = None
    for graph in range(3**6):
        for syndrome_code in range(1, 81):
            syndrome = WORDS[syndrome_code]
            frame = graph_frame(graph, syndrome)
            values = moments(frame)
            if max(abs(values[t] - values[15 ^ t]) for t in range(1, 15)) > 1e-9:
                continue
            value = determinant_sum(frame)
            count += 1
            if value < minimum:
                minimum, min_witness = value, (graph, syndrome_code)
            if value > maximum:
                maximum, max_witness = value, (graph, syndrome_code)
    print(
        "balanced", count,
        "min", minimum, "min_witness", min_witness,
        "max", maximum, "max_witness", max_witness,
    )
    exact_report(395, 53)


def eis_add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def eis_mul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] - x[1] * y[1]


def eis_conj(x: tuple[int, int]) -> tuple[int, int]:
    return x[0] - x[1], -x[1]


def eis_norm(x: tuple[int, int]) -> int:
    return x[0] * x[0] - x[0] * x[1] + x[1] * x[1]


EIS_ZETA = ((1, 0), (0, 1), (-1, -1))


def graph_phases(graph: int, syndrome_code: int) -> tuple[list[int], list[int]]:
    adjacency = [[0] * 4 for _ in range(4)]
    code = graph
    for i in range(4):
        for j in range(i + 1, 4):
            adjacency[i][j] = adjacency[j][i] = code % 3
            code //= 3
    syndrome = WORDS[syndrome_code]
    phase_u, phase_v = [], []
    for word in WORDS:
        phase = sum(adjacency[i][j] * word[i] * word[j]
                    for i in range(4) for j in range(i + 1, 4)) % 3
        shift = sum(syndrome[i] * word[i] for i in range(4)) % 3
        phase_u.append(phase)
        phase_v.append((phase + shift) % 3)
    return phase_u, phase_v


def exact_moment(
    phase_u: list[int], phase_v: list[int], retained_mask: int
) -> tuple[int, int]:
    retained = [i for i in range(4) if retained_mask >> i & 1]
    erased = [i for i in range(4) if not (retained_mask >> i & 1)]
    total = 0
    for left in itertools.product(range(3), repeat=len(retained)):
        for right in itertools.product(range(3), repeat=len(retained)):
            entry = (0, 0)
            for rest in itertools.product(range(3), repeat=len(erased)):
                x = [0] * 4
                y = [0] * 4
                for pos, site in enumerate(retained):
                    x[site], y[site] = left[pos], right[pos]
                for pos, site in enumerate(erased):
                    x[site] = y[site] = rest[pos]
                ix = sum(x[i] * 3**i for i in range(4))
                iy = sum(y[i] * 3**i for i in range(4))
                for phases in (phase_u, phase_v):
                    entry = eis_add(
                        entry,
                        EIS_ZETA[(phases[ix] - phases[iy]) % 3],
                    )
            total += eis_norm(entry)
    # Each reduced entry has denominator 81.
    return total, 6561


def exact_determinants(
    phase_u: list[int], phase_v: list[int]
) -> list[tuple[int, int]]:
    phases = (phase_u, phase_v)
    out = []
    for labels in itertools.product(range(3), repeat=4):
        entries = [[(0, 0) for _ in range(2)] for _ in range(2)]
        for input_word in WORDS:
            output = [0] * 4
            sign = 1
            for site, (label, value) in enumerate(zip(labels, input_word)):
                candidates = [
                    candidate for candidate in range(3)
                    if L[label, candidate, value] != 0
                ]
                if not candidates:
                    sign = 0
                    break
                output[site] = candidates[0]
                sign *= int(L[label, output[site], value].real)
            if sign == 0:
                continue
            input_index = sum(input_word[i] * 3**i for i in range(4))
            output_index = sum(output[i] * 3**i for i in range(4))
            for p in range(2):
                for q in range(2):
                    term = EIS_ZETA[(phases[p][output_index] + phases[q][input_index]) % 3]
                    if sign < 0:
                        term = (-term[0], -term[1])
                    entries[p][q] = eis_add(entries[p][q], term)
        determinant = eis_add(
            eis_mul(entries[0][0], entries[1][1]),
            tuple(-z for z in eis_mul(entries[0][1], entries[1][0])),
        )
        out.append(determinant)
    return out


def exact_report(graph: int, syndrome: int) -> None:
    phase_u, phase_v = graph_phases(graph, syndrome)
    moment_values = [exact_moment(phase_u, phase_v, mask) for mask in range(16)]
    assert all(
        moment_values[mask] == moment_values[15 ^ mask]
        for mask in range(1, 15)
    )
    determinants = exact_determinants(phase_u, phase_v)
    norm_counts: dict[int, int] = {}
    for value in determinants:
        norm_counts[eis_norm(value)] = norm_counts.get(eis_norm(value), 0) + 1
    print("exact moments", moment_values)
    print("determinant norm counts", sorted(norm_counts.items()))
    print(
        "absolute numerator sum",
        sum(count * math.sqrt(norm) for norm, count in norm_counts.items()),
        "denominator", 6561,
    )


if __name__ == "__main__":
    main()
