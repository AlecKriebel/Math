# Bounded literature comparison for the square-root overhead candidate

12 October 2026. This is an authored source comparison, not a novelty certificate, acceptance report, or independent proof audit. No external mutation, publication, or source-author code execution was performed.

## Conclusion

No inspected later source supplies an unconditional upper bound for the actual Erdős–Selfridge minimum that subsumes

\[
\log g(k)\leq \log L_k+(13/5+o(1))\sqrt{k},\qquad
g(k)=\min\{n>k+1:P^-(\binom nk)>k\}.
\]

That negative finding is limited to the sources and searches below. It does **not** establish that the square-root overhead is new, best known, or previously unpublished.

The finite counting inequality is a direct specialization of **Brun's pure sieve / the Bonferroni inequalities with CRT remainder bounds**. It should be credited accordingly. The particular forced-prime selection and its growing-order, initial-interval error analysis are the parts that must carry any application-specific contribution claim. A claim to a new general sieve theorem would be misleading.

The comparison against the 1974 displayed construction is valid: its overhead above \(\log L_k\) is \(O(k/\log k)\), while this candidate's overhead is \(O(\sqrt{k})\). Say explicitly that the comparison is with that construction. Neither a literature-wide improvement nor a resolution of EP-1095 follows.

### Separate principal-coefficient candidate

The same bounded source comparison found **no inspected unconditional actual-minimum bound** of the form \(g(k)\leq\exp((a+o(1))k)\) with a fixed \(a<1\). This is relevant to the separately proposed, unaccepted \(a\approx0.936\) construction, but is not an audit or endorsement of that construction. The \(0.7884305\) in SSW2021 is a coefficient on \(k/\log k\) for \(\widehat g\), not a coefficient on \(k\) for actual \(g\). The absence of a subsuming result in the inspected sources is not proof of novelty.

## 1. The original actual-minimum construction

E. F. Ecklund Jr., P. Erdős and J. L. Selfridge, *A New Function Associated with the Prime Factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649.

Primary source: https://www.renyi.hu/~p_erdos/1974-01.pdf

Printed p.648, equation (8), states for sufficiently large \(k\)

\[
g(k)<k^2L_kP_\ell,\qquad \ell=\lfloor6k/\log k\rfloor,
\qquad P_\ell=\prod_{p\leq\ell}p.
\]

The proof on pp.648–649 searches the actual integers \(tL_kP_\ell-1\), \(1\leq t\leq k^2\), and rules out covering all of them by bad primes. Its PNT consequence is \(g(k)<\exp(k(1+o(1)))\). More precisely, taking logarithms of the displayed bound gives \(\log g(k)<\log L_k+(6+o(1))k/\log k\). The authors explicitly allow reducing 6 but do not prove \(g(k)<L_k\).

The candidate retains this lattice idea, while changing the forcing set and replacing a first-order exclusion bound by a growing Brun truncation. The previously authored local coefficient-1 refinement of the \(k/\log k\) overhead is not a separate published prior theorem.

## 2. Computational sieve predecessors

R. Scheidler and H. C. Williams, *A Method of Tabulating the Number-Theoretic Function g(k)*, Mathematics of Computation 59 (1992), 251–257.

Primary author-hosted PDF: https://cspages.ucalgary.ca/~rscheidl/Papers/gk.pdf

Printed pp.251–253 formulate simultaneous admissible residue sets with a bounded search interval, give the digit criterion, and distinguish lower-digit congruences from a leading-digit filter. The paper provides algorithms and a finite table, not a uniform square-root-overhead existence estimate. Theorem 2, p.253, explicitly retains the leading-digit condition.

R. F. Lukes, R. Scheidler and H. C. Williams, *Further Tabulation of the Erdős–Selfridge Function*, Mathematics of Computation 66 (1997), 1709–1717.

Primary author-hosted PDF: https://cspages.ucalgary.ca/~rscheidl/Papers/es.pdf

