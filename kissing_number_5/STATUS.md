# Status

Last updated: 2026-07-24T03:34:00Z

## Rigorous bounds

\[
\boxed{40\leq\tau(5)\leq44}.
\]

- Lower bound 40: **independently exact-verified** from the \(D_5\) root
  configuration.  See
  [`proofs/lower_bound_d5.md`](proofs/lower_bound_d5.md) and run
  `python3 verifiers/verify_d5.py certificates/d5_roots.json`.
- Upper bound 44: **imported published baseline**, due to the
  Bachoc--Vallentin three-point SDP as computed at high precision by
  Mittelmann--Vallentin.  This project has not yet reconstructed a standalone
  exact certificate for that bound.

No exact value has been established.

## Completion estimate

**Best guess: 21% toward a complete exact resolution.**  The lower
construction and several new universal necessary conditions are exact and
audited, including an exact one-sided bound \(B(5)\le34\) and a quantitative
enlargement of that cap theorem, but the decisive step—either a 41-point
exact construction or a
classification-free exclusion of every continuous 41-point Gram
realization—is still absent.  The estimate is intentionally uncertain and
may decrease if the surviving continuous-support barriers prove broader
than currently known.

## Strongest candidate routes

The strongest current candidate is a **rank-aware higher-harmonic
local-to-global route** coupling very negative pairs, forced positive wedges,
colored-degree consistency, and the finite ranks of several harmonic Gram
matrices.  For every real harmonic combination \(K\) of rank at most \(r\),
the newly proved sharp inequality
\[
r(r-1)D_K^2\le (r-2)^2V_K^3
\]
adds rank information visible in pair/triple moments.  Its \(H_2\) and
\((H_0+5H_1)/6\) instances exactly reject the strongest degree-four
pseudo-distribution.  Together with degree-five BV blocks and necessary
outer rank bands, these cuts now give an exact rational dual excluding the
entire historical five-node support with its fixed pair multiplicities.
This is a genuine fixed-support theorem, not a universal 41-point exclusion.
The missing global ingredient must either control continuously varying
supports or retain four-cycle/comparable common-source information.
The sparse cases are sharply localized: with 23 deep pairs the graph is
exactly \(C_5\sqcup18K_2\), while with 24 it is one of three explicit
component types.  A rank-20 countermodel passes all aggregate
projective-kernel and local angular inequalities for the 23-edge graph, so
the needed continuation must use rank five across distinct components.

Other active incompatible routes are:

1. rank-aware Gram/nullspace inequalities, including a degree-two sign kernel
   of rank at most 20 and an exact degree-two Tverberg partition at \(N=41\);
2. compatible local-cap/link and deep-pair graph bounds;
3. unrestricted numerical construction searches for 41--44 points, followed
   by exact reconstruction if a genuine candidate appears;
4. a maximum-volume-basis semialgebraic reduction with explicit rational
   conditioning and a boundary-safe finite cell cover.

An exact degree-11 cap-SDP certificate now gives
\[
A(4,1/\sqrt3)\le33,\qquad B(5)\le34.
\]
Consequently, every open hemisphere of a hypothetical 41-code contains at
least seven points, and the origin remains in the interior of the convex hull
after deletion of any six points.  Independently, tangent projection of
the nonnegative neighborhood at each code point proves that every vertex
has at least seven strictly negative neighbors, so the negative-pair graph
has minimum degree at least seven and at least 144 edges; the two oriented
hemisphere bounds also force at least six other strictly positive neighbors
at every vertex.  The new proof
uses exact rational Gram factors, diagonal bound \(1647/50\),
off-diagonal bound \(-969/1000\), and a 5,995-leaf Bernstein certificate
over the full closed semialgebraic domain.  Its objective is
\(11303/323=35-2/323\), so integrality gives 34.  A separate verifier
independently rebuilt every polynomial term and tree leaf, checked the
previously missed symmetry ridge and all pole/contact/determinant
boundaries, and found no flaw.  The earlier degree-10 proof of
\(B(5)\le35\) remains as a smaller independent certificate.

