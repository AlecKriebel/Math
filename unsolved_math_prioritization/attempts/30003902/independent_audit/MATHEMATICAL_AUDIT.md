# Independent audit of the surface automorphism dimension counterexample

## Verdict and scope

**ACCEPT the original mathematical conclusion, without a correction patch.** Problem 30003902, OWR-16408-015, rank 873, has a prior literature counterexample to its universal genus-one formulation. The accepted witness is a complex projective K3 surface with Néron–Severi lattice

\[
L=\langle32\rangle\oplus D_4(-1).
\]

For this witness, every associated Jacobian Mordell–Weil rank is zero, the full automorphism group is infinite, and the ordinary argument below gives

\[
0=\max_f\operatorname{rank}\operatorname{MW}(J_f)
<1\leq\operatorname{vcd}(\operatorname{Aut}S)\leq4.
\]

This is an independent adversarial review of the supplied, frozen explanation of a known example. It is not a new research approach, a new counterexample, a computation of the exact virtual dimension, or a formal proof certificate. The imported classification is accepted as a cited mathematical theorem, not re-proved by a finite calculation. Review date: 6 October 2026.

## Authenticated object and complete input review

The immutable author archive has 12,203 bytes and SHA-256 `616c01a36dc02a39e1648e293ca8682b5526910956f636194fcb14d6588392e6`. Its external manifest has 1,544 bytes and SHA-256 `e250178fe2553c8d5243cdab69f10c438fdc21668a07fbdb67ff6ab92ba731cb`. All seven regular files agree among the archive, the author directory, the internal inventory, and the externally pinned inventory. There is no executable author checker. The original archive and files are preserved unchanged in this review package.

Static authentication succeeded under isolated Python with and without optimization. The output was identical. Twenty-four positive and negative controls covered pristine copies, relocation, changed bytes, extra and missing files, an extra empty directory, links, and a Python shadow file. No author code was executed. These checks establish byte identity only.

The complete catalog, problem collection, and research-results collection were independently hashed and parsed. The entire selected problem record was read, including its background and dated literature triage. A precision point: the research-results collection has **no key** for OWR-16408-015. Under the established review convention this contributes `{}`, rather than a truncated or overlooked report. The combined serialization hash is `da199480a09842ab43e491aa518a9b896fe9f45bdf67501fdc510291acaeb492`, and the statement hash is `d054e52f07ab350007745da675f5bf354c3ec800c296d1b453fcb66470740f04`. Both match the pinned catalog. No substantive inherited proof report exists. CORPUS_VERIFICATION.json records exact corpus byte counts and hashes without including corpus contents.

## The question really includes the witness

The original OWR contribution's Conjecture 1, printed page 2024, concerns the full automorphism group and ranges over all genus-one fibrations, using the Mordell–Weil groups of their Jacobians. Its following formula with constant 8 is expressly confined to the Coble and Enriques cases. The K3 counterexample does not require that inappropriate constant. The page was read through the publisher's PDF and independently re-rendered from the authenticated local PDF for visual inspection. [O]

The distinction between a genus-one fibration and a fibration possessing a section is essential. The right-hand side may use a Jacobian belonging to a different surface. The modern source explicitly formulates Mukai's K3 conjecture for surfaces admitting a genus-one fibration. Its rank-zero witness belongs to precisely that class. This removes the otherwise possible terminological ambiguity in “elliptic K3.” [F]

The complete inherited statement has the same quantifiers. The live catalog webpage was not needed to establish this match, and no claim is made that its current displayed status was checked. One K3 surface over the complex numbers suffices to refute the stated universal claim; nothing is concluded about the separate Coble, Enriques, section-required, or positive-maximum-rank variants.

## The decisive current source and its dependencies

Fujiwara–Oguiso–Yu, arXiv:2507.13726**v3**, Remark 1.5(4), page 5, explicitly identifies the lattice \(\langle2^5\rangle\oplus D_4\), gives maximum genus-one Mordell–Weil rank zero and infinite automorphism group, and draws a positive-vcd conclusion. Their root lattices are negative definite, so the author's \(D_4(-1)\) convention matches. Their introduction distinguishes all genus-one fibrations from section-bearing fibrations. Their Proposition 2.4 and Theorem 2.5 provide the isotropic and lattice-rank bridges. [F]

The v3 identifier and 2 May 2026 date were checked both in the actual PDF and against the versioned arXiv record. The record describes it as the final version to appear in Crelle's journal. That is a manuscript-status report, not a separate verification of journal publication. [F metadata]

The classical dependency is Nikulin's classification. The introductory definitions distinguish finite reflection quotients from the condition that every isotropic orthogonal quotient is generated up to finite index by roots. Theorems 0.2.6 and 0.2.7 supply the relevant classification and finite-case distinction. The public Russian scan's extracted introduction was inspected, but its formula OCR is imperfect; it is corroboration, not a replacement for the unambiguous modern statement. Neither the complete classification proof nor every historical lattice case was re-audited. [N]

