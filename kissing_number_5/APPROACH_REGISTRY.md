# Approach Registry

Last updated: 2026-07-23T21:51:06Z

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
  `experiments/construction_round1.md`; `experiments/random_codes/`;
  `experiments/construction_round2/`.
- **Numerical evidence:** Broad asymmetric searches and perturbations found no
  feasible 41--44 code.  The best inspected public basins have maximal inner
  products approximately \(0.51499465,0.51824116,0.52470960,0.52745771\).
  The best independently generated 41-point value is
  \(0.5155570516153127\). These values are not lower bounds.
- **Counterexamples:** Non-uniqueness and non-antipodality of 40-point codes
  invalidate symmetry-only search assumptions.
- **Restricted theorem:** Every antipodal code has at most 40 points, by an
  exact even Gegenbauer polynomial and an integrality obstruction at the
  apparent 42-point equality case.  This does not restrict a general optimum.
- **Second-round target:** 18 near-antipodal pairs plus a five-point odd-cycle
  component, motivated by the sharp minimum-edge deep-pair graph
  \(C_5\sqcup18K_2\). The constrained and released searches remained above
  \(1/2\); this numerical failure does not rule out the graph cell.
- **Third round:** 152 unrestricted Riemannian
  augmented-Lagrangian trials covered \(N=41,42,43,44\).  The best 41-point
  value remained the imported benchmark \(0.5149946525251737\); eleven
  independent Gaussian starts converged near \(0.515557052\) with a common
  155-edge active-graph profile.  All coordinates, histories, spectra, seeds,
  and hashes are stored in `experiments/construction_round3/`.  These are
  numerical basin diagnostics only.
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
  \(\pi_u\nu=\pi_v\nu=\pi_t\nu=39\alpha\).
- **Exact all-degree barrier:** Positive rational pair/triple measures on a
  seven-point inner-product grid satisfy the full closed support domain, all
  fixed-size marginals, every radial harmonic block for every \(k\geq0\), and
  every pair Gegenbauer moment.  Exact LDL checks cover \(k\leq505\);
  rational even/odd limiting matrices and perturbation bounds cover the
  infinite tail.  Thus the complete fixed-cardinality pair/triple formulation
  used here is rigorously feasible at \(N=41\).
- **Unresolved:** Add genuinely four-point/common-source or rank-five
  information.  Raising only harmonic or radial degree in this formulation
  cannot work against the certified witness.
- **Artifacts:** `proofs/fixed41_three_point_formulation.md`;
  `proofs/fixed41_bv_all_harmonics.md`; four exact JSON certificates; two
  dependency-free rational verifiers.  Patched
  discovery-only second-level Lasserre runs give objectives 90 at degree 4
  and 48 at degrees 6 and 8; these are numerical evidence only.
- **Known counterexamples:** Solver status or near-PSD matrices are not
  certificates.  The exact pseudo-distributions refute low-degree
  fixed-cardinality infeasibility claims.
- **Restrictions:** Universal if the full three-point domain and all boundary
  cases are retained.
- **Status:** certified as a barrier; four-point extensions remain active.

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
- **Tverberg consequence:** Applying affine Tverberg to
  \(\Phi(x)=(x,xx^T-I/5)\in\mathbb R^{19}\) at the exact threshold 41 forces
  three disjoint measures with identical first and second moments.  Exact
  interval-factor inequalities follow.
- **Tverberg barrier:** An exact rank-five 18-point code, split into three
  regular 5-simplices, realizes the common moments \(m=0,M=I/5\).  Hence the
  degree-two Tverberg conclusion alone is insufficient.
- **Restrictions:** None intended.
- **Status:** active.

## E. Contact and deep-pair graphs

- **Route:** Derive universal consequences of first-order optimality only after
  proving the required maximality/rigidity hypotheses, and combine local
  contact links with stress identities.
- **Proved lemmas:** Contact degrees are at most 15 and any distinct pair has
  at most seven common contact neighbors.  For the graph joining pairs with
  inner product \(<-1/2\) in a hypothetical 41-code, every independent set
  has size at most 20 (otherwise antipodalization gives 42 points), the graph
  is triangle-free, and it has at least 23 edges.
- **Unresolved:** A contact lower bound or stress certificate valid for every
  maximum 41-point code, including flexible and degenerate cases; or a
  rank/geometric contradiction from the deep-pair graph.
