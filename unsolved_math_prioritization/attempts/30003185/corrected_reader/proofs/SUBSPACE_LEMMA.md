**Integrated reader status.** Independent supporting subspace proof. The integrated theorem uses the simpler e≥384 cutoff and stronger exponent from the class-generation proof. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# An independent subspace-action estimate for class-random strong involutions

13 October 2026. This is an authored supporting lemma. It is independent of the inaccessible Praeger–Seress 2011 article.

## Statement

Let q be odd, let V be a nondegenerate symplectic or quadratic space of dimension e, and put J=Sp(V) or Ω(V), respectively. Assume e≥192. For any prescribed sequence of 192 J-conjugacy classes of natural involutions whose two eigenspaces have dimensions in [e/3,2e/3], independently choose one uniform element from each class. Then the probability that all 192 elements preserve a common nonzero proper subspace is at most

13 q^(−7e) < (1/2)q^(−e).

For the combined proof one can use the author's simpler cutoff e≥384 and the correspondingly stronger estimate 13q^(−11e). Either bound is sufficient. No assertion is made for arbitrary projective involutions without natural order-two lifts.

## 1. Count normalization

For the full isometry group D(W), write its order as q raised to its usual quadratic dimension exponent times a bounded product correction. The already-audited order formulas give

- Sp: |Sp_d(q)|=q^(d(d+1)/2) ψ_d, with 7/8≤ψ_d≤1 (including d=0).
- O: |O(W)|=q^(d(d−1)/2) η(W), with 7/6≤η(W)≤8/3 for d>0; |O(0)|=1.

Consequently, when 0<k<e, the number N(V,k,τ) of nondegenerate k-subspaces of any fixed occurring isometry type τ is bounded by

(21/128)q^(k(e−k)) ≤ N(V,k,τ) ≤ 2q^(k(e−k)).        (1)

In Sp there is just one permitted type for even k; the sharper bounds 7/8 and 64/49 apply. In O there are at most two types. Zero-dimensional and whole-space counts equal one, so the upper bound 2q^(k(e−k)) remains valid for these boundary cases.

The full O group is transitive on subspaces of a fixed nondegenerate isometry type, by extending an isometry using Witt's theorem. Its stabilizer is O(W)×O(W⊥), so (1) follows directly from the order quotient. The analogous statement holds in Sp.

## 2. Totally singular counts, including maximal split spaces

Let T(V,k) count all totally singular k-subspaces, with T(V,0)=1 and T(V,k)=0 if none exist. Set

Fσ(e,k)=ke−(3k²+σk)/2,

where σ=−1 for Sp and σ=+1 for O. Whenever T(V,k)>0,

(1/2)q^Fσ(e,k) ≤ T(V,k) ≤ 8q^Fσ(e,k).              (2)

Here is a direct derivation, including uniform constants. Build an ordered singular basis one vector at a time. After choosing an i-dimensional totally singular space, the quotient W_i⊥/W_i has dimension e−2i, and each nonzero singular vector in that quotient has q^i lifts. Divide the resulting ordered-basis count by

|ordered bases of F_q^k| = q^(k²) ∏_{j=1}^k(1−q^(−j)).

For Sp, every vector is singular and the quotient has q^(e−2i)−1 nonzero vectors. The correction factor in the resulting count is

∏_{i=0}^{k−1}(1−q^(−(e−2i))) / ∏_{j=1}^k(1−q^(−j)).

Its lower bound is 7/8, because the numerator is a subproduct of the even-degree product and ∑_{j≥1}q^(−2j)≤1/8. Its upper bound is 2, because the denominator is strictly greater than 1−∑_{j≥1}q^(−j)≥1/2.

In odd orthogonal dimension d, the number of nonzero singular vectors is q^(d−1)−1. The same even-exponent numerator bound applies. In even orthogonal dimension d=2m with Witt sign ε=±, the number is

(q^(m−1)+ε)(q^m−ε).

After dividing by q^(d−1), the correction is (1+εq^(−(m−1)))(1−εq^(−m)). A totally singular quotient removes hyperbolic planes, so ε remains fixed throughout the product. In minus type every occurring m is at least 2; the product of the factors (1−q^(−(m−1))) is greater than 1/2, and the other factors exceed one. In plus type every paired correction exceeds one. For an upper bound, discard the factors less than one: the product is at most

∏_{j≥0}(1+q^(−j)) < 4.

For example, ∏_{j≥1}(1+q^(−j))≤exp(∑_{j≥1}q^(−j))≤exp(1/2)<2. Division by the denominator correction, greater than 1/2, gives (2). The terminal plus-type factor m=1 is allowed. Thus T includes both families of maximal totally singular subspaces; no family was silently discarded.

## 3. Why full-isometry orbit counts apply to Ω-class samples

