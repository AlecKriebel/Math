# Higher-genus surfaces and skein torsion: a credited affirmative answer

**10400080 / AMR-103-0080 / Przytycki's Problem 4.2. Known result; separate source/proof review pending.** The existential question has an affirmative answer in Belletti–Detcherry's 2024 preprint, subsequently published in 2025. Recommended status: **already_solved, 0/5 new-discovery attempts**. The argument below validates the exact coefficient and source scope; it is not a campaign discovery.

## 1. Exact problem and known resolution

[Ohtsuki's problem list, printed p.446, Problem4.2](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf) asks, on behalf of J. Przytycki, whether surfaces other than incompressible tori and essential spheres can yield torsion in the Kauffman bracket skein module. The immediately preceding definition fixes
$$R=\mathbb Z[A,A^{-1}],\qquad S(M)=S_{2,\infty}(M),$$
with unoriented framed links, including the empty link, and the ordinary Kauffman crossing and trivial-circle relations. Here torsion means a nonzero skein element annihilated by a nonzero Laurent polynomial. This is a question about existence, not a request to characterize every manifold or every surface.

Belletti and Detcherry's [*On torsion in the Kauffman bracket skein module of 3-manifolds*, arXiv:2406.17454v1](https://arxiv.org/abs/2406.17454), Corollary3.1, gives:

- Every closed hyperbolic 3-manifold with positive first Betti number has $(A+1)$-torsion in $S(M)$
- For every integer $k\ge0$, there exists a closed oriented 3-manifold whose skein module has $(A+1)$-torsion but which has no closed essential orientable surface of genus at most $k$

Their Proposition3.2 supplies the latter manifolds with arbitrarily large first Betti number. Taking $k\ge1$ excludes essential spheres and tori, while positive first Betti number ensures the presence of higher-genus essential surfaces. This answers the original question affirmatively without using a low-genus surface as an alternative source of torsion.

The paper is published as [*International Mathematics Research Notices* 2025, issue21, rnaf333](https://academic.oup.com/imrn/article/2025/21/rnaf333/8315094), published 5November2025. Publication metadata and the journal abstract were verified, as were both authors' publication listings. The full 2024 preprint, including Sections2–3, was retrieved and read. The final journal full text was not retrieved or compared line by line.

The neighboring universal Conjecture4.3 in Ohtsuki's list is a different target. Neither this note nor the cited existential resolution establishes that all essential surfaces produce torsion, or classifies all torsion-free skein modules. The phrase “incompressible sphere” is used in its essential-sphere sense; spheres bounding balls are not being excluded from an arbitrary manifold.

## 2. Integral coefficient check: the dimension-jump argument

The central algebraic mechanism is Belletti–Detcherry's Theorem2.1. The following reconstruction records the localization step explicitly.

**Lemma.** Let $R=\mathbb Z[A,A^{-1}]$, $K=\mathbb Q(A)$ and $h=A+1$. Let $V$ be any $R$-module with $\dim_K(V\otimes_R K)=d<\infty$. If $d+1$ elements $v_0,\ldots,v_d$ have linearly independent images in
$$ (V/hV)\otimes_{\mathbb Z}\mathbb Q,$$
then $V$ has a nonzero element killed by $h$.

**Proof.** The images of the $v_i$ are dependent over $K$. Clearing coefficient denominators gives Laurent polynomials $p_i\in R$, not all zero, such that $\sum p_i v_i$ maps to zero in $V\otimes_R K$. The definition of localization then supplies a further nonzero $s\in R$ with
$$\sum_i s p_i v_i=0\quad\text{in }V.$$
This additional multiplier is important: $V\to V\otimes_R K$ need not be injective.

Let $h^e$ be the largest common power of $h$ dividing the nonzero coefficients $sp_i$. Write $sp_i=h^e q_i$, where at least one integer $q_i(-1)$ is nonzero. Set $v=\sum q_i v_i$. Its image in the displayed rational specialization is nonzero, by independence. Thus $v\ne0$ in $V$, and $h^e v=0$. The case $e=0$ would contradict that nonzero specialized image. Therefore $e\ge1$. If $m\ge1$ is the least exponent with $h^m v=0$, then $h^{m-1}v$ is nonzero and is killed by $h$. This proves the lemma. No finite-generation or torsion-freeness assumption on $V$ was used. $\square$

For example, in $V=R\oplus R/(h)$, the difference of $(1,1)$ and $(1,0)$ vanishes after localization but is nonzero in $V$. Multiplying by $h$ makes it an actual relation. The lemma explicitly allows this situation.

## 3. Why positive first Betti number forces an infinite specialization

For a closed connected oriented manifold $M$ with $b_1(M)>0$, choose an epimorphism $\phi:\pi_1(M)\to\mathbb Z$. The diagonal representations
$$\rho_z(g)=\begin{pmatrix}z^{\phi(g)}&0\\0&z^{-\phi(g)}\end{pmatrix},\qquad z\in\mathbb C^*,$$
have a nonconstant character. The classical trace evaluation at $A=-1$ sends an unoriented framed link $L=L_1\sqcup\cdots\sqcup L_r$ to
$$\prod_{j=1}^r\bigl(-\operatorname{tr}\rho_z(L_j)\bigr).\tag{1}$$
It is well defined on the specialized skein module: reversal does not change the trace, a trivial circle evaluates to $-2$, and the crossing relation is the $\mathrm{SL}_2$ trace identity
$$\operatorname{tr}(X)\operatorname{tr}(Y)
 =\operatorname{tr}(XY)+\operatorname{tr}(XY^{-1}).$$
Framing twists act by $-A^3$, which equals one at $A=-1$. This is the familiar classical skein/character evaluation credited to Bullock and Przytycki–Sikora; its full scheme-theoretic isomorphism is not needed for this dimension argument.

Choose a framed knot $\gamma$ representing a loop with $\phi(\gamma)=1$. Its $j$ parallel copies, with the empty link for $j=0$, evaluate to
$$(-z-z^{-1})^j.$$
These Laurent polynomials are linearly independent over $\mathbb Q$: their highest positive powers of $z$ have distinct degrees and nonzero coefficients $(-1)^j$. Therefore
$$\dim_{\mathbb Q}\bigl((S(M)/(A+1)S(M))\otimes\mathbb Q\bigr)=\infty.\tag{2}$$

The [Gunningham–Jordan–Safronov finiteness theorem](https://doi.org/10.1007/s00222-022-01167-0), published in *Inventiones mathematicae*232(2023),301–363, states that $S(M)\otimes_R\mathbb Q(A)$ is finite dimensional for every closed oriented 3-manifold. The full published paper was retrieved; the exact statement is Theorem1, with the general result in Theorem5.8. This is a substantial imported theorem, not re-proved here.

Apply the lemma to enough parallel-copy skeins. Equations (1)–(2) supply the independent specialization classes, and generic finiteness supplies finite rank. Thus every closed oriented $M$ with $b_1(M)>0$ has a nonzero integral skein element annihilated by $A+1$. This is the known mechanism behind the cited examples. It is not merely torsion after extension to complex coefficients, and it does not assume the integral skein module is finitely generated.

## 4. The geometric existence input and source coverage

Belletti–Detcherry's Proposition3.2 is used as the credited geometric existence theorem: for any prescribed genus bound and Betti-number bound there is a closed oriented manifold with larger first Betti number and no essential closed orientable surface below the genus bound. Its full proof in Section3.2 was read. It combines high-distance Heegaard splittings with Torelli gluing so that the first homology remains a free abelian group of the chosen Heegaard genus. The genus can be chosen strictly larger than the required Betti bound.

The cited distance constraints were checked in primary sources: [Hempel, Theorem2.7 and its proof](https://arxiv.org/abs/math/9712220), and [Hartshorn, Theorem1.2](https://msp.org/pjm/2002/204-1/pjm-v204-n1-p05-p.pdf). Hartshorn assumes the irreducible Haken setting and bounds Heegaard distance by twice the genus of an orientable incompressible surface; the standard sphere obstruction gives distance zero in the reducible case. The construction uses sufficiently large distance. The full geometric machinery concerning measured laminations and pseudo-Anosov elements is an imported dependency; this note does not present a new stand-alone proof of it or an explicit triangulated example.

Positive first Betti number in a closed oriented manifold gives a nonzero integral second-homology class. Represent it by an embedded oriented surface and compress until incompressible, discarding null-homologous sphere components. In the examples with no essential spheres or tori, some component of the surviving representative is an essential orientable surface of genus at least two. It is not boundary parallel, since the manifold is closed. Combined with Section3, these are exactly the witnesses requested by Problem4.2.

The stronger existence statements in [Kalfagianni's August2026 preprint](https://arxiv.org/abs/2608.12668) are not dependencies of this answer. Its introduction explicitly credits the earlier Belletti–Detcherry examples. In particular this package does not claim to certify that later paper's uniqueness-of-incompressible-surface statement or any new explicit torsion representative.

## 5. Result and verification limits

The literal existential problem is already answered affirmatively. The package validates the credited result and makes its integral localization step, generic-field convention and geometric scope explicit. It does not claim an explicit nonzero torsion link combination, a universal surface-to-torsion classification, or a new theorem.

The accompanying exact checker tests the trace identities, independence of specialized parallel-copy polynomials, localization-kernel controls and extraction of an actual $(A+1)$-torsion element in finite algebraic models. These controls do not independently certify the imported finiteness and high-distance existence theorems.

Recommended status: **already_solved, 0/5 new-discovery attempts**, credited to Belletti–Detcherry's 2024 preprint/2025 publication and its stated dependencies. Separate source/proof review is required before publication of this campaign package.
