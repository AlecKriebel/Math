# Bennequin sharpness and the missing transverse surface construction

**Problem 2728, KP-1.69. Unresolved after two substantive approaches.** This document records credited standard reductions and the exact remaining gaps. It gives no proof or counterexample to the general question and makes no discovery claim. Separate adversarial review is pending.

## 1. Original question and current status

The original statement in *K3: A New Problem List in Low-Dimensional Topology*, Problem 1.69, printed pp. 65–66, starts with a positively transverse link $T\subset(S^3,\xi_{\mathrm{std}})$ and a Seifert surface $\Sigma\subset S^3$ satisfying
\[
\operatorname{sl}(T)=-\chi(\Sigma).
\tag{1}
\]
It asks whether the link must be strongly quasipositive. The surface is a three-dimensional Seifert surface, not an arbitrary surface in $B^4$. There is no fiberedness, canonical-surface, braid-index, or fractional Dehn twist coefficient assumption.

The general converse remains a conjecture in the current primary source checked here: Stoimenow, *Realizing Strongly Quasipositive Links and Bennequin Surfaces*, published 1 April 2026, states it as Conjecture 2.5 on p. 258. His Corollary 4.31 covers canonically minimal links, and the paper reports verification for prime knots through 16 crossings. This attempt does not independently reproduce that classification.

The older Ito–Kawamuro paper distinguishes the corresponding transverse formulation explicitly: its Conjecture 2 asks for a strongly quasipositive braid representing the given transverse link. Producing such a representative would in particular answer the original question affirmatively. We retain the transverse link throughout the reduction below, so no replacement by a different transverse representative is hidden.

## 2. Exact band accounting

We use the disk open book of $S^3$. A band word is written in the embedded band generators
\[
\sigma_{i,j}=(\sigma_{j-1}\cdots\sigma_{i+1})
\sigma_i(\sigma_{j-1}\cdots\sigma_{i+1})^{-1},
\qquad 1\leq i<j\leq n,
\]
and their inverses, following [IK, p. 1]. Let $w$ be such an $n$-strand braid word whose closure represents the **same transverse link** $T$. Write $b_+(w),b_-(w)$ for its positive and negative band counts. The associated embedded disk-and-band surface $F_w$ has
\[
\chi(F_w)=n-b_+(w)-b_-(w),\qquad
\operatorname{sl}(T)=b_+(w)-b_-(w)-n.
\tag{2}
\]
The first formula counts handles. The second is the braid self-linking formula, since each band generator has Artin exponent sum one. Neither formula requires $F_w$ to have minimal genus.

Combining (1) and (2) gives
\[
\boxed{\ \chi(\Sigma)-\chi(F_w)=2b_-(w).\ }
\tag{3}
\]
Thus a braided surface for the same transverse link realizes the Euler characteristic of the sharp surface if and only if it has no negative bands. In that case its boundary has a strongly quasipositive braid representative.

This is the zero-defect case of [IK, Observation 1.2], not a new criterion. The point of displaying the equality is to identify the entire missing geometric step:

> Construct a disk-and-band surface of Euler characteristic $\chi(\Sigma)$ whose boundary is transversely isotopic to the original sharp link.

For precision, let $\chi_B(T)$ be the largest Euler characteristic among disk-and-band surfaces obtained from all braid words representing $T$. This maximum exists: there is at least one braid representative, and (3) bounds the integer values above by $\chi(\Sigma)$. Equivalently, let $\kappa(T)$ be the minimum number of negative bands in such a word. Then
\[
\kappa(T)=\frac{\chi(\Sigma)-\chi_B(T)}2.
\tag{4}
\]
The desired transverse construction is exactly the statement $\kappa(T)=0$. Giving it a name or writing (4) does not bound it. Proving that every sharp link has $\chi_B(T)=\chi(\Sigma)$ would supply the missing result rather than simplify it to an established theorem.

These formulas apply to links and do not assume that all Seifert surfaces have the same number of connected components. They compare Euler characteristics directly; no knot-genus formula has been substituted for a link formula.

## 3. Why the topological braiding theorem is insufficient

[IK, Theorem 1.7 and its proof on manuscript pp. 17–18] constructs a minimal-genus braided surface for a **topological** link type. The proof explicitly uses both positive and negative braid stabilizations to remove tiles. It does not establish the required construction for a fixed transverse link.

Indeed, under positive stabilization, the strand number and exponent sum each increase by one, so self-linking is unchanged. Under negative stabilization they change by $+1$ and $-1$, respectively, so
\[
\operatorname{sl}(T_{\mathrm{negative\ stab}})
=\operatorname{sl}(T)-2.
\tag{5}
\]
Both operations preserve the smooth link type. Only the positive operation preserves the transverse type in the transverse Markov theorem. Therefore the topological theorem cannot be used in (3) with the original value of self-linking without an additional argument.

For a concrete control, the positive trefoil braid $\sigma_1^3$ has two strands, exponent sum three, self-linking one, and disk-and-band Euler characteristic $-1$. Its negative stabilization $\sigma_1^3\sigma_2^{-1}$ has the same smooth knot type and the same surface Euler characteristic $-1$, but self-linking $-1$ and one negative band. This example does not refute the question; it demonstrates exactly the lost hypothesis in that proposed shortcut.

