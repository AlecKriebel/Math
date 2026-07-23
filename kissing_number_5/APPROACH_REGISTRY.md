# Approach Registry

Last updated: 2026-07-23T19:32:06Z

Statuses are `active`, `blocked`, `falsified`, `subsumed`, or `certified`.

## A. Exact constructions and unrestricted optimization

- **Route:** Optimize \(N=41,42,43,44\) unit vectors directly, using nonsmooth
  max-inner-product objectives, soft-max/energy continuation, manifold
  optimization, random asymmetric starts, and surgery on all four known
  40-point configurations.
- **Proved lemmas:** The exact \(D_5\) construction gives \(N=40\).  Keeping
  all 40 \(D_5\) roots fixed, every added unit vector has inner product at
  least \(\sqrt{2/5}>1/2\) with one of them.  This proves saturation only,
  not global optimality.
- **Unresolved:** Whether any \(N\geq41\) feasible code exists; whether persistent
  near misses have a common exact obstruction.
- **Artifacts:** `certificates/d5_roots.json`; `proofs/d5_saturation.md`;
  `experiments/construction_round1.md`; `experiments/random_codes/`.
- **Numerical evidence:** Broad asymmetric searches and perturbations found no
  feasible 41--44 code.  The best inspected public basins have maximal inner
  products approximately \(0.51499465,0.51824116,0.52470960,0.52745771\).
  These values are not lower bounds.
- **Counterexamples:** Non-uniqueness and non-antipodality of 40-point codes
  invalidate symmetry-only search assumptions.
- **Restrictions:** The main search must be unrestricted; structured searches
  are discovery subroutines only.
- **Status:** active.

## B. Two-point harmonic/linear programming

- **Route:** Use exact pseudo-distance distributions to delimit the two-point
  cone, then retain only strengthenings that add genuinely local, rank, or
  higher-order information.
- **Proved lemmas:** The mass-41 rational measure
  \[
  \delta_1+\frac1{41}\left(
  176\delta_{-77/100}+262\delta_{-11/25}
  +652\delta_{-9/100}+550\delta_{499/1000}\right)
  \]
  has every normalized dimension-five Gegenbauer moment strictly positive.
  Hence no finite-degree Delsarte polynomial, or absolutely convergent
  nonnegative Schoenberg series, proves a strict bound below 41.
- **Unresolved:** Determine the weakest cap, marginal-consistency, or rank
  constraint that eliminates this witness.  Pfender-generator compatibility is
  proved algebraically but awaits an independent source-normalization audit.
- **Artifacts:** `proofs/two_point_lp_barrier.md`;
  `verifiers/verify_two_point_barrier.py`;
  `tests/test_two_point_barrier.py`.
- **Known counterexamples:** The exact measure above refutes any claim that
  ordinary two-point positivity, pair-count parity, or contact-count
  upper bounds permitting zero alone separate 40 from 41.  It does not test a
  universally valid positive contact lower bound or rowwise contact
  constraint.  Its nontrivial support is strictly below \(1/2\).
- **Restrictions:** No symmetry assumption; two-point information only.
- **Status:** certified as a barrier; strengthened local variants remain active.

## C. Three-point and higher-order SDP/SOS

- **Route:** Implement the Bachoc--Vallentin three-point bound with explicit
  polynomial normalizations, then explore higher degree and k-point/Lasserre
  strengthenings.  Recover exact rational/algebraic duals from high-precision
  discovery runs and certify PSD/nonnegativity independently.
- **Proved lemmas:** Published three-point computations imply the imported upper
  bound 44.  For fixed cardinality \(N=41\), the usually omitted
  three-point marginal identity becomes linear:
  \(\sum_{u,v}x(u,v,t)=41x(t,t,1)\) as a measure identity.
- **Unresolved:** Formulate and solve the fixed-41 marginal-consistent
  three-point moment/SOS feasibility problem, then obtain an exact infeasibility
  certificate.  Exactification of every PSD and domain-nonnegativity condition
  remains mandatory.
- **Artifacts:** A low-degree second-level Lasserre trial was attempted against
  the public `LasserreSphericalCodes` code, but failed during exact
  symmetry-adapted-basis generation under the current Nemo version; the
  exception and environment are recorded in the research log.
- **Known counterexamples:** Solver status or near-PSD matrices are not
  certificates.
- **Restrictions:** Universal if the full three-point domain and all boundary
  cases are retained.
- **Status:** active.

## D. Rank-aware Gram matrices and nullspace/stress

- **Route:** Use \(G\succeq0\), `diag(G)=1`, \(G_{ij}\leq1/2\), and
  `rank(G)<=5` simultaneously through principal minors, stresses, spectral
  moments, Gale duality, low-rank completion, or sign/rank inequalities.
