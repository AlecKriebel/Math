# Independent full audit of the binomial LP counterexample

**Verdict: PASS_COMPLETE_COUNTEREXAMPLE.** The candidate gives a negative answer to the exact augmented-image hypothesis asked about in Takagi's OWR Question 8. Recommend **claimed_solved, 1/5**, subject to the standing distinction between an AI-reviewed proof and human peer review. No mandatory mathematical correction was found. Historical priority is unconfirmed.

Reviewed on 30 September 2026 by a separate GPT-6 Astra agent at xhigh effort. Frozen CANDIDATE.md SHA-256:
**1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf**.

## Exact primary condition

I independently read the relevant [OWR 21/2009](https://ems.press/content/serial-article-files/46224) contribution and visually inspected printed pp. 1138–1139. Proposition 5 requires an optimal point whose augmented image differs from that of every other distinct optimal point. Question 8 asks whether a monomial-free binomial ideal with a minimal binomial generating system always satisfies this condition. The condition is also stated in Proposition 2.1 and Question 2.2 of the complete [Shibuta–Takagi primary preprint](https://arxiv.org/abs/0810.1278v3).

This is an existence assertion for a **singleton fiber among optimal points**, not an assertion that all optimizers have a common image, and not merely uniqueness of the optimizer. The source uses nonnegative rational coordinates and nonstrict inequalities. The full matrix includes both the monomial-exponent block and the $(I_r\ I_r)$ block. No regular-sequence or space-monomial-curve condition is imposed in the question; those are hypotheses of separately stated positive results.

Since the objective is the sum of the bottom coordinates of the augmented image, a feasible point in the fiber of an optimal point is automatically optimal. The candidate's equivalent feasible-fiber interpretation is therefore correct.

## Ideal hypotheses, including localization

The cyclic generators
\[
x_1y_2-x_2y_1,\qquad
x_2y_3-x_3y_2,\qquad
x_3y_1-x_1y_3
\]
are the three minors of a generic $2\times3$ matrix, with one sign reversed. They are legitimate binomials over every characteristic-zero field, with coefficient one and two nonzero exponent vectors. The ideal is a nonzero proper ideal inside the homogeneous maximal ideal.

Evaluation of all variables at one proves absence of nonzero monomials in the polynomial ideal. This argument is correctly limited to that polynomial ring: evaluation at this torus point need not extend to localization at the origin. The stronger localization claim nevertheless follows from the independently verified primeness below. Since no variable belongs to the prime ideal and it is contained in the origin's maximal ideal, no monomial can enter its localization there. If a denominator outside that maximal ideal multiplied a monomial into the prime ideal, primeness would force either the monomial or that denominator into the prime ideal, both impossible.

The generators are minimal for an elementary graded reason. Their six degree-two monomials are all distinct, so the three quadrics are linearly independent. The degree-two part of the ideal has dimension three, and all higher-degree terms lie in the maximal ideal times the ideal. Thus their classes form a basis of $\mathfrak a/\mathfrak m\mathfrak a$. This gives minimality in the polynomial ring and, after localization and reduction modulo the residue field, minimality at the origin. Nonconstant polynomial coefficients or local denominators cannot reduce the number of generators.

The prime-ideal proof is complete. Under
\[
x_i\mapsto sz_i,\qquad y_i\mapsto tz_i,
\]
two monomials have equal images exactly when their three column totals and total $x$-degree agree. Given distinct allocations $\alpha,\alpha'$ with those data, choose an excess coordinate $j$ and a deficit coordinate $i$. The first monomial contains $x_jy_i$: its $x_j$ exponent is positive, while its $y_i$ exponent is at least $\alpha_i'-\alpha_i>0$. Replacing this product by $x_iy_j$ is one of the three minor relations and reduces the $\ell^1$ distance of the allocations by two.

Induction identifies all monomials in each image fiber modulo the ideal. Group a polynomial in the map's kernel by its distinct image monomials; linear independence in the target polynomial ring says the coefficients in each group sum to zero. Each group is a sum of the just-verified monomial differences. Thus the kernel equals the ideal, and the quotient is a subring of a domain. No unproved determinantal primeness theorem is needed.

## Reconstructed LP and its entire optimal set

I reconstructed every matrix column directly from the displayed binomials. The resulting nine rows agree with the candidate. In particular the first six inequalities are
\[
\begin{aligned}
\mu_1+\nu_3&\le1,& \mu_2+\nu_1&\le1,& \mu_3+\nu_2&\le1,\\
\mu_3+\nu_1&\le1,& \mu_1+\nu_2&\le1,& \mu_2+\nu_3&\le1,
\end{aligned}
\]
and the remaining three are $\mu_i+\nu_i\le1$.

Summing the latter inequalities gives objective at most three. This is also an exact nonnegative dual certificate, using coefficient one on those three rows and zero elsewhere. The rational feasible point $(1,1,1,0,0,0)$ attains three, so the maximum exists and equals three.

At every optimizer, all three pair caps are saturated; otherwise their sum would be strictly below three. Substitution $\nu_i=1-\mu_i$ into the first three inequalities gives
\[
\mu_1\le\mu_3\le\mu_2\le\mu_1.
\]
Hence the complete rational optimal set is precisely
\[
F=\{(t,t,t,1-t,1-t,1-t):t\in\mathbb Q,\ 0\le t\le1\}.
\]
The unused inequalities impose no additional restriction: direct substitution makes all nine rows equal to one.

For every point of this segment, including its endpoints, one of the two rational endpoints is a distinct optimizer with the same image. Therefore **no optimizer has a singleton augmented-image fiber**. This proves the exact negation of the source assertion. Rationality does not create an exceptional point or remove the second optimizer.

The rank-five and one-dimensional-kernel assertions follow independently: the three bottom homogeneous equations force $\nu=-\mu$, and the cyclic top equations force all three $\mu_i$ equal. The image of the entire optimal segment is indeed the singleton $\{\mathbf1_9\}$, but every fiber over that image is the whole segment. The candidate consistently distinguishes these facts.

## Scope, attribution, and current literature

The ideal and determinantal theory are classical. The conclusion is solely the elementary negative answer to the stated LP-fiber question. It neither contradicts the conditional threshold theorem nor depends on computing any log canonical threshold.

I compared the relevant LP in the [published LaClair article](https://doi.org/10.1007/s10801-025-01439-x) with the original program. The extra vertex-subset inequality for all three vertices bounds total edge weight by two and excludes the segment above. Remark 3.15 expressly discusses dropping those additional constraints. This later program cannot be substituted for the 2009 LP. The candidate accurately acknowledges related determinantal-threshold results.

The broader [Blanco–Encinas procedure](https://arxiv.org/abs/1405.3942) concerns a different computation and does not make the source's particular fiber hypothesis automatic. The primary introduction and its scope were inspected; this review does not certify the complete analytic proofs of either later paper.

A bounded primary-source search was performed. No first-discovery claim is justified by that search, and the verdict does not certify that the numbered question had no earlier answer. These qualifications do not affect the explicit mathematical counterexample.

## Exact verification

The submitted checker passes **3,045** assertions and reproduces the frozen receipt byte for byte. It considers all **5,005** six-row active-basis selections, finds the **15** polytope vertices and the two optimal endpoints, and verifies finite straightening instances and the central-product cancellation.

My independently written standard-library checker passes **5,368** assertions. It reconstructs the augmented matrix, verifies two distinct dual certificates, checks rank and kernel, tests rational non-singleton fibers including endpoints, exhausts a separate saturated rational grid, and verifies all paired monomial allocations of column-total degree at most five by exact minor moves.

The proofs above establish the unbounded algebraic claims and the whole optimal segment; these are not inferred from finite sampling. All reviewed author files remain unchanged. The self-contained publication file list, preserved snapshot, hashes, and source-read receipt are in review_summary.json.
