# Theorem map and dependencies

This map is a reading guide to the frozen full proofs. “Barrier” means failure of the specified inference or method. No listed deterministic or abstract example is a positive-uniform-probability counterexample. Dependencies refer to the IDs below or to explicitly credited external inputs. Independent reviews are AI mathematical audits, not human peer review.

## F1 Two seed limits

**Type:** uniform-class theorem.

Exactly uniform 1342 avoiders have exponential fixed weak-deviation tails about the anti-diagonal; exact symmetries prove the original target for alpha=132 and 213.

**Dependencies:** Bóna exact labeled-tree/forest bijection and minima preservation.

**Full proof:**
- [TWO_SUBCASE_THEOREM.md](diagonal_permuton_1778_20261014/pass1_uncovered_case/TWO_SUBCASE_THEOREM.md)
- [KERNEL_ENUMERATION_APPENDIX.md](diagonal_permuton_1778_20261014/pass1_entropy/KERNEL_ENUMERATION_APPENDIX.md)

**Independent audit:**
- [WEIGHTED_HEIGHT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass1_bijection_audit/WEIGHTED_HEIGHT_ACCEPTANCE.md)
- [DERIVATIVE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass1_bijection_audit/DERIVATIVE_ACCEPTANCE.md)
- [KERNEL_ENUMERATION_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass1_bijection_audit/KERNEL_ENUMERATION_ACCEPTANCE.md)
- [INDEPENDENT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/independent_family_reaudit/INDEPENDENT_ACCEPTANCE.md)

## F2 Two infinite seeded families

**Type:** uniform-class theorem.

For every fixed r>=0, alpha=132 skew-sum J_r or 213 skew-sum J_r has the diagonal limit with exponential fixed-deviation tails. The closure theorem requires a starts-with-1 pattern and an exponentially concentrating seed.

**Dependencies:** F1; Bóna exact growth equality for starts-with-1 patterns.

**Full proof:**
- [MERGE_TRANSFER_THEOREM.md](diagonal_permuton_1778_20261014/pass2_protected_tail_extension/MERGE_TRANSFER_THEOREM.md)

**Independent audit:**
- [MERGE_TRANSFER_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_bijection_audit/MERGE_TRANSFER_ACCEPTANCE.md)
- [INDEPENDENT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/independent_family_reaudit/INDEPENDENT_ACCEPTANCE.md)

## G1 Frontier and small-value localization

**Type:** general partial theorem.

For fixed alpha of length at least two, alpha-free initial prefixes and positions of the smallest o(n) values have exponential linear-scale tails. Positive-density localization retains binary entropy.

**Dependencies:** Catalan descendant comparison; exact unique minimum-deletion ancestry.

**Full proof:**
- [ACTIVE_FRONTIER_PROOF.md](diagonal_permuton_1778_20261014/pass1_concentration/ACTIVE_FRONTIER_PROOF.md)

**Independent audit:**
- [AUDIT.md](diagonal_permuton_1778_20261014/pass1_concentration_audit/AUDIT.md)
- [CONCENTRATION_LEMMA_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass1_bijection_audit/CONCENTRATION_LEMMA_ACCEPTANCE.md)

## G2 Completion-weighted bulk and pointwise limits

**Type:** exact reduction and barrier.

The descendant-weighted inversion identity exposes the remaining bulk estimate. Single off-diagonal points and maximum displacement need not concentrate; one point has mass 1/n. Growth and independent quadrant counts alone do not settle weak convergence.

**Dependencies:** G1.

**Full proof:**
- [BULK_BOTTLENECK.md](diagonal_permuton_1778_20261014/pass1_concentration/BULK_BOTTLENECK.md)
- [ENTROPY_OBSTRUCTIONS.md](diagonal_permuton_1778_20261014/pass1_entropy/ENTROPY_OBSTRUCTIONS.md)

**Independent audit:**
- [AUDIT.md](diagonal_permuton_1778_20261014/pass1_concentration_audit/AUDIT.md)
- [BULK_BOTTLENECK_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass1_concentration_audit/BULK_BOTTLENECK_ACCEPTANCE.md)

## G3 Scalar numerical assumptions are insufficient

**Type:** abstract method obstruction.

The repaired abstract tree satisfies the stated full numerical completion constraints but has macroscopic completion-weighted ancestors. It is not a principal avoidance class. The earlier coarse model fails a sharper bound (51>50).

**Dependencies:** G1; G2.

