# Independent adversarial review: 30006020

## Verdict and exact version

**PASS_COMPLETE_SOURCE_TARGET.** The frozen candidate establishes its whole-multiset total-variation approximation, its Poisson point-process limit at every stated mesoscopic scale, and convergence of every fixed compact-window joint count moment. In particular, the original window [1/sqrt(g),2/sqrt(g)] has limiting Poisson law with mean (log 2)/2, and its mean and variance converge to that value.

This verdict binds CANDIDATE.md SHA256 `f1d43a7f4ae54e6c3ac8318cac8f2106b937d4657101bdd3a9b91523e0e5de4b` and author MANIFEST.json SHA256 `ac3784fed092db1c0f7e22b7434264939d3f4ce46afc47b7dddfaa37028f1803`. All 13 author artifacts and four pinned source PDFs match their supplied hashes. No mandatory mathematical or metadata correction was found. The reviewer did not contribute to the author route or modify any frozen author file. No novelty or priority is certified.

The conclusion retains the exact iterated N-then-g sampling law and principal holomorphic quadratic stratum. It concerns maximal horizontal cylinders, with the same vertical marginal by rotation. No joint horizontal/vertical independence, diagonal N(g) limit, all-directions count, primitive-cover restriction, height cutoff, or theorem for other strata is included.

## 1. Source match and geometric input

I checked the original OWR contribution and visually inspected printed p. 2387, including Problem 2 and the separate Problem 3. The requested mesoscopic interval and order of limits match the candidate. The surrounding theorem is explicitly for the principal quadratic stratum. The finite-area normalization is by the entire surface area, and the cylinder count is without multiplicity of its core curve.

The final Delecroix–Liu paper was checked at Theorems 1.4 and 3.2, the probability-mixture definitions, the simplex measure convention, equation (6.1), and Lemma 6.4 with its monomial-expansion proof. I visually checked printed pp. 5097, 5116 and 5117. The final DGZZ paper was checked at Theorems 1.7, 1.12 and 5.2 and its discussion of the negligible nonprincipal strata in the fixed-genus square-count limit. The key statements of Theorems 1.12 and 5.2 were visually checked.

The geometric identification and intersection-number estimates are substantial published inputs. The proof correctly derives the uniform whole-mixture comparison from positive coefficients, rather than treating DL Theorem 4.1's literal test-function statement as a quantitative total-variation theorem. Its use of DGZZ Theorem 5.2 is confined to the first, valid low-k range. No unrestricted large-k interpretation of later source statements is needed.

The original OWR microscopic summary's scale 4g−4 differs from the exact mixture's total Gamma parameter 6g−6. The candidate records that discrepancy and does not use the microscopic summary. Its mesoscopic conclusion is proved directly with n=3g−3 and total shape 2n; there is no hidden replacement of the requested window. The scale-invariant intensity also makes a fixed rescaling irrelevant to the displayed mesoscopic mean, but this observation is not used to certify an unproved microscopic statement.

## 2. Mixture coefficients and automorphisms

The stable graph has one vertex of genus g−k and k loops. Its unlabeled graph automorphism factor is 2^k k!. Summing unrestricted positive heights produces zeta(2j), rather than imposing height one or a primitive-cover condition. Integrating the positive monomial with exponent 2j−1 changes the denominator (2j)! into the factor 1/(2j). The resulting conditional distribution is Dirichlet(2j_1,...,2j_k), with total shape 2n.

I independently reconstructed the candidate's A_(g,k) from the source polynomial and then divided by 2^k. The resulting D_(g,k) and its exact consecutive ratio agree. In the range k=O(log g), the ratio is 1+O((k+1)/g), uniformly. Multiplying the ratios introduces O((log g)^2/g), hence no surviving k-dependent tilt.

The coefficient uniformity also survives replacing the source genus by g−k: this remains asymptotic to g, while 2k is logarithmic. The degree constraint is correct because sum(j_i−1)=3g−3−k. Positivity permits comparison of the latent composition masses before normalization. Normalizing only changes their common 1+o(1) bounds, and applying the shared Dirichlet kernel or forgetting labels cannot increase total variation. Thus the Radon–Nikodym comparison genuinely controls every nonnegative measurable statistic on the good event, including g-dependent windows.

## 3. Exceptional events and unbounded moments

The cutoff 0.6 log(2n) lies strictly within DGZZ Theorem 5.2's first range. Its separating contribution is at most a logarithmic factor times g^(-1+0.6 log 2), which is polynomially small. The fixed t=1.1 probability-generating bound from Theorem 1.12 gives the separate upper-count tail, with exponent

    0.6 log(1.1) - 0.05 > 1/220 > 0.

The floor in the cutoff only changes a constant. This is enough; no exponential-in-g tail is asserted or required.

The same fixed-t bound yields E[K^r]=O((log n)^r) for every fixed r by splitting the tail at a sufficiently large multiple of log n. Cauchy–Schwarz therefore makes every fixed count moment on the polynomially rare bad event vanish. The corresponding model probability-generating series gives identical types of estimates. This explicitly closes the otherwise invalid inference from total variation to convergence of unbounded moments.

