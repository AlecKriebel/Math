#!/usr/bin/env python3
"""Dense independent cross-check of the exact majority-search certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
PAULI = [I2, X, Y, Z]
I3 = np.eye(3, dtype=np.complex128)
T = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=np.complex128)


def local_word(code: list[int]) -> np.ndarray:
    q, exponent = code
    return np.kron(PAULI[q], I3 if exponent == 0 else T)


def tensor_word(codes: list[list[int]]) -> np.ndarray:
    result = np.array([[1.0 + 0.0j]])
    for code in codes:
        result = np.kron(result, local_word(code))
    return result


def main(certificate_path: Path, output_path: Path | None) -> int:
    data = json.loads(certificate_path.read_text(encoding="utf-8"))
    best = data["best_nonzero_residual"]

    h = np.zeros((36, 36), dtype=np.complex128)
    for word, radical, coefficient in best["terms"]:
        h += coefficient * np.sqrt(radical) * tensor_word(word) / 6.0

    h1 = np.kron(h, np.eye(6))
    h2 = np.kron(np.eye(6), h)
    residual = h1 @ h2 @ h1 - h2 @ h1 @ h2 - (h1 - h2) / 3.0

    reconstructed = np.zeros((216, 216), dtype=np.complex128)
    for row in best["residual"]:
        c3r, c3i, c6r, c6i = row["coefficient"]
        coefficient = (c3r + 1j * c3i) * np.sqrt(3.0)
        coefficient += (c6r + 1j * c6i) * np.sqrt(6.0)
        reconstructed += coefficient * tensor_word(row["word"])

    report = {
        "hermiticity_error": float(np.linalg.norm(h - h.conj().T)),
        "involution_error": float(np.linalg.norm(h @ h - np.eye(36))),
        "trace_abs": float(abs(np.trace(h))),
        "dense_residual_frobenius": float(np.linalg.norm(residual)),
        "certificate_reconstruction_error": float(
            np.linalg.norm(216.0 * residual - reconstructed)
        ),
        "certificate_nonzero": bool(np.linalg.norm(reconstructed) > 1.0),
    }
    assert report["hermiticity_error"] < 1e-12
    assert report["involution_error"] < 1e-12
    assert report["trace_abs"] < 1e-12
    assert report["certificate_reconstruction_error"] < 1e-9
    assert report["certificate_nonzero"]

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if output_path is not None:
        output_path.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        default="results/d6_majority_transposition_exact.json",
    )
    parser.add_argument("--output")
    args = parser.parse_args()
    raise SystemExit(
        main(
            Path(args.certificate),
            Path(args.output) if args.output is not None else None,
        )
    )
