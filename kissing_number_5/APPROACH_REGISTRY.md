# Approach Registry

Last updated: 2026-07-24T01:08:00Z

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
- **Fourth round:** 36 asymmetric deletion/reinsertion, contact-stress
  basin-hopping, smoothmax-release, and epigraph-SQP runs covered
  \(N=41,42,43,44\).  Every recomputed maximum remained above \(1/2\);
  the released portfolio, seeds, coordinates, and checker are in
  `experiments/construction_round4_surgery/`.  This is numerical evidence
  only.
- **Fifth round:** 30 unrestricted inverse-chord \(p\)-energy population
  runs used aligned crossover, hyperplane splicing, tangent mutation,
  diversity retention, random immigrants, and final SQP.  The best maxima
  were approximately
  \(0.51499465,0.51824116,0.52472448,0.52747119\); no exact reconstruction
  target appeared.  The full package is in
  `experiments/construction_round5_population/`.
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
- **Rank-aware separation:** The sharp five-eigenvalue inequality
  \(20D^2\le9V^3\) rejects the stored all-degree witness exactly.  A second
  integral triple incidence passes all total-degree-two blocks and the first
  residual-vector square, but fails both this rank inequality and an explicit
  total-degree-three radial square.  Numerical reoptimization indicates that
  the three-point cone can move to \(D=0\), so the separator is not by itself
  an infeasibility certificate.
- **Higher-harmonic rank separation:** For every real harmonic combination
  \(K\) of rank at most \(r\), the sharp centered traces satisfy
  \(r(r-1)D_K^2\le(r-2)^2V_K^3\).  The \(H_2\) and
  \((H_0+5H_1)/6\) instances exactly reject the strongest degree-four
  five-node pseudo-measure.  Necessary rational outer bands, degree-five BV
  forms, and color covariance give an exact dual excluding that fixed
  support and pair multiplicity vector.
- **Convex-mixture audit:** The direct segment joining C039 to the
  degree-three/rank-feasible witness cannot satisfy both families.  A
  degree-six radial interpolation polynomial annihilates the complete C039
  support and gives a strictly negative \(H_{3,9}\) form on every positive
  mixture.  This rules out that synthesis only, not other union-support
  reoptimizations.
- **Unresolved:** Extend the nonlinear harmonic-rank hierarchy to the full
  continuous pair/triple domain, or add genuinely four-point/common-source
  information.  Raising only harmonic or radial degree in the old
  formulation cannot work against the certified witness.
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
- **Spectral moment cone:** For the five padded eigenvalues, the centered
  moments satisfy the sharp exact inequality
  \(20D^2\le9V^3\).  The centered fourth moment obeys
  \(7V^2/30\le C_4\le13V^2/20\), the moment Hankel determinant gives
  \(5VC_4\ge5D^2+V^3\), and Newton's identity eliminates the sixth moment:
  \[
  C_6=-V^3/8+3VC_4/4+D^2/3.
  \]
  The four-cycle expansion of \(\operatorname{tr}(G^4)\) has also been
  derived exactly; all terms are pair/triple moments except the all-distinct
  four-cycle statistic.
- **Harmonic rank hierarchy:** The centered-skew argument is now proved for
  every symmetric rank-\(r\) matrix and therefore for arbitrary real linear
  combinations of harmonic Gram matrices.  It detects defects in \(H_2\)
  and mixed low-harmonic kernels that C047 misses.  The separate quadratic
  frame-potential matrix inequalities are exact but insufficient: the
  all-harmonic mass-41 witness passes all eleven instances whose summed
  feature dimension is below 41.
- **Unresolved:** Bound the all-distinct four-cycle statistic jointly with its
  overlapping triples, or convert the large nullspace plus entry inequalities
  into a contradiction without assuming a contact pattern.  Pure abstract
  spectral completion is insufficient once \(D=0\).
