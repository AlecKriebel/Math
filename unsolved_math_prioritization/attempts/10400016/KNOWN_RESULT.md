# Alternating-link signature and polynomial degrees: a credited resolution

**10400016 / AMR-103-0016, Ohtsuki Problem1.16. Recommended classification: already_solved.** This is a source-status correction and normalization audit of existing results, not a new solution. Separate adversarial review is pending. No substantive new proof attempt was used.

## 1. Exact original question

For an oriented alternating link \(L\), set
\[
 h(L)=\min\deg_l P_L(l,m),\qquad
 k(L)=\min\deg_a F_L(a^{-1},z).
\]
Ohtsuki's collection, printed p.392, asks whether
\[
 \sigma(L)\ \ge h(L)\ \ge k(L). \tag{1}
\]
Its Section1.2, p.390, uses unknot-normalized polynomials:
\[
 l^{-1}P_{L_+}-lP_{L_-}=mP_{L_0},\qquad P_{\bigcirc}=1,
\]
and the usual writhe-normalized Kauffman polynomial. Thus
\[
 k(L)=-\max\deg_a F_L(a,z). \tag{2}
\]
These are individual variable degrees, not degree spans. All orientations and split alternating links are included; no prime-knot restriction is introduced. The signature convention has value \(+2\) on the positive trefoil, as specified explicitly in Ito's exact treatment of this question.

**Known result.** Both inequalities in (1) hold. More precisely, if \(q(L)\ge1\) is the number of non-split factors in the split-union decomposition, then
\[
 h(L)+q(L)-1\le \sigma(L),\qquad k(L)\le h(L). \tag{3}
\]
The first inequality is Ito's Theorem5 in the inspected 2025 preprint, whose paper was published in2026. The second is Rutherford's Corollary5.4 in the inspected primary preprint, published in2006. Ito expressly identifies both parts of Ohtsuki Problem1.16 and cites Rutherford for the second.

## 2. Signature inequality: precise known mechanism

Tetsuya Ito's paper *A slice Cromwell inequality for homogeneous links* is published in **Bulletin of the Australian Mathematical Society114(1) (2026), 182–190**, DOI [10.1017/S0004972726101002](https://doi.org/10.1017/S0004972726101002), online2March2026. The retrieved full primary preprint is [arXiv:2504.13491v1](https://arxiv.org/abs/2504.13491), posted18April2025, with the slightly different title *A slice Cromwell inequality of homogeneous links*.

The relevant argument is not merely an inference from a common upper bound on two invariants. For a connected reduced alternating diagram, let \(B_i\) be the homogeneous blocks of its signed Seifert graph and let \(\epsilon_i\) be their signs. Ito's Theorem7 records the noncancelling monomial consequence of Cromwell's homogeneous-link proof:
\[
 P_L(v,z)\text{ contains a nonzero monomial with }v\text{-exponent }
 A=\sum_i\epsilon_i\operatorname{rank} B_i. \tag{4}
\]
Consequently \(\min\deg_v P_L\le A\).

In the positive-trefoil signature convention, the alternating-diagram signature formula used in Ito's proof is
\[
 \sigma(L)=w(D)-(d_+-d_-), \tag{5}
\]
where \(d_\pm\) count signed edges of a spanning tree of the Seifert graph. Each block contributes \(|V(B_i)|-1\) tree edges, so
\[
 w(D)-(d_+-d_-)
 =\sum_i\epsilon_i\bigl(|E(B_i)|-|V(B_i)|+1\bigr)
 =A. \tag{6}
\]
Thus (4) yields the signature inequality for each non-split factor. Ito notes a spurious factor of one-half in the displayed formula of the cited Traczyk reference; the corrected convention (5), rather than that misprint, is used here.

