# Final adversarial reproducibility review

Date: 2026-08-17
Scope: bounded v1.1.3 pre-seal release candidate
Method: fresh read-only implementation and mutation audit

## Verdict

No blocking defect was found.  This report validates the release machinery
and current submission-package bytes before the immutable tag, external
archive, envelope, and clean-checkout transcripts are created.  Those final
public objects remain subject to `verify_public_release.py`.

## Gates independently passed

1. **Literal source replay.**  Each source ZIP was extracted into a fresh
   directory after removing inherited `SOURCE_DATE_EPOCH`; its documented
   commands reproduced all six article/supplement PDFs and both cover letters
   byte for byte.
2. **Tag/archive binding.**  The public verifier requires a genuine annotated
   tag, compares the complete tracked project path set, Git blob hashes, and
   executable modes against the release archive, and executes the extracted-
   archive verifier.
3. **Clone/archive distinction.**  All three byte-identical verifier capsules
   distinguish commands that require a cloned tag from the fail-closed gate
   available in a complete plain release archive.  None presents the small
   capsule as the proof archive.
4. **Journal-aware routing.**  bioRxiv receives the compact capsule;
   Systematic Biology and the Journal of Mathematical Biology retain it for
   the external repository deposit rather than misclassifying it as a portal
   manuscript file or JMB Online Resource.
5. **Current manifest coverage.**  The v1.1.3 gate fixes the exact 7/9/9-file
   package universes, includes each capsule, and rejects capsule omission.
   The v1.1.2 regression is explicitly historical and is not used as the
   current manifest parser.
6. **Status and dependency hygiene.**  No fixed stale archive-size claim, DOI
   invention, contradictory active outcome, or active absolute/cloud-only
   executable dependency was found.
7. **Exact package checks.**  All three outer manifests, every capsule-internal
   checksum, and the targeted v1.1.3 verifier passed.  The pre-seal capsule
   SHA-256 was
   `03e6d20c426782a79599013fa59a4a6da6d8ddb8a4dbc11f2529b2923212bc60`.

## Mutations rejected

- altered tagged source byte or executable mode;
- missing or extra tracked file;
- lightweight tag or annotated tag pointing to another tag;
- missing public release asset;
- capsule omission from each actual package manifest;
- altered capsule member without checksum update;
- removal of the archive-local deterministic build epoch;
- failing nested extracted verifier;
- archive path traversal;
- changing Omega taxonomy from type (2c) to type (1b);
- breaking the `q_{123}`/`q_{111}` notation transport;
- replacing a rank determinant by zero; and
- changing the Omega Jacobian row set.

The earlier two failed reproducibility reviews are preserved separately.  The
repairs they forced are part of this reviewed state rather than being erased
from the record.

PASS
