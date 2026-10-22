# Étale stage-3 obstruction: audited partial reconstruction

Problem 30005646; queue position 1851. Five approaches. Package date: 2026-10-21 UTC.

**Status: UNSOLVED in this reconstruction.** A September 2024 primary seminar announcement already claims a positive separation result. Its proof and explicit construction were not recovered. This package neither asserts that the problem remains open in the literature nor claims a new example or novelty for the partial observations.

The target is strict inclusion X(A_K)^h ⊊ X(A_K)^{h,2} for K=k(C), k a finite extension of Q_p, using the closed-point places of C. The smooth projective geometrically integral model of C is the working convention. The source's geometrically simply connected, geometric homology H_3=0 subclass is highlighted, not imposed on every possible answer.

## Contents and accepted scope

- SOURCE_GATE.md recovers the target, announced status, and exact source limitations.
- FIVE_APPROACHES.md records five reconstruction attempts and their unresolved bridges.
- FINITE_STAGE_LEMMA.md proves the finite lifting and local-monodromy-orbit matching criterion, with its countable finite-module limit qualification.
- INDEPENDENT_OBSTRUCTION_AUDIT.md proves the corrected Mittag-Leffler lemma and audits why Tian's different cohomological separation is not a stage-3 witness.
- FINAL_CLAIMS_ACCEPTANCE.md accepts only the bounded mathematical partials.
- SOURCE_METADATA.json lists public scholarly source metadata, without redistributing sources.

Accepted partials include an explicit finite-support H^3 mismatch, a rational-surface Whitehead pi_3 calculation, R-equivalence pruning for unrigidified point evaluation, and the split P^1 x P^1 and SL_2/G_m nonexamples. Tian's construction has geometric pi_1 through pi_3 zero; this does not independently establish a full-tower triviality theorem.

**No algebraic variety with an actual adelic point witnessing the requested strictness has been constructed here.** The formal cohomology family is not asserted to be realized by local rational points. Every local monodromy orbit and every matching global stage-2 component must still be handled. The displayed arguments and cited theorems, not computational tests, support the partial mathematics.

## Reproducibility

Run from this directory:

    python3 -B verify.py
    python3 -B -O verify.py

The verifier checks an exact recursive inventory, SHA-256 hashes and byte lengths, rejects symbolic links, and tests missing, altered, extra, nested-manifest, and manifest-key tampering under normal and optimized Python. Only the root MANIFEST.json is exempt from self-hashing; its hash is frozen externally in the release receipt. There are no computational arithmetic proofs or mathematical-check scripts in this package. Verification output concerns packaging integrity only, not validity of an arithmetic existence theorem. The external independent package audit must review privacy and the mathematical scope separately.
