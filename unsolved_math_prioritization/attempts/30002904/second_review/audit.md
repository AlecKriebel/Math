# Second independent audit of the SL3 Haar correction

Date: 2026-10-06. Problem identifier: 30002904, selection rank 864.

## Verdict and scope

The claimed correction to the numerical bound in Fuchs–Rivin Theorem 3.4 is accepted under the theorem's intended limit-of-normalized-Haar-volumes interpretation. For ordinary operator-norm balls in SL3(R), and every fixed s >= 0, the top logarithmic singular-value gap has limiting tail

\[
2e^{-2s}-e^{-4s}.
\]

At the theorem's threshold sigma1/sigma2 >= eta², this gives 2eta^(-4)-eta^(-8), which exceeds eta^(-4) for every eta > 1. In particular, it contradicts the printed strict upper bound throughout the stated eta > 4 range.

The first auditor's exact finite-radius formulas for the gap tail and inverse-bounded subball are also correct. The inverse-bounded-to-ordinary Haar-volume ratio is asymptotic to 6X^(-2). No correction to the frozen author proof or the first audit's targeted mathematical claims is required. This second audit is a separate, narrowly scoped acceptance; it does not replace either original archive or certify every other claim in the first audit.

All probabilities in this report refer to normalized Haar measure on the specified subsets of SL3(R). No assertion about uniform matrices in SL3(Z), no lattice-point transfer, and no solution of the original fixed-n >= 3 discrete genericity question is made. No novelty claim or conclusion about the whole Fuchs–Rivin paper is made.

## Immutable materials

The following supplied pins were checked before relying on archive content:

- Author: `GENERIC_INTEGRAL_SUBGROUPS_30002904_AUTHOR_SAFE_FREEZE.zip`, 12022 bytes, SHA-256 `3696f895d693276cd2f5cd31ed57c619c51621910ddcea36a169b3b40e8f67ba`.
- First audit: `GENERIC_INTEGRAL_SUBGROUPS_30002904_INDEPENDENT_AUDIT_SAFE.zip`, 14321 bytes, SHA-256 `ace08895493a04303f1427f880ae2795c457b810027e0d5bc0fb484b19b3012d`.

Every member was checked against its manifest. The working copies read for this review were compared byte-for-byte to the corresponding frozen members. Neither archive contains executable files, and no author or first-auditor program was run. Both original archives are preserved unchanged.

The mathematical review concerns Proposition 3 and its numerical-bound discussion in the author proof, and Sections A–D of the first audit's independent derivations. The first audit's rank-two counting argument, group examples, and corpus reconstruction are outside this second review's acceptance scope.

## What the primary theorem says

