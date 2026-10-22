# Turn 2/5: complete finite segments using products of free groups

## Attempt

Try to realize all requested finiteness lengths by varying the character on a product of nonabelian free groups. This produces every finite initial segment, but a classification below proves that a fixed finite product cannot solve the problem, even after taking arbitrary finite-index subgroups.

## 1. A finite initial segment in one ambient group

Fix M≥2 and let P_M=F(a_1,b_1)×⋯×F(a_M,b_M). For 1≤s≤M define χ_s:P_M→Z by sending a_i and b_i to 1 for i≤s, and all generators in the other factors to 0. Then

ker χ_s = B_s × F_2^{M-s},

where B_s is the classical Bieri–Stallings kernel of the all-ones character on F_2^s. The established Bestvina–Brady theorem shows B_s is F_{s-1}: its defining flag complex is the join of s two-point sets, a sphere S^{s-1}, which is (s-2)-connected. For s=1, F_0 is automatic. A product with an F_∞ group preserves F_{s-1}.

Here is a direct certificate of the negative finiteness statement. The product X of s two-petal roses is a finite K(F_2^s,1). The infinite cyclic cover X_χ is a K(B_s,1). Put R=Z[t,t^{-1}], the deck-transformation ring. Its cellular chain complex is the tensor product over R of s two-term complexes

R a_i ⊕ R b_i → R v_i,

where ∂a_i=∂b_i=(t−1)v_i. Therefore the top chain

z=(a_1−b_1)⊗⋯⊗(a_s−b_s)

is a cycle. There are no cells in degree s+1, and z has a coefficient equal to 1 in the free R-module C_s. Thus Rz injects into H_s(B_s;Z). Its underlying abelian group is free on infinitely many powers t^j z. A finitely generated abelian group cannot contain such a subgroup, so H_s(B_s;Z) is not finitely generated. In particular B_s is not FP_s, hence not F_s.

The inclusion B_s→B_s×F_2^{M-s} splits by projection, so it injects H_s(B_s;Z) as a direct summand of the product's H_s. Consequently ker χ_s is F_{s-1} and not FP_s. Choosing s=n+1 gives, in the single group P_M, every requested n from 1 through M−1. These are credited applications of the Bieri–Stallings/Bestvina–Brady construction, not a new resolution.

## 2. Arbitrary finite-index subgroups do not evade the bound

Let H≤P_M have finite index, and let χ:H→Z be nonzero. Set U_i=H∩F(a_i,b_i). Each U_i has finite index in its factor and is a nonabelian finitely generated free group. The commuting product U=∏U_i is contained in H and has finite index in P_M, hence in H. The restriction χ|_U is nonzero. It splits as the sum of its restrictions χ_i on the factors.

Let s be the number of nonzero χ_i. Then 1≤s≤M. The inactive factors lie in the kernel and split off. To put the active characters in a standard form, write χ_i(U_i)=d_i Z, d_i>0, and choose a positive common multiple D of all d_i. Replace each active U_i by V_i=χ_i^{-1}(DZ), a finite-index free subgroup. Then ψ_i=χ_i/D:V_i→Z is primitive. A primitive integer character on a finite-rank free group has a free basis in which its values are (1,0,…,0): this follows from elementary Nielsen moves and the Euclidean algorithm. Replacing each remaining basis element b by a b, where ψ_i(a)=1, makes all basis values equal to 1 while preserving the free-basis property.

Thus the kernel of χ on the finite-index product V of these groups is the standard all-ones Bieri–Stallings kernel on s nonabelian free factors, times the inactive free factors. The defining flag complex is now the join of s finite discrete sets of cardinalities r_i≥2. That join is (s−2)-connected and has nonzero reduced homology in degree s−1. Bestvina–Brady gives F_{s-1}. The preceding chain calculation works with any two chosen basis elements in each factor and shows H_s has an R-free submodule, so this kernel is not FP_s.

Finally ker(χ|_V) has finite index in ker χ. Finiteness properties F_m and FP_m are invariant under finite index. Therefore ker χ itself is F_{s-1}, not FP_s.

## 3. Exact conclusion for this construction class

The virtual fiber spectrum of P_M is exactly {0,1,…,M−1}; each value is attained and the classification excludes all others. In particular, increasing subgroup index does not imitate adding a new direct-product factor. The direct-limit idea P_1<P_2<⋯ gives a restricted direct product, but this group is not finitely generated, contradicting the F_∞ necessity from turn 1. An unrestricted countable product also has a quotient ∏Z and is not finitely generated.

## Outcome and gap

Every finite initial segment is achievable in one group, with explicit integral homology certificates. The same method cannot supply an unbounded spectrum in a fixed finite product or its commensurability class. The remaining task is an F_∞ construction with genuinely unbounded complexity, rather than a disguised increase in the number of ambient factors.
