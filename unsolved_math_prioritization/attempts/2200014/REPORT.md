# Independent audit of the weighted parity conjecture

Audit date: 2026-10-11 UTC. Target: problem 2200014, AMR-021-0014, Conjecture 9 in Shapiro's polynomial problem list.

This is a separate AI-assisted mathematical audit of an AI-assisted proof reconstruction. Acceptance does not mean external human peer review, journal acceptance of the reconstruction, or formal proof-assistant certification. The full proof in PROOF.md is self-contained. The raw finite arithmetic certificates are supplemental and are omitted from this public edition.

## Verdict

**ACCEPT: the conjecture has a credited negative resolution.** Katkova, Shapiro and Vishnyakova (KSV), *In search of Newton-type inequalities* (2024), Section 5, explicitly disprove the target as their Conjecture 2. An independent exact reconstruction confirms a degree-24 counterexample with 22 real roots counted with multiplicity and parity bound 20. An explicitly specified integer perturbation has 22 distinct simple negative roots and the same parity bound, so the conclusion also holds if “real zeros” is read as distinct real zeros.

This audit credits KSV for the disproof and primitive family. The degree-24 specialization, root-splitting choice and supplemental exact checks are reconstructions of that published obstruction. No novelty, construction-priority or minimum-degree claim is made.

## Source scope and definitions

