# Simultaneous-core size moments: prior-result and normalization audit

Problem identifier: 20003198 / AIM-OTHER-0005. Audit date: 2026-10-11 UTC.

This is an AI-assisted, unrefereed authored mathematical audit and correction edition. Acceptance records an internal AI audit of prior-result status, normalization and written deductions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical audit, every written formula and example, the full correction patch and all substantive acceptance qualifications are retained. Executable code, raw partition or moment datasets, copied source PDFs or text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

## Decision

**Accept the prior-work and normalization corrections below. Do not accept a new solution of the arbitrary-order problem.**

The 2015 AIM request concerns unnormalized raw power sums over all simultaneous cores, not only cores with one modulus two. General mean, variance, and third central moment formulas are established prior results. Ekhad–Zeilberger's September 1, 2015 update explicitly changes the status of their displayed theorems to rigorously proved, on the strength of polynomiality and interpolation. Their older interior conjectural language does not override that update. The general formulas through order six, and consecutive-modulus formulas through order nine, must be credited as prior work with that stated status.

All-order polynomiality and effective finite computation were already available. Neither is a new contribution here. This audit does not supply or locate a compact coefficient formula uniform in arbitrary moment order and arbitrary coprime moduli. Moreover, the AIM source does not formally define “compact” or “pleasant,” so that stronger requirement must not be silently substituted for the original open-ended request. A fully solved label needs a declared acceptance criterion and an exact source match; this packet establishes neither a new solution nor a proof that such a compact formula remains unknown everywhere.

## 1. Exact object and domain

For positive integers a,b with gcd(a,b)=1, let C(a,b) be the finite set of partitions whose hook lengths are divisible by neither a nor b. Include the empty partition. Set

\[
N(a,b)=|C(a,b)|=\frac1{a+b}\binom{a+b}{a}
=\frac1a\binom{a+b-1}{a-1}.
\]

The AIM display is

\[
S_i(a,b)=\sum_{\lambda\in C(a,b)}|\lambda|^i.
\]

The letter i is an exponent; the sum index is “c an (a,b)-core”; the trailing 4 in the extraction is a page number. The following rotation/toggle sentence is context, not an extra moment condition. “Higher” naturally includes integer i≥2; this audit also records the lower orders. Define S_0=N as a counting convention, without relying on 0^0.

If X is uniform size on C(a,b), distinguish

\[
m_i=\mathbb E[X^i]=S_i/N,\qquad
\mu=m_1,\qquad c_i=\mathbb E[(X-\mu)^i].
\]

Thus c_0=1 and c_1=0. The unnormalized central sum is N c_i. The cumulants satisfy κ_1=μ, κ_2=c_2, κ_3=c_3, but κ_4=c_4−3c_2^2. Starting at order four, a central moment is not a cumulant. The generating function F(q)=Σ q^{|λ|} has S_i=[(q d/dq)^i F(q)]_{q=1}, not the ordinary i-th derivative, which instead gives a falling-factorial moment.

For min(a,b)=1, C(a,b)={∅}, N=1, and S_i=0 for i≥1. For gcd(a,b)>1 the core set is infinite; the finite-moment claims here do not extend to that domain. Polynomial continuations used in interpolation must not be mistaken for a uniform distribution on a nonexistent finite core set.

## 2. Two source corrections with exact witnesses

### 2.1 The AIM mean contains a printed sign error

Physical page 4 of the original AIM PDF visibly prints a+b−1 in the mean. This is not merely an OCR error or a missing vertical stroke in extraction. Johnson, Thiel–Williams, and the direct example below give the correct formula

\[
\mu=\frac{(a-1)(b-1)(a+b+1)}{24}.
\]

For (a,b)=(2,3), the only cores are ∅ and (1), so μ=1/2. The printed minus-one expression gives 1/3. The statement about the higher raw sums itself remains intact.

### 2.2 The full arXiv third-moment display omits normalization

The inspected 31-page full *Strange Expectations* PDF, arXiv:1508.05293v1, has the same unnormalized third-central-sum left side in Theorem 1.6 on physical pages 2 and 25. Its right side is

\[
T(a,b)=\frac{ab(a-1)(b-1)(a+b)(a+b+1)}{60480}
\left(2a^2b+2ab^2-3a^2-3ab-3b^2-3\right).
\]

The official FPSAC 2016 version, Theorem 1.6 on physical page 2 (printed page 1160), includes 1/N on the left. That normalization is mathematically correct:

\[
c_3=T(a,b),\qquad
\sum_{\lambda\in C(a,b)}(|\lambda|-\mu)^3=N(a,b)T(a,b).
\]

