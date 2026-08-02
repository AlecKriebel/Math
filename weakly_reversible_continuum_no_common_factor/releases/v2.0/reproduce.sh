#!/bin/sh
set -eu

release_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
venv_dir="$release_dir/.venv-release"

python3 -m venv --clear "$venv_dir"
"$venv_dir/bin/python" -m pip install --disable-pip-version-check \
    --no-input -r "$release_dir/requirements.lock"

run_check() {
    label=$1
    shift
    echo "==> $label"
    "$venv_dir/bin/python" "$@"
}

run_check "release metadata and byte-anchor verifier" \
    "$release_dir/verify_release_metadata.py"
run_check "frozen v1 construction verifier" \
    "$release_dir/verify_construction.py"
run_check "independent frozen v1 clean-room verifier" \
    "$release_dir/cleanroom/verify_v1_cleanroom.py"
run_check "four-parameter family verifier" \
    "$release_dir/family/verify_family.py"
run_check "clean rates, radical, optimality, and stability verifier" \
    "$release_dir/strengthening/clean_rates_stability_verifier.py"
run_check "minimality arithmetic verifier" \
    "$release_dir/minimality/verify_complexity_arithmetic.py"
run_check "independent v2 audit" \
    "$release_dir/audit_v2/verify_v2_independent.py"
run_check "integrated v2 manuscript cross-check" \
    "$release_dir/source/verify_v2_claims.py"

echo "PASS: all Version 2.0.0 release verifiers succeeded"
