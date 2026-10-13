#!/bin/bash
set -euo pipefail

# This script modifies only this audit copy and its generated cache.
# Ensure adequate disk before running; prior build was stopped for low space.
task_audit_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$task_audit_dir/lean"

export MATHLIB_NO_CACHE_ON_UPDATE=1
export MATHLIB_CACHE_DIR="$task_audit_dir/cache"

lean --version
lake --version
lake update
lake exe cache get Mathlib
lake build OAI.Analysis.VlasovMaxwell.Main
lake env lean Audit.lean

# This is not a comparator run. The comparator's separate programs are required
# for the exact upstream ComparatorChallenges/VlasovMaxwell.json procedure.