An exact counterexample to the unnormalized printed identity is (3,5). Its seven partitions are ∅, (1), (2), (1,1), (3,1), (2,1,1), and (4,2,1,1). Their sizes are 0,1,2,2,4,4,8 and their mean is 3. The central cubic sum is

\[
(-3)^3+(-2)^3+2(-1)^3+2(1)^3+5^3=90,
\]

whereas T(3,5)=90/7. This is a conclusive arithmetic disproof of the missing-denominator reading, rather than a numerical approximation. The corrected reading agrees with FPSAC and Ekhad–Zeilberger Theorem 3 and its worked example. No claim is made here that the inaccessible 2017 journal full text retains the arXiv typo.

## 3. Correct raw sums obtained from the prior formulas

Write

\[
V(a,b)=\frac{ab(a-1)(b-1)(a+b)(a+b+1)}{1440}.
\]

Then the formulas in the exact AIM normalization are

\[
\boxed{S_1=N\mu},\qquad
\boxed{S_2=N(\mu^2+V)},\qquad
\boxed{S_3=N(\mu^3+3\mu V+T)}.
\]

For all i≥0, binomial expansion gives the exact conversion

\[
S_i=N\sum_{j=0}^i\binom ij\mu^{i-j}c_j.
\]

Consequently the central moments printed by Ekhad–Zeilberger provide raw sums after including N and applying this conversion. For example

\[
S_4=N(\mu^4+6\mu^2V+4\mu T+c_4)
=N(\mu^4+6\mu^2\kappa_2+4\mu\kappa_3+3\kappa_2^2+\kappa_4).
\]

The (3,5) raw sums through order three are 21,105,657. Its central moments are c_2=6, c_3=90/7, c_4=726/7, while κ_4=−30/7. These distinct values make a useful normalization test.

## 4. What the proof mechanisms actually establish

### 4.1 Johnson and Thiel–Williams

Johnson's abacus maps a-cores to the rank-(a−1) charge lattice; his Theorem 2.10 and Lemma 3.4 express size as a quadratic function. Lemma 3.5 identifies simultaneous cores with a simplex subject to a congruence. Cyclic symmetry equidistributes the lattice cosets and preserves size. The proof of Theorem 3.7 uses weighted lattice-point polynomiality, then divisibility by the counting polynomial, to show that the normalized first moment has degree at most two in b. Corollary 3.8 identifies the mean.

Thiel–Williams transport the statistic to the dilated fundamental alcove (Corollary 6.8 and Theorem 6.9), prove the relevant symmetry (Lemma 6.11), and pass from coweight sums to coroot sums by the lattice index. In type A_(a−1) that index is a and the alcove is integral in the coweight lattice. Their Sections 7.1–7.3 develop the weighted enumeration and compute the variance. Section 7.5 computes the third central moment using symbolic evaluations at b=2,3,4,5 for all ranks. This audit inspected the mathematical setup and interpolation strategy; it did not execute their Mathematica, Maple, Normaliz, or other author software.

Two qualifications matter. First, weighted Ehrhart theory for a rational polytope generally gives a quasipolynomial; the type-A lattice change and integral-simplex argument are needed to obtain a polynomial. Second, the transported weight depends on b. One must expand it into polynomial terms in both b and the lattice coordinates, rather than blindly invoke a fixed-weight theorem without accounting for that parameter. The following reconstruction supplies both points explicitly.

### 4.2 Explicit type-A reconstruction and the divisibility step

This is an elementary audit of the established method, not a novelty claim. For a≥2, let z=(z_0,...,z_(a−1)) run over all nonnegative integer vectors with Σz_i=b. In fundamental-weight coordinates, the transported size is

\[
Q_{a,b}(z)=\frac12\sum_{i,j=1}^{a-1}(a\min(i,j)-ij)z_i z_j
-\frac b2\sum_{i=1}^{a-1}i(a-i)z_i
+\frac{(a^2-1)(b^2-1)}{24}.
\]

This follows by expanding a/2 ||x−bρ/a||²−(a²−1)/24 and using (C_A^−1)_(ij)=min(i,j)−ij/a. The z_0 coordinate is the slack variable. The cited core/alcove bijection and cyclic coset symmetry imply, for coprime a,b,

\[
S_k(a,b)=\frac1a\sum_{\substack{z_i\ge0\\\sum z_i=b}}Q_{a,b}(z)^k,
\quad
m_k(a,b)=\frac{1}{\binom{a+b-1}{a-1}}
\sum_{\sum z_i=b}Q_{a,b}(z)^k.
\]

These finite formulas are already a consequence of prior work. Their dimension and number of terms grow with the parameters; displaying them is not a new compact arbitrary-order coefficient formula.

Here is a direct check of the polynomial and denominator claims, avoiding any ambiguous sign conventions in a printed reciprocity formula. Use falling factorials z_i^{\underline{r_i}} and let R=Σr_i. The ordinary generating function identity

