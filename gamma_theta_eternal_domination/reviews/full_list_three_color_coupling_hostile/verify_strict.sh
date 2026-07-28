#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../.." && pwd)
repository=$(CDPATH= cd -- "$campaign/.." && pwd)
candidate="$campaign/math/working/full_list_three_color_coupling"
actual=$(mktemp "${TMPDIR:-/tmp}/full-list-coupling-hostile.XXXXXX")
trap 'rm -f "$actual"' EXIT HUP INT TERM

resolved=$(git -C "$repository" rev-parse db9c046d)
test "$resolved" = "db9c046d029b7d074676e658a9728e5fa2846ca9"
git -C "$repository" diff --quiet db9c046d -- \
  gamma_theta_eternal_domination/math/working/full_list_three_color_coupling

sh "$candidate/verify_strict.sh"
python3 -I -B -W error "$here/independent_replay.py" > "$actual"

actual_sha=$(shasum -a 256 "$actual" | awk '{print $1}')
expected_sha=$(sed -n '1p' "$here/expected_independent_sha256.txt")
test "$actual_sha" = "$expected_sha"

python3 -I -B -W error - "$campaign" "$candidate" "$actual" "$here" <<'PY'
import hashlib
import json
import math
import pathlib
import sys

campaign = pathlib.Path(sys.argv[1])
candidate = pathlib.Path(sys.argv[2])
actual = pathlib.Path(sys.argv[3])
review_directory = pathlib.Path(sys.argv[4])

review_manifest = json.loads(
    (review_directory / "MANIFEST.json").read_text(encoding="utf-8")
)
assert review_manifest["verdict"] == "UNCONDITIONAL_PASS"
assert review_manifest["reviewed_commit"] == (
    "db9c046d029b7d074676e658a9728e5fa2846ca9"
)
for name, expected in review_manifest["review_hashes"].items():
    obtained = hashlib.sha256((review_directory / name).read_bytes()).hexdigest()
    assert obtained == expected, (name, expected, obtained)

manifest = json.loads((candidate / "MANIFEST.json").read_text(encoding="utf-8"))
assert manifest["status"] == "CANDIDATE_AWAITING_HOSTILE_REVIEW"

for name, expected in manifest["candidate_hashes"].items():
    obtained = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    assert obtained == expected, (name, expected, obtained)

dependency_paths = {
    "C149_NOTE.md": campaign / "math/working/full_list_safe_color_proof/NOTE.md",
    "C154_NOTE.md": campaign / "math/working/full_list_terminal_gate/NOTE.md",
    "C157_CANDIDATE.md": campaign / "math/working/full_list_nonsingleton_terminal/CANDIDATE.md",
    "C163_CANDIDATE.md": campaign / "math/working/full_list_positive_rank_terminal/CANDIDATE.md",
    "C165_NOTE.md": campaign / "math/working/full_list_anchor_restoration/NOTE.md",
    "accepted_control_verifier.py": campaign / "math/working/full_list_nonsingleton_terminal/verify_cyclic_corridor_control.py",
}
assert set(dependency_paths) == set(manifest["accepted_dependency_hashes"])
for name, path in dependency_paths.items():
    obtained = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = manifest["accepted_dependency_hashes"][name]
    assert obtained == expected, (name, expected, obtained)

independent = json.loads(actual.read_text(encoding="utf-8"))
assert independent["theorem_truth_table"]["implication_failures"] == 0
assert independent["color_maps"]["fixed_point_free_maps"] == 8
assert independent["color_maps"]["directed_3_cycles"] == 2
assert independent["color_maps"]["two_cycle_with_tail"] == 6
assert independent["equality_control"]["parameters"] == {
    "gamma": 3,
    "i": 3,
    "alpha": 3,
    "gamma_infinity": 3,
    "theta": 3,
}
assert independent["gamma_two_control"]["parameters"] == {
    "gamma": 2,
    "i": 2,
    "alpha": 3,
    "gamma_infinity": 3,
    "theta": 4,
}

observed = json.loads(
    (candidate / "OBSERVED_RESULTS.json").read_text(encoding="utf-8")
)
assert observed["classification"] == "OBSERVED"
assert observed["not_claimed"]
assert observed["runs"][-1]["status"] == "TIMEOUT_NO_RESULT"
assert all(
    row["status"] == "UNSAT_NO_PROOF_LOG"
    for row in observed["runs"][:-1]
)
assert observed["generator_sha256"] == hashlib.sha256(
    (candidate / observed["generator"]).read_bytes()
).hexdigest()

expected_counts = []
for order in range(10, 17):
    pairs = math.comb(order, 2)
    triples = math.comb(order, 3)
    expected_counts.append({
        "order": order,
        "variables": (
            pairs
            + triples
            + pairs * (order - 2)
            + 3 * triples * (order - 3)
        ),
        "clauses": (
            67
            + math.comb(order, 4)
            + pairs * (3 * (order - 2) + 1)
            + 11 * triples * (order - 3)
        ),
    })
assert independent["formula_counts"] == expected_counts
assert [
    {
        "order": row["order"],
        "variables": row["variables"],
        "clauses": row["clauses"],
    }
    for row in observed["runs"]
] == expected_counts

note = (candidate / "NOTE.md").read_text(encoding="utf-8")
for required in (
    "does **not** prove that a safe color exists",
    "Open cross-ban rank gate",
    "These rows are **OBSERVED only**",
    "does not resolve the gamma--theta conjecture",
):
    assert required in note, required
PY

echo "PASS full-list three-color coupling hostile review $actual_sha"
