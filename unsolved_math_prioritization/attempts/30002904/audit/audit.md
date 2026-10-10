# Independent adversarial audit: problem 30002904

Date: 2026-10-06. Disposition: **accepted as an honest partial result**. The original ordinary operator-ball problem for fixed matrix size n >= 3 is not solved by this work.

## Immutable object reviewed

The author archive is `GENERIC_INTEGRAL_SUBGROUPS_30002904_AUTHOR_SAFE_FREEZE.zip`, 12022 bytes, SHA-256 `3696f895d693276cd2f5cd31ed57c619c51621910ddcea36a169b3b40e8f67ba`. Its six entries and five manifest-listed payloads were independently verified. The archive was not altered. This audit is a separate artifact, rather than a replacement author snapshot.

No mathematical repair is required for the stated partial results. The separate `independent_derivations.md` supplies stronger independent checks, including exact finite-radius continuous formulas. The author snapshot's statements that review was pending correctly describe its historical state; this acceptance report provides the later review result.

## 1. Target and scope

The [original report, printed p. 1709](https://ems.press/content/serial-article-files/46576) uses two independent uniform choices from the same ordinary operator-norm ball. Its norm is the largest singular value, and its inverse-bounded model is separately defined. The author retains these distinctions. The ambient dimension is fixed and at least two; the trivial n=1 case is not a hidden solution.

The inherited corpus record was independently located and hashed using the complete problem and the empty inherited research record. The supplied review hash matches. The empty record arose from an absent report key, not from a truncated nonempty report. Only verification metadata is included here; no corpus text is reproduced.

## 2. Dimension two: accepted

For B_X in SL2(Z), the finite-index probability bound X^(-1+o(1)) is valid. The crucial input is the exceptional count for failure of four separated isometric disks, not merely an estimate for nonfree pairs. The cited [Bulinski--Ostafe--Shparlinski preprint, Lemma 3.6](https://arxiv.org/pdf/2304.10980), has precisely the required Q=1 form. Definitions and tangency inequalities were checked. Its elementary counting argument was independently reconstructed in the companion derivations.

The proof's changes of norm are legitimate here because they are used to bound a number of exceptional pairs in a containing height box, and because the operator ball independently has cardinality bounded below by a constant times X^2. There is no inference that equivalent norms preserve all probability laws.

The upper size estimate handles primitive first columns with a zero coordinate and uses only one coordinate of maximum magnitude to control completions. The lower construction uses positive coprime columns, distinct resulting matrices, and a Bezout completion of height at most floor(X/2). The union-bound coprimality lower bound has a strictly positive constant. Matrices with lower-left entry zero number O(X), producing only O(X^3) exceptional pairs.

The infinite-index deduction is sound. Reduced words keep a point outside the disks in a bounded union of disks, whereas a finite-index subgroup contains a positive power of the translation matrix, forcing an unbounded orbit. This also handles the central kernel of the projective action: no nontrivial reduced word can fix that chosen point. Freeness alone would not justify infinite index in SL2(Z), and the author does not rely on that false implication.

The modern paper's Section 4.1 specifically challenges the earlier Lemma 2.5 argument. It does not itself certify all other parts of the older paper. The inspected proof version is arXiv v1 dated 2023; [the publisher's bibliographic record](https://journals.sns.it/index.php/annaliscienze/abstract/downloadAbstractFile/6279) confirms the 2025 journal publication. These are distinguished rather than represented as identical inspected files.

## 3. Continuous SL3 distribution: accepted

The author correctly proves, for each fixed s >= 0,

\[
\lim_{X\to\infty}\Pr_{\mathrm{Haar},\,\|g\|_{op}\le X}
\left(\log\frac{\sigma_1}{\sigma_2}\ge s\right)
=2e^{-2s}-e^{-4s}.
\]

Adversarial checks covered:

- Positive ordered singular values, logarithmic determinant constraint, and the precise operator norm rather than the Frobenius norm or a squared-singular-value threshold.
- Multiplicity-one real Cartan density. Compact-factor volumes, finite Cartan ambiguities, and the constant between Euclidean area on the trace-zero plane and coordinate area all cancel. No dimension-dependent probability factor is missing.
- The exact domain u >= 0, d >= 0, 3u+2d <= 3L for u=L-log(sigma1), d=log(sigma1/sigma2), L=log X. This includes the entire chamber and forces log(sigma1) >= 0.
- Absolute Jacobian one from the two free logarithms to (u,d).
- The nonnegative dominating density (1/4)e^(-6u-3d)sinh(d), with mass 1/192. The determinant cutoff is retained before extension by zero to a fixed quadrant.
- Pointwise convergence, domination for every fixed tail, the boundary case s=0, and absence of a claim uniform in a threshold growing with X. For negative s the probability would instead be one; the stated restriction s >= 0 is essential and present.
- The inverse cutoff is exactly 2u+d >= L. Its indicator tends pointwise to zero and the same integrable bound applies.

An independent change to the two simple-root gaps gives a closed formula at finite X, agreeing with the author's limit without using that dominated-convergence calculation. It also proves the continuous inverse-bounded ratio is asymptotic to 6X^(-2). Both statements remain exclusively about Haar volume.

## 4. Printed Fuchs--Rivin numerical bound: correction accepted

The displayed threshold and exponent in [Fuchs--Rivin, Theorem 3.4](https://academic.oup.com/imrn/article/2017/17/5385/3056825) were checked in the current journal rendering and the author-hosted primary PDF. The diagonal entries in its KAK decomposition are the singular values, so the threshold is not secretly a ratio of their squares.

The printed quotient has limits applied separately to divergent quantities. The author expressly repairs this only to the intended limit of normalized volumes before testing the numerical claim. At n=3 and s=2 log(eta), the true limit is

\[
2\eta^{-4}-\eta^{-8},
\]

which is strictly greater than the claimed upper bound eta^(-4) for every eta > 1, in particular throughout the stated eta > 4 range. At eta=5 these are exactly 0.00319744 and 0.0016. This is an analytic contradiction, independent of floating-point evidence.

The correction has a precise narrow scope: the n=3 numerical bound under the intended normalized-volume interpretation fails. The calculation retains a positive limiting probability strictly below one. It neither disproves the inverse-bounded main theorem nor supplies a higher-dimensional correction. It is distinct from the modern paper's criticism of Lemma 2.5. No novelty priority is asserted.

## 5. Other barriers: accepted

The singular-value inequality ||A^(-1)||op <= ||A||op^(n-1) and the two ball inclusions are correct. The unipotent family I+mN has inverse corner entry of magnitude m^(n-1), while its own norm is at most 1+m. For n >= 3 this excludes a uniform linear comparison even on integer matrices. It does not by itself estimate densities.

The [Aoun reference](https://arxiv.org/abs/1005.3445) is a random-walk result. The author correctly stops before transferring its conclusions to uniform operator balls.

The free-word counterexample is valid. The 3-cycle permutation and one elementary transvection generate SL3(Z); the specified conjugations and commutator supply all elementary directions. The squared upper and lower transvections form a free subgroup by the usual two-set ping-pong inequalities, fix the third basis vector, and have infinite index, although their two parent generators generate the full lattice. Thus finding free words cannot establish the requested property of the parent subgroup.

## 6. Acceptance boundary and publication safety

The target remains unresolved by this package for every n >= 3. In particular, no lattice-point transfer of the continuous gap law, the continuous inverse-ball rate, or its zero limit has been proved. Such a claim would require a separately checked counting argument for the precise changing regions.

The package accurately records five attempted approaches and their stopping points. It does not turn five approaches into a solution or a proof that further approaches cannot work. A bounded literature check is not an exhaustive current-status or novelty certificate.

Both archives are data-only. No source PDF, source HTML, extracted source passage, raw corpus, private coordination material, or executable verifier is included in this audit package. Integrity tests are distinct from mathematical proof checks. `validation.json`, `provenance.json`, and `acceptance.json` record the precise tests and limitations.
