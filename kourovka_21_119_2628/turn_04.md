# Turn 4/5: Thompson's group F and all its finite-index subgroups

## Attempt

Thompson's group F passes the F_∞ and infinite-cohomological-dimension tests. Moreover, the established theorem of Bieri–Geoghegan–Kochloukova says F contains subgroups with every finite homotopical finiteness length. Try to upgrade those subgroups to the virtual algebraic fibers demanded by the question. The computation below rules out that upgrade for F itself and its entire commensurability class.

The input facts are classical and are explicitly recalled or proved in Bieri–Geoghegan–Kochloukova, *The Sigma invariants of Thompson's group F*, Groups Geom. Dyn. 4 (2010), 263–273; https://arxiv.org/abs/0807.5138 . We use that F/F′≅Z², the derived group F′ is infinite simple, and their Theorem A computes all BNSR invariants of F. This attempt derives the virtual-kernel consequence rather than claiming to rediscover their theorem.

## 1. Every virtual character extends rationally

Let H≤F have finite index. The action of F on its finite coset set F/H gives a homomorphism F→Sym(F/H). Restricted to the infinite simple group F′, its kernel is either trivial or all of F′. Triviality would embed an infinite group in a finite group, which is impossible. Hence F′ lies in the kernel, and in particular F′≤H.

An infinite nonabelian simple group is perfect: its derived subgroup is nontrivial and normal, and therefore is the whole group. Consequently

F′=[F′,F′]≤[H,H]≤[F,F]=F′.

Thus H/[H,H]=H/F′ is a finite-index subgroup of F/F′≅Z². Any integral character χ:H→Z is a linear map on this full-rank lattice and extends uniquely to a rational linear functional on Q². Multiplying the extension by a positive integer D clears denominators and gives an integral character χ̃:F→Z with χ̃|_H=Dχ.

It follows that ker χ=H∩ker χ̃. This has finite index in ker χ̃, so the two kernels have the same F_n and FP_n properties. Therefore passing to finite-index subgroups of F introduces no new finiteness lengths of character kernels.

## 2. Read the exact kernel trichotomy

Let χ_0 and χ_1 be the integer logarithms of the endpoint slopes at 0 and 1, using the sign convention in the cited paper. Every nonzero rational character has the form aχ_0+bχ_1 with (a,b)≠(0,0).

Theorem A states that Σ¹(F) is the character circle with [χ_0] and [χ_1] removed; for every m≥2, the complement of Σ^m(F) is the closed short arc consisting of their nonnegative linear combinations. The BNSR kernel criterion tests both antipodal rays. It gives:

- If ab=0, one antipodal ray is [χ_0] or [χ_1]. The kernel is not finitely generated, so its exact F-length is 0.
- If ab>0, neither ray is an endpoint, so both lie in Σ¹(F); one ray has both coefficients positive and lies outside Σ²(F). The kernel is F_1 and not F_2. In fact the same source gives the stronger failure of FP_2.
- If ab<0, both antipodal rays lie outside that closed short arc. Both lie in Σ^m(F) for every m, so the kernel is F_∞.

All cases occur: χ_0, χ_0+χ_1, and χ_0−χ_1 are examples, respectively. Multiplying by a nonzero rational scalar does not change a kernel. Combined with the extension argument, this proves that the finite virtual fiber spectrum of F is exactly {0,1}. In particular, F has no virtual character kernel of type F_2 but not F_3, let alone all higher lengths.

## 3. Explain the misleading positive construction

Theorem B in the same paper constructs subgroups of every finite F-length using direct powers F^r embedded in F on disjoint subintervals and suitable characters of those powers. Those ambient embedded products are not finite-index substitutes for F.

Indeed every finite-index subgroup H≤F has abelianization of rank exactly two by section 1. But (F^r)_ab≅Z^{2r}; for r≥2, F^r cannot be isomorphic to a finite-index subgroup of F. In the standard interval-supported embedding there is also a direct geometric obstruction: the product fixes the partition points, whereas F′ contains compactly supported elements that move them. It therefore does not contain F′ and cannot have finite index.

So an F_n but not F_{n+1} subgroup inside F is insufficient. The problem requires it to be a character kernel in a finite-index subgroup, a much stronger normality and quotient condition.

## Outcome and exact gap

Thompson F and all groups commensurable with it are excluded, despite its unbounded subgroup finiteness spectrum and infinite cohomological dimension. The attempted shortcut through its embedded direct powers fails exactly at the finite-index requirement. The remaining search needs a different infinite-dimensional F_∞ group with genuinely nonstabilizing virtual character-kernel behavior. The final attempt tests a permutational-wreath construction designed to manufacture that behavior.