**Full proof:**
- [COMPLETION_BOUND_COUNTERMODEL.md](diagonal_permuton_1778_20261014/pass2_bulk_concentration/COMPLETION_BOUND_COUNTERMODEL.md)
- [COARSE_TREE_COUNTERMODEL.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/COARSE_TREE_COUNTERMODEL.md)

**Independent audit:**
- [COMPLETION_COUNTERMODEL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/COMPLETION_COUNTERMODEL_ACCEPTANCE.md)
- [COARSE_COUNTERMODEL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_bijection_audit/COARSE_COUNTERMODEL_ACCEPTANCE.md)

## G4 First-hit prefix state

**Type:** exact reduction.

The standardized first-hit prefix and its absent flag determine the entire minimum-insertion continuation tree; scalar length alone does not.

**Dependencies:** G1.

**Full proof:**
- [PREFIX_STATE_REDUCTION.md](diagonal_permuton_1778_20261014/pass2_bulk_concentration/PREFIX_STATE_REDUCTION.md)

**Independent audit:**
- [COMPLETION_COUNTERMODEL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/COMPLETION_COUNTERMODEL_ACCEPTANCE.md)

## G5 Growth packing and spatial compatibility

**Type:** general partial theorem and deterministic barrier.

For fixed alpha of length at least two, Av(alpha) has a strict growth gap, deletion distance is linear, and disjoint alpha packing is linear with exponentially high probability. Actual perfect-packing sequences still have fixed positive weak deviation; no uniform-probability claim follows.

**Dependencies:** G1; G2.

**Full proof:**
- [GROWTH_PACKING_AND_SPATIAL_BARRIER.md](diagonal_permuton_1778_20261014/pass4_general_alpha/GROWTH_PACKING_AND_SPATIAL_BARRIER.md)

**Independent audit:**
- [GENERAL_ALPHA_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/GENERAL_ALPHA_ACCEPTANCE.md)
- [PASS4_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/PASS4_STRUCTURAL_ACCEPTANCE.md)

## G6 General diagonal-cut states

**Type:** exact transfer and partial theorem.

Open endpoint orders and closed-interior gridded pattern profiles give exact exposure states. Fixed width K has rational enumeration and lambda_K<lambda with supremum lambda; fixed bounded width is exponentially rare. Width/n is uncontrolled. Closed context matters exponentially already at width one.

**Dependencies:** G5.

**Full proof:**
- [EXACT_CUT_STATES_AND_CONTEXT_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass5_general_cuts/EXACT_CUT_STATES_AND_CONTEXT_OBSTRUCTION.md)

**Independent audit:**
- [GENERAL_CUT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/GENERAL_CUT_ACCEPTANCE.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)

## S1 Canonical staircase prefixes

**Type:** 1324 partial theorem.

Every fixed number of initial canonical cells has o(n) mass with exponential linear-scale tails. Bounded canonical width has a strict growth gap. The deterministic metric bound uses three times largest-cell mass.

**Dependencies:** G1; Bevan–Brignall–Elvey Price–Pantone canonical staircase gridding.

**Full proof:**
- [FIXED_STAIRCASE_PREFIX_THEOREM.md](diagonal_permuton_1778_20261014/pass2_1324_shape/FIXED_STAIRCASE_PREFIX_THEOREM.md)

**Independent audit:**
- [FIXED_STAIRCASE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/FIXED_STAIRCASE_ACCEPTANCE.md)
- [STAIRCASE_GEOMETRY_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_bijection_audit/STAIRCASE_GEOMETRY_ACCEPTANCE.md)

## S2 Directed kernel and both completion factors

**Type:** exact transfer.

The canonical normalized-state encoding has exact kernel K. Marked-cell mass uses z^|A| ell_A h_A. Incoming completion factors can be exponentially large.

**Dependencies:** S1.

**Full proof:**
- [EXACT_GREEDY_TRANSFER.md](diagonal_permuton_1778_20261014/pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md)

**Independent audit:**
- [PAIR_LOCAL_KERNEL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_bijection_audit/PAIR_LOCAL_KERNEL_ACCEPTANCE.md)
- [TRANSFER_ANALYTIC_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/TRANSFER_ANALYTIC_ACCEPTANCE.md)

## S3 Squared-kernel bridge and its obstruction

**Type:** conditional theorem with impossible hypothesis.

The implication beta<lambda => exponential largest-cell tails is valid, but exact parity collapse and guards prove beta>=lambda. Reciprocal products obstruct every positive diagonal Hilbert–Schmidt reweighting for z>rho. No general operator or weak-limit impossibility is asserted.

**Dependencies:** S1; S2.