There is also no obstruction in merely finding many negative bands in a word. For each $N\geq0$,
\[
w_N=\sigma_1^3(\sigma_1\sigma_1^{-1})^N\in B_2
\]
is the same braid element as the positive trefoil braid. Its displayed surface has $N$ negative bands and Euler characteristic $-1-2N$, in exact agreement with (3). The minimum over all representatives, not the count in one presentation, is the relevant quantity.

## 4. The signed-singularity and canonical-surface approaches

The open-book-foliation formulas [IK, Lemma 3.1] read
\[
\chi(\Sigma)=e_++e_--h_+-h_-,\qquad
\operatorname{sl}(T)=-(e_+-e_-)+(h_+-h_-).
\tag{6}
\]
Here $e_\pm$ and $h_\pm$ count elliptic and hyperbolic singularities of the indicated signs. Sharpness therefore gives
\[
e_-=h_-,
\tag{7}
\]
not the separate conclusions $e_-=h_-=0$. A Bennequin surface has $e_-=0$; reaching that configuration while preserving the transverse boundary is the essential issue.

For example the nonnegative numerical tuple
$(e_+,e_-,h_+,h_-)=(2,1,3,1)$ satisfies (6) with
$\chi=-1$ and $\operatorname{sl}=1$. This is only a consistency check on the counts. We do not claim a geometric realization of this tuple, a counterexample, or the impossibility of eliminating its negative singularities. Equality of counts does not specify the separatrices or the allowed cancellation moves.

The precise obstruction already appears in the published construction: [IK, Lemma 4.9] removes an $ab$-tile by a stabilization whose sign is opposite to the tile's hyperbolic sign. Removing positive tiles can therefore require negative stabilization. The general zero-defect case supplies no argument here that all necessary moves can be chosen transverse-preserving. The paper obtains this control under additional fractional Dehn twist hypotheses; those hypotheses are absent from Problem 1.69.

The second substantive approach uses canonical surfaces. For knots, the classical slice-Bennequin and genus inequalities give
\[
\operatorname{sl}(T)\leq 2\tau(K)-1
\leq 2g_4(K)-1\leq 2g(K)-1.
\tag{8}
\]
If the knot satisfies (1), the ordinary Bennequin inequality first forces $\Sigma$ to have minimal genus, and then (8) forces
$\tau(K)=g_4(K)=g(K)$. When a canonical Seifert surface realizes $g(K)$, [FLL, Theorem D and Corollary E] supplies strong quasipositivity. This is a known positive case, not a solution for arbitrary surfaces.

For a hypothetical knot counterexample, these results force its canonical genus to exceed its Seifert genus. Nothing in (8) proves that a genus-minimizing surface is canonical. No construction removing that gap, and no verified knot or link counterexample, was obtained in this attempt.

## 5. Remaining target and exclusions

The general question remains unresolved here. The first route stops at the missing construction of a maximal-Euler-characteristic braided surface for the fixed sharp transverse link. The second stops at the absent canonical-surface hypothesis. The finite checks accompanying this note verify the displayed numerical identities and stabilization effects; they do not certify geometric realizability, transverse isotopy, or quasipositivity of arbitrary braids.

Problem 2729 / KP-1.70 asks separately about surfaces in the four-ball and about quasipositive links with equal Seifert and slice genus. It is related but is not the same target. The stronger question about **every** minimal-genus Seifert surface and the general-contact-manifold question in the remarks are likewise not silently substituted for Problem 1.69.

## Sources

- *K3: A New Problem List in Low-Dimensional Topology* (2026), Problem 1.69 and all remarks, printed pp. 65–66. [Author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf). The exact statement on p. 65 was visually checked. The dataset's four-page AIM report is not the complete source.
- T. Ito and K. Kawamuro, *The defect of the Bennequin–Eliashberg inequality and Bennequin surfaces*, Indiana University Mathematics Journal **68** (2019), 799–833. [Author version](https://arxiv.org/abs/1703.09322), [DOI](https://doi.org/10.1512/iumj.2019.68.7662). Definitions and Observation 1.2, Conjectures 1–2, Lemmas 3.1 and 4.9, and the proof of Theorem 1.7 were read in the complete author PDF.
- P. Feller, L. Lewark and A. Lobb, *Almost positive links are strongly quasipositive*, Mathematische Annalen **385** (2023), 481–510. [Author version](https://arxiv.org/abs/1809.06692), [published full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9889511/), [DOI](https://doi.org/10.1007/s00208-021-02328-x). Theorem D, Corollary E and their proofs were checked.
- A. Stoimenow, *Realizing Strongly Quasipositive Links and Bennequin Surfaces*, Publications of the Research Institute for Mathematical Sciences **62** (2026), 245–339, published 1 April 2026. [Publisher page and full text](https://ems.press/journals/prims/articles/14299640), [DOI](https://doi.org/10.4171/PRIMS/62-2-1). Conjecture 2.5, printed p. 258, was checked visually; Corollary 4.31 and the scope of Appendix B were checked. The original author-page PDF URL returned 404; the complete publisher PDF was successfully retrieved instead.
