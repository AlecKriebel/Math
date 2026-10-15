# Reproduce this review

Run from `/Users/alec/Documents/Math`. The core interpreter is `draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python` (Python 3.12.14, SymPy 1.14.0).

Set a task-specific path variable:

```sh
review_dir=/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/audits/pr662_2306086/reviews/covariance_source_01
core_python=/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python
packet_dir=/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/audits/pr662_2306086/native/unsolved_math_prioritization/attempts/2306086
```

The independently authored identities, endpoint counterpath, normalized inverse, nonlinear perturbation, and all native/archive bindings need only:

```sh
"$core_python" -B "$review_dir/independent_controls.py"
"$core_python" -B -O "$review_dir/independent_controls.py"
```

Each emits the same JSON with 87 passing controls (45 symbolic and 42 binding). The input packet is read only.

The supplied publication checker was inspected and run as follows; TMPDIR confines its copied test packets to this review:

```sh
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$core_python" -B "$packet_dir/verify_publication.py" --replay --selftest
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$core_python" -B -O "$packet_dir/verify_publication.py" --replay --selftest
```

For optional uncertified numerical reproduction, the ignored `tmp/numerical-venv` was created from the same Python base and populated only with the pinned packages in `requirements_numerical.txt`. If that temporary environment is absent, recreate it locally before running:

```sh
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$core_python" -B -m venv "$review_dir/tmp/numerical-venv"
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$review_dir/tmp/numerical-venv/bin/python" -B -m pip install --no-cache-dir -r "$review_dir/requirements_numerical.txt"
"$review_dir/tmp/numerical-venv/bin/python" -B "$review_dir/independent_numerical.py"
"$review_dir/tmp/numerical-venv/bin/python" -B -O "$review_dir/independent_numerical.py"
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$review_dir/tmp/numerical-venv/bin/python" -B "$packet_dir/verify_publication.py" --replay --numerical --selftest
TMPDIR="$review_dir/tmp" PYTHONDONTWRITEBYTECODE=1 "$review_dir/tmp/numerical-venv/bin/python" -B -O "$packet_dir/verify_publication.py" --replay --numerical --selftest
```

The saved normal/optimized JSON files are already included in this review. `TEST_RESULTS.json` binds them by size and SHA-256. `assemble_results.py` checks pair equality and regenerates the metadata; it also expects the source PDF and two page renders under ignored tmp. Source acquisition and page identities are recorded in `SOURCE_BINDINGS.json`.

All numerical results remain uncertified. Passing these commands does not formalize the analytic proof or determine a sharp radius.
