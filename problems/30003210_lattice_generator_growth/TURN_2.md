# Turn 2: bounded-degree arithmetic models and compact-kernel descent

AI-assisted proof attempt; independent review pending. Original unresolved. Turn-one bytes remain frozen.

## Compactness survives commensurability
Let k be a number field, v a place over3, and L≤GL_N(k) a group commensurable with a subgroup of GL_N(O_k). Here the precise condition needed is that L has a finite-index subgroup L_0 contained in GL_N(O_k); no bound on [L:L_0] is assumed. In GL_N(k_v), the closure of L_0 is compact. A finite coset decomposition L=union_j g_j L_0 makes the closure of L compact as well. Consequently turn1 supplies a torsion-free normal H≤L with index at most3^([k_v:Q_3]N²)≤3^([k:Q]N²). The bound does not contain the possibly enormous commensurability index.

This also covers groups that preserve a different integral lattice after a k-linear conjugation. It does not cover an arbitrary finitely generated subgroup of GL_N(k): unbounded p-adic powers may prevent compactness.

## Compact-kernel descent
Suppose L is discrete in a locally compact group E, π:E→G is a continuous homomorphism with compact kernel, and Γ=π(L) is a lattice in the fixed source group G. Let H≤L be torsion-free of finite index. Then π|H is injective and π(H) is torsion-free. Indeed the intersection L∩kerπ is finite, because it is a discrete closed subgroup of a compact group. If π(h) has finite order, some h^a lies in this finite intersection; hence h has finite order and is1. Also [Γ:π(H)]≤[L:H]. No assumption that the projection preserves torsion-freeness for arbitrary nondiscrete groups is made.

## Family theorem
Consider Γ_i in fixed G with volumes tending to infinity. Suppose each is π_i(L_i), with compact-kernel discrete arithmetic models as above, each L_i having a faithful k_i-linear representation of dimension at most N and a finite-index subgroup preserving an O_(k_i)-lattice. If [k_i:Q]≤D uniformly, then Γ_i satisfies the source conclusion, with torsion-free subgroup index at most3^(DN²).

Proof: choose any place of k_i over3, apply the compactness lemma and turn1, descend the subgroup, and apply the bounded-cover/FMW argument. The real compact factors and the sizes of finite kernels need not be bounded separately. The result is uniform over all the stated integral models, not merely over finite-index subgroups of a single lattice.

Gelander–Slutsky §2 uses precisely discrete arithmetic lifts and compact-kernel descent, and its unconditional proof uses restriction of scalars and a third congruence subgroup. Those ingredients and the bounded-degree consequence are credited. The contribution of this turn is an explicit hypothesis-by-hypothesis derivation with a conservative matrix-size bound, not a claim of new arithmetic structure or priority.

## The attempted generalization and its gap
Higher-rank arithmeticity does not bound [k_i:Q] across all cocompact lattices. Even when a faithful algebraic representation has uniformly bounded dimension N, the estimate becomes exponential in field degree. It cannot be replaced by a bound independent of degree merely because the real ambient group is fixed. Thus this turn removes the commensurability-index obstacle under the displayed model assumptions, but not the varying-degree obstacle in the original conjecture.