The [journal rendering of Theorem 3.4](https://academic.oup.com/imrn/article/2017/17/5385/3056825) specifies Haar measure on SLn(R), ordered positive diagonal entries in a KAK decomposition, eta > 4, threshold a1/a2 >= eta², and upper bound eta^(-2(n²-3n+2)). The displayed limits occur separately above and below the fraction. The proof then works with normalized integrals. At n=3 the printed numerical bound is eta^(-4).

The [author-hosted PDF](https://www.math.ucdavis.edu/~efuchs/genericsln4.pdf), printed pages 2, 10, and 12, was independently rendered and visually inspected. Equation (1.1) defines norm squared as the largest eigenvalue of gᵀg. Theorem 3.4 and its proof therefore use the ordinary Euclidean operator norm and positive KAK entries. Nearby prose identifies singular values with eigenvalues of gᵀg; that terminology is inconsistent with the displayed decomposition. This review uses the theorem's explicit decomposition, as the frozen proof does.

The original PDF and journal HTML are distinct sources; no claim of byte identity between versions is made. Rehashed local source-file metadata and the fresh public-page inspection are distinguished in `provenance.json`. No source files or extracted passages are redistributed.

## Resolving the possible squared-value objection

Let g=kDℓ with k,ℓ in SO3(R) and D positive diagonal. Then

\[
g^Tg=\ell^TD^2\ell.
\]

Thus D's entries are the positive square roots of the eigenvalues of gᵀg. They are the ordinary singular values, regardless of informal terminology elsewhere. Also ||g||op is the largest entry of D. This resolves both the threshold and radius conventions directly, without relying on a phrase in a secondary source.

Even the alternative event formed from the eigenvalue ratio of gᵀg would not rescue the printed bound. That event would be sigma1/sigma2 >= eta, with limiting probability 2eta^(-2)-eta^(-4), again greater than eta^(-4) for eta > 1. This is an ambiguity check, not a replacement interpretation of the theorem.

Replacing the radius parameter X by its square merely reparametrizes the limit to infinity; it cannot change the fixed-threshold limiting tail. The inverse-ball rate in this report, however, is explicitly in the ordinary operator-radius X, so its exponent must not be silently moved to a different radius convention.

## Haar density and the chamber

Write the singular values as exp(a), exp(b), exp(c), in descending order. Their product is one, so a+b+c=0. The exact ordinary-ball region is

\[
a\le L=\log X,\quad a\ge b\ge c=-a-b.
\]

It is important to retain the last inequality, equivalently b >= -a/2. The region is compact; for X > 1 it has positive Haar volume. Its boundary is null for the radial density, so open or closed inequalities do not change the probabilities. At X=1 the ball has zero ambient Haar measure, and no normalized probability at that radius is claimed.

A local differential calculation gives radial density

\[
C\,\sinh(a-b)\sinh(a-c)\sinh(b-c)\,da\,db,
\]

where C>0 is independent of the point and region. For a pair i<j, the two skew-symmetric compact directions give, after left translation to the identity, determinant exp(t_i-t_j)-exp(t_j-t_i). Taking the absolute determinant produces 2sinh(t_i-t_j) on the descending chamber. The product of the three pair factors gives the formula. The diagonal-area normalization, compact-group volumes, and finite decomposition multiplicity are constant and cancel from all ratios. In particular, the real group has root multiplicity one, not the squared Vandermonde density of a different field.

This calculation is independent of signs attached to an ascending versus descending root convention in a cited formula. Reversing chamber order cannot change a probability computed from the absolute Jacobian.

## Independent proof of the gap law

The companion `derivations.md` proves the limit by a new bounded-domain calculation. Put

\[
t=\sigma_1/X,\qquad r=(\sigma_2/\sigma_1)^2.
\]

The exact domain is X^(-1) <= t <= 1 and X^(-3)t^(-3) <= r <= 1. After removing the constant C and dividing by X^6, the radial measure has density

\[
F_X(t,r)=\frac{t^5(1-r)}{16}
\left(1-\frac1{X^6t^6r}\right)
\left(1-\frac1{X^6t^6r^2}\right)
\]

on that domain, extended by zero to the unit square. Each parenthesis lies between zero and one. Therefore

\[
0\le F_X(t,r)\le t^5(1-r)/16.
\]

For every interior point of the square, F_X tends to this upper bound; its integral is 1/192. Dominated convergence is thus valid on a fixed, bounded domain with an explicitly integrable majorant. The limiting normalized joint density is 12t^5(1-r). Integrating over r <= exp(-2s) proves the claimed gap tail exactly.

This independently checks the author argument: u=L-a and d=a-b have absolute coordinate Jacobian one and domain u,d >= 0, 3u+2d <= 3L. The author's majorant is exp(-6u-3d)sinh(d)/4, with integral 1/192. Its fixed-tail calculation agrees with the bounded-domain derivation. There is no omitted determinant cutoff, chamber wedge, normalization constant, or near-wall contribution.

For s=0 the answer is one. For s>0 it is strictly between zero and one. The limiting gap density is 4(exp(-2s)-exp(-4s)), which is nonnegative and integrates to one. A statement for fixed s is all that is needed here; no moving-threshold relative asymptotic is asserted.

## Exact finite-radius and inverse-ball cross-checks

The first auditor's gap-tail radial mass I(L,s), including all lower-order terms, was checked by independently integrating the inner root coordinate, differentiating the proposed answer in its lower limit, and checking the empty-domain boundary s=3L/2. The total mass is

\[
I(L,0)=\frac{\sinh(6L)}{96}-\frac{\sinh(3L)}{12}+\frac{3L}{16}
\sim\frac{e^{6L}}{192}.
\]

For the inverse-bounded subball, this review instead uses coordinates a=log(sigma1) and v=-log(sigma3), and integrates over 0 <= a,v <= L with a/2 <= v <= 2a. It recovers

\[
K(L)=\frac{\sinh(4L)}{16}-\frac{\sinh(3L)}6
+\frac{\sinh(2L)}{16}+\frac L8
\sim\frac{e^{4L}}{32}.
\]

A separate dominated-convergence proof at the corner (a,v)=(L,L), given in `derivations.md`, establishes the same leading constant without using that exact expression. The common Haar constant C is the same for I and K. Consequently K(L)/I(L,0) is asymptotic to 6e^(-2L)=6X^(-2). This verifies both the first auditor's coefficient and the author's continuous zero limit.

## The precise contradiction and its limits

At s=2log(eta), the actual limit minus the printed upper bound equals

\[
(2\eta^{-4}-\eta^{-8})-\eta^{-4}
=\frac{\eta^4-1}{\eta^8}>0\quad(\eta>1).
\]

For eta=5 the exact limiting value is 1249/390625=0.00319744, whereas the proposed upper bound is 1/625=0.0016. These exact rational values are consequences of an analytic limit; no numerical integration is needed to disprove the bound.

Both unnormalized Haar volumes appearing in the source's separately written limits grow as positive constants times X^6. Their separate limits are therefore both infinite, and their quotient is not a real-number expression. The acceptance is expressly about the intended limit of the ratio, supported by the proof's normalized-integral calculation. Merely moving the limit symbol outside the fraction would correct the notation but would not correct the numerical bound.

The cancellation mechanism can also be seen explicitly. The two leading exponential terms of the radial density at b=a-d are proportional to exp(6a-2d)-exp(6a-4d). Their coefficients have opposite signs. After integration and normalization, they produce 2exp(-2s)-exp(-4s), rather than a positive weighted average bounded by exp(-2s). This identifies the obstruction to the numerical comparison in dimension three. It supplies no general-n replacement and no verdict on a separate inverse-bounded thinness theorem.

## Validation and acceptance boundary

An independently written verifier checked both supplied archives under isolated Python in normal and optimized modes. All 70 valid/hostile archive-control outcomes agreed between modes. Controls covered immutable pins, lengths, truncation, duplicate ZIP and JSON keys, missing or additional files, malformed manifests, traversal and absolute paths, symlinks, executable members, invalid UTF-8, nonfinite JSON including numeric overflow, opaque ZIP metadata, preambles and trailers, oversized entries, stale payload hashes, and self-consistent rewrites tested against the original external pin.

There were 26 independently authored symbolic mathematical checks, also run with `python -I` and `python -I -O`; all passed and agreed. They corroborate Jacobians, density identities, finite-radius integrals, leading coefficients, the counterexample, and the limiting-density normalization. They are not a substitute for the analytic proofs above. No data sampling, finite-lattice experiment, or floating-point diagnostic is used as proof.

The accepted statements are enumerated in the separate `acceptance.json`. The public-safe archive contains only authored prose and mathematical derivations, acceptance, and verification metadata. Original sources, datasets, screenshots, private coordination, and executable test code are excluded. Publication was not performed.
