#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT/src"
for f in \
  model.py workload_excursion.py aggregate_debt.py carrier_race_bounds.py \
  slower_arrival_bound.py debt_queue_foster.py physical_carrier_reactivation.py \
  debt_reactivation.py source_layer_hierarchy.py unpaired_service.py \
  one_active_debt.py one_active_poisson.py chart_flow_gluing.py \
  global_green_closure.py current_target_regressions.py counterexample_search.py claim_audit.py
do
  python "$ROOT/src/$f"
done
python -m pytest -q "$ROOT/tests"
python "$ROOT/src/independent_verifier.py" >/dev/null
printf '%s\n' 'ALL T3-2 WORKLOAD-REACTIVATION CHECKS PASSED'
