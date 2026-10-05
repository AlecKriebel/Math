# Independent full review: robustness 30004656

**PASS for all five stated partial results, with the separately frozen deterministic-chaining clarification included. The original problem remains unsolved, 5/5.**

This is an independent AI-assisted source and mathematical audit, not human peer review or a novelty certificate. It reads and checks all five proofs, not merely their summaries. One notation/quantifier clarification was requested and supplied additively; no other mathematical revision is required.

## 1. Immutable bindings

The original 35-file author packet is bound by FINAL_AUTHOR_MANIFEST.json SHA-256 1c50623aa192f334537774bc34eb71f58128c34b3ca0515996ca3e59e0190d5e, at WIP457bd908a974dc45bda952b71298dd1d345c25a1. Every original file was independently fetched and compared with the local bytes and Git blob SHA-1.

The required clarification has ADDITIVE_MANIFEST.json SHA-256 669e634c7d0e3ddac28d34f2f23a0aa916a6793d16bb47f02bb3965cb1261878. Its single bound file, ADDITIVE_CHAINING_CLARIFICATION.md, has SHA-256 41b00d9b3e388c8e0c96e9ab08fef39667898a16e9e21ecc063290a31c441f6b. Both files were fetched at corrected WIP07e33c276e4757773a844082d5f6003ebf124e7c. All37 corrected-tree blob IDs and sizes match; the original35 remain unchanged. REMOTE_BINDING.json records both bindings.

The full author replay is byte-exact: 329,914 assertions,60 historical/final bindings and six source files verified. Independent standard-library controls import no author code and pass91,084 exact assertions. These checks supplement the analytic review; no infinite probability claim is inferred from finite enumeration.

## 2. Exact source and hypothesis match

The original OWR contribution, printed862, was visually inspected. It points to the Bubeck--Li--Nagaraj paper rather than stating a deterministic theorem about every data set. The official EMS record confirms report year2021 and publication15March2022:
https://ems.press/journals/owr/articles/4990384 .

The published COLT2021 paper was read at its definitions, Conjecture1 and footnotes, and relevant lower-bound Theorems6,8 and9. Conjecture1 was visually checked on PDF page3. It concerns a fixed Lipschitz activation and arbitrary real weights and biases, independent spherical or normalized-Gaussian inputs, and independent random signs. The conjectural bound is sphere-restricted, and its probability is intentionally not numerically quantified. The matching upper construction is a different conjecture. Primary:
https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf .

The source's inclusion of Gaussian observations away from the sphere does not make a global Lipschitz proof into a sphere-restricted one. The author preserves that domain issue and makes no original resolution from it. The low-dimensional Gaussian partial explicitly uses a global/domain-appropriate norm. The growing-dimensional spherical partials explicitly use the sphere norm.

The original projection and polynomial/spectral results are credited. The official Wu--Huang--Zhang publication confirms the authors and its polynomial-weight restriction:
https://proceedings.mlr.press/v202/wu23g.html .
The Bubeck--Sellke primary abstract likewise retains polynomial-size weights in its broad parameterized theorem:
https://arxiv.org/abs/2105.12806 .
The Shmalo2026 preprint was checked for its stated piecewise-linear, dimension and logarithmic scope, and its projection discussion. Its full claimed theorem is not recertified here or used as an unaudited premise of the author's proofs:
https://arxiv.org/abs/2607.07778v1 .

No bounded-activation, bounded-weight, fixed-dimension or special-network result is promoted to the original arbitrary-parameter/activation statement.

## 3. Turn1: circle interpolation and the exact distribution

The deterministic optimum is the maximum label difference divided by sample distance; the McShane finite minimum attains it among all real functions. That does not assert width-constrained neural attainment. The least opposite-label circular separation equals the smallest marked cyclic gap: the shorter arc of any opposite-label pair must cross a flip edge, and the minimum marked gap is at most1/J<=1/2. Thus the chord formula is correct.

Rooting at one of the sampled points, not at a deterministic origin, yields Dirichlet(1,...,1) spacings after rotating that point to zero. The independent labels remain independent of this order and the spacings. The parity-conditioned binomial flip count has the stated coefficient and atom at J=0. Translating the j marked coordinates gives the simplex survival power n-1, with no spacing-independence assumption.

The CDF uses the correct monotonicity between T and1/sin(pi T), includes the all-equal-label atom at zero, and has no spurious atom at one. The n=2 case is consistent. The Chernoff and survival estimates imply the displayed n^2/log n floor with the stated failure probabilities. Its event is independent of the eventual interpolant. This is a fixed-circle geometric theorem, not a contradiction of separated high-dimensional smooth interpolation.

## 4. Turn2: chart collisions and dimension scope

The injective Lipschitz chart and the lower/upper density bounds give the stated cell mass and diameter estimates. An opposite-label cell enforces the Lipschitz floor on any domain containing the two collision points. Poisson sign/cell splitting gives independent cells with mean np_j/4 for each sign. The lower bound (1-exp(-x))^2>=x^2/4 on[0,1] and the product bound yield the exponent64.

The de-Poissonization direction is correct: if the n-sample has no opposite-label cell and N<=n, the N-sample has none either. This gives an upper bound on the n-sample no-collision probability without conditioning on N=n. The rounding bound and sufficiently-large-n restrictions are retained, as are the dimension-dependent constants.

The sphere chart stays on the actual prediction domain and has the stated Jacobian and derivative bounds. For fixed spherical d<=4, the geometric power beats sqrt(n); for fixed Gaussian d<=3 the analogous claim concerns the global/domain-appropriate norm. Nothing is asserted uniformly in growing d. The exceptional d=5 logarithm and width comparison are correctly scoped. The finite equal-cell inclusion-exclusion formula independently matches direct occupancy counting.

