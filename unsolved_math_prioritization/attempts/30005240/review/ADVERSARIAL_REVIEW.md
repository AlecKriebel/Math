# Independent adversarial review: 30005240

**Review date:** 2026-10-02.  
**Verdict:** PASS for the five scoped mathematical results **with the additive rank correction applied**.  
**Original problem disposition:** unsolved, exhausted5/5. No full actual-density theorem or physical counterexample has been established. This is independent AI mathematical review, not human peer review or formal proof-assistant certification. Historical priority is not certified.

## 1. Frozen objects and correction

The original author packet has46 files. Its `FINAL_AUTHOR_MANIFEST.json`, SHA256 `2791a4f342f256ce032c6b8b16c6577267f19453074608e5fca77322add10c9e`, binds the other45. All45 entries, including every turn proof and historical manifest, were checked against their exact bytes. The original checkpoint is commit `cc420a4aceceaee76f38cbb81711059e9a511936` on `dot/math-30005240`.

One mandatory localized correction was found in TURN_5 §5: the displayed compact clock operator has **rank L**, not L+1. Only coordinates1,…,L of the input are used, and output coordinates L−1 and L coincide. Conversely, output coordinates0,…,L−1 versus input coordinates1,…,L form sigma times the identity, giving the lower bound L. This does not change its compactness, spectrum, norm, exact iterates, summability, or countermodel conclusion.

The author preserved every original byte and added `REVIEW_CORRECTION_1.md`, SHA256 `491b2e9cbe7c5c6cec1168ac2629c9fbb221de214482bf5f0f5c503a8403753f`. Its three-file correction manifest has SHA256 `c44adf11a49e3a394735c0a9550b66b8b44231206aeb83e590500c29b99d1af4`. Those bindings and the supplementary checker were verified. The combined50-file author/correction checkpoint is `568b552dde64f40a0376e6df697359343d95d115`. This review applies to the original freeze **read together with that correction**, not to the uncorrected rank sentence in isolation. The correction is proof review, not a sixth author search.

## 2. Exact primary-source audit