- **Artifacts:** `proofs/local_link_geometry.md`;
  `proofs/negative_tail_graph.md`.
- **Known counterexamples:** The exact 26-point code in the local-link note is
  inclusion-maximal with an empty contact graph.  Thus maximality does not
  imply contacts, positive contact degree, or contact rigidity.
- **Restrictions:** Potentially severe; every use must be audited.
- **Status:** active.

## F. Local cap, projection, and overlapping-link geometry

- **Route:** Condition on points, contacts, or small simplices; project to
  orthogonal complements; derive exact cap/link occupancy bounds and
  compatibility constraints between overlapping neighborhoods.
- **Proved lemmas:** The exact conditional projection lemma reduces the common
  link of a contact \(k\)-clique to
  \(A(5-k,1/(k+2))\).  This gives link bounds \(15,7,4,2,0\).  A separate
  four-dimensional LP certificate proves \(A(4,9/16)\leq32\), yielding the
  strict frame inequality \(S\succ(9/25)I\) for every hypothetical 41-code.
- **Unresolved:** A global averaging or compatibility inequality that excludes
  total size 41.
- **Artifacts:** `proofs/local_link_geometry.md`;
  `verifiers/verify_local_links.py`;
  `proofs/max_volume_semialgebraic_reduction.md`.
- **Known counterexamples:** Averaging a weak isolated cap bound is insufficient.
- **Restrictions:** Case assumptions must cover boundary contacts exactly.
- **Status:** active.

## G. Semialgebraic exhaustive proof

- **Route:** Fix orthogonal gauge safely, describe a compact coordinate/Gram
  domain, and use exact rational interval branch-and-bound, Bernstein
  enclosures, CAD, or Positivstellensatz certificates.
- **Proved lemmas:** A maximum-volume five-point basis has Gram determinant at
  least \(6488829/7318339843750\), an explicit eigenvalue lower bound, and
  coefficient vectors in \([-1,1]^5\).  Every coefficient minor is bounded
  by one.  This gives a bidirectionally exact compact rational system in 190
  variables (154 after norm equalities), with rank five automatic.  An
  \(11^5\)-cell coefficient cover is boundary-safe and has capacity one per
  cell.
- **Unresolved:** A tractable complete branching scheme and independently
  checkable tree covering the continuous domain.
- **Artifacts:** `proofs/max_volume_semialgebraic_reduction.md`;
  `certificates/max_volume_semialgebraic_reduction.json`;
  `verifiers/verify_max_volume_semialgebraic.py`.
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
- **Proved lemmas:** For \(a>3/4\), with \(b=2a^2-1\), ordered deep-pair and
  high-pair counts obey
  \[
  Q_b\geq2\sum_x\binom{d_a(x)}2\geq8D_a-20N.
  \]
  Common-center multiplicity and strict endpoint handling have been audited.
  For \(a>1/\sqrt2\), \(d_a(x)\leq5\).  A rank-deficit refinement for
  \(3/4<a<\sqrt{3/5}\) couples deep-edge and forced-positive-pair slacks.
- **Unresolved:** Retain enough incidence information to rule out the exact
  rational distance-distribution witnesses that survive the aggregate
  inequalities.
- **Artifacts:** `proofs/local_hybrid_barrier.md`;
  `certificates/local_hybrid_pseudodistribution.json`;
  `verifiers/verify_local_hybrid_barrier.py`.
- **Known counterexamples:** Uniqueness of a common deep center fails at the
  endpoint \(a=3/4\); an exact four-point \(K_{2,2}\) configuration shows that
  multiplicity two is necessary there.
- **Incidence-level separator:** A 41-vertex exact labeled object now survives
  all pair counts, all \(3\times3\) principal minors, all scalar cuts above,
  and every BV block through total degree two.  Nevertheless, for
  \(f(u)=u-\frac83u^2\), it violates
  \[
  N^{-1}\sum_i\left\|\sum_{j\ne i}f(g_{ij})
       (x_j-g_{ij}x_i)\right\|^2\ge0
  \]
  by an exact negative rational amount.  Its failure is dominated by 1,056
  explicitly counted deep--middle colored wedges.  This supplies a concrete
  four-point/common-source target, but not yet a continuous-label exclusion.
- **Artifacts:** also `proofs/degree2_bv_barrier.md`,
  `verifiers/verify_degree2_bv_barrier.py`.
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
