# Complete surfaces in the genus four moduli space

## Outcome and exact scope

**Status: unsolved.** No complete surface in the complex moduli space of smooth genus-four curves, and no proof excluding all such surfaces, was obtained. Five distinct approach families were examined. The results below are necessary conditions and obstructions to particular constructions. No new theorem resolving the target is claimed.

The target is the existence of an integral closed subvariety
\[
S\subset M_4(\mathbb C),\qquad \dim_{\mathbb C}S=2,
\]
proper over \(\mathbb C\). Here \(M_4\) is the coarse moduli space of **smooth connected projective curves**, with no marked points. The surface \(S\) is allowed to be singular. Since \(M_4\) is quasi-projective, a complete subvariety is projective. A compact complex analytic subvariety has the same interpretation after a projective embedding and Chow's theorem.

The source is Dawei Chen's Question 8, printed p. 3188 of [OWR]. The neighboring Question 9 concerns \(A_4\), a different problem. This distinction is important: [GMST], v3, resolves maximal compact dimensions for abelian varieties while its Table 5 still leaves the smooth-curve value between 1 and 2.

Finite level covers and resolution allow a hypothetical \(S\) to be replaced by a smooth projective surface \(B\) carrying a smooth genus-four family whose classifying map has two-dimensional image. That map need only be generically finite; it need not embed \(B\). Conversely, the proper image of any such family supplies a surface in \(M_4\). This equivalence does not require the original surface to be nonsingular. Neither a surface in \(\overline M_4\) meeting its boundary nor a surface in \(M_4^{\mathrm{ct}}\) consisting of nodal curves answers the question.

## Route 1 Affine strata and tautological positivity

Let \(D\subset M_4\) be the thetanull divisor and \(H\subset D\) the hyperelliptic locus. Theorem 3.1 of [FL] establishes that the three successive strata
\[
M_4\setminus D,\quad D\setminus H,\quad H
\]
are affine. Its Corollary 3.2 gives \(A^*(M_4)_{\mathbb Q}=\mathbb Q[\lambda]/(\lambda^3)\). We tested whether these facts improve the upper bound from 2 to 1.

Here is the precise geometric consequence. If \(S\) is a hypothetical integral complete surface, then:

1. \(S\not\subset D\).
2. \(S\cap D\) contains a complete curve, generically parametrizing nonhyperelliptic curves on a rank-three canonical quadric.
3. \(S\cap H\) is finite and nonempty, and every complete irreducible curve in \(S\cap D\) meets \(H\).

For completeness, these conclusions follow from a simple projective argument. The closed intersection \(S\cap H\) is proper and affine, hence zero-dimensional. If \(S\subset D\), choose a sufficiently general very ample curve section of \(S\) missing these finitely many points. It would be a complete curve in the affine variety \(D\setminus H\), a contradiction. Thus \(S\not\subset D\). If \(S\cap D\) were finite, the same argument using \(M_4\setminus D\) would give a contradiction. Consequently \(S\cap D\) contains a curve. Such a curve cannot be contained in the affine closed locus \(H\), and cannot avoid \(H\), because \(D\setminus H\) is affine. Its general point is therefore in \(D\setminus H\), whose canonical quadric is a cone. This argument applies also to singular \(S\).

These conditions are compatible with a surface. A projective curve can be the union of an affine open curve and finitely many points. There is no justification for treating the entire divisor \(D\) as affine merely because both displayed pieces are affine. Likewise, the vanishing of \(\lambda^3\) excludes complete threefolds, whereas \(\lambda^2\) is nonzero and is positive on a hypothetical complete surface.

Another false shortcut is \([S]=0\) in \(A^7(M_4)\). Rational equivalence in a nonproper ambient space does not make the degree of an ample line bundle on the proper surface vanish. There is no degree pushforward from arbitrary zero-cycles on \(M_4\) to a point. The elementary analogue is a closed point of \(\mathbb A^1\): it is proper although its class in \(CH_0(\mathbb A^1)\) is zero.