The same degree-11 positive kernel has now been exact-certified on the
strictly larger closed cap
\[
\langle e,x\rangle\ge-1/300.
\]
On that domain the exact diagonal and off-diagonal bounds are \(3291/100\)
and \(-121/125\), giving
\[
|C|\le\frac{16939}{484}=35-\frac1{484}<35.
\]
The rebuilt 650-term polynomial and 6,053-leaf Bernstein tree therefore
prove that every hypothetical 41-code has at least seven points with
\(\langle e,x\rangle<-1/300\) and at least seven with
\(\langle e,x\rangle>1/300\), for every unit direction \(e\).  At a code
vertex this gives at least seven other points below \(-1/300\) and at least
six other points above \(1/300\).  All thresholds are strict consequences
of an audit on a closed domain.

Deletion-six robustness also forces two disjoint inclusion-minimal positive
circuits, each with between two and six points, and therefore two disjointly
supported positive Gram-kernel vectors.  This is exact but not decisive:
the \(D_5\) code realizes every one of the 15 possible circuit-size pairs,
and an exact 41-point subset of \(D_6\) satisfies the same entry and circuit
conditions at rank six.  A continuation must exploit genuinely global
rank-five compatibility rather than circuit sizes alone.

The Lorentzian transform
\[
A=2G-J,\qquad W=I-A
\]
now gives another exact structural view.  Any hypothetical 41-code has
\(\operatorname{inertia}(A)=(5,1,35)\), \(W\) irreducible and nonnegative,
and Perron root \(18<\rho(W)\le42\).  A nonsingular six-vertex principal
core represents the other 35 rows on one signature-\((5,1)\) quadric.
Most importantly, if a normalized positive circuit satisfies
\(A\alpha=-c{\bf1}\), then \(A+cJ\succeq0\) has rank five and \(c\) is the
unique critical rank-one shift.  Thus the genuine identity \(c=1\) is
already equivalent to recovering the omitted PSD rank-five Gram lift.
An exact rational 41-point surrogate satisfies the separate inertia,
interval, graph, depth, and two-circuit conditions but has \(c=21/19\);
its pseudo-Gram matrix is explicitly indefinite.  This sharply identifies,
rather than removes, the common-source bottleneck.

An independent exact \(S^3\) cap polynomial improves the frame conditioning
of every hypothetical 41-code to
\[
\sum_{x\in C}xx^{\mathsf T}\succ \frac{15059}{40000}I_5.
\]
For its five nonzero Gram eigenvalues, if
\(V=\sum_i(\lambda_i-41/5)^2\) and
\(D=\sum_i(\lambda_i-41/5)^3\), the sharp rank-five constraint
\[
20D^2\le9V^3
\]
is proved exactly.  It rejects both stored high-quality pair/triple
pseudo-witnesses, demonstrating genuine information absent from all
three-point harmonic blocks.  A separate feasible spectral completion with
\(D=0\), and now an exact degree-three BV/wedge pseudo-measure satisfying the
sharp inequality with strict slack, show that spectral moments alone cannot
finish the proof.  The latter pseudo-measure fails a simpler common
edge-colored-graph covariance square, so the two constraints carry
independent information.  Convexly mixing that witness with the all-degree
three-point witness cannot repair both defects: an exact radial interpolation
polynomial annihilates the old support and exposes a negative
\(H_{3,9}\) direction for every positive mixture weight.

The best stored unrestricted 41-point numerical candidate has maximum inner
product approximately \(0.514994652512\); a repeatedly reached fully
independent basin is \(0.5155570516153127\).  Both exceed \(1/2\) and are
numerical near misses, not lower or upper bounds.

A seventh construction round compressed 20 feasible six-dimensional starts
toward rank five.  Every path crossed above \(1/2\) at the same coarse
homotopy stage, and the best final 41-point maximum was
\(0.5207137808832133\), worse than the stored unrestricted record.  Exact
\(D_6\)-label checking and binary64 trajectory verification make this
reproducible numerical evidence about one mechanism only.

