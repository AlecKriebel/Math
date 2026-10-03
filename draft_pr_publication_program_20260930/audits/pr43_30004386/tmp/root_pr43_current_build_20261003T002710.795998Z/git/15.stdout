# Independent source-match review: 30004386 / OWR-17469-011

**Verdict: PASS. The exact two-part target is already solved by the cited published work of Johnston, Kabluchko and Prochno.**

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is a source-match audit with checks of the stated intermediate implication, not a new discovery or a claim of independent priority.

Frozen SOURCE_STATUS.md SHA-256:

98918841ab30dd1e41d51dbc7ec8515a66f1f1c82f01ff08ccc5462b758a2727

No author artifact was edited.

## 1. Original problem and publication identity

The original is the group-work report in Oberwolfach Report **6/2020**, pp. 411–413. Its underlying workshop ran 2–8 February 2020. The surrounding definitions concern a Haar-uniform direction on the Euclidean unit sphere and the one-dimensional projection of the uniform cube law. The random object in the large-deviation statement is the resulting probability measure on the real line.

Conjecture 1 asks for the full stated rate function at speed \(N\). Lemma 1 separately asks for every possible Prohorov limit of projection laws with unit coefficient vectors, including both necessity and attainability. The original definitions and the rendered conjecture/lemma page were checked. Any 2021 label in imported metadata does not change this source.