\[
\sum_{z\ge0}z^{\underline r}t^z=\frac{r!t^r}{(1-t)^{r+1}}
\]

gives

\[
\sum_{\sum z_i=b}\prod_i z_i^{\underline{r_i}}
=\Big(\prod_i r_i!\Big)\binom{b+a-1}{a-1+R}.
\]

After dividing by the weak-composition count, the right side becomes

\[
\Big(\prod_i r_i!\Big)\frac{b^{\underline R}}{a^{\overline R}}.
\]

For fixed a, expand Q_(a,b)^k in the falling-factorial basis in z with polynomial coefficients in b. Since Q has total degree at most two in (z,b), a basis term of z-degree R has b-coefficient degree at most 2k−R. The last display therefore proves that m_k is a polynomial in b of degree at most 2k. Equivalently, its unnormalized numerator is a polynomial of degree at most a−1+2k divisible by the counting polynomial. This argument also accounts for b-dependence of the weight.

By swapping a and b, m_k has degree at most 2k in either variable separately on the coprime domain. To justify joint polynomiality on this domain, choose 2k+1 distinct positive a-values A_j and let p_j(b) be their polynomials. Form P(a,b)=Σ_j L_j(a)p_j(b), where L_j are their Lagrange basis polynomials. For any positive A and infinitely many b coprime to A and all A_j, the polynomial in a at that b agrees with P at 2k+1 points; hence it agrees at A. The two polynomials in b at A therefore agree identically. It follows that P equals m_k on every coprime pair. Its degree is at most 2k in each variable and at most 4k in total. Symmetry follows from equality on the coprime domain. This supplies the step behind the September 2015 feedback, including the coprimality issue.

The central moment c_k=Σ_j binom(k,j)(−μ)^(k−j)m_j obeys the same separate degree bounds, since μ has degree at most two in either variable. These bounds are upper bounds, not claims of exact degree in every degenerate case. A sharper total-degree bound is neither needed nor claimed here.

**Crucially, these bivariate polynomial assertions concern normalized moments.** The raw S_k=N m_k has fixed-a degree at most a−1+2k, but no fixed total-degree bivariate polynomial description follows. The growing rational-Catalan factor must be retained. For k≥1, along (a,b)=(n,n+1), convexity gives S_k≥N μ^k; N is a Catalan number and grows faster than any polynomial in n. Thus S_k itself cannot be a single bivariate polynomial.

### 4.3 What interpolation does and does not certify in this audit

The degree bounds make finite interpolation a rigorous method when the sample set is unisolvent, its values are exact, and the proposed polynomial matches all required data. They do not certify an unspecified finite sample automatically. The September 1 feedback gives the bound 2k in each variable, hence total at most 4k; the v2 front page says all the paper's theorems are proved. Those status claims must be reported faithfully.

This audit has not reconstructed an exact unisolvent interpolation certificate for every coefficient of Ekhad–Zeilberger's fourth-through-sixth formulas or their order-nine specialization. It must not describe those formulas as still conjectural merely because it did not redo that computation; nor may it describe its own finite tests as an independent all-parameter proof of them. In particular, c_5 and c_6 were tabulated in the checks but their printed polynomial coefficients were not independently transcribed or certified.

## 5. Version and status reconciliation

- Ekhad–Zeilberger arXiv:1508.07637v2 bears September 1, 2015 and has an added update on physical page 1. The original internal conjectural discussion on pages 2 and 11 was not rewritten. The update takes precedence when reporting the authors' stated theorem status.
- The update's hyperlink labeled as the Thiel–Williams paper points to arXiv:1502.07934, which is Johnson. The actual Thiel–Williams arXiv identifier is 1508.05293.
- The retrieved Thiel–Williams PDF has an arXiv v1 stamp dated August 21, 2015, but its title-page compilation date and PDF creation metadata say November 3, 2021. This is a version/compilation distinction, not evidence of a new arXiv submission; the arXiv record lists v1 only. The precise bytes are pinned in SOURCES.json.
- The 2017 journal article is *Strange expectations and simultaneous cores*, Journal of Algebraic Combinatorics 46(1), 219–261, DOI 10.1007/s10801-017-0754-6. Its publisher abstract explicitly includes all-moment polynomiality. The publisher's PDF request returned a subscription-preview HTML page, not a PDF. The full journal text and its exact theorem numbering were not independently inspected here; secondary indexed references to Theorem 1.7 are not used as the mathematical proof source.
- The official FPSAC conference PDF is an extended abstract, distinct from the full 2015 preprint and the 2017 journal article. Its Theorem 1.6 has the correct denominator. The DMTCS landing page's 2020 publication/deposit date does not change the conference year 2016.
- Ekhad–Zeilberger's separate limit-law challenge must not be called presently open from the 2015 PDF alone. The authors' webpage has a March 31, 2020 update crediting Even-Zohar, and arXiv:2003.13671 describes the resulting Watson-law theorem. That theorem is a different target from exact arbitrary-order finite-parameter formulas; its proof was not audited here.

