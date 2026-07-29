#!/usr/bin/env python3
"""Search for a rank-six square restriction of amplified exact d=4 family points.

This is a falsifier for a construction mechanism, not a nonexistence
certificate.  It replaces the published d=4 interaction in
``search_d6_subspace_of_d8_amplification.py`` by three exact points of the
color/face circle s^2+2t^2=1, amplifies by a two-dimensional identity
spectator, and minimizes

    ||[H_8,Q tensor Q]||_F^2 / 64

over rank-six projections Q on C^8.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "search_d6_subspace_of_d8_amplification.py"
SPEC = importlib.util.spec_from_file_location("subspace_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {BASE_PATH}")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def tensor(*matrices: np.ndarray) -> np.ndarray:
    result = np.array([[1]], dtype=np.complex128)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def color_face_h4(s: float, t: float) -> np.ndarray:
    """Numerical assembly of the exact symbolic family in its defining basis."""

    identity_2 = np.eye(2, dtype=np.complex128)
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    z = np.diag([1, -1]).astype(np.complex128)
    hadamard = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)

    b_operators = (x, -y)
    c_operators = (
        -t * x - t * y - s * z,
        -t * x - t * y + s * z,
    )
    blocks: list[np.ndarray] = []
    for first_color in range(2):
        for second_color in range(2):
            parity = (first_color + second_color) % 2
            sign = 1 if parity == 0 else -1
            blocks.append(
                sign * tensor(z, identity_2) / np.sqrt(3)
                + np.sqrt(2 / 3)
                * tensor(
                    b_operators[parity],
                    c_operators[second_color],
                )
            )

    h0 = np.zeros((16, 16), dtype=np.complex128)
    for block, (first_color, second_color) in zip(
        blocks,
        (
            (first_color, second_color)
            for first_color in range(2)
            for second_color in range(2)
        ),
    ):
        indices = [
            (2 * first_color + first_internal) * 4
            + (2 * second_color + second_internal)
            for first_internal in range(2)
            for second_internal in range(2)
        ]
        h0[np.ix_(indices, indices)] = block

    pair_change = tensor(np.eye(4), hadamard, identity_2)
    h4 = pair_change @ h0 @ pair_change.conj().T
    identity_4 = np.eye(4, dtype=np.complex128)
    h1 = np.kron(h4, identity_4)
    h2 = np.kron(identity_4, h4)
    residual = h1 @ h2 @ h1 - h2 @ h1 @ h2 - (h1 - h2) / 3
    if abs(s * s + 2 * t * t - 1) > 1e-13:
        raise ValueError("family point does not satisfy s^2+2t^2=1")
    assert np.linalg.norm(h4 - h4.conj().T) < 1e-12
    assert np.linalg.norm(h4 @ h4 - np.eye(16)) < 1e-12
    assert np.linalg.norm(residual) < 1e-11
    return h4


def amplify(h4: np.ndarray) -> np.ndarray:
    """Reorder H4 tensor I4 into local site order (U1,C1),(U2,C2)."""

    grouped = np.kron(h4, np.eye(4, dtype=np.complex128))
    tensor_form = grouped.reshape(4, 4, 2, 2, 4, 4, 2, 2)
    return tensor_form.transpose(0, 2, 1, 3, 4, 6, 5, 7).reshape(64, 64)


POINTS = {
    "axis_s": (1.0, 0.0),
    "axis_t": (0.0, 1 / np.sqrt(2)),
    "interior": (1 / np.sqrt(2), 0.5),
}


def source_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--point", choices=POINTS, required=True)
    parser.add_argument("--seed-start", type=int, required=True)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--maximum-iterations", type=int, default=2000)
    parser.add_argument("--tolerance", type=float, default=1e-24)
    parser.add_argument("--output-jsonl", type=Path)
    args = parser.parse_args()

    s, t = POINTS[args.point]
    interaction = amplify(color_face_h4(s, t))
    assert np.linalg.norm(interaction @ interaction - np.eye(64)) < 1e-12

    records: list[str] = []

    def emit(record: dict[str, object]) -> None:
        line = json.dumps(record, sort_keys=True)
        records.append(line)
        print(line, flush=True)

    emit(
        {
            "kind": "metadata",
            "point": args.point,
            "s": s,
            "t": t,
            "rank": 6,
            "seed_start": args.seed_start,
            "runs": args.runs,
            "maximum_iterations": args.maximum_iterations,
            "tolerance": args.tolerance,
            "source_sha256": source_hash(),
            "base_source_sha256": hashlib.sha256(BASE_PATH.read_bytes()).hexdigest(),
            "python": sys.version.replace("\n", " "),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        }
    )

    for offset in range(args.runs):
        seed = args.seed_start + offset
        rng = np.random.default_rng(seed)
        initial = BASE.random_projection(rng, 8, 6)
        started = time.time()
        projection, result = BASE.optimize(
            initial,
            interaction,
            args.maximum_iterations,
            args.tolerance,
        )
        result.update(
            {
                "kind": "run",
                "point": args.point,
                "seed": seed,
                "elapsed_seconds": time.time() - started,
                "projection_sha256": hashlib.sha256(
                    np.ascontiguousarray(projection).view(np.uint8)
                ).hexdigest(),
            }
        )
        emit(result)

    if args.output_jsonl is not None:
        args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        args.output_jsonl.write_text("\n".join(records) + "\n")


if __name__ == "__main__":
    main()
