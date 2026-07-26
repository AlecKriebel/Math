#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
umbrella_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)
binary_dir=$(CDPATH= cd -- "$umbrella_dir/.." && pwd)
taxonomy_dir=$(CDPATH= cd -- "$binary_dir/../../taxonomy_freeze" && pwd)
canonical_dir=$(CDPATH= cd -- "$binary_dir/../audit_delta_ge3_denominator" && pwd)
python_bin=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}

test -x "$python_bin"

temporary_root=$(mktemp -d "${TMPDIR:-/tmp}/exact-delta4-hostile.XXXXXX")
temporary_row="$temporary_root/fixed_quadratic_line_doublecover"
temporary_binary="$temporary_row/binary_locus"
temporary_umbrella="$temporary_binary/exact_delta4_exclusion"
temporary_canonical="$temporary_row/audit_delta_ge3_denominator"
mkdir -p "$temporary_umbrella" "$temporary_canonical"

aggregate_output="$temporary_root/aggregate.out"
baseline_output="$temporary_root/baseline.out"
plan_output="$temporary_root/plan.out"
mutation_output="$temporary_root/mutation.out"
taxonomy_output="$temporary_root/taxonomy.out"
temporary_manifest="$temporary_umbrella/FAMILIES.json"
mutated_manifest="$temporary_umbrella/FAMILIES.mutated"
temporary_denominator="$temporary_canonical/DENOMINATOR.json"
mutated_denominator="$temporary_canonical/DENOMINATOR.mutated"
alternate_denominator="$temporary_canonical/ALT_DENOMINATOR.json"

family_directories="
d4_sf_21c_exclusion
d4_sf_20cc_exclusion
d4_sf_11cc_exclusion
d4_dn3_full_descent
d4_dn2c_full_descent
d4_dn1cc_full
"

cleanup() {
    for family_directory in $family_directories; do
        rm -f "$temporary_binary/$family_directory"
    done
    rm -f \
        "$aggregate_output" \
        "$baseline_output" \
        "$plan_output" \
        "$mutation_output" \
        "$taxonomy_output" \
        "$temporary_umbrella/verify_manifest.py" \
        "$temporary_manifest" \
        "$mutated_manifest" \
        "$temporary_denominator" \
        "$mutated_denominator" \
        "$alternate_denominator"
    rmdir "$temporary_umbrella" 2>/dev/null || true
    rmdir "$temporary_binary" 2>/dev/null || true
    rmdir "$temporary_canonical" 2>/dev/null || true
    rmdir "$temporary_row" 2>/dev/null || true
    rmdir "$temporary_root" 2>/dev/null || true
}
trap cleanup EXIT HUP INT TERM

# Full revised aggregate replay.  Require each terminal marker exactly once.
if ! KELLER_PYTHON="$python_bin" sh "$umbrella_dir/verify_strict.sh" \
    >"$aggregate_output" 2>&1; then
    cat "$aggregate_output"
    echo "FAIL: revised exact-delta-four aggregate failed" >&2
    exit 1
fi
cat "$aggregate_output"

for marker in \
    EXACT_DELTA4_MANIFEST_PASS_6_OF_6_CANONICAL_19_6_1 \
    DELTA_GE3_RECONCILIATION_STRICT_PASS_26 \
    D4_SF_21C_FULL_STRICT_PASS \
    D4_SF_20CC_FULL_STRICT_PASS \
    D4_SF_11CC_FULL_STRICT_PASS \
    D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS \
    D4_DN2C_FULL_DESCENT_STRICT_PASS \
    D4_DN1CC_FAIL_CLOSED_STRICT_PASS \
    EXACT_DELTA4_SIX_FAMILY_EXCLUSION_STRICT_PASS
do
    marker_count=$(grep -Fxc "$marker" "$aggregate_output")
    if test "$marker_count" -ne 1; then
        echo "FAIL: aggregate marker count for $marker is $marker_count" >&2
        exit 1
    fi
done

# Immutable global taxonomy replay and explicit no-scope-creep check.
if ! (
    cd "$taxonomy_dir"
    /usr/bin/python3 verify_frozen_manifest_v1.py
) >"$taxonomy_output" 2>&1; then
    cat "$taxonomy_output"
    exit 1
fi
cat "$taxonomy_output"
grep -Fx \
    "PASS: frozen manifest schema, Markdown synchronization, finite arithmetic, and required checksums" \
    "$taxonomy_output" >/dev/null
grep -F \
    '| `Q2-E2-A1-B2-D1-N2` | 2 | 2 | 1 | 2 | 1 | 2 | fixed conic, line double cover | open |' \
    "$taxonomy_dir/FROZEN_TAXONOMY_v1.md" >/dev/null
grep -F \
    '| `Q2-E2-A1-B2-D1-N2` | open | -- |' \
    "$taxonomy_dir/CERTIFIED_EXCLUSION_STATUS.md" >/dev/null

