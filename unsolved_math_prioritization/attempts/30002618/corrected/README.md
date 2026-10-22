# Monodromy exactness for isocrystals: a residue criterion and a cycle case

Problem 30002618 / OWR-13102-007. Research date: 2026-10-06.

**Status: rigorous partial result, independently audited with a minor terminology correction and an explicit Gysin-hypothesis clarification.** This package does not solve the general coefficient-classification question or its geometric-origin expectation, and does not assert novelty.

The mathematical deliverable is `PROOF.md`. It derives a finite-dimensional criterion for the exactness defect from established residue, Gysin, and Mayer–Vietoris results. It then classifies the defect when the dual graph is a cycle and the coefficient connection is trivial on each component wide open.

Writing A for the horizontal-section incidence map and D for the signed Gysin map, the defect has dimension

    rank(A) - rank(DA).

In the cycle case, with graph holonomy T, exactness is equivalent to

    ker(T - I) intersect im(T - I) = 0.

Equivalently, eigenvalue 1 has only size-one Jordan blocks. This gives a precise restricted classification and recovers the mechanism of the already-published rank-two Tate-curve example.

`SOURCE_SCOPE.md` records the original question, the hypotheses, the established obstruction, later-literature scope checks, and limitations. `verification.json` and `source_metadata.json` contain bounded public verification metadata. No third-party source documents, source text, dataset contents, private records, or executable programs are included.

The independent audit checked the signs in the Gysin/incidence construction, residue surjectivity onto ker(D), the cycle quotient calculation, coefficient/Frobenius scope, and the stated symbolic examples. Acceptance is limited to these partial results; it is not a full solution or a novelty claim.
