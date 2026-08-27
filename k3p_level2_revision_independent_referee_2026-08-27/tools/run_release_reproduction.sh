#!/bin/zsh -f

set -euo pipefail

if (( $# != 1 )); then
  print -u2 -- "usage: run_release_reproduction.sh ABSOLUTE_RUN_DIRECTORY"
  exit 64
fi

typeset -r audit_root="/Users/alec/Documents/Math/k3p_level2_revision_independent_referee_2026-08-27"
typeset -r source_clone="/tmp/k3p-release-audit.wccfQn/repo"
typeset -r source_commit="76a097fbc4ddadf23ba0119a371c5ac29f4802b1"
typeset -r project_relative="k3p_level2_identifiability_final"
typeset -r run_root="$1"
typeset -r checkout_root="$run_root/checkout"
typeset -r project_root="$checkout_root/$project_relative"
typeset -r reviewer_python="$audit_root/package_copy/.venv/bin/python"
typeset -r delivered_compact="/Users/alec/Documents/Math/k3p_level2_identifiability_final/release/dist/k3p_level2_compact_verifier.zip"
typeset -r delivered_full="/Users/alec/Documents/Math/k3p_level2_identifiability_final/release/dist/k3p_level2_reproducibility.tar.gz"
typeset -r build_root="$project_root/release/work/referee_release_reproduction"

if [[ "$run_root" != "$audit_root/package_copy/review_runs/"* ]]; then
  print -u2 -- "run directory must be below the copied package review_runs tree"
  exit 65
fi
if [[ -e "$run_root" ]]; then
  print -u2 -- "refusing to reuse an existing run directory: $run_root"
  exit 66
fi

/bin/mkdir -p "$run_root/tmp"
export TMPDIR="$run_root/tmp"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export LC_ALL=C
export LANG=C
export TZ=UTC
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0

exec > >(/usr/bin/tee "$run_root/transcript.log") 2>&1

run_timed() {
  typeset -r step_name="$1"
  shift
  print -r -- "STEP $step_name"
  /usr/bin/time -p -o "$run_root/$step_name.time" "$@" 2>&1 |
    /usr/bin/tee "$run_root/$step_name.log"
  /bin/cat "$run_root/$step_name.time"
}

print -r -- "RELEASE_REPRODUCTION_START"
print -r -- "source_commit=$source_commit"
print -r -- "sandbox_tmp=$TMPDIR"

run_timed clone_exact_source \
  /usr/bin/git clone --shared --no-checkout "$source_clone" "$checkout_root"
/usr/bin/git -C "$checkout_root" sparse-checkout init --cone
/usr/bin/git -C "$checkout_root" sparse-checkout set "$project_relative"
/usr/bin/git -C "$checkout_root" checkout --detach "$source_commit"

typeset observed_commit
observed_commit="$(/usr/bin/git -C "$checkout_root" rev-parse HEAD)"
[[ "$observed_commit" == "$source_commit" ]]
[[ -z "$(/usr/bin/git -C "$checkout_root" status --porcelain=v1 --untracked-files=all -- "$project_relative")" ]]
print -r -- "EXACT_CLEAN_CHECKOUT_PASS $observed_commit"

run_timed release_mutations \
  "$reviewer_python" "$project_root/reproducibility/test_release_engineering_mutations.py" \
  --output "$run_root/replayed_release_engineering_mutations.json"
/usr/bin/cmp -s \
  "$run_root/replayed_release_engineering_mutations.json" \
  "$project_root/reproducibility/RELEASE_ENGINEERING_MUTATION_REPORT.json"
print -r -- "RELEASE_MUTATION_REPORT_BYTE_IDENTITY_PASS"

/bin/mkdir -p "$build_root/a" "$build_root/b"
run_timed compact_build_a \
  "$reviewer_python" "$project_root/release/build_release.py" compact \
  --output "$build_root/a/k3p_level2_compact_verifier.zip"
run_timed compact_build_b \
  "$reviewer_python" "$project_root/release/build_release.py" compact \
  --output "$build_root/b/k3p_level2_compact_verifier.zip"

/usr/bin/cmp -s \
  "$build_root/a/k3p_level2_compact_verifier.zip" \
  "$build_root/b/k3p_level2_compact_verifier.zip"
/usr/bin/cmp -s \
  "$build_root/a/k3p_level2_compact_verifier.zip" \
  "$delivered_compact"
print -r -- "COMPACT_DOUBLE_BUILD_AND_DELIVERED_IDENTITY_PASS"

run_timed full_build_a \
  "$reviewer_python" "$project_root/release/build_release.py" full \
  --output "$build_root/a/k3p_level2_reproducibility.tar.gz"
run_timed full_build_b \
  "$reviewer_python" "$project_root/release/build_release.py" full \
  --output "$build_root/b/k3p_level2_reproducibility.tar.gz"

/usr/bin/cmp -s \
  "$build_root/a/k3p_level2_reproducibility.tar.gz" \
  "$build_root/b/k3p_level2_reproducibility.tar.gz"
/usr/bin/cmp -s \
  "$build_root/a/k3p_level2_reproducibility.tar.gz" \
  "$delivered_full"
print -r -- "FULL_DOUBLE_BUILD_AND_DELIVERED_IDENTITY_PASS"

[[ -z "$(/usr/bin/git -C "$checkout_root" status --porcelain=v1 --untracked-files=all -- "$project_relative")" ]]
print -r -- "FINAL_CLEAN_CHECKOUT_PASS"

/usr/bin/shasum -a 256 \
  "$run_root/replayed_release_engineering_mutations.json" \
  "$build_root/a/k3p_level2_compact_verifier.zip" \
  "$build_root/b/k3p_level2_compact_verifier.zip" \
  "$build_root/a/k3p_level2_reproducibility.tar.gz" \
  "$build_root/b/k3p_level2_reproducibility.tar.gz" \
  "$audit_root/logs/offline_release_git_read.sb" \
  "$audit_root/tools/run_release_reproduction.sh" \
  > "$run_root/SHA256SUMS_AUDIT_PRE_TRANSCRIPT"
/bin/cat "$run_root/SHA256SUMS_AUDIT_PRE_TRANSCRIPT"

print -r -- "RELEASE_REPRODUCTION_PASS"