An eighth construction round tested unit-norm tight frames.  Exact directed
interval arithmetic rejects every canonical cyclic 41-vector harmonic frame
and every row-sign switching of one: a forced sign reversal around a
41-cycle has odd parity.  A separate determinant argument shows that no five
oriented \(D_5\) roots form an orthonormal basis.  The best general numerical
UNTF search ended at \(0.5262002628454\), still infeasible.  These are
restricted construction results, not a universal upper bound.

A ninth unrestricted construction round attacked the persistent
35-point-core/six-rattler basin by complete floating one-point facet scans,
deletion/reinsertion of 2--8 points, all-coordinate release, large core
quakes, and replica exchange.  It found no 41--44 point code.  The best
recomputed maxima were
\[
0.5149946525121668,\ 0.5182411558622623,\
0.5247244770145227,\ 0.5274711925359574.
\]
The extracted 35-core active graph has 153 edges and minimum vertex cover
26, explaining exactly why replacing only 2--8 locked core vertices cannot
remove every old maximum edge.  This is an exact fact about one
well-separated finite graph extracted from floating data, not a geometric
upper bound.

The proposed anchored row-energy BV route is now exactly blocked in its pure
three-point form.  The all-harmonic pseudo-measure forces its objective to be
\(7.209745740250104\ldots>36/5\).  Degree-6, 8, and 10 numerical
antipodal-belt searches also remain far from their required objective below
39.  Any useful continuation of either route must add genuinely new rank or
four-point consistency.

Ordinary two-point LP is now **certifiably blocked**: an exact mass-41
pseudo-distance distribution satisfies every Gegenbauer moment inequality and
has no off-diagonal atom at the contact value.

The entire fixed-cardinality two/three-point route, in the formulation
recorded here, is now **certifiably blocked**: one exact rational
pseudo-distribution satisfies every radial block in every harmonic degree and
every pair Gegenbauer inequality.  The proof uses exact finite checks through
harmonic degree 505 and rational parity-tail estimates thereafter.  It does
not extend to four-point consistency or to a rank-five Gram matrix.

One useful four-point/common-source separator is the residual-vector square.
For
\[
 f(u)=u-\frac83u^2,\qquad
 r_{ij}=x_j-\langle x_i,x_j\rangle x_i,
\]
every genuine code satisfies
\[
 \frac1N\sum_i\left\|\sum_{j\ne i}f(g_{ij})r_{ij}\right\|^2\ge0.
\]
The first labeled 41-vertex pseudo-Gram object surviving all
\(3\times3\) minors and all degree-two BV blocks violates this inequality by
the exact amount
\(-105027064094021/15375000000000\).  Converting this separator into a
universal continuous-label bound remains an important gap.  A second exact
integral triple pseudo-incidence survives this residual square and all
degree-two BV blocks, but fails an explicit degree-three radial square and
the sharp rank-five spectral inequality.  A third exact integral
pseudo-incidence passes every BV block through total degree three and every
certified wedge capacity on the same support; within the BV hierarchy it
first fails a displayed degree-four block, while the independent sharp
rank-five spectral cut already rejects it.  A fourth assignment passes the
degree-three and rank-five tests simultaneously but fails the exact
color-degree covariance square
\(\sum_v(2d_0(v)-d_1(v)+d_4(v))^2\ge
(\sum_v(2d_0(v)-d_1(v)+d_4(v)))^2/41\).
A fifth exact assignment repairs that covariance defect as well, passes
individual-color graphical degree sequences and all induced three-vertex
motif counts, and still satisfies the rank-five \(H_1\) cut.  A sixth exact
assignment passes every BV block through total degree four, the old
rank/color/clique conditions, a joint colored-degree decomposition, and all
negative-degree requirements.  Both are rejected by the new
higher-harmonic centered-skew constraints.  An exact degree-five dual then
rules out every triple distribution on this fixed support and pair data
using only necessary outer rank bands.  Thus these constraints are genuinely
independent, while continuous-support universality remains unresolved.

