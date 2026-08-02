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

## 2026-08-01 18:05 PDT — weighted triangles classified for beneficial fitness

- Solved the six transient dB equations for a positive weighted triangle and
  obtained an exact homogeneous rational comparison with `K_3`.
- Factored the numerator into three nonnegative symmetric coefficients and
  supplied explicit weighted-square identities. The strict coefficient is
  positive exactly off the uniform weighting ray.
- Proved that every nonuniform positive weighted triangle is a strict dB
  suppressor for every `r>1`; uniform triangles tie exactly.
- A hostile no-import verifier independently reconstructed all transition
  equations, determinant coefficients, rational identities, boundary limits,
  near-uniform expansion, and 123 exact stress cases. The audit passed without
  mathematical correction and refined one independence label.
- Began integrating the directed closure and triangle theorem into the
  expanded Paper I manuscript.
- Best-guess completion: Paper I 80% after scope expansion; directed extension
  100%; triangle classification 100%; asymptotic-family resolution 20%;
  overall final-closure program 52%.

## 2026-08-01 18:22 PDT — symmetric K4 and asymptotic partial obstructions audited

- Classified both maximally symmetric nontrivial complete-support weighted
  `K_4` orbit families.  The `1+3` comparison factors through `(x-1)^2` and
  positive-coefficient polynomials.  The `2+2` comparison has a positive
  determinant denominator and a global `(g,d,t)` coefficient certificate;
  equality occurs only at the uniform complete graph.
- A hostile audit independently repeated the full symbolic 14-state solutions,
  checked all 123 positive denominator monomials, verified the square-root
  domain coverage and strictness, and found no theorem-level defect.  The
  unrestricted six-edge `K_4` problem remains open; 5,000 exact sampled
  instances are recorded only as an observation.
- Proved that eventual dB amplification at every fixed fitness forces support
  degree to diverge in probability.  A second theorem excludes fixed-class,
  positive-proportion dense equitable blow-ups with fixed irreducible kernel
  and unequal limiting weighted degrees by a stopped-generator branching limit
  and strict Jensen inequality.
- A hostile asymptotic audit identified and repaired the class-rounding error
  term, the branching-to-fixation lemma, and three scope overstatements.  The
  diffuse asymptotically regular, mesoscopic, vanishing-class, and reducible
  limiting-kernel regimes remain genuinely open.
- Integrated the symmetric `K_4` certificate and the necessary support-degree
  condition into Paper I.  The earlier integrated-paper hostile audit passed;
  a final post-integration audit and visual PDF review remain.
- Best-guess completion: Paper I 92%; directed extension 100%; triangle and
  symmetric-`K_4` classifications 100%; asymptotic-family resolution 45%
  (partial, with explicit open regimes); publication package 25%; overall
  final-closure program 74%.

## 2026-08-01 19:11 PDT — v1.0.0 independently replayed and published

- The final hostile audit passed the integrated directed theorem, triangle and
  symmetric-`K_4` certificates, asymptotic support proposition, quantifier
  scope, diagrams, TeX diagnostics, and visual inspection of all 13 pages.
- Detected that ordinary Tectonic builds embedded the wall-clock build time.
  Pinned `SOURCE_DATE_EPOCH` in the one-command target; two rebuilds are now
  byte-for-byte identical.  Rasterized pages also agree exactly with the
  already-audited pre-normalization PDF.
- Replayed `make paper1` from a clean Git archive.  All exact tests,
  independent full-state cross-checks, symbolic certificates, lumpability
  checks, and the manuscript build passed.  The final PDF SHA-256 is
  `1572d2fd4abd495c4eed61075afdc1dbd74a7d90fb0fe1f379bfa12c50fbf69b`.
- Rebased without conflict onto four concurrent, unrelated `main`-branch
  commits and pushed commit `cf61bfdffb1531b328fb0dcd147714782932036b`.
- Published release `universal-db-obstruction-v1.0.0` with the paper PDF,
  editable manuscript-source ZIP, full reproducibility tarball, checksum
  manifest, and clean-archive build log.  Verified the release asset digests
  and a fresh public PDF download.
- Published and checked the reader-facing GitHub Pages article and PDF.  No
  journal submission, external outreach, or external specialist review was
  performed.  No Zenodo DOI was claimed because none was yet discoverable in
  the public API immediately after release.
- One minute later, the public Zenodo API exposed the completed automatic
  deposit.  Verified version DOI `10.5281/zenodo.21753405`, concept DOI
  `10.5281/zenodo.21753404`, version
  `universal-db-obstruction-v1.0.0`, and the related identifier pointing to the
  exact GitHub tag.
- Completion: fixed-graph theorem, directed closure, triangle classification,
  symmetric-`K_4` classifications, Paper I, exact verifier, hostile audits,
  release archive, and public project page 100%.  The requested final-closure
  and publication deliverables are 100% complete.  The deliberately separate
  reversed-quantifier asymptotic program remains approximately 45% resolved,
  with surviving regimes listed explicitly rather than promoted to claims.
