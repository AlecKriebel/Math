# Independent acceptance of a credited prior disproof

This audit concerns ID 2200007 / AMR-021-0007, rank 899. The mathematical verdict
is FALSE_BY_PRIOR_COUNTEREXAMPLE, credited to DannyExperiments, with zero new
research approaches. Read AUDIT.md for the proof and executable limitations.

ACCEPTANCE.json identifies the exact original freeze and separately hardened
replay derivative. HARDENING.patch is the real three-file change, not a proposed
repair. SOURCE_AUDIT.json records independent corpus identities and source
inspection without redistributing source or dataset contents.

Run from any working directory, using actual paths:

    python3 -I -S -B verify_audit.py ORIGINAL_ZIP HARDENED_ZIP

Use the exact original and hardened archives identified in ACCEPTANCE.json.
Optionally add -O or -OO after the interpreter. Successful output equals
CHECK_RESULTS.json. The audit checks archive pins before executing either input,
then replays exact arithmetic and adversarial cases offline. A trusted Python
installation is required. Pin this audit itself using its external manifest.

This is mathematical/code verification, not human peer review, formal proof
certification, an exact-maximum determination, or a new discovery. No publication
is performed by the checker.
