# Acceptance of the corrected Jiang–Su investigation

Date: 2026-10-06 UTC. Problem 30002218 / OWR-12175-007.

## Disposition

The original question remains unresolved after five substantive approaches. No counterexample or novelty claim is accepted or made.

The frozen original package is not accepted unchanged. The corrected ten-file derivative is accepted at its explicit scope. Seven files change through CORRECTION.patch; applying that patch to a fresh extraction of the original reproduces every corrected file exactly. The original archive and external manifest still match their initial pins.

The same independent auditor identified the issues, prepared the corrective patch, and reran acceptance. No additional independent post-patch reviewer is claimed.

## Mathematical changes

- The source's Cuntz-transfer radius 1/6422957 is preserved as a published statement. It is not independently certified by the original or corrected arithmetic audit: PTWW Lemma 4.12 includes a leading k in β which Proposition 4.13 drops. This is a proof-chain discrepancy, not a counterexample to the published conclusion.
- Retaining k gives a verified conservative radius 1/16000000 for the common-unit unital subcase. The scope restriction respects the nondegeneracy hypothesis of the complete-near-inclusion proposition. No arbitrary-support or arbitrary-nonunital quantitative reconstruction is claimed.
- The conditional central-sequence theorem is accepted after choosing γ<γ₁<1/12600000 before invoking strict uniform near inclusion. Its theorem statement is unchanged.
- The separability bridge, nuclear nonunital isomorphism subcase, commutator upper bound, coordinate-selection warning, relative-commutant example, and common-unit unital closedness argument are accepted as explained in INDEPENDENT_AUDIT.md.

## Machine checks and their limits

The 28 recorded validation checks passed. They cover original and corrected hashes, strict inventories, UTF-8 and JSON parsing, CRCs, normal and optimized isolated Python runs, relocation, import-shadow and poisoned-cache immunity, authoritative root selection, adverse root and archive mutations, exact patch replay, preservation of the original, and supplementary exact arithmetic.

Validation is run under -I -S, with -O comparison. The checker is not part of either public bundle; both bundles contain zero executable programs. Code-execution gates are consequently inapplicable to the deliverable itself. The reported runner controls describe the private integrity checks, not a formal mathematical verifier. Exact arithmetic does not certify the analytic arguments.

The strict external manifest and its separately pinned digest are the authority for the corrected archive. The human report gives the mathematical acceptance scope; a successful checksum comparison does not expand it.