**Gap:** excluding the complete curve configuration inside \(D\), or deriving a stronger obstruction to its extension into \(M_4\), remains unproved. The elementary boundary-curve consequence substantially overlaps the prior report attached to related catalogue record 20000117 and is not presented as novel.

## Route 2 Satake sections and the Schottky divisor

Put \(X=\overline{J(M_4)}\subset A_4^*\), the closure in the projective Satake compactification. Its dimension is 9. The locus of products of an elliptic Jacobian and a genus-three Jacobian has closure
\[
B=\overline{A_1\times J(M_3)},\qquad \dim B=1+6=7,
\]
inside \(X\setminus J(M_4)\). These products are principally polarized decomposable abelian varieties, never Jacobians of smooth connected curves. This is different from being merely isogenous to a product.

Seven general hyperplanes in a projective embedding of \(X\) produce a surface. Their intersection with \(B\) is a nonempty zero-cycle: its degree is the positive degree of the 7-dimensional projective variety \(B\). Thus this surface meets the forbidden locus. Eight general hyperplanes can avoid \(B\) and the other boundary strata, but leave only a curve. This is the precise dimension threshold behind the familiar complete-curve construction.

We also tested the apparently stronger idea of taking a complete threefold \(Z\subset A_4\) and cutting it with the Schottky divisor to obtain a surface. The modern result [GMST, Section 9.1] says that every complete subvariety of \(A_4\setminus(A_1\times A_3)\) has dimension at most 2. Hence any such threefold meets \(A_1\times A_3\). That entire product locus is in the compact-type Jacobian locus, hence in the Schottky divisor. If the Schottky section of \(Z\) is an irreducible surface, it therefore contains a decomposable point and fails the target. If the section is reducible, this only proves that at least one component is bad; it does **not** exclude a different complete component lying entirely in \(J(M_4)\).

Conversely, general complete surfaces in the indecomposable locus \(A_4^{\mathrm{ind}}\) are possible: in \(A_4^*\), dimension 10, eight hyperplanes avoid the bad locus of dimension at most 7. But intersecting such a surface with the Schottky divisor normally gives dimension 1. Obtaining dimension 2 requires containment in that divisor, the missing condition rather than a consequence of dimension counting.

**Gap:** produce a compact two-dimensional component wholly in the smooth Jacobian locus, or show no such component exists. The results on \(A_4\), \(A_4^{\mathrm{ind}}\), and compact-type curves do not fill this gap.

## Route 3 Covering constructions and automorphisms

Consider a double cover of a smooth genus-two curve with two distinct branch points. Riemann--Hurwitz gives
\[
2g(C)-2=2(2\cdot2-2)+2=6,
\]
so the covering curve has genus 4. Moving the branch pair is a standard source of complete curves. We tested whether it can provide a complete surface.

For a fixed smooth projective curve \(C\), the ordered configuration space
\[
F(C,r)=C^r\setminus\bigcup_{i<j}\{p_i=p_j\}
\]
has no complete subvariety of dimension greater than 1. For \(r=1\) this is immediate. For \(r\ge2\), let \(T\) be a complete subvariety and project to its first coordinate. Each fiber is a complete closed subvariety of the affine variety \((C\setminus\{p\})^{r-1}\) with diagonals removed. That open subset is quasi-affine; a complete subvariety in it is zero-dimensional. Thus the projection has zero-dimensional fibers and \(\dim T\le1\). The same conclusion holds for unordered configurations by pulling back along the finite ordering cover.

Allowing the genus-two target to vary does not help on a complete base: its moduli image in the affine space \(M_2\) is constant. After finite base change the target is fixed. For a fixed target and branch divisor, the square roots determining double covers form a finite set. Consequently this construction has moduli image dimension at most 1.