**Full proof:**
- [SQUARED_KERNEL_NEXT_TARGET.md](diagonal_permuton_1778_20261014/pass2_staircase_bias/SQUARED_KERNEL_NEXT_TARGET.md)
- [SQUARED_KERNEL_GAP_IMPOSSIBLE.md](diagonal_permuton_1778_20261014/pass3_kernel_feasibility/SQUARED_KERNEL_GAP_IMPOSSIBLE.md)
- [TWO_SHUFFLE_BOUND.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/TWO_SHUFFLE_BOUND.md)
- [WEIGHTED_OPERATOR_BOUNDARY.md](diagonal_permuton_1778_20261014/pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md)

**Independent audit:**
- [CONDITIONAL_SPECTRAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_bijection_audit/CONDITIONAL_SPECTRAL_ACCEPTANCE.md)
- [TRANSFER_ANALYTIC_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass2_concentration_audit/TRANSFER_ANALYTIC_ACCEPTANCE.md)
- [DOMINO_OBSTRUCTION_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_bijection_audit/DOMINO_OBSTRUCTION_ACCEPTANCE.md)
- [TWO_POINT_PADDING_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_bijection_audit/TWO_POINT_PADDING_ACCEPTANCE.md)
- [OPERATOR_AND_MARK_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/OPERATOR_AND_MARK_ACCEPTANCE.md)

## S4 Arbitrary-index isolated blocks

**Type:** 1324 partial theorem.

For fixed K, macroscopic K-cell blocks with sufficiently small neighboring mass are exponentially rare. Some fixed largest-cell fraction c<1 is exponentially unlikely, but sublinearity is not established.

**Dependencies:** S1; S2.

**Full proof:**
- [ISOLATED_BLOCK_TAIL.md](diagonal_permuton_1778_20261014/pass3_kernel_feasibility/ISOLATED_BLOCK_TAIL.md)
- [LARGEST_CELL_FRACTION_COROLLARY.md](diagonal_permuton_1778_20261014/pass3_kernel_feasibility/LARGEST_CELL_FRACTION_COROLLARY.md)

**Independent audit:**
- [ISOLATED_BLOCK_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_bijection_audit/ISOLATED_BLOCK_STRUCTURAL_ACCEPTANCE.md)
- [ISOLATED_BLOCK_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/ISOLATED_BLOCK_ACCEPTANCE.md)

## S5 Rerooting and one-sided marks

**Type:** 1324 partial theorem.

One-point rerooting retains the removed incoming shuffle and yields all-index large upward-jump tails. A common first-cell exponential mark holds throughout z<rho. Graded actual canonical mountains show why local cones do not settle the limit.

**Dependencies:** G1; S1; S2.

**Full proof:**
- [REROOTING_ONE_POINT_BOUND.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/REROOTING_ONE_POINT_BOUND.md)
- [WEIGHTED_OPERATOR_BOUNDARY.md](diagonal_permuton_1778_20261014/pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md)
- [GRADED_CELL_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass3_kernel_bounds/GRADED_CELL_OBSTRUCTION.md)

**Independent audit:**
- [REROOTING_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_bijection_audit/REROOTING_STRUCTURAL_ACCEPTANCE.md)
- [REROOTING_INDEPENDENT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_kernel_bounds/REROOTING_INDEPENDENT_ACCEPTANCE.md)
- [OPERATOR_AND_MARK_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_concentration_audit/OPERATOR_AND_MARK_ACCEPTANCE.md)
- [GRADED_STAIRCASE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass3_bijection_audit/GRADED_STAIRCASE_ACCEPTANCE.md)

## S6 Terminal and joint endpoint marks

**Type:** 1324 partial theorem.

A parity-dependent symmetry and guard give z ell_A<=2 h_(12 skew-sum inverse(A)), common terminal marks and joint endpoint marks. Multiplying the one-sided estimates does not yield a bulk mark near rho.

**Dependencies:** S2; S5.

**Full proof:**
- [TERMINAL_MARK_AND_POINTWISE_LIFT.md](diagonal_permuton_1778_20261014/pass4_two_sided_mark/TERMINAL_MARK_AND_POINTWISE_LIFT.md)

**Independent audit:**
- [TERMINAL_MARK_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/TERMINAL_MARK_ACCEPTANCE.md)
- [PASS4_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/PASS4_STRUCTURAL_ACCEPTANCE.md)

## S7 One-ended and two-ended window certificates

**Type:** exact finite-width bounds.

Exact minimax local reroot certificates lower-bound true gaps, but decay exponentially in width. Fixed-width unrestricted/canonical growth agrees; g1=4 and g2=27/4, with a credited fixed-width source lower bound.

