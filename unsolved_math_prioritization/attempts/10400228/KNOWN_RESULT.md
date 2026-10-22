# Stoimenow Problem 12.23: affirmative, already in the literature

**Record:** 10400228 / AMR-103-0228. **Disposition proposed:** already_solved, **0/5**.
This is a source-status correction and an immediate interpretation of a known theorem, not an original proof attempt or a new signature estimate.

## Exact target and conventions

Ohtsuki's Problem 12.23, printed p.541 (PDF169), asks whether positive links with fixed signature σ have their maximal Euler characteristic χ bounded below. The following remark explicitly distinguishes general positive links from positive braid links and special alternating links, for which the answer was already known in 2002.

A positive link is an oriented link in S³ admitting a diagram whose crossings are all positive. This is broader than a positive braid closure. We use the classical signature with the convention that positive links have nonnegative signature, as in both the original question and the cited paper. With the opposite signature sign convention, replace σ by |σ| below.

A Seifert surface is a compact, embedded, oriented surface with oriented boundary L and no closed components; it may be disconnected. Let

\[
 \chi(L)=\max_{\partial F=L}\chi(F),\qquad
 b_1(L)=\min_{\partial F=L}\dim H_1(F;\mathbb Q).
\]

Removing closed components is essential to the meaning of maximal Euler characteristic. These are three-dimensional Seifert surfaces, not slice surfaces in a four-ball. The extrema exist: the possible first Betti numbers form a nonempty set of nonnegative integers, and χ(F)≤ the number of boundary components of L. No fixed number of link components or surface components is assumed.

Stoimenow's later paper, *Genus generators and the positivity of the signature* (2006), pp.2351–2352, explicitly uses this maximal Seifert-surface Euler characteristic and distinguishes the number of components from the number of split factors. This confirms the intended interpretation; imposing connectedness on every spanning surface would change the question.

## Published theorem

Baader, Dehornoy and Liechti, *Signature and concordance of positive knots*, Theorem 2, states for **all positive links**

\[
 \frac1{24}b_1(L)\le \sigma(L)\le b_1(L).\tag{A}
\]

The exact cited primary version is arXiv:1503.01946v2, 15 May 2018, p.1. It defines b₁ immediately below the theorem as the minimum over Seifert surfaces. The paper is published in *Bulletin of the London Mathematical Society* 50 (2018), no.1, 166–173, DOI 10.1112/blms.12124. Its Section 3 proves (A) for positive link diagrams using the Gordon–Litherland formula and planar graph coloring. The title's word “knots” does not restrict Theorem 2 to knots.

The first arXiv version (6 March 2015) has the weaker constant 1/48. That earlier theorem already gives the required boundedness. The revised version and the author's 2017 manuscript use 1/24. We record both, rather than importing the older constant from a later paper's citation. The final publisher-typeset PDF was not available for direct comparison; the complete primary arXiv versions and author manuscript were read, and the publication metadata was checked. A HAL copy is the revised arXiv manuscript with a repository cover, not a claimed final journal PDF.

## Immediate answer to the original question

Choose a surface F whose first Betti number is b₁(L). Every connected component of F has boundary, so H₂(F)=0 and

\[
 \chi(F)=b_0(F)-b_1(F).
\]

For a nonempty link, b₀(F)≥1. Therefore (A) gives

\[
 \boxed{\chi(L)\ge \chi(F)=b_0(F)-b_1(L)
       \ge 1-b_1(L)\ge 1-24\sigma(L).}\tag{B}
\]

This proves an affirmative answer for every fixed signature. It does **not** assume χ(L)=1−b₁(L), which can fail for disconnected surfaces, and it does not require the same surface to maximize χ and minimize b₁. One admissible Betti-minimizing surface is enough for the lower bound.

Using only the original 2015 theorem gives the independent weaker bound χ(L)≥1−48σ(L), already sufficient to classify the original problem as solved. Neither numerical constant is asserted to be optimal.

## Split links, zero signature and empty-link convention

The stated theorem includes split links. Disconnected spanning surfaces are allowed throughout, so adding split unknots does not invalidate (B). For example, the r-component unlink has σ=0, b₁=0 and χ=r; it illustrates why replacing b₀ by1 as an identity would be wrong. The inequality χ≥1−24σ still holds for every r≥1.

If σ=0, (A) forces b₁(L)=0. A minimizing surface is then a disjoint union of disks; in particular its χ is nonnegative and (for a nonempty link) at least1. There is no exception concealed at zero signature.

Links are ordinarily nonempty in this question. If the empty link is included with χ(empty)=0, it is one additional trivial case. The slightly weaker uniform bound χ(L)≥−24|σ(L)| includes it as well, so the answer to boundedness is unchanged.

No claim is made about all quasipositive or strongly quasipositive links. The paper itself explains why its positive-link bound cannot be extended to those larger classes indiscriminately. This packet also makes no claim that fixed signature gives finitely many positive link types; bounded χ is the exact target.

## Attribution and verification scope

All difficult mathematics is the credited Baader–Dehornoy–Liechti theorem. The Euler-characteristic implication is elementary and is supplied only to certify the scope match. The finite checker verifies this arithmetic with varying surface component count, the unlink control and the change of constants; it is not a new proof or an empirical validation of the signature theorem. Independent source/scope review is required before publication.
