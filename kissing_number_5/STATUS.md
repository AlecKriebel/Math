# Status — paused research checkpoint

Last updated: 2026-07-24T16:33:20Z

> **Program state: PAUSED. This is not a resolution of the
> five-dimensional kissing-number problem.**

## Rigorous global status

\[
\boxed{40\leq\tau(5)\leq44}.
\]

- The lower bound \(40\) is exact.  The normalized \(D_5\) roots are written
  out in [`certificates/d5_roots.json`](certificates/d5_roots.json), proved in
  [`proofs/lower_bound_d5.md`](proofs/lower_bound_d5.md), and checked with
  exact integer arithmetic by
  [`verifiers/verify_d5.py`](verifiers/verify_d5.py).
- The upper bound \(44\) is the published baseline from the
  Bachoc--Vallentin/Mittelmann--Vallentin semidefinite-programming method.  It
  is imported here; this repository does not contain a standalone exact
  certificate for it.
- The July 2026 literature check still reports \(44\) as the best proved upper
  bound and at least four non-isometric 40-point configurations:
  [Cohn--Rajagopal, *Variations on Five-Dimensional Sphere
  Packings*](https://doi.org/10.1007/s00454-026-00841-x).

**This program did not improve either global bound, construct 41 points, or
prove that 41 points are impossible.**  No percentage-to-completion estimate
is defensible.  The earlier “22%” estimate measured accumulated infrastructure,
not mathematical proximity to a solution, and is retired.

## What survived exact audit

The following are useful necessary conditions or restricted theorems.  None
alone, or in the combinations checked so far, excludes every continuous
rank-five \(41\times41\) Gram matrix.

### Universal statements

- Every antipodal five-dimensional kissing code has at most 40 points.
- For a hypothetical 41-code, the graph of pairs with inner product below
  \(-1/2\) is triangle-free, has independence number at most 20, and has at
  least 23 edges.
- If such a code has \(r\) antipodal pairs, those pairs are isolated components
  of the strict-deep graph and
  \[
  e(H)\le r+(20-r)^2+1.
  \]
  At \(r=18\), equality forces \(H=18K_2\sqcup C_5\).  The five residual cycle
  products obey an exact projective-harmonic energy lower bound, forcing one
  product at most
  \[
  -\sqrt{\frac{1+\sqrt{17}}8}.
  \]
  This localizes but does not eliminate the branch.
- Exact tangent-projection certificates give the positive-height occupancy
  ladder
  \[
  \#\{y\ne x:\langle x,y\rangle\ge h\}\le
  \begin{cases}
  23,&h=1/4,\\
  22,&h=3/10,\\
  21,&h=1/3,\\
  20,&h=3/8,\\
  19,&h=2/5.
  \end{cases}
  \]
- Exact cap certificates in this repository independently prove
  \(B(5)\le34\) and several robust variants.  This is weaker than the published
  \(B(5)\le33\) value in Bachoc--Vallentin's spherical-cap table, so no record
  is claimed.
- The exact rank-five spectral, harmonic-combination, Lorentzian, weighted
  isotropy, and common-source identities recorded in the claims ledger are
  valid necessary conditions.  Exact countermodels show that their aggregate
  low-order shadows do not yet recover one global rank-five Gram source.

### Restricted and finite-model statements

- In the **quarter-grid model only**, where all inner products are multiples
  of \(1/4\), exact certificates exclude the branches with 14, 15, or 16
  antipodal pairs.
- An exact ADE core-shell calculation excludes one specific \(r=12\) endpoint
  with edge-count vector
  \((12,35,199,40,279,0,255)\).
- The same machinery excludes all 38 profiles stored in
  [`r11_quarter_grid_global_profiles.json`](experiments/centered_quarter_k4_flag_psd/audit/k5_centering_products/rank5_strengthening/r11_quarter_grid_global_profiles.json).
  The upstream generators proving that these lists exhaust their whole
  \(r=11\) and \(r=12\) branches were temporary and did not survive.  Therefore
  **the complete \(r=11\) and \(r=12\) branches are not repository-certified**.
- Earlier exploratory claims concerning complete \(r=13\), \(r=17\), or
  \(r=18\) quarter-grid exclusions have no surviving exact package and are not
  claimed here.  The interrupted \(r=10\) exploration likewise produced no
  theorem-strength artifact.
- On the closed five-cycle sign cell, an exact proof gives
  \(\lambda_{\max}(G)\le3\).  A separate exact Bernstein certificate proves
  the target quartic-energy upper bound only on the minimal angular-metric
  face \(\sum A_i=3\).  The off-face region remains open, so this does not
  eliminate the \(r=18\) branch.
- A degree-three root-triangle dual is exact on one finite 1,782-atom \(K_7\)
  catalog.  An exact rank-five quarter-grid counteratom outside the catalog
  violates it, refuting any universal interpretation of that finite dual.
- The realized-\(D_5\) extension audit proves a small-union Hall lemma and
  supplies exact counterexamples to two tempting stronger charging
  principles.  It is a study of one support, not a classification of arbitrary
  41-codes.

## Construction search at pause

No exact configuration with 41--44 points was found.  The best repeatedly
reproduced numerical maxima were approximately:

| Points | Best maximum inner product | Required |
|---:|---:|---:|
| 41 | 0.5149946525 | \(\le0.5\) |
| 42 | 0.51824116 | \(\le0.5\) |
| 43 | 0.52470960 | \(\le0.5\) |
| 44 | 0.52745771 | \(\le0.5\) |

These are basin-search outcomes, not lower bounds on the optimum and not
evidence of nonexistence in the logical sense.  The dedicated \(r=18\)
five-cycle search reached a best common load near \(0.54248\).

## Strongest route if resumed

The best remaining direction is a **global common-source/rank-five
compatibility inequality** that couples several overlapping local views.
Pair distributions, three-point SDP blocks, finite local rank-five mixtures,
integer row moments, and many cap rows all admit exact mass-41
pseudodistributions.  What repeatedly separates those shadows from geometry
is that their local vectors need not live in one common five-dimensional
column space.

A useful restart should bring one genuinely new mechanism:

1. an exact positive square or stress identity involving overlapping
   four-cycles/rooted triangles and retaining a common Gram source;
2. a boundary-safe continuous-to-finite theorem, not merely a finer grid; or
3. a rigorously certified higher-order SDP/SOS dual with objective strictly
   below 41.

More optimization of the same pair/triple or quarter-grid relaxations is
unlikely to be a good use of a fixed research budget.

## Theorem-strength unresolved gaps

1. No construction of 41, 42, 43, or 44 points is known here.
2. No universal inequality excludes every real PSD unit-diagonal
   \(41\times41\) matrix with off-diagonal entries at most \(1/2\) and rank at
   most five.
3. No theorem maps an arbitrary continuous code to the quarter grid or any
   other finite alphabet while preserving feasibility.
4. No complete continuous classification of the \(r=18\) five-cycle branch is
   available.
5. No exact exhaustive generator currently authenticates the stored \(r=11\)
   profile list or the upstream \(r=12\) endpoint list.
6. The root-triangle degree-three radical and the off-face five-cycle energy
   argument are incomplete.

## Claims that survived adversarial audit

- The exact \(D_5\) lower construction and its boundary pairs.
- Antipodal optimality, the deep-graph structure, and the \(r=18\) residual
  projective-energy lower bound.
- The local positive-height ladder and the scoped cap certificates.
- Rank-five spectral and common-source identities with their stated
  hypotheses.
- Quarter-grid \(r=14,15,16\) exclusions.
- The specifically scoped ADE, five-cycle-face, finite-catalog, and realized
  \(D_5\)-extension results described above.

## Principal failed or overbroad claims

- Ordinary two-point linear programming, the implemented three-point
  relaxation, and the current finite local mixtures do not separate 40 from
  41; exact pseudodistributions witness the barriers.
- “Local rank five through \(K_6\), \(K_7\), or even \(K_{11}\) implies one
  global rank-five code” is false at the symmetrized marginal level.
- Fixed-support or finite-catalog infeasibility does not imply a continuous
  upper bound.
- The full five-cycle quartic-energy lemma is not proved.
- The stored \(r=11/r=12\) profile exclusions are not complete branch
  exclusions without their missing enumeration generators.
- Floating solver infeasibility, near-PSD matrices, and failure to find a
  construction prove no upper bound.

The full record, including more than 160 individually scoped claims and their
counterexamples, remains in [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md).  Mechanism
history is in [`APPROACH_REGISTRY.md`](APPROACH_REGISTRY.md).

## Reproducibility and resumption

- [`RESUME.md`](RESUME.md) is the operational handoff, with five-minute smoke
  tests, exact package commands, missing-artifact warnings, and restart
  priorities.
- [`PAUSE_MANIFEST.sha256`](PAUSE_MANIFEST.sha256) hashes the final tracked
  research tree.
- [`MANIFEST.md`](MANIFEST.md) explains how to verify that checksum manifest.
- Search code is under `experiments/`; proof-facing checkers are under
  `verifiers/`; claims and proof notes are separate from numerical discovery
  output.

The workstream was paused on 24 July 2026 because the global bounds had not
moved and marginal returns had narrowed to increasingly restrictive finite
models.  The repository is intended to make a later restart possible without
mistaking those restricted results for a solution.
