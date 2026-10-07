# Nonseparable type-I extension: independent route and fixed-corner audit

Research timestamp: 2026-10-07 13:58 UTC. Author of this note: internal research agent, under the parent project's independent-research policy. No external individual was contacted. No manuscript, Git, release, deposit, or tracker action was taken.

Checkpoint estimate: **90%** toward a rigorous arbitrary-scope reduction conditional on the validated cohomology input; publication/priority readiness is **not assessed by this assignment**. This estimate reflects a concrete proof mechanism, not certification of the upstream cohomology theorem or novelty.

## Exact target and source status

The target is a threshold depending only on a fixed complex von Neumann algebra \(M\), valid for every von Neumann comparison algebra \(N\), without separability. Ordinary bounded, complex-linear Banach--Mazur distance is meant. The conclusion is Jordan \(*\)-isomorphism.

The full local Roydor source was read in the portions needed for the extension: Theorem 1.2, Corollary 2.4, Lemma 2.5, Proposition 2.13 and its proof, Lemma 3.1 and its proof, Theorem 3.2 and its proof, Section 4.2.2, and the Johnson statement in Theorem 4.5.

- `sources/roydor/roydor2020_user_supplied.pdf`, SHA256 `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`.
- `sources/roydor/roydor2020_reading_text.txt`, SHA256 `66cd604671be8249af91b4009fb1d8c13a4f47f9448552d239aa5a44dba5342b`.

Theorem 1.2 explicitly assumes separable predual. Its type-I classification step uses only finite degrees and one countable infinite degree. Thus citing it unchanged for arbitrary \(M\) is invalid. Theorem 3.2, in contrast, has no separability hypothesis: it assumes only that the finite type-I part has even homogeneous degrees. Its proof uses a single unital system of two-by-two matrix units and finite algebraic/norm estimates; it does not use separable direct-integral theory.

The standard structural inputs needed below are supported by Brent Nelson's [operator algebra notes](https://users.math.msu.edu/users/banelson/teaching/209/209_notes.pdf), Lemma 5.3.11 and Corollary 5.3.12 (centers of full corners), Lemma 5.3.13 (abelian projections with equal central support are equivalent), Proposition 5.3.15 (arbitrary-cardinal homogeneous type-I decomposition), and Theorem 5.3.17 (finite homogeneous matrix form). Their statements and the relevant proofs were inspected on PDF physical pp. 55--59. These statements impose no separability assumption. The finite-degree matrix form is sufficient for the preferred route below.

## Independently developed initial route

Before receiving the parent's competing proof, I developed the following route:

1. Replace Roydor's finite/countable degree index by the full set of nonzero cardinal degrees in the homogeneous type-I decomposition.
2. All infinite cardinal homogeneous algebras halve their identity, so Theorem 3.2 still handles every infinite degree, as well as finite even degrees.
3. Do not apply a separately chosen Johnson threshold to every moving central orientation corner. For a central projection \(p\in M\), extend a transported multiplication on \(pM\) by the original multiplication on \((1-p)M\). The norm defect on the fixed full algebra equals the corner defect. Johnson constants for the fixed \(M\) then work independently of \(p\), \(N\), and the orientation.
4. There is a real remaining issue in that argument: Roydor's odd/odd comparison compresses to rank \(j-1\), which is a **noncentral** corner of the fixed source. Extension by a central complement does not cover that operation.

I repaired the fourth issue by the contractive-diagonal lemma proved below. It supplies primitive bounds independent of the finite degree and of the abelian center. The original Johnson text was not obtained in this assignment, so I do **not** claim that its numerical constants \(K=L=1\), \(1/11\), and \(10\) have been independently derived here. The exact primitive-bound lemma is verified; the preferred fixed-corner argument does not require that numerical inference.

## Preferred mechanism: only two fixed Johnson algebras

After preserving the preceding independent findings, the parent supplied a different mechanism for adversarial comparison. My audit finds the following rigorous version. Assume that the two fixed algebras \(P\) and \(E\) defined here satisfy \(H^2(B,B)=0\) and closed \(B^3(B,B)\). Universal family-295 vanishing supplies those hypotheses directly. This statement does not need any uniform bound across all von Neumann algebras.

Decompose the **fixed source** once as

\[
 M=P\oplus A\oplus O,
\]

