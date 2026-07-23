#!/usr/bin/env python3
"""Verify an exact D5 kissing configuration using integer arithmetic only."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


class CertificateError(ValueError):
    """Raised when an exact root certificate is invalid."""


def _dot(left: list[int], right: list[int]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def verify_payload(payload: dict[str, Any]) -> dict[str, int]:
    if payload.get("schema") != "kissing-number-exact-roots-v1":
        raise CertificateError("unsupported certificate schema")
    dimension = payload.get("dimension")
    normalization_squared = payload.get("normalization_squared")
    max_inner = payload.get("max_normalized_inner_product")
    roots = payload.get("roots")
    if dimension != 5:
        raise CertificateError(f"expected dimension 5, got {dimension!r}")
    if normalization_squared != 2:
        raise CertificateError("this verifier requires normalization_squared = 2")
    if max_inner != "1/2":
        raise CertificateError("this verifier requires the exact bound 1/2")
    if not isinstance(roots, list):
        raise CertificateError("roots must be a list")
    if len(roots) != 40:
        raise CertificateError(f"expected 40 roots, got {len(roots)}")

    checked: list[list[int]] = []
    for index, root in enumerate(roots):
        if (
            not isinstance(root, list)
            or len(root) != dimension
            or any(type(entry) is not int for entry in root)
        ):
            raise CertificateError(f"root {index} is not an integer 5-vector")
        if _dot(root, root) != normalization_squared:
            raise CertificateError(f"root {index} does not have squared norm 2")
        checked.append(root)

    tuples = [tuple(root) for root in checked]
    if len(set(tuples)) != len(tuples):
        raise CertificateError("roots are not distinct")

    pair_count = 0
    boundary_pair_count = 0
    minimum_dot = normalization_squared
    maximum_dot = -normalization_squared
    for (i, left), (j, right) in combinations(enumerate(checked), 2):
        dot = _dot(left, right)
        pair_count += 1
        minimum_dot = min(minimum_dot, dot)
        maximum_dot = max(maximum_dot, dot)
        # Since x = left/sqrt(2), y = right/sqrt(2), x.y = dot/2.
        if dot > 1:
            raise CertificateError(
                f"pair ({i}, {j}) violates the bound: integer dot={dot} > 1"
            )
        if dot == 1:
            boundary_pair_count += 1

    return {
        "dimension": dimension,
        "point_count": len(checked),
        "pair_count": pair_count,
        "boundary_pair_count": boundary_pair_count,
        "minimum_integer_dot": minimum_dot,
        "maximum_integer_dot": maximum_dot,
    }


def verify_file(path: Path) -> dict[str, int]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise CertificateError("top-level JSON value must be an object")
    return verify_payload(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        summary = verify_file(args.certificate)
    except (CertificateError, json.JSONDecodeError, OSError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(json.dumps({"status": "PASS", **summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
