# KP 1.63: fixed-knot infinitude remains unresolved

**Status:** Unresolved, with credited structural obstructions to two attempted routes. Independent review pending. No novel theorem or counterexample is claimed.

## 1. Exact scope

Fix the standard tight contact structure on \(S^3\), equivalently work in standard contact \(\mathbb R^3\). For an oriented smooth knot type \(K\), let \(\mathcal L(K)\) be its Legendrian isotopy classes, and put
\[
 \mathcal P(K)=\mathcal L(K)\setminus
 \bigl(S_+\mathcal L(K)\cup S_-\mathcal L(K)\bigr).
\]
Thus a peak is a class admitting neither sign of destabilization, even after Legendrian isotopy. Absence of a visible zigzag in one diagram does not suffice.

The question asks whether **one fixed \(K\)** has peaks with \(tb\) unbounded below. Allowing \(K\), the contact structure, or the ambient manifold to change changes the problem. Forgetting knot orientation changes each class by at most a two-element choice, so the existence/finiteness issue is equivalent to the oriented formulation used below.

The source is K3 Problem 1.63, pp. 61–62, tracing back to Etnyre–Ng, Question 44, p. 12 of the author PDF. The latter's Part II explicitly fixes \((S^3,\xi_{\rm std})\). The K3 background's sentence placing classified examples immediately after the infinitude equivalence has a defective antecedent: those classifications establish finiteness, not the requested fixed-type infinitude.

## 2. The finiteness equivalence and its missing bound

We use two credited results:

- The Bennequin inequality bounds \(tb\) above for each fixed smooth knot type.
- Colin–Giroux–Honda, Theorem 10, proves finiteness of Legendrian isotopy classes in standard \(S^3\) at a fixed smooth type and fixed \(tb\). No additional fixed rotation number is needed in that theorem.

It follows that the following are equivalent for fixed \(K\):

1. \(\mathcal P(K)\) is finite.
2. The integers \(tb(\mathcal P(K))\) are bounded below.
3. There is a finite list of Legendrian classes of type \(K\) such that every class is obtained from an element of the list by finitely many stabilizations.

Indeed, (1) implies (2). Under (2), the integer \(tb\)-values of peaks lie in a finite interval, and each level contains finitely many classes, giving (1). Every successive destabilization raises \(tb\) by one, so any destabilization process terminates at a peak. This proves (1) implies (3). Conversely, a peak cannot be obtained from a different class by a nonempty stabilization sequence; under (3), every peak must itself occur on the finite list.

This is an equivalence, not a proof of any of its three assertions for every \(K\). Fixed-level finiteness does not control an infinite sequence of successively lower levels.

## 3. Route 1: connected sums cannot create the missing infinitude from finite factors

