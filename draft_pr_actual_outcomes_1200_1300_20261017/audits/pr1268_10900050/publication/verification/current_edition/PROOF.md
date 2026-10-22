# A counterexample to Long's clique number equality

## Conclusion and scope

Long's Question 7.2 in *Problems In Groups, Geometry, and Three-Manifolds* asks whether the displayed upper bound for the prime-difference graph is always an equality. Under the prime-element convention specified by the cited Long–Thistlethwaite manuscript, the answer is **no**. The totally real field

\[
k=\mathbb Q(\sqrt {10})
\]

has

\[
\omega(\Gamma_{\rm unit})=\omega(\Gamma_{\rm prime})=2,
\qquad
\min_{\mathfrak q\text{ nonzero prime}}|\mathcal O_k/\mathfrak q|=2.
\]

Consequently the two sides of the proposed equality are 2 and 4.

Here a prime element means a nonzero nonunit \(p\) whose principal ideal \((p)\) is prime. The graph \(\Gamma_{\rm unit}\) has vertex set \(\mathcal O_k\), with distinct vertices adjacent exactly when their difference is a unit. The graph \(\Gamma_{\rm prime}\) adds the edges whose differences are prime elements. This is precisely condition (i) of the cited manuscript's first definition; Section 3 specifies that prime cliques require condition (i) alone. Its additional condition concerning the image of the unit group applies to Lenstra–Hurwitz cliques and is not part of the prime graph. See [1, Questions 7.1–7.2] and [2, p. 1 and beginning of Section 3 on p. 9].

The proof below uses no class-number computation, prime search, unproved conjecture, or numerical approximation.

## The field and its full ring of integers

The polynomial \(f(X)=X^2-10\) lies in \(\mathbb Z[X]\), is irreducible over \(\mathbb Q\), and has two real roots. For irreducibility, a rational root of this monic polynomial would be an integer whose square is 10, which is impossible. Thus \(k\) satisfies the polynomial and total-reality hypotheses of [1, Question 7.1].

We prove directly that

\[
\mathcal O_k=\mathbb Z[\sqrt {10}].
\]

Every \(a+b\sqrt {10}\), with \(a,b\in\mathbb Z\), is an algebraic integer: it is a root of the monic integer polynomial

\[
X^2-2aX+(a^2-10b^2).
\]

Conversely, let \(\alpha=r+s\sqrt {10}\) be an algebraic integer, where \(r,s\in\mathbb Q\). Its trace \(2r\) and norm \(r^2-10s^2\) are integers. One elementary justification is that for \(s\ne0\) these are the coefficients of its monic minimal polynomial, which has integer coefficients by Gauss's lemma; for \(s=0\), the rational-root argument shows \(\alpha\in\mathbb Z\).

Put \(m=2r\in\mathbb Z\). Then

\[
40s^2=m^2-4(r^2-10s^2)\in\mathbb Z.
\]

If \(s=u/v\) in lowest terms with \(v>0\), then \(v^2\mid40\), so \(v\) is 1 or 2. Thus \(n=2s\in\mathbb Z\), and integrality of the norm gives

\[
m^2-10n^2\equiv0\pmod4.
\]

If \(n\) were odd, this would require \(m^2\equiv2\pmod4\), which is impossible. Therefore \(n\) is even, and the same congruence then makes \(m\) even. Hence \(r,s\in\mathbb Z\), proving the claim. Write \(O=\mathcal O_k\) from now on.

## A prime ideal of norm two

Define

\[
\varphi:O\longrightarrow\mathbb F_2,
\qquad
\varphi(a+b\sqrt {10})=a\bmod2.
\]

This is a ring homomorphism: the constant coefficient of a product is \(ac+10bd\), which reduces to \(ac\) modulo 2. It is surjective because 1 maps to 1. Its kernel is

\[
P=(2,\sqrt {10}).
\]

Indeed, both generators have image zero, and an element of the kernel has even constant coefficient and is therefore of the form \(2c+b\sqrt {10}\). It follows that \(O/P\cong\mathbb F_2\). In particular, \(P\) is nonzero, proper, prime and maximal, and its ideal norm is

\[
N(P)=[O:P]=2.
\]

## The norm and nonprincipality of the ideal

For \(\delta=a+b\sqrt {10}\in O\), multiplication by \(\delta\), in the integral basis \((1,\sqrt {10})\), has integer matrix

\[
M_\delta=\begin{pmatrix}a&10b\\b&a\end{pmatrix}.
\]

For \(\delta\ne0\), its determinant \(a^2-10b^2\) is nonzero: otherwise \(b\ne0\) would express \(\sqrt {10}\) as a rational number, or \(a=b=0\). The image of this multiplication map is the additive subgroup \(\delta O\). Therefore

\[
[O:\delta O]=|\det M_\delta|=|a^2-10b^2|. \tag{1}
\]

The integer-lattice fact used here is that a nonsingular square integer matrix has image of index the absolute value of its determinant. It follows, for example, by reducing the matrix to Smith normal form with unimodular integer row and column operations; those operations preserve index and absolute determinant, while the assertion for a diagonal matrix is immediate.

Suppose \(P=(\delta)\). Since \(P\ne0\), the generator \(\delta\) is nonzero. Equating (1) with \([O:P]=2\) yields

