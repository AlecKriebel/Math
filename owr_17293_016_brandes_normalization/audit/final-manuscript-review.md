# Final pre-publication mathematical review

Checkpoint: 2026-09-23 04:14 UTC. Completion estimate: **100% of this review**.
Reviewed `manuscript/paper.tex`, SHA-256 `42fc573b476c5f4d9386af2c9b6c81d0a876126b039ed3e3d54bb423de5f74d4`, together with the authenticated original page, the source and priority audits, and verifier results.

**Verdict:** the complete proof is sound and proves the stated strengthening of the original question. No mathematical repair is required. Two small editorial corrections were requested before publication:

1. In the opening sentence, change “be homogeneous of positive degree” to “be a homogeneous polynomial of positive degree.” The theorem already says “form,” but the opening definition should explicitly give the polynomial hypothesis needed for its unique symmetric polarization.
2. Correct the Oberwolfach bibliography's Problem Session page range from `3179--3182` to `3179--3183`. Problems 14 and 15 continue onto printed page 3183 before the next contribution. Problem 11 itself is correctly cited at page 3182.

No other required change was identified.

## Source match and hypotheses

I independently inspected the supplied rendering of the publisher's original printed page 3182. Problem 11 is attributed to Brandes; its form is real, homogeneous, and positive definite. Its displayed sum uses tuple indices, and the requested coefficient inequality contains absolute values. The allowed coordinate operation is a linear change with no printed orthogonality, integrality, or conditioning constraint. The manuscript explicitly defines the canonical symmetric ordered coefficients and proves the requested inequality for them. It correctly explains the multinomial factor relating these entries to ordinary monomial coefficients.

The theorem's unit diagonal and positive strict mixed bounds imply the original absolute-value inequality. Positive degree and positive definiteness imply even degree at least two. Dimension one is explicitly addressed, and the proof works with an empty tangent basis. Degree two is valid throughout, including the tangent lemma and polynomial expansions.

## Proof completeness

The normalized sphere minimum is attained and positive by compactness and positive definiteness. Its homogeneous extension gives `p(x)>=|x|^d`, including zero. The tangent comparison function therefore has zero first derivative and nonnegative second derivative, yielding exactly the displayed tangent linear vanishing and coercivity constant `1/(d-1)`.

The clustered vectors are independent for every nonzero displacement. Their multilinear expansions have no linear terms. Expansion of the polynomial gap gives the displayed quadratic coefficient

\[
\frac d2\sum_{r<s}Q(a_r-a_s,a_r-a_s).
\]

It is positive for each mixed tuple because the chosen tangent perturbations are distinct. Each such fixed polynomial is consequently positive for all sufficiently small positive displacement; taking the minimum threshold over the finite tuple family is valid. Pure gaps vanish identically. A second finite continuity argument simultaneously makes all multilinear numerators positive. These observations establish positivity and the absolute-value bound with no implicit global uniformity or computational assumption.

Restoration of the original form is correct: multiplying normalized `p,A` by `c` multiplies the left side and the geometric-mean right side by `c`. The final column rescaling uses the **original** values `p(x_i)`, so the resulting basis has original diagonal values exactly one. Multilinearity divides a mixed value by precisely its geometric-mean denominator. Strictness is preserved.

## Rational-density remark

The rational-density observation is correct even when the coefficients of the given form are arbitrary real numbers. The determinant, the finitely many numerator values, and the finitely many mixed polynomial gaps vary continuously with the matrix entries. Their strict nonzero/positive conditions hold in an open neighborhood of the constructed real matrix. A rational matrix exists in that neighborhood. Pure equality is an identity and imposes no additional closed condition. The manuscript correctly separates this rational unnormalized basis from the possibly irrational unit-diagonal rescaling.

The phrase “can also be chosen rational” means that the clustered construction can be perturbed to rational matrix entries; it need not retain the exact orthonormal clustered parametrization. This is the natural reading of the density argument. It would also be accurate to write “can be perturbed to a rational basis.”

## Supporting computation and provenance

The manuscript claims 12 exact rational examples; this agrees with both the executed verifier and the recorded results. The package's more detailed totals are 120 coefficient classes and 110 independent inclusion-exclusion polarization checks. The nonconvex positive quartic claim is correct. The fixed-coordinate example has tensor entry `12/6=2` and diagonal entries one, exactly as stated.

The text accurately states that finite checks are supplemental and do not constitute a formal proof of the universal theorem. No software result is used as an assumption in the analytic argument.

I checked the primary [2015 precursor](https://arxiv.org/html/1506.05343): its introduction discusses pseudo-diagonal forms, and its Lemma 2.1 treats positive definite quadratic matrices. The manuscript's limited attribution is supported. It does not adopt that source's stronger invariance sentence or conflate its conventions with the explicitly defined ordered coefficients.

The provenance paragraph identifies the preprint as unrefereed, discloses AI assistance, and limits the literature result to a dated bounded search that found no earlier general resolution. It expressly declines to establish first priority. These statements agree with the scope recorded in the priority audit. The affirmative-resolution language is justified by the proof and is not presented as community acceptance or an established priority claim.

## Final disposition

The mathematical manuscript is ready for publication after the two minor corrections listed at the start. This review does not certify website deployment, artifact hashes after packaging, or DOI registration; those are separate release checks.

## Correction verification and archived spot checks

Checkpoint: 2026-09-23 04:16 UTC. Completion estimate: **100%**. I independently reread the current source and confirmed both requested corrections: its opening explicitly says “homogeneous polynomial,” and the Problem Session bibliography now gives pages `3179--3183`. The corrected manuscript SHA-256 is `317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43`. No requested mathematical or editorial correction remains open.

The previously executed 500 determinant comparisons and 20 polarization comparisons are now preserved as `verification/adversarial_checks.py`, using the same deterministic seed and cases. Run `python3 verification/adversarial_checks.py` to reproduce them. The comparisons remain finite implementation checks; neither their number nor their success constitutes a proof of the universal theorem.
