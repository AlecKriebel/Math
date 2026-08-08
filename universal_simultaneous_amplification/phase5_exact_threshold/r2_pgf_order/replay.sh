#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
"$repo_dir/.venv/bin/python" -B \
  "$repo_dir/universal_simultaneous_amplification/phase5_exact_threshold/r2_pgf_order/verify_uniform_pgf_refutation.py"
"$repo_dir/.venv/bin/python" -B \
  "$repo_dir/universal_simultaneous_amplification/phase5_exact_threshold/r2_pgf_order/verify_weak_module_pcdf_refutation.py"
