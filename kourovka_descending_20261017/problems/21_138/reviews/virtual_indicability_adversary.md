# Independent adversarial audit: virtually indicable IF groups

Audit checkpoint: **2026-10-24T17:01:35Z**. Reviewer: an independent AI subagent that did not author the proposed deduction. Audit completion estimate: **100% of this restricted review**; this does not measure completion of Kourovka 21.138. The parent research note currently estimates full-problem discovery at 12%.

Reviewed artifact: `../root_virtual_indicability.md`. No external individuals were contacted. No Git, publication, tracker, queue, or unrelated research operations were performed.

## Verdict and exact scope

**PASS as a restricted deduction from the cited established theorems. No outstanding substantive objection was found.** Every infinite finitely generated virtually indicable group in which every subgroup of infinite index is free is free or a closed aspherical surface group. Consequently, an actual finitely presented counterexample to 21.138 would have to be FAb.

This does **not** resolve 21.138: no argument establishes that an arbitrary finitely presented IF group is virtually indicable. The deduction is a synthesis of existing results, and the review certifies neither novelty nor first priority. It is not a formal verification or independent human peer review.

## Primary-source checks

1. [Gardam–Kielak–Logan, arXiv:2202.11093v2](https://arxiv.org/html/2202.11093v2), Proposition 3.5, is stated for every finitely generated group admitting an epimorphism to Z and having all infinite-index subgroups free. Its conclusion is hyperbolicity or being a surface group. There is no one-relator, two-generator, finite-presentation, or finite-rank-kernel hypothesis in this proposition. Its proof explicitly permits an infinitely generated free kernel. Theorem 3.4 states that torsion-free virtually surface groups are surface groups. The definition in the introduction explicitly includes the torus and Klein bottle.
2. [Linton, arXiv:2510.10178v2](https://arxiv.org/html/2510.10178v2), Corollary 1.5, asserts that a hyperbolic free-by-cyclic group is virtually compact special. The introductory convention explicitly permits free kernels of infinite rank. Corollary 1.4 supplies the quasiconvex embedding into a hyperbolic mapping torus with finite-rank free kernel; it is an embedding, not an operation imposing additional relations. Thus the proposed proof does not make the common invalid finite-rank substitution.
3. [Wilton, arXiv:2406.02121v3](https://arxiv.org/html/2406.02121v3), Theorem A, applies to a hyperbolic group that is the fundamental group of a compact nonpositively curved cube complex. Unless the group is free or surface, its conclusion gives a one-ended quasiconvex subgroup of infinite index. A compact special finite-index subgroup has exactly the required cubical classifying space. Wilton's Question 0.1 also restates the full unresolved IF question, confirming the distinction between the restricted argument and the original target.

The web retrievals identified the versions as GKL v2 (9 August 2022), Linton v2 (22 April 2026), and Wilton v3 (22 January 2026). A provenance manifest accompanies this review.

## Independent reconstruction and falsification attempts

Let G be infinite, finitely generated, virtually indicable, and IF.

* A nontrivial finite cyclic subgroup would have infinite index in G and would fail to be free. Thus G is torsion-free. This step uses the infinitude of G, which is among the hypotheses.
* IF passes to any subgroup H: an infinite-index subgroup L of H is also of infinite index in G. In particular it passes to the chosen finite-index indicable subgroup H and to every further finite-index subgroup. Schreier's theorem ensures that H is finitely generated.
* The kernel K of a surjection H to Z has infinite index and therefore is free. Choosing a lift of 1 in Z splits the extension, giving H = K semidirect Z. This is valid whether K has finite or infinite rank; no finiteness assumption is introduced here.
* Apply GKL Proposition 3.5 to H. If H is a surface group, use the surface finite-extension argument below. Otherwise H is hyperbolic, and Linton gives a compact special finite-index subgroup S. Hyperbolicity and IF persist on S. If S were neither free nor surface, Wilton would produce an infinite-index quasiconvex subgroup L of S that is one-ended. Quasiconvexity in a hyperbolic group ensures finite generation. IF makes L free, which contradicts one-endedness: finite-rank free groups have zero, two, or infinitely many ends. In particular the argument does not invoke ends for an infinitely generated free group.
* Therefore G is torsion-free and virtually free or virtually surface. The following checks justify the exact isomorphism conclusion for G, rather than only a virtual conclusion.

### Finite-extension checks

For a virtually free group, the standard tree characterization supplies an action on a tree with finite stabilizers. In the torsion-free case all stabilizers are trivial, so the group acts freely on a tree and is free. This also covers the virtually cyclic case: an infinite torsion-free virtually cyclic group is Z.

For a negative-Euler-characteristic surface subgroup, take an orientable surface subgroup N normal and of finite index by taking the core of an orientable finite-index subgroup. Its center is trivial. The centralizer C_G(N) injects into the finite quotient G/N and is therefore finite; torsion-freeness makes it trivial. Hence G/N embeds faithfully in Out(N). Nielsen realization realizes this finite outer action on the closed surface. Since a centerless kernel has its extension determined by the outer action, G is the resulting compact hyperbolic orbifold group. Torsion-freeness excludes cone-point and mirror stabilizers, leaving a closed surface group. This is the content of the cited GKL Theorem 3.4; the reconstruction checks that no ineffective finite kernel is being ignored.

For the torus or Klein bottle, G is torsion-free and virtually Z^2. Take a normal finite-index Z^2 subgroup A. The centralizer C = C_G(A) contains A centrally and with finite index. Schur's theorem makes the derived subgroup of C finite, so torsion-freeness forces C to be abelian; it is then Z^2. The finite quotient G/C acts faithfully on C. Over R^2 the finite quotient has vanishing positive-degree cohomology, so the extension admits the usual faithful affine realization. The translation lattice C makes this action properly discontinuous and cocompact; averaging an inner product makes it isometric. A point stabilizer is finite and is therefore trivial. The quotient is a closed flat surface, hence a torus or Klein bottle. Thus the flat cases do not require negative curvature or the centerless-kernel argument.

### FAb and L2 scope checks

For every finite-index H in a finitely generated group, H is finitely generated. Its abelianization is therefore a finitely generated abelian group. That abelianization is infinite exactly when it has a nonzero free abelian summand, equivalently when H surjects onto Z. Thus failure of FAb is exactly virtual indicability in the stated setting. There is no converse inference from finite abelianization of G alone.

The final L2 remark is correctly conditional on an applicable approximation theorem and a residual normal chain. Since FAb makes every normalized rational first Betti number zero, such an approximation gives zero first L2-Betti number when its hypotheses hold. It does not imply freeness or existence of a surface subgroup. Closed surfaces with negative Euler characteristic have positive first L2-Betti number; the torus and Klein bottle have zero, as allowed by the wording. No claim of residual finiteness for arbitrary IF groups, or an unconditional approximation theorem for arbitrary finitely generated groups, is used.

## Boundary cases and remaining gap

The audit tested the trivial free kernel, infinite cyclic group, finite-rank and infinite-rank free kernels, orientable and nonorientable hyperbolic surfaces, torus, Klein bottle, and torsion in finite extensions. None gives a counterexample to the proposition. Finite groups are excluded at the start, as required.

Finite presentation was never used in the restricted proof. It is used only in defining the remaining original problem class and in the parent note's separate coherence observation. That coherence observation is valid: finitely generated infinite-index subgroups are finite-rank free, while finite-index subgroups of a finitely presented group are finitely presented.

**Exact full-scope obstruction:** the argument offers no mechanism forcing a finitely presented FAb IF group to have an indicable finite-index subgroup, to be cubulated, or to contain a surface subgroup. Assuming any of these missing properties would transfer the main difficulty into an unsupported assertion. No result should be promoted to a complete solution or publication on the basis of this review.
