# Formulation audit: closed leaves and genus minimization

ID 2999 / KP-4.123. Checked 2026-10-06.

## Result

The literal weak-form definition in K3 is refuted by the explicit Hopf-product foliation of S³×S¹. The stronger closed-positive-form problem posed by Kronheimer is not resolved by this work. PROOF.md supplies a complete elementary counterexample and proves why it is excluded by the original hypothesis.

Do not report this as a solution of Kronheimer's original conjecture. The elementary construction is not claimed to be new. The S²×S² subquestion remains untouched. The counterexample uses a null-homologous leaf; it does not refute a variant restricted to nonzero homology classes.

## Source comparison

K3, p. 292, imposes positivity of a two-form on the leaf tangent planes and vanishing of its exterior derivative when two input vectors are leafwise. Kronheimer's original discussion requires a globally closed positive two-form on a closed oriented ambient four-manifold. Closedness implies the K3 differential condition; the Hopf product proves that the converse fails even for smooth coorientable compact-leaf foliations of closed four-manifolds.

Scorpan's Theorem 3.5 describes the weaker differential condition as the geometric tautness criterion. Thus the issue is not merely corrupted OCR. The K3 page was visually inspected. The original Kronheimer paragraph was inspected through the public PDF text; direct binary retrieval from that site returned HTTP 403, so no locally fetched PDF hash is claimed for it.

## Literature boundary

- Kronheimer Question 7.12: original closed-positive-form hypothesis, and associated adjunction question.
- Ozsváth–Szabó Theorem 1.1: genus minimality for an embedded symplectic surface in a closed symplectic four-manifold. This settles the compatible symplectic special case, not an arbitrary weakly taut foliation.
- Scorpan, Existence of foliations on 4-manifolds, Theorem 3.5 and discussion of Conjecture 3.9: useful distinction between geometric tautness, forms, and additional assumptions for genus bounds. https://arxiv.org/abs/math/0302318
- Bowden, On closed leaves of foliations, multisections and stable commutator lengths, Examples 2.6–2.7: non-minimal compact leaves in general foliations. That construction does not establish the stronger closed-form hypothesis. https://arxiv.org/abs/1105.4444

The dated public problem-list evidence continues to present the original-type question as open. Bounded current literature searches did not produce a verified theorem resolving the closed-positive-form generality. Search absence is not proof of openness or originality. The exact public problem page was attempted with and without www but the web retrieval tool could not open it; the catalog identity and authoritative K3 source were used instead.

## Verification

The analytic construction, global foliation, integral bounding chain, and lower-genus competitor are proved explicitly. The standalone checker uses exact integer polynomial differential-form algebra to verify positivity, tangency, the weak derivative condition, nonclosedness, and the relevant sphere-product homology ranks. The checker is a finite identity check, not a formal verifier for the topological proof or a solver of the original conjecture.

All checks use explicit exceptions rather than Python assert statements and run identically under python -O. Self-tests check that deliberately false identities are rejected. Optional dataset verification requires all three input files, exact sizes and SHA-256 values, a unique exact-ID record, the statement hash, the complete record/report pair hash, and an empty inherited report. It does not reclassify inherited prose automatically.

## Recommended status

Formulation counterexample; original problem unresolved here. Two substantive approaches were used, then stopped because the weaker literal statement had a complete counterexample while the original case had an exact excluded hypothesis. The remaining three approach slots were not consumed. No external correspondence, publication, or queue edit is part of this package.
