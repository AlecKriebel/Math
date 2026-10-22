# Independent full scoped review: 30006017 / OWR-14298589-002

## Verdict and binding

**PASS for the complete scoped five-turn packet. Original disposition: UNSOLVED, 5/5 substantive author turns. No mandatory mathematical correction.**

The author freeze contains46 files, with final manifest SHA256 `b906861fd73389bc37e60b347f737740595273a5710027a641c8eae5b25c20c2`. All45 bound files plus the manifest were verified locally, and all46 were read back byte-exact from author head `20e0b89358d665bd6052ee18a31507227a8cfac4` on `dot/math-30006017`. All32 historical manifest entries and all five author checker receipts replay exactly.

This is an independent AI-assisted mathematical audit, not formal verification, human peer review, or historical novelty certification. It audited the full source scope, all five proof files, cited theorem hypotheses and relevant proof passages, finite verification scripts, geometric construction, and final disposition. It did not extend the unfinished author search.

The original problem asks for a centered limiting law of areas of conditional-uniform flat disks sampled from standard planar Brownian-bridge side increments. This packet does not prove that law or give a counterexample. Its continuum functional theorem is rigorous within its own stated model, with pre-existing tree results explicitly credited. A finite uniform-disk area representation or quantitative transfer remains missing.

## 1. Source normalization and actual finite ensemble

The complete OWR contribution and the relevant author slides agree on the Brownian increment ensemble and on intrinsic area with multiplicity. The imported short statement's omitted normalization is properly restored. It is not used to manufacture a rescaling counterexample. The report/slide mean and (n-2)! enumeration are explicit credited inputs; their in-preparation source manuscript was not located, so this review does not claim to have independently checked an unpublished full proof of those inputs.

For a simply connected translation disk, developing coordinates are globally defined up to translation. Stokes computes intrinsic area from the oriented boundary, retaining multiplicity. The possible multiple fillings affect their weight but not the area of a fixed oriented boundary. Rooting at one designated distinct side selects one representative of each cyclic order; there is no missing factor n. Conditional exchangeability gives (n-1)! orders, while the source counts (n-2)! fillings, producing exactly the factor n-1 in the annealed multiplicity tilt.

The isotropic Gaussian input, before selecting its disk filling, separates into a uniform direction and an independent radius in real dimension2(n-1). Its energy law is (2/n)Gamma(n-1,1). Dilation preserves the conditional uniform filling law, so the radius remains independent of the selected unit-energy shape. This does not say the selected boundary direction itself has the unweighted sphere law. The L1 removal bound E[A_n]/sqrt(n-1) correctly uses independence and the credited logarithmic mean; it establishes equivalence of centered convergence questions without proving tightness of the shape variable.

The discrete Fourier identity has coefficient cot(pi p/n)/4. The increments form a proper complex Gaussian vector, so opposite Fourier modes need not be conjugates: the two coordinate bridges are independent. Pairing their exponential quadratic terms gives the stated characteristic function and variance. The ordinary bridge signed area is tight without logarithmic centering, so it cannot replace the filling-tilted law. The positive-definite affine covariance scaling is det(Sigma)^(1/2), as stated.

## 2. Excursion layers and conditional Gaussian centering

The positive-length superlevel intervals form a measurable laminar family. Cutoff measure is finite; the component-length layer cake gives integral s dnu=integral e. The exact bridge increment covariance is overlap minus the product of lengths. Gaussian interpolation gives the absolute-width covariance bound used in the proof, including negative increment correlations and degenerate limits.

The nested-pair estimate counts at most one ancestor per level, with total ancestor measure bounded by excursion height H; disjoint pairs contribute at most the product of component lengths. The resulting2H T_epsilon+T_epsilon^2 bound is integrable for a fixed continuous excursion and is uniform in the lower cutoff. It proves the conditional L2 Cauchy claim. The modulus-of-continuity estimate follows by integrating over levels within omega_e(epsilon) of e(t), not by an unwarranted independence assertion. Random-excursion L2 convergence uses a valid H^2 domination; the Brownian-excursion height bound follows from the credited three-bridge representation.

The bounded-variation folded-area identity has the stated negative signed orientation before reversal. Its Stieltjes/Fubini use is confined to continuous bounded-variation paths. Brownian widths are defined by interval increments rather than an unjustified classical pathwise Stokes integral.

## 3. Critical tree input and Abel renormalization

The published Fill--Janson version expressly distinguishes the meromorphic uncentered Y from the centered analytic family Y_tilde. Theorem1.3 supplies joint moment continuity under the extra offspring moment condition; Poisson(1), or a bounded admissible auxiliary law, meets it. Remark1.27/(1.41) and its Section8 proof give a measurable same-excursion realization including alpha=1/2. Hence the author's analytic matching and L2 limit use the same excursion, rather than only equality of unrelated one-dimensional distributions.

The factor of two is correct: the source's Y(alpha) is twice the author's layer functional F_e(alpha) when Re alpha>1. The integer-moment argument recovers the finite expected measure s E[nu_e], yielding density1/sqrt(8pi) times s^(-1/2)(1-s)^(-1/2). Division on positive lengths is legitimate. This gives the exact width mean1/(2pi z) under Abel weighting and the stated residual constant -log(2)/sqrt(2pi).

