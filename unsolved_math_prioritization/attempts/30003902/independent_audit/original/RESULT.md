# Problem 30003902: a prior counterexample to the universal equality

## Disposition

**PRIOR RESOLUTION: the stated universal equality is false.** This is a literature-based negative answer, not a new counterexample or a claim that every subcase has been classified. Checked 6 October 2026. The decisive current reference is Fujiwara–Oguiso–Yu [F], Remark 1.5(4), version 3, PDF page 5.

For a complex projective K3 surface with Néron–Severi lattice

\[
L=\langle32\rangle\oplus D_4(-1),
\]

that reference gives the two essential facts

\[
\max_f\operatorname{rank}\operatorname{MW}(J_f)=0,
\qquad |\operatorname{Aut}(S)|=\infty.
\]

Here our notation makes the negative sign explicit: the same lattice is written \(\langle2^5\rangle\oplus D_4\) in [F]. The maximum includes every genus-one fibration, with the group of its Jacobian. These are imported classification facts, not conclusions of a finite search in this report. They are attributed in [F] to Nikulin [N], Theorem 0.2.6; the adjacent Theorem 0.2.7 distinguishes the finite-automorphism cases. We do not re-prove Nikulin's classification.

Below we check existence, the surface/fibration scope, and the group-theoretic implication, including a direct proof that

\[
1\leq\operatorname{vcd}(\operatorname{Aut}(S))\leq4.
\]

Consequently the two sides of the proposed equality differ on an actual surface in the stated class.

## 1. Match the question and its quantifiers

Mukai's Conjecture 1 in the original Oberwolfach report [O], printed page 2024, compares virtual cohomological dimension of the full automorphism group with the maximum Jacobian Mordell–Weil rank over all genus-one fibrations. It includes Coble, Enriques, and elliptic K3 surfaces.

We work over \(\mathbb C\). One counterexample in this subclass suffices to disprove the universal statement. “Elliptic K3” is used here in the genus-one sense, without requiring a section. This is the convention in [H], Chapter 11, Definition 1.1, and is consistent with [O]'s use of the Jacobian of each genus-one fibration. A strengthened hypothesis requiring a Jacobian fibration on the surface itself would define a different question; this report does not settle it. Section 2 verifies that the particular counterexample has no such section-bearing fibration.

## 2. A genuine K3 surface and a nonempty fibration family

Use the concrete realization

\[
D_4(-1)=\{x\in\mathbb Z^4:\sum_i x_i\text{ is even}\},
\qquad (x,y)=-\sum_i x_iy_i.
\]

Let \(h^2=32\) and \(h\perp D_4(-1)\). The lattice is even and has signature \((1,4)\). By [H], Corollary 14.3.1, every even lattice of signature \((1,\rho-1)\) with \(\rho\leq10\) occurs as the Néron–Severi lattice of a complex projective K3 surface. Thus there is a surface \(S\) with precisely this \(L\), and \(\rho(S)=5\).

The vector

\[
u=h+(4,4,0,0)
\]

belongs to \(L\), is primitive, and has square \(32-16-16=0\). By the isotropic-class criterion [H], Proposition 11.1.3, the surface admits a genus-one fibration. The maximum in the conjecture is therefore not over an empty set. The criterion allows passing to a nef representative; no assertion that the displayed vector is already nef is needed.

For completeness, this lattice cannot contain the fiber and section of a Jacobian fibration. If \(v=ah+x\) is any isotropic integral vector, then

\[
\sum_i x_i^2=32a^2.
\]

Modulo 4 the number of odd \(x_i\) is either zero or four. Four odd coordinates would give a sum congruent to 4 modulo 8, which is impossible. Therefore all \(x_i\) are even. Write \(x_i=2y_i\) and repeat the same argument in \(\sum_i y_i^2=8a^2\). This proves that every \(x_i\) is divisible by 4. Hence every pairing \((v,w)\), \(w\in L\), is divisible by 4. In particular no integral class pairs to 1 with an isotropic fiber class. A section would pair to 1, so none exists. This computation also explains why restricting the problem to Jacobian K3 surfaces would lose the example.

## 3. Full automorphism group and virtual cohomological dimension

Let \(G=\operatorname{Aut}(S)\), the full group, not merely its image on the Néron–Severi lattice. Two standard surface facts are used: its action on \(H^2(S,\mathbb Z)\) is faithful, and its action on \(L\) has finite kernel [H], Proposition 15.2.1 and Remark 15.2.2(ii).

### 3.1 A specific torsion-free finite-index subgroup

Embed \(G\) in \(\mathrm{GL}_{22}(\mathbb Z)\) through its faithful cohomology action, and let \(\Gamma\) be the kernel of reduction modulo 3. Its index is finite.

Here is a proof of its torsion-freeness. If a nonidentity matrix in this congruence subgroup has finite order, an appropriate power \(B\) has prime order \(q\). Write \(B=I+3^s C\), with \(s\geq1\) maximal and some entry of \(C\) nonzero modulo 3. For \(q\neq3\), the binomial expansion of \(B^q=I\), divided by \(3^s\) and reduced modulo 3, gives \(qC=0\), a contradiction. For \(q=3\), divide

\[
3^{s+1}C+3^{2s+1}C^2+3^{3s}C^3=0
\]

by \(3^{s+1}\). The last two terms are divisible by 3 because \(s\geq1\), so again \(C=0\) modulo 3, a contradiction.

Thus \(\operatorname{vcd}(G)=\operatorname{cd}_{\mathbb Z}(\Gamma)\). Independence of the chosen torsion-free finite-index subgroup is the standard virtual-dimension theorem; see [T], Section 4.1, Theorem 4.4 and Definition 4.5.

### 3.2 Positive dimension follows from infinitude

