# Reproduce the KP-4.80 audit

Requirements: Python 3.10 or newer, standard library, real/effective UID 1000 for the readonly harnesses. No network or source-document inputs are needed for the finite checks. Keep the original frozen candidate available separately. Work in the root of this audit folder.

## Corrected verifier

    python -B corrected_v1/verify_exact.py > /tmp/kp480-normal.json
    python -B -O corrected_v1/verify_exact.py > /tmp/kp480-O.json
    python -B -OO corrected_v1/verify_exact.py > /tmp/kp480-OO.json
    cmp corrected_v1/EXACT_CHECKS.json /tmp/kp480-normal.json
    cmp corrected_v1/EXACT_CHECKS.json /tmp/kp480-O.json
    cmp corrected_v1/EXACT_CHECKS.json /tmp/kp480-OO.json

The optional --output argument is also supported, but its destination must be writable. For a readonly input directory, stdout redirection to a separate writable destination is sufficient. Do not interpret failure to create an output file as mathematical rejection.

## Runtime optimization and mutation controls

Replace ORIGINAL with the path to the original frozen verify_exact.py, whose input pin is in public/INPUT_PINS.json.

    python public/run_readonly_audit.py --original ORIGINAL --corrected corrected_v1/verify_exact.py --expected corrected_v1/EXACT_CHECKS.json --output /tmp/kp480-readonly-results.json

This runs six baseline checks and thirty semantic-mutant checks in genuine non-root readonly working directories, verifies actual write denials, and verifies that source bytes remain unchanged. Ten original optimized false-PASS results are expected negative controls; all corrected mutants must reject.

## Independent verification and controls

    python public/independent_exact.py --candidate corrected_v1/EXACT_CHECKS.json --output /tmp/kp480-independent.json
    cmp public/INDEPENDENT_EXACT_RESULTS.json /tmp/kp480-independent.json
    python public/run_independent_mutations.py --checker public/independent_exact.py --candidate corrected_v1/EXACT_CHECKS.json --expected public/INDEPENDENT_EXACT_RESULTS.json --output /tmp/kp480-independent-mutations.json

The independent harness recomputes all subspaces and permutation matrices for its three normal/optimized baselines. Its eight mutation cases use the pinned independent computation as an expected-data cache; they do not claim to recompute the large enumeration on each failing mutation. Every failure must be an explicit semantic AssertionError, not a permission error.

## Limits

These commands check finite group/module algebra and arithmetic conditional on stated imported theorems. They do not construct a geometric neck configuration, prove smooth non-isotopy, compute stable stems or gauge invariants, or settle either original existence question.
