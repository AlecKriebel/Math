# Research log: 10000062

All times UTC,2026-09-30. Budget04:13–06:13, maximum5 substantive approaches.
Execution model:gpt-6-astra,xhigh. Completion estimates are subjective and
refer to the stated scope, not verified novelty.

## 04:13–04:19: exact source and prior work

- Pinned dataset, prior report, queue, source instructions and duplicate checks
  completed; no previous attempt or duplicate found in accessible records.
- Recovered the original archived PDF and visually checked Question5.7,p.7.
- The word periodic is undefined. Euclidean and hyperbolic clauses preserved.
- Located Frettlöh–Garber's prior alternating-layer family, including Figure17.
  Its monocoronal property alone does not establish the stronger ball condition.
- Formulated the separate Euclidean cocompactness subproblem explicitly.
- Completion estimate:0% full source resolution;40% scoped construction.

## 04:19–04:27: first construction and exact boundary audit

- Fixed rational coordinates: row spacing2, band heights1 and3, short shifts
  1/2 or3/2, and radius squared10.
- Proved a shielding inequality at each far-row boundary vertex, including
  edge traces outside the central vertex star and the entire circular cap.
- Reduced all vertices to one patch using translations, a half-turn, and
  possibly a reflection.
- For one exceptional layer, proved the translation group is exactly2Z×{0}
  and the full symmetry group is non-cocompact.
- Fresh exact checker passes all16 rooted local configurations, comparing
  vertices, edge pieces, oriented face pieces, and point-only boundary traces.
- Candidate proof saved in CANDIDATE.md. It resolves the named Euclidean
  cocompact subproblem only; hyperbolic metric balls are not settled.
- Completion estimate:100% candidate artifact for scoped result; no full-source
  or novelty completion claim. Separate adversarial review is pending.

## 2026-09-30 04:44 UTC: independent review

A separate adversarial reviewer returned PASS for the exact Euclidean non-cocompact claim, with no mandatory mathematical correction. The reviewer checked the original source, prior layered family, full clipped-cell geometry including singleton boundary incidences, half-turn reindexing, and full symmetry group. All 16 submitted rooted cases and 212 independently coded assertions over 64 rooted cases passed. The proof hash remains unchanged. The scoped proof/review package is complete (100%); the full original target remains unresolved because periodicity is undefined and the hyperbolic clause is untreated. No novelty claim is added.