By the imported counterexample fact, \(G\) is infinite, and so is \(\Gamma\). Choose a nonidentity \(\gamma\in\Gamma\). It has infinite order. Therefore \(\mathbb Z\cong\langle\gamma\rangle\leq\Gamma\).

Cohomological dimension does not increase on passing to a subgroup: restricting a projective group-ring resolution preserves projectivity because \(\mathbb Z\Gamma\) is a free module over the subgroup ring. Since \(\operatorname{cd}_{\mathbb Z}(\mathbb Z)=1\), we obtain \(\operatorname{cd}_{\mathbb Z}(\Gamma)\geq1\).

There is also a finite upper bound in this example. The finite kernel of \(G\to O(L)\) meets torsion-free \(\Gamma\) trivially. Its image is a discrete group of isometries of the hyperbolic space \(\mathbb H^4\) determined by the positive cone of \(L\). A point stabilizer in this discrete group is finite, hence trivial. The quotient \(\mathbb H^4/\Gamma\) is consequently an aspherical smooth 4-manifold and supplies a 4-dimensional classifying space. Thus \(\operatorname{cd}_{\mathbb Z}(\Gamma)\leq4\).

This reasoning avoids an unjustified transfer from a cohomological image to the full group. No exact value of its virtual cohomological dimension is asserted.

## 4. Why the familiar lower bound is insufficient

For a genus-one fibration on a complex projective K3 surface, sections of its Jacobian act by translations on its generic genus-one fiber. These give faithful birational self-maps, which extend to automorphisms of the minimal K3 surface. A free abelian subgroup of rank \(r=\operatorname{rank}\operatorname{MW}(J_f)\) therefore lies in \(G\). Its intersection with a torsion-free finite-index subgroup has the same rank. Subgroup monotonicity and the torus classifying space yield \(r\leq\operatorname{vcd}(G)\). This also explains the lower-bound observation in [T], Remark 1.1.

That inequality does not force equality. Here all the translation ranks vanish while the full group is infinite. In the hyperbolic-cone description, a positive-rank fibration stabilizer contributes a cusp, but ideal rational fiber classes with finite stabilizer need not be cusps of the group. It is invalid to estimate the entire group's dimension merely by the largest translation rank. The current geometrical-finiteness description in [K], Theorem 4.11, explicitly allows genus-one K3 surfaces for which every Jacobian Mordell–Weil group is finite.

For K3 fibrations the Shioda–Tate rank formula is \(\rho(S)-2-\sum_v(m_v-1)\), using the associated Jacobian; [T], Lemma 2.6. The expression \(8-\sum_v(m_v-1)\) printed in [O] applies there to Coble and Enriques surfaces and must not be substituted indiscriminately for a K3 surface.

## 5. Literature-version caution and stopping point

Kikuta's first arXiv version [K1], Example 4.13, asserted a different rank-three counterexample using a uniform-lattice claim. That example and the corresponding abstract claim are absent from versions 2 and 3. We do not use it. Absence of roots is compatible with rational isotropic classes and noncompact arithmetic quotients; it does not by itself imply cocompactness. The accepted witness above is the distinct rank-five example explicitly retained in the current Fujiwara–Oguiso–Yu paper.

The dated inherited “partially solved” triage is therefore not an adequate status for the universal wording. The correct conclusion supported here is **false by prior literature**. We stop after the first substantive literature-verification approach. We make no new solution claim, no exact dimension claim, and no assertion that the separate Enriques, Coble, section-required, or positive-maximum-rank variants have been settled.

## References

- [O] Shigeru Mukai, “Automorphism of K3 surfaces and decomposition groups of rational sextics,” in *Classical Algebraic Geometry*, Oberwolfach Reports 33/2018, Conjecture 1, printed p. 2024. DOI: https://doi.org/10.4171/owr/2018/33 . Public PDF: https://ems.press/content/serial-article-files/46758?nt=1 .
- [F] Koji Fujiwara, Keiji Oguiso, Xun Yu, *On K3 surfaces with hyperbolic automorphism groups*, arXiv:2507.13726v3, 2 May 2026, Remark 1.5(4). https://arxiv.org/abs/2507.13726v3 ; https://arxiv.org/pdf/2507.13726v3 . Related journal DOI: https://doi.org/10.1515/crelle-2026-0036 . The checked arXiv metadata describes this as the final version to appear in Crelle's journal; no separate publication-date determination is required here.
- [N] V. V. Nikulin, *Quotient-groups of groups of automorphisms of hyperbolic forms by subgroups generated by 2-reflections. Algebro-geometric applications*, 1981; English translation, *Journal of Soviet Mathematics* 22 (1983), 1401–1475. https://www.mathnet.ru/eng/intd51 ; https://doi.org/10.1007/BF01094757 . The classification is used through the explicit current statement in [F]; the Russian scan's introductory theorem statements were also inspected. Its full proof was not re-audited here.
- [H] Daniel Huybrechts, *Lectures on K3 Surfaces*, author's draft, Chapters 11, 14, and 15 as cited. https://www.math.uni-bonn.de/people/huybrech/K3Global.pdf .
- [T] Taiki Takatsu, *Blown-up boundaries associated with ample cones of K3 surfaces*, arXiv:2312.13831v2, 11 February 2024. https://arxiv.org/abs/2312.13831v2 ; https://arxiv.org/pdf/2312.13831v2 .
- [K] Kohei Kikuta, *Geometrical finiteness for automorphism groups via cone conjecture*, arXiv:2406.18438v3, 12 May 2026. https://arxiv.org/abs/2406.18438v3 ; https://arxiv.org/pdf/2406.18438v3 .
- [K1] Historical version of [K], 26 June 2024: https://arxiv.org/pdf/2406.18438v1 . Consulted only to exclude an obsolete argument.
