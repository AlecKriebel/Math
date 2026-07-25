#!/usr/bin/python3
"""Fail-closed exact checks for the version-one quartic denominator."""

import hashlib
import itertools
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "frozen_manifest_v1.json"
CHECKSUMS = HERE / "FROZEN_SHA256_v1.txt"
TAXONOMY = HERE / "FROZEN_TAXONOMY_v1.md"
EXPECTED_CHECKSUM_FILES = {
    "FROZEN_TAXONOMY_v1.md",
    "frozen_manifest_v1.json",
    "verify_frozen_manifest_v1.py",
    "FREEZE_PROTOCOL.md",
    "blind_independent/BLIND_TAXONOMY.md",
    "RECONCILIATION.md",
    "HOSTILE_FREEZE_AUDIT_v1.md",
    "HOSTILE_FREEZE_REAUDIT_v1.md",
}


def fail(message: str):
    raise AssertionError(message)


data = json.loads(MANIFEST.read_text(encoding="utf-8"))
rows = data["rows"]
if data["version"] != 1:
    fail("wrong version")
if data["status"] != "frozen":
    fail("manifest is not frozen")
if len(rows) != data["frozen_row_count"] or len(rows) != 14:
    fail("row count")
if len({row["id"] for row in rows}) != 14:
    fail("duplicate row id")
if (
    rows[0]["id"] != "Q1"
    or rows[0]["rank"] != 1
    or rows[0]["tuple"] is not None
):
    fail("rank-one row")

id_pattern = re.compile(r"^Q2-E(\d+)-A(\d+)-B(\d+)-D(\d+)-N(\d+)$")
for row in rows[1:]:
    if row["rank"] != 2 or row["tuple"] is None:
        fail(f"rank-two schema: {row['id']}")
    match = id_pattern.fullmatch(row["id"])
    if match is None:
        fail(f"rank-two id syntax: {row['id']}")
    encoded_tuple = tuple(int(value) for value in match.groups())
    if encoded_tuple != tuple(row["tuple"]):
        fail(f"id/tuple mismatch: {row['id']}")

expected_tuples = set()
for e in range(4):
    for a in range(1, 5):
        for b in range(1, 5):
            if e + a * b != 4:
                continue
            for delta in range(1, b + 1):
                if b % delta == 0:
                    expected_tuples.add((e, a, b, delta, b // delta))

actual_tuples = {
    tuple(row["tuple"]) for row in rows if row["rank"] == 2
}
if actual_tuples != expected_tuples or len(actual_tuples) != 13:
    fail("rank-two tuple enumeration")

statuses = [row["status"] for row in rows]
if statuses.count("open") != 7:
    fail("open count")
if statuses.count("excluded-audited") != 7:
    fail("excluded count")

monomials = data["coefficient_order"]["degree_four_monomials"]
components = data["coefficient_order"]["target_components"]
expected_monomials = [
    "x^4",
    "x^3*y",
    "x^3*z",
    "x^2*y^2",
    "x^2*y*z",
    "x^2*z^2",
    "x*y^3",
    "x*y^2*z",
    "x*y*z^2",
    "x*z^3",
    "y^4",
    "y^3*z",
    "y^2*z^2",
    "y*z^3",
    "z^4",
]
if monomials != expected_monomials:
    fail("monomial order")
if components != [1, 2, 3]:
    fail("component order")

pivot_ids = data["pivot_ids"]
expected_pivots = [f"C{i:02d}" for i in range(45)]
if pivot_ids != expected_pivots:
    fail("pivot ids")
if data["coverage_kind"] != "disjoint_locally_closed_coefficient_pivot_partition":
    fail("coverage kind")
if data["pivot_strata_per_row"] != 45:
    fail("pivot count per row")
if data["pivot_intersection_count_including_empty"] != 14 * 45:
    fail("total pivot intersections")

# Check that the Cartesian coefficient labels are themselves unique.
coefficient_labels = list(itertools.product(components, monomials))
if len(coefficient_labels) != 45 or len(set(coefficient_labels)) != 45:
    fail("coefficient labels")

taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
table_rows = {}
for line in taxonomy_text.splitlines():
    if not line.startswith("| `Q"):
        continue
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    row_id = cells[0].strip("`")
    if row_id == "Q1":
        parsed = {"rank": int(cells[1]), "tuple": None, "status": cells[8]}
    else:
        parsed = {
            "rank": int(cells[1]),
            "tuple": [int(cells[index]) for index in range(2, 7)],
            "status": cells[8],
        }
    if row_id in table_rows:
        fail(f"duplicate Markdown row: {row_id}")
    table_rows[row_id] = parsed

manifest_rows = {
    row["id"]: {
        "rank": row["rank"],
        "tuple": row["tuple"],
        "status": row["status"],
    }
    for row in rows
}
if table_rows != manifest_rows:
    fail("Markdown table/manifest mismatch")

if not CHECKSUMS.is_file():
    fail("required checksum file is absent")

checksum_lines = [
    line for line in CHECKSUMS.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
if not checksum_lines:
    fail("checksum file is empty")

declared_checksums = {}
for line in checksum_lines:
    parts = line.split("  ")
    if len(parts) != 2:
        fail(f"malformed checksum line: {line!r}")
    expected, filename = parts
    if re.fullmatch(r"[0-9a-f]{64}", expected) is None:
        fail(f"malformed digest: {filename}")
    if filename in declared_checksums:
        fail(f"duplicate checksum entry: {filename}")
    relative = Path(filename)
    if relative.is_absolute() or ".." in relative.parts:
        fail(f"unsafe checksum path: {filename}")
    resolved = (HERE / relative).resolve()
    try:
        resolved.relative_to(HERE.resolve())
    except ValueError:
        fail(f"checksum path escapes freeze directory: {filename}")
    declared_checksums[filename] = expected

if set(declared_checksums) != EXPECTED_CHECKSUM_FILES:
    fail("checksum filename set")

for filename, expected in declared_checksums.items():
    payload = (HERE / filename).read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected:
        fail(f"checksum mismatch: {filename}")

print(
    "PASS: frozen manifest schema, Markdown synchronization, "
    "finite arithmetic, and required checksums"
)