For \(L=L_1\sqcup\cdots\sqcup L_q\), the normalized split-union formula is
\[
 P_L(v,z)=\left(\frac{v^{-1}-v}{z}\right)^{q-1}
 \prod_{j=1}^qP_{L_j}(v,z). \tag{7}
\]
The Laurent coefficient ring is an integral domain, so minimum \(v\)-degrees add. Signature is additive under split union. It follows that
\[
 h(L)+q-1=\sum_jh(L_j)\le\sum_j\sigma(L_j)=\sigma(L).
\]
In particular, (3) implies the first part of (1). For an unlink with \(q\) components, the strengthened inequality is equality: \(h=1-q\) and \(\sigma=0\).

Theorem7's noncancellation and the alternating signature formula are credited knot-theoretic dependencies. The graph algebra and split-union deduction above were checked directly. This package does not claim a new proof of Cromwell's original skein construction.

## 3. Kauffman comparison and convention conversion

Dan Rutherford's *The Thurston–Bennequin number, Kauffman polynomial, and ruling invariants of a Legendrian link: the Fuchs conjecture and beyond* appeared in **International Mathematics Research Notices2006, Article78591**, DOI [10.1155/IMRN/2006/78591](https://doi.org/10.1155/IMRN/2006/78591). The inspected full primary preprint is [arXiv:math/0511097v1](https://arxiv.org/abs/math/0511097).

Its Corollary5.4 says, in its maximum-degree conventions,
\[
 \max\deg_a P_L^{R}(z,a)\le\max\deg_a F_L^{R}(z,a)
 \quad\text{for alternating }L. \tag{8}
\]
The proof uses Ng's alternating-link front construction and Rutherford's ruling criterion to show that the Kauffman upper bound on the Thurston–Bennequin number is attained. Applying the HOMFLY upper bound to that same representative gives (8). No comparison of two unrelated upper bounds alone is asserted.

Rutherford's HOMFLY variable is the inverse of Ohtsuki's \(l\), so
\[
 -\max\deg_a P_L^{R}=\min\deg_l P_L=h(L).
\]
His Kauffman polynomial is the Dubrovnik version. Its framing-variable degree distribution agrees with the corresponding standard Kauffman version; this conversion is also explicitly recorded in Kálmán's *Maximal Thurston–Bennequin number of +adequate links*, [arXiv:math/0610659v1](https://arxiv.org/abs/math/0610659), p.2, footnote2. The changes by coefficient units do not alter framing exponents. Negating (8) therefore gives \(h(L)\ge k(L)\).

As a separate source-level safeguard against a normalization mistake, Ito's p.3 footnote2 states the second inequality directly in the original \(F_L(a^{-1},z)\) convention and attributes it to Rutherford's Corollary5.4. The front construction and ruling theorem apply to links, not only knots. One can also reduce split links to their non-split factors: the normalized Kauffman split factor has maximum \(a\)-degree1, matching the minimum-degree shift minus one in (7).

## 4. Evidence limits and classification

The full original Ohtsuki PDF and full primary Ito, Rutherford and Kálmán preprints were obtained. Ito's entire short argument, Rutherford's definitions and exact corollary/proof, and Kálmán's convention explanation were read; the key Ohtsuki, Ito and Rutherford pages were visually inspected. Publisher metadata and Ito's institutional author publication list confirm the journal publication. The attempted Ito journal-PDF endpoint returned an access/HTML page, not a PDF. The final journal texts were not independently compared line by line to these primary preprints, and the numbering above is explicitly the inspected preprint numbering.

The arXiv versions inspected are not marked withdrawn. Later TeX-generated dates printed on the Rutherford and Kálmán PDF title pages do not replace their arXiv submission-version dates. No exhaustive re-audit of every classical ingredient or novel theorem is claimed.

The exact checks accompanying this record test Laurent degree inversion and split factors, the signed-block arithmetic in (6), the split-count shift, and the integer bound comparison behind (8). They are algebraic diagnostics, not a computation of knot polynomials or a substitute for the cited geometric theorems.

**Conclusion:** the imported open-triage status is stale. The exact bundled target is a credited known result; it should not count as a new campaign solution. This does not settle unrelated adjacent Whitehead-double degree questions, arbitrary nonalternating links, or stronger positivity conjectures discussed in the same sources.