A new four-point/common-source audit gives a much shorter rejection of the
sixth assignment.  If a base pair has inner product at most \(-11/25\),
it has at most one common neighbor whose two incident inner products are at
least \(499/1000\).  Exact projection gives the forbidden lower bound
\(109001/140000>1/2\) for two such neighbors.  The stored witness requires
243 such triangles but has only 219 eligible base edges.  An independent
enumeration of all 198 Gram-PSD colored-\(K_4\) orbits reduces to the same
one-row covariance contradiction.  This is a universal threshold lemma but
still only rejects the fixed-support witness.

Adversarial audit found that the subsequently proposed five-node
common-pair “survivor” was not a survivor at all: cumulative base thresholds
had incorrectly allowed unused deeper edges to subsidize shallower ones.
The valid pointwise theorem can be summed over any measurable base stratum.
Exact singleton strata give \(n_{244}=219>131=E_2\) and
\(n_{344}=1424>1304=4E_3\); the seven-node all-harmonic witness also fails
its exact \(q=-1/4,b=1/2\) stratum.  Combining two such rows with only three
total-degree-three BV scalar forms yields a short exact Farkas certificate
excluding every nonnegative triangle measure on the historical five-node
support and pair data.  The original cumulative-only artifact is retained
but explicitly marked **REFUTED**.

This correction still does not globalize.  A fresh atomic search reoptimized
the triangle measure on both a seven-node quarter grid and a thirteen-node
refinement.  The quarter-grid numerical witness simultaneously passes all
corrected stratum/weighted capacities, full-radial BV through harmonic
degree 16, ordinary pair moments, frame PSD constraints, and 27 sampled
sharp harmonic-rank inequalities; its independently recomputed active BV
margin is about \(2.02\cdot10^{-6}\).  The thirteen-node refinement also
passes numerically, but only at a \(4.96\cdot10^{-11}\) BV margin.  These are
finite-grid, finite-degree pseudodistributions—not codes or exact
certificates—and they show why a continuous-domain dual or a new four-point
mechanism is still required.

## Theorem-strength unresolved gaps

- No universal inequality excludes a 41-point code.
- No exact three-point or higher-point dual certificate below 41 is known here.
- The all-degree fixed-cardinality three-point pseudo-distribution proves that
  no contradiction can follow from only the complete pair/triple measure
  conditions formalized in this repository; four-point consistency, rank, or
  another genuinely stronger invariant is necessary.
- No complete interval, semialgebraic, or finite-cell exhaustion of all
  41-point codes is known here.
- No construction with 41 or more points is known here.
- No theorem justifies restricting a hypothetical extremizer to a contact
  graph, finite inner-product alphabet, symmetry class, rigidity class, or
  lattice.
- The compact maximum-volume formulation still has 154 intrinsic continuous
  dimensions; no complete interval tree or SOS infeasibility certificate has
  been produced.
- The fixed five-node support is now eliminated, but no theorem reduces an
  arbitrary real inner-product distribution to that support or pair data.
- Exact-stratum common-pair cuts are universal, but no continuous-support
  combination of them currently excludes all possible 41-point pair/triple
  measures; corrected finite-grid relaxations remain numerically feasible.
- The residual-vector square above separates the best labeled pseudo-object,
  but no classification-free bound yet forces enough high closures among its
  deep--middle wedges for arbitrary real inner products.
- The sharp rank-five inequality eliminates the stored witnesses but can be
  evaded by other three-point-feasible moment data; a successful rank route
  must impose the new harmonic-combination hierarchy on a continuous
  pair/triple domain and likely control the all-distinct four-cycle term in
  \(\operatorname{tr}(G^4)\), or an equivalent common-source statistic.
- The deep-graph cases with 23 and 24 edges are finite, but no
  rank-five/cross-component elimination of their continuously labeled Gram
  realizations is known.
