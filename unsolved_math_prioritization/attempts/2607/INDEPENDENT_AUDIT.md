# Independent adversarial audit: KOU-21.98 / catalogue 2607

Date: 2026-10-03 UTC.

## Verdict

**PASS as an unresolved five-attempt partial-research package.** No blocking mathematical error was found in the affirmative propositions in the frozen release. The original question is not resolved, and this audit does not authorize representing it as solved or establishing novelty or exhaustive current openness. No sixth proof-search attempt was performed.

Audit target: the eleven-file author package preserved at [WIP commit 6bb9c35](https://github.com/AlecKriebel/Math/commit/6bb9c35a799cf1760784eaf6cc7e4e770b2772b2). The audit verified the frozen contents and their file hashes; it did not verify the remote branch state. The five original attempt files are unchanged. No proof-search attempt was added by the audit.

The finite controls were both replayed and independently reimplemented. Their results support the explicit mechanisms only; the universal statements were checked by the written arguments below.

## 1. Normal-set and soluble reductions: PASS

**Common powers.** For infinite-order elements, common nonzero powers give an equivalence relation even in a group without unique roots. If a^p=b^q and b^r=c^s, then a^(pr)=b^(qr)=c^(sq). No commutation between a and c is needed. Conjugation preserves the relation, and an infinite cyclic subgroup meets at most one class of infinite-order elements. The finite class-permutation kernel G_0 therefore exists as claimed.

**Ratio and denominator argument.** A relation (x^g)^a=x^b determines b/a uniquely: comparing it with (x^g)^c=x^d gives x^(bc)=x^(ad), hence bc=ad. Conjugating and powering the two relations for g and h gives the multiplicative ratio for gh. This uses only powers of the same element at each step. If a covering cyclic group <c_i> meets x's class, its generator has a relation c_i^(a_i)=x^(b_i). An element c_i^k has ratio k b_i/a_i. Thus one denominator D works for all the covered conjugates of the fixed x. Applying this to x^(g^n) for every positive and negative n forces r(g)=+1 or -1: any prime in the reduced numerator or denominator otherwise yields unbounded denominators in one of the two directions.

**FC conclusion.** Within each covering cyclic group, either permitted ratio determines at most one exponent k. Consequently there are at most two permitted conjugates in that subgroup. This does not use unique roots in G. Finite-order elements also have finite conjugacy classes because each cyclic subgroup has only finitely many elements of any fixed bounded order. Passing from G_0 to G uses finite index and is valid.

**Finite generation and torsion.** Each <X intersect C_i> is cyclic and lies in H=<X>. Their chosen generators generate H; each chosen generator is a finite product from X and its inverses. Thus a finite subset of X generates H, not merely a finite subset of the original covering groups. Intersecting the finite-index centralizers of that finite subset gives C_G(H) of finite index. Hence H/Z(H) is finite, and Schur yields finite H'. The torsion subgroup of the finitely generated abelian group H/H' is finite, so its full preimage T is finite. It is characteristic in H and, in the verbal setting, normal in G. Since every element of T has finite order and every torsion element maps into the torsion subgroup of H/H', T is exactly the torsion of H. The quotient is a finite-rank free abelian group; the conjugation action is finite.

**Ambient reduction.** Taking all arguments of finitely many generating values produces a finitely generated subgroup K with w(K)=H, because the two inclusions are explicit. The original cover restricts by intersection with K. Quotienting by the finite normal subgroup T preserves the word-image hypothesis. The derived-word substitution assertion follows by induction on the two disjoint subtrees, including unequal subtree heights; deeper derived values are values of each shallower derived word. Therefore G^(h) is contained in w(G), and an abelian w(G) implies derived length at most h+1. There is no hidden residual-finiteness or nilpotence assumption.

The exact remaining target is indeed rank(H/T)<=1. No implication in this attempt establishes it.

## 2. Polynomial and locally nilpotent argument: PASS

The polynomial-image lemma is sound. For each proper rational subspace not containing the whole image, some rational annihilating functional has nonzero composition with F. Their product is nonzero in the rational polynomial ring but vanishes on all of Z^d. The lattice is Zariski dense, as the stated induction on the variables proves, giving the contradiction. A full ambient subspace makes the conclusion immediate. This proof requires one polynomial map on one integral lattice, which the text explicitly retains.

For a finitely generated torsion-free nilpotent group, the stated Mal'cev rational-completion/BCH input and an integral Mal'cev coordinate parametrization are standard applicable structural results. Composition of truncated BCH expressions makes the logarithm of each fixed word polynomial. Powers of a covering generator have logarithms on its one-dimensional rational span. The image therefore lies on a single rational line. Such a line is a Lie subalgebra with additive BCH law; products and inverses remain on it. Finite generation of the verbal subgroup is then used essentially: a finitely generated additive subgroup of a one-dimensional rational vector space is cyclic after clearing finitely many denominators. No arbitrary subgroup-of-Q cyclicity claim is made.

For locally nilpotent G, the preceding finite-generation reduction gives one finitely generated nilpotent K with v(K)=v(G). The torsion subgroup U of this K is finite and characteristic, and K/U is torsion-free nilpotent. The descended verbal subgroup is cyclic and the original kernel H intersect U is finite. This proves finite-by-cyclic for every fixed word in the stated locally nilpotent class. There is no illicit assertion that all of a possibly infinitely generated locally nilpotent group's torsion is finite.

The Hall-polynomial input was independently checked against the introduction of [Cant–Eick's author preprint](https://arxiv.org/pdf/1801.02932). Mal'cev completion is separately identified as standard input, not falsely attributed as a new result proved in that paper. The proposed extension to arbitrary soluble groups is correctly rejected.

## 3. Affine variation and action bound: PASS

For substitutions g_i h_i with h_i in an abelian normal subgroup H, moving each correction to the right conjugates it by the appropriate fixed base-word suffix. Inverse letters contribute a negative correction with its corresponding conjugation. Corrections from other h_j do not change the action on H, because conjugation by H is trivial on H. Hence each coefficient is an integral sum of fixed conjugation operators, and the entire correction is exactly linear in the independently varying h_i. This remains valid for arbitrary group words, without a multilinearity assumption.

For w with values in H, every point of w(g)+sum_i D_i(g)(H) is an actual w-value. The affine-lattice lemma therefore applies to the image itself, rather than to arbitrary products in w(G). Independent vectors would produce infinitely many rational directions; otherwise the base point lies on the one-dimensional span. Since H is finitely generated, a nonzero image subgroup in that line really is a rank-one lattice.

Direct multiplication in the stated semidirect-product convention gives the translation part

A^(-1)(B^(-1)-I)v + A^(-1)B^(-1)(A-I)u.

The order of the factors is correct even when A and B do not commute. Substituting A=B=-I gives 2v-2u as claimed. When H is central, the corrections reduce to exponent sums; those sums vanish for commutator words. The central obstruction is genuine.

Conjugation permutes the finitely many actual nonzero value directions. A line-fixing lattice automorphism restricts to +1 or -1 on its rank-one lattice. Since the lines span H tensor Q, these signs determine the automorphism, giving the bound 2^s s!. This does not impose rank one.

Nonblocking clarity suggestion: define s explicitly as the number of lines Qx for **nonzero** word values x. The existing phrase “nonzero rational lines that actually contain w-values” is evidently intended in this sense; excluding the zero value explicitly prevents a literal ambiguity.

## 4. Derived-word rigidity: PASS

**Actual values, not products.** Use the standard convention delta_0(x)=x. Then c_0=h is a delta_0-value. A delta_(k-1)-value is a delta_i-value for every i<=k-1. Inductively, the two arguments of c_j=[c_(j-1),v] are delta_(j-1)-values, so c_j is an actual delta_j-value. Disjoint formal variable sets do not forbid assigning repeated group elements or copying a realizing tuple. Thus c_k ranges over the subgroup (M-I)^k H consisting of genuine delta_k-values.

**Matrix step.** A rank-two image subgroup would meet infinitely many rational lines, so the cyclic cover gives rank((M-I)^k)<=1. The action on H is finite by Attempt 1. Since k>=2, v is a commutator, and the determinant character on this G-invariant rational lattice kills it. A finite-order characteristic-zero matrix is semisimple; the ranks of positive powers of M-I are equal. If rank(M-I)=1, its rational invariant image is a one-dimensional nontrivial root-of-unity representation, necessarily eigenvalue -1, contradicting determinant one. Hence M=I. The displayed unipotent countercontrol correctly shows why finite order cannot be omitted.

**General conclusion.** Every delta_(k-1)-value centralizes H, so their generated subgroup K=G^(k-1) centralizes K'=H after quotient by T. Thus K/T is class at most two; equivalently gamma_3(K) is contained in the finite normal subgroup T in the original group. No finite generation of K is needed for this conclusion.

**Virtually abelian conclusion.** A finite-index abelian subgroup of a finitely generated G is finitely generated by Schreier. Taking a finite-index torsion-free subgroup and then its core gives the required normal finite-index free abelian A. Conjugation on A factors through the finite group G/A. For h in A, the same repeated-commutator construction gives actual delta_k-values in A and the same rank and determinant argument. Hence K centralizes A. The finite-index subgroup K intersect A is central in K, and Schur gives K'=G^(k) finite. Schur does not require K to be finitely generated. Every transition used in the written proof is justified.

The general class-two reduction does not supply a finite cyclic cover of all commutators of K: only commutators of individual delta_(k-1)-values are covered. The text correctly identifies this as an unproved premise and does not apply Attempt 2 without it.

Nonblocking clarity suggestion: explicitly introduce delta_0(x)=x before the induction; the construction already uses the standard convention correctly.

## 5. Heisenberg countermodel and counting diagnostic: PASS

The multiplication is the product of two upper-unitriangular 3x3 integer matrix laws. The inverse and commutator formulas have the correct signs. An element centralizing every horizontal basis vector must have all four horizontal coordinates zero; the two corresponding basis-pair commutators give the two central basis vectors. Thus both center and derived subgroup are exactly Z^2.

Conjugation fixes all four horizontal coordinates, inversion negates them, and an integer power multiplies them by that integer. Accordingly the specified set X, with at most one nonzero horizontal coordinate and arbitrary central coordinates, is normal in K, inverse closed, and closed under all integer powers. It contains a generating basis. For two such elements, only complementary coordinates in the same Heisenberg factor can produce a nonzero commutator, so every commutator is on one of the two central axes. Choosing the complementary coordinates n and 1 produces every element of either axis. The equality [X,X] as a **set** with the union of the two cyclic subgroups is correct. Its generated subgroup is Z^2, which is not finite-by-cyclic because it is torsion-free and noncyclic.

This refutes exactly the auxiliary normal/power-closed-generating-set inference. It does not realize X as the full value set of an outer commutator word in a common ambient G. The package repeatedly states this limitation and contains no false original-problem counterexample claim.

The stated role of the PCG-series theorem agrees with [Fernández-Alcober–Morigi, Theorem B and Definition 3.3](https://arxiv.org/abs/0911.3048): power closure is for selected generators in the relevant sections, not arbitrary products. The coordinate-axis counting example is also valid. For m=1+r(p-1), p^r<=2^(m-1) follows from p<=2^(p-1), so the cited exponential bound is compatible with every fixed r as p grows. That diagnostic does not purport to be a word-value realization.

## 6. Reproducibility and source/status checks

1. The frozen script was copied to a temporary directory and run there. The output was byte-identical to `control_results.json`, leaving the frozen release untouched.
2. `independent_controls.py` does not import the candidate's code. It uses SymPy exact matrix rank, determinant, and powers for all 442 signed permutation matrices in dimensions 1 through 4 and powers 1 through 5. It obtained 2,210 power/rank checks and 20 determinant-one/rank-at-most-one checks.
3. The Heisenberg calculation was independently represented by two 3x3 unitriangular matrices. Symbolic multiplication and inversion verified the commutator formula, the horizontal coordinates under conjugation, and inverse closure. Evaluation on the specified 153-element sample produced 23,409 successful pairs. The two actual basis commutators gave independent central generators. The 201 affine directions were independently distinguished by nonzero determinants.
4. The original controls also verify the order-three matrix and the unipotent hypothesis countercontrol. None of these finite enumerations substitutes for the universal proofs.
5. An image of the original Notebook page was visually inspected: 21.98 is the stated multilinear-word finite-cyclic-cover problem, attributed to M. Morigi and unstarred; the adjacent solved/problem notes concern other numbers. A live re-fetch of the Notebook PDF failed in this audit, so no fresh live-PDF-read claim is made. The editors' [October-update announcement](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/) was accessible.
6. The accessible [Acciarri–Shumyatsky survey, Problem 2.5, p. 243](https://ems.press/content/serial-article-files/43947) independently confirms the exact arbitrary-abstract-group question and its distinction from the lower-central and noncommutator results. The release's catalogue-access failure and restricted earlier full text are visible, rather than concealed.
7. There are five substantial, distinct written attempts. Their final status is explicitly unresolved, and no full-resolution or novelty claim is made. A bounded negative source search and an unstarred entry are explicitly not treated as exhaustive current-openness certificates.
8. The audited author package contains only the five attempts, README, research log, source scope, audit scope, control script, and control results. This publication also includes the full mathematical audit, its independent controls, and a clarity addendum. No source PDFs, screenshots, raw catalogue/research corpus, private conversation material, credentials, or internal receipts are included.

## Required repairs and remaining gap

**Required mathematical repairs: none found.** The two wording suggestions above are optional clarity improvements; they are not prerequisites for accepting the stated partial results.

**Unresolved original claim:** force all nonzero rational word-value directions to coincide in the finitely generated soluble reduction with a finite-rank free abelian verbal subgroup and finite conjugation action, or produce a genuine multilinear-word counterexample. Neither the affine restriction, the class-two reduction, the PCG-series citation, nor the auxiliary Heisenberg generating set provides that missing conclusion. Retain the unresolved 5/5 status.