- **Artifacts:** `proofs/rank_kernel_barriers.md`;
  `proofs/split_kernel_abstract_barrier.md`;
  `proofs/split_kernel_full_interval_barrier.md`;
  `proofs/rank_five_spectral_moment.md`;
  `proofs/rank_five_four_cycle_moments.md`;
  `verifiers/verify_rank_kernel_barriers.py`;
  `verifiers/verify_rank_five_spectral_moment.py`;
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
- **Split-spectrum barrier:** An exact 41-row construction over
  \(\mathbb Q(\sqrt2)\) has separate PSD factors of ranks 5 and 14 with the
  correct diagonals and traces, satisfies the quadratic-kernel sign condition
  and both Ky Fan bounds, but violates the genuine common-source entry range.
  The full interval provably prevents this same extension while retaining the
  old \(D_5\) factors.  Thus split spectrum alone is certified insufficient.
- **Full-interval barrier:** A stronger cyclic Fourier construction satisfies
  the entire genuine off-diagonal interval for \(R\) and \(K\), with a strict
  rationally certified buffer, while retaining all split ranks, diagonals,
  traces, signs, inertia, and Ky Fan constraints.  It fails the original
  kissing inequality on \(G=2A\) and the nonlinear identity
  \(B=G\circ G-J/5\).  These common-source conditions are indispensable.
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
- **Sparse classification:** At exactly 23 edges the graph is uniquely
  \(C_5\sqcup18K_2\).  At 24 edges it is one of
  \(C_7\sqcup17K_2\), a \(C_5\) with a pendant length-two path plus
  \(17K_2\), or \(C_5\sqcup P_4\sqcup16K_2\).  Incident antipodal
  deviations sum to at least \(\pi/3\), and every odd deep cycle has total
  deviation at least \(\pi\).
- **Unresolved:** A contact lower bound or stress certificate valid for every
  maximum 41-point code, including flexible and degenerate cases; or a
  rank/geometric contradiction from the deep-pair graph.
- **Artifacts:** `proofs/local_link_geometry.md`;
  `proofs/negative_tail_graph.md`;
  `proofs/sparse_deep_graph_stability.md`.
- **Known counterexamples:** The exact 26-point code in the local-link note is
  inclusion-maximal with an empty contact graph.  Thus maximality does not
  imply contacts, positive contact degree, or contact rigidity.  Separately,
  an exact rank-20 code with deep graph \(C_5\sqcup18K_2\) passes the
  aggregate degree-four projective kernel and every subset inequality, so
  sparse graph/local component information needs rank-five cross-component
  input.
- **Exact-antipodal obstruction:** With 16--18 collapsed base lines, zero
  base/base and base/core projective penalty would generate a simply-laced
  rank-five root system with at least 32 roots, hence \(D_5\).  The remaining
  root lines accommodate one fewer oriented core point than required.
  Therefore the cross loss is strictly negative.  For 18 base lines,
  \(D_5\) minus any two root lines is also proved projectively saturated.
  Determinant rounding makes the gap explicit as
  \(1/1658880000\) and gives a robust near-antipodal inequality, but this
  certified constant is far too small for the full argument.
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
  A stronger exact degree-11 certificate proves
  \(A(4,7123/12877)\le30\), and a closed-slab projection improves this to
  \[
  S\succ(15059/40000)I.
  \]
- **Earlier one-sided strengthening:** An exact degree-11
  \(\mathbb Q(\sqrt3)\) polynomial proves
  \(A(4,1/\sqrt3)\le33\).  Equatorial projection and boundary-safe cap
  reflection, together with the rigorous baseline \(\tau(5)\le44\), give
  \(B(5)\le38\).  Thus every open origin hemisphere of a hypothetical
  41-code contains at least three points; deletion of any two points leaves
  the origin in the convex-hull interior.  Directionally,
  \(\max(0,8-r(u))\le b(u)\le r(u)+3\), and at a code vertex
  \(d(x)+r(x)\ge7,\ d(x)\le r(x)+2\).
- **Direct cap SDP and tangent projection:** Exact rational degree-10 Gram
  factors and a complete 2,483-leaf Bernstein tree on the full closed
  cap-pair domain prove \(B(5)\le35\).  Hence a hypothetical 41-code has at
  least six points in every open hemisphere and remains origin-spanning
  after deletion of any five points.  Independently, the nonnegative
  neighborhood at every code point projects injectively to an
  \(A(4,1/\sqrt3)\)-code, proving at least seven strictly negative
  neighbors per vertex.