The checked original is [B. Shapiro, *Problems around polynomials — the good, the bad and the ugly*, arXiv:1503.05295v1, p. 4](https://arxiv.org/pdf/1503.05295v1#page=4). Conjecture 9 is credited there to J. Forsgård and B. Shapiro. Its hypotheses and statistic are:

- \(f(x)=\sum_{k=0}^n a_kx^k\), with **every** \(a_k>0\); hence \(n\) is the actual degree.
- Extend the coefficient sequence by \(a_{-1}=a_{n+1}=0\).
- Set \(c_k=(k+1)a_k^2-k a_{k-1}a_{k+1}\), for \(0\leq k\leq n\).
- Retain exactly the indices for which \(c_k>0\), in increasing order, and count changes between consecutive parities. Call the count \(v(f)\).
- The proposed inequality is that the number of real zeros is at most \(v(f)\).

The original displays the selected indices as \(k_1,\ldots,k_m\) but starts its parity sequence at \(i=0\). Since no \(k_0\) is defined, that lower limit is an indexing typo. The meaningful statistic is the parity-change count along the displayed, increasing selected sequence. The endpoints are always selected: \(c_0=a_0^2>0\) and \(c_n=(n+1)a_n^2>0\). No cyclic closing comparison is made. In our examples both endpoint parities are even, so adding a cyclic closing comparison would not change the count anyway.

The selection is **strictly positive**, unlike the unweighted Conjecture 10 beside it. Neither monicity nor constant term one is required. All real roots of a positive-coefficient polynomial must be negative: for \(x\geq0\), its value is positive.

The checked later source is [O. Katkova, B. Shapiro and A. Vishnyakova, *In search of Newton-type inequalities*, arXiv:2403.12200v1, Section 5, pp. 20–21](https://arxiv.org/pdf/2403.12200v1#page=20). Its Conjecture 2 explicitly points to Shapiro's Conjecture 9 and reproduces the weighted statistic. The paper's root-counting convention includes multiplicity (Notation 3, p. 3); its Section 5 argument also explicitly uses increasing multiplicity at −1. Shapiro's Conjecture 9 itself does not say “with multiplicity.” The simple-root witness below removes reliance on resolving that omission.

KSV's journal publication is *Journal of Mathematical Analysis and Applications* 538(1) (2024), article 128349, [DOI 10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349). The [author's publications list](https://staff.math.su.se/shapiro/Articles/) independently confirms this bibliographic information. The mathematics in this audit was checked against the identified arXiv PDF, not against an unavailable publisher PDF.

## Reconstruction of the primitive family

KSV begins with the degree-15 polynomial

\[
Q_{15}(x)=\frac{(x+1)^{13}}{720720}(38x^2-89x+83)
\]

and defines \(Q_n(x)=\int_{-1}^{x}Q_{n-1}(u)\,du\) for \(n>15\). Put \(t=x+1\) and define

\[
P_n(x)=t^{n-2}\{38t^2-11nt+n(n-1)\}.
\]

At \(n=15\), the quadratic bracket becomes \(38x^2-89x+83\), so \(P_{15}=720720Q_{15}\). Differentiation gives

\[
P_n'(x)=38nt^{n-1}-11n(n-1)t^{n-2}+n(n-1)(n-2)t^{n-3}
       =nP_{n-1}(x).
\]

Also \(P_n(-1)=0\). Thus uniqueness of the based primitive gives the exact normalization

\[
Q_n(x)=\frac{15!}{720720\,n!}P_n(x) \qquad(n\geq15).
\]

All normalization factors are positive. Scaling a polynomial by a positive scalar scales each \(c_k\) by its square and does not change roots or the selected indices.

The independent audit checker reconstructs \(Q_{15}\) from the rational coefficient expansion printed in KSV, performs all nine integrations up through \(Q_{24}\) in rational arithmetic, and compares each result with the binomial expansion of \(P_n\). It also verifies every derivative recurrence and basepoint. The closed form was checked independently rather than assumed.

## Complete degree-24 witness

At \(n=24\),

\[
P_{24}(x)=(x+1)^{22}(38x^2-188x+326).
\]

Its coefficients can be computed directly from

\[
a_k=326\binom{22}{k}-188\binom{22}{k-1}+38\binom{22}{k-2},
\]

where out-of-range binomial coefficients are zero. Independently, the checker uses the equivalent expansion

\[
a_k=38\binom{24}{k}-264\binom{23}{k}+552\binom{22}{k}.
\]

A further simplification is

\[
a_k=\binom{24}{k}((k-18)^2+2).
\]

The standalone authored proof in `PROOF.md` uses this identity and proves an explicit relative perturbation bound below 1/2000 for the specified distinct-root witness. It needs no full coefficient table or machine certificate. The independent checker verifies that proof's rational constants and all three robust sign comparisons as well.

For an additional cross-check, multiplying \(c_k/\binom{24}{k}^2\) by \((k+1)(25-k)\) gives

\[
-k^6+119k^5-5331k^4+114753k^3-1192272k^2+4620724k+2656900.
\]

This symbolic identity was checked exactly at all indices, including both endpoints.

The original audit also computed the complete 25-row integer coefficient and weighted-difference table. That raw finite certificate is supplemental and is omitted here. The symbolic coefficient identity and PROOF.md supply the self-contained mathematical proof; the exact sign and parity results below record the audit's additional cross-check.

Every coefficient is strictly positive and the leading coefficient is 38, so this is an admissible polynomial of actual degree 24. No \(c_k\) is zero. The selected indices are

\[
0,1,\ldots,16,20,21,22,23,24.
\]

There are 16 changes through indices 0 to 16, no change from the even index 16 to the even index 20, and four changes from 20 to 24. Hence \(v(P_{24})=20\).

The remaining quadratic has discriminant

\[
(-188)^2-4\cdot38\cdot326=-14208<0.
\]

It has no real roots and is nonzero at −1. Therefore \(P_{24}\) has exactly 22 real zeros counted with multiplicity, all at −1. Consequently \(22>20=v(P_{24})\), disproving the multiplicity reading.

## Explicit witness with distinct real roots

Let \(D=10^6\) and set

\[
R(x)=(38x^2-188x+326)\prod_{j=1}^{22}(Dx+D+j).
\]

This is \(D^{22}\) times the corresponding monic-linear-factor product, a positive scaling. It is an integer polynomial of actual degree 24 with leading coefficient \(38D^{22}>0\).

For an independently reproducible expansion, let \(b_j=D+j\) and let \(e_m\) be the degree-\(m\) elementary symmetric function in \(b_1,\ldots,b_{22}\), with \(e_0=1\). Newton's identities give the exact integer recurrence

\[
p_i=\sum_{j=1}^{22}b_j^i,\qquad
m e_m=\sum_{i=1}^{m}(-1)^{i-1}e_{m-i}p_i.
\]

Define \(B_k=D^k e_{22-k}\) for \(0\leq k\leq22\), and \(B_k=0\) otherwise. The coefficients of \(R\) are

\[
r_k=326B_k-188B_{k-1}+38B_{k-2},\quad 0\leq k\leq24.
\]

The independent audit checker applied this recurrence with arbitrary-precision integers. It checks exact divisibility in every Newton step, computes all 25 \(r_k\) and all 25 weighted differences, and verifies:

1. \(r_k>0\) at every index.
2. The weighted differences are negative exactly at \(17,18,19\), positive at all other indices, and zero nowhere.
3. The selected parity sequence has exactly 20 changes.

The full integer arrays are omitted supplemental certificates. PROOF.md instead proves coefficient positivity and negativity at indices 17, 18 and 19 through an explicit relative perturbation bound below 1/2000; these three signs already imply the sufficient bound \(v(R)\leq20\). For a separate identity check, the computed polynomial and the displayed factorized expression are evaluated exactly at each integer from −12 through 12. Both have degree at most 24, so agreement at these 25 distinct points proves equality.

Each linear factor has the root

\[
-1-\frac{j}{10^6},\qquad j=1,\ldots,22.
\]

These are 22 pairwise distinct negative rational numbers. The quadratic has negative discriminant, so it has no real root in common with any factor and contributes no real root. Thus these are all the real roots of \(R\), each simple. The checker additionally verifies all 22 rational root evaluations, the nonzero derivative at each one, and exact synthetic division down to \(D^{22}(38x^2-188x+326)\).

Therefore \(R\) has exactly 22 distinct real roots and exactly 22 real roots with multiplicity, while \(v(R)=20\). This is a counterexample under either convention. No numerical root solver or unspecified continuity argument is involved.

## Correction to finite-index quotient formulas

This issue does not invalidate the result, but it matters when reproducing a finite-degree example from KSV. Write \(q_k=a_k^2/(a_{k-1}a_{k+1})\). If a primitive shifts coefficient \(a_k\) to \(a_k/(k+1)\), then

\[
q_{k+1}(Q_{n+1})=q_k(Q_n)\frac{k(k+2)}{(k+1)^2}.
\]

Starting from KSV's seed values \(q_{10}=99/100\), \(q_9=140/243\), \(q_8=27/28\), the correct telescoped expressions are

\[
q_{n-5}=\frac9{10}\frac{n-4}{n-5},\qquad
q_{n-6}=\frac{14}{27}\frac{n-5}{n-6},\qquad
q_{n-7}=\frac67\frac{n-6}{n-7}.
\]

For example, the first product ends at \((n-6)(n-4)/(n-5)^2\), because the final coefficient index is \(n-5\); it does not end at \((n-1)(n+1)/n^2\). The latter endpoint and the resulting \((n+1)/n\) finite factors are printed on pp. 20–21 of the inspected arXiv:2403.12200v1. The publisher PDF was not inspected, so this correction is restricted to that arXiv version. They do not agree with the primitive recurrence or, already at \(n=15\), with the seed. The displayed limits \(9/10,14/27,6/7\) remain correct.

At \(n=24\), the exact ratios are

\[
q_{19}=\frac{18}{19}<\frac{19}{20},\qquad
q_{18}=\frac{133}{243}<\frac{18}{19},\qquad
q_{17}=\frac{108}{119}<\frac{17}{18}.
\]

For positive coefficients, \(c_k<0\) is equivalent to \(q_k<k/(k+1)\). These ratios agree with the supplemental direct integer checks. The audit does not depend on the misindexed displayed products or on any claimed least degree.

## Independence and acceptance checks

A separate exact-arithmetic checker was written for this audit. It did not read, import or run the earlier checker or its output, and no source-author code was executed. The program is not distributed in this edition. Its main expansion algorithms differ from the supplied checker: binomial/Taylor expansion plus rational integration for \(P_n\), and Newton identities plus 25-node identity verification for \(R\). Exact factor division and derivative tests verify root properties.

The audit records successful runs under Python 3.12.14 in isolated, no-bytecode mode, both without optimization and at optimization levels 1 and 2. Those historical exact-arithmetic runs are reported as verification metadata; the omitted program is not a dependency of the public proof.

The three outputs were byte-identical. Checks use explicit exceptions rather than Python assertions, so optimization cannot disable them. The arithmetic is exact; this is a finite arithmetic certificate and accompanying mathematical proof, not a formal proof-assistant development.

Only after independently producing the new certificate, a separate comparison checked the supplied certificate's full perturbed coefficient list and full weighted-difference list. Both match exactly. Its discriminant, signs, parity counts and root counts also match. These match results are recorded in SOURCE_VERIFICATION.json; the raw comparison artifact is not distributed.

**Acceptance conditions met:** exact conjecture match; strict coefficient hypothesis; actual degree; auxiliary endpoint coefficients; weighted rather than unweighted statistic; complete selected-index order; strict selection; no zero cases; parity calculation; both real-root conventions; exact root factorization; primitive normalization; correct attribution; and independent reproducibility.

**Scope limits:** this audit does not claim a minimal counterexample degree, new mathematical priority, a proof of unrelated conjectures, or verification of every result in KSV. This edition records the completed mathematical audit; it does not claim external human review or formal certification. Source PDFs and their rendered/extracted inspection material are not part of the authored mathematical deliverable.

## Source provenance

SOURCE_VERIFICATION.json records titles, public URLs, version dates, source-byte sizes and SHA-256 values, inspection history, publication evidence and access limitations. The two source PDF hashes match the supplied source manifest. Their existing retrieval history was inherited and is explicitly distinguished from this audit's new hash, text and visual checks. No fresh upstream PDF-byte match is claimed.
