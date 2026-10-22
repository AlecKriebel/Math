# Research log: 30004494

Date: 2026-10-05 (UTC). Original target remains unsolved. Percentages below are subjective completion estimates toward a full proof of the original target, not probabilities of correctness or measured progress. The source-verification deliverable and mathematical target are separate.

## Initial inspection, 16:10-16:19 UTC

- Started with the specified problem URL. Direct retrieval was unavailable/403; no access restriction was bypassed.
- Matched the descriptor to the exact record in a byte-verified copy of the public dataset and then checked the official OWR contribution and 2021 precise formulation.
- Read actual repository instructions, README, current selected queue row, related-target groups and targeted prior-attempt searches. No matching prior proof attempt was found. The imported report collection has no matching key/ID; therefore there was no prior imported proof to adopt or refute.
- Checked current primary arXiv versions, not just old source descriptions. Discovered the withdrawn 2021 progress report, 2025 determinant-descent correction, BFMT 2025 full-Griffiths semiampleness, 2025 boundary-theta paper and 2025 generalized toroidal completion.
- Full-target estimate: 10%. Status inference: meaningful adjacent progress, no verified resolution of the fixed-boundary assertion.

## Attempt 1: modern completion and bundle-comparison route

Mechanism: try to deduce the target from the latest Baily-Borel/Griffiths semiampleness theorem.

Work retained: exact determinant pairing under polarization. In even weight the full Griffiths bundle is a torsion twist of the square of the old augmented bundle; in odd weight it has the middle factor only once. The even-weight semiampleness deduction is valid, with a torsion-killing power. The old odd-weight descent claim cannot be recycled.

Outcome: partial. Ampleness on the image pulls back only to a semiample bundle on X. Positive-dimensional fibres still need an effective boundary divisor with relatively ample negative. The corresponding global boundary support and signs have not been supplied. A completion after modifying X also changes the question.

Checkpoint estimate: 15%. Proof source: SOURCE_AUDIT.md section 4 and PROOFS.md section 4. No claim of reproducing BFMT's long proof.

## Attempt 2: Hodge-index and Nakai route

Mechanism: exploit nefness/bigness and isolate period-constant boundary curves.

Work retained: complete algebraic surface theorem, including finiteness of null curves, negative definiteness of their intersection matrix, a strictly positive rational vector -A^(-1)1, denominator clearing, and a Kodaira-lemma argument producing one threshold valid for all curves. The disconnected-eigenvector shortcut is rejected explicitly. The unweighted correction fails in the exact matrix [[-5,2],[2,-1]], while coefficients (3,7) work.

Outcome: known surface mechanism reconstructed rigorously. Higher-dimensional null loci are not governed by one negative-definite boundary-curve matrix, so this is not an extension to the whole target.

Checkpoint estimate: 20%. Proof source: PROOFS.md section 3. No novelty claim.

## Attempt 3: birational and hypothesis stress tests

Mechanism: test whether generic immersion or replacing the compactification can be used harmlessly.

Work retained: an interior blowup of a generically immersive VHS gives an exceptional curve invisible to every boundary correction, disproving the generic-immersion weakening. The construction is explicitly outside logarithmic fibrewise injectivity. A boundary-blowup stability theorem includes the necessary exceptional correction and proves eventual ampleness for every integer m.

Outcome: useful controls; no counterexample to the actual target. Pullback, birational modification, generic immersion and logarithmic local Torelli must remain distinct.

Checkpoint estimate: 20%. Proof source: PROOFS.md sections 4.2-4.3.

## Attempt 4: closed-null-face and uniformity route

Mechanism: translate the problem into positivity on the compact normalized closed cone of curve classes.

Work retained: exact equivalence between eventual ampleness of mL-E and strict positivity of -E on the whole closed L-null face. The proof produces a uniform threshold using compactness and Kleiman. Real coefficients can be rationalized and cleared to fixed nonnegative integers because the ample cone is open and L is nef.

Outcome: exact reduction, not a solution. The target hypothesis has not been shown to imply the existence of a common boundary E in the required cone. The curved-cone example proves why separate m(C) thresholds are insufficient.

Checkpoint estimate: 20%. Proof source: PROOFS.md sections 1-2.

## Attempt 5: global compatibility and exact dual certificates

Mechanism: in the rational-polyhedral case, express the common coefficient problem as a strict finite linear system on null rays, then study its alternative.

Work retained: necessary-and-sufficient finite-cone criterion; a separating-hyperplane proof of the nonnegative dual certificate; and a two-row obstruction showing that separate local choices do not imply a common choice. The recent boundary-theta relation was checked with the actual normal/conormal sign and is not silently converted into nonnegative global correction coefficients.

Outcome: partial. The numerical obstruction matrix is not a geometric counterexample. No theorem here establishes the required Hodge-realizability restrictions or excludes all dual obstructions in general. The original target remains unsolved, and the five-turn budget is exhausted. No further proof search is included in auditing this packet.

Final full-target estimate: 20%. A precise reduction and known special cases have been secured; the central compatibility problem remains open in this investigation.

## Validation checkpoint, 16:26 UTC

The standard-library exact control runner passes 18,549 assertions over 2,200 positive-definite sign-controlled matrices, 1,000 curved-cone tests, weights 1 through 40 for determinant bookkeeping, the disconnected-matrix control, and finite feasibility/duality tests. An initial output-serialization variable-shadowing bug was fixed; the final runner and complete output were rerun successfully. These tests supplement the proofs and do not establish the conjecture.

The authored safe packet is to be frozen for an uninvolved audit. No remote repository changes, messages to researchers, releases or external submissions were made by the author. Independent review must check the whole written argument and current source qualifications, not only replay arithmetic.
