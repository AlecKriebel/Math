# Research log: weakly reversible continuum without a common factor

## 2026-08-01 15:23 PDT — Program opened

- Objective: construct and exactly verify a finite weakly reversible mass-action
  system having a positive-dimensional equilibrium continuum inside one
  positive stoichiometric class, while the coordinate vector-field polynomials
  have gcd (1).
- Discovery policy: first-principles algebra and local symbolic computation
  only. No literature, web, database, or earlier-project search before a
  complete result.
- Acceptance gate: a standalone exact verifier must reconstruct the vector
  field from the reaction list and certify positivity, graph properties,
  stoichiometry, the parametrized continuum, and the gcd assertion.
- Parallel avenues begun: direct three-species construction; structured exact
  search over reversible realizations; structural/minimality analysis and a
  higher-species fallback.
- Repository note: the supplied worktree was already on
  `codex/h668-theory`, with unrelated modified/untracked work, while `main` is
  checked out in another heavily dirty worktree. To avoid altering or losing
  independent work, this program is being isolated by path and commits will
  stage only this directory. This pre-existing branch-state conflict should be
  resolved by the human before any eventual integration to `main`.

## 2026-08-01 15:50 PDT — Full-rank construction found

- A homogeneous four-coordinate conic construction was exactly
  dehomogenized by setting the fourth coordinate to one and projecting every
  degree-three complex to its first three exponents.
- The projection produces three species with full stoichiometric rank, while
  preserving the reversible connected complex graph and the positive rational
  equilibrium curve.
- Direct reconstruction (not the dehomogenization heuristic) gave coordinate
  gcd `1`.  This resolved the main existence question with three species and
  one linkage class.
- In parallel, a first-principles obstruction was proved for the tempting
  rank-two architecture: one linkage class makes the field weighted
  homogeneous, and a curve in one affine class sweeps to a hypersurface under
  the transverse torus action, forcing a common factor.  Hence full rank is
  structurally necessary for a one-linkage three-species example.

## 2026-08-01 15:56 PDT — Exact support minimization and hostile audits

- Successive exact nullspace reductions improved the construction from 20 to
  12, then 11, and finally 10 complexes.  The final graph has 10 reversible
  pairs and 20 directed reactions.
- The final integer rates come from an exact fixed-support nullspace.  Four
  free directed-rate slots were chosen in exact ratio `(1,1,4,168)` and the
  resulting rational vector was scaled to primitive integers.  Floating-point
  feasibility is not part of the proof.
- Three independent raw-table reconstructions checked graph connectivity,
  reversibility, rate positivity, stoichiometric rank, the mass-action field,
  rational-curve substitution, multivariate gcd, ideal membership, and
  Jacobian rank.  All passed exactly.
- The steady ideal has dimension exactly one.  The prime conic
  `(z-x-y+1, 7x^2-2xy-16x+7y^2-16y+16)` is a smooth minimal component.  The
  full radical, including possible isolated components, was not determined.
- A structured search within the fixed cubic/conic architecture exhausted the
  exact support-rank filter below ten complexes.  There were no candidates at
  most seven; 198 eight-complex and 3,772 nine-complex supports survived that
  filter, but their normalized bidirectional positivity MILPs were infeasible
  at the chosen threshold.  This is scoped search evidence, not an
  impossibility theorem or a global minimality claim.

## 2026-08-01 16:00 PDT — Proof package complete

- `network.csv` records all 20 directed reactions.
- `verify_construction.py` independently reconstructs the field and verifies
  every exact algebraic and graph claim.
- `MANUSCRIPT.md` contains the theorem, reaction table, full vector field,
  parametrization, height-two certificates, gcd and dimension proofs,
  anti-degeneracy discussion, and minimality results.
- Exact verifier status: **PASS**.

## 2026-08-01 16:30 PDT — Post-solution priority audit

- Only after the exact proof package passed, a narrow primary-source audit was
  opened.  No outside source had been used during discovery.
- Boros, Craciun, and Yu (2020) explicitly posed the no-common-factor question
  answered by this construction.  Their own weakly reversible and reversible
  continua arise from a common scalar polynomial.
- Closely related primary work through 2026 was checked.  Later examples either
  retain a common factor or drop weak reversibility; recent generic-geometry
  results concern perturbation-open parameter sets and do not preclude this
  exceptional exact parameter choice.
- No prior example with the full conjunction of properties was found.  The
  priority statement is recorded conservatively in `PRIORITY_AUDIT.md`; it is
  not an exhaustive universal priority claim.

## 2026-08-01 16:36 PDT — Full radical determined

- An exact reduced lexicographic Gröbner basis factors in the form
  `(G0, D*H, D*R)`, where `D` cuts out the conic after eliminating `x`, and
  `R` is irreducible of degree 15.
- The complementary ideal has a triangular basis with one monic equation in
  `x`, one in `y`, and the degree-15 equation in `z`; it is maximal over the
  rationals.
- Exact product reductions prove that the steady ideal is the intersection of
  this maximal ideal with the conic prime.  The two primes are comaximal.
  Therefore the steady ideal itself is radical; over the algebraic closure the
  variety is the conic disjoint from 15 reduced isolated points.

## 2026-08-01 16:47 PDT — Publication checkpoint

- The complete package was committed locally as `ba89fcb6` after a final
  hostile proof audit and exact verifier run.
- The pre-existing working branch could not be pushed because its unrelated
  unpublished ancestry contains certificate blobs larger than the remote's
  object limit.  Those commits and files were not modified or discarded.
- To publish only this research program, its two dedicated commits were
  replayed onto the clean remote base and pushed as commit `42ee2ce6` on
  `codex/weakly-reversible-continuum`.