Write x=−I_A⊕I_B, with a=dim A, b=dim B. For our strong x, a,b≥e/3≥64. The orthogonal centralizer of x is O(A)×O(B). A nondegenerate finite quadratic space of dimension at least three contains a hyperbolic plane and represents every nonzero field element. Reflections inside A therefore realize both determinant/spinor pairs (−1,square) and (−1,nonsquare). They generate O(V)/Ω(V). Hence

O(V)=Ω(V) C_{O(V)}(x), and x^{O(V)}=x^{Ω(V)}.

The equality is one of actual conjugacy classes. A uniform Ω-class element is therefore uniform in this full O-class. For a fixed subspace W in any full-O orbit X, the probability that a uniform class element stabilizes W is |Fix_X(x)|/|X|. This remains true if X splits into two or more Ω-orbits. We do not divide by the smaller Ω-orbit size or assume that no orbit splitting occurs. For Sp the full group is J already.

## 4. Fixed nondegenerate subspaces

Because q is odd, an x-invariant subspace decomposes as W=(W∩A)⊕(W∩B). If W is nondegenerate, both summands are nondegenerate and orthogonal. Put i=dim(W∩A), j=dim(W∩B), so i+j=k.

For each i, each summand has at most two possible orthogonal isometry types, and (1) bounds each type count above by 2q raised to its dimension exponent. Thus the numerator for any fixed target type is at most

16(k+1) max_{i+j=k} q^(i(a−i)+j(b−j)).

The denominator is at least (21/128)q^(k(e−k)). The exponent loss is

Δ_nd = k(e−k)−i(a−i)−j(b−j) = ib+ja−2ij.

For k≤e/2, a,b≥e/3 and ij≤k²/4 give

Δ_nd ≥ ek/3−k²/2 ≥ ek/12.

Therefore, for every specified nondegenerate W with 1≤k≤e/2,

P(x_class stabilizes W) ≤ (2048/21)(k+1)q^(−ek/12)
                       < 128(k+1)q^(−ek/12).         (3)

Summing all component isometry types only overcounts, so no determinant/discriminant compatibility hypothesis is needed in this upper bound.

## 5. Fixed totally singular subspaces

If W is totally singular and x-invariant, W∩A and W∩B are totally singular. For i+j=k, there are exactly T(A,i)T(B,j) such decompositions. Only i≤a/2 and j≤b/2 can occur. By (2), the numerator is at most

64(k+1) max_{i+j=k} q^(Fσ(a,i)+Fσ(b,j)).

The exponent loss from the denominator is

Δ_ts = Fσ(e,k)−Fσ(a,i)−Fσ(b,j) = ib+ja−3ij.

The linear σ terms cancel. The Witt-index restrictions give ib+ja≥4ij, so

Δ_ts ≥ (ib+ja)/4 ≥ ek/12.

Using the denominator lower bound in (2) proves, for every specified totally singular k-space,

P(x_class stabilizes W) ≤128(k+1)q^(−ek/12).          (4)

## 6. The union bound and fixed class sequence

For each k≤e/2, all nondegenerate spaces of all types number at most 4q^(k(e−k))≤4q^(ek), and all totally singular spaces number at most 8q^Fσ(e,k)≤8q^(ek). Thus at most 12q^(ek) spaces need consideration.

For k≥1, k+1≤2^k and 128≤128^k, giving

128(k+1)≤256^k≤3^(8k)≤q^(ek/24) if e≥192.

Equations (3)–(4) therefore bound each single-class stabilization probability by q^(−ek/24). This bound holds separately for every prescribed strong class, so independence of the 192 representatives gives a common-stabilization probability at most q^(−8ek) for any fixed W. A union bound yields

P(common relevant subspace) ≤12 ∑_{k=1}^{⌊e/2⌋} q^(−7ek)
                           <13q^(−7e)
                           <(1/2)q^(−e).

The last two inequalities follow from q≥3 and e≥1: 12/(1−3^(−7))<13 and 13·3^(−6)<1/2.

Finally, if a group of isometries preserves a degenerate nonzero proper W, it preserves the nonzero totally singular radical W∩W⊥. If W is nondegenerate, replace it by W⊥ when necessary to arrange dim W≤e/2. Thus the union indeed covers all reducible subgroups.

## 7. Reproducible finite safeguards

The finite subspace reconstruction enumerates actual RREF subspaces for symplectic and both orthogonal signs over F_3, including dimensions 4,5,6, and both orthogonal signs in dimension 4 over F_5. It checks the exact singular-subspace product formulas and the invariant singular/nondegenerate decomposition convolution. It separately checks 2,255,650 integer exponent instances through e=120 and the exact rational constants used in the geometric tail. No assertion statements or random sampling are used. These controls are safeguards; Sections 1–6 prove the uniform theorem.