Write the oriented prime decomposition of a nontrivial knot as
\[
 K=\mathop{\#}_{i=1}^{s} K_i^{\#m_i},
\]
where the \(K_i\) are pairwise distinct oriented prime types, \(m_i\ge1\), and \(m=\sum_i m_i\).

**Credited structural fact.** Etnyre–Honda's connected-sum classification, Theorem 3.4, identifies \(\mathcal L(K)\) with the product of the factor class sets, modulo transfers of a stabilization between factors and permutations of identical prime types. Its restriction to peaks is
\[
 \mathcal P(K)\ \cong\
 \prod_{i=1}^{s}\operatorname{Sym}^{m_i}\mathcal P(K_i).          \tag{1}
\]
This restriction is already stated explicitly in Byung Hee An's Corollaries 7–8 (2016). No novelty is claimed for it.

For completeness, the restriction has a short check. A tuple with a stabilized factor produces a stabilized connected sum, since a stabilization can be placed in that factor. Conversely, a tuple all of whose factors are peaks admits no stabilization-transfer move in either direction: both ends of every such move contain a stabilized factor. Its equivalence class therefore consists only of the permitted permutations. If its connected sum were stabilized, the classification and compatibility with stabilization would identify it with a tuple containing a stabilized factor, which is impossible. This also proves that two peak tuples define the same peak exactly when the permitted permutations relate them.

Two exact consequences are:
\[
 |\mathcal P(K)|=
 \prod_{i=1}^{s}\binom{p_i+m_i-1}{m_i},
 \qquad p_i=|\mathcal P(K_i)|<\infty,                           \tag{2}
\]
and, if every factor peak set is finite,
\[
 \min_{\mathcal P(K)}tb=
 \sum_{i=1}^{s}m_i\min_{\mathcal P(K_i)}tb+(m-1).               \tag{3}
\]
The latter follows from the standard identity
\(tb(L_1\#L_2)=tb(L_1)+tb(L_2)+1\); each factor minimum is attained independently.

Every knot type has at least one peak by the terminating-destabilization argument. Therefore (1) proves that \(\mathcal P(K)\) is infinite exactly when at least one prime-factor peak set is infinite. In particular, any counterexample to the universal finiteness conjecture already has a prime-knot counterexample.

This closes the attempted connected-sum amplification route: increasing the number of factors may produce more and more peaks, but it changes the smooth knot type. Keeping the decomposition fixed and starting from finite peak sets cannot produce KP 1.63's example.

## 4. Route 2: finite-dimensional DGA certificates stop at maximal \(tb\)

Let \((\mathcal A(L,*),\partial)\) denote the based Chekanov–Eliashberg DGA over \(\mathbb F_2\) in Ng–Rutherford's conventions, including the invertible basepoint generator \(t\). A finite-dimensional representation here is a **unital** algebra map
\[
 \varphi:\mathcal A(L,*)\longrightarrow
          \operatorname{End}_{\mathbb F_2}(V),\qquad
 0<\dim_{\mathbb F_2}V<\infty,\qquad \varphi\partial=0.
                                                               \tag{4}
\]
An ungraded representation is 1-graded in the source's terminology.

**Published obstruction.** Ng–Rutherford, Theorem 4.9 (also Theorem 1.2), proves that (4) forces
\[
                         tb(L)=\overline{tb}(K).                \tag{5}
\]
This includes scalar augmentations and every positive finite matrix dimension. Merely enlarging matrices does not bypass this obstruction. The claim here is over \(\mathbb F_2\) with the cited based DGA; it is not extended to unverified coefficient conventions.

A useful explanation of the mechanism is the following elementary lemma.

**Certificate-ceiling lemma.** Suppose a property \(Q\) of Legendrian classes (a) depends only on smooth type and \(tb\), and (b) is false for every stabilized knot. Then \(Q(L)\) implies \(tb(L)=\overline{tb}(K)\).

**Proof.** If \(tb(L)<\overline{tb}(K)\), choose a representative \(L_{\max}\) attaining the maximum and stabilize it \(\overline{tb}(K)-tb(L)>0\) times. The result \(L'\) has the same smooth type and \(tb\) as \(L\). By (a), \(Q(L)=Q(L')\), while (b) makes the latter false. \(\square\)

For (4), topological-type/\(tb\) invariance in each fixed dimension is part of Ng–Rutherford's theorem, obtained via satellite rulings. Stabilization precludes a unital representation because its DGA has a chain with differential \(1\). The scalar case also follows from the normal-ruling/augmentation correspondence and the Kauffman-bound characterization. These are imported published inputs, not re-proved contact-topological results in this package.

For a fixed \(K\), all sufficiently negative members of any family sought by KP 1.63 necessarily satisfy \(tb<\overline{tb}(K)\). None can be certified by (4). This obstructs the attempted finite-dimensional certificate route, not the knots' existence or nondestabilizability.

## 5. Why failure of those certificates is not destabilization

Nonzero associative algebras need not have nonzero finite-dimensional unital representations. Here is the standard Leavitt-type algebraic diagnostic, not a claimed Legendrian realization.

Over \(\mathbb F_2\), take the unital algebra generated by \(a_0,a_1,b_0,b_1\) subject to
\[
 a_i b_j=\delta_{ij}1,\qquad b_0a_0+b_1a_1=1.                 \tag{6}
\]
It is nonzero: on the vector space with basis \(e_0,e_1,\ldots\), define
\[
 b_i(e_n)=e_{2n+i},\qquad
 a_i(e_{2n+j})=\delta_{ij}e_n.
\]
These operators satisfy (6), and the identity operator is nonzero. They act on the algebraic direct sum, so no convergence issue arises.

On a nonzero finite-dimensional \(V\), however, the maps
\[
 A:V\to V\oplus V,\quad A(v)=(a_0v,a_1v),\qquad
 B:V\oplus V\to V,\quad B(u,v)=b_0u+b_1v
\]
would satisfy \(AB=I_{V\oplus V}\) and \(BA=I_V\). Hence \(\dim V=2\dim V\), impossible for a positive finite integer dimension. This uses dimension, not a trace argument that could fail in characteristic two.

The distinction occurs in actual Legendrian topology as well. Ng–Rutherford Remark 4.10 credits nonmaximal-\(tb\), nontrivial-DGA examples of Shonkwiler–Vela-Vick without finite-dimensional representations. In the other direction, Sivek's published example of the mirror of \(10_{132}\) has a maximal-\(tb\) representative with trivial contact homology. A maximal-\(tb\) representative cannot destabilize. Thus even vanishing contact homology is not a destabilization criterion. These examples are credited literature controls, not constructions or full DGA computations revalidated here.

## 6. Grid and algorithm scope

Dynnikov–Prasolov's current arXiv version 2309.05087v1 (2023), Conjectures 1.1 and 1.3, retains the peak-finiteness problem and its rectangular-diagram counterpart. Their Theorem 1.4 supplies an algorithm for comparing two Legendrian links; that is not an effective uniform bound on the sizes of all nonsimplifiable diagrams of one knot type.

Here nonsimplifiability excludes a sequence of exchange moves and destabilizations containing at least one destabilization and no stabilization. Testing only immediately removable corners of one diagram is weaker. A finite search at bounded grid size, or a decision procedure for comparing each given pair, does not certify that no further peaks occur at arbitrarily large sizes.

## 7. Exact stopping point

Two substantive routes were examined and stopped at structural obstructions:

1. Fixed connected sums of classified factors: cannot create infinitude; a prime factor would already need the unresolved property.
2. Augmentations or finite-dimensional \(\mathbb F_2\) DGA representations: force maximal \(tb\), excluding the desired unbounded-negative sequence from this certificate class.

What remains is a fixed prime smooth knot type with peaks at unboundedly negative \(tb\), certified by a method outside those finite-dimensional representations, or a proof of a type-dependent lower peak bound for every prime type. Neither has been established in this attempt. No example in another contact manifold, no varying-knot family, and no finite enumeration settles that gap.

The exact controls in *verify.py* validate finite symmetric-product counts, connected-sum \(tb\) arithmetic, the ceiling lemma on finite models, and (6) on basis vectors. They are not computations of all Legendrian representatives or a knot-diagram search.

## References

1. R. İ. Baykur, R. Kirby, D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, Problem 1.63, pp. 61–62, 2026. [Author copy](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
2. J. Etnyre, L. Ng, *Problems in Low Dimensional Contact Topology*, Proc. Sympos. Pure Math. 71 (2003), 337–357, Question 44. [Author PDF](https://etnyre.math.gatech.edu/preprints/papers/problems.pdf).
3. V. Colin, E. Giroux, K. Honda, *Finitude homotopique et isotopique des structures de contact tendues*, Publ. Math. IHÉS 109 (2009), 245–293, Theorem 10, §5, Question 61. [Published PDF](https://www.numdam.org/article/PMIHES_2009__109__245_0.pdf).
4. J. Etnyre, K. Honda, *On connected sums and Legendrian knots*, Adv. Math. 179 (2003), 59–74; Theorem 3.4 and Lemma 3.3. [Author preprint](https://arxiv.org/abs/math/0205310).
5. B. H. An, *A criterion for the Legendrian simplicity of the connected sum*, Topology Appl. 204 (2016), 175–184, Corollaries 7–8. [DOI](https://doi.org/10.1016/j.topol.2016.03.011); [author preprint](https://arxiv.org/abs/1503.01188).
6. L. Ng, D. Rutherford, *Satellites of Legendrian knots and representations of the Chekanov–Eliashberg algebra*, Algebr. Geom. Topol. 13 (2013), 3047–3097, Theorems 1.2 and 4.9, Remark 4.10. [Published PDF](https://msp.org/agt/2013/13-5/agt-v13-n5-p16-s.pdf).
7. S. Sivek, *The contact homology of Legendrian knots with maximal Thurston–Bennequin invariant*, J. Symplectic Geom. 11 (2013), 167–178. [Author preprint](https://arxiv.org/abs/1012.5038).
8. I. Dynnikov, M. Prasolov, *An algorithm for comparing Legendrian knots*, 2023, Conjectures 1.1 and 1.3, Theorem 1.4. [Current preprint](https://arxiv.org/abs/2309.05087).
