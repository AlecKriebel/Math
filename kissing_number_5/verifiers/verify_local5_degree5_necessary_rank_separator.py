#!/usr/bin/env python3
"""Exact verifier for the necessary-rank degree-five local5 separator."""

from pathlib import Path

try:
    from verifiers.verify_local5_degree5_exact_separator import (
        verify as verify_certificate,
    )
except ModuleNotFoundError:  # Direct execution from this directory.
    from verify_local5_degree5_exact_separator import (
        verify as verify_certificate,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "local5_degree5_necessary_rank_separator.json"
)


def verify():
    result = verify_certificate(CERTIFICATE)
    assert result["variant"] == "necessary-rank-outer-bands"
    assert result["rank_band_mode"] == "outer"
    return result


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
