#!/usr/bin/env python3
"""Cross-check the compiled degree-12 character engine against repository L.

The compiled audit uses a compressed F_(167^12) power basis.  This verifier
asks it for deterministic product-character probes and independently
recomputes every probe in the repository's 36-coordinate ambient field.
Agreement checks the exporter, degree-12 multiplication, exponentiation,
factor ordering, and physical-alphabet option ordering together.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
PROMOTED = SEARCH_ROOT / "lp333_shell_two_primitive_units"
for path in (HERE, SEARCH_ROOT, PROMOTED):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import audit_primitive_degenerate as audit  # noqa: E402
import export_character_instances as exporter  # noqa: E402
import verify_lp333_order3_phase_prime167 as phase167  # noqa: E402
import verify_lp333_order3_prime167_split as split  # noqa: E402


P = 167
E_SIZE = P**12


def parse_coordinates(value: str) -> tuple[int, ...]:
    result = tuple(int(entry) for entry in value.split(","))
    if len(result) != 12 or any(not 0 <= entry < P for entry in result):
        raise ValueError("invalid compiled field coordinates")
    return result


def compiled_probes(
    helper: Path, binary_input: Path, order: int
) -> dict[int, tuple[tuple[int, ...], tuple[int, ...]]]:
    completed = subprocess.run(
        [
            str(helper),
            str(binary_input),
            str(order),
            "1",
            "probe",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("probe="):
            continue
        fields = dict(part.split("=", 1) for part in line.split())
        index = int(fields["probe"])
        result[index] = (
            parse_coordinates(fields["product"]),
            parse_coordinates(fields["character"]),
        )
    if len(result) != 15:
        raise AssertionError("the compiled helper returned the wrong probes")
    return result


def verify(helper: Path, binary_input: Path) -> dict[str, object]:
    _, powers, selected, inverse = exporter.field_basis()
    coordinates = exporter.coordinate_map(powers, selected, inverse)
    alpha = phase167.ninth_root_of_unity()
    cases = exporter.load_cases()
    checked = 0
    order_summaries = []
    for order in (2, 83, 28057):
        probes = compiled_probes(helper, binary_input, order)
        for case_index, case in enumerate(cases):
            channel = 0 if case["channel"] == "A" else 1
            profile_ids = tuple(int(value) for value in case["profile_ids"])
            values = []
            for factor in range(6):
                value = audit.zero_column_value(channel, alpha)
                options = audit.class_options(
                    profile_ids, alpha, factor, channel
                )
                for class_index, (_, alphabet) in enumerate(options):
                    choice = (
                        (case_index + 1) * (class_index + 3) + 7
                    ) % len(alphabet)
                    ambient = tuple(
                        (
                            int(alphabet[choice][2 * index]),
                            int(alphabet[choice][2 * index + 1]),
                        )
                        for index in range(18)
                    )
                    value = split.l_add(value, ambient)
                values.append(value)
            product = split.L_ONE
            for value in values:
                product = split.l_multiply(product, value)
            character = split.l_power(product, (E_SIZE - 1) // order)
            expected_product, expected_character = probes[case_index]
            if coordinates(product) != expected_product:
                raise AssertionError("compiled product probe disagrees")
            if coordinates(character) != expected_character:
                raise AssertionError("compiled character probe disagrees")
            checked += 1
        order_summaries.append({"order": order, "cases": len(cases)})
    return {
        "schema": "h668-character-field-bridge-v1",
        "orders": order_summaries,
        "compiled_repository_probe_agreements": checked,
        "all_agree": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--helper", type=Path, required=True)
    parser.add_argument(
        "--input",
        type=Path,
        default=HERE / "character_instances.bin",
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.helper, args.input), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