The residual is H-dominated, and the weighted centered-width covariance is dominated by the already established finite laminar covariance integral. These justify the L2 Abel limit and conditional orthogonality of its two components. Independence of those components is not claimed. The positive random-measure example correctly refutes a general Abel-to-sharp inference even with exact mean and bounded variance; it is explicitly outside the source disk law.

## 4. The consequential sharp-cutoff transfer

Janson's Theorem6.7/(6.24) does have a toll-independent constant and a sum of toll second-moment square roots divided by k. Thus it applies to the n-dependent size-band toll. The bound on the sum is epsilon^alpha/alpha for0<alpha<=1, and normalization by2sqrt(n) cancels the outer sqrt(n) factor. No hidden n-dependent constant is introduced.

The weighted finite-measure convergence is adequately justified by contour moment convergence and compact polynomial approximation. One can check the normalization directly: add one auxiliary root edge and let k_v be the fringe sizes. Across its unit-height edge layer, the normalized contour component length is (k_v-u)/n for0<u<1. Thus the scaled continuous alpha-moment is proportional to sum_v integral_0^1((k_v-u)/n)^alpha du, whereas J_n uses sum_v(k_v/n)^alpha. For fixed integer alpha>=1 their difference after multiplication by2sqrt(n) is at most alpha. At alpha=1 it is exactly1/2. The auxiliary root edge is an O(n^(-1/2)) height change. This confirms both the limiting moment statement and the factor1/2 independently of a probabilistic simulation.

The zeroth moment is total mass and has uniformly bounded second moments from the credited alpha=1 moment result. Fixed positive cutoff points have zero limit mass by the mean intensity density. Therefore bounded band integrands converge in law, and their means converge by uniform integrability. Lower semicontinuity of the centered second moment then transfers the variance inequality; full second-moment convergence for a discontinuous band function is not assumed.

At alpha=1/2 the uniform band bound is precisely enough to make sharp-centered cutoffs L2-Cauchy with O(sqrt(epsilon)) norm error. Abel averaging identifies that limit with the same centered critical tree functional. This direction uses the established sharp convergence, not the invalid general reverse inference. At alpha=1, monotone convergence plus the uniform variance/mean bounds gives E[T_epsilon^2]=O(epsilon). The residual-mean error is O(epsilon), and the Gaussian fluctuation norm error is O(epsilon^(1/4)); hence the stated complete continuum sharp-cutoff theorem and its rate follow.

Nothing in this passage couples the auxiliary Poisson conditioned trees to the finite source disks. Their role is to prove a theorem about the specified Brownian excursion functional. Equality of leading logarithmic means does not establish A_n-W_(1/n) convergence or identify its deterministic constant. The final packet retains exactly this missing finite-model step.

## 5. Flat-disk discontinuity construction

The quadrilateral chain is a strip with two distinct radial cut edges; it is not closed into an annulus. Its intrinsic vertices remain distinct when their developed coordinates repeat. The triangulated complex has one boundary cycle, every vertex link is a boundary interval, and Euler characteristic one. Shared interior edges have opposite directed incidences and positive triangles on opposite sides. Thus there are no hidden interior cone singularities.

The area, energy and matrix formulas count all sheets and both radial sides. Scaling to energy2 preserves the stated different positive area limits while developed boundaries uniformly collapse. This refutes a general continuity claim under the stated weak boundary/quadratic conditions. It does not show nonconvergence for the source ensemble, nor rule out a stronger almost-sure continuity or quantitative transfer theorem at its particular random boundary limit.

Positivity of the finitely many oriented triangles is open in all boundary coordinates modulo translation. Those coordinates are linearly equivalent to ordered zero-sum sides. Every forbidden genericity determinant is a nonzero polynomial on that space, by the given three-index witness. The finite union of their zero sets cannot fill the open positive-orientation neighborhood. Rational generic perturbations therefore exist, and the O(N delta_N) area/energy estimates preserve the limits after renormalization. Selecting these special disks says nothing about their conditional-uniform Gaussian probabilities.

## Replays and independent controls

- All46 author files and32 historical manifest entries verify
- All five author receipts replay byte-exact: **244,308 exact assertions**
- The independently written checker imports no author verification code and passes **132,813 exact assertions**
- It checks contour/fringe identities and normalization on all626 rooted plane trees through eight vertices; abstract strip topology, vertex links and exact geometry; and two actual rational perturbed disks, verifying all111,960 relevant genericity determinants across them
- It also checks independent exact closed-walk and affine-area identities
- **224 floating-point Fourier diagnostics** pass a stated numerical tolerance; these are nonrigorous diagnostics, separately counted and not a proof dependency

All infinite-dimensional conclusions depend on the audited written arguments and credited theorems, not on these finite controls. The scope and dependency qualifications in RESULT.md are consistent with the proofs.

## Final recommendation

Publish as a reviewed unresolved five-turn partial result, with both the actual-ensemble reductions and the separate continuum theorem labeled accurately. Preserve source credits, the restored Brownian normalization, report year2024 versus actual publication14February2025, and the corrigendum-access limitation. Keep source PDFs/images/raw imports outside the public packet. Do not label the deterministic disks or abstract measures counterexamples to the original probabilistic statement, or claim its limiting law is U+C. No sixth author search is warranted by this review.
