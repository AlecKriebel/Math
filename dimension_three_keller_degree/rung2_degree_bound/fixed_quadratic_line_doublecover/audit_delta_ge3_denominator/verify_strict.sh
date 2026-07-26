#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ledger="$audit_dir/DENOMINATOR.json"
checker="$audit_dir/verify_delta_ge3_denominator.py"

python3 -m json.tool "$ledger" >/dev/null

python3 - "$ledger" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as stream:
    data = json.load(stream)

families = data["families"]
ids = [family["id"] for family in families]
assert len(ids) == len(set(ids)) == data["counts"]["total"] == 26

expected = {
    "delta3_independent": 19,
    "delta4_independent": 6,
    "dependent_power_fibre": 1,
}
actual = {
    coarse: sum(family["coarse"] == coarse for family in families)
    for coarse in expected
}
assert actual == expected == {
    key: data["counts"][key]
    for key in expected
}

known = set(ids)
for family in families:
    assert {
        "id",
        "coarse",
        "delta",
        "h_chart",
        "normal_form",
        "parameter_space",
        "quotient",
        "guards",
        "retained_pivots",
        "exit_boundaries",
    } <= family.keys()
    for pivot in family["retained_pivots"] + family["exit_boundaries"]:
        destination = pivot["destination"].split(";", 1)[0]
        if destination.startswith("same "):
            continue
        assert destination in known, (family["id"], destination)

assert [family["delta"] for family in families].count(3) == 19
assert [family["delta"] for family in families].count(4) == 6
assert [family["delta"] for family in families].count(5) == 1
PY

output=$(python3 "$checker")
printf '%s\n' "$output"
printf '%s\n' "$output" |
    grep -Fqx 'DELTA_GE3_DENOMINATOR_EXACT_PASS_19_6_1'

printf '%s\n' 'DELTA_GE3_DENOMINATOR_STRICT_PASS_26'