where \(A\) is the type-I degree-one summand, \(O\) is the sum of its finite odd degree \(n\ge3\) summands, and \(P\) is the complement (all type II/III, infinite type I, and finite even type I). Zero summands are omitted. The identity of \(P\) halves. In

\[
 O=\prod_{n\ge3,\ n\text{ odd}} A_n\bar\otimes M_n,
\]

choose once

\[
 e_n=1_{A_n}\otimes\operatorname{diag}(1,\ldots,1,0),
 \qquad e=(e_n)_n,\qquad E=eOe.
\]

Then \(E\) has only finite even degrees \(n-1\), and hence halves; both \(e\) and \(1_O-e\) have central carrier \(1_O\); and \((1_O-e)O(1_O-e)\) is abelian. The algebra \(E\) is fixed by \(M\) before \(N\) is chosen. Its Johnson threshold may therefore depend on \(M\) without threatening the required quantifier.

### One oriented product on a fixed halving algebra

Let \(B\) be either fixed algebra \(P\) or \(E\), and let \(S:B\to C\) be a unital self-adjoint linear isomorphism with both norms at most \(1+s\). Put

\[
 f(s)=988\sqrt{s},\qquad
 g(s)=3147585\sqrt{s},\qquad
 W(s)=(1+f(s))g(s).
\]

For \(s<5\cdot10^{-13}\), Roydor's Theorem 3.2 gives central projections \(p\in B\), \(r\in C\), an almost multiplicative \(U:pB\to rC\), and an almost anti-multiplicative \(V:(1-p)B\to(1-r)C\). By Lemma 3.1, their norms and inverse norms are at most \(1+f(s)\), and their respective bilinear defects are at most \(g(s)\).

Define on the **whole fixed** \(B\)

\[
 \mu(x,y)=U^{-1}(U(px)U(py))
 +V^{-1}(V((1-p)y)V((1-p)x)).
\]

The central direct-product structure makes \(\mu\) associative, bounded, unital, and compatible with the given involution. Furthermore

\[
 \|\mu-m_B\|\le W(s),
\]

because the norm in a two-central-summand product is the maximum of the two block norms. This is one perturbed product on \(B\), not separate applications of Johnson on the moving corners. Fix Johnson constants \(\delta_B,C_B>0\) for that fixed \(B\). If \(W(s)<\delta_B\), its self-adjoint version gives \(\Phi:B_\mu\to B\) with \(\Phi(\mu(x,y))=\Phi(x)\Phi(y)\). Then

\[
 J_B=(U\oplus V)\Phi^{-1}:B\longrightarrow C
\]

is a surjective Jordan \(*\)-isomorphism. Since \(\mu\) has the same unit as \(B\), surjectivity and multiplicativity already force \(\Phi\) to preserve the unit. This avoids an extra unitality assumption. The \(*\)-preserving Johnson conclusion is explicitly included in Roydor's Theorem 4.5; it remains a dependency to check against the original Johnson/Raeburn--Taylor source if one wants an audit independent of Roydor's reproduction.

### Full central carrier survives without a halving hypothesis

This was the central adversarial check. Let \(T:B\to C\) be unital, self-adjoint, with both norms at most \(1+t\), and sufficiently small \(t\). Proposition 2.13 gives a center isomorphism \(\varphi:Z(B)\to Z(C)\) and the associated bijection of central projections. For any projection \(h\in B\) with carrier \(c_B(h)=1\), let \(q\) be any projection with

\[
 \|T(h)-q\|\le r_t=140\sqrt t.
\]

Set \(z=c_C(q)\), \(p=\varphi^{-1}(z)\). Then \(q\le z\), and approximate positivity of \(T^{-1}\), together with the projection approximation bounds, gives

\[
 h-p\le\left((2+t)r_t+4(1+t)\sqrt{2t+t^2}\right)1.
\]

The factor \(4\) is a conservative bound; Lemma 2.5 allows a smaller one. Once the displayed scalar is below one, \(h\le p\): indeed \(p\) is central, so if \(h(1-p)\ne0\), restricting the inequality to its range gives \(1\le\text{scalar}<1\). Thus \(c_B(h)=1\) forces \(p=1\), and hence \(z=1\). This argument applies to both \(e\) and \(1-e\), even though they are not central.

### Recovering the finite odd summand, including arbitrary centers