- The six-core Lorentzian star-complement representation is exact, but the
  normalized positive-circuit identity needed to recover the PSD rank-five
  lift is already equivalent to the original common-source condition.  No
  weaker tractable shadow yet excludes all continuous star-complement
  realizations.
- In the exact-antipodal reduction for the sparse graphs, a zero-slack
  root-system argument forces the base lines into \(D_5\) and proves a strict
  cross-component projective-energy loss.  An effective determinant-rounding
  proof gives the explicit gap \(1/1658880000\) and a robust
  near-antipodal inequality, but this certified constant is far too small for
  the remaining global margin.

## Reproducible artifacts

- Exact \(D_5\) coordinates:
  [`certificates/d5_roots.json`](certificates/d5_roots.json)
- Independent verifier:
  [`verifiers/verify_d5.py`](verifiers/verify_d5.py)
- Verifier tests:
  [`tests/test_verify_d5.py`](tests/test_verify_d5.py)
- Exact ordinary-LP barrier proof:
  [`proofs/two_point_lp_barrier.md`](proofs/two_point_lp_barrier.md)
- Exact barrier verifier:
  [`verifiers/verify_two_point_barrier.py`](verifiers/verify_two_point_barrier.py)
- Exact fixed-\(D_5\) saturation lemma:
  [`proofs/d5_saturation.md`](proofs/d5_saturation.md)
- Exact quadratic-kernel constraints and counterexamples:
  [`proofs/rank_kernel_barriers.md`](proofs/rank_kernel_barriers.md)
- Fixed-\(41\) three-point formulation and exact pseudo-distributions:
  [`proofs/fixed41_three_point_formulation.md`](proofs/fixed41_three_point_formulation.md)
- All-degree exact three-point barrier:
  [`proofs/fixed41_bv_all_harmonics.md`](proofs/fixed41_bv_all_harmonics.md)
- Degree-two BV-surviving labeled object and its exact degree-three separator:
  [`proofs/degree2_bv_barrier.md`](proofs/degree2_bv_barrier.md)
- Exact local links and a contact-free maximal code:
  [`proofs/local_link_geometry.md`](proofs/local_link_geometry.md)
- Exact one-sided bound, Tukey-depth, and contact/sign consequences:
  [`proofs/one_sided_tukey_bound.md`](proofs/one_sided_tukey_bound.md)
- Exact degree-10 cap-SDP bound \(B(5)\le35\):
  [`proofs/one_sided_cap_degree10_bound.md`](proofs/one_sided_cap_degree10_bound.md)
- Exact degree-11 cap-SDP bound \(B(5)\le34\) and independent audit:
  [`proofs/one_sided_cap_degree11_bound.md`](proofs/one_sided_cap_degree11_bound.md)
  and
  [`proofs/one_sided_cap_degree11_adversarial_audit.md`](proofs/one_sided_cap_degree11_adversarial_audit.md)
- Exact enlarged-cap degree-11 theorem at height \(-1/300\):
  [`proofs/one_sided_cap_degree11_robust.md`](proofs/one_sided_cap_degree11_robust.md)
- Tangent nonnegative-neighborhood projection and minimum negative degree:
  [`proofs/tangent_nonnegative_neighborhood.md`](proofs/tangent_nonnegative_neighborhood.md)
- Improved exact cap/frame conditioning:
  [`proofs/improved_frame_cap_bound.md`](proofs/improved_frame_cap_bound.md)
- Sharp rank-five spectral moment and four-/six-cycle identities:
  [`proofs/rank_five_spectral_moment.md`](proofs/rank_five_spectral_moment.md)
  and
  [`proofs/rank_five_four_cycle_moments.md`](proofs/rank_five_four_cycle_moments.md)
- Exact weighted-residual/triple-incidence barrier:
  [`proofs/weighted_residual_barrier.md`](proofs/weighted_residual_barrier.md)
- Exact degree-three local-hybrid barrier:
  [`proofs/local_hybrid_degree3_barrier.md`](proofs/local_hybrid_degree3_barrier.md)
