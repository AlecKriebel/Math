# Analysis, geometry, dynamics, quantum, physics and biology overlap audit

Catalogue snapshot: OpenAI `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. This is a scope/relationship comparison, not certification of either repository’s proofs. Claims below describe what the pinned catalogue or manuscript asserts. Our open/draft PR scope comes from `sources/open_prs.json`; current main work and retained no-PR branches are included where materially relevant. Fifteen selected matches are ranked approximately by directness, with explicit non-implications.

## 1. Family 149: [Classwise permanence for weakly reversible mass-action systems](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/permanence.pdf)

**Relation:** Close, same deterministic network class; different theorem from stochastic recurrence.

**Our work:** Our [single-linkage bimolecular stochastic recurrence package](../../bimolecular_positive_recurrence_submission_v1_2_4/README.md), [Turing decision program](../../qbio_mass_action_turing_topology_phase3/README.md), [stable Turing patterns](../../maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/CLAIM_LEDGER.md), [reversible realization framework](../../reversible_mass_action_realization_theory/README.md), and `codex/weakly-reversible-continuum` at `0a21e84a288bf41c41b2ced8f83050469a9c3336`.

**Precise comparison:** The source claims classwise permanence of the deterministic ODE xdot = sum k x^y (y′−y) for every finite weakly reversible fixed-positive-rate network, with arbitrary molecularity and linkage count. Every positive stoichiometric class has one compact convex forward-invariant absorbing set. This is directly relevant literature for all our deterministic mass-action projects. It does not establish positive recurrence or nonexplosion of the discrete stochastic reaction chain: deterministic concentrations and integer-valued jump populations are different state/process models. Our recurrence theorem assumes one linkage class and molecularity at most two; its stochastic conclusion is not implied by the stated deterministic theorem. Our compact equilibrium ellipse and diffusion-driven instability can coexist with permanence, which asserts neither uniqueness of equilibria nor absence of spatial instability. Single-linkage deterministic permanence is explicitly credited in their introduction to earlier work; the advertised new scope is arbitrary weakly reversible networks/classwise bounds.

**Verification boundary:** Primary manuscript introduction, including Theorem 1 and historical-scope comparison, was read at the pinned commit. No proof audit or stochastic bridge was performed.

## 2. Family 156: [Borsuk's conjecture fails in dimension nine](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/paper.pdf)

**Relation:** Same named conjecture; dimension boundary prevents subsumption.

**Our work:** Our [four-dimensional Borsuk program](../../borsuk_dimension4/README.md); archival [PR #8](https://github.com/AlecKriebel/Math/pull/8).

**Precise comparison:** They claim a compact counterexample in R^9, the trace-one rank-one real 4×4 orthogonal projectors with Frobenius distance, requiring more than ten smaller-diameter pieces. Our target asks whether every bounded subset of R^4 admits five such pieces. The fact that their projectors are indexed by lines in R^4 does not put the diameter example in Euclidean R^4: symmetric 4×4 trace-one matrices occupy an affine nine-dimensional space. The construction is relevant to low-dimensional Borsuk research and orthogonality/diameter graph mechanisms, but leaves our dimension-four question open.

**Verification boundary:** Catalogue abstract compared to our exact scope and diameter-certificate acceptance criteria; construction proof was not audited.

## 3. Family 360: [Weak MTW curvature gives convexity and regular optimal transport](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Global-Support-and-Convex-Injectivity-Domains-under-Weak-MTW-September-25-2026/paper.pdf)

**Relation:** Shared A3w hypothesis; our desired stronger implication remains distinct.

**Our work:** Open draft [PR #400: 30000997, reviewed partial MTW separation](https://github.com/AlecKriebel/Math/pull/400), branch `dot/math-30000997`, snapshot `e6472b7b2276d74670c94df193ec2cae4c247c3f`.

**Precise comparison:** They claim weak MTW/A3w on closed smooth connected Riemannian manifolds implies convex tangent injectivity domains, including conjugate cut points, plus global support and bi-Hölder optimal transport with positive upper/lower density bounds. Our draft asks whether global A3w forces nonnegative full cross-curvature on all direction pairs; it retains the candidate sphere/global-A3w gap. Their introduction expressly imposes curvature only for orthogonal direction pairs and does not claim nonnegative cross-curvature on nonorthogonal pairs. Convexity and regular transport are useful neighboring consequences, but do not answer our stronger implication as stated.

**Verification boundary:** Primary introduction/Theorem 1 and the explicit orthogonality convention were read; no comparison of the detailed proofs was attempted.

## 4. Family 147: [The near-boundary Birkhoff conjecture](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Continuous-Phase-Foliations-Create-Analytic-Caustic-Collars-September-24-2026/paper.pdf)

**Relation:** Elliptic billiard setting; rigidity rather than individual periodic-orbit identities.

**Our work:** Open draft [PR #205: odd-period focal-pedal k601](https://github.com/AlecKriebel/Math/pull/205), the elliptical-billiard drafts [#147](https://github.com/AlecKriebel/Math/pull/147), [#148](https://github.com/AlecKriebel/Math/pull/148), and [#140](https://github.com/AlecKriebel/Math/pull/140).

**Precise comparison:** They claim a smooth strictly convex billiard of positive curvature must be an ellipse when an entire grazing annulus is continuously foliated by individually invariant curves, or when a full boundary collar has smooth convex caustics. Our drafts start with an ellipse and prove or refute exact focal/pedal/area invariants for specified periodic orbits and caustics. Their table-rigidity result does not supply those orbit identities, counterexamples, parity conventions, or focal formulas. It is strong relevant background for why confocal elliptical dynamics are distinguished.

**Verification boundary:** Catalogue statements only; the complete foliation hypotheses must be preserved, and no general Birkhoff conjecture claim is inferred beyond that collar.

## 5. Family 150: [Weak mixing of triangular billiards with an irrational angle](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Weak-mixing-of-triangular-billiards-with-an-irrational-angle-October-5-2026/weak-mixing-triangular-billiards.pdf)

**Relation:** Polygonal billiards; global statistical conclusion versus local finite-trajectory relations.

**Our work:** Open drafts [PR #152: sine ratio for short polygon trajectories](https://github.com/AlecKriebel/Math/pull/152), [#191: signed parallel-trajectory type rule](https://github.com/AlecKriebel/Math/pull/191), and [#190: parity-aware parallel rule](https://github.com/AlecKriebel/Math/pull/190).

**Precise comparison:** They claim weak mixing of the unit-speed billiard flow for every triangle with at least one angle irrational relative to pi. Our polygonal-trajectory results are exact geometric relations for finite labelled paths; they neither assume nor conclude typical-orbit ergodicity or weak mixing. The source therefore gives relevant triangular dynamics background and could matter for future statistical use of our identities, but does not replace them. It also does not answer our constant-width billiard draft #471, which has a different geometry and normal-moment question.

**Verification boundary:** Catalogue abstracts and our draft bodies were compared; no weak-mixing proof audit or extension to general polygons is claimed.

## 6. Family 266: [Exactly three mutually unbiased bases in dimension six](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf)

**Relation:** MUB structure is relevant to Bell recipes; cardinality result does not settle Bell-setting minimality.

**Our work:** Our [cyclic Bell exact values/randomness manuscript](../../cyclic_bell_exact_values_and_randomness/README.md), especially its private-MUB composition lemma and computational-MUB exposure obstruction; [minimum Bell randomness program](../../minimum_bell_randomness/CLAIMS_LEDGER.md).

**Precise comparison:** They claim exactly three mutually unbiased bases in C^6, with a separately described computer-assisted four-basis exclusion. Our work supplies a sufficient private-reference/MUB composition criterion and restrictions on exposing a common computational MUB through separately bounded Bell terms. A bound on how many pairwise MUBs exist does not prove purification-stable privacy, Bell self-testing, uniqueness of a maximizing behavior, or the minimum number of measurement inputs. Their result would constrain designs specifically requiring four MUBs in dimension six; three available MUBs do not by themselves satisfy our private-MUB hypotheses.

**Verification boundary:** Catalogue source explicitly makes the upper bound conditional on its arithmetic/compiler verification conditions. The certified computation was not rerun. Our source lemma and scoped obstruction wording were checked.

## 7. Family 272: [Entanglement without distillable secret key](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/paper.pdf)

**Relation:** Bound entanglement/privacy connection; PPT construction does not resolve NPT Werner target.

**Our work:** Our [NPT Werner-state distillability research program](../../werner_npt_bound_entanglement/README.md); Bell randomness/privacy program [README](../../cyclic_bell_exact_values_and_randomness/README.md).

**Precise comparison:** They claim an entangled 10×10 PPT-derived state with zero distillable secret key for their specified local-instrument protocols, plus a trace-preserving PPT channel on M_21 whose square is not entanglement breaking. Our Werner question is all-copy two-block positivity for X_(alpha,d) = I + alpha d P_d in the NPT interval −1/2 ≤ alpha < −1/d. Their state is PPT, so it is outside this NPT Werner family; no finite-copy Schmidt-rank-two witness or all-copy NPT-undistillability conclusion follows. Distillable secret key is also a different operational resource from singlet distillability and Bell-value randomness. The exact protocol/reference compatibility model is material to the source claim.

**Verification boundary:** Primary introduction, protocol qualifications, PPT-map construction and theorem statements were read. No operational-protocol proof audit or comparison to unrestricted alternative models was performed.

## 8. Family 277: [Threshold repetition for entangled games](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/paper.pdf)

**Relation:** Same finite-dimensional entangled-game framework; statistical repetition rather than one-shot equality structure.

**Our work:** Our [cyclic Bell operator manuscript](../../cyclic_bell_exact_values_and_randomness/README.md), [two-setting qubit POVM–PVM closure](../../two_setting_qubit_povm_pvm_equivalence/README.md), and [Lalonde quantum coloring package](../../lalonde20_quantum_coloring/README.md).

**Precise comparison:** They claim exponential upper tails for achieving a win fraction above v+delta in k independently repeated finite two-player games, allowing joint finite-dimensional entangled strategies and correlated single-round question laws. Our papers determine particular one-shot Bell values, maximizing behaviors, minimum measurement architectures or exact finite-graph quantum chromatic numbers. Repetition takes v as an input and supplies neither the value/equality classification nor a Bell-randomness certificate. Their theorem is potentially useful after a Bell expression is converted to a bounded win-probability game, but that conversion and any application are not established here. The source is finite-dimensional; our cyclic values also compare approximate and commuting models.

**Verification boundary:** Catalogue abstract and our README scopes only. No commuting-operator repetition extension, robustness/self-testing result, or new randomness inference is claimed.

## 9. Family 291: [Cuntz comparison and Jiang–Su absorption](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Cuntz-comparison-and-Jiang-Su-absorption-September-23-2026/paper.pdf)

**Relation:** Same absorption theme; a potential restricted route requires additional hypotheses.

**Our work:** Open draft [PR #797: Jiang–Su stability, corrected partial results](https://github.com/AlecKriebel/Math/pull/797), exact [current README](https://github.com/AlecKriebel/Math/blob/0d48332f8a882e408a0aaf665fa9415fc0edcd50/unsolved_math_prioritization/attempts/30002218/README.md).

**Precise comparison:** The source claims that a separable nuclear C*-algebra absorbs Z whenever its Cuntz semigroup is almost unperforated and fully almost divisible. It also states simple-algebra strict-comparison and nuclear-dimension variants; those separate hypotheses should not be conflated. Our accepted corrected theorem has common-unit unital A,B in B(H), A Z-stable, and distance below 1/16000000; it yields complete distance below 1/42 and an isomorphism of scaled Cuntz semigroups. Its stated assumptions do not include separability or nuclearity. Consequently the advertised source criterion does not resolve the general perturbation target. There is a potentially useful restricted consequence if the target B is separable nuclear, A's Z-stability gives both precise source semigroup properties, and the transferred scaled-Cu isomorphism preserves them. Those property/hypothesis bridges were not proved by this scoping task, so this remains a candidate conditional route, not an established new implication. The source's amenable-action theorem starts with an already Z-stable algebra and is not a theorem that ordinary algebra closeness forces absorption.

**Verification boundary:** Read the exact #797 primary README and its accepted scope; read the OpenAI catalogue's separate Cu, nuclear-dimension and equivariant abstracts. No primary source proof/theorem-definition audit of fully almost divisible, perturbative nuclearity transfer, or new absorption derivation was performed. The general target retains both nonnuclear/nonseparable and non-common-unit/nonunital gaps.

## 10. Family 351: [Scalar curvature and finite-time Ricci-flow singularities](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-closed-Ricci-flow-with-bounded-scalar-curvature-and-finite-time-curvature-blowup-September-24-2026/paper.pdf)

**Relation:** Ricci flow family; extension question distinct from our pointwise cone-preservation equivalence.

**Our work:** Open draft [PR #779: 30001006, Ricci PDE/ODE bridge](https://github.com/AlecKriebel/Math/pull/779), with local curvature-pinching investigations identified in its body.

**Precise comparison:** They claim bounded scalar curvature forces finite-time extension for closed real four-manifold Ricci flows, and provide a sufficiently high-dimensional counterexample to unrestricted extension. Our draft equates Hamilton-ODE preservation of scal(R) ≥ d ||W(R)|| with preservation for all closed n-manifold Ricci flows for n≥4, realizing every ODE failure by a compact metric. The source treats singularity extension under a scalar bound; our target classifies preservation of a stronger pointwise scalar/Weyl cone, including the unresolved n_0=12 threshold/global Weyl-cubic extremum. Neither of the advertised extension statements determines that cone threshold.

**Verification boundary:** Catalogue abstract and our draft body only. High-dimensional source examples were not checked for the cone condition, so no counterexample to our cone conjecture is inferred.

## 11. Family 371: [Stable blowup for the defocusing Schrödinger equation](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Stable-Self-Similar-Blowup-for-a-Supercritical-Defocusing-Schrodinger-Equation-on-the-Torus-September-24-2026/paper.pdf)

**Relation:** NLS shared subject; equations and regimes differ sharply.

**Our work:** Open drafts [PR #829: graph quadratic NLS/resonance](https://github.com/AlecKriebel/Math/pull/829) and [#93: resonant stochastic NLS model separation](https://github.com/AlecKriebel/Math/pull/93).

**Precise comparison:** They claim stable finite-time blowup for sufficiently large odd-power scalar defocusing NLS on the twelve-dimensional torus, with initial data in H^k and k>8. Our #829 concerns quadratic NLS on a necklace metric graph with Kirchhoff domains, product compatibility and 1:2 resonance obstructing a corrector under its stated rescaling; #93 concerns a stochastic resonant system with bath/generator specification gaps. Their high-dimensional deterministic supercritical blowup theorem neither answers our wave-packet approximation/continuation question nor settles the stochastic recurrence/smoothness/NESS question. It is related PDE background, not a direct logical conflict.

**Verification boundary:** Catalogue statement versus draft bodies; no adaptation of the blowup mechanism or global-existence inference across models.

## 12. Family 365: [Joint metric and connection recovery from one boundary patch](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf)

**Relation:** Smooth inverse-recovery theme; observational models are different.

**Our work:** Our merged [PR #302: smooth fixed-lag spectral diffusion tensor consistency](https://github.com/AlecKriebel/Math/pull/302), current [accepted result](../../unsolved_math_prioritization/attempts/30003508/CURRENT_RESULT.md), and retained branch `dot/math-30003508` at `152882a5cfb85f09635d131db83c1e19118f4c98`.

**Precise comparison:** They claim recovery of a smooth metric and smooth rank-two unitary connection from zero-frequency boundary measurements on one open patch, modulo patch-fixed diffeomorphism/gauge; a companion supplies indistinguishable bounded measurable scalar conductivities. Our result consistently estimates a smooth unknown anisotropic diffusion tensor and stationary density from exact stationary reflecting-diffusion positions at fixed positive lag on a known domain. Both solve inverse coefficient-identification problems using elliptic/spectral structure, but boundary DN-type data and statistical path observations are different experiments. Their theorem does not give our estimator, sampling consistency or rates, and the rough-coefficient nonuniqueness example is outside our smooth model. Our latest local accepted result supersedes the old pending-review branch README.

**Verification boundary:** Catalogue source and current accepted local theorem were compared. No attempt to reconstruct boundary data from samples or conversely was made.

## 13. Family 262: [Sharp finite-matrix Lieb–Thirring inequalities and all equality cases](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Equality-cases-in-the-sharp-one-dimensional-matrix-Lieb-Thirring-inequality-October-5-2026/sharp-one-dimensional-lieb-thirring-inequalities-matrix-potentials.pdf)

**Relation:** Spectral extremal inequalities; Schrödinger/matrix one-dimensional result distinct from Dirac threshold target.

**Our work:** Open draft [PR #745: 30005664, Dirac threshold partials](https://github.com/AlecKriebel/Math/pull/745).

**Precise comparison:** They claim sharp one-dimensional finite-matrix Lieb–Thirring bounds for 1/2<gamma<3/2 and classify equality cases as constant-unitary direct sums of scalar sech² solitons. Our draft seeks a global reverse inequality/optimal threshold-potential norm for Dirac operators in dimensions d≥2. It retains exact candidate branches, scalar upper-component Schur forms, domain restrictions, and the distinction between Schur-form sharpness and a full-Dirac spectral gap. The operator, spatial dimension, exponent and quantity optimized all differ. Matrix potential sharpness/equality structure is relevant methodological literature, but there is no established route from this source to the missing Dirac optimality bound.

**Verification boundary:** Catalogue abstract and our carefully qualified draft body; no Dirac-to-Schrödinger bridge or equality transfer was proved.

## 14. Family 213: [Critical percolation on every quasi-transitive graph](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Critical-bond-and-site-percolation-on-the-cubic-lattice-September-24-2026/paper.pdf)

**Relation:** Independent critical percolation versus dependent finite-energy/FGK models.

**Our work:** Open drafts [PR #838: finite-energy percolation with internal threshold one](https://github.com/AlecKriebel/Math/pull/838), [#837: half-plane FKG percolation partials](https://github.com/AlecKriebel/Math/pull/837), and [#112: inverse-square long-range ordinary-end correction](https://github.com/AlecKriebel/Math/pull/112).

**Precise comparison:** They claim no infinite cluster for critical independent Bernoulli bond percolation on any connected locally finite quasi-transitive graph with p_c<1. Our #838 constructs a dependent translation-mixing lattice bond law with ordinary nonuniform finite energy and an infinite cluster whose internal Bernoulli p_c equals one. Independence is absent in the outer law, and p_c<1 is explicitly absent for its internal graph, so it is not a counterexample to their theorem. Our #837 retains a half-plane survival question under dependent FKG/finite energy; the claimed independent criticality theorem does not supply its missing existence implication. #112 uses a long-range inverse-square model, whose ambient complete countable graph is not locally finite. Family 214 is an additional nearby result for independent Bernoulli percolation on nonamenable quasi-transitive graphs, but does not remove these hypothesis gaps.

**Verification boundary:** Catalogue abstracts and draft bodies compared. No full percolation proof audit or inference from finite energy to Bernoulli independence.

## 15. Family 377: [Interior $`C^{1,\alpha}`$ regularity for infinity-harmonic functions](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Uniform-Interior-C1alpha-Estimates-for-Infinity-Harmonic-Functions-October-4-2026/interior-c1-infinity-harmonic.pdf)

**Relation:** Infinity-Laplacian topic; local and fractional operators must remain separate.

**Our work:** Open draft [PR #796: 30002288, fractional infinity eigenfunction representation partial](https://github.com/AlecKriebel/Math/pull/796).

**Precise comparison:** They claim interior C^(1,alpha_d) regularity for bounded local infinity-harmonic functions in dimension d≥3, with a nonexplicit alpha_d>0 and no boundary claim. Our draft refutes an unweighted ridge-subset representation for whole-space zero-exterior fractional infinity-eigenfunctions using finite positive weighted maxima, for every fixed 0<alpha≤1, while finite-p maximal selection remains unresolved. Local infinity-harmonic regularity and nonlocal fractional infinity-eigenfunction representation are different equations and boundary settings. The source neither proves our proposed representation nor contradicts the nonsmooth weighted-max examples without an operator-equivalence argument, which is not present.

**Verification boundary:** Catalogue and draft body only. This is a useful neighboring-area match and false-positive warning, not the same problem.

## Coverage notes and negative findings

- Family 280 (strongly rational unitary VOAs/conformal nets) gives braided categorical context for the exceptional YBE localization program, but does not advertise an explicit exceptional local operator, faithful localization or minimal local dimension. This is background only.
- No catalogue entry was located that resolves our exact cyclic Bell operator value/equality problem, two-setting qubit POVM–PVM minimum architecture, Lalonde G19 quantum-coloring theorem, exceptional YBE local operator/minimum dimension, or all-copy NPT Werner distillability. The quantum matches above are neighboring results, not those resolutions. This is a bounded catalogue comparison, not an exhaustive global literature search.
- No obvious direct catalogue overlap was located for the phylogenetic JC/K2P/K3P/LGT identifiability programs. Family 229 (tree broadcasting reconstruction thresholds) is adjacent probabilistic biology/information theory, but should not be described as generic algebraic network identifiability. A separate algebra/probability agent may cover it.
- Family 372 (smooth isotropic elasticity inverse uniqueness) and draft #132 (nonlinear forward elastic-equilibrium uniqueness under identical constant minor multipliers) share elasticity vocabulary but solve different problems. Do not report the former as resolving the latter.
- Family 212 (planar nearest-neighbor FPP shape/bigeodesics) is related to draft #173 (growing-seed two-type FPP on random configuration graphs) and #169 (optimal-path shape edges in a correlated product environment), but their models and conclusions differ; no implication was established.
- The compact equilibrium ellipse on no-PR branch `codex/weakly-reversible-continuum` was confirmed by reading its README directly via `git show`, without checkout or Git mutations. Reversible realization’s local README independently records the compact-conic scope.
- Sources inspected for family 149, 272 and 360 were the pinned primary manuscript introduction/theorem sections. Catalogue abstracts were used for all other OpenAI rows, with our project README/manuscript portions or PR bodies. Passing code/review labels from either repo are not treated here as theorem certificates.
- No external contact, messaging, repository writes outside this agent folder, branch switch, commit or push was performed.
