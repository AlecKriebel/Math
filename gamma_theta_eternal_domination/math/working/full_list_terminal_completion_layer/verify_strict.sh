#!/bin/sh
set -eu

directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary=$(mktemp "${TMPDIR:-/tmp}/full-list-completion.XXXXXX")
trap 'rm -f "$temporary"' EXIT HUP INT TERM

PYTHONDONTWRITEBYTECODE=1 python3 "$directory/verify_completion.py" >"$temporary"
cmp "$directory/expected_result.json" "$temporary"

PYTHONDONTWRITEBYTECODE=1 python3 - "$directory" "$temporary" <<'PY'
import hashlib
import json
import pathlib
import sys

directory = pathlib.Path(sys.argv[1])
actual = pathlib.Path(sys.argv[2]).read_bytes()
manifest = json.loads((directory / "MANIFEST.json").read_text(encoding="utf-8"))

if manifest["status"] != "CANDIDATE_AWAITING_HOSTILE_REVIEW":
    raise AssertionError("candidate status changed")
if manifest["strict_result_sha256"] != hashlib.sha256(actual).hexdigest():
    raise AssertionError("strict result hash mismatch")

for name, expected in manifest["candidate_hashes"].items():
    actual_hash = hashlib.sha256((directory / name).read_bytes()).hexdigest()
    if actual_hash != expected:
        raise AssertionError((name, expected, actual_hash))

dependency_root = directory.parent
for relative, expected in manifest["accepted_dependency_hashes"].items():
    actual_hash = hashlib.sha256((dependency_root / relative).read_bytes()).hexdigest()
    if actual_hash != expected:
        raise AssertionError((relative, expected, actual_hash))

note = (directory / "NOTE.md").read_text(encoding="utf-8")
required_scope = (
    "No safe-color theorem",
    "complete parameter-three theorem",
    "gamma--theta conjecture is claimed",
    "closed neighborhood",
    "does **not** by itself compare",
)
for phrase in required_scope:
    if phrase not in note:
        raise AssertionError(("scope phrase missing", phrase))

result = json.loads(actual)
if result["equality_rank_reversal"]["parameters"] != {
    "alpha": 3,
    "gamma": 3,
    "gamma_infinity": 3,
    "i": 3,
    "theta": 3,
}:
    raise AssertionError("equality scope mismatch")
if result["gamma_two_all_completed"]["restricted_kernel_sizes"] != {
    "0": 0,
    "1": 0,
    "2": 0,
}:
    raise AssertionError("all-empty control mismatch")
if result["gamma_two_all_completed"]["parameters"]["gamma"] != 2:
    raise AssertionError("gamma-two boundary was promoted")
PY

actual_sha=$(shasum -a 256 "$temporary" | awk '{print $1}')
printf '%s\n' "PASS full-list terminal completion strict replay $actual_sha"