- Exact degree-three plus rank-five barrier and its common-graph covariance
  failure:
  [`proofs/local_hybrid_degree3_rank_barrier.md`](proofs/local_hybrid_degree3_rank_barrier.md)
- Strongest degree-three/rank/color-moment barrier:
  [`proofs/local_hybrid_degree3_rank_color_barrier.md`](proofs/local_hybrid_degree3_rank_color_barrier.md)
- Universal harmonic-combination centered-skew rank inequality and exact
  witness separators:
  [`proofs/harmonic_combination_centered_skew.md`](proofs/harmonic_combination_centered_skew.md)
- Exact degree-five necessary-rank separator for the historical five-node
  support:
  [`proofs/local5_degree5_necessary_rank_separator.md`](proofs/local5_degree5_necessary_rank_separator.md)
- Exact common-neighbor/edge-conditioned \(K_4\) obstruction:
  [`proofs/edge_conditioned_k4_exact_obstruction.md`](proofs/edge_conditioned_k4_exact_obstruction.md)
- Corrected common-pair hierarchy audit and exact fixed-support dual:
  [`proofs/common_pair_capacity_hierarchy_adversarial_audit.md`](proofs/common_pair_capacity_hierarchy_adversarial_audit.md)
  and
  [`proofs/common_pair_capacity_stratified_obstruction.md`](proofs/common_pair_capacity_stratified_obstruction.md)
- Continuous-grid rank/BV barrier search:
  [`experiments/continuous_rank_bv_search/RESULTS.md`](experiments/continuous_rank_bv_search/RESULTS.md)
- Exact anchored negative-cap inequality and nonseparation audit:
  [`proofs/anchored_negative_cap_kernel.md`](proofs/anchored_negative_cap_kernel.md)
- Depth-seven positive-circuit packing and exact barrier catalog:
  [`proofs/positive_circuit_packing_from_depth.md`](proofs/positive_circuit_packing_from_depth.md)
- Low-harmonic frame-potential inequalities and their all-harmonic
  mass-41 barrier:
  [`proofs/harmonic_rank_frame_barrier.md`](proofs/harmonic_rank_frame_barrier.md)
- Exact sparse deep-graph classification, angular bounds, and rank-20
  countermodel:
  [`proofs/sparse_deep_graph_stability.md`](proofs/sparse_deep_graph_stability.md)
- Effective root-system stability bound:
  [`proofs/quantitative_root_system_stability.md`](proofs/quantitative_root_system_stability.md)
- Exact split quadratic-kernel countermodel:
  [`proofs/split_kernel_abstract_barrier.md`](proofs/split_kernel_abstract_barrier.md)
- Lorentzian inertia/Perron/star-complement structure and exact weakened
  surrogate:
  [`proofs/lorentzian_inertia_graph.md`](proofs/lorentzian_inertia_graph.md)
- Stronger full-entry-interval split-kernel countermodel:
  [`proofs/split_kernel_full_interval_barrier.md`](proofs/split_kernel_full_interval_barrier.md)
- Exact separator for the attempted all-harmonic/rank-witness mixture:
  [`proofs/fixed41_rank_mixture_separator.md`](proofs/fixed41_rank_mixture_separator.md)
- Exact maximum-volume semialgebraic reduction:
  [`proofs/max_volume_semialgebraic_reduction.md`](proofs/max_volume_semialgebraic_reduction.md)
- Degree-two Tverberg constraint and exact rank-five barrier:
  [`proofs/tverberg_moment_barrier.md`](proofs/tverberg_moment_barrier.md)
- Exact antipodal upper bound and unrestricted deep-pair corollary:
  [`proofs/antipodal_bound.md`](proofs/antipodal_bound.md) and
  [`proofs/negative_tail_graph.md`](proofs/negative_tail_graph.md)
- Exact Pfender/local-hybrid inequalities and their surviving mass-41
  two-point witness:
  [`proofs/local_hybrid_barrier.md`](proofs/local_hybrid_barrier.md)