Normalize an initial nearly isometric map using Corollary 2.4, and use Proposition 2.13 and Lemma 3.1 to restrict it to the three central source pieces. Let \(T_O:O\to C_O\) be the resulting map. Choose \(q\) close to \(T_O(e)\); then \(1-q\) is equally close to \(T_O(1-e)\). The full-carrier lemma gives

\[
 c_{C_O}(q)=c_{C_O}(1-q)=1.
\]

Lemma 3.1 gives nearly isometric maps from \(E=eOe\) to \(qC_Oq\), and from the abelian complement corner to \((1-q)C_O(1-q)\). Proposition 2.13 applied to the latter map makes that target corner abelian and identifies its center. Its full carrier implies that \(C_O\) is type I. The fixed-halving correction above gives an exact Jordan \(*\)-isomorphism

\[
 J_E:E\longrightarrow qC_Oq.
\]

Full-corner center identification \(Z(qC_Oq)=Z(C_O)q\), together with \(Z(E)=Z(O)e\), produces an exact center isomorphism \(\beta:Z(O)\to Z(C_O)\). For a source degree-\(n\) central component \(z_n\), the corner \(\beta(z_n)qC_Oq\) is homogeneous of degree \(n-1\). Jordan \(*\)-isomorphisms preserve this property: their usual central homomorphism/anti-homomorphism decomposition preserves abelian projections and their Murray--von Neumann equivalence, with initial/final projections interchanged on an anti-homomorphic block.

Here is an elementary rank-addition argument which avoids measurable fields, pointwise fibers, and any unstated infinite-cardinal cancellation. Write \(w=\beta(z_n)\). The projection \(wq\) is a sum of \(n-1\) orthogonal equivalent abelian projections, each with carrier \(w\). Their carrier is the same in the full algebra because \(q\) has full carrier and centers of its corner are identified by compression. The complementary projection \(w(1-q)\) is abelian and also has carrier \(w\). Abelian projections with the same carrier are equivalent. Therefore

\[
 w=wq+w(1-q)
\]

is a sum of exactly \(n\) orthogonal equivalent abelian projections. Thus \(wC_O\) is homogeneous of degree \(n\). Its center is \(wZ(C_O)\), isomorphic through \(\beta\) to \(z_nZ(O)\). Finite matrix classification consequently gives a \(*\)-isomorphism of the corresponding degree-\(n\) summands. Their bounded direct product gives \(O\cong C_O\). Only the countable family of finite odd integers is used; the abelian centers themselves can have any density/cardinality.

The source pieces \(P\) and \(A\) are handled respectively by the fixed-halving correction and Proposition 2.13. Their direct sum with the odd-piece reconstruction yields the desired exact Jordan \(*\)-isomorphism \(M\to N\).

### One threshold, chosen before comparison with N

No moving algebra enters the choice of Johnson constants. Choose \(\delta_P,C_P\) and \(\delta_E,C_E\) once; omit a pair if its algebra is zero. If the initial normalized map has distortion parameter \(t\), its central restrictions have parameters at most \(f(t)\), and its further \(e\)-corner map has parameter at most \(f(f(t))\). It is enough to choose a fixed small \(t_M>0\) so that all Roydor compression/center/halving hypotheses hold, the full-carrier scalar at \(f(t_M)\) is below one, and

\[
 W(f(t_M))<\delta_P,
 \qquad W(f(f(t_M)))<\delta_E.
\]

If a near-identity bound is wanted as well, impose \(C_PW(f(t_M))<1/2\) and \(C_EW(f(f(t_M)))<1/2\). Every left-hand side tends to zero as \(t_M\downarrow0\), so a positive choice exists. Corollary 2.4 has normalized parameter bounded by \(10\sqrt{\eta}\) for a sufficiently small original Banach--Mazur excess \(\eta\). Choose \(\varepsilon_M>0\) with \(10\sqrt{\varepsilon_M}<t_M\) and the initial normalization hypotheses. This threshold depends only on \(M\), through its two fixed Johnson algebras. It is independent of \(N\), all orientation projections, all nonseparable centers, and all infinite cardinal homogeneous degrees.

For the canonical-predual version, a bounded complex-linear predual isomorphism adjoints to an algebra-space isomorphism with the same norm product. Exact Jordan \(*\)-isomorphisms of von Neumann algebras are normal order isomorphisms, and induce isometric canonical-predual maps. This part does not require separability. The zero algebra is harmless: it is Banach-space isomorphic only to itself.

