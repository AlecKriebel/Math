# Independent adversarial audit: rank 663 / 4000018

## Verdict

**ACCEPT the seven precisely scoped results. Retain UNSOLVED, with five substantive approaches completed. No mandatory mathematical correction identified.**

This is an independent AI mathematical audit of the frozen authored packet, not human peer review, a formal proof-assistant certificate, a novelty determination, or a complete resolution of Ollivier's open-ended Problem R. In particular, the verdict does not certify that no later paper resolves any interpretation of that problem.

Reviewed archive: `rank663-4000018-authored-packet.zip`, 26,133 bytes, SHA256 `82f9acc92840eaef8ad85c7473817ed3eca5107ba4c851aaabd23c874eb2714e`. Review date: 2026-10-04 UTC. The originals were preserved. No helper agents or remote writes were used.

## Integrity and reproducibility

- Independently matched the archive hash and byte count.
- Verified all 12 internal SHA256SUMS entries and all 11 author-manifest file sizes and hashes.
- Ran the frozen author program without its mutation flag. All 28,156 assertions passed, and parsed output matched the frozen CONTROL_RESULT.json exactly.
- Wrote a separate standard-library-only audit program. All 52,820 independent exact assertions passed.
- Independently retrieved all four complete primary PDFs. Every source hash, byte count, and page count matched the frozen source metadata. The relevant statements, hypotheses, and formula normalizations were checked. Four key pages were rendered and visually inspected.
- No scholarly PDF, extracted source text, source-page image, catalog contents, private correspondence, or private coordination record is in this portable audit bundle.

The two control programs provide finite corroboration. The analytic arguments, universal quantifiers, and external theorem applicability were also reviewed below; a large assertion count does not replace that review.

## Claim-by-claim review

### C1. Reset process: correct

The proposed coupling has the exact source and target marginals. For ordered times, write a = exp(-2s), b = exp(-2t). Its three components have masses b, 1-a, and a-b, all nonnegative; they move x to y, match the common reference measure, and move x to the remaining reference mass. Its cost is at most b r + (a-b)D.

For 0 <= s <= t <= 1/4, the gap A = exp(-s)-exp(-2t) is at least (2t-s)/2. The gap B = exp(-2s)-exp(-2t) is at most 2(t-s). Writing u = sqrt(s), v = sqrt(t), the potentially delicate polynomial inequality has the exact remainder

4(2t-s) - (u+v)^2 = (v-u)(7v+5u) >= 0.

Consequently B^2 <= 32 A(v-u)^2, and the asserted AM-GM argument gives A r + 8D^2(v-u)^2/r >= BD for every r > 0. This proves the stated constant 16D^2, including s=0. Equal times are covered separately. Reversing time order also exchanges the spatial labels, so symmetry handles all ordered pairs. No evaluation at r=0 is required.

The semigroup, invariance, reversibility, compact-space Feller property, and exact equal-time distance are correct. The latter follows from the distance-to-y Lipschitz test without needing an unproved equality case in transport duality. The claim does not assume strong Feller regularization, locality, or an intrinsic metric-generator relation.

### C2. Reset BE profile: correct

With g = f - integral(f) and V = integral(g^2), direct generator algebra gives Gamma = V+g^2 and Gamma2 = 3V+g^2. Thus the BE residual is

(3-K)V + (1-K-4/N)g^2.

For K <= 1-4/N both coefficients are nonnegative. For K above this threshold, indicator tests on positive-measure sets with arbitrarily small mass give a negative residual on a positive-measure set. Atomlessness supplies these sets. The same limit with 1/N=0 gives optimal infinite-dimensional curvature 1.

The continuous tent calculation has the correct mean, variance, and finite-dimension obstruction. Since the residual is continuous and strictly negative at zero for sufficiently small tent width, its failure extends to a positive-measure neighborhood. The bounded generator's domain on C([0,1]) includes these tests.

The qualification about lower curvature is indispensable and is correctly retained: at every K<1, N >= 4/(1-K) is sufficient. The result concerns BE(1,N), not absence of every finite BE pair.

### C3. Geometric dimension: correct

Normalized Euclidean cubes have diameter one and unchanged Hausdorff dimension n. They are compact geodesic spaces with full-support atomless probability measure. All reset hypotheses hold uniformly in n.

For the stated Hilbert cube, 3 times the squared tail after coordinate m equals 4^(-m), giving uniform tail control and total diameter one. Finite-dimensional compactness plus that tail bound gives compactness. Convexity yields geodesics. Product measure has full support by controlling finitely many coordinates and making the deterministic tail smaller than the remaining ball radius. Each finite coordinate subcube is bi-Lipschitz to an n-dimensional box, so Hausdorff dimension is infinite.

This refutes a dimension bound in the expressly stated broad class. It does not refute a theorem restricted to canonical strongly local heat flow, an intrinsic metric, RCD heat flow, or smooth Brownian motion.

### C4. Finite-dimensional heat flow: correct, conditional on its hypotheses

The EKS v2 displayed W2 expansion formula, time parameter, and coefficient agree with equation (10). The introduction's stale proposition reference is correctly replaced by the actual body Proposition 2.22. The proof uses the valid direction W1 <= W2.

For s <= t, tau-2s = (2/3)(sqrt(t)-sqrt(s))(sqrt(t)+2sqrt(s)) >= 0. For K>0, the exponential quotient is at most one. Linearizing the square root at the positive number exp(-Ks)r then gives the coefficient N exp(Ks)/r, bounded by N exp(KT)/r. Therefore C = 2N exp(KT) is valid. Neither a reverse W1-to-W2 implication nor an unproved equality of optimal constants appears.

