#!/usr/bin/env python3
"""Numerical canonical-channel diagnostics for retained d=4 candidates.

This script does not certify the numerical candidates.  It measures the YBE
residual, channel commutator, spectra, and operator-Schmidt rank so that the
numerical evidence can be compared with the exact channel certificates.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import platform
from pathlib import Path

import numpy as np


def partial_trace_second(matrix: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijkj->ik", matrix.reshape(d, d, d, d))


def partial_trace_first(matrix: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijil->jl", matrix.reshape(d, d, d, d))


def superoperator(channel, d: int) -> np.ndarray:
    columns = []
    for i in range(d):
        for j in range(d):
            matrix_unit = np.zeros((d, d), dtype=np.complex128)
            matrix_unit[i, j] = 1
            columns.append(channel(matrix_unit).reshape(-1))
    return np.column_stack(columns)


def realignment(matrix: np.ndarray, d: int) -> np.ndarray:
    return matrix.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(
        d * d, d * d
    )


def diagnostics(path: Path, rank_tolerance: float) -> dict[str, object]:
    h = np.load(path)["h"]
    d = int(round(np.sqrt(h.shape[0])))
    if d != 4:
        raise ValueError(f"{path} has local dimension {d}, not 4")
    identity = np.eye(d, dtype=np.complex128)
    projection = (np.eye(d * d, dtype=np.complex128) - h) / 2
    scale = 2 / d
    channel_r = superoperator(
        lambda x: scale
        * partial_trace_second(
            projection @ np.kron(x, identity) @ projection, d
        ),
        d,
    )
    channel_l = superoperator(
        lambda x: scale
        * partial_trace_first(
            projection @ np.kron(identity, x) @ projection, d
        ),
        d,
    )
    super_identity = np.eye(d * d, dtype=np.complex128)
    identity_vector = identity.reshape(-1) / np.sqrt(d)
    omega = np.outer(identity_vector, identity_vector.conj())
    paired_residual = (
        (channel_r + channel_l - 4 * super_identity / 3)
        @ (channel_r - super_identity / 3)
        @ (channel_l - super_identity / 3)
        - 8 * omega / 27
    )
    h_1 = np.kron(h, identity)
    h_2 = np.kron(identity, h)
    residual = h_1 @ h_2 @ h_1 - h_2 @ h_1 @ h_2 - (h_1 - h_2) / 3
    singular_values = np.linalg.svd(realignment(h, d), compute_uv=False)

    return {
        "path": str(path.resolve()),
        "ybe_residual_frobenius": float(np.linalg.norm(residual)),
        "channel_commutator_frobenius": float(
            np.linalg.norm(channel_r @ channel_l - channel_l @ channel_r)
        ),
        "paired_joint_polynomial_frobenius": float(
            np.linalg.norm(paired_residual)
        ),
        "channel_spectrum_difference": float(
            np.linalg.norm(
                np.linalg.eigvalsh((channel_r + channel_r.conj().T) / 2)
                - np.linalg.eigvalsh((channel_l + channel_l.conj().T) / 2)
            )
        ),
        "channel_r_spectrum": [
            float(value)
            for value in np.linalg.eigvalsh(
                (channel_r + channel_r.conj().T) / 2
            )
        ],
        "channel_l_spectrum": [
            float(value)
            for value in np.linalg.eigvalsh(
                (channel_l + channel_l.conj().T) / 2
            )
        ],
        "channel_r_supertrace": float(np.trace(channel_r).real),
        "channel_l_supertrace": float(np.trace(channel_l).real),
        "operator_schmidt_singular_values_h": [
            float(value) for value in singular_values
        ],
        "operator_schmidt_rank_h": int(
            np.count_nonzero(singular_values > rank_tolerance)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--rank-tolerance", type=float, default=1e-7)
    args = parser.parse_args()

    report = {
        "status": "NUMERICAL_EVIDENCE_ONLY",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "rank_tolerance": args.rank_tolerance,
        "candidates": [
            diagnostics(path, args.rank_tolerance) for path in args.candidates
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
