# Stoimenow's Kauffman minimum-degree bounds: signed-positive partial result

Problem 10400018 / AMR-103-0018, priority rank 1250. First substantive attempt, 1/5. Checked 10 October 2026 UTC. **Partial only: both universal clauses remain unresolved.**

This AI-assisted, unrefereed proof-only edition includes the complete accepted arguments and their [mathematical audit](MATHEMATICAL_AUDIT.md). Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No historical novelty is claimed.

## 1. Exact target and outcome

Use the original Kauffman normalization

\[
F_L(a,z)=a^{-w(D)}\Lambda_D(a,z),\qquad F_O=1,
\]

with the plus skein relation for \(\Lambda\), and define

\[
d(L)=\min\deg_a F_L(a^{-1},z)=-\max\deg_a F_L(a,z).
\]

The two questions are

\[
d(L)\le 1-\chi(L)\quad\hbox{for every oriented link }L,
\qquad d(K)\le2u(K)\quad\hbox{for every knot }K.
\]

Here \(\chi\) is the maximum Euler characteristic of compact, embedded, oriented Seifert surfaces in \(S^3\) with the prescribed oriented boundary and **no closed components**. Surfaces may be disconnected. Thus \(1-\chi(K)=2g(K)\) for a knot. Smooth slice genus is denoted by \(g_4\).

The original statement and surrounding caveat were visually rechecked in Ohtsuki, printed pp.392–393/PDF pp.20–21 [O]. Tanaka's Proposition 5.1 [T] already proves both knot bounds when the Kauffman bound for maximal Thurston–Bennequin number is sharp. That is prior work, not a result of this attempt.

This attempt proves the following elementary extension from established results:

**Theorem A.** Suppose
\[
J=P_1\#\cdots\#P_p\#\overline{Q_1}\#\cdots\#\overline{Q_q},
\]
where all \(P_i,Q_j\) are positive knots, a bar denotes mirror image, and either list may be empty. A connected sum with no summands denotes the unknot. Then, in Rasmussen's convention \(s(T(2,3))=2\),
\[
\boxed{d(J)=s(J)-\sum_{j=1}^{q}\operatorname{span}_aF_{Q_j}.}
\tag{1}
\]
Consequently \(d(J)\le2g_4(J)\le2g(J)\) and \(d(J)\le2u(J)\). Every split union of such knots satisfies the link Euler-characteristic bound.

The class contains knots with positive \(d\) and arbitrarily large failure of Kauffman-bound sharpness. The exact family is established in Section 5. These are consequences assembled from credited prior theorems; no historical-firstness claim is made.

## 2. Polynomial identities and normalization

All degree calculations take place in the Laurent polynomial domain \(\mathbb Z[z^{\pm1}][a^{\pm1}]\). For nonzero Laurent polynomials the maximum and minimum \(a\)-degrees of a product are the sums of the corresponding degrees: the extremal coefficients multiply nontrivially in an integral domain. This observation rules out an implicit cancellation assumption in the following formulas.

