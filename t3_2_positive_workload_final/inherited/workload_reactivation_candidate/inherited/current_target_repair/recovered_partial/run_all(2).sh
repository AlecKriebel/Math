#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT/src"
python "$ROOT/src/model.py"
python "$ROOT/src/current_target_episode.py"
python "$ROOT/src/conditional_activation_regression.py"
python "$ROOT/src/activation_pair_counterexample.py" >/dev/null
python "$ROOT/src/source_layer_trace.py"
python "$ROOT/src/one_active_generator.py"
python "$ROOT/src/one_active_phase_classifier.py"
python "$ROOT/src/exact_linear.py"
python "$ROOT/src/current_target_bellman.py"
python "$ROOT/src/one_active_poisson.py"
python -m pytest -q "$ROOT/tests"
python "$ROOT/inherited_cleanroom_atlas/cleanroom_atlas_check.py"
python "$ROOT/src/independent_verifier.py" >/dev/null
printf '%s\n' 'ALL CERTIFIED CURRENT-TARGET REPAIR CHECKS PASSED; T3-2 IS NOT CERTIFIED'
