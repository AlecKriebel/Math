# Review01 reproduction

This is the closed, fresh adversarial review of the exact six preprint inputs in INPUT_BINDINGS.json. REPORT.md and VERDICT.json are operative. A P3 OWR bibliography page-range correction remains; no package mutation or promotion was performed.

Authenticate this review with the externally reported MANIFEST.json SHA256:

    python3 -B verify_review.py --manifest-sha256 EXTERNAL_HASH --inputs
    python3 -B -O verify_review.py --manifest-sha256 EXTERNAL_HASH --inputs

To replay the audit code, first copy this closed review to a new scratch directory and point its sibling preprint path to the exact reviewed six files. Extract source-and-verification.zip into an `extracted` subdirectory of that scratch copy, then run independent_checks.py, replay.py and build_and_guards.py. These commands create receipts/scratch and therefore belong in a copy. The complete4-runtime checks use both Python3.14.6 and bundled3.12.14 paths recorded in replay.py. read_primary.py uses bundled pypdf for in-memory source retrieval; fetched content may change or become inaccessible. Primary URLs, actual identities and read-page ranges are in PRIMARY_RECEIPTS.json.

The packet preserves no source PDF or full source-paper text. The four rendered preprint pages are retained as visual evidence. Extracted/rebuilt/control scratch was removed after inspection, with receipts retained. Mathematical proofs and scope analysis are in REPORT.md; finite computations are not proof-assistant or exhaustive-priority certification.