The normalized Kauffman polynomial has the standard identities
\[
F_{K\#J}=F_KF_J,\qquad F_{\overline K}(a,z)=F_K(a^{-1},z).
\tag{2}
\]
Multiplicativity can also be obtained by applying the defining skein recursion in the first one-string summand, leaving the second summand fixed. The unknot and curl terminal values are the same terminal values multiplied by \(F_J\); uniqueness of the skein invariant gives (2). This proof does not assume anything about genus or unknotting number.

Write \(M(K)=\max\deg_aF_K\), \(m(K)=\min\deg_aF_K\), and \(b(K)=M(K)-m(K)\). Equation (2) gives
\[
d(K\#J)=d(K)+d(J),\qquad
d(\overline K)=m(K)=-d(K)-b(K).
\tag{3}
\]
In particular,
\[
d(K\#\overline K)=-b(K)\le0.
\tag{4}
\]

The normalization of a split unknot must be treated separately. Applying the plus skein relation at a curl gives
\[
(a+a^{-1})\Lambda_D
=z\bigl(\Lambda_{D\sqcup O}+\Lambda_D\bigr).
\]
Thus
\[
\delta(a,z)=\frac{a+a^{-1}}z-1,\qquad
F_{L_1\sqcup L_2}=\delta F_{L_1}F_{L_2}
\tag{5}
\]
for a split union. The second formula follows by the same skein recursion in one split factor, starting with the just-established unknot factor. The writhe normalization multiplies correctly because the diagrams are disjoint. Crucially,
\[
\min\deg_a\delta(a^{-1},z)=-1,
\]
with nonzero extremal coefficient \(z^{-1}\). Therefore an \(r\)-fold split union satisfies
\[
d(L_1\sqcup\cdots\sqcup L_r)=\sum_{i=1}^r d(L_i)-(r-1).
\tag{6}
\]
For the \(r\)-component unlink this yields \(d=1-r\), agreeing with \(\chi=r\). There is no imposed connected-surface convention and no missing split-union correction.

## 3. Proof of the signed-positive knot theorem

For a positive knot diagram \(D\), let \(c\) be its number of crossings and \(v\) its number of Seifert circles. Positive diagrams are +adequate and their +state circles are their Seifert circles [K, Definition 2 and following discussion, PDF p.3]. Kálmán's Corollary 6 [K, PDF p.8], recovering Tanaka's positive-knot result, gives
\[
d(P)=c-v+1.
\tag{7}
\]
The variable convention in [K] is explicit: minimum degree in \(v=a^{-1}\) equals minus maximum degree in \(a\), exactly the \(d\) used here. Rasmussen's positive-diagram calculation [R, Section 5.2, PDF p.14] gives
\[
s(P)=c-v+1=2g(P)=2g_4(P).
\tag{8}
\]
These are cited published results, not new positive-knot proofs. In particular \(d(P)=s(P)\) for every positive knot, including positive knots that are not closures of positive braids.

Rasmussen's Theorems 1 and 2 give \(|s(K)|\le2g_4(K)\), additivity under connected sum, and sign reversal under mirroring [R, PDF p.1; the mirror formula is also Proposition 3.9]. Knot orientation reversal does not change \(s\), so mirror image rather than inverse oriented knot causes no ambiguity here. Combining these facts with (3) yields
\[
\begin{aligned}
d(J)
&=\sum_i d(P_i)+\sum_j d(\overline{Q_j})\\
&=\sum_i s(P_i)-\sum_j s(Q_j)-\sum_j b(Q_j)\\
&=s(J)-\sum_j b(Q_j).
\end{aligned}
\]
This proves the exact identity (1). Each span is nonnegative, so
\[
d(J)\le s(J)\le |s(J)|\le2g_4(J).
\]
Pushing a Seifert surface into the four-ball proves \(g_4(J)\le g(J)\). A sequence of \(u(J)\) crossing changes to the unknot gives an immersed disk with that many double points; resolving each double point by an orientable local handle gives an embedded surface of genus at most \(u(J)\). Thus \(g_4(J)\le u(J)\), proving both requested bounds for \(J\).

No assertion of unknotting-number additivity occurs. The inequality \(u(K\#J)\le u(K)+u(J)\) has the wrong direction to combine arbitrary factorwise lower bounds for \(u\). The concordance invariant \(s\) is what supplies the necessary lower bound here.

## 4. Split-link Euler characteristic, with disconnected surfaces

**Lemma B.** For an oriented split union,
\[
\chi(L_1\sqcup L_2)=\chi(L_1)+\chi(L_2).
\tag{9}
\]

**Proof.** Let a sphere \(S\) separate the links. Take a spanning surface \(F\) with no closed components and make it transverse to \(S\), with boundary disjoint from \(S\). Their intersection consists of finitely many circles. Pick a circle innermost on \(S\); its disk on \(S\) has interior disjoint from \(F\). Compress \(F\) along that disk, pushing the two new disks slightly off \(S\). This removes the circle and preserves the oriented boundary. Compression adds 2 to Euler characteristic. If it creates a closed component, discard that component. At most one closed component is created because the original component had nonempty boundary. A closed oriented surface has Euler characteristic at most 2, so this discard does not lower the Euler characteristic below its precompression value. The remaining surface still has no closed components.

Repeat until the surface is disjoint from \(S\). It is then the disjoint union of spanning surfaces for \(L_1\) and \(L_2\), so
\(\chi(F)\le\chi(L_1)+\chi(L_2)\).
Conversely, maximal-Euler surfaces for the separate links can be chosen in their respective balls: apply the same compression procedure to the ball-boundary sphere and discard components in the empty ball. Their disjoint union realizes the sum. This proves (9), and induction proves its \(r\)-factor version. \(\square\)

Now let \(L=J_1\sqcup\cdots\sqcup J_r\), each \(J_i\) a knot from Theorem A. Equations (6), (9), and Theorem A give
\[
\begin{aligned}
d(L)
&=\sum_i d(J_i)-(r-1)\\
&\le\sum_i2g(J_i)-(r-1)\\
&=1-\sum_i(1-2g(J_i))=1-\chi(L).
\end{aligned}
\]
The proof actually shows split-union closure of the Euler-characteristic bound for any link factors already known to satisfy it. The theorem above only claims the explicitly established knot factors.

## 5. Positive degree with unbounded Kauffman-bound defect

Let \(T=T(2,3)\) be the right-handed trefoil and \(Q=T(3,4)\) the positive torus knot. Set
\[
K_{n,m}=\#^{n}T\ \#\ \#^{m}\overline Q,\qquad m\ge1,\quad n\ge0.
\]

The standard positive diagrams give \(g(T)=1\), \(g(Q)=3\), and hence \(d(T)=2\), \(d(Q)=6\), \(s(T)=2\), \(s(Q)=6\) by (7)–(8). Ng's explicit discussion of the negative \((4,-3)\) torus knot [N, printed p.428/PDF p.2] gives
\[
\overline{\mathrm{tb}}(\overline Q)=-12,
\qquad d(\overline Q)-1=-11.
\tag{10}
\]
Ng uses the inverse framing-variable convention for the Kauffman polynomial, so his minimum degree is our \(d\). His identification is the negative torus knot, independent of potentially ambiguous table chirality. Thus \(d(\overline Q)=-10\), and (3) gives \(b(Q)=4\).

It follows exactly that
\[
d(K_{n,m})=2n-10m,
\qquad s(K_{n,m})=2n-6m,
\qquad d=s-4m.
\tag{11}
\]
The trefoil has \(\overline{\mathrm{tb}}(T)=1\), again from positive-diagram sharpness. Torisu's Theorem 1.1 [A, printed p.359/PDF p.3] applies to arbitrary topological knots in standard contact three-space, without a prime, positive, or sharp-bound hypothesis, and gives
\[
\overline{\mathrm{tb}}(K\#J)=\overline{\mathrm{tb}}(K)+\overline{\mathrm{tb}}(J)+1.
\]
Using it \(n+m-1\) times proves
\[
\overline{\mathrm{tb}}(K_{n,m})
=n-12m+(n+m-1)=2n-11m-1.
\tag{12}
\]
Define the nonnegative Kauffman-bound defect by
\(\Delta(K)=d(K)-1-\overline{\mathrm{tb}}(K)\). Equations (11)–(12) establish
\[
\boxed{\Delta(K_{n,m})=m.}
\tag{13}
\]
For \(n>5m\), the degree is strictly positive while the defect is arbitrarily large. Nonetheless Theorem A proves both bounds. For example \(n=6m\) gives \(d=2m\), \(s=6m\), maximal \(\mathrm{tb}=m-1\), and defect \(m\). These knots are genuinely outside Tanaka Proposition 5.1's sharp-Kauffman hypothesis. We do **not** claim their exact unknotting numbers.

For completeness, their ordinary genera are \(g(K_{n,m})=n+3m\): the boundary connected sum of the standard genus-1 and genus-3 surfaces gives the upper bound, while the Alexander polynomials of \(T\) and \(Q\) have breadth 2 and 6 respectively. Alexander multiplicativity and the standard Seifert-matrix breadth bound give the reverse inequality. This last equality is not needed for Theorem A or the defect computation.

## 6. Failed routes and exact remaining gap

1. A theorem \(d(K)\le2g_4(K)\) for every knot would imply both knot clauses, but [O] explicitly records a 15-crossing obstruction. This attempt did not identify that knot or determine its \(g,u\). It is not a target counterexample.
2. The two upper bounds \(\overline{\mathrm{tb}}\le d-1\) and \(\overline{\mathrm{tb}}\le2g_4-1\) do not compare \(d\) and \(2g_4\). Tanaka uses equality in the first. Our exact family demonstrates why a growing sharpness defect need not violate the target either.
3. Kauffman multiplicativity plus factorwise unknotting bounds is insufficient: unknotting subadditivity points the wrong way. The 2025 Brittenham–Hermiller example has the form \(K\#\overline K\), for which (4) excludes a violation automatically. Their inspected v2 gives an upper bound 5 for the example, not an exact value 5 [B].
4. The signed-positive proof cannot be promoted to arbitrary knots: it uses \(d(P)=s(P)\) for its positive building blocks, and the historical slice-bound obstruction rules out such universal domination by \(s\).
5. Split-link normalization is fully handled here, but no reduction of arbitrary nonsplit links to these factors was proved. No band-surgery degree inequality is asserted.

Thus a complete solution still needs a proof or a correctly certified violating example for arbitrary nonsplit links in the first clause, and arbitrary knots outside the proved classes in the second. The proved classes justify only **partial, first attempt 1/5**.

## References and dependency status

- [O] T. Ohtsuki (ed.), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), Problem 1.18, pp.392–393. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- [T] T. Tanaka, *The maximal Thurston–Bennequin number of a doubled knot*, Osaka J. Math. 47 (2010), 177–187, Proposition 5.1. https://doi.org/10.18910/5513
- [K] T. Kálmán, *Maximal Thurston–Bennequin number of +adequate links*, Definition 2 and Corollary 6. Author manuscript https://arxiv.org/abs/math/0610659 . The cited positive-link result is credited there to Tanaka, *Maximal Bennequin numbers and Kauffman polynomials of positive links*, Proc. AMS 127 (1999),3427–3432, DOI https://doi.org/10.1090/S0002-9939-99-04983-7 . The latter publisher PDF returned403 and was not bypassed; this report uses the inspected distinct Kálmán source.
- [R] J. Rasmussen, *Khovanov homology and the slice genus*, Invent. Math.182 (2010),419–447, DOI https://doi.org/10.1007/s00222-010-0275-6 ; inspected author manuscript https://arxiv.org/abs/math/0402131 , Theorems1,2,4, Proposition3.9 and Section5.2. No use is made of the manuscript's subsequently disproved conjecture \(s=2\tau\) for all knots.
- [N] L. Ng, *Maximal Thurston–Bennequin number of two-bridge links*, Algebr. Geom. Topol.1 (2001),427–434, p.428. https://msp.org/agt/2001/1-1/agt-v1-n1-p21-p.pdf
- [A] I. Torisu, *On the additivity of the Thurston–Bennequin invariant of Legendrian knots*, Pacific J. Math.210 (2003),359–365, Theorem1.1. https://msp.org/pjm/2003/210-2/pjm-v210-n2-p10-p.pdf . Torisu also credits the independently obtained Etnyre–Honda connected-sum theorem.
- [D] KnotInfo, *Combinatorial definitions of polynomial invariants*. https://knotinfo.org/descriptions/jones_homfly_kauffman_description/polynomial_defn.html . This confirms the original Kauffman convention used here.
- [B] M. Brittenham and S. Hermiller, *Unknotting number is not additive under connected sum*, inspected arXiv v2 (15 September2025), especially Question4.4. https://arxiv.org/abs/2506.24088v2 . Preprint statement used only to exclude a candidate family, not as a dependency of Theorem A.

Established input theorems are cited rather than re-proved from their original foundations. The algebraic combinations, normalization calculations, and split-surface argument above are supplied in full. No independent correctness audit of every cited paper is claimed.
