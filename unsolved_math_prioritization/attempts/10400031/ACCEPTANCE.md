# Acceptance report: pointwise signature approximation reductions

Problem 10400031 / AMR-103-0031, Ohtsuki Problem 2.9. Edition dated 2026-10-11.

**ACCEPTED as scoped partial results with explicitly imported dependencies. The original all-knots full-signature question remains unresolved by this work.**

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made, and no exhaustive current-openness claim is made.

## Accepted mathematical scope

- Finite-type invariants form a filtered rational algebra; products add degree bounds and fixed connected-sum, mirror and reversal pullbacks preserve them.
- For a rational target on countably many knot types, finite-type pair separation, exact finite interpolation, pointwise approximation and eventual-exact approximation are equivalent.
- Full signature approximation on all knots is equivalent to detecting every nonzero-signature knot against its mirror by some rational finite-type invariant.
- An explicit rational finite-type sequence R_n=1-h_n(D_n), of type at most 2n(2n-1), is eventually exactly the representative 0 or 2 of signature modulo 4 on every knot.
- Willerton’s v_2,v_3 torus formulas give a globally defined finite-type sequence Q_n, of type at most 6(n-1), eventually equal to full signature on every torus knot; no convergence outside that family is asserted.
- Stoimenow’s imported strict-cutoff theorem gives infinite global error for every fixed finite-type invariant, which does not prohibit pointwise convergence.
- Alexander-only approximants fail on opposite trefoils; the imported rational S-equivalence theorem extends that obstruction to individually S-equivalence-invariant rational finite-type approximants.

The full mathematical argument is retained in PROOF.md and the complete independent review in AUDIT.md. No blocking proof defect was found. The edition incorporates the auditor’s nonblocking torus-domain clarification and makes the audited strict-degree cutoff n=d+1 explicit. Neither change claims a new theorem beyond the accepted scope.

## Exact remaining problem and boundaries

- The all-knots full-signature question is unresolved by this work.
- The exact residual is nonzero-signature mirror detection at all degrees, or one fixed knot violating it.
- Interpolation is nonconstructive until its separating invariants are supplied.
- Different knots at different finite cutoffs do not give one all-degree counterexample.
- The signed normalized Alexander value is essential; the absolute determinant and residue alone do not recover full signature.
- Torus parameters are coprime integers, unknot representations are handled before division, and oriented torus knots are invertible.
- Willerton’s formulas and standard classification, Stoimenow’s realization theorem, and the rational S-equivalence result are imported dependencies with the source limits in SOURCES.json.
- No novelty, priority, exhaustive current-status, human peer-review, or proof-assistant certification is claimed.

A positive resolution must prove finite-type mirror detection for every nonzero-signature knot. A negative resolution must supply one fixed such knot with an all-degree proof of mirror invisibility. Neither finite tests nor the torus family meet that requirement.

## Historical evidence and review status

The creator’s closed 41-member inventory and the independent audit’s closed 19-member inventory were authenticated with separate external seals. The creator tested 210 sign nodes, 125 genus-one Seifert forms and 16 block pairs, 156 signed torus parameter instances, and five interpolation nodes, with five actual mathematical negative controls. The independent audit used a separate implementation: 156 sign nodes, 184 Seifert matrices of genera 0 through 3, 21 eventual-residue instances, 640 coprime signed parameter instances including 128 unknot representations and 129 distinct types, and 15 interpolation nodes, with ten actual mathematical negative controls. Both historical studies ran under normal, -O, and -OO Python. The independent auditor inspected but did not execute the creator’s code. Five copied-fixture integrity corruptions were independently rejected.

These bounded calculations corroborate the prose proofs and do not establish knot separation. The edition preparer only rechecks byte integrity and packaging and does not rerun mathematical programs or inspect new scholarly-source bodies. Source retrieval, selected-page reading, full-proof limitations, exact arXiv revisions, and historical versus current-status claims remain separate in SOURCES.json.

Only eight authored prose and metadata files are distributed. Code, raw computational data, copied sources, source images, derived source extracts, and private coordination material are excluded. All essential formulas, the opposite-trefoil matrices, and the finite-control examples remain as mathematical proof content.