**Zero maximum Mordell–Weil rank is not zero entropy.** No zero-entropy assumption or inference is part of the accepted proof. No such conflation occurs in the original RESULT.md. Likewise, the rank-at-least-six finiteness result in the surrounding modern discussion cannot be applied at rank five. The acceptance uses the explicit rank-five remark and does not extrapolate the neighboring theorem.

## Realization and a fibration exist

Write \(D_4(-1)=\{x\in\mathbb Z^4:\sum x_i\equiv0\pmod2\}\) with negative Euclidean pairing, and let \(h\) generate the orthogonal summand of square 32. For any such \(x\), \(\sum x_i^2\equiv\sum x_i\equiv0\pmod2\); hence \(L\) is even. Its rank is five and its signature is \((1,4)\). Its determinant has absolute value \(32\cdot4=128\).

The source used by the author really does assert existence of a complex projective K3 surface with **exactly** a specified even Néron–Severi lattice of signature \((1,\rho-1)\) when \(\rho\leq10\), not merely a finite-index or primitive sublattice of its Néron–Severi lattice. It also supplies primitive embedding and explains generic period selection. Thus all hypotheses are met. [H, Corollary 14.3.1]

There is a direct embedding check as an additional elementary verification of this same witness. In one hyperbolic plane \(U=\mathbb Ze\oplus\mathbb Zf\), with \(e^2=f^2=0\) and \((e,f)=1\), send \(h\) to \(e+16f\). This vector is primitive and has square 32. In the usual coordinate model of \(E_8\), the intersection with the subspace where the last four coordinates vanish is the integral even-sum lattice on the first four coordinates, namely \(D_4\); half-integral vectors cannot have those last four coordinates zero. This intersection description proves saturation. These embeddings in separate summands give a primitive embedding of \(L\) into \(U^3\oplus E_8(-1)^2\). The complementary signature is \((2,15)\), consistent with the period argument. This is not an additional classification claim.

The displayed vector \(u=h+(4,4,0,0)\) belongs to \(L\), has square zero, and is primitive because its \(h\)-coefficient is one. The author's cited isotropic-class criterion gives a genus-one fibration over \(\mathbb P^1\). It does not require that this initially displayed vector already be nef. Passing to a nef representative, with the appropriate sign and reflections, preserves the relevant lattice properties. In characteristic zero the general fiber is smooth. The set over which the maximum is taken is therefore nonempty. [H, Definition 11.1.1 and Proposition 11.1.3]

## No fibration on this surface has a section

This part is an ordinary integral calculation, not a search over finitely many vectors. Let \(v=ah+x\in L\) be any isotropic vector. Then

\[
x_1^2+x_2^2+x_3^2+x_4^2=32a^2.
\]

Modulo 4, the number of odd coordinates is either zero or four. If all four were odd their squared sum would be 4 modulo 8, contrary to the equation. Hence every \(x_i\) is even. Set \(x_i=2y_i\). The equation becomes \(\sum y_i^2=8a^2\), and the same argument makes every \(y_i\) even. Thus all \(x_i\) are divisible by four.

For every \(w=bh+z\in L\),

\[
(v,w)=32ab-\sum x_i z_i\in4\mathbb Z.
\]

A fiber and section would have intersection one, so no isotropic fiber class can have a section. For the particular \(u\), divisibility is exactly four, since pairing with \((1,0,1,0)\in D_4(-1)\) gives \(-4\). Therefore the example would be lost if the problem were altered by adding a section-bearing-fibration hypothesis. Its use of associated Jacobians remains valid.

## The full group has positive finite virtual dimension

Let \(G=\operatorname{Aut}(S)\). The two distinct source inputs are a faithful integral action on \(H^2(S,\mathbb Z)\) and a finite kernel for the action on \(L\). Both cited statements apply to complex projective K3 surfaces. Confusing these representations would leave a gap; the original argument keeps them separate. [H, Proposition 15.2.1 and Remark 15.2.2(ii)]

Take \(\Gamma\) to be the kernel of reduction modulo three in the faithful rank-22 integral representation. It has finite index because its quotient is contained in a finite matrix group. To verify that it is torsion-free, suppose a nonidentity element has finite order, and take a suitable power \(B\) of prime order \(q\). Write \(B=I+3^sC\), with \(s\geq1\) maximal and \(C\) not zero modulo three. For \(q\neq3\), expansion of \(B^q=I\), division by \(3^s\), and reduction modulo three give \(qC=0\), impossible. For \(q=3\), division by \(3^{s+1}\) gives

\[
C+3^sC^2+3^{2s-1}C^3=0.
\]

