# Independent review: free-Lie current algebra partial results

**Verdict: PASS for the known reduction, elementary layers, and credited low-degree translations.** The unrestricted polynomial-functor decomposition remains unresolved. No substantive mathematical revision is required, and none of the displayed reductions should be promoted to a full answer.

**Target:** 30003713 / OWR2018/2, Question 13.  
**Reviewed document:** PARTIAL.md.  
**SHA-256:** 18a8e197df03ba5d1127874233b93f8dd96599b499ddaa2e1fa816f81c380362.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This is an independent AI source and mathematical review, not human peer review or formal verification. The package makes no novelty claim for the known formulas.

## Source scope and attribution

[Petersen's question in the original report](https://ems.press/content/serial-article-files/46724), printed p. 118, explicitly asks for a sum of polynomial functors in both vector spaces. It also notes that the case of a one-dimensional square-zero ideal can be calculated by hand. It does not ask merely for a chain complex or a renamed kernel. The package correctly preserves this stronger target.

The [2017 discussion by Petersen and Tosteson](https://mathoverflow.net/questions/273196/homology-of-an-interesting-lie-algebra) already contains the adjoint-coefficient reformulation, the two-term tensor-algebra calculation, and the Whitehouse-module interpretation of the adjoint case. Petersen explicitly distinguishes this reformulation from evaluating the homology. The provenance claim is therefore supported directly by the original discussion.

[Gadish–Hainaut](https://ahl.centre-mersenne.org/item/10.5802/ahl.213.pdf) states its complete computational range of at most ten particles and additional families; Section 4.4 supplies the relevant coefficient dictionary. [Powell's 2023 structural paper](https://arxiv.org/abs/2309.07607) describes a differential graded category and two-term complex, not an all-degree irreducible decomposition. [Powell's relative-degree-two paper](https://arxiv.org/abs/2507.03453v4) has the precise restricted theorem used in the package. The publisher independently gives its online publication date as [4 March 2026](https://www.tandfonline.com/doi/abs/10.1080/10586458.2025.2608243). These statements support the package's attribution and limited-literature wording.

## Direct decomposition and the action complex

The square-zero ideal gives a split semidirect product with abelian ideal $M=E\otimes L(V)$. In the Chevalley–Eilenberg complex, an $L$–$L$ bracket decreases the number of $L$ factors by one and preserves the number of ideal factors. An $L$–$M$ bracket does the same, while an $M$–$M$ bracket is zero. Thus the number of ideal factors is preserved by the differential. The resulting direct-sum decomposition by that number is an actual decomposition of complexes. There is no unresolved spectral-sequence extension issue.

For $T(V)$, the augmentation ideal is free on the last letter as a left module, or on the first letter as a right module. The displayed left-module resolution has the usual right-module counterpart under the opposite-algebra identification. Tensoring that resolution with a left coefficient module gives the two-term action complex $V\otimes N\to N$, up to the harmless global sign associated with left/right Lie-module conventions. This validates the formula used for homology, including arbitrary coefficient modules.

Only homological degrees zero and one survive for this coefficient calculation. At total homological degree $n$, the ideal-factor degrees are consequently $n$ and $n-1$, giving exactly the cokernel and kernel in equation (1). Scaling $E$ distinguishes these two weights naturally. The $r=0$ map is zero, so the low-degree and zero-variable edge cases also follow correctly.

The exterior Cauchy identity has the correct conjugate partition. The free Lie algebra is infinite-dimensional, but every fixed homogeneous degree in $V$ is finite-dimensional, so the identity applies degree by degree and then as a direct sum. Naturality makes the action map preserve each $E$-isotypic component. This establishes the remaining Schur-functor action maps in equation (2), without calculating their general kernels or cokernels.

## The first ideal-weight layer

For ideal weight one, the coefficient module is $E\otimes L(V)$ and its homology is the adjoint homology tensored with $E$. Surjectivity of the degree-$d$ bracketing map for $d\geq2$ follows because brackets with a generator span the free Lie algebra in that degree: Jacobi recursively rewrites arbitrary bracketings in that form. Hence the stated short exact sequence is valid.

The Frobenius characteristic of the source is $p_1\ell_{d-1}$, and the target has characteristic $\ell_d$. Their difference gives the kernel character. This is an equality for an actual kernel representation, supported by the surjective short exact sequence; it is not an unsupported assumption about cancellation in a virtual character.

The components in degrees two, three and four are respectively $\operatorname{Sym}^2V$, $\Lambda^3V$ and $S_{(2,2)}V$. Powell's Example 3.1 identifies the full kernel with the cyclic-Lie functor, with the same convention. Ideal weight one contributes only to total homological degrees one and two. The package correctly distinguishes this single weight from the full specialization $\dim E=1$, which retains every exterior coefficient degree.

For $\dim V=1$, the free Lie algebra is one-dimensional and abelian, so the entire current algebra is abelian. Its exterior-algebra homology agrees with the two summands in equation (1) by the exterior-power formula for a direct sum. The $E=0$ and $V=0$ cases are also consistent.

## Audit of the recent theorem's translation

Powell's Proposition 3.3 and Theorem 1 were checked with the paper's explicit symmetric-group conventions: row partitions denote trivial representations and column partitions denote sign representations. The additional $S_r$ action permutes the coefficient tensor factors in the ordinary, ungraded way.

The exterior power introduces exactly one additional sign representation:
\[
\Lambda^r(E\otimes L)
=\bigl(E^{\otimes r}\otimes L^{\otimes r}\otimes\operatorname{sgn}_r\bigr)_{S_r}.
\]
The Lie action commutes with this permutation action. Over characteristic zero, taking coinvariants and tensoring with the finite tensor power of $E$ are exact, so they commute with the two-term homology. This proves equation (3).

On the first nonzero diagonal, Powell gives a trivial coefficient-permutation representation times the divided power of $V$. The exterior sign twist therefore produces $\Lambda^rE$, and characteristic zero identifies divided with symmetric powers. This gives exactly equation (4), including the vanishing below that diagonal.

On the next diagonal, the first source summand already carries the sign representation, so the extra exterior sign cancels it and produces $\operatorname{Sym}^rE$. The second source summand is trivial, so it produces $\Lambda^rE$. The $V$ partitions and total degrees are unchanged. This is exactly equation (5). The exceptional $r=1$ case has one copy of $\Lambda^3V$, not two, and the package handles it separately.

These translations are valid over $\mathbb C$: each homogeneous calculation and all maps are defined over $\mathbb Q$, and scalar extension is exact. Partition lengths exceeding the vector-space dimension simply give zero functors. The sign twist is thus correct even in small-dimensional evaluations.

## Independent exact checks

The author's script was rerun in an isolated directory. Its nine adjoint models and 52 abelian edge cases passed, and the JSON receipt reproduced byte for byte.

The separate independent_checks.py constructs free-Lie components by spanning generator commutators in the tensor algebra and selecting an exact independent basis. It then builds the exterior coefficient action, including the sorting signs in wedge products. This is independent of the author's Lyndon-word basis implementation.

Nine finite action matrices passed exact rational rank checks. They include an ideal-weight-two model with $\dim E=1,\dim V=4$, whose degree-four kernel has dimension one; a model with $\dim E=2,\dim V=3$, whose corresponding kernel has dimension three; and the ideal-weight-three first diagonal with $\dim E=\dim V=3$, whose kernel has dimension fifteen. These test both different sign twists and nontrivial higher ideal weights. Three cyclic-Lie character identities were also verified. The receipt lists every matrix size, rank and predicted dimension. Reproduce from this directory with python independent_checks.py.

These finite checks test the translation, signs and degree conventions. They do not prove arbitrary-degree multiplicities. The general low-diagonal formulas rest on the explicitly cited theorem and the exact coinvariant argument.

## Remaining gap and disposition

The requested answer still requires the Schur kernels in every ideal weight and every unrestricted $V$ degree. The package has not evaluated those multiplicities. An Euler-characteristic relation alone fixes only a difference; it becomes sufficient for the cokernel once the kernel is independently known, but it cannot determine both simultaneously.

The known adjoint layer and the two quoted diagonals therefore constitute partial information, not the full polynomial-functor answer. The package states this distinction correctly and should retain an unresolved queue status. This review supplies no assertion that the bounded literature check is exhaustive and no new discovery claim.