The entire relevant Ecevit contribution in [OWR43/2022](https://ems.press/content/serial-article-files/46980), printed2545–2548, was read. The printed two-period expression on2547 was independently inspected visually. The target concerns periodic high-frequency convergence rates for actual multiple-scattering densities; fixed-reflection expansions are already part of the background. The phase convention and the restriction to illuminated regions cannot be omitted. The adjacent question about summing collective returns and infinite tails is distinct.

The [Ecevit–Reitich primary manuscript](https://www.researchgate.net/publication/225156275_Analysis_of_multiple_scattering_iterations_for_high-frequency_scattering_problems_I_The_two-dimensional_case) was independently opened. Its Assumption C specifies the nonplanar incident-wave expansion input. Corollary4.1 explicitly requires the remainder ratios to be controlled independently of reflection count. The numerical discussion expressly describes the whole-boundary transfer as heuristic. The earlier [MPI137/2006 version](https://files-www.mis.mpg.de/mpi-typo3/preprints/2006/preprint2006_137.pdf) was separately read at the recurrence, illumination, amplitude, phase and conditional-current estimates. Its numbering is not silently identified with published pagination.

The [Iantchenko source](https://arxiv.org/abs/math/0702022) explicitly defines the boundary return through outgoing single-obstacle solution operators and relates scattering poles to I−M. Its resonance sign convention and additional analytic/nonresonance hypotheses were checked. It does not directly supply the pointwise high-frequency quotient and excitation bounds needed here. The [Neumann expansion paper](https://arxiv.org/abs/2208.06257) is used as fixed-iteration background, without upgrading it to the missing all-return result.

All five retained primary PDFs match their recorded hashes. The full source list and correction bindings are in `SOURCE_AND_CORRECTION_BINDINGS.json`. Third-party PDF bytes are not reproduced in this review packet.

## 3. Turn1: source shortcut, phase and limit exchange

At a normal two-bounce orbit, the source recurrence indeed reduces to L0=2a−1/L1 and L1=2b−1/L0, with a,b>1. Setting A=ab and P=L0L1 gives P²+(2−4A)P+1=0. The admissible root is (sqrt(A)+sqrt(A−1))², hence q=sqrt(A)−sqrt(A−1). The printed shortcut instead corresponds to P_print=A+sqrt(A(A−1)), and its nonzero residual is computed correctly. The earlier manuscript recurrence and the printed product were both visually checked. The paraxial calculation in Turn4 supplies an independent consistency check. This validates an algebraic discrepancy in the simplification, not a proof that the physical densities have a particular asymptotic rate.

The full complex multiplier requires exp(2ikd) in the selected outgoing convention. The exact quotient perturbation identity and its constant follow from the stated nonvanishing lower bound and one-period increment bound. The logarithmic reflection threshold makes the available optical phase error O(1/k); a fixed reflection count does not do so. The two-mode example is positive, uniformly summable, and agrees to all algebraic high-frequency orders at each fixed iterate, while its eventual quotient is controlled by the larger mode. Its stated limitation as an abstract example is essential and is preserved.

## 4. Turn2: same-space dominant-mode theorem

The weighted-composition conjugation is valid on the stated Lipschitz Banach space. Compactness of X and positivity of a give a bounded Lipschitz logarithm, and contraction of F makes the logarithmic product converge uniformly with a Lipschitz reciprocal. Multiplication is bounded in the anchored norm.

The constant/B0 splitting is an exact l1 decomposition. Each perturbation block inherits the stated epsilon bound. The disc centered at1 of radius2epsilon stays outside the D0 norm ball; the Schur map has the stated invariant-disc and q² contraction bounds. The fixed-point construction gives both left and right eigenvectors, with normalization d0 bounded away from zero. Parameterizing the complementary invariant subspace by J gives D0−cbR and the claimed beta bound. The factor2 in the all-power remainder estimate is valid for q≤1/13.

The excitation condition supplies a uniform lower bound for the observed projected mode; it cannot be dropped. The denominator and numerator estimates yield the factor96, and the explicit k and j thresholds imply the final (2KC+3lambda)/k bound. These arguments remain valid with complex blocks because only norm estimates and the resolvent identity are used. Independent controls include genuinely nontriangular examples with both couplings nonzero.

The translation example correctly shows why a derivative-losing fixed-function expansion does not imply the needed same-space operator-norm approximation. The strong-norm approximation and physical excitation remain unproved for the Helmholtz return; the theorem does not claim otherwise.

## 5. Turn3: analytic Gaussian model

Schwarz's lemma gives the composition contraction on the vanishing-at-zero subspace. The nonvanishing weight has a holomorphic logarithm on a disc neighborhood, and the infinite product and reciprocal are bounded. The analytic interior margin delta is positive throughout each averaging segment.

The normalized Gaussian is centered. Integration by parts gives the stated second and fourth moments; Cauchy's estimates and Taylor's integral remainder yield a genuine O(h) operator estimate in the same H-infinity norm. The conversion to the split norm costs at most3. The variance-replacement bound is valid: the relevant elementary maximum is3sqrt(3)/e<3. The fourth-order remainder and both norm conversions give the stated C2. The first multiplier correction is gamma=(v²/2)g''(0); the off-diagonal Schur contribution is correctly second order.

The ratio theorem uses all the original smallness and excitation assumptions. The example f_h=g supplies nonempty admissible data. This is a complete theorem for the expressly defined analytic Gaussian operator. No contour deformation, physical kernel representation, or extension from smooth to analytic obstacle geometry has been established, and none is claimed.

## 6. Turn4: exact physical reduction and observation

At fixed real frequency, separated boundaries permit interior elliptic regularity across the receiving boundary. The cross-trace maps are smoothing; compact Sobolev inclusion gives compactness of M. These are frequency-dependent bounds. Combining the smoothing with the own-boundary Dirichlet-to-Neumann map gives the stated smooth observation B.

The two Dirichlet reflection signs cancel in f_(j+1)=A12A21 f_j. The total current on the return obstacle is exactly B M^j f0, with B=D1M−N12A21. Thus the reduction includes the single-obstacle solves and is genuinely physical at fixed frequency.

The exclusion of eigenvalue1 is justified by exterior uniqueness followed by gluing the common outgoing field through the first obstacle. For a nonzero eigenvalue mu, smoothness of the eigenvector permits the boundary Cauchy-uniqueness argument: zero Dirichlet and Neumann traces on an open patch allow extension by zero and interior unique continuation. Connectedness of the common exterior propagates this, and the trace on the second obstacle forces a contradiction. Hence Bv is nonzero on a dense open boundary set, without a global or frequency-uniform lower bound.

Given an algebraically simple dominant eigenvalue and excitation, the resolvent-circle power estimate has the correct factor r/(2pi). The current quotient estimate follows with the stated denominator threshold. The high-frequency polynomial-loss assumption then gives the advertised logarithmic threshold and constant. None of simplicity, the uniform spectral gap, the optical eigenvalue approximation, or the observation/excitation loss is deduced from compactness.

The paraxial matrix has determinant1 and trace4A−2, confirming the corrected two-bounce magnitude. The resonance sign translation is consistent. The two abstract matrix families have identical resonance-zero sets but different dominant real-frequency iteration modes; this is a valid logical countermodel, not a scattering construction.

## 7. Turn5: diagonal and growth-envelope scope

The source's fixed-iteration relative expansion is used only with its geometric and incident-wave assumptions. On a fixed compact subset of stabilized illumination, the limiting incidence factor is bounded away from zero; the amplitude ratios and ray-phase increments then have the stated geometric bounds. The normal-incidence sign cancels in each return amplitude ratio.

The diagonal thresholds control the finite set of indices through2l+1, which correctly covers both numerator and denominator throughout l≤j≤2l. The bound Ca theta^l+4Q/(l+2) gives actual-density modulus and exact-ray-phase convergence on that window. Thresholds can be increased to keep the window below any prescribed diverging nondecreasing function. This supplies no lower reflection-growth bound and does not establish an arbitrary slowly diverging window.

Replacing the exact increment by the limiting periodic phase introduces k theta^j, which the slow diagonal does not control. Under the additional exponential envelope, the chosen c and tau balance the two errors correctly, including the ceiling and the next-iterate applicability condition. Failure of that balance when sigma≥a is a limitation of this sufficient method, not a physical impossibility theorem.

With the rank correction from §1, the clock family has all the claimed remaining properties. Its single nonzero eigenvalue is simple, its norm is sigma, and direct iteration gives the exact optical transient followed by the sigma quotient. It is a fixed-space family of compact operators with frequency-dependent transient length; its piecewise frequency dependence is explicitly disclosed. It demonstrates the insufficiency of the specified abstract hypotheses without asserting a physical counterexample.

## 8. Controls, integrity and disposition

- All45 entries of the original author manifest were verified. The original five checkers replayed byte-identically: **139,156 exact assertions**. The replay procedure separately verifies32 historical manifest entries.
- The additive correction's bindings were verified and its **338,550 exact checks** replayed byte-identically.
- Independently written code in this review passed **24,641 exact rational checks**: continued-fraction/shortcut identities, unequal-curvature paraxial matrices, nontriangular Schur decompositions and quotient constants, an independent clock-rank elimination, explicit diagonal windows with very rapidly growing fixed-index constants, and the logarithmic envelope exponents. It imports no author checker.

Finite controls supplement the proof audit and do not establish any absent physical hypothesis. No further mandatory correction was found after applying the additive note.

**Recommended QUEUE disposition: unsolved5/5.** The sharp gap remains uniform physical high-frequency remainder or full-return spectral control, together with incident-data excitation and observation/denominator estimates on the required region. A whole-boundary theorem also needs shadow/transition and zero control. The two-dimensional/two-obstacle reductions do not settle general periods or the three-dimensional variant. Preserve all partial proofs, source qualifications, this review, the rank correction, and the exhausted author count. Do not promote the source shortcut correction, analytic model, conditional spectral theorem, or slow diagonal to a solution of the original target.
