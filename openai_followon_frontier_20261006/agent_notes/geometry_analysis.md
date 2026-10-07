# Geometry and analysis frontier screen

Checkpoint: 2026-10-06 PDT. Screening complete (100% of this delegated screen); no discovery/proof claim. Primary local proof components and current primary literature were inspected. No external communications or research execution.

## Important priority exclusion: KLS

Do **not** recommend proving KLS as a first new result. Current primary arXiv records confirm:

- Bizeul–Klartag–Lehec, *Presenting a proof of the Kannan–Lovasz–Simonovits conjecture*, submitted October 4, 2026: https://arxiv.org/abs/2610.05474 . Abstract explicitly claims the full conjecture, via Song–Zhang's high-derivative tilt-average criterion.
- Song–Zhang, *An O(1) Bound for the KLS Constant*, revised October 4, 2026: https://arxiv.org/abs/2610.01447 . Current abstract explicitly claims universal bounds for both KLS and isotropic Poincare constants.

These are claims, not independently audited proofs here, but defeat an unqualified priority claim. Local #093 is the subgaussian LSI theorem, with entropy-extremizer, noisy-prediction, tensor-hierarchy and Gaussian covariance information arguments; #101 is sharp simplex/entropy. Neither is needed to rediscover a result already publicly claimed by two teams. Also, slicing does not imply KLS by the familiar implication chain: the familiar direction runs from KLS/thin-shell toward slicing.

## Strongest well-grounded mechanism: full pointwise multiple ergodic theorem

**Exact target.** For every invertible probability-preserving transformation T, every finite k, and every fixed tuple of bounded measurable f_1,...,f_k, prove almost-everywhere convergence, along every positive integer N, of

    A_N(x) = N^(-1) sum_{n=1}^N product_{j=1}^k f_j(T^(jn)x).

The limit is the known Host–Kra/Ziegler norm limit, generally NOT the product of the integrals. Aim at this single-transformation linear-pattern theorem first, not arbitrary commuting transformations or polynomial patterns. Impact estimate **9.2**, assuming correct, novel and published; it settles the classical pointwise Furstenberg problem in full finite length.

**New input actually read.** Local #154, `preprints/Pointwise-Multiple-Ergodic-Averages-for-Mixing-Transformations-October-4-2026/build/sections/{introduction,channels,correlations,packing,inputs}.tex`. Its introduction says the distinct-slopes companion proves a triple oscillation estimate on arbitrary systems and thereby triple convergence with distinct positive slopes without mixing. That general triple consequence is ALREADY INSIDE the release; do not propose it as new.

The new arbitrary-length proof builds a probability law from a measurably selected bad averaging length, organizes outputs into three groups, uses a tensor-packing bound to preserve channel independence under selected laws, minimizes correlation support, saturates conditional-expectation energies under extensions, and uses a square construction to increase the number of output-only slots. That is substantial reusable machinery, beyond the bare headline theorem for mixing systems.

**Exact gap.** `channels.tex`, proof of channel closure, especially lines 123–180, uses mixing of all orders in two ways: absolute Cesaro decay of centered multiple correlations, and bounded maximum degree of the exceptional Gram-pair graph. In the latter, small inner products hold except when finitely many pairs of affine times are separated by a bounded amount. `packing.tex` then bounds the captured vectors by

    C (1+L) epsilon^(-2) exp(C epsilon^(-2) sqrt(d) log(2+d)),

where L is the bad graph's maximum degree and d≈(log m)^(3/2). It needs this to be o(m), and the selector-control remainder must also be summable across dyadic length scales. Weak mixing gives sparse bad-pair sets in an averaged sense, not bounded L. Arbitrarily slow decay and rigidity sequences are the obstruction. Simply replacing 'mixing' with 'weakly mixing' is unjustified.

