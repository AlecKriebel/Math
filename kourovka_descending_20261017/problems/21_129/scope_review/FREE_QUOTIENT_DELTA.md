# Adversarial delta: the free-quotient filter

**Verdict: pass.** The proof in `../root_structure/FREE_QUOTIENT_FILTER.md` establishes, for every T in {F4,H4,D6,E6,D7,E7,D8,E8}, an epimorphism

\[
Q_T=P_T/Z(P_T)\twoheadrightarrow F_2
\]

and exact index-m subgroups \(V_m\le Q_T\) with \(b_1(V_m;\mathbb Q)\ge m+1\), for all positive integers m. This is a check of an elementary derived filter, not a novelty or full-solution claim. A fresh independent topology auditor also found no failure in these steps.

The reflection-arrangement identification of the pure group is the established input recalled in [Cumplido–Paris §3](https://ems.press/content/serial-article-files/39000?nt=1), printed pp508–509. The remaining deductions can be checked directly as follows.

1. **The three hyperplanes exist.** F4 has adjacent diagram labels 3,4,3; H4 has 5,3,3; and the listed D/E diagrams have edges labelled3. Two simple reflections joined by a 3-edge generate the rank-two dihedral reflection subgroup I2(3)=A2. Its two simple hyperplanes and their reflected third hyperplane are distinct ambient reflecting hyperplanes. Their normal forms span a two-dimensional subspace. A linear coordinate change takes the three forms to nonzero scalar multiples of x,y,x−y; arbitrary three distinct lines through the origin in dimension two have this form after rescaling coordinates.

2. **The complement inclusion is surjective on fundamental groups.** Put \(X=M(\mathcal B)\), and choose a basepoint b in the full complement \(M(\mathcal A_T)\). For each extra hyperplane H, the set \(H\cap X\) is a closed, embedded smooth real codimension-two submanifold of X, although it can be noncompact. Start with a smooth based loop constant in a small parameter interval about b. Smooth transversality relative to that interval makes it transverse to every one of the finitely many \(H\cap X\). The preimage of each has expected dimension 1−2<0, hence is empty. The perturbation and homotopy stay in X: the original loop is compact and X is open, so the perturbation may be chosen sufficiently small. Thus every class in \(\pi_1(X,b)\) has a representative in the full complement. This proves the required epimorphism. It does not assert a retraction or a splitting of that epimorphism.

3. **The target and center are correct.** On \(x\ne0\), the coordinates \((x,t=y/x)\) identify the three-line complement with \(\mathbb C^*\times(\mathbb C\setminus\{0,1\})\), with the remaining affine coordinates unchanged. Its fundamental group is \(\mathbb Z\times F_2\). Projection gives an epimorphism from P_T to F2. Surjectivity is crucial: every image of a central element then commutes with every element of F2, so it is trivial. The epimorphism therefore descends to Q_T.

4. **The exact indices and lower bounds follow.** The kernel \(U_m\) of the displayed map \(F_2\to\mathbb Z/m\) has index m, including m=1. Nielsen–Schreier gives rank m+1. Its inverse image under the epimorphism \(Q_T\to F_2\) has exactly index m and still surjects onto U_m. The induced map on rational abelianizations is surjective, giving the bound. The inverse image in P_T has the same index m in P_T; it has index \([A_T:P_T]m\) in A_T, sufficient for infinite virtual first Betti number of A_T. The argument does not claim an index-m subgroup of A_T for every m.

All eight types share the conclusion, so the qualitative property cannot separate a residual pair. Nothing here claims quasi-isometry invariance of virtual first Betti number, a residual chain with trivial intersection, or positive first L2-Betti number. For perspective, even the centerless group \(F_2\times F_2\) surjects onto F2 and has infinite virtual first Betti number, while its first L2-Betti number vanishes by the product formula. The filter correctly avoids that unsupported inference.

No mathematical repair is required. One optional wording refinement is to replace the final phrase “exact missing step” with the four residual implications themselves: a direct positive commensurability theorem would also settle a pair, without requiring a new large-scale invariant or a shared geometric model.
