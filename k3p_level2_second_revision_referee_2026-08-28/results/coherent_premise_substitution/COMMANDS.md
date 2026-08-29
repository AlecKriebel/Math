# UNACCREDITED AND SUPERSEDED: first premise-substitution commands

This execution used `env -i` but did **not** use an enforced sandbox profile.
It is retained only as historical debugging evidence and must not be credited.
The credited replay is recorded in `COMMANDS_SANDBOXED.md` and
`TRANSCRIPT_SANDBOXED.txt`.

Executed at `2026-08-29T03:23:19Z`.  The commands used a fresh disposable
directory and a credential-free environment.  `package_copy` was read only;
all producer writes landed under `TEST_SANDBOX`.

```sh
REVIEW_ROOT=/Users/alec/Documents/Math/k3p_level2_second_revision_referee_2026-08-28
SOURCE_ROOT="$REVIEW_ROOT/package_copy/proof_package"
PYTHON_BIN=/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python
TEST_SANDBOX=$(mktemp -d "$REVIEW_ROOT/tmp/coherent-premise-substitution.XXXXXX")

mkdir -p "$TEST_SANDBOX/baseline/proof_package/cut_recovery/strong_crossbridge"
mkdir -p "$TEST_SANDBOX/baseline/proof_package/cut_recovery/upstream_frozen"
mkdir -p "$TEST_SANDBOX/baseline/proof_package/cut_recovery/global_logic"
mkdir -p "$TEST_SANDBOX/baseline/proof_package/marginals"

cp -R "$SOURCE_ROOT/cut_recovery/strong_crossbridge/global_transfer" \
  "$TEST_SANDBOX/baseline/proof_package/cut_recovery/strong_crossbridge/global_transfer"
cp -R "$SOURCE_ROOT/cut_recovery/strong_crossbridge/final_certificate" \
  "$TEST_SANDBOX/baseline/proof_package/cut_recovery/strong_crossbridge/final_certificate"
cp "$SOURCE_ROOT/cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json" \
  "$TEST_SANDBOX/baseline/proof_package/cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
cp "$SOURCE_ROOT/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json" \
  "$TEST_SANDBOX/baseline/proof_package/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
cp "$SOURCE_ROOT/marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json" \
  "$TEST_SANDBOX/baseline/proof_package/marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"

cd "$TEST_SANDBOX/baseline/proof_package"
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  LC_ALL=C LANG=C TZ=UTC "$PYTHON_BIN" \
  cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  LC_ALL=C LANG=C TZ=UTC "$PYTHON_BIN" \
  cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py \
  --no-write-report

mkdir -p "$TEST_SANDBOX/mutated"
cp -R "$TEST_SANDBOX/baseline/proof_package" \
  "$TEST_SANDBOX/mutated/proof_package"
cp "$REVIEW_ROOT/results/coherent_premise_substitution/CUT_GLOBAL_LOGIC_REPORT.substituted.json" \
  "$TEST_SANDBOX/mutated/proof_package/cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"

cd "$TEST_SANDBOX/mutated/proof_package"
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  LC_ALL=C LANG=C TZ=UTC "$PYTHON_BIN" \
  cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  LC_ALL=C LANG=C TZ=UTC "$PYTHON_BIN" \
  cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py \
  --no-write-report
```

The concrete disposable directory assigned by `mktemp` was
`/Users/alec/Documents/Math/k3p_level2_second_revision_referee_2026-08-28/tmp/coherent-premise-substitution.k3IndZ`.