Source: [OWR 6/2020, original report](https://publications.mfo.de/bitstream/handle/mfo/3713/OWR_2020_06.pdf?isAllowed=y&sequence=4).

The publisher confirms the three authors, title, DOI 10.4064/sm210413-16-9, **Studia Mathematica 264 (2022), 103–119**, and online publication on **17 December 2021**. Its abstract explicitly states the same cube random-measure LDP and rate formula. The complete open author manuscript is arXiv:2103.16430v2, revised 19 September 2021. The inspected full text is that manuscript; a typeset journal PDF was not obtained. This access distinction does not obscure the exact published main-result statement, which appears on the publisher's own page.

Sources: [publisher record and abstract](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/online/114493/projections-of-the-uniform-distribution-on-the-cube-a-large-deviation-perspective), [versioned open manuscript](https://arxiv.org/abs/2103.16430v2).

## 2. Exact theorem match

Theorem A uses the space of real Borel probability measures with the weak topology, speed \(N\), and a good rate
\[
 I(\kappa_a)=-\tfrac12\log(1-\|a\|_2^2)
 \quad\text{for }\|a\|_2<1,
\]
with infinite rate otherwise. Its law is precisely the uniform series plus an independent Gaussian of variance \((1-\|a\|_2^2)/3\). It is a full LDP, not merely a compact-set upper bound. The theorem and its continuation were read directly.

Proposition 3.1 identifies the compact space of decreasing nonnegative sequences with squared sum at most one, using coordinatewise convergence, homeomorphically with its image of laws. Lemma 3.2 gives uniqueness of the ordered coefficient representation. This also makes the rate unambiguous, including the distinction between norm-one and smaller-norm parameters.

Thus both the random object and topology agree with the original. An LDP for a sampled scalar projection, or for its direction-averaged law, would be a different claim. Independence of directions across different ambient dimensions is unnecessary because these LDP bounds concern each marginal distribution.

Source: [Johnston–Kabluchko–Prochno, Theorem A and §3.1](https://arxiv.org/pdf/2103.16430v2).

## 3. Normalization and coefficient conventions

For independent \(U_i\sim\operatorname{Unif}[-1,1]\), centeredness and \(\operatorname{Var}(U_i)=1/3\) give
\[
 \operatorname{Var}\left(\sum_i a_iU_i+
       \sqrt{(1-\|a\|_2^2)/3}\,Z\right)
 =\frac{\|a\|_2^2}{3}+\frac{1-\|a\|_2^2}{3}
 =\frac13 .
\]
The independent series converges in \(L^2\) and almost surely since the sum of variances is finite. Symmetry removes coefficient signs, and rearranging the nonzero coefficients preserves the law and squared norm. Zero terms can be discarded. These assertions hold for infinite square-summable sequences by \(L^2\) convergence, not by assuming absolute summability of the coefficients.

The isolated sentence after equation (2) in the open manuscript stating variance one is inconsistent with its displayed law. The formula, Theorem A, and publisher abstract agree with the calculation above. The package correctly records this typo and uses variance \(1/3\).

At \(a=0\) the law is \(N(0,1/3)\) and the rate is zero. Norm-one laws remain valid members of the limit set, while their LDP rate is infinite. A law cannot acquire a finite rate by a second smaller-norm ordered representation, because that representation is unique.

## 4. Both directions of the limit-set claim

Let \(W\) be the ordered closed unit ball and \(K=\{\kappa_a:a\in W\}\).

For necessity, each law in \(E_N\) is \(\kappa_b\) for the decreasing absolute coefficients of its unit vector, padded by zeros. Its Gaussian term is zero. Proposition 3.1 makes \(K\) compact, hence closed in the Hausdorff weak topology on real probability measures. Every weak limit of such laws lies in \(K\).

For attainability, the package retains \(m_N=\lfloor\sqrt N\rfloor\) coefficients and fills the remaining \(r_N=N-m_N\) positions with
\[
 c_N=\sqrt{\frac{1-\sum_{i\le m_N}a_i^2}{r_N}} .
\]
For \(N\ge2\), the vector is well-defined and has squared norm exactly one. Moreover \(0\le c_N^2\le1/r_N\to0\).

Here is a direct check of the rearrangement step. If \(b^{(N)}\) is the sorted vector, then for every \(j\le m_N\),
\[
 a_j\le b_j^{(N)}\le\max(a_j,c_N).
\]
The lower bound holds because at least \(j\) retained entries are at least \(a_j\). For the upper bound, only the preceding \(j-1\) retained entries can exceed \(\max(a_j,c_N)\). Thus every fixed coordinate converges, even with ties, zeros or infinitely many positive coordinates. Proposition 3.1 gives convergence of the laws to \(\kappa_a\).

There is also a direct distributional check. The retained sum converges in \(L^2\) to the uniform series. An independent filler sum has variance tending to \((1-\|a\|_2^2)/3\); its log characteristic function has quadratic term \(-r_Nc_N^2t^2/6\) and error bounded by a constant times
\[
 r_Nc_N^4\le 1/r_N\longrightarrow0
\]
for fixed \(t\). Its limit is the required independent Gaussian, possibly degenerate. This independently confirms that no boundary law is lost.

This constructs a sequence for every sufficiently large integer \(N\), not only a subsequence. The first term can be arbitrary. Since Prohorov convergence metrizes weak convergence of probabilities on \(\mathbb R\), the original limit-set topology is exactly the one used.

## 5. Exact controls and their limits

All **527 author assertions** were replayed in a separate copy; the resulting JSON receipt is byte-identical to the frozen receipt. The author's script writes its own output file, so it was not run in the author's directory.

The independent standard-library checker passes **664 exact rational assertions**. It uses a different prefix rule, \(\lfloor N/2\rfloor\), and checks six coefficient families, including plateaus, finite boundary points, infinite interior points and infinite norm-one points. It verifies the uniform coordinate-error inequality, unit normalization, vanishing filler fourth powers, and exact fourth-moment bounds.

Separate characteristic-function calculations through degree six confirm the variance and higher-moment coefficients, including permutation controls and a negative check against variance one. Diffuse unit vectors verify that norm-one coefficients can converge coordinatewise to zero while higher uniform cumulants disappear.

Run from this review directory:

    python independent_checks.py > independent_results.json

These are finite diagnostics of normalization and the approximation argument. They do not constitute an experimental proof of a large-deviation principle. The published theorem supplies the LDP.

The original report and author-manuscript PDF hashes and byte sizes match the frozen source manifest. The original problem page and theorem continuation were visually inspected; current arXiv and publisher metadata were read independently.

## 6. Disposition

**The status already_solved is justified for both Conjecture 1 and Lemma 1 in the original report.** Credit belongs to Johnston, Kabluchko and Prochno. The elementary construction explaining the intermediate implication is not promoted as a new result.

The package requires no mathematical or source-scope correction for publication. Its scope remains one-dimensional projections of the continuous uniform cube law, with ambient dimension growing. No new substantive proof attempt was used. The review does not claim to reconstruct every proof estimate in the published paper or to certify unrelated projection LDPs.

## Final artifact hash coverage

The final SOURCE_STATUS.md was checked on 2026-09-30 by exact byte replacement against the originally reviewed artifact. Its only change updates the pending-review sentence to record the completed scoped AI review and link this report. All mathematics and attribution are unchanged. This verdict also covers final SHA-256:

90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3