- Reproducible construction round:
  [`experiments/construction_round1.md`](experiments/construction_round1.md)
- Independent layer, higher-root-map, projective-line, and sharp
  deep-graph construction searches:
  [`experiments/construction_round2/RESULTS.md`](experiments/construction_round2/RESULTS.md)
- 152 unrestricted Riemannian augmented-Lagrangian trials and complete
  numerical diagnostics:
  [`experiments/construction_round3/README.md`](experiments/construction_round3/README.md)
- Asymmetric deletion/reinsertion, basin-hopping, and released SQP surgery:
  [`experiments/construction_round4_surgery/README.md`](experiments/construction_round4_surgery/README.md)
- Unrestricted inverse-chord population continuation and crossover:
  [`experiments/construction_round5_population/README.md`](experiments/construction_round5_population/README.md)
- Riemannian nonsmooth active-bundle and facet-escape continuation:
  [`experiments/construction_round6_bundle/README.md`](experiments/construction_round6_bundle/README.md)
- Core/rattler deletion, facet-insertion, quake, and replica-exchange search:
  [`experiments/construction_round9_core_rattler/README.md`](experiments/construction_round9_core_rattler/README.md)
- Imported discovery-only numerical 41-point near miss:
  [`experiments/input/spherical_codes_5_41.txt`](experiments/input/spherical_codes_5_41.txt)

## Claims surviving adversarial audit

- The 40 stored vectors are distinct.
- Every stored vector has squared norm 2 before normalization.
- Every distinct stored pair has integer dot product at most 1, hence normalized
  inner product at most \(1/2\).
- Boundary equality is accepted: many pairs have inner product exactly
  \(1/2\).

These statements currently have a direct proof and a separate exact checker;
a second human/agent audit is still pending.

- The mass-41 two-point witness has exact total mass and pair-count parity.
- Its normalized Gegenbauer moments are positive through degree 53 by rational
  recurrence and in all higher degrees by an explicit analytic tail bound.
- The fixed \(D_5\) code is saturated against adding one point; its exact
  covering value is \(\sqrt{2/5}\).
- The finite-field and \(D_6\) examples exactly refute generic sign/rank
  shortcuts, while the split harmonic-factor Ky Fan inequalities remain valid
  for every actual rank-five Gram matrix.
- Contact-clique links have exact bounds \(15,7,4,2,0\), and every pair has at
  most seven common contact neighbors.
- Every antipodal five-dimensional kissing code has at most 40 points.
  Consequently the \(<-1/2\) graph of a hypothetical 41-code is triangle-free,
  has independence number at most 20, and has at least 23 edges.
- Every hypothetical 41-code admits the exact compact 190-variable
  maximum-volume formulation recorded in the semialgebraic certificate.
- Every one-sided five-dimensional kissing code has at most 34 points.
  Hence a hypothetical 41-code has origin Tukey depth at least seven and
  remains positively spanning after any six deletions.  The exact
  degree-11 cap kernel, all hemisphere boundary conventions, and the complete
  5,995-leaf Bernstein tree passed a separate independent audit.
- The same exact kernel bounds every kissing code in the enlarged cap
  \(\langle e,x\rangle\ge-1/300\) by 34.  Its independently rebuilt
  6,053-leaf tree includes the new cap face and every determinant/contact
  boundary, forcing seven points on each strict side of the
  \(\pm1/300\) slabs in every direction.
- The Lorentzian matrix \(A=2G-J\) of a hypothetical 41-code has exact
  inertia \((5,1,35)\), and \(W=I-A\) has \(18<\rho\le42\).  A normalized
  circuit identity \(A\alpha=-c{\bf1}\) makes \(c\) the unique PSD
  rank-five shift; an exact \(c=21/19\) surrogate demonstrates why the
  normalization cannot be weakened.
- The fixed-41 rational pair/triple pseudo-distribution passes all ordinary
  and Bachoc--Vallentin three-point harmonic inequalities at every degree,
  with unrestricted radial test functions.  An independent adversarial audit
  rederived the endpoint normalization, parity recurrence, finite/tail
  coverage, norm argument, and arbitrary-radial factorization and found no
  mathematical gap.