**Dependencies:** S1; S2; S3; S5; S6; Bevan–Brignall–Elvey Price–Pantone domino enumeration and construction.

**Full proof:**
- [QUANTITATIVE_WINDOW_GAPS.md](diagonal_permuton_1778_20261014/pass4_window_gaps/QUANTITATIVE_WINDOW_GAPS.md)
- [TWO_ENDED_WINDOW_GAPS.md](diagonal_permuton_1778_20261014/pass4_window_gaps/TWO_ENDED_WINDOW_GAPS.md)
- [FIXED_WIDTH_CALIBRATION.md](diagonal_permuton_1778_20261014/pass4_window_gaps/FIXED_WIDTH_CALIBRATION.md)

**Independent audit:**
- [QUANTITATIVE_GAP_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/QUANTITATIVE_GAP_ACCEPTANCE.md)
- [TWO_ENDED_GAP_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/TWO_ENDED_GAP_ACCEPTANCE.md)
- [FIXED_WIDTH_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/FIXED_WIDTH_ACCEPTANCE.md)
- [PASS4_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/PASS4_STRUCTURAL_ACCEPTANCE.md)
- [TWO_ENDED_SUPPLEMENT.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/TWO_ENDED_SUPPLEMENT.md)

## S8 Adaptive windows and true gaps

**Type:** conditional theorem and deterministic barriers.

If the sum of true gaps log(lambda/gK) diverges, bounded total centered-window boundary entropy gives exponential largest-cell tails. Actual mountains defeat the proved one-/two-ended certificates at every bounded width, and even the true gaps at widths one and two. No true all-width obstruction is proved.

**Dependencies:** S4; S5; S6; S7.

**Full proof:**
- [ADAPTIVE_WINDOW_ENTROPY.md](diagonal_permuton_1778_20261014/pass4_adaptive_profiles/ADAPTIVE_WINDOW_ENTROPY.md)
- [EXACT_CANONICAL_WINDOW_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass4_adaptive_profiles/EXACT_CANONICAL_WINDOW_OBSTRUCTION.md)
- [TWO_ENDED_CERTIFICATE_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass4_adaptive_profiles/TWO_ENDED_CERTIFICATE_OBSTRUCTION.md)
- [SMALL_WINDOW_TRUE_GAPS.md](diagonal_permuton_1778_20261014/pass4_adaptive_profiles/SMALL_WINDOW_TRUE_GAPS.md)

**Independent audit:**
- [ADAPTIVE_ENTROPY_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/ADAPTIVE_ENTROPY_ACCEPTANCE.md)
- [FIXED_WIDTH_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/FIXED_WIDTH_ACCEPTANCE.md)
- [TWO_ENDED_GAP_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/TWO_ENDED_GAP_ACCEPTANCE.md)
- [PASS4_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/PASS4_STRUCTURAL_ACCEPTANCE.md)
- [PROFILE_SUPPLEMENT_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_geometry_audit/PROFILE_SUPPLEMENT_ACCEPTANCE.md)

## S9 Increasing pairs and internal chains

**Type:** exact equivalent criterion.

Expected increasing-pair count o(n²) is equivalent to the 1324 anti-diagonal limit. The exact series retains both completion factors and actual edge-shuffle pair counts. Within-state pairs are bounded by size times (LIS-1); cross-state pairs still require control.

**Dependencies:** S2.

**Full proof:**
- [POINT_PAIR_TARGET.md](diagonal_permuton_1778_20261014/pass4_two_sided_mark/POINT_PAIR_TARGET.md)
- [INTERNAL_CHAIN_REDUCTION.md](diagonal_permuton_1778_20261014/pass4_two_sided_mark/INTERNAL_CHAIN_REDUCTION.md)

**Independent audit:**
- [POINT_PAIR_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/POINT_PAIR_ACCEPTANCE.md)
- [INTERNAL_CHAIN_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass4_concentration_audit/INTERNAL_CHAIN_ACCEPTANCE.md)

## S10 Arbitrary-length low-chain runs

**Type:** 1324 restricted-run theorem.

Canonical paths with every cell LIS<=2 have growth at most 8. Macroscopic such runs with sufficiently small boundary mass are exponentially rare because lambda>=81/8. Whole-path low-chain probability is exponentially small. Genuine dense edges show small endpoint LIS does not suppress cross-pair density.

**Dependencies:** S2; S4; S9; Bevan–Brignall–Elvey Price–Pantone lower bound 81/8.

