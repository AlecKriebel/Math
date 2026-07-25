#!/usr/bin/env python3
"""Small independent verifier for the two decisive K5 product violations."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path


F = Fraction
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = ROOT / "certificates" / "centered_quarter_k5_extension.json"
EXPECTED_HASHES = {
    SOURCE: "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550",
    EXTENSION: "133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef",
}
EDGES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
ROWS = (
    (
        F(-1, 2),
        1,
        F(7819447598603429, 228000000000000),
    ),
    (
        F(-1, 4),
        3,
        F(
            1222373249978570665696597731104959481,
            81785237862093261678000000000000000,
        ),
    ),
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> tuple[dict[str, str], ...]:
    for path, expected in EXPECTED_HASHES.items():
        assert file_hash(path) == expected
    source = json.loads(SOURCE.read_text())
    extension = json.loads(EXTENSION.read_text())
    grid = tuple(F(value) for value in source["grid"])
    alpha = tuple(F(value) for value in source["alpha"])
    weights = tuple(F(atom["weight"]) for atom in extension["atoms"])
    assert len(weights) == 51 and sum(weights) == 1

    reports = []
    for base_value, capacity, expected_violation in ROWS:
        base_total = F(0)
        depth_total = F(0)
        common_total = F(0)
        product_total = F(0)
        for atom, weight in zip(extension["atoms"], weights):
            colors = atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
            values = {
                edge: grid[color] for edge, color in zip(EDGES, colors)
            }
            for y, z in EDGES:
                if values[(y, z)] != base_value:
                    continue
                base_total += weight
                h = 0
                g = 0
                for x in range(5):
                    if x == y or x == z:
                        continue
                    u = values[tuple(sorted((x, y)))]
                    v = values[tuple(sorted((x, z)))]
                    incident_sum = u + v
                    # Strict comparison against
                    # -(1/300)sqrt(2+2q), without radicals.
                    if (
                        incident_sum < 0
                        and incident_sum * incident_sum
                        > F(2 + 2 * base_value, 300**2)
                    ):
                        h += 1
                    if u == F(1, 2) and v == F(1, 2):
                        g += 1
                assert h + g <= 3
                depth_total += weight * h
                common_total += weight * g
                product_total += weight * h * g

        color = grid.index(base_value)
        assert base_total == alpha[color] / 4
        # This is left minus right in
        # 247P <= 13 M H + 91 Gamma - 7 M D.
        violation = (
            247 * product_total
            - 13 * capacity * depth_total
            - 91 * common_total
            + 7 * capacity * base_total
        )
        assert violation == expected_violation > 0
        reports.append(
            {
                "base_inner_product": str(base_value),
                "positive_threshold": "1/2",
                "capacity": str(capacity),
                "exact_scaled_violation": str(violation),
            }
        )
    return tuple(reports)


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
