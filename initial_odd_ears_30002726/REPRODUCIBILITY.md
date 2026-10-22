# Reproducing the initial odd ear checks

## Requirements

Python 3.10 or later; only the standard library is used. Assertions must stay
enabled. The documented commands do not use optimization flags. No third-party
package, network request, input dataset, or scholarly PDF is required.

## Commands

Run from the package directory:

    python3 -I -S -B verify_manifest.py
    python3 -I -S -B run_checks.py

The first command verifies the exact file inventory, sizes, and SHA-256 values
in `MANIFEST.json`. The manifest excludes only itself to avoid circular
hashing. The verifier rejects missing files, extra files, changed bytes, and
symbolic links. It is an integrity check, not an external authenticity or
mathematical correctness certificate.

The second command makes a fresh temporary directory and copies only
`audit_set_cover.py` and `audit_set_cover_results.json` there. It invokes the
checker with Python's isolated, no-site-packages, no-bytecode options
`-I -S -B`. It requires a zero exit code, no standard-error output, valid
JSON stdout equal to the expected object, and byte-for-byte equality of the
generated result file with the shipped result. The original package is not
modified, and the temporary directory is removed afterward.

The checker can also be run directly as `python3 -I -S -B audit_set_cover.py`.
That direct invocation rewrites its neighboring result JSON with the same
deterministic bytes. The wrapper is preferred for read-only replay.

## What is checked

The proof's cone identity and Set Cover construction are corroborated in
three stages. First, explicit subset enumeration on 63 small block graphs
agrees with a separately coded compressed optimizer. Second, explicit
factor-critical subset enumeration on 14 cones agrees with that optimizer.
Third, 1,719 threshold decisions on all 441 fully covered set systems with
1 <= m,n <= 3 agree with exact Set Cover for every budget 0,...,n.

The compressed optimizer enumerates selected connectors, active blocks, their
connected incidence graphs, and injections matching connectors to block
representatives. Saturation gives the exact objective for this family;
`AUDIT_HARDNESS.md`, Section 7, explains this invariant. The larger checks
therefore do not enumerate every subset of their full expanded graphs.

The counts in `audit_set_cover_results.json` are deterministic. Date, runtime
version, and elapsed wall-clock time in a new replay report can vary.
`REPLAY_VERIFICATION.json` records the packaging-time run of the shipped
mathematical checker. `MANIFEST.json` covers that report and all other payload
files. The final package was separately replayed after manifest creation.

## Limits

Finite enumeration is corroboration, not the acceptance basis for an
unbounded complexity theorem. Read the complete proof and independent audit.
The computation checks the initial-odd-prefix factor-critical formulation,
not the distinct maximum total number of odd ears. The mathematical result
concerns a variable input threshold, not fixed-threshold NP-hardness.
