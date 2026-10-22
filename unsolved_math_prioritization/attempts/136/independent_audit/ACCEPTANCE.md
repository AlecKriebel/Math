# Independent acceptance: bounded partial only

Problem ID 136; GREEN-048; rank 879. Date: 6 October 2026.

## Decision

ACCEPT the corrected derivative identified below for the stated elementary partial theorem and qualified source assessment. The general straight-line discrepancy-at-most-100 question remains unresolved. This is neither acceptance of a complete solution nor a novelty certification.

The original mathematical proof is valid and byte-unchanged. The original package is not accepted as final prose without the accompanying qualification of its source-correction language. The repaired derivative has actually been constructed, and the supplied patch reproduces it exactly from the original freeze.

## Exact accepted artifact

- Corrected archive: BALANCED_HAM_SANDWICH_136_CORRECTED_SAFE.zip
- Archive size: 14,935 bytes
- Archive SHA-256: 4e8760aad4c89b87a70299c2bf1a625a85f995827dadb67734f3621ec75c2aac
- External manifest: BALANCED_HAM_SANDWICH_136_CORRECTED_EXTERNAL_MANIFEST.json
- Manifest size: 2,141 bytes
- Manifest SHA-256: d96da59ed024b2c8eae8647a564a7b15f1128aa2637eb4e9c40f50fa1c2f0378
- Six member hashes and byte counts: ACCEPTED_DERIVATIVE_MANIFEST.json, an exact copy of that external manifest
- Unchanged PROOF.md SHA-256: 60be39fa2267ac5010f1d6247fb46853e347c773c2bdc35fed3412ce2c3a007a

## Accepted mathematical content

For every finite set of n>=2 distinct planar points and every exposed hull vertex p, a determined straight line through p has open-half-plane discrepancy at most m_p-2+(n mod 2), where m_p is maximum collinearity through p. The proof handles complete collinear blocks, one-dimensional hulls, n=2, and both parities.

Consequently, threshold 100 is proved whenever some exposed p has m_p<=101, or m_p<=102 for even n. The global bound, exact general-position values, rich-line implication, symmetry-zero result, and necessary counterexample conditions in PROOF.md are accepted. The perturbation argument correctly accounts for disappearing boundary signs and supplies no uniform constant independent of collinearity.

## Accepted limits

- No universal bound of 100 or 2 is proved.
- No counterexample to the straight-line target is produced.
- The D=2 example recorded by Pinchasi only disproves universal bound 1; it does not exclude another stronger example.
- Green's stronger threshold sentence is treated as an apparent source discrepancy in light of dated primary reports, not as definitively corrected.
- Pseudoline counterexamples are not treated as straight-line realizations.
- The 2025 computational construction/minimality and the full proofs of cited asymptotic theorems were not independently reproduced.
- Current-status conclusions are dated and bounded by the inspected sources and searches.
- The finite exact-integer checks are supplementary sanity checks, not universal proof or formal verification.

## Integrity and provenance

The original author ZIP has 13,843 bytes and SHA-256 2d1d617f117691972a13f391d685c5668fa7593a7f87fb749d70522da8d130c2. Its external manifest has 1,897 bytes and SHA-256 2253df64708be4d8331bd37726dc0cf7b3f0893342c2c17d3084da93ec8e05e3. These originals remain unchanged.

The three complete corpus pins, the 198-byte target-statement pin, the complete 2,579-byte problem/report pair pin, and all five public source-document pins were independently rechecked. The inherited report is absent and evaluates to the specified empty-object default. All six original and six corrected ZIP members were read back. The source-wording patch replay reproduces the corrected members byte-for-byte.

Publication was not performed. The mathematical rationale and inspection limits are in AUDIT.md; machine-readable checks are in AUDIT_VERIFICATION_METADATA.json.
