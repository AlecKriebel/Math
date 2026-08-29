# Credited default-deny premise-substitution replay

Executed on 2026-08-29 and completed at `2026-08-29T03:34:57Z`.  The expanded
commands used `/usr/bin/sandbox-exec` for every probe and every package-script
invocation.  For readability, the repeated exact prefix is factored below.

```sh
REVIEW_ROOT=/Users/alec/Documents/Math/k3p_level2_second_revision_referee_2026-08-28
SOURCE_ROOT="$REVIEW_ROOT/package_copy/proof_package"
TEST_ROOT="$REVIEW_ROOT/tmp/coherent-premise-substitution-sandboxed.QeuPXv"
PROFILE="$REVIEW_ROOT/results/coherent_premise_substitution/SANDBOX_PROFILE.sb"
PROBE="$TEST_ROOT/SANDBOX_BOUNDARY_PROBE.py"
PYTHON_BIN=/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python

mkdir -p "$TEST_ROOT/runtime_home" "$TEST_ROOT/runtime_tmp"
mkdir -p "$TEST_ROOT/baseline/proof_package/cut_recovery/strong_crossbridge"
mkdir -p "$TEST_ROOT/baseline/proof_package/cut_recovery/upstream_frozen"
mkdir -p "$TEST_ROOT/baseline/proof_package/cut_recovery/global_logic"
mkdir -p "$TEST_ROOT/baseline/proof_package/marginals"

cp -R "$SOURCE_ROOT/cut_recovery/strong_crossbridge/global_transfer" \
  "$TEST_ROOT/baseline/proof_package/cut_recovery/strong_crossbridge/global_transfer"
cp -R "$SOURCE_ROOT/cut_recovery/strong_crossbridge/final_certificate" \
  "$TEST_ROOT/baseline/proof_package/cut_recovery/strong_crossbridge/final_certificate"
cp "$SOURCE_ROOT/cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json" \
  "$TEST_ROOT/baseline/proof_package/cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
cp "$SOURCE_ROOT/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json" \
  "$TEST_ROOT/baseline/proof_package/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
cp "$SOURCE_ROOT/marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json" \
  "$TEST_ROOT/baseline/proof_package/marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"

mkdir -p "$TEST_ROOT/mutated"
cp -R "$TEST_ROOT/baseline/proof_package" "$TEST_ROOT/mutated/proof_package"
cp "$REVIEW_ROOT/results/coherent_premise_substitution/CUT_GLOBAL_LOGIC_REPORT.substituted.json" \
  "$TEST_ROOT/mutated/proof_package/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
cp "$REVIEW_ROOT/results/coherent_premise_substitution/SANDBOX_BOUNDARY_PROBE.py" \
  "$PROBE"

run_isolated() {
  /usr/bin/env -i \
    PATH=/usr/bin:/bin:/usr/sbin:/sbin \
    LC_ALL=C LANG=C TZ=UTC \
    PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
    HOME="$TEST_ROOT/runtime_home" TMPDIR="$TEST_ROOT/runtime_tmp" \
    __CF_USER_TEXT_ENCODING=0x1F5:0:0 \
    /usr/bin/sandbox-exec -f "$PROFILE" "$PYTHON_BIN" "$@"
}

cd "$REVIEW_ROOT"
run_isolated "$PROBE" environment
run_isolated "$PROBE" network
run_isolated "$PROBE" credential
run_isolated "$PROBE" sibling
run_isolated "$PROBE" active-review
run_isolated "$PROBE" source-read
run_isolated "$PROBE" source-write
run_isolated "$PROBE" disposable-write

cd "$TEST_ROOT/baseline/proof_package"
run_isolated cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py
run_isolated cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py \
  --no-write-report

cd "$TEST_ROOT/mutated/proof_package"
run_isolated cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py
run_isolated cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py \
  --no-write-report
```

The package source was only copied before sandbox entry.  Every execution of a
reviewer probe or package script used the same frozen profile.  No network or
credential-bearing environment was available to the sandboxed processes.