Printed p.1710, equation (2.1), already formulates the general finite residue-set sieve with interval boundaries and filters. The subsequent density comparisons are not unconditional least-survivor upper bounds. The separate correction to the printed Lemma 3.8 must remain narrow: the leading-digit filter is not automatically valid, but the implementation's retained filters prevent inferring a table-wide failure. This source cannot justify dropping that digit in the candidate.

## 3. Sorenson–Sorenson–Webster: distinguish the two functions

B. Sorenson, J. P. Sorenson and J. Webster, *An Algorithm and Estimates for the Erdős–Selfridge Function*, Open Book Series 4 (2020), 371–385.

Published source: https://doi.org/10.2140/obs.2020.4.371

Published PDF: https://msp.org/obs/2020/4-1/obs-v4-n1-p23-s.pdf

The relevant exact statements are:

- Theorem 5.1, p.377: **under the Uniform Distribution Heuristic**, \(\widehat g(k)/k\leq g(k)\leq k\widehat g(k)\) with model probability \(1-o(1)\).
- Theorem 5.2, p.378: \(G(x,k)\sim x/\widehat g(k)\) for sufficiently large \(x\), with \(k\) fixed. Its proof has error \(O(R_k)\), where \(\widehat g(k)=M_k/R_k\).
- Theorem 6.1, p.379: \(0.530684+o(1)\leq \log\widehat g(k)/(k/\log k)\leq1+o(1)\).
- Lemmas 6.2–6.3, pp.379–380: square-root exponential controls on component factors of **\(\widehat g\)**.

None is the required unconditional actual-minimum bound. In particular, the periodic-count error need not be small at a proposed first-survivor scale. Theorem 6.5 is an algorithm-running-time statement conditional on UDH, not a new unconditional size bound for \(g\). The introduction still attributes the actual exponential upper bound to 1974.

The frozen published PDF was inspected as text and its printed pp.377–379 were freshly rendered and visually checked. The accessible ANTS-hosted PDF at https://www.math.auckland.ac.nz/~sgal018/ANTS/papers/Sorenson-Sorenson-Webster.pdf is a June 2020 submitted version, **not** the final published artifact; its front matter makes this explicit.

### 2021 addendum

Primary full HTML: https://arxiv.org/html/1907.08559v3

Version record: https://arxiv.org/abs/1907.08559v3

The full addendum, not merely its abstract, was available and inspected. Theorem 4.1 gives

\[
\log\widehat g(k)\sim C\,k/\log k,
\qquad C=\sum_{a\geq1}\frac{\log(1+1/a)}{a+1}
\approx0.7884305.
\]

Theorem 3.1 concerns \(\limsup\widehat g(k+1)/\widehat g(k)=\infty\). Neither substitutes \(g\) for \(\widehat g\). The addendum's Lemma 4.3 states an \(\exp(O(\sqrt{k}\log\log k))\) bound for a component of the density model. Its remaining additions are two computed values. Thus the improved coefficient and the square-root-scale factor estimates do not subsume the candidate.

The candidate's statement that only the updated abstract was checked can now be replaced by the narrower, accurate inspection account above. No full-paper proof audit of the density asymptotic was undertaken here.

## 4. Lower bounds and 2026 sources

S. V. Konyagin, *Estimates of the Least Prime Factor of a Binomial Coefficient*, Mathematika 46 (1999), 41–55, DOI https://doi.org/10.1112/S0025579300007555.

Its actual-minimum result is the lower bound \(g(k)>\exp(c(\log k)^2)\), as recorded in the inspected SSW introduction and the 2026 paper below. This comparison has an access qualification: the publisher abstract was accessible but its displayed formula was an image, and the full Konyagin paper was not inspected in this pass. No claim that all of its auxiliary results were screened is made.

A. van Doorn and Q. Tang, *Consecutive Integers Free of Certain Prime Factors*, 18 June 2026: https://arxiv.org/html/2606.19863v1 . The introduction explicitly identifies the binomial problem as EP-1095 and cites Konyagin's lower bound, but the paper's new theorem concerns EP-451. It is not an improved actual-minimum upper bound for EP-1095.

