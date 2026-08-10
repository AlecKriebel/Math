#!/usr/bin/env bash
set -euo pipefail

review_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "${review_dir}/../../.." && pwd)"
python_bin="/opt/homebrew/opt/python@3.11/bin/python3.11"

if [[ ! -x "${python_bin}" ]]; then
  echo "Pinned exact-algebra runtime is unavailable: ${python_bin}" >&2
  exit 1
fi

cd "${repo_dir}"

"${python_bin}" - <<'PY'
import sympy
assert sympy.__version__ == "1.14.0", sympy.__version__
PY

"${python_bin}" s_tc_jc_landmark_closure/reviews/invariant_engine/run_review.py

"${python_bin}" - <<'PY'
import hashlib
import json
from pathlib import Path

root = Path("s_tc_jc_landmark_closure/reviews/invariant_engine")
certificate = json.loads((root / "certificate.json").read_text())
mutations = json.loads((root / "mutation_transcript.json").read_text())
failures = json.loads((root / "failure_log.json").read_text())
manifest = json.loads((root / "manifest.json").read_text())

assert certificate["overall_status"] == "VERIFIED"
assert certificate["review_scope"].startswith("primary JC invariant engine only")
assert mutations["all_rejected"] is True
assert len(mutations["mutations"]) == 8
assert {row["observed"] for row in mutations["mutations"]} == {"REJECT"}
assert any(row["id"] == "DEFAULT_PYTHON_MISSING_EXACT_ALGEBRA_DEPENDENCY" for row in failures["preserved_failures"])
assert manifest["scope_exclusions"] == [
    "finite-atlas exhaustiveness",
    "local relation coverage",
    "bounded-support promotion and probe coherence",
    "global identifiability theorem",
]
for relative, expected in manifest["artifact_hashes"].items():
    path = root / relative
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    assert observed == expected, (relative, expected, observed)
print("VERIFIED: clean-room JC invariant-engine audit")
PY