\[
a^2-10b^2=2\quad\hbox{or}\quad a^2-10b^2=-2.
\]

Reduction modulo 5 would make \(a^2\) congruent to 2 or 3. But the quadratic residues modulo 5 are exactly 0, 1 and 4. Thus neither equation has an integer solution, and \(P\) is nonprincipal.

## No permitted edge difference lies in the ideal

First, no unit lies in the proper ideal \(P\). If \(u\in P\) and \(uv=1\) for some \(v\in O\), the ideal property would give \(1\in P\), a contradiction.

We also verify the maximality fact required for prime elements, without appealing to the general theory of Dedekind domains. Let \(Q\) be a nonzero prime ideal of \(O\). Choose \(0\ne\delta\in Q\). By (1), \(O/(\delta)\) is finite; the quotient \(O/Q\), being an image of it, is finite as well. Since \(Q\) is prime and proper, \(O/Q\) is a finite integral domain with at least two elements. Every finite integral domain is a field: multiplication by a nonzero element is injective, hence surjective, and in particular takes some element to 1. Thus every nonzero prime ideal of \(O\) is maximal.

Now suppose a prime element \(p\) belonged to \(P\). The nonzero prime ideal \((p)\) would satisfy \((p)\subseteq P\subsetneq O\). Its maximality would force \((p)=P\), contrary to the nonprincipality just proved. Hence no prime element lies in \(P\).

## Exact clique numbers and the strict inequality

If \(x,y\in O\) have the same image under \(\varphi\), then \(x-y\in P\). For \(x\ne y\), the preceding section shows that this difference is neither a unit nor a prime element. Thus neither graph has an edge within a residue class modulo \(P\).

The two residue classes give a proper coloring of each graph with two colors. Any clique must have distinct colors at all its vertices, so

\[
\omega(\Gamma_{\rm unit})\le2,
\qquad
\omega(\Gamma_{\rm prime})\le2.
\]

The vertices 0 and 1 are adjacent in the unit graph because their difference is a unit. They are also adjacent in the larger prime graph. Therefore both displayed upper bounds are attained, and both clique numbers equal 2.

Every quotient by a proper ideal has distinct zero and one, so its cardinality is at least two. Since \(P\) is a nonzero prime ideal with a two-element quotient, the minimum prime-ideal norm is exactly two. If the question's unqualified word “prime” were taken to include the zero ideal, its quotient is the infinite ring \(O\) and cannot lower this minimum.

We have consequently proved

\[
\boxed{\omega(\Gamma_{\rm prime})=2
<4=\omega(\Gamma_{\rm unit})
\min_{\mathfrak q\text{ nonzero prime}}|O/\mathfrak q|.}
\]

This is a counterexample to the universal equality in [1, Question 7.2].

## Boundaries of the conclusion

Question 7.1 asks how often the ring of integers is a PID; it does not assume that it is one. Question 7.2 inherits the preceding field setup, so the nonprincipal ideal in this example does not violate a hypothesis. This proof makes no assertion about a separately imposed PID-only version of the question.

The difference between prime and irreducible is essential. Indeed, 2 is an irreducible element of this ring: its absolute norm is 4, and a factorization into two nonunits would require two factors of absolute norm 2, which the congruence above rules out. Here an element of absolute norm 1 is a unit because its inverse is its conjugate divided by its norm. But 2 is not prime, since \(\sqrt {10}\notin(2)\) and \((\sqrt {10})^2=10\in(2)\). In a graph using irreducible differences, the vertices \(0,1,2\) would already be a triangle. That different graph is excluded by the cited source's explicit definition.

Theorem 3.1 of [2, p. 10] is printed in terms of a minimum principal-ideal norm, whereas [1] displays a minimum prime-ideal norm. No identification of those minima, and no repair of the manuscript's proof wording, is needed here: every quantity in the actual displayed question has been evaluated directly.

## References and source pins

1. Kelly Delp, Diane Hoffoss and Jason Fox Manning, editors, *Problems In Groups, Geometry, and Three-Manifolds*, arXiv:1512.04620v1, 15 December 2015. Question 7.1: PDF p. 5; Question 7.2: PDF p. 6; reference [19]: PDF p. 7. [Versioned primary PDF](https://arxiv.org/pdf/1512.04620v1). Inspected copy: 280293 bytes; SHA-256 `7c0dbfb0f5f5f5e39d876dbe0734c4c9df927ed23a29917008ccec77073f00e4`.
2. D. D. Long and Morwen B. Thistlethwaite, *Lenstra-Hurwitz cliques and the class number one problem*, author-hosted 16-page manuscript, cited as a 2015 preprint in [1]. First definition: PDF p. 1; prime-clique convention: Section 3, PDF p. 9; Theorem 3.1 and its proof: PDF p. 10. [Primary manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf). Inspected copy: 250475 bytes; SHA-256 `166238dd17c2a2ffe1408c5f5c3d2f1ce9ae914c48f657ac309b7a83ee07594c`.

The argument and the separate mathematical review are AI-assisted. The review was completed on 11 October 2026; it is not external human peer review, journal acceptance, or formal proof-assistant certification. This document makes no claim of novelty or priority. [ACCEPTANCE.json](ACCEPTANCE.json) binds the review verdict to this exact public proof and its [audit report](ACCEPTANCE_REPORT.md).