A. Eastwood's public repository and note: https://github.com/AlexanderEastwood/erdos-selfridge . The repository reports finite tabulation through 400 and expressly distinguishes witness checks from exhaustive minimality evidence. The inspected README and research-note HTML present computational work and density-model comparisons; no subsuming asymptotic actual-minimum upper theorem was located. This is a source report, not an independent replay or an assertion of editorial acceptance.

## 5. The established finite-sieve formulation

Kevin Ford, *Sieve Methods Lecture Notes*, Spring 2023, pp.12–13, Theorem 1.5 and Lemma 1.6: https://ford126.web.illinois.edu/sieve2023.pdf . These give the odd Brun truncation as a lower bound and bound its difference from the product density by the next elementary symmetric term. Theorem 1.7 is a broader quantitative pure-sieve consequence. These results are not restricted to a fixed number of exclusion classes per prime.

Terence Tao, *254A, Notes 4: Some Sieve Theory*, 21 January 2015: https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/ . Equation (5) gives the CRT count with remainder bounded by a constant times the product of the local residue counts; Exercise 9 gives the odd lower Brun sieve; equation (13) isolates the density term and discrepancy.

Here is the direct specialization, using the candidate's notation. Set

\[
P=\prod_{p\in F}p,\quad b(d)=\prod_{p\mid d}b_p,
\quad w(d)=b(d)/d,
\quad A_d(T)=Tw(d)+r_d(T),\quad |r_d(T)|\leq b(d).
\]

For even \(r\), take \(\lambda_d=\mu(d)\mathbf1_{\omega(d)\leq r-1}\). Brun's lower inequality immediately gives

\[
N(T)\geq T\sum_{j=0}^{r-1}(-1)^je_j(w)
-\sum_{j=1}^{r-1}e_j(b).
\]

The product-density remainder gives \(Q_{r-1}\geq\rho-e_r(w)\). The exact constant 1 in the CRT error follows directly from counting a single residue class in \([1,T]\). These are the candidate's finite inequalities. The nonnegative generating-function coefficient bound is another elementary step, not an assumption of random placement of the first survivor.

Thus standard finite-sieve machinery explains the candidate's finite theorem. Establishing whether this particular use already occurs in EP-1095 literature requires more than observing its classical ingredients.

## 6. Search boundary and remaining access gaps

The search covered accented and unaccented names of the Erdős–Selfridge function, upper-bound terminology, lcm and square-root terminology, Bonferroni/Brun terminology, references in the 2020/2021 papers, and targeted 2021–2026 searches. Many hits concerned unrelated Maker–Breaker games, odd covering systems, or factorial problems; those were excluded by their definitions.

This is not an exhaustive citation-index search, author correspondence, or a search of unpublished work. The Erdős Problems 1095 page returned HTTP 403 in this pass. Both MSP PDF endpoints produced no inspectable web-tool text, so the already frozen published PDF was used; the ANTS copy and arXiv HTML supplied independent access to related versions. The 1993 Erdős–Lacampagne–Selfridge publisher PDF was not obtained in this pass. Konyagin full text remains an explicit inspection gap. The underlying later-source results were classified by their hypotheses and mathematical objects, not presumed correct merely from abstracts.

## Recommended manuscript wording

“We apply Brun's pure sieve, with explicit CRT endpoint errors, to a selectively forced version of the Ecklund–Erdős–Selfridge lattice. This yields \(\log g(k)\leq\log L_k+(13/5+o(1))\sqrt{k}\), sharpening the secondary overhead in their displayed 1974 construction. A bounded literature comparison did not identify a later unconditional actual-minimum upper bound subsuming this estimate; no claim of priority or best-known status is made.”

Do not say that the finite sieve principle itself is new, that SSW proved this for actual \(g\), or that a density asymptotic controls the first surviving residue. Do not replace \(\log L_k\) by \(k\) with a claimed \(O(\sqrt{k})\) error merely from the PNT.