**Research mechanism and first decisive test.** Seek a selected-length tensor-packing inequality using the dynamical structure of the Gram matrices, or a rank schedule adapted to sparse bad-pair graphs, that retains the dyadic summability. Test it first on rigid weakly mixing transformations; a statement allowing arbitrary sparse graphs may fail and must not be assumed. If this closes the weakly mixing case, formulate its conditional version over the maximal distal factor and run the selected-law/saturated-extension argument with conditional product laws. Pointwise convergence on distal systems is already available, making the conditional lift a concrete target rather than a new guess at the structured component.

The relative version is a significant second gap: unconditional convergence for weakly mixing systems alone does not automatically imply the theorem for extensions over distal factors. No unsupported general 'relative transfer principle' should be used.

**Primary background.** Huang–Shao–Ye, *Pointwise convergence of multiple ergodic averages and strictly ergodic models*, J. Anal. Math.139 (2019), 265–305, Theorem C for measure-distal systems: https://doi.org/10.1007/s11854-019-0061-3 . Austin, *Pleasant extensions retaining algebraic structure I*: https://doi.org/10.1007/s11854-015-0001-9 . Frantzikinakis's open-problems survey (general pointwise question): https://www.math.uoc.gr/~nikosf/OpenProblems/OpenProblems.pdf . Current search found no full arbitrary-system all-length resolution; this is a screen, not a complete priority audit.

## Higher absolute-impact but less-developed route: all-dimensional Kakeya

**Exact target.** Every Kakeya set in R^d has Hausdorff dimension d for every finite d. Impact estimate **9.5**. An all-dimensional maximal L^d theorem would be stronger, but it is a separate problem; do not infer it from Hausdorff dimension.

**New mechanism.** Local #074's four-dimensional proof uses weighted incidence laws, chart-comparison and finite-label recovery, extremal critical paths, three narrowness regimes, conditional scalar projections, and a horizontal finite-narrowness model. In the critical regime 2k=1, three successive trajectory changes fill the three-dimensional base; noncommuting horizontal directions enforce near-affineness. Read `Every-four-dimensional-Kakeya-set-has-full-Hausdorff-dimension-September-24-2026/build/sections/{01-introduction,08-critical-rates,10-consequences}.tex`.

**Real next test.** Rebuild the critical horizontal model in dimension five, classify the additional rank/anisotropy regimes, and determine whether a four-leg switched path has a quantitatively nondegenerate endpoint map on a four-dimensional base with the requisite mass/label budgets. A uniform induction would additionally need rank-stratified scalar-sheet rigidity and preservation of the original-resolution subpower label bounds across every dimension. These are proposed tests, not established lemmas. The old planar horizontal model does not automatically generalize.

**Why not my main recommendation.** The four-dimensional proof creates a credible new approach family, but its higher-dimensional rigidity/critical-rate mechanism is not yet identified; saying 'induct on dimension' would hide the main difficulty. The full pointwise ergodic route above has a more sharply isolated missing estimate and more transferable machinery, albeit slightly lower impact.

**Exclusions.** Projection of the four-dimensional theorem gives only dimension at least four in larger ambient dimensions. The release already includes its direction-set, segment-extension, constant-curvature Nikodym and rank-one quadratic curved-Kakeya corollaries. None is a new candidate. Current primary context: Guth, *The Kakeya conjecture, after Wang and Zahl*, April 2026, https://arxiv.org/abs/2604.03416 .

## Other exclusions

- General and symmetric Mahler, their equality cases, sharp functional forms and width-four symmetric polar products are already #087, so generic nonsymmetric-Mahler or polar-product proposals duplicate the release.
- Triangular universal optimality, Coulomb/Riesz renormalized minima and the spherical logarithmic linear term are already #090; the user also solved the first-batch surface consequences. Extending planar certification to three-dimensional crystallization lacks an identified transferable positivity mechanism and faces competing lattice phases; no blanket FCC universal-optimality conjecture should be asserted.
- Three-dimensional restriction, three-dimensional strict Bochner–Riesz and their stated Schrödinger local-smoothing consequences are already #077–078. Endpoint Carleson convergence in all dimensions is already #080.