A broader known obstruction is [Zaal, Theorem 6.6]: the nontrivial-automorphism locus in \(M_4(\mathbb C)\) contains no complete surface. Its mechanism can be checked directly in genus 4. After a finite cover choose a prime-order automorphism of order \(p\). If its quotient has genus \(h\) and \(r\) branch points, then
\[
6=p(2h-2)+r(p-1),
\]
which forces \(h\le2\). The arithmetic possibilities are
\[
(p,h,r)=(2,0,10),(2,1,6),(2,2,2),
(3,0,6),(3,1,3),(3,2,0),(5,0,4),(7,1,1).
\]
The last triple is not realizable: a cyclic cover cannot have exactly one branch point, since its nonzero local monodromy would have to sum to zero in \(\mathbb Z/7\). The other possibilities need not all define separate components; the list is only a Riemann--Hurwitz control.

The quotient-with-marked-branch-points map has finite fibers: the branch exponents are discrete, and the relevant \(p\)-th roots in the Picard group have finite ambiguity. A complete surface would therefore give a complete surface in some \(M_{h,r}\). For \(h=0\), the ordered branch space is affine. For \(h=1\), its image in \(M_{1,1}\) is constant; fixing the first marked point leaves a quasi-affine configuration space in a punctured elliptic curve. For \(h=2\), the image in \(M_2\) is constant and the configuration-space argument applies. The unramified \((3,2,0)\) case has only finite covering data over its fixed target. None yields a complete surface.

**Gap:** these arguments exclude automorphism-supported constructions, not surfaces with generically automorphism-free curves. A hypothetical surface may meet the automorphism locus along proper subsets. Non-Galois covers and families that cannot remain in one smooth Hurwitz space are not ruled out by this argument.

## Route 4 Prym compression of higher genus families

The known complete-surface construction in genus 8 suggests taking a Prym to reduce the abelian dimension to 4. For a double cover \(\widetilde C\to C\), where \(g(C)=4\) and there are two branch points, Riemann--Hurwitz gives \(g(\widetilde C)=8\), and the Prym has dimension \(8-4=4\). With the usual principal Prym polarization in this two-branch-point case, the construction maps to \(A_4\).

This numerical match does not make the Prym a smooth genus-four Jacobian. Two independent conditions are needed: the Prym image must have dimension 2, and every image point must lie in \(J(M_4)\).

Here is a direct diagnostic. Let \(P:S\to A_4\) be a morphism from an integral complete surface with two-dimensional image. Restrict an equation of the Schottky divisor to \(S\); it is a section of a positive power of the pulled-back Hodge line bundle. If this section is not identically zero, its zero locus has dimension at most 1. Indeed, after a finite level cover it is a nonzero section of a line bundle on an integral surface, so its zero scheme is an effective Cartier divisor or empty. The entire surface can be Jacobian-valued only if that section vanishes identically. One must additionally avoid the decomposable locus, which also lies on the Schottky divisor.

For the specific iterated genus-eight family in Zaal's Chapter 2, Theorem 7.6 of his thesis states that its Pryms are not all Jacobians of smooth genus-four curves. That theorem rules out that particular proposal; no universal claim about Prym families is being inferred from it. The note does not independently reprove the trigonal/Prym characterization used in that theorem.

**Gap:** find a different complete family whose Prym image has dimension 2, satisfies the Schottky relation identically, and avoids every decomposable fiber. Merely restricting the existing family to its Schottky zero locus normally loses a dimension. The positive-characteristic constructions discussed in [Choi] do not supply the required complex family.

## Route 5 Smoothing a compact type boundary surface

Choose two fixed nonisomorphic smooth genus-two curves \(C_1,C_2\). Over \(S_0=C_1\times C_2\), glue \(p\in C_1\) to \(q\in C_2\). The resulting stable curve has arithmetic genus \(2+2=4\) and exactly one separating node. The clutching map has finite fibers, since the two components are fixed, nonisomorphic, and have finite automorphism groups. Its proper image is thus a complete surface in the boundary \(\Delta_2\subset M_4^{\mathrm{ct}}\).

This is an explicit false positive for the original question: all its curves are singular. Its Torelli image is even constant, equal to \(J(C_1)\times J(C_2)\), since the gluing points do not affect the compact-type Jacobian.

