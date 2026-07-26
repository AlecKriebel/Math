#!/bin/sh
set -eu

output=$(/usr/bin/python3 -u "$(dirname "$0")/verify_bridge_exact.py" 2>&1) || {
    printf '%s\n' "$output" >&2
    exit 1
}
printf '%s\n' "$output"
case "$output" in
    *FAIL*|*Traceback*|*Warning*)
        echo "strict wrapper rejected diagnostic output" >&2
        exit 1
        ;;
esac
last_line=$(printf '%s\n' "$output" | tail -n 1)
[ "$last_line" = "terminal kinds: 3 AUTOMORPHISM_EXIT; 10 DET_L_ZERO" ] || {
    echo "strict wrapper rejected missing terminal attestation" >&2
    exit 1
}
echo "AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B"