# Recreate the bridge verifier in an isolated but path-faithful layout.
cp "$umbrella_dir/verify_manifest.py" "$temporary_umbrella/verify_manifest.py"
cp "$umbrella_dir/FAMILIES.json" "$temporary_manifest"
cp "$canonical_dir/DENOMINATOR.json" "$temporary_denominator"
cp "$canonical_dir/DENOMINATOR.json" "$alternate_denominator"
for family_directory in $family_directories; do
    ln -s "$binary_dir/$family_directory" "$temporary_binary/$family_directory"
done

"$python_bin" "$temporary_umbrella/verify_manifest.py" >"$baseline_output" 2>&1
cat "$baseline_output"
grep -Fx "EXACT_DELTA4_MANIFEST_PASS_6_OF_6_CANONICAL_19_6_1" \
    "$baseline_output" >/dev/null

"$python_bin" "$temporary_umbrella/verify_manifest.py" --emit-plan \
    >"$plan_output"
test "$(wc -l <"$plan_output")" -eq 6
for plan_line in \
    '../d4_sf_21c_exclusion|D4_SF_21C_FULL_STRICT_PASS' \
    '../d4_sf_20cc_exclusion|D4_SF_20CC_FULL_STRICT_PASS' \
    '../d4_sf_11cc_exclusion|D4_SF_11CC_FULL_STRICT_PASS' \
    '../d4_dn3_full_descent|D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS' \
    '../d4_dn2c_full_descent|D4_DN2C_FULL_DESCENT_STRICT_PASS' \
    '../d4_dn1cc_full|D4_DN1CC_FAIL_CLOSED_STRICT_PASS'
do
    grep -Fx "$plan_line" "$plan_output" >/dev/null
done

reset_manifest() {
    cp "$umbrella_dir/FAMILIES.json" "$temporary_manifest"
}

mutate_manifest() {
    sed_expression=$1
    sed "$sed_expression" "$temporary_manifest" >"$mutated_manifest"
    if cmp -s "$temporary_manifest" "$mutated_manifest"; then
        echo "FAIL: requested bridge mutation changed no text" >&2
        exit 1
    fi
    mv "$mutated_manifest" "$temporary_manifest"
}

require_rejection() {
    mutation_label=$1
    expected_diagnostic=$2
    if "$python_bin" "$temporary_umbrella/verify_manifest.py" \
        >"$mutation_output" 2>&1; then
        cat "$mutation_output"
        echo "FAIL: bridge mutation $mutation_label was accepted" >&2
        exit 1
    fi
    grep -F "$expected_diagnostic" "$mutation_output" >/dev/null
    printf '%s\n' "EXACT_DELTA4_BRIDGE_MUTATION_REJECTED_$mutation_label"
}

# Required-failure canonical-ID mutation.
reset_manifest
mutate_manifest \
    's/"atlas_id": "D4-SF-21C"/"atlas_id": "D4-SF-21X"/'
require_rejection ID "bridge order or membership differs from frozen atlas"

# Required-failure alias mutation.
reset_manifest
mutate_manifest \
    's/"certificate_label": "D4-SF-21C"/"certificate_label": "D4-SF-21X"/'
require_rejection ALIAS "canonical ID and certificate label differ"

# Required-failure proof-path mutation to a different existing certificate.
reset_manifest
mutate_manifest \
    's#../d4_sf_21c_exclusion#../d4_sf_20cc_exclusion#'
require_rejection CERTIFICATE_PATH "wrong certificate binding"

# Required-failure terminal-marker mutation.
reset_manifest
mutate_manifest \
    's/D4_SF_21C_FULL_STRICT_PASS/D4_SF_21C_FULL_STRICT_PAST/'
require_rejection MARKER "wrong certificate binding"

# Required-failure canonical-source mutation.  The alternate file exists
# and has identical content, so rejection proves path identity is bound.
reset_manifest
mutate_manifest \
    's#../../audit_delta_ge3_denominator/DENOMINATOR.json#../../audit_delta_ge3_denominator/ALT_DENOMINATOR.json#'
require_rejection FROZEN_SOURCE "canonical denominator path changed"

# Required-failure scope-creep mutation.
reset_manifest
mutate_manifest \
    's/fixed-quadratic line-double-cover binary locus, exact gcd degree delta=4/all fourteen quartic rows, delta at least four/'
require_rejection SCOPE "theorem scope changed"

# Required-failure canonical-count mutation.
reset_manifest
cp "$canonical_dir/DENOMINATOR.json" "$temporary_denominator"
sed 's/"delta3_independent": 19/"delta3_independent": 18/' \
    "$temporary_denominator" >"$mutated_denominator"
if cmp -s "$temporary_denominator" "$mutated_denominator"; then
    echo "FAIL: canonical count mutation changed no text" >&2
    exit 1
fi
mv "$mutated_denominator" "$temporary_denominator"
require_rejection CANONICAL_COUNT "canonical denominator counts changed"

printf '%s\n' "EXACT_DELTA4_HOSTILE_UMBRELLA_AUDIT_STRICT_PASS"