## 5. Turn3: adaptive projection and sphere fibers

The lifted points lie on the sphere, and rationalizing their last coordinates gives the2/sqrt3 Lipschitz bridge for projected points of norm at most1/2. It is valid for nonsmooth functions and does not estimate the sphere norm through an off-sphere segment.

The spherical even-moment calculation gives the exponential moment bound. The fixed1/4-net event controls the empirical covariance operator before a projection is chosen. The arithmetic n>=8d makes its failure probability at most exp(-n/4). Taking trace against any later rank-r projection gives the simultaneous bound, so an adaptive span does not require a new uncountable union bound.

The counts of inaccurate and high-projection observations, the disjoint opposite-label pairs, and the projected energy sum have the correct factors. At least n/4 good pairs remain in the small-rank case. Rank zero is excluded by the empirical variance of the labels, and the large-rank case uses a direct opposite-label pair, including r=d where the fiber lift is unavailable. The numerical constant covers both regimes.

The neural conclusion is a sqrt(d/k) floor, with the affine-skip rank adjustment explicit. It has the requested sqrt(n/k) order only when n/d is bounded. Biases and data-dependent nonlinearities do not change the projection factorization, but the missing n/d factor is not hidden.

## 6. Turn4: independent-row ReLU and deterministic chaining

Full row rank makes every strict activation pattern, including the empty pattern, occur on an open cone. The empty pattern supplies a network-dependent sphere point at which the homogeneous part vanishes. Sphere Lipschitzness then bounds its absolute sphere values by2L, and the radial decomposition proves the global bound G<=3L. This is a genuine domain bridge, not an assumed equivalence of norms.

The gradient on every open cone is the corresponding subset sum. Bounding complementary subset gradients and averaging the squared signed sum proves the coefficient-energy bound36L^2. It would fail as an inference for dependent rows; exact cancellation controls confirm why that restriction matters. Hidden biases would destroy this homogeneity argument and are expressly excluded.

For the stochastic bound, labels are fixed first, and z_i=y_i-bar(y) satisfy sum z_i=0 and sum z_i^2<=n. Rotational invariance centers increments between unit directions. Their absolute value is bounded by a one-dimensional spherical projection. Independent-copy symmetrization and the even-moment series give the stated subgaussian constant. For the single-direction base value, apply Jensen directly to A-EA and compare A with an independent A': E exp(t(A-EA))<=E exp(t(A-A')), whose2m-th moment is at most2^(2m)E|A|^(2m). This gives the same constant without incorrectly bounding a centered ReLU by the uncentered projection. The deterministic mean cancels in the z-weighted sum.

**Required clarification.** The frozen text reused u_0 for the chaining base point, although Section1's empty-pattern u_0 can depend on the network. The additive clarification fixes S_0={e_1}, replaces the Section2 base-point occurrences accordingly, and fixes every net before inputs and labels. That is the interpretation required for this PASS. The Section1 vector is unrelated to the probability construction. No bound or author turn changes.

With that correction, all possible approximating links have the stated lengths and cardinality bounds. The union estimates are summable, the process is continuous and separable, and telescoping gives a uniform event over every direction. The centered-label correlation removes the output constant and combines with coefficient energy to give the claimed sqrt(n/k) bound. The event is independent of the chosen network. Its displayed probability need not be strong for fixed small d, which the theorem explicitly acknowledges.

## 7. Turn5: spectral spread, balanced data and quadratic scope

The actual sphere Lipschitz constant of x^T A x is the spectral spread, not the raw operator norm. Subtracting the midpoint scalar proves the upper bound, and a great-circle tangent through the extreme eigenspaces proves equality. Antipodal even/odd parts then bound both spectral spread and the linear slope by L. The low-rank zero eigenvalue and full-rank scalar-shift nuclear estimates are correctly distinguished.

Selecting equal numbers of each sign depends only on labels. Conditional on the labels, the selected inputs remain independent uniform sphere points. The signed matrix is exactly trace zero; this permits removal of radial constants. Its scalar centered-moment series, two Chernoff regimes and net constants are valid. The vector concentration bound is separate and also uniform in the balanced sign sequence. All coefficient matrices and slopes can therefore be chosen after seeing the data.

The full-sample error bound controls the selected correlation through Cauchy--Schwarz. The output constant cancels, and one of the matrix or vector terms is large. Both rank regimes imply the final constant after N>=3n/4. The same event controls every k. No bound on parameter magnitudes is used.

Quadratic activation itself is not globally Lipschitz. The fixed quadratic-core activation supplied by the author is2-Lipschitz and realizes every stated quadratic-neuron representation on the sphere after rescaling. This establishes only the core-realized subclass, not arbitrary networks with that activation outside the core. Likewise the theorem covers rank-bounded quadratics, not all Lipschitz activations. These restrictions are prominent and mathematically necessary to the proof.

## 8. Disposition

Approve the complete scoped packet, including both additive files, as original **unsolved5/5**. Fixed-dimensional geometric floors, adaptive-rank floors, independent bias-free ReLU networks and rank-bounded quadratics do not jointly cover the general growing-dimensional arbitrary-activation/parameter target. No further author search occurred in this review.

The accompanying portable verifier binds the original and additive manifests, all37 remote blob IDs, the full author replay and the independent controls. SOURCE_BINDINGS.json records the separately verified local source files. Raw sources are not part of this public review bundle.
