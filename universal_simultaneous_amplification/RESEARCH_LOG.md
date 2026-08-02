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

## 2026-08-01 17:33 PDT — final-closure continuation initialized

- Continued from the inherited theorem without restarting discovery.
- Split the new work into exact directed complete-support, exact weighted
  triangle, and asymptotic-family tracks, with separate output directories.
- Began Phase 0 hardening: an explicit differentiated first-step proof now
  establishes `q'_S(0)=0` for every state with at least three mutants, and the
  vertexwise singleton expansion is displayed before averaging.
- Corrected the family conclusion to distinguish `exists N0, forall N,
  forall r` from `forall r, exists N0(r), forall N`.
- Clarified that finite exact computations audit the implementation while
  symbolic identities prove the universal theorem.
- Best-guess completion: Paper I hardening 65%; directed extension 10%;
  triangle classification 10%; asymptotic-family resolution 5%; overall
  final-closure program 20%.

## 2026-08-01 17:40 PDT — Phase 0 proof hardening verified

- Rebuilt the exact differentiated first-step proof, including analyticity,
  the proper-state size induction, the `n<=3` boundary case, pair forcing, and
  the requested singleton expansion before averaging.
- Added a claims ledger and a reproducible `make paper1` target. A fresh local
  environment running SymPy 1.14 passed all six unit tests, the independent
  exact verifier, and the complete manuscript build.
- Rendered all seven pages of the repaired PDF and inspected them visually;
  no clipping, overlap, broken glyph, or equation-placement defect remains.
- Best-guess completion: Paper I hardening 95%; directed extension 15%;
  triangle classification 15%; asymptotic-family resolution 5%; overall
  final-closure program 25%.

## 2026-08-01 17:48 PDT — directed complete-support theorem proved

- Two independent derivations obtained the directed coefficient
  `A_dir/[n^2(n-2)]`, with excess over the complete baseline equal to the
  incoming-column sum of squares `E_dir/[n^2(n-2)]`.
- Equality is exactly column-uniform weighting `w_uv=c_v`; independent
  incoming-column scaling proves exact dB equivalence to `K_n` for all
  fitness values. A row-oriented alternative was falsified exactly.
- The separate full-state verifier passed genuinely asymmetric `n=3,4`
  examples, independent column rescaling, and a column-uniform negative
  control. Script and recorded-output SHA-256 hashes agree with the audit.
- After verification, a narrow primary-source audit confirmed that the prior
  noncomplete theorem matches the source-target convention, loopless directed
  weights, uniform initialization, and strongly connected support.
- Added a first-principles source-component argument for non-strong supports,
  completing the fixed-graph directed model under positive incoming degrees.
- Best-guess completion: Paper I hardening 95%; directed extension 90%;
  triangle classification 25%; asymptotic-family resolution 10%; overall
  final-closure program 38%.
