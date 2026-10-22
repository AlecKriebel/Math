# Borderline soliton independent audit

Problem 30001591 / OWR-4429-002, queue rank 978. The PDE target remains unsolved, with five approaches completed out of five.

FULL_AUDIT.md gives the complete mathematical and source audit. The original packet requires a genuine Section 5 hypothesis repair: strict increase does not imply a positive derivative at the turning point. CORRECTION.patch applies the repair, explains a flat-crossing counterexample, and clarifies boundedness in the cubic lemma and the distinction between profile scale and center velocity. PARTIAL_RESULTS.corrected.md is the accepted corrected authored proof. Original files are not changed.

The bundle includes 78 independent exact controls, nine rejected wrong mathematical controls, public source-verification metadata, and 12 packet-integrity and direct-replay checks. These support the mathematical audit; they do not prove the original PDE asymptotic or constitute formal verification or human peer review.

## Reproduction

With Python 3 and SymPy installed, run:

    python3 -B verify_audit.py /path/to/original/release TRUSTED_AUDIT_MANIFEST_SHA256

The trusted digest is published separately from this bundle. Omitting it checks self-consistency only. The verifier independently pins the supplied original author's manifest and original proof, verifies exact correction bytes, and directly replays both the author's and independent algebra scripts in ordinary and optimized Python. It requires the original release directory to be available unchanged.

AUDIT_MANIFEST.json records frozen audit payload hashes and byte counts. The audit contains no source PDFs, copied third-party source text, corpus records, screenshots, or private coordination material. AUDIT_SOURCE_METADATA.json distinguishes locally verified byte identities from remote revision authentication and records the actual source inspection limits.