The independent Kuwada route is also correct: the denominator in alpha is at least exp(Ks) times its numerator, and the weight is at most sqrt(N/(2r)). Integration yields J <= sqrt(2N)(sqrt(t)-sqrt(s)). The complete smooth diffusion assumptions, N>=m convention, and prohibition of nonzero drift at N=m match the cited theorem.

The endpoint extension needs moment continuity as stated. The small-horizon conclusion proves admissibility for each C>2N, and only an infimum bound at 2N. The half-Laplacian rescaling and K=0 statement are correct.

### C5. Scaling: correct

Time acceleration multiplies kappa and C by the same factor and divides the horizon by it. Metric dilation multiplies W1 and spatial distance by b, hence C by b^2. Generator acceleration multiplies Gamma by a and Gamma2 by a^2, so it preserves the BE dimension parameter while multiplying curvature by a. Upward closure of admissible C and N is correctly qualified. These facts block an unnormalized identification and do not block normalized relations.

### C6. Brownian calibration: correct

The common-Gaussian coupling gives W2 squared equal to r^2+nq^2; the covariance Cauchy-Schwarz bound proves the reverse inequality. Square-root linearization gives C<=n.

For a Dirac initial endpoint, W1 is the expectation of a norm. Its Hessian at a nonzero point has trace (n-1)/r. Localization away from the origin and Gaussian tails justify the first-order expectation expansion, giving C>=n-1 for every positive horizon. In dimension one, choosing r=sqrt(t) yields a strictly positive lower bound because a centered Gaussian shifted by one still has positive probability of being negative. Thus the tempting universal replacement C=n-1 is indeed false on the line. No claim of optimality for the whole bracket is made.

### C7. Ornstein-Uhlenbeck obstruction: correct

The transition mean, covariance, Gamma, and Gamma2 use the same generator normalization. Equal-time laws are translates and have the asserted exact W1 distance. At fixed unequal positive times and fixed initial separation, sending the common initial location to infinity makes the mean difference diverge, while the proposed right-hand side stays fixed. This excludes every finite C, every real kappa, and every positive horizon.

The linear-coordinate BE witness is valid; a local smooth cutoff gives the same pointwise derivatives if a compactly supported test domain is required. The obstruction is compatible with the finite-N sufficient result because finite BE dimension at the stated curvature is absent.

## Source assumptions and status

The original [Problem R](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf) concerns T1/W1. The label L2 must not be read as changing the displayed transport distance. The short statement asks for a relationship rather than specifying one precise equivalence.

The relevant [Ollivier theorem](https://www.yann-ollivier.org/rech/publs/curvmarkov.pdf), Proposition 52, has epsilon-geodesicity, an annular spatial assumption, small-time uniformity, the restriction epsilon <= (1/2)sqrt(C/(2kappa)), and additive diameter correction 4 pi epsilon. The packet records these correctly. Passing to an uncorrected bound requires arbitrarily fine admissible scales with fixed constants. Its Brownian normalization and n-versus-(n-1) caution are also retained.

[EKS v2](https://arxiv.org/pdf/1303.4382v2) is applied to canonical RCD* heat flow with finite N and finite-second-moment inputs. The source's Hilbertian and regularity distinctions are preserved. [Kuwada v2](https://arxiv.org/pdf/1308.5471v2) provides the alternative finite-dimensional route; the packet preserves its differentiability, strong Feller, reference-measure/geodesic assumptions where needed. Neither source authorizes replacing these conditions with arbitrary W1 contraction.

The five approaches are mathematically distinct: normalization, positive finite-dimensional transfer, Gaussian calibration, the drift obstruction, and the nonlocal reset construction. Counting them does not count source reconstruction or script assertions as extra approaches. Keeping the original target unresolved is justified by the explicit remaining canonical and sharp-constant questions. Literature checking was bounded; absence of a search hit is not a proof of absence.

## Additional adversarial boundary result

The packet already says kappa=1 is not the reset process's optimal equal-time curvature. The following independent check shows why that distinction cannot be removed.

On the unit interval with uniform reference measure, choose x=0, y=r with 0<r<1/2, and 0<s<t. Direct integration of the CDF difference gives

W1 = exp(-2s)r + [exp(-2s)-exp(-2t)](1/2-r).

Set t=s+h for fixed positive s. The excess above exp(-2s)r has positive first-order coefficient 2 exp(-2s)(1/2-r)h. If kappa were changed to 2, the proposed correction C(sqrt(s+h)-sqrt(s))^2/(2r) would be only order h^2. Therefore no finite C works at kappa=2 on any positive horizon. This is a boundary supplement, not a correction to the audited claims, which use kappa=1.

The independent controls also explicitly reject reversing W1<=W2 and reject the false statement that this reset generator has no finite BE dimension at any curvature.

## Reproduce

Run the frozen author's program from its extracted authored directory to reproduce 28,156 assertions. Run `python3 independent_checks.py` in this portable audit directory to reproduce 52,820 assertions. No package installation, network, credentials, source PDFs, or private input is needed for the latter. AUDIT_BINDING.json binds the reviewed input; SOURCE_RECHECK.json records public source verification metadata; AUDIT_RESULT.json records the decision. The frozen author files were not revised by this audit.