- Every genuine Gram source satisfies the exact residual-vector square
  inequality displayed above; its negative value on the labeled pseudo-object
  is independently recomputable in rational arithmetic.
- Every hypothetical rank-five Gram spectrum satisfies
  \(20D^2\le9V^3\).  The bound is sharp, including for a concrete exact
  11-point code, and rejects both stored pair/triple witnesses by exact
  rational margins.
- The exact cap polynomial proves
  \(A(4,7123/12877)\le30\), including the closed endpoint, and therefore the
  strict frame floor \(15059/40000\).  Its coefficients and objective have
  been independently recomputed.
- A triangle-free 41-vertex graph with independence number at most 20 and
  exactly 23 edges is uniquely \(C_5\sqcup18K_2\); at 24 edges exactly three
  graph types occur.  Exact component bookkeeping and strict angular
  boundaries are independently checked.
- At the exact-antipodal boundary of each sparse deep graph, the vanishing of
  every base/base and base/core projective penalty is impossible: ADE
  classification forces a \(D_5\) root system with one fewer unused oriented
  root slot than the core requires.

## Failed or rejected claims

- “An extremal 40-point configuration must be \(D_5\), antipodal, or unique”:
  **refuted** by the known \(D_5,L_5,Q_5,R_5\) examples.
- “A generic PSD relaxation of the Gram constraints proves the desired upper
  bound”: **rejected** because it discards the essential rank-at-most-5
  condition unless an additional mechanism recovers it.
- “A floating-point SDP objective below 41 is itself a proof”: **rejected**;
  exact or directed-interval dual feasibility is required.
- “Positive diagonal, nonpositive off-diagonal entries, rank below half the
  order, and at most one negative eigenvalue are mutually incompatible”:
  **refuted** by the analogous quadratic kernel of the exact \(D_6\) root code.
- The first low-degree public Lasserre-code trial did not reach an SDP: exact
  symmetry-basis generation raised `UndefRefError` under the resolved
  Julia/Nemo environment.  This is an environment failure, not evidence about
  feasibility or the bound.
- “Failure to append one point to \(D_5\) proves the global upper bound”:
  **refuted**; it proves saturation of one fixed configuration only.
- “An inclusion-maximal code must have contacts or a positive minimum contact
  degree”: **refuted** by an exact 26-point inclusion-maximal code whose
  contact graph is empty.
- “Matching first and second moments on three disjoint Tverberg parts is
  contradictory for a five-dimensional kissing code”: **refuted** by an exact
  18-point rank-five code partitioned into three regular simplices with common
  moments \(m=0,M=I/5\).
- “The fixed-\(41\) three-point relaxation is already infeasible at low
  degree, or eventually becomes infeasible at high harmonic degree”:
  **refuted** for the complete formulation used here by the all-degree exact
  rational pseudo-distribution.
- “The displayed rank-five spectral inequalities alone exclude all feasible
  fixed-41 pair/triple moments”: **refuted** by a feasible small-variance
  five-eigenvalue completion with \(D=0\); actual four-point linkage is still
  required.
- “The quadratic-kernel sign, rank, trace, and both split Ky Fan constraints
  imply \(N\le40\)”: **refuted** by an exact 41-row split-feature
  counterexample.  It fails precisely the common-source entry range.
- “Adding the full genuine off-diagonal interval for the split quadratic
  kernel makes those abstract constraints sufficient”: **refuted** by an
  exact cyclic Fourier 41-row counterexample with a strict \(1/2000\) interval
  buffer.  It still violates the original kissing inequality on the linear
  factor and the nonlinear common-source factor identity.
- “Aggregate projective-kernel positivity and every local deep-component
  inequality force at least 24 deep pairs”: **refuted** by an exact rank-20
  code with deep graph \(C_5\sqcup18K_2\).  Rank five and cross-component
  compatibility are indispensable.
