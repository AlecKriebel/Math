# Turn 5: torsion normal generators, homology, and the missing rank step

AI-assisted proof attempt; independent review pending. Original unresolved; this is the fifth and final author turn.

## A uniform finite-stabilizer generator bound
Fix a faithful complex linear representation G→GL_N(C). Jordan's classical theorem gives an abelian normal subgroup A of every finite F≤G with [F:A]≤J(N). Simultaneous diagonalization embeds A in a product of N finite cyclic groups, hence d(A)≤N. Lifting at most floor(log_2 J(N)) generators of F/A gives d(F)≤C_N=N+floor(log_2 J(N)). This bound is independent of |F|. Primary exposition: Breuillard, Model Theory 2(2)(2023),429–447, Theorem1.1, https://msp.org/mt/2023/2-2/mt-v2-n2-p12-p.pdf . Only Jordan's stated theorem is used, not a sharp value of J(N).

Let f(Γ) be the number of conjugacy classes of maximal finite subgroups. Samet, https://arxiv.org/abs/1209.2484 , Theorems1.1–1.2, proves finiteness and f(Γ_i)=o(v_i) for pairwise nonconjugate irreducible lattices in higher-rank semisimple groups with property(T). A fixed higher-rank simple G satisfies these hypotheses. This also applies asymptotically to arbitrary sequences with v_i→infinity: a violating subsequence can be chosen pairwise nonconjugate, since a conjugacy class has one fixed covolume.

Let T(Γ) be the normal closure of all finite-order elements. Choose one representative F_j of each maximal finite subgroup and at most C_N generators for each. Their union normally generates T(Γ). Every finite subgroup is contained in a maximal finite subgroup: Samet's finiteness of conjugacy classes of finite subgroups bounds their possible orders, so ascending finite-subgroup chains terminate. Therefore T(Γ_i) has a normal generating set of size at most C_N f(Γ_i)=o(v_i).

## Exact first-homology consequence
Put Q_i=Γ_i/T(Γ_i). For every prime p there is a surjection H_1(Γ_i;F_p)→H_1(Q_i;F_p) whose kernel has dimension at most C_N f(Γ_i). Indeed it is the image of T(Γ_i) in Γ_i/[Γ_i,Γ_i]Γ_i^p. Conjugation disappears in this abelian quotient, so the images of the chosen normal generators span the kernel. Thus
0≤dim H_1(Γ_i;F_p)−dim H_1(Q_i;F_p)≤C_N f(Γ_i)=o(v_i),
uniformly in p. Over Q the difference is zero, since every selected generator has finite order. This is a precise consequence of Samet and Jordan; it does not prove that either mod-p dimension itself is sublinear.

## Why this does not prove the generator conjecture
Normal generators do not become ordinary generators after lifting generators of Q. The tempting estimate d(Γ)≤d(Q)+number_of_normal_generators(T) is false without extra structure. An explicit abstract witness is P_r=A_5^r. Let x be a3-cycle and z=(x,...,x), of order3. Its normal closure is all P_r: commuting z with elements supported in coordinate j produces a nonidentity element supported only there; simplicity of A_5 and conjugation then generate the entire j-th factor. Nevertheless d(P_r) is unbounded. If k elements generated P_r with r>60^k, two coordinate columns of these k tuples would agree by pigeonhole. Every word would then agree in those coordinates, impossible in the full product. So d(P_r)≥log_60 r, while the indicated normal generating set has size1 and Q is trivial.

For completeness simplicity of A_5 follows from its conjugacy-class sizes1,12,12,15,20: no proper sum containing1 is a divisor of60 except1 itself. The checker independently computes these sizes and the normal closure of a3-cycle.

This finite-product family is explicitly NOT a lattice counterexample in fixed G: its faithful representation dimension grows, and it does not satisfy the source's fixed ambient Lie-group hypotheses. It isolates the invalid group-theoretic implication only. Additional geometric control on how stabilizers and quotient generators assemble, rather than merely their normal generation, remains needed. Neither Samet's sublinear class count nor the proved homology estimate closes that gap.

## Final boundary
The five turns establish bounded local-linear and bounded-degree arithmetic-model families, a non-effective growing-cover window, exact quantitative thresholds, a reduction to maximal lattices, and the homological torsion comparison. The original arbitrary cocompact torsion-lattice rank conjecture remains unresolved. No sixth author search, new full resolution, or novelty certification is claimed.
