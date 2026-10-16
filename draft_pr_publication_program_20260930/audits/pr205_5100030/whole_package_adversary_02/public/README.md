# PR205 second fresh whole-package adversarial review

REPORT.md is the scoped clean assessment. FINDINGS.json records zero substantive repair requests and the separately disclosed index-handling incident. Root owns acceptance and publication. The reviewed packet and all upload hashes are in REPORT.md and EXACT_BINDINGS.json.

Only files in PUBLIC_SAFE_MANIFEST.json are proposed as public authored outputs. The parent audit directory's private primary PDFs/text/images, wrappers, full command receipts, operational/Git snapshots and pilot outputs are excluded. No full third-party texts or dependency/runtime copies are supplied.

## Reproduce the new diagnostics

Use Python3.10+ with mpmath1.3.0 installed. Extract the exact reviewed verification-package.zip into an empty folder named packet. From this review folder run:

    python3 -B independent_diagnostics.py > my_independent.json
    python3 -B fault_probes.py --verifier packet/verification/verify.py --historical packet/materials/original_submitted_head > my_fault_normal.json
    python3 -B -O fault_probes.py --verifier packet/verification/verify.py --historical packet/materials/original_submitted_head > my_fault_optimized.json

Both authored programs optionally take --runtime /path/to/external/site-packages, enabling strict -E -S -B -P execution without installation or copying. Run the current packet verifier using its documented commands in packet/verification; the recorded current stdout must match the packet's ordinary/optimized result files on the stated Python3.14.6/mpmath1.3.0 environment. Different Python versions alter the reported version field. Actual execution records also bind exact exit codes and source identities.

The two historical ordinary replays are provenance checks only; they additionally used existing read-only sympy1.14.0. Those old scripts are vulnerable controls, never the current recommended checker. The new fault probes execute selected exact historical AST functions to demonstrate those vulnerabilities without running either historical suite.

All numerical evidence is finite and noninterval. FROZEN_INDEPENDENT_MATH.md has a separate, explicit MATH_FREEZE_ERRATUM.md for the reviewer's shorthand transcription; read them together. The current packet needed no correction.
