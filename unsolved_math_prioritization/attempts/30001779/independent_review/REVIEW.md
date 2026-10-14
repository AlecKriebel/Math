# Independent review of 30001779

**Verdict: PASS_SCOPED_RADIAL_CLASSIFICATION_AND_BOUNDED_RADIUS_EXPECTATION.** No mandatory correction. Retain **unsolved, 3/5** for the original general characterization. The unrestricted marginal-moment obstruction is credited prior work, while the fixed-law radial classification and expectation application are scoped mathematical deductions. This is an adversarial AI review, not human peer review or a priority determination.

Reviewed artifact: `PARTIAL_RESULT.md`, SHA-256 `5f79a4f530e351018fe224c92529f133a1c38aa9a75a2f8645a43242e1ed468c`. The frozen snapshot and its verifier are preserved in `author_replay/`.

## Exact question and source coverage

The original [OWR24/2011, printed p.1291](https://ems.press/content/serial-article-files/46338) specifies the ordinary empirical second moment of a mean-zero vector and expected operator-norm error relative to the covariance norm. It asks for a characterization of distributions permitting linear sample size. The preceding bounded-radius paragraph and the later informal moment conjecture do not spell out a single uniform hypothesis class. The artifact correctly preserves that ambiguity, the dimension-uniform constants, and the prescribed estimator. It does not replace expected norm error by a probability statement or a lower-edge statement.

I checked the full journal-reprint [Srivastava–Vershynin paper, arXiv1106.2775v4](https://arxiv.org/pdf/1106.2775v4), Theorem1.1, Corollary1.2, Theorem1.5 and Section1.8. The two-sided expectation theorem assumes the unscaled all-projection bound

\[
\Pr\{\|PX\|^2>t\}\le Ct^{-1-\eta},\qquad t>C\operatorname{rank}P.
\]

The one-dimensional moment theorem controls only the expected smallest eigenvalue. A normalized moment of a rank-r projection is not interchangeable with this tail estimate: its naive Markov bound carries a power of r. Section1.8 explicitly supplies the Gaussian radial multiplier counterexample, credits Aubrun, and separately discusses the added almost-sure radius restriction. The artifact's attribution and scope correction are accurate. A dimensional shorthand in that source's informal maximum estimate is not needed by the submitted proof, which uses the exact n/N factor.

I also checked [Tikhomirov's full v1 preprint](https://arxiv.org/pdf/1606.03557v1), Theorem1 on pp.2–3, including the rendered formula. Its hypotheses are centered isotropic vectors with a uniform p-th marginal moment bound, p>2, and N>=2n; its exceptional probability is at most 1/n. The three displayed terms, moment-constant power 2/p, ratio logarithm, and exponents in (T) match. [The publisher's issue listing](https://academic.oup.com/imrn/issue/2018/20) confirms IMRN2018(20),6254–6289, DOI10.1093/imrn/rnx067. This review checks the application of that theorem and its source hypotheses; it does not independently reprove the full imported high-probability estimate or compare every line to the final typeset version.

## Expectation upgrade

For independent isotropic samples, put Z_i=X_iX_i^T-I. Their centered Frobenius cross terms have expectation zero, and

\[
\mathbb E\Big\|N^{-1}\sum_iZ_i\Big\|_F^2
=N^{-1}(\mathbb E\|X\|^4-n).
\]

The bounded-radius assumption gives \(\mathbb E\|X\|^4\le L^2n\mathbb E\|X\|^2=L^2n^2\). For an exceptional event of probability at most 1/n, Cauchy–Schwarz consequently gives \(L\sqrt{n/N}\). This is the required dimension cancellation; bounding the exceptional norm only by its worst-case value would not suffice. Adding the deterministic good-event bound proves (B). Every exponent is positive when p>2, and a fixed power of log r is dominated by a positive power of r. The n=1 case follows from the same Frobenius identity without invoking a useful good-event probability. Whitening requires the assumptions on the whitened vector, as stated; restriction to the covariance range handles singular covariance.

## Fixed-law radial classification

For X=R epsilon, independence of the signs and E R²=1 give mean zero and identity covariance. Positivity of each summand gives the exact lower bound \(\lambda_{\max}(\Sigma_N)\ge(n/N)\max R_i^2\). If the fixed radial law is unbounded, its independent sample maxima diverge almost surely and in expectation. Thus for every fixed C and n<=N(n)<=Cn, the expected error and the error in probability diverge. If N<n, rank deficiency prevents accuracy below one. This proves necessity for the uniform linear-sampling property. It would not prove the same assertion for an arbitrary dimension-dependent sequence of radial laws, which the artifact expressly excludes.

For bounded R, the conditional product of coshes yields the stated subgaussian moment-generating function. I independently checked the numerical constants in the subsequent centered-square estimate. The moment-series majorant is

\[
\sum_{k\ge2}(8B^2|t|)^k
=\frac{(8B^2t)^2}{1-8B^2|t|}\le128B^4t^2
\]

for |t|<=1/(16B²). Choosing t=min(s/(256B⁴),1/(16B²)) proves both Chernoff branches: below s=16B² the exponent is s²/(512B⁴); above it, the exponent is at least s/(32B²). A 1/4-net gives the factor two and cardinality 9^n. Both terms in the threshold in (5) are individually large enough to make the corresponding exponent at least A_0+t. Integrating its increasing threshold, including its derivative, gives (6); A_0 is bounded above and below by absolute multiples of n. Hence sufficiency is an expectation statement, not just a high-probability statement. Integer rounding of N changes only the harmless sampling constant.

## Exponential-radius quantitative obstruction

For R=Y/sqrt2, the exponential moments and coefficientwise Rademacher-to-Gaussian comparison give (7) with the displayed factorial normalization. All fixed moment constants are independent of n, though they depend on the moment order. The maximum exponential has mean H_N and, independently via its exponential spacings, second moment H_N²+sum(j^-2). Thus the artifact's Jensen lower bound is valid and slightly weaker than the exact value. Rank deficiency forces N>=n when epsilon<1; applying H_N>=log(N+1) then proves the n log²(n+1)/(2(1+epsilon)) necessary bound. No matching upper sample bound is asserted. The elementary maximum-event probability and factor 1/8 in (10) are correct.

For the identity projection, a threshold An leaves a fixed positive radial tail but the required strong-regularity right side tends to zero. Hence this example does not violate the correctly stated Srivastava–Vershynin theorem. It also fails the almost-sure bounded-radius hypothesis. The broad arbitrary-distribution characterization remains open within this package.

## Reproduction and limitations

All **11,164** submitted assertions replay byte-for-byte. The separate standard-library checker passes **5,903** assertions, using a different rational radial mixture and full three-sample enumeration for the Frobenius identity, polynomial convolution for marginal moments, exponential spacings versus survival integration, an alternative fixed unbounded geometric radial law, and exact concentration constants. These finite checks support algebraic steps; the written arguments establish the asymptotic quantifiers, and the cited theorem supplies the imported probabilistic estimate.

From this directory, run `python independent_checks.py`. For the submitted replay, run `cd author_replay && python verify.py`. The stored receipts record hashes. No general distribution characterization, new historical priority, or proof of the original informal conjecture under every interpretation is established.