- **Proved lemmas:** A code exists iff such a Gram matrix exists; a hypothetical
  41-point matrix has nullity at least 36.  The entrywise quadratic kernel
  \(K=(G+J)\circ(G-\tfrac12J)\) has diagonal one, nonpositive
  off-diagonal entries, rank at most \(1+5+14=20\), and at most one negative
  eigenvalue.  Keeping the harmonic factors separate, if
  \(R=K+3J/10=(4/5)H_2+G/2\), then
  \[
  \sum_{i=1}^5\lambda_i(R)\geq N/2,\qquad
  \sum_{i=1}^{14}\lambda_i(R)\geq4N/5.
  \]
- **Unresolved:** Convert the large nullspace plus entry inequalities into a
  contradiction without assuming a contact pattern.  Identify additional
  dimension-five information not captured by the generic sign/rank statement.
- **Artifacts:** `proofs/rank_kernel_barriers.md`;
  `verifiers/verify_rank_kernel_barriers.py`;
  `tests/test_rank_kernel_barriers.py`.
- **Known counterexamples:** Dropping rank admits irrelevant correlation
  matrices and cannot establish the geometric claim.  The normalized \(D_6\)
  roots give 60 vectors and an analogous sign kernel of rank at most 27,
  refuting the tempting general assertion that every such sign kernel has
  rank at least half its order, even with at most one negative eigenvalue.
  A 49-vertex finite-field graph independently gives rank 19 and a 41-by-41
  principal example with the same signs and one negative eigenvalue; it even
  admits the same fixed-coefficient PSD-minus-\(3J/10\) decomposition.  The
  common rank-five Gram source and Hadamard-square identity are essential.
- **Restrictions:** None intended.
- **Status:** active.

## E. Contact graphs and rigidity

- **Route:** Derive universal consequences of first-order optimality only after
  proving the required maximality/rigidity hypotheses, and combine local
  contact links with stress identities.
- **Proved lemmas:** none beyond definitions.
- **Unresolved:** A contact lower bound or stress certificate valid for every
  maximum 41-point code, including flexible and degenerate cases.
- **Artifacts:** none yet.
- **Known counterexamples:** Maximum need not imply a prescribed graph;
  locally jammed does not imply globally maximum; known 40-point codes are
  nonunique.
- **Restrictions:** Potentially severe; every use must be audited.
- **Status:** active.

## F. Local cap, projection, and overlapping-link geometry

- **Route:** Condition on points, contacts, or small simplices; project to
  orthogonal complements; derive exact cap/link occupancy bounds and
  compatibility constraints between overlapping neighborhoods.
- **Proved lemmas:** elementary projection identities pending formal write-up.
- **Unresolved:** A global averaging or compatibility inequality that excludes
  total size 41.
- **Artifacts:** none yet.
- **Known counterexamples:** Averaging a weak isolated cap bound is insufficient.
- **Restrictions:** Case assumptions must cover boundary contacts exactly.
- **Status:** active.

## G. Semialgebraic exhaustive proof

- **Route:** Fix orthogonal gauge safely, describe a compact coordinate/Gram
  domain, and use exact rational interval branch-and-bound, Bernstein
  enclosures, CAD, or Positivstellensatz certificates.
- **Proved lemmas:** Compactness of \((S^4)^{41}\) ensures feasibility is attained
  when nonempty.
- **Unresolved:** A tractable complete branching scheme and independently
  checkable tree covering the continuous domain.
- **Artifacts:** none yet.
- **Known counterexamples:** Finite guessed combinatorial types or solver
  “infeasible” statuses are incomplete.
- **Restrictions:** Symmetry breaking must be proved safe.
- **Status:** active.

## H. Certified spherical-cell discretization

- **Route:** Partition \(S^4\) into cells with rigorous pairwise angle
  enclosures, map every continuous code to a graph/hypergraph object, and prove
  a clique/independence bound with boundary-safe coverage.
- **Proved lemmas:** none yet.
- **Unresolved:** Cell system fine enough to separate 40 from 41 while retaining
  a provable continuous-to-discrete implication.
- **Artifacts:** none yet.
- **Known counterexamples:** A heuristic mesh cannot rule out boundary or
  between-grid configurations.
- **Restrictions:** None if coverage is rigorous.
- **Status:** active.

## I. Classification-free universal inequalities

- **Route:** Seek moment forcing, rank-versus-sparsity, average-degree, or
  global consistency inequalities applying to every 41-point code.
- **Proved lemmas:** none yet.
- **Unresolved:** The separating inequality.
- **Artifacts:** none yet.
- **Known counterexamples:** All proposed statements must be tested against the
  four known 40-point configurations and randomized smaller codes.
- **Restrictions:** None intended.
- **Status:** active.

## J. Hybrid finite-list plus exact elimination

- **Route:** Use SDP/optimization to discover finitely many candidate local
  patterns, prove a completeness theorem with interval margins, then eliminate
  each candidate by exact algebra or a small certificate.
- **Proved lemmas:** none yet.
- **Unresolved:** A noncircular completeness mechanism.
- **Artifacts:** none yet.
- **Known counterexamples:** Enumerating guessed contact graphs is not complete.
- **Restrictions:** Depends on the eventual completeness theorem.
- **Status:** active.