On the good event, uniform density comparison multiplies the bounded model moment rather than the worst-case count n. That distinction is essential and correctly used. No rate for the correlator o(1) is required at this last step.

## 4. Coefficients and mesoscopic factorial moments

The factorization H(z)=(1−z)^(-1/2)B(z) is correct, with B analytic in the disk of radius four and B(1)=sqrt(2). Its coefficients and those of every fixed positive power B^t are exponentially bounded. The convolution proof gives h_n~sqrt(2/pi)/sqrt(n), the global square-root upper ratio bound, and uniform h_(n-r)/h_n→1 for r=o(n).

The assembly factorial-moment formula handles coincident selected part sizes correctly: falling factorials select distinct components, while the sum over ordered selected sizes includes repetitions of the size labels. Every fixed-order selection in a compact mesoscopic window uses only O(q_n)=o(n) total mass. The coefficient ratio is therefore uniform over the entire summation. The harmonic sum of zeta(2j)/(2j) over the window tends to half its logarithmic width.

These factorial moments give the joint independent-Poisson count laws. Tightness and moment determination can also be seen directly: higher fixed factorial moments remain bounded on each compact window, so subsequential limits inherit the limiting moments, and the Poisson vector is moment-determinate. This verifies vague convergence on (0,infinity), with no assertion about either endpoint scale.

## 5. Gamma marking and arbitrarily slow mesoscopic growth

I checked all three ranges in the marking estimate. For j comparable to q_n, the weighted standard-deviation estimate sums to O(q_n^(-1/2)), rather than an estimate multiplied by the total number of cylinders. Below a q_n/2, the upper-tail bound has strictly negative exponent a(1−log 2)q_n. Above 2b q_n, the lower-tail exponent is at most −(2 log(3/2)−1/2)j. Both constants are positive. The potentially large coefficient ratio near j=n is at most O(sqrt(n)) and is dominated by that latter exponential tail.

Consequently the marking error tends to zero even when q_n tends to infinity arbitrarily slowly. There is no hidden requirement q_n much larger than log log n. Compactly supported Lipschitz test functions and their Laplace functionals suffice to determine vague point-process convergence.

The total Gamma shape is exactly 2n for every composition. Therefore T_n/(2n) converges to one in probability. Joint independence between this total and the unnormalized point process is unnecessary: Slutsky's theorem and continuity of positive dilation suffice. The scale identity between normalized areas and marked points is correct.

## 6. Uniform integrability and the iterated sampling limit

The marked factorial-moment expression in Section 8 is valid, including repeated j_i. For selected total size at most n/2, the coefficient ratio is bounded and the product sums have uniform bounds. For larger selected mass, one part is at least n/(2r); since q_n=o(n), the probability that this Gamma mark falls into the mesoscopic window is exponentially small in n. This dominates the square-root ratio bound and all fixed powers of log n.

On the event that the total Gamma variable is between n and 4n, the normalized window count is bounded by a marked count in the stated enlarged compact interval. Off that event, K≤n and the total's exponential tail controls every fixed moment. Thus every required higher moment is bounded. Distributional convergence then gives all fixed joint moments, including the claimed mean and variance. The subsequent geometric transfer is justified by the good-event density comparison and bad-event estimates audited above.

For fixed genus, the cylinder number is bounded by 3g−3. Apart from the one-cylinder atom at area one, the mixture has simplex densities. The shrinking-window endpoints at each sufficiently large fixed genus are therefore continuity points. The N→infinity weak limit applies to their counts and moments before the g limit is taken. No diagonal interchange is hidden in the argument.

## 7. Independent controls and disposition

The inspected author exact checker reproduces its receipt byte-for-byte with 3,439 assertions. Its optional floating diagnostic also reproduces byte-for-byte under the documented OPENBLAS_NUM_THREADS=1 setting. An initial default-thread replay differed only in floating digits; this does not concern the exact or analytic proof. The diagnostics remain explicitly non-rigorous finite model calculations.

The fresh independent checker passes **2,032 exact assertions**. It uses integer partitions rather than the author's ordered-composition enumeration, and checks the full infinite-height zeta model rather than a finite-height substitute. Each zeta(2j)/(2j) is a rational multiple of pi^(2j), and the common pi^(2n) cancels at fixed total size. Independently computed Bernoulli weights are compared against the reciprocal-square-root sine power series. The checks include full-model mixed factorial moments, exact rational Beta window means, Dirichlet normalization, source-prefactor ratios and strict tail-exponent constants. These finite controls corroborate the identities; the limiting arguments and geometric inputs have been reviewed analytically.

The exact frozen candidate is suitable for a claimed-solved draft for this source target after the coordinator's publication gate. Preserve the iterated-limit, principal-stratum and marginal-only scope, the credited published inputs, and the no-novelty disclaimer. No mathematical revision is requested.