The last two summands vanish modulo three, again impossible. The exponent \(2s-1\) is at least one, including the boundary case \(s=1\). Thus the torsion argument covers every possible prime order.

The cited infinitude of \(G\) implies infinitude of \(\Gamma\), since its index is finite. A nonidentity \(\gamma\in\Gamma\) generates an infinite cyclic subgroup. Restricting a projective \(\mathbb Z\Gamma\)-resolution to \(\mathbb Z\langle\gamma\rangle\) preserves projectivity, because the larger group ring is free over the subgroup ring. Consequently

\[
1=\operatorname{cd}_{\mathbb Z}(\mathbb Z)
\leq\operatorname{cd}_{\mathbb Z}(\Gamma).
\]

For the upper bound, the finite kernel of \(G\to O(L)\) meets torsion-free \(\Gamma\) trivially. Automorphisms preserve the positive-cone component containing ample classes, so its image is a discrete subgroup of the isometry group of \(\mathbb H^4\); the unwanted scalar \(-I\) does not preserve this sheet. A point stabilizer is a discrete subgroup of a compact orthogonal stabilizer and is finite. Torsion-freeness makes it trivial. Therefore the action is free and properly discontinuous. The quotient is a smooth aspherical four-manifold. Its four-dimensional CW structure provides a classifying space even when the quotient is noncompact, giving \(\operatorname{cd}_{\mathbb Z}(\Gamma)\leq4\).

Independence from the chosen torsion-free finite-index subgroup is the standard theorem recalled by Takatsu in Section 4.1. Applied to intersections of two such subgroups, it identifies this cohomological dimension with \(\operatorname{vcd}(G)\). No finite-kernel invariance shortcut, cocompactness assumption, or exact-dimension assertion is needed. [T, Theorem 4.4 and Definition 4.5]

## Remaining checks and exclusions

The translation/Jacobian identification is sound: a rational point of the Jacobian acts on its generic genus-one torsor, giving a birational self-map; on a smooth minimal K3 surface this extends to an automorphism. Faithfulness on the generic fiber preserves the group rank. Thus the familiar Mordell–Weil lower bound does not prove the reverse inequality. Takatsu's Lemma 2.6 also confirms that the K3 rank formula uses \(\rho(S)-2\), rather than the constant 8 printed for the other surface classes. [T]

Kikuta v1's rank-three example is excluded. Its uniform-lattice step cannot be justified solely from the absence of roots: rational isotropic classes matter. The later version no longer supplies that former counterexample. Current v3 distinguishes lattices from uniform lattices and explicitly allows genus-one surfaces with all Jacobian groups finite. Section 4.3 has a non-elementary hypothesis, which should not be silently dropped when applying its theorems. Here this discussion is supporting context, not a necessary step in the strict inequality, so no geometrical-finiteness or entropy classification is imported into the decisive proof. [K1, K2, K3]

The author correctly stops at a prior negative resolution after one substantive literature approach. Approaches two through five, new candidate-proof searches, exact-vcd investigations, and the remaining surface variants are outside this audit. The original status file's “awaiting independent review” remains preserved as historical data; the separate ACCEPTANCE files supply the reviewed disposition. No mathematical change, corrected derivative, or patch is necessary.

## References

- [O] Shigeru Mukai, Automorphism of K3 surfaces and decomposition groups of rational sextics, in Classical Algebraic Geometry, Oberwolfach Reports 33/2018, Conjecture 1, printed p. 2024. https://doi.org/10.4171/owr/2018/33 ; https://ems.press/content/serial-article-files/46758?nt=1
- [F] Koji Fujiwara, Keiji Oguiso, Xun Yu, On K3 surfaces with hyperbolic automorphism groups, arXiv:2507.13726v3. https://arxiv.org/pdf/2507.13726v3
- [F metadata] Versioned arXiv record. https://arxiv.org/abs/2507.13726v3
- [N] V. V. Nikulin, Quotient-groups of groups of automorphisms of hyperbolic forms by subgroups generated by 2-reflections. Algebro-geometric applications, 1981; English translation, Journal of Soviet Mathematics 22 (1983), 1401–1475. https://www.mathnet.ru/eng/intd51 ; https://doi.org/10.1007/BF01094757
- [H] Daniel Huybrechts, Lectures on K3 Surfaces, author-hosted draft, cited chapters and propositions. https://www.math.uni-bonn.de/people/huybrech/K3Global.pdf
- [T] Taiki Takatsu, Blown-up boundaries associated with ample cones of K3 surfaces, arXiv:2312.13831v2. https://arxiv.org/pdf/2312.13831v2
- [K1], [K2], [K3] Kohei Kikuta, Geometrical finiteness for automorphism groups via cone conjecture, respective versioned PDFs. https://arxiv.org/pdf/2406.18438v1 ; https://arxiv.org/pdf/2406.18438v2 ; https://arxiv.org/pdf/2406.18438v3
