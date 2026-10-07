# Adversarial report review

Checkpoint: 2026-10-07 15:10 UTC. Bounded report review **100% complete**. Reviewed REPORT.md, SCORES.json, all six subject-note files (the root quantum/Sperner note included), and the four geometry final manuscripts already inspected. This is not a new full proof audit. No external communication, Git operation, or source/report mutation was performed.

## Verdict

The report passes on paper coverage, record identities, main A/B calibration and attribution. There are **two small but concrete wording corrections** worth making before delivery; neither changes a score. I found no omitted paper, material wrong theorem range, or improper claim of an independent upstream breakthrough. A script confirms 19 unique score rows, exactly rows 35–53, 19 report table rows, and correct inventory DOI/record identifiers throughout.

## Correct the target class in even Minkowski's summary

Current report/SCORES summary says a symmetric measurement determines "one convex shape in the stated smooth setting." The theorem requires the sought shape to be **origin-symmetric**, not only the measured data to be even. The current wording could be read as uniqueness among all smooth convex shapes. Replace with:

> Shows that prescribed smooth positive even curvature-type data determine one origin-symmetric convex shape, across the logarithmic and related parameter range.

This follows the actual final theorem's positive even support-function class. The existing endpoint limitation is accurate. An optional extra sentence could mention the nonsmooth positive-p uniqueness theorem, but its omission does not invalidate the compact summary.

## Correct the C*-simplicity lay wording

The Thompson row says "no proper internal ideals." A unital algebra still has the zero ideal, and C*-simplicity concerns **closed** two-sided ideals. Use "no nontrivial proper closed ideals" (or "cannot be decomposed through a nontrivial closed ideal") and retain "only one normalized trace." This is precision in the lay assertion, not a new scope objection. The exact subject notes correctly distinguish reduced group C*-algebras and the action-containment hypothesis.

## Items deliberately not treated as substantive objections

- Binary A=9 and hafnian A=9 are coherent with the conditional theorem-content rubric: fixed-binary superpolynomial simulation lower bounds already refute the canonical polynomial target, and nonnegative rational hafnians include all unweighted perfect-matching instances. Their low B scores correctly retain external credit.
- Finite-field A=7 rates the actual principal sparse theorem, rather than silently awarding the inherited dense breakthrough. The new sparse descent justifies the high incremental B=7. Choosing 7 versus 8 is calibration, not a scope error.
- Random-cone A=5 and cubic A=7 match the final manuscripts' actual emphasis. The report does not pretend that their inherited idempotent or complex K/GIT conclusions are new principal contributions. The threshold is specifically dyadic in the exact notes; adding "dyadic" to its short row would improve precision but "permitted parameter for one recipe" already limits the summary.
- Bosonic A=8/B=6 are supported by the root note: the two dynamic resource regions and the operational secrecy repair are distinct, the private formula has the replacement GEN convention, and eta>=1/2 plus average photon budget are stated. No unrepaired literal-model characterization is claimed. This is more actual new work than an ordinary corollary note.
- Sperner A=7.5/B=4 correctly distinguishes the broad all-ideal characteristic-zero complete-intersection statement from inherited EGH and the established implication. It does not claim Lefschetz or unrestricted positive characteristic.
- The planar numerical programs have L2=2/sqrt(3), P2=4/3; their packing bounds agree **after the stated square-root normalization**. The report says their packing bound is the same, rather than asserting L2=P2, so I do not flag this as false. Adding "after normalization" would make the lay wording unambiguous.
- The Costa summary's "algebraic space" is technically broad rather than false (the image is a smooth affine variety). "Smooth affine variety" would be clearer. Cubic summary and attribution agree with the actual singular Cartier-index theorem and already public KSZZ complex comparison.
- Unrefereed or AI status is not used as a disguised correctness penalty; the report expressly conditions A on correctness. Public source hashes establish custody, not proof validity, and the report preserves this distinction.

Recommendation: make the two direct wording repairs in both REPORT.md and SCORES.json, then deliver. No reranking or additional proof audit is needed for this bounded impact task.