## 6. The modulus-two candidate and the remaining target

The title referring to “one modulus two” describes a narrow candidate, not the original AIM scope. The known staircase description gives, for b=2m+1,

\[
S_i(2,2m+1)=\sum_{r=0}^m\left(\frac{r(r+1)}2\right)^i.
\]

For integer i≥1, the binomial theorem and the Bernoulli convention t e^(xt)/(e^t−1)=Σ B_j(x)t^j/j! yield

\[
S_i(2,2m+1)=2^{-i}\sum_{j=0}^i\binom ij
\frac{B_{i+j+1}(m+1)-B_{i+j+1}(0)}{i+j+1}.
\]

This is a correct immediate all-order special-case calculation. Its degree in m is 2i+1 and leading coefficient is 1/(2^i(2i+1)); advancing m adds exactly the next triangular-number power. It is not a solution for general coprime a,b, and no novelty is accepted. The fixed-modulus square-of-a-uniform limit is also distinct from Watson's U² law, despite the similar notation.

The constructive all-order lattice sum and degree-bounded interpolation are already known. A meaningful future target would have to specify an additional requirement, for example an explicit coefficient or cumulant expression at arbitrary order with controlled complexity, or a new structural/dynamical explanation. Merely reproving polynomiality, converting central moments to raw sums, or packaging staircase power sums does not meet that bar. A bounded search cannot certify that no later formula exists.

## 7. Independent checks and acceptance boundary

The historical authored Python checker, which is not distributed in this edition, used exact rational arithmetic and no author packages. It enumerated gap-poset ideals, reconstructed their partitions, directly checked every hook condition, verified the rational-Catalan count, and compared mean, variance, third and fourth central formulas for every coprime 1≤a≤b≤10: 32 pairs and 9,246 partitions. Selected smaller pairs also compared the entire size distribution with the coweight quadratic, including its a-fold multiplicity. The raw second- and third-moment conversions passed. The program ran under ordinary Python, -O, and -OO without reliance on assert statements. These historical checks were not rerun during editorial preparation.

These are finite supporting checks, not proofs of the universal formulas or a replacement for the cited mathematical mechanisms. The exact (3,5) counterexample, the binomial conversions, and the elementary polynomiality reconstruction are separately written mathematical arguments. No formal verification, author-code replication, full-paper inspection, or new arbitrary-order acceptance is claimed.

## References

1. AIM, *Problems for 2015 AIM Workshop on Dynamical Algebraic Combinatorics*, May 29, 2015, Problem 2.2, physical page 4. https://aimath.org/pastworkshops/dac_preworkshop.pdf . Authenticated archived retrieval: https://web.archive.org/web/20230414041754id_/https://aimath.org/pastworkshops/dac_preworkshop.pdf .
2. Paul Johnson, *Lattice points and simultaneous core partitions*, arXiv:1502.07934v2, June 23, 2015; especially Sections 2.5 and 3. https://arxiv.org/abs/1502.07934v2 .
3. Marko Thiel and Nathan Williams, *Strange Expectations*, arXiv:1508.05293v1; Theorems 1.4–1.6, Sections 6.3–6.5, 7.1–7.5, 8.1. https://arxiv.org/abs/1508.05293v1 .
4. Marko Thiel and Nathan Williams, *Strange Expectations and Simultaneous Cores*, FPSAC 2016, DMTCS proceedings, 1159–1170. https://fpsac2016.sciencesconf.org/file/final_102.pdf ; https://doi.org/10.46298/dmtcs.6364 .
5. Shalosh B. Ekhad and Doron Zeilberger, *Explicit Expressions for the Variance and Higher Moments of the Size of a Simultaneous Core Partition and its Limiting Distribution*, arXiv:1508.07637v2, September 1, 2015. https://arxiv.org/abs/1508.07637v2 .
6. Marko Thiel and Nathan Williams, public feedback dated September 1, 2015. https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/stcoreFeedback.html .
7. Ekhad–Zeilberger author webpage, including March 31, 2020 update. https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/stcore.html .
8. Marko Thiel and Nathan Williams, 2017 journal article, publisher metadata and abstract only. https://doi.org/10.1007/s10801-017-0754-6 .
9. Chaim Even-Zohar, *Sizes of Simultaneous Core Partitions*, arXiv:2003.13671; abstract/status only, not a proof audit. https://arxiv.org/abs/2003.13671 .