- **Unresolved:** A global averaging or compatibility inequality that excludes
  total size 41.  A degree-11 cap candidate has audited numerical objective
  below 35, but exact rationalization has already exposed a missed narrow
  interior ridge in the first attempt; no \(B(5)\le34\) certificate is
  claimed.
- **Artifacts:** `proofs/local_link_geometry.md`;
  `verifiers/verify_local_links.py`; `proofs/one_sided_tukey_bound.md`;
  `verifiers/verify_one_sided_tukey.py`;
  `proofs/one_sided_cap_degree10_bound.md`;
  `verifiers/verify_one_sided_cap_degree10.py`;
  `proofs/tangent_nonnegative_neighborhood.md`;
  `verifiers/verify_tangent_nonnegative_neighborhood.py`;
  `proofs/improved_frame_cap_bound.md`;
  `verifiers/verify_improved_frame_cap_bound.py`;
  `proofs/max_volume_semialgebraic_reduction.md`.
- **Known counterexamples:** Averaging a weak isolated cap bound is insufficient.
- **Restrictions:** Case assumptions must cover boundary contacts exactly.
- **Audit:** The one-sided polynomial, projection square, reflection
  self-pair, open/closed conventions, integer optimization, and all convex
  consequences were independently recomputed with no mathematical objection.
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
- **Stronger barrier:** A second exact integral triple pseudo-incidence
  retains the same pair data, all triangle determinants, all BV blocks
  through total degree two, Pfender/deep-wedge patterns, and the displayed
  residual square.  It fails a specific degree-three radial square and the
  sharp rank-five spectral inequality.  This pinpoints the next target as
  simultaneous degree-three, realizability, and rank consistency.
- **Degree-three barrier:** A third exact integral pseudo-incidence passes
  every fixed-\(N\) BV block through total degree three and all certified
  wedge event cells, including the tight mixed capacities.  Its first pure
  BV failure is an explicit total-degree-four direction, and the independent
  rank-five spectral cut also rejects it.
- **Degree-three plus rank barrier:** A fourth assignment passes total
  degree three, all wedge cells, and the sharp rank-five spectral inequality
  with strict slack.  It fails an exact common-graph color-degree covariance
  square by \(-570/41\).  This supplies a new inexpensive realizability block
  for the next search and proves that the rank and graph-incidence cuts are
  independent on the stored assignments.
- **Degree-three/rank/color barrier:** A fifth assignment repairs the full
  color-degree covariance matrix, has explicit Erdős--Gallai graphical
  sequences for every color, and nonnegative induced same-color
  three-vertex motif counts.  It passes degree three, all wedge cells, and
  C047, but fails the scalar degree-four block \(H_{4,4}\).  No simultaneous
  five-color graph is claimed.
- **Degree-four/rank/color/clique barrier:** A sixth integral assignment
  passes every BV block through total degree four, C047, all five
  color-degree covariances, the support-specific rank clique cut, a joint
  degree-vector decomposition, all color-union Erdős--Gallai tests, and the
  minimum-negative-degree requirements.  It fails total degree five and the
  new \(H_2\) and mixed-harmonic centered-skew constraints.
- **Fixed-support closure:** With necessary outer C047 and harmonic-rank
  bands, an exact degree-five dual proves that no triple distribution exists
  on this historical five-node support with the fixed pair multiplicities.
  This is a fixed-support theorem only; no discretization theorem reduces an
  arbitrary code to it.
- **Artifacts:** also `proofs/degree2_bv_barrier.md`,
  `verifiers/verify_degree2_bv_barrier.py`;
  `proofs/weighted_residual_barrier.md`,
  `verifiers/verify_weighted_residual_barrier.py`;
  `proofs/local_hybrid_degree3_barrier.md`,
  `verifiers/verify_local_hybrid_degree3.py`;
  `proofs/local_hybrid_degree3_rank_barrier.md`,
  `verifiers/verify_local_hybrid_degree3_rank.py`;
  `proofs/local_hybrid_degree3_rank_color_barrier.md`,
  `verifiers/verify_local_hybrid_degree3_rank_color.py`;
  `proofs/harmonic_combination_centered_skew.md`,
  `verifiers/verify_harmonic_combination_centered_skew.py`;
  `proofs/local5_degree5_necessary_rank_separator.md`,
  `verifiers/verify_local5_degree5_necessary_rank_separator.py`.
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
