#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
repository=$(CDPATH= cd -- "$campaign/.." && pwd)
candidate="$campaign/math/working/full_list_terminal_completion_layer"
actual=$(mktemp "${TMPDIR:-/tmp}/completion-layer-hostile.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

resolved=$(git -C "$repository" rev-parse e83ad600)
test "$resolved" = "e83ad600adcd1932ce9612239cf8a72b2f15a7a8"
git -C "$repository" diff --quiet e83ad600 -- \
  gamma_theta_eternal_domination/math/working/full_list_terminal_completion_layer

sh "$candidate/verify_strict.sh"
python3 -I -B -W error "$here/independent_replay.py" > "$actual"
cmp "$here/expected_result.json" "$actual"

python3 -I -B -W error - "$campaign" "$candidate" "$actual" "$here" <<'PY'
import hashlib
import json
import pathlib
import sys

campaign = pathlib.Path(sys.argv[1])
candidate = pathlib.Path(sys.argv[2])
actual_path = pathlib.Path(sys.argv[3])
review = pathlib.Path(sys.argv[4])

review_manifest = json.loads((review / "MANIFEST.json").read_text(encoding="utf-8"))
assert review_manifest["verdict"] == "UNCONDITIONAL_PASS"
assert review_manifest["reviewed_commit"] == "e83ad600adcd1932ce9612239cf8a72b2f15a7a8"
assert review_manifest["candidate_manifest_sha256"] == hashlib.sha256(
    (candidate / "MANIFEST.json").read_bytes()
).hexdigest()
assert review_manifest["independent_result_sha256"] == hashlib.sha256(
    actual_path.read_bytes()
).hexdigest()
for name, expected in review_manifest["review_hashes"].items():
    obtained = hashlib.sha256((review / name).read_bytes()).hexdigest()
    assert obtained == expected, (name, expected, obtained)

candidate_manifest = json.loads((candidate / "MANIFEST.json").read_text(encoding="utf-8"))
assert candidate_manifest["status"] == "CANDIDATE_AWAITING_HOSTILE_REVIEW"
assert candidate_manifest["strict_result_sha256"] == (
    "cd0d99948fea753ebd6c8706d404ddc89ffacc9a47ed9420eddefef033152bb2"
)
assert review_manifest["candidate_note_sha256"] == hashlib.sha256(
    (candidate / "NOTE.md").read_bytes()
).hexdigest()
assert review_manifest["candidate_strict_result_sha256"] == (
    candidate_manifest["strict_result_sha256"]
)
assert review_manifest["accepted_dependency_hashes"] == (
    candidate_manifest["accepted_dependency_hashes"]
)
for name, expected in candidate_manifest["candidate_hashes"].items():
    obtained = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    assert obtained == expected, (name, expected, obtained)
for relative, expected in candidate_manifest["accepted_dependency_hashes"].items():
    obtained = hashlib.sha256((candidate.parent / relative).read_bytes()).hexdigest()
    assert obtained == expected, (relative, expected, obtained)

independent = json.loads(actual_path.read_text(encoding="utf-8"))
assert independent["collision_truth_table"]["failures"] == 0
assert independent["equality_rank_reversal"]["parameters"] == {
    "alpha": 3,
    "gamma": 3,
    "gamma_infinity": 3,
    "i": 3,
    "theta": 3,
}
assert independent["equality_rank_reversal"]["restricted_kernel_sizes"] == {
    "0": 0,
    "1": 150,
    "10": 0,
}
assert independent["equality_rank_reversal"]["dominating_pairs"] == []
assert independent["gamma_two_all_completed"]["parameters"] == {
    "alpha": 3,
    "gamma": 2,
    "gamma_infinity": 3,
    "i": 2,
    "theta": 4,
}
assert independent["gamma_two_all_completed"]["restricted_kernel_sizes"] == {
    "0": 0,
    "1": 0,
    "2": 0,
}
assert independent["gamma_two_all_completed"]["dominating_pairs"] == [
    [1, 10],
    [5, 10],
]
assert independent["gamma_two_full_terminal"]["parameters"] == {
    "alpha": 3,
    "gamma": 2,
    "gamma_infinity": 3,
    "i": 2,
    "theta": 3,
}
assert independent["gamma_two_full_terminal"]["restricted_kernel_sizes"] == {
    "0": 68,
    "1": 65,
    "2": 65,
}

# Audit the subtle membership-versus-physical-response quantifier.
equality_rows = independent["equality_rank_reversal"]["rows"]
assert equality_rows[0]["completion_rows"][0]["first_branch_retained"]
assert not equality_rows[0]["completion_rows"][0]["first_branch_edge"]
assert equality_rows[1]["completion_rows"][1]["first_branch_retained"]
assert not equality_rows[1]["completion_rows"][1]["first_branch_edge"]
gamma_two_row = independent["gamma_two_all_completed"]["rows"][2]["completion_rows"][0]
assert gamma_two_row["first_branch_retained"]
assert not gamma_two_row["first_branch_edge"]

for control_name in (
    "equality_rank_reversal",
    "gamma_two_all_completed",
):
    for row in independent[control_name]["rows"]:
        assert row["completions"]
        for completion in row["completion_rows"]:
            assert completion["first_branch_retained"]
            assert completion["second_branch_retained"]
            assert completion["closed_witness_hit"]
            assert completion["unique_return_guard"] == row["t"]

note = (candidate / "NOTE.md").read_text(encoding="utf-8")
for required in (
    "No safe-color theorem",
    "does **not** by itself compare",
    "These runs have no proof logs",
    "OBSERVED only",
    "gamma--theta conjecture",
):
    assert required in note, required
PY

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
printf '%s\n' "PASS full-list terminal-completion hostile review $actual_sha"
