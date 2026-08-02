#!/bin/sh
set -eu

release_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
venv_dir="$release_dir/.venv-release"

python3 -m venv --clear "$venv_dir"
"$venv_dir/bin/python" -m pip install --disable-pip-version-check \
    -r "$release_dir/requirements.lock"
"$venv_dir/bin/python" "$release_dir/verifiers/verify_construction.py"
"$venv_dir/bin/python" "$release_dir/verifiers/verify_independent.py"