**Full proof:**
- [LOW_CHAIN_RUN_THEOREM.md](diagonal_permuton_1778_20261014/pass5_pair_counts/LOW_CHAIN_RUN_THEOREM.md)

**Independent audit:**
- [LOW_CHAIN_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/LOW_CHAIN_ACCEPTANCE.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)

## S11 Height-three size-weight threshold

**Type:** restricted upper bound and method barrier.

LIS<=3 canonical paths have growth at most 6+2sqrt(5). Pure exponential size weights cannot improve the actual-kernel contraction threshold beyond that number. No inspected lower growth bound supplies the necessary strict gap; Norton v3 supplies no upgrade.

**Dependencies:** S2; S10.

**Full proof:**
- [HEIGHT_THREE_SIZE_WEIGHT_BARRIER.md](diagonal_permuton_1778_20261014/pass5_pair_counts/HEIGHT_THREE_SIZE_WEIGHT_BARRIER.md)

**Independent audit:**
- [HEIGHT_THREE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/HEIGHT_THREE_ACCEPTANCE.md)
- [NEW_LOWER_BOUND_STATUS.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/NEW_LOWER_BOUND_STATUS.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)

## S12 Rectangle deletion and occupied/sparse branches

**Type:** 1324 partial theorem and exact reduction.

Deleting an increasing rectangle gives an empty marked skeleton with exact allocation and admissibility records. Positive entropy margin gives an exponential tail; p+q<=m suffices for macroscopic m. A fixed coarse grid yields occupied-core or many small-interior-pair branches, without favorable contamination automatically.

**Dependencies:** S2; S7; S9.

**Full proof:**
- [RECTANGLE_DELETION_AND_ENTROPY.md](diagonal_permuton_1778_20261014/pass5_pair_rectangles/RECTANGLE_DELETION_AND_ENTROPY.md)
- [COARSE_RECTANGLE_DICHOTOMY.md](diagonal_permuton_1778_20261014/pass5_pair_rectangles/COARSE_RECTANGLE_DICHOTOMY.md)

**Independent audit:**
- [RECTANGLE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/RECTANGLE_ACCEPTANCE.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)

## S13 Comb and near-empty rectangles

**Type:** actual deterministic method barriers.

Canonical comb mountains defeat the raw favorable-rectangle score. Canonical near-empty examples have LIS=o(n), exactly-empty count=o(n²), and positive total pair density while every interior is o(n). Neither family has an established positive uniform probability.

**Dependencies:** S2; S5; S9; S12.

**Full proof:**
- [COMB_RECTANGLE_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass5_pair_rectangles/COMB_RECTANGLE_OBSTRUCTION.md)
- [NEAR_EMPTY_PAIR_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass5_pair_rectangles/NEAR_EMPTY_PAIR_OBSTRUCTION.md)

**Independent audit:**
- [RECTANGLE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/RECTANGLE_ACCEPTANCE.md)
- [NEAR_EMPTY_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/NEAR_EMPTY_ACCEPTANCE.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)
- [PASS5_SUPPLEMENTAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_SUPPLEMENTAL_ACCEPTANCE.md)

## S14 Folding information and quadratic model gaps

**Type:** specific encoding obstruction and comparison theorem.

The specified canonical fold has exponentially large fibres even with source turnaround coordinates retained. A distinct decreasing-staircase model has exact growth 4cos²(pi/(K+2)) and summable quadratic gaps. Neither result determines actual 1324 gap summability or refutes the weak-limit target.

**Dependencies:** S2; S3; S7; S8; Albert–Brignall–Ruskuc–Vatter monotone staircase existence; Bevan grid growth attribution.

**Full proof:**
- [FOLDING_ENTROPY_OBSTRUCTION.md](diagonal_permuton_1778_20261014/pass5_collective_windows/FOLDING_ENTROPY_OBSTRUCTION.md)
- [QUADRATIC_STAIRCASE_BARRIER.md](diagonal_permuton_1778_20261014/pass5_collective_windows/QUADRATIC_STAIRCASE_BARRIER.md)

**Independent audit:**
- [FOLDING_DERIVATIVE_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/FOLDING_DERIVATIVE_ACCEPTANCE.md)
- [QUADRATIC_MODEL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_concentration_audit/QUADRATIC_MODEL_ACCEPTANCE.md)
- [PASS5_STRUCTURAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_STRUCTURAL_ACCEPTANCE.md)
- [PASS5_SUPPLEMENTAL_ACCEPTANCE.md](diagonal_permuton_1778_20261014/pass5_geometry_audit/PASS5_SUPPLEMENTAL_ACCEPTANCE.md)
