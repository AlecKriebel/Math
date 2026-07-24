#!/usr/bin/env python3
"""Independent verification of the released zero-profile epigraph polish."""

from __future__ import annotations

from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "epigraph_polished.json"
VERIFIER_PATH = HERE / "verify.py"
SPEC = importlib.util.spec_from_file_location(
    "round11_verify", VERIFIER_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load portfolio verifier")
portfolio_verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(portfolio_verifier)


class VerificationError(RuntimeError):
    """Raised when the polished portfolio fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def decimal_maximum(array: np.ndarray) -> tuple[Decimal, tuple[int, int]]:
    with localcontext() as context:
        context.prec = 90
        converted = [
            [Decimal.from_float(float(value)) for value in row]
            for row in array
        ]
        best: Decimal | None = None
        pair = (-1, -1)
        for first in range(len(array)):
            for second in range(first + 1, len(array)):
                value = sum(
                    (
                        converted[first][coordinate]
                        * converted[second][coordinate]
                        for coordinate in range(5)
                    ),
                    Decimal(0),
                )
                if best is None or value > best:
                    best = value
                    pair = (first, second)
        if best is None:
            raise VerificationError("empty pair set")
        return best, pair


def verify(path: Path = SOURCE) -> dict[str, object]:
    source_bytes = path.read_bytes()
    source = json.loads(source_bytes)
    require(
        source["schema"]
        == "kissing5.construction_round11_x12_epigraph_polish.v1",
        "wrong polished schema",
    )
    require(
        source["evidence_status"]
        == "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE",
        "unsafe evidence status",
    )
    require(source["profile_penalties"] == 0, "profile penalty survived polish")
    portfolio_path = ROOT / source["source"]
    require(
        hashlib.sha256(portfolio_path.read_bytes()).hexdigest()
        == source["source_sha256"],
        "source portfolio hash mismatch",
    )
    portfolio = json.loads(portfolio_path.read_text())
    edge_counts = np.asarray(portfolio["profile_edge_counts"], dtype=float)
    row_types = portfolio["profile_row_types"]

    records = []
    n44_maxima = []
    for record in source["records"]:
        require(record["profile_penalties"] == 0, "record used a profile penalty")
        cardinality = record["cardinality"]
        for label in ("initial", "polished", "retained"):
            stored = record[label]
            computed = portfolio_verifier.recompute(
                stored["coordinates_float64"], edge_counts, row_types
            )
            require(
                computed["shape"] == (cardinality, 5),
                "polished coordinate shape mismatch",
            )
            portfolio_verifier.compare_record(stored, computed)
        initial_maximum = record["initial"]["maximum_inner_product"]
        polished_maximum = record["polished"]["maximum_inner_product"]
        retained_maximum = record["retained"]["maximum_inner_product"]
        require(
            retained_maximum <= initial_maximum + 2.0e-15,
            "retention made a candidate worse",
        )
        require(
            record["retained_from"]
            == ("slsqp" if polished_maximum <= initial_maximum else "initial"),
            "wrong retained-source label",
        )
        require(
            retained_maximum > 0.5,
            "threshold candidate requires an exact certificate",
        )
        array = np.asarray(
            record["retained"]["coordinates_float64"], dtype=float
        )
        decimal_value, pair = decimal_maximum(array)
        portfolio_verifier.close(
            float(decimal_value), retained_maximum, 2.0e-15
        )
        summary = {
            "cardinality": cardinality,
            "kind": record["kind"],
            "source_locator": record["source_locator"],
            "initial_maximum": initial_maximum,
            "retained_maximum": retained_maximum,
            "decimal_maximum_of_binary64_coordinates": str(decimal_value),
            "maximizing_pair": list(pair),
            "coordinate_sha256": record["retained"][
                "coordinate_little_endian_float64_sha256"
            ],
            "solver_success": record["solver"]["success"],
        }
        records.append(summary)
        if cardinality == 44:
            n44_maxima.append(retained_maximum)

    require(len(records) == 12, "wrong polish record count")
    require(not source["exact_candidate_found"], "unsafe exact-candidate flag")
    previous_n44 = portfolio["baseline_sources"]["44"][
        "coordinate_sha256"
    ]
    best_n44_record = min(
        (
            record
            for record in records
            if record["cardinality"] == 44
        ),
        key=lambda record: record["retained_maximum"],
    )
    require(
        best_n44_record["retained_maximum"] < 0.5274711925359575,
        "N=44 polish did not improve the stored numerical benchmark",
    )
    require(
        best_n44_record["coordinate_sha256"] != previous_n44,
        "claimed N=44 improvement reused old coordinates",
    )

    return {
        "status": "polished binary64 coordinates independently recomputed",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "records": records,
        "best_n44": best_n44_record,
        "improvement_below_previous_n44": (
            0.5274711925359575
            - best_n44_record["retained_maximum"]
        ),
        "exact_candidate_found": False,
    }


def main() -> None:
    try:
        result = verify()
    except (
        KeyError,
        TypeError,
        ValueError,
        VerificationError,
        portfolio_verifier.VerificationError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
