# Research log

## 2026-08-01 15:24 PDT — program initialization

- Created a clean sibling clone on `main` because the original checkout and
  the existing `main` worktree both contain unrelated active changes.
- Fixed the discovery embargo: no catalogue, construction, formula, or prior
  computational-search lookup before an internally derived candidate theorem
  has passed independent exact verification.
- Split the first pass into three independent tracks: general weak-selection
  coefficients, general strong-selection asymptotics, and an exact small-state
  explorer for symmetric weighted families.
- Initial working objective: test endpoint compatibility before investing in
  large exact rational functions.  Any numerical computation is conjectural
  evidence only.

## 2026-08-01 15:31 PDT — strong-selection obstruction found

- Derived the exact dB strong-selection limit
  `n^{-1} sum_i s_i/(s_i+1)`, where `s_i` is support degree.  This is strictly
  below the complete limit whenever an edge is missing.
- For complete positive support and `n>=3`, derived
  `rho_dB=(n-1)/n-a_G/r+O(r^-2)` with
  `a_G=T/[n^2(n-2)]` and
  `T=sum_i sum_{j!=i}(d_i-w_ij)/w_ij`.
- Two independent agents reproduced every factor in the singleton/doubleton
  expansion.  Vertexwise Cauchy--Schwarz shows `a_G >= (n-1)/n`, with equality
  only for globally uniform weights.

## 2026-08-01 15:37 PDT — exact certificate and verifier

- Strengthened Cauchy--Schwarz to the transparent identity
  `a_G-(n-1)/n = [n^2(n-2)]^{-1} sum_i sum_{j<k}
  (w_ij-w_ik)^2/(w_ij w_ik)`.
- Implemented a full exact subset-state solver and a separate replay verifier.
  Both reconstruct Bd and dB transitions from the process definition and solve
  over `QQ(r)`.
- Exact checks recover both complete baselines, the path/star support limits,
  nonuniform complete-graph coefficients `22/27` and `343/320`, and a full
  numerator/denominator sign certificate for a weighted triangle.
- Unit tests and the independent verifier pass.

## 2026-08-01 15:42 PDT — hostile review passed

- An independent hostile audit found no coefficient, sign, equality, or
  quantifier error.
- Incorporated its requested hardening: a finite-state perturbation lemma,
  explicit `n=2` closure, pointwise-in-graph order of limits, and a single
  consistent shifted `T` convention.
- Built a five-page manuscript PDF.  Rendered and visually inspected every
  page; corrected crowded equation numbering and confirmed clean output.

## 2026-08-01 15:47 PDT — post-verification literature audit

- Lifted the discovery embargo only after independent verification and hostile
  review.
- Found that Tkadlec et al. (2020) prove transience for every noncomplete graph
  but explicitly leave weighted complete graphs as the only possible universal
  dB amplifiers and list their existence as an open direction.
- Found subsequent transient dB constructions and simultaneous amplifiers on
  the bounded interval `(1,1.2)`, neither of which closes the weighted-complete
  strong-selection case.
- The present sum-of-squares correction closes that residual case for finite
  undirected symmetric loopless graphs.  Novelty wording remains qualified
  because the audit was narrow rather than exhaustive.