We tested first-order simultaneous smoothing. On the ordered clutching cover, the normal smoothing line along this family is
\[
N=\operatorname{pr}_1^*T_{C_1}\otimes
\operatorname{pr}_2^*T_{C_2}.
\]
This follows from the node model \(xy=t\): rescaling the two local coordinates makes the smoothing parameter transform as the tensor product of the two tangent directions. See also [Polishchuk] for the formal clutching framework. The degree of \(N\) on either ruling of \(C_1\times C_2\) is \(-2\). A global section restricts to zero on every such fiber, since a negative-degree line bundle on a smooth projective curve has no nonzero section. Hence
\[
H^0(S_0,N)=0.
\]
Every first-order deformation of this fixed parameterized family has zero normal smoothing component. Pointwise smoothability of a node therefore does not provide a global first-order deformation moving this whole surface into \(M_4\).

**Gap:** this is a first-order obstruction for this clutching family. It is not a classification of all degenerations, and no conclusion about every higher-order deformation or every complete surface in the smooth locus is claimed. A different degeneration or a wholly different construction remains possible.

## What remains

The existence question itself is untouched: construct a proper two-dimensional subvariety wholly in \(M_4(\mathbb C)\), or prove that none exists, including singular subvarieties. The approaches establish useful rejection tests, but none proves a universal exclusion. The literature search is dated 4 October 2026 and is not a proof that no uncatalogued resolution exists. In particular, an upper bound of 2, a compact surface in \(A_4\), and a compact-type boundary construction must not be reported as solutions.

## References

- **[OWR]** B. Farb, U. Hamenstädt, A. Ranicki, organizers, *Surface Bundles*, Oberwolfach Reports 13 (2016), 3149–3195; problem session, Dawei Chen, Question 8, p. 3188. [DOI](https://doi.org/10.4171/OWR/2016/56); [official report record](https://publications.mfo.de/handle/mfo/3560).
- **[GMST]** S. Grushevsky, G. Mondello, R. Salvati Manni, J. Tsimerman, *Compact Subvarieties of the Moduli Space of Complex Abelian Varieties*, arXiv:2404.06009v3, 21 November 2025. Section 9.1; Section 9.2, especially Table 5 and the concluding discussion. [Versioned text](https://arxiv.org/html/2404.06009v3).
- **[FL]** C. Fontanari, E. Looijenga, *A perfect stratification of M_g for g ≤ 5*, Geometriae Dedicata 136 (2008), 133–143. Theorem 3.1 and Corollary 3.2. [DOI](https://doi.org/10.1007/s10711-008-9280-y); [author manuscript](https://webspace.science.uu.nl/~looij101/affinestrat3.pdf).
- **[Zaal]** C. G. Zaal, *Complete subvarieties of moduli spaces of algebraic curves*, University of Amsterdam thesis, 2005. Section 6.1; Lemmas 6.4–6.5 and Theorem 6.6; Section 7.2, especially Theorem 7.6. [University record](https://dare.uva.nl/id/502659b5-ce0a-492e-8042-b670058cb4fd); [thesis](https://pure.uva.nl/ws/files/3915897/36235_Thesis.pdf).
- **[Choi]** D. Choi, *Complete Subvarieties of M_{g,n} and a Lifting Problem*, arXiv:2304.08568v1. Introduction, Theorems 1.1–1.2 and Prior Results 1.1; characteristic-zero discussion in Section 4.3. [Versioned text](https://arxiv.org/html/2304.08568v1).
- **[Polishchuk]** A. Polishchuk, *Extended clutching construction for the moduli of stable curves*, arXiv:2110.04682v3, 19 October 2024. Introduction and Sections 2–4. [Versioned text](https://arxiv.org/html/2110.04682v3).
- **[Diaz]** S. Diaz, *A bound on the dimensions of complete subvarieties of M_g*, Duke Mathematical Journal 51 (1984), 405–408. [DOI](https://doi.org/10.1215/S0012-7094-84-05119-6). The dimension bound is also explicitly restated in [OWR] and [GMST].
