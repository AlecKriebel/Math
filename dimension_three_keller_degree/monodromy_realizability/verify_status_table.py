#!/usr/bin/env python3
"""Check the degree-2--10 monodromy status ledger against the audited GAP TSV."""

from __future__ import annotations

import csv
import hashlib
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CENSUS = ROOT / "regular_obstruction" / "transitive_actions_2_10.tsv"
NOTE = ROOT / "NOTE.md"

EXPECTED_SHA256 = "21373021fe85115a27141360626edab1abb83209ec5808b2456ef94609d166f7"
EXPECTED_TOTALS = {2: 1, 3: 2, 4: 5, 5: 5, 6: 16, 7: 7, 8: 50, 9: 34, 10: 45}
EXPECTED_EXCLUDED = {
    2: {"2T1"},
    3: {"3T1"},
    4: {"4T1", "4T2"},
    5: {"5T1"},
    6: {"6T1", "6T2"},
    7: {"7T1"},
    8: {f"8T{i}" for i in range(1, 6)},
    9: {"9T1", "9T2"},
    10: {"10T1", "10T2"},
}
EXPECTED_REALIZED = {
    2: set(),
    3: {"3T2"},
    4: {"4T5"},
    5: {"5T5"},
    6: {"6T16"},
    7: {"7T7"},
    8: {"8T50"},
    9: {"9T31", "9T34"},
    10: {"10T45"},
}


def load_census() -> tuple[str, list[dict[str, str]]]:
    lines = CENSUS.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0].startswith("# GAP "), "missing GAP version line"
    rows = list(csv.DictReader(lines[1:], delimiter="\t"))
    return lines[0], rows


def expand_ids(cell: str) -> set[str]:
    text = cell.replace("`", "").replace(" ", "")
    if text == "-":
        return set()
    answer: set[str] = set()
    for token in text.split(","):
        match = re.fullmatch(r"(\d+)T(\d+)(?:-(\d+)T(\d+))?", token)
        assert match, f"unparseable action list token: {token!r}"
        d1, i1, d2, i2 = match.groups()
        if d2 is None:
            answer.add(f"{d1}T{i1}")
            continue
        assert d1 == d2, f"range crosses degrees: {token}"
        for index in range(int(i1), int(i2) + 1):
            answer.add(f"{d1}T{index}")
    return answer


def load_note_rows() -> dict[int, tuple[int, set[str], set[str], set[str], str]]:
    result = {}
    for line in NOTE.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*(?:[2-9]|10)\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        assert len(cells) == 6, f"unexpected ledger row: {line}"
        degree = int(cells[0])
        result[degree] = (
            int(cells[1]),
            expand_ids(cells[2]),
            expand_ids(cells[3]),
            expand_ids(cells[4]),
            cells[5],
        )
    return result


def main() -> None:
    digest = hashlib.sha256(CENSUS.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, "audited GAP census changed"

    version, rows = load_census()
    assert len(rows) == 165, f"expected 165 actions, found {len(rows)}"

    by_degree: dict[int, dict[str, dict[str, str]]] = {
        degree: {} for degree in EXPECTED_TOTALS
    }
    for row in rows:
        degree = int(row["degree"])
        action_id = row["id"]
        assert degree in by_degree, f"degree outside ledger: {degree}"
        assert action_id not in by_degree[degree], f"duplicate action: {action_id}"
        order = int(row["order"])
        stabilizer_order = int(row["stabilizer_order"])
        regular = row["regular"] == "true"
        assert order == degree * stabilizer_order, f"orbit-stabilizer failed: {action_id}"
        assert regular == (stabilizer_order == 1), f"stabilizer test failed: {action_id}"
        assert regular == (order == degree), f"order test failed: {action_id}"
        by_degree[degree][action_id] = row

    note_rows = load_note_rows()
    assert set(note_rows) == set(EXPECTED_TOTALS), "NOTE ledger omits a degree"

    all_excluded: set[str] = set()
    all_realized: set[str] = set()
    all_open: set[str] = set()

    for degree, expected_total in EXPECTED_TOTALS.items():
        records = by_degree[degree]
        all_ids = set(records)
        expected_ids = {f"{degree}T{i}" for i in range(1, expected_total + 1)}
        assert all_ids == expected_ids, f"nonconsecutive TransGrp IDs in degree {degree}"

        regular_ids = {
            action_id
            for action_id, row in records.items()
            if row["regular"] == "true"
        }
        excluded = EXPECTED_EXCLUDED[degree]
        realized = EXPECTED_REALIZED[degree]
        open_ids = all_ids - excluded - realized

        assert regular_ids == excluded, f"excluded/regular mismatch in degree {degree}"
        assert not (excluded & realized), f"excluded realization in degree {degree}"
        assert all(records[action_id]["regular"] == "false" for action_id in realized)
        assert excluded | realized | open_ids == all_ids
        assert not (excluded & open_ids or realized & open_ids)

        # The weighted-lift realization is the natural symmetric action.
        if degree >= 3:
            symmetric_id = max(realized, key=lambda value: int(value.split("T")[1]))
            if degree == 9:
                symmetric_id = "9T34"
            symmetric = records[symmetric_id]
            assert symmetric["structure_description"] == f"S{degree}"
            assert int(symmetric["order"]) == math.factorial(degree)
            assert int(symmetric["stabilizer_order"]) == math.factorial(degree - 1)

        # The additional degree-nine realization is the certified wreath action.
        if degree == 9:
            wreath = records["9T31"]
            assert int(wreath["order"]) == 1296
            assert int(wreath["stabilizer_order"]) == 144
            assert wreath["regular"] == "false"

        table_total, table_excluded, table_realized, table_open, count_cell = note_rows[
            degree
        ]
        assert table_total == expected_total
        assert table_excluded == excluded
        assert table_realized == realized
        assert table_open == open_ids
        expected_counts = f"{len(excluded)}/{len(realized)}/{len(open_ids)}"
        assert count_cell == expected_counts, f"count cell mismatch in degree {degree}"

        all_excluded |= excluded
        all_realized |= realized
        all_open |= open_ids

    assert (len(all_excluded), len(all_realized), len(all_open)) == (17, 9, 139)
    assert len(all_excluded | all_realized | all_open) == 165
    print(f"PASS {version}")
    print("PASS 165 actions = 17 excluded regular + 9 realized + 139 open")
    print("PASS degree 9 wreath realization: 9T31, order 1296, stabilizer 144")


if __name__ == "__main__":
    main()
