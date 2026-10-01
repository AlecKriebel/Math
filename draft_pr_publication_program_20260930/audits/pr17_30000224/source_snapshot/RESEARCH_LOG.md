# Research log: 30000224

All timestamps UTC. Budget: 2026-09-30 03:53–05:53; at most five substantive
approaches. Execution model: gpt-6-astra, xhigh. Completion estimates concern
the full original question, not the amount of documentation completed.

## 03:53–03:58: source and literature audit

- Verified the pinned complete record and exact original OWR question, p.1116,
  together with Singh–Walther Example3.5/Question3.6.
- No prior repository attempt, issue/PR, or duplicate dataset target found.
- The quantifier permits nonhomogeneous b; neither a set-theoretic complete
  intersection nor a homogeneous thickening may silently replace the target.
- Ma–Schwede–Shimomoto's Du Bois obstruction does not immediately apply; the
  cone has the missing degree-one monomial s²t² and is not seminormal.
- Checked the newer residual-intersection theorem of Hassanzadeh (2025).
  Applying it requires hypotheses on the linked ideal, not merely linkage.
- No complete resolution found in the bounded current-literature search.
- Completion estimate: 0% toward full resolution. No candidate claimed.

## 03:58–04:06: four bounded approaches

1. Reconstructed the one-dimensional positive-degree deficiency and the exact
   seminormality failure. The standard Du Bois/nonpositive-degree tests do not
   apply. This provides a precise failed route rather than a negative answer.
2. Proved that any CM thickening containing the quadric would be a symbolic
   divisorial power, whose projective cohomology is nonzero. Separately, the
   explicit balanced conormal bundle excludes homogeneous double structures.
3. Checked the recent residual-intersection theorem on the natural skew-line
   link. An explicit Koszul socle proves that the needed depth hypotheses fail.
4. Proved the binomial route impossible by Laurent localization and reduced
   abelian group algebras in characteristic zero.

No full candidate was obtained. The unexcluded case is a non-binomial ideal
with transverse nilpotence along the quadric; in the homogeneous case its
generic multiplicity must be at least three. The nonhomogeneous case is not
replaced by its associated graded ring.

Completion estimate: 5% toward the full original target, reflecting only
restricted exclusions; this is not a success probability or novelty claim.

## 04:06–04:11: proof and exact certificate checkpoint

- Saved the complete restricted proofs and exact remaining gap in
  PARTIAL_RESULTS.md.
- Wrote a fresh standard-library sparse-polynomial verifier. All135 assertions
  passed, including polynomial frame identities, covering minors, four Koszul
  annihilator identities, and the rank6/rank7 nonboundary certificate.
- Source review includes the 2025 theorem and original OWR page image.
- Further search was stopped after the tested mechanisms failed to address
  the remaining class. No fifth attempt or full-resolution claim was created.
- Independent adversarial review remains required before a draft PR.
- Completion estimate remains5% toward the original target.
