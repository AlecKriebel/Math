# Independent audit of Function Theory 6.31

## Verdict

**PASS as a rigorously delimited partial-results package. The original problem remains unsolved in this package, with the five substantive approaches exhausted.** No blocking mathematical correction was found. This is a fresh audit of the stated analytic arguments, not a sixth attempt to solve the general problem and not a formal proof certificate.

The main restricted-class theorem is valid as stated: for normalized holomorphic f with Re((1-z)^2 f'(z))>0, the assumed radial power remainder implies O(n^(-delta)) for 0<delta<1 and O(log(n)/n) for delta>=1. Symmetry of the representing measure yields O(n^(-min(delta,1))). The exactly univalent rational example with delta=2 and error 1/(2n) is valid. Neither result supplies an improved rate for every f in S, and neither proves logarithmic sharpness.

Audit date: 2026-10-04 UTC. Auditor: independent task audit_quantitative_hayman_regularity. No helper tasks were used. No remote writes were performed. Frozen author files were not changed.

## Frozen input and reproducibility

Input directory: ../public.

- SHA256SUMS.json SHA-256: 9ab04885a8047744a57fa36e383cad8da80ff6148d2cbdb6d1b44625571aaae3.
- FULL_PROOF.md SHA-256: c7489ad57ca50abf958aaa52695e54e78333d5c96672d637b0a13a8bd2a7cbe0.
- The author manifest verifier passed all 10 listed files.
- FROZEN_INPUT_HASHES.json records all 11 actual input files, including the manifest itself.
- The author control function was replayed by runpy under a non-main name and then run() was called. This avoids the script's main-block write to CONTROL_RESULTS.json. Its returned object exactly equals the frozen control result: 369 exact rational checks, 10,752 kernel checks, and 768 positive-real-part samples.
- independent_checks.py is independently authored and imports no author implementation. Its exact polynomial identities cover the cleared-denominator kernel formula; its independent Laurent multiplication checks the Fejer identity. High-precision tests include angles absent from the original grid.

The final integrity check confirms that every frozen input byte remains unchanged. The audit manifest covers this audit's authored reports, results and scripts, not the third-party source files.

## Statement and source fidelity

The target is correctly transcribed from [Hayman and Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), Problem and Update 6.31, printed pp.128-129, one-based PDF pages 129-130. Both target page images were inspected, the text was checked, and the chapter's definition of S was checked at printed p.114. The private PDF's SHA-256 is 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0, matching the author's source manifest.

The source concerns the complex radial value, not merely its modulus, with nonzero lambda and positive delta. It reports Duren's logarithmic coefficient estimate and asks for its improvement. Its no-progress update is historical; it does not certify the literature's status in 2026.

[Duren's publisher record](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms/s2-8.2.279) independently confirms the title, July 1974 publication, volume s2-8, pages 279-282 and DOI. Full access to the institutional PDF was not obtained during this audit. The exact target and quoted background theorem remain supported by the checked Hayman-Lingham statement. The audit does not certify Duren's complete original proof.

The live catalogue URL was inaccessible through the web reader. Focused searches of the exact paper title, Problem 6.31/Duren, and univalent Tauberian-remainder rate terminology produced no verified later resolution. This is a bounded corroboration, not an exhaustive citation search or a current-open-status certificate. No novelty is certified. The author's historical repository/duplicate-search observations were not rerun as part of this analytic audit, and are not independently certified here.

## Detailed mathematical audit

Line references below refer to the frozen FULL_PROOF.md.

### 1. Normalization and radial exponent cap, lines 7-24

Since f has a simple zero at zero, B=(1-z)^2 f/z is holomorphic on D with B(0)=1. The coefficient of z^n in kB is sum_{j=0}^{n-1}(n-j)b_j. Division by n gives equation (1), including n=1. Equivalently, it is the average of the first n partial sums of B.

With s=1-r, B(r)=(lambda+O(s^delta))/r=lambda+O(s)+O(s^delta), using r bounded away from zero near the endpoint. Thus epsilon=min(delta,1) is justified. The division by r prevents retaining an exponent greater than one without additional cancellation. The package explicitly states this limitation and does not introduce a uniform-in-f bound.

### 2. Nonunivalent obstruction, lines 28-46

The power expansion of z^2/(1+z)^2 gives coefficient (-1)^(n-2)(n-1) for n>=2, so the claimed alternating normalized coefficients are correct. Multiplication by (1-r)^2 gives radial limit one with an O(1-r) error. Direct differentiation gives the displayed numerator. Its values at -1 and 0 are -16u and 1. Its zero is strictly inside (-1,0), where the denominator is nonzero. A holomorphic injective function cannot have an interior critical point. This example is correctly excluded from S; there is no false counterexample claim.

### 3. Conditional angular transfer, lines 54-76

Cauchy's formula on r=1-1/n yields the stated integral bound for n>=2. Here (1-1/n)^(-n)<=4. On [-pi,pi], 1-cos(t)>=2t^2/pi^2 and r>=1/2 imply the lower bound for |1-r exp(it)|^2.

For 0<eta<1, the rescaled integral of (1+v^2)^(-1+eta/2) converges and contributes O(n^(1-eta)). At eta=1 the integral is O(log n). For 1<eta<2, the integrable singularity away from the cutoff contributes O(1); the central interval contributes O(n^(1-eta)). For eta>=2 one uses the upper bound |1-z|<=2 rather than reversing a negative-exponent inequality. All three coefficient conclusions follow after division by n.

The all-disk assumption is expressly additional. No radial-to-angular inference appears in the proof. The proposition is true without univalence and is not a general-S theorem.

### 4. Weighted moments, lines 82-106

The positive moment M_s implies absolute summability, so L is defined and the radial limit follows by dominated convergence. Splitting the exact coefficient error at j=n gives two terms whose multipliers are bounded by (j/n)^s for 0<s<=1. This proves the claimed constant M_s without a missing factor.

For s=1, adding M/n leaves exactly n^(-1) sum_{j>=n}(j-n)b_j. Its bound by n^(-1) sum_{j>=n}j|b_j| is o(1/n). The Abel estimate uses 1-r^j<=min(1,j(1-r))<=j^s(1-r)^s. Finally, multiplying by r adds an O(1-r) term, which is harmless for s<=1. The criterion is only sufficient; the package never derives it from the original radial condition.

### 5. Exact admissible obstruction, lines 110-131

For 0<c<=1, w=1/(1-z) maps D onto Re(w)>1/2, and

    f_c = c w^2 + (1-2c)w + c-1.

If two distinct w values had equal images, c(w_1+w_2)+1-2c would vanish. Its real part is strictly greater than 1-c>=0, a contradiction. The strict inequality also handles the endpoint c=1. Normalization holds directly.

The coefficient and radial expansions in equation (7) are exact. For c=1/2, f=((1-z)^(-2)-1)/2 has coefficients (n+1)/2 and radial expression 1/2-s^2/2. Thus delta=2, lambda=1/2, and a_n/n-lambda=1/(2n) exactly. This rules out universal o(1/n), including the delta=2 subcase. It does not establish any universal O(1/n) upper bound. It also does not claim an obstruction for every separately fixed delta>2.

The later C_0 membership assertion is valid: (1-z)^2 f'_c(z)=c(1+z)/(1-z)+(1-c), with strictly positive real part. Adding this one-line calculation is an optional readability improvement.

### 6. Positive-real-part representation, lines 141-149

The measures u(rho exp(i theta)) dtheta/(2pi) are positive probability measures by the mean-value property. Sequential weak compactness is applied on the unit circle, not on a half-open angular interval regarded as a noncompact topological space. For each fixed z, eventually rho>|z|; the Poisson kernels with parameter z/rho converge uniformly on the circle to the kernel at z. This justifies passage to the weak limit.

The integral's holomorphy follows from compact-subdisk bounds. Equality of real parts leaves an imaginary constant, removed by p(0)=1. Thus the normalizing mass and absence of an extra imaginary constant are correct. Angular endpoints are identified on the circle.

### 7. Starlike rigidity, lines 155-169

The argument uses the standard analytic characterization Re(z f'/f)>0 for normalized starlike univalent maps. Since f/z is nonvanishing, its analytic logarithm normalized to zero at the origin exists. Integrating the Herglotz kernel yields equation (10); compact-subdisk estimates justify interchange.

For T=log(1/(1-r)), the real logarithmic integrand divided by T is bounded between -log(2)/T and 1. For all sufficiently large T it has a fixed integrable bound. Its pointwise limit is the indicator of the zero-angle atom. A nonzero quadratic radial limit makes log|f(r)/r|/(2T) tend to one. The probability measure must therefore consist solely of that atom, forcing f=k and lambda=1. The fixed positive direction and the starlike restriction are both essential and are both retained.

### 8. Restricted class univalence, lines 175-203

For w=z/(1-z), the target half-plane Re(w)>-1/2 is convex. The inverse derivative is 1/(1+w)^2=(1-z)^2, so the transformed derivative F'(w) equals p(z), with no missing factor. The segment integral of F' has positive real part and therefore cannot vanish. This proves global injectivity; nonvanishing of f' alone would not suffice, but is not what the package uses.

### 9. Atom identification and positivity after subtraction, lines 205-238

The normalized p has a probability measure mu. Kernel integration reconstructs f because f(0)=0. On each compact subdisk all denominators have uniform lower bounds, justifying holomorphic integration and subsequent power series manipulations.

The bound s^2 |f_theta(r)|<=r<=1 follows because the radial majorant integrates to k(r). For every fixed nonzero circle angle the first Herglotz factor remains bounded on [0,1], so s^2 f_theta(r) tends to zero. At zero angle the limit is one. Dominated convergence therefore gives lambda=mu({0})=c in [0,1]; the nonzero assumption gives c>0. No derivative asymptotic is inferred by differentiating the radial hypothesis.

The measure nu=mu-c delta_0 is positive, finite and has no zero-angle atom. Since s^2 c k(1-s)=c(1-s), equation (15) has the correct positive cs term and the correct exponent cap.

For 0<s<1/4, |theta|<=s and t in [1-2s,1-s],

    |1-t exp(-i theta)|^2 = (1-t)^2+2t(1-cos theta)
                        <= 4s^2+theta^2,
    1-t^2 >= 1-t >= s,
    (1-t)^(-2) >= 1/(4s^2).

Hence the real integrand is at least 1/(20s^3). Integrating over an interval of length s and multiplying by s^2 gives the factor 1/20. The integrand's real part is nonnegative outside the restricted range, so discarding that portion is legitimate. Combining with the absolute O(s^epsilon) bound gives the local mass estimate. Positivity is an indispensable class-specific input.

### 10. Complex coefficient kernel and all-angle bound, lines 240-256

Expanding p/(1-z)^2 and then integrating gives

    n a_n = n + 2 sum_{j=1}^{n-1}(n-j) mu_hat(j),

and therefore equation (17). The triangular coefficients are nonnegative and sum to one after normalization, yielding |K_n|<=1 and K_n(0)=1.

Multiplying equation (18) by n^2(1-q)^2 gives the polynomial identity

    [n+2 sum_{j=1}^{n-1}(n-j)q^j](1-q)^2
       = n(1-q^2)-2q(1-q^n).

Its signs and n powers are correct, including n=1. For nd>=1 the displayed estimate is valid. For the complementary nd<1 case, d>=2|theta|/pi implies n|theta|<pi/2, so 3pi/(n|theta|)>6 and the minimum in (19) is one. Thus the omitted complementary sentence is immediate and the stated bound genuinely holds for every nonzero theta, not only for nd>=1. The value at theta=0 is handled separately.

Subtracting the c atom gives equation (20) with no unaccounted constant. Complex phases are bounded in modulus for the nonsymmetric case; positivity of Re(K_n) alone is not wrongly used to control its imaginary part.

### 11. Summation, endpoint and symmetry, lines 258-270

Choose a fixed R inside the range on which nu([-x,x])<=A x^epsilon is valid. For sufficiently large n, the central arc is bounded by A n^(-epsilon). Each full dyadic annulus within R gives at most a constant times n^(-epsilon)2^(j(epsilon-1)). There are O(log n) annuli. A final partial annulus can be included with the last full-scale estimate or with the region |theta|>=R/2. Outside that fixed arc the bound is O(1/n), since nu is finite.

For epsilon<1 the geometric sum is bounded independently of n, with constants allowed to depend on epsilon. At epsilon=1 it has O(log n) terms; there is no illicit summation of a divergent endpoint series and no claim of an epsilon-uniform constant.

Under circle-reflection symmetry, K_n(-theta)=conjugate(K_n(theta)) and the imaginary integral vanishes. The real part is the squared geometric sum divided by n^2, exactly as in (21). The symmetric dyadic ratio is 2^(epsilon-2), uniformly summable for each 0<epsilon<=1. The exterior arc is O(1/n^2). The case c=1 has nu=0 and zero remainder, and is covered. This proves all stated restricted rates.

## Independent controls and their limits

INDEPENDENT_CHECK_RESULTS.json records:

- 512 exact cleared-denominator kernel polynomial identities, including q=1 after clearing denominators.
- 16,384 exact Laurent-coefficient equalities for the Fejer identity.
- 1,044 exact rational-family checks.
- 116 high-precision kernel points at 120 decimal digits, with n up to 1,024 and nonzero angles down to 10^(-24), including both signs and angles at or near pi.
- 150 high-precision local lower-bound points, including s close to 1/4 and down to 10^(-24).

Maximum observed closed-form discrepancy: approximately 8.48e-76. Maximum observed Fejer discrepancy: approximately 1.37e-119. All assertions passed. The exact identities and analytic arguments above, rather than sampling, justify the infinite statements. Neither control set proves univalence, sharp asymptotics, novelty, or a full solution.

## Classification and action

Retain the mathematical status **unsolved**, the approach count **5/5**, and the explicit absence of a general-S improvement. Retain the author's qualifications about non-novelty, finite controls and bounded literature checks. Do not convert the C_0 theorem into a close-to-convex or all-univalent theorem.

There are no required proof corrections. CORRECTIONS.json lists only optional clarifications and a narrower replacement for the README's phrase “Sharp boundary example.” The frozen STATUS.json entry saying independent_audit is pending is a historical frozen field; this separate report supplies the completed audit without rewriting it.
