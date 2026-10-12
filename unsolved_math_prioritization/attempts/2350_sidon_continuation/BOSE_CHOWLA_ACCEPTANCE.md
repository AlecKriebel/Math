# Acceptance: Bose–Chowla canonical carries

Status: ACCEPTED AFTER A MINOR TOPOLOGY CLARIFICATION.

Accepted proof: `BOSE_CHOWLA_CARRY_PROOF.md`

- SHA-256: `6fa26f9c48ee904ef3f7b739d50a42ebf7e40c2cb2c4b03105b3032f8b8f4390`
- Bytes: 14902
- Frozen authored input manifest: `4088f2b016f57293f67daa0a97bf33e706c2c8da7ed8f30d6fe9f204eb1d1d9d`
- Original proof: `d6568efa627e1904813fe5509806c1f408f76e7dec53ce97b8c3fc06e97737b3` (14,185 bytes), preserved unchanged.

The proof is accepted for canonical length-q integer and single-coset half-integer lifts of every translate/unit dilation of the Bose–Chowla p-set, q=p²−1, uniformly as odd field order tends to infinity. It proves carry proportions 1/6, 2/3, 1/6 and a deletion requirement of at least (1/30−o(1))p for a triple-sum-free subset.

The correction makes the continuity-set argument explicitly relative to the supporting subgroup H. The original algebra, complete nonprincipal CRT-character split, half-integer congruence, seam estimates, and repeated-entry deletion incidence all passed. A small source-page correction and notation clarification are included. No theorem constant changed.

The external input is established function-field Dirichlet RH. Its general-modulus applicability was independently checked in the inspected Kopparty notes; no irreducibility-only bound was silently extended.

Independent checks passed for all 736 μ parameters over field orders 3, 5, 7, 9, 11, 13, 17; 2,021,760 direct triple products; 14,832 canonical lifts; 12,800 subset/lift checks; and numerical global/local Fourier diagnostics with explicit scope. Finite computation is not offered as the asymptotic proof. Full coverage and caveats are in `AUDIT_BOSE_CHOWLA_CARRIES.md`; exact program/results hashes are in `INPUT_PINS.json`.

This acceptance does not resolve Erdős 864, establish the √(2/3) bound, cover arbitrary Sidon sets or noncanonical lifts, supply an effective threshold, or certify novelty. No publication, repository mutation, queue change, or remote action occurred.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