## Verified independent lemma: finite homogeneous contractive primitives

For any abelian von Neumann algebra \(A\), any finite \(n\), any \(k\ge1\), and any bounded Hochschild cocycle \(\phi:(A\bar\otimes M_n)^k\to A\bar\otimes M_n\), there is a bounded primitive \(\psi\) with

\[
 \delta\psi=\phi,\qquad \|\psi\|\le\|\phi\|.
\]

Put \(B=A\bar\otimes M_n\). Finite partitions \(\mathcal P\) of \(1_A\) by central projections give finite-dimensional unital algebras \(F_\mathcal P=\operatorname{span}(\mathcal P)\otimes M_n\). Their union is norm dense: approximate the finitely many matrix entries by finite spectral step functions and take a common refinement. This directed family is available for arbitrary \(A\).

Normalized Haar measure on the compact finite-dimensional unitary group gives

\[
 d_F=\int_{U(F)}u\otimes u^*\,du\in B\widehat\otimes_\pi B,
 \qquad \|d_F\|_\pi\le1,\quad m(d_F)=1.
\]

For \(v\in U(F)\), substitution \(w=vu\) shows \(vd_F=d_Fv\); unitaries linearly span \(F\). Consequently \(\|ad_F-d_Fa\|_\pi\to0\) for each fixed \(a\in B\): after approximating \(a\) by \(b\in F_0\), every \(F\supset F_0\) has defect at most \(2\|a-b\|\).

Write \(d_F=\sum_i x_i\otimes y_i\), and define

\[
 \psi_F(a_1,\ldots,a_{k-1})
 =\sum_i x_i\phi(y_i,a_1,\ldots,a_{k-1}).
\]

This tensor contraction is well defined and has norm at most \(\|\phi\|\). The cocycle identity gives the exact defect formula

\[
 (\delta\psi_F-\phi)(a_1,\ldots,a_k)
 =\sum_i a_1x_i\phi(y_i,a_2,\ldots,a_k)
 -\sum_i x_i\phi(y_i a_1,a_2,\ldots,a_k),
\]

whose norm is at most

\[
 \|\phi\|\,\|a_1d_F-d_Fa_1\|_\pi
 \prod_{j=2}^k\|a_j\|.
\]

It tends to zero pointwise in norm. **It need not tend to zero in full cochain norm.** Product weak* compactness gives a pointwise weak* convergent subnet of the \(\psi_F\). Multilinearity passes to the limit, weak* closed norm balls preserve the bound, and separate weak* continuity of multiplication makes the differential commute with these limits. Thus the limit is the asserted primitive. Degree one has the same sign convention: \(\delta\psi(a)=a\psi-\psi a\). No normality of the original cocycle is assumed.

A common ultrafilter containing the partition tails makes these contractions linear in \(\phi\) and gives norm-at-most-one Hochschild homotopies. The internal adversarial child `contractive_diagonal_audit` independently checked this entire proof and reported no defect. It explicitly cautioned that identifying the resulting primitive constants with the particular named constants in Johnson's original paper requires checking those definitions. This numerical claim is not used in the preferred route.

## Status, falsification checks, and exact remaining validation

The fixed-corner route survives the following attacks: arbitrary center density, uncountable type-I infinite degrees, all finite odd degrees at once, noncentral full carriers, orientation dependence, comparison-dependent thresholds, the zero summand, and preserving the complex involution. Rank addition has a checkable projection proof rather than an informal fiberwise assertion. The threshold uses a finite minimum of constants attached to two fixed algebras, with no transfinite multiplication correction.

The initial cardinal route remains a secondary mechanism, and its noncentral uniformity gap is recorded rather than hidden. The preferred route is simpler and avoids its unverified numerical Johnson inference.

What this note does **not** certify: family-295's universal vanishing proof, the original Johnson/Raeburn--Taylor \(*\)-stable perturbation theorem independent of Roydor's statement, full-package review, or novelty/priority. The parent's separate source/cohomology/priority audits must discharge those dependencies. In particular, a more general statement in Roydor's older slides may already announce this conditional arbitrary-scope result; this construction is not evidence of a new theorem's priority.
