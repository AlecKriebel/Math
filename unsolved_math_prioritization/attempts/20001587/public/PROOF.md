# Amenable clopen corners: exact reductions and the remaining gap

**Problem 20001587 / AIM-GEOMETRIC_GROUP_THEORY-0096. Partial results only.**

The intended question in AIM *Amenability of discrete groups*, §2.1, is whether a minimal, nonamenable topological full group on a Cantor space has nonamenable restriction to every nonempty clopen subset. This packet does not settle that question. Its main exact reformulation is Theorem 6: the universal question is equivalent to preservation of amenability under a two-layer amplification. The word “amplification” below means adding finitely many discrete layers, not merely taking the topological full closure.

## 1. Conventions and exact target

A Cantor space is a nonempty compact metrizable, zero-dimensional space with no isolated points. All groups have the **discrete** topology. For a subgroup G of Homeo(X), write [[G]] for the homeomorphisms locally equal to elements of G. Compactness allows a finite clopen partition of local definitions. Assume throughout Sections 2–6 that

- G=[[G]];
- every G-orbit is dense in X;
- U is a nonempty clopen subset of X.

Write G_U={g in G: g is the identity on X\U}, and identify it with its faithful restriction H to U. A homeomorphism fixing X\U necessarily preserves U. The target is

                 H amenable  ==>  G amenable.                    (Q)

The source does not explicitly exclude U=empty; then G_U is trivial. We record that degenerate case without treating it as a resolution of the intended question. U=X is tautological. “Full” here means topological full closure, not the usually larger group of all orbit-preserving homeomorphisms.

A clopen partial G-map is a homeomorphism between clopen subsets, locally equal to elements of G. Its source and range may overlap. No global extension of an arbitrary such map is assumed.

We use elementary permanence of amenability under subgroups, quotients, finite products, extensions and directed unions, and the invariant-mean definition. References and complete relevant proof locations appear in SOURCE_GATE.md. The proofs below also supply the particular constructions on which the reductions depend.

## 2. Germ realization and local transport

**Lemma 1 (local realization).** If x,gx are in U and g is in G, there are a clopen neighborhood V of x in U and h in G_U such that h|V=g|V. Consequently, every clopen partial G-map with source and range in U is locally a partial H-map. The H-action on U is minimal, and H=[[H]].

**Proof.** If gx differs from x, shrink V so that V and gV are disjoint clopen subsets of U. The map equal to g on V, g^{-1} on gV, and the identity elsewhere is a homeomorphism in G_U, by fullness.

If gx=x, minimality and the absence of isolated points give k in G with kx in U\{x}. Shrink V around x so that W=kV is contained in U and disjoint from V union gV. Let s1 swap V and W by k and k^{-1}. Let s2 swap W and gV by gk^{-1} and kg^{-1}. Both maps belong to G_U, and s2s1 agrees with g on V. This includes nontrivial germs fixing x.

Apply this at each point of the source of a partial G-map, first on a neighborhood where that map is one element of G. Compactness and a finite clopen refinement give finitely many H-labels. For minimality of H, given x in U and nonempty relatively open O in U, choose g with gx in O and apply the lemma. If a homeomorphism of U is locally H, extend it by the identity on X\U; the extension is locally G, hence is in G_U. Thus H is full. ∎

This lemma is a weaker version, with an elementary swap proof, of Scarparo's Lemma 3.3, which realizes the germ inside the alternating full group. No novelty is claimed for germ realization.

**Lemma 2 (finite local transport).** There is a finite clopen partition P={A_1,...,A_m} of X and elements t_i in G with t_i A_i contained in U. One can choose A_1=U and t_1=1, omitting empty atoms. For each atom, conjugation by t_i embeds G_{A_i} into G_U. Thus amenability of G_U gives a clopen neighborhood basis at every point consisting of sets V with amenable G_V.

**Proof.** Minimality gives, for each x outside U, an element t with tx in U and a clopen neighborhood V of x in X\U with tV contained in U. Compactness of X\U gives a finite cover of that set. Disjointify it by successively subtracting earlier members, and adjoin U. Conjugation carries G_{A_i} into G_{t_iA_i}, a subgroup of G_U. The same construction with arbitrarily small neighborhoods, or merely taking clopen subsets of the cover members, proves the basis assertion. ∎

In particular, if a clopen V can be carried into U by one clopen partial G-map θ, then G_V embeds in G_U: conjugate its restriction by θ and extend by the identity outside θ(V). Fullness and the local definition of θ justify that extension. A nonamenable corner therefore cannot admit such a compression into an amenable one.

## 3. The invariant probability measure is forced

**Proposition 3 (measure transfer).** If G_U is amenable, X has a nonatomic, full-support G-invariant Borel probability measure. More precisely, for any H-invariant probability ν on U there is a unique finite G-invariant measure λ with λ|U=ν. For the partition in Lemma 2,

       λ(E) = sum_i ν(t_i(E intersection A_i)),
       1 <= λ(X) <= m,       μ=λ/λ(X),       μ(U)>=1/m.             (1)

Normalization of restriction is a bijection between invariant probabilities on X and invariant probabilities on U. It need not be affine.

**Proof.** An invariant mean on H produces an H-invariant probability on U: fix u in U and average f(hu), for f in C(U), using the mean; the Riesz representation theorem gives ν. By Lemma 1, ν is invariant under all clopen partial G-maps inside U. Indeed, finitely partition the source into sets on which such a map is one H-element, and add the equalities of measures. This equality also holds for Borel subsets of those pieces.

Define λ by (1). It is a finite Borel measure, being a sum of pushforwards of restrictions. The choice A_1=U, t_1=1 gives λ|U=ν. Each summand in λ(X) is at most 1, and the first is 1.

For g in G and Borel E, decompose E into E_ij=E intersection A_i intersection g^{-1}A_j. The map t_j g t_i^{-1} is a clopen partial G-map from t_i(A_i intersection g^{-1}A_j) into U. Its invariance on Borel subsets gives

                  ν(t_i E_ij)=ν(t_j gE_ij).

Summing over i,j proves λ(E)=λ(gE). If another finite invariant measure agrees with ν on U, invariance under t_i forces its values on E intersection A_i, proving uniqueness. Any invariant probability has positive mass on U, because finitely many translates cover X. This proves the normalized-restriction bijection.

The support of μ is nonempty, closed and G-invariant, and hence is X. Every orbit is infinite, so an atom of positive mass would give infinitely many distinct atoms of that same mass. Therefore μ is nonatomic. ∎

The transfer formula and normalized-restriction bijection are established results: compare Scarparo, Proposition 3.1 and its complete proof. They are included to make the dependence on the single amenable corner explicit. In particular, the existence of an invariant measure is not the missing step in (Q). An invariant probability for a compact action is not an invariant mean on the underlying group.

## 4. What finite clopen gluing actually proves

**Proposition 4 (partition stabilizers and the exact mean gap).** Let P={A_1,...,A_m} be as in Lemma 2 and suppose G_U is amenable. Define

- K_P={g in G: gA_i=A_i for every i};
- L_P={g in G: g permutes the collection P}.

Then

                K_P is isomorphic to product_i G_{A_i},
                K_P is normal in L_P,
                L_P/K_P embeds in Sym(m).                       (2)

Both K_P and L_P are amenable. The following are equivalent:

(a) G is amenable;
(b) the G-action on the orbit G.P of P admits an invariant mean;
(c) L_P is coamenable in G.

**Proof.** If g preserves every A_i, restrict g to A_i and extend by the identity on its complement. Fullness puts the extension in G_{A_i}. These extensions commute and their product is g. Conversely, arbitrary elements of these rigid subgroups combine to an element of K_P; disjoint supports make the product injection faithful. This proves the first assertion. The action on the finite set of atoms gives the remaining assertions of (2). Amenability follows from Lemma 2 and elementary permanence.

The orbit G.P is G/L_P. Amenability of G immediately yields an invariant mean on any G-set, by pushing forward a mean on G. Conversely suppose m is a G-invariant mean on G/L_P and n a left-invariant mean on L_P. For f in the bounded real functions on G, put

                 F_f(gL_P)= n(l -> f(gl)).

This is well defined: replacing g by gl_0 translates the argument of n on the left. It intertwines left translations by G. Consequently f -> m(F_f) is a left-invariant mean on G. This proves (b) implies (a); (c) is the definition of coamenability. ∎

Thus any counterexample to (Q) has amenable stabilizers of these finite partitions but a nonamenable action on their orbit. It cannot be obtained from a subgroup that preserves one such partition. More generally, if every finite subset S of G preserves some finite clopen partition whose atom rigid groups are amenable, then each finitely generated subgroup is amenable and G is amenable.

A finite partition used to specify the generators locally need not be preserved by the generators. Refining it by all translates may require infinitely many atoms. Replacing the unproved invariant-partition assertion by “each generator is piecewise defined” is precisely an invalid finite-gluing argument. Proposition 4 makes no such replacement.

## 5. Embedding into a finite amplification

For any full minimal H acting on a Cantor space Y and positive integer n, define

                Amp_n(H) = [[ H x Sym(n) acting on Y x [n] ]].

Here (h,σ)(y,i)=(hy,σ(i)), and [n]={1,...,n}. Elements of Amp_n(H) are exactly homeomorphisms locally of the form (y,i) -> (hy,j), with h in H and i,j allowed to vary over a finite clopen partition. This equivalence follows because Sym(n) can send any chosen i to any chosen j. The group is full by idempotence of local closure, and minimal because the product action is minimal. Its rigid subgroup on Y x {1} is canonically H: any such restriction is locally H and hence belongs to H, and every h extends by the identity on other layers.

**Proposition 5 (finite-amplification embedding).** For G,U as above, without any amenability assumption, there are m and an injective homomorphism

                         G -> Amp_m(G_U).                        (3)

**Proof.** Identify H with its action on U and choose P,t_i from Lemma 2. Let

             Z = disjoint union_i (t_i A_i) x {i} subset U x [m],
             φ(x)=(t_i x,i) when x belongs to A_i.

The map φ is a homeomorphism from X onto the clopen subset Z. For g in G, conjugate by φ on Z and act identically on its complement. This defines an injective homomorphism into Homeo(U x [m]). On the clopen part corresponding to A_i intersection g^{-1}A_j, its coordinate map is t_j g t_i^{-1}, a partial G-map within U. Lemma 1 says this is locally an H-map. Therefore the homeomorphism lies in Amp_m(H). The formula on the complement is the identity, also an allowed local map. Composition is exact conjugation, rather than a generator-by-generator approximation. ∎

The images t_i A_i need not be disjoint in U. The added layer labels are essential: nothing here constructs an embedding of G into H itself.

## 6. Binary stability is exactly the remaining universal question

**Theorem 6.** These universal assertions are equivalent:

(Q) For every full minimal Cantor group G and nonempty clopen U, amenability of G_U implies amenability of G.

(B) For every amenable full minimal Cantor group H, Amp_2(H) is amenable.

(F) For every amenable full minimal Cantor group H and every n>=1, Amp_n(H) is amenable.

**Proof.** (Q) implies (B): the two-layer full group is minimal and its first-layer rigid subgroup is H. Apply (Q). Clearly (F) implies (B).

To prove (B) implies (F), first observe, after identifying layer pairs with one product layer, that

                     Amp_b(Amp_a(H)) = Amp_{ab}(H).              (4)

Both sides are the homeomorphisms locally mapping (y,i,j) to (hy,i',j'). For the inclusion from left to right, expand each local Amp_a(H)-map into its local H-maps; compactness makes the expansion finite. Conversely an H-map between two prescribed inner-layer indices is locally supplied by an element of H x Sym(a), while the outer index is changed by Sym(b). This proves equality.

Starting from amenable H, (B) applies successively because each amplification is again full and minimal. Equation (4) gives amenability of Amp_{2^k}(H) for every k. If n<=2^k, extension by the identity on the remaining layers embeds Amp_n(H) into Amp_{2^k}(H), proving (F).

Finally (F) implies (Q) by Proposition 5 and subgroup permanence. ∎

Theorem 6 is an exact reformulation, not a proof of (B). The subgroup H x Sym(2) is amenable, but taking its topological full closure is an additional operation. No theorem used here says amenability survives that operation in this setting. Nor is Amp_2(H) identified with the abstract wreath product H wr Sym(2): its routing between layers can depend on y.

## 7. Countability and boundary controls

**Proposition 7 (countable reduction).** If (Q) has any counterexample, it has a countable counterexample on the same Cantor space.

**Proof.** Nonamenability of G gives a finite subset generating a nonamenable subgroup Γ. Choose a countable clopen basis (B_n) of nonempty sets in X. For each n, minimality and compactness give finitely many elements g_{n,j} with X=union_j g_{n,j}B_n. Let L be generated by Γ and all these elements. This is countable and acts minimally: any point lies in some g_{n,j}B_n, so its L-orbit meets every basis member. Its full closure G_0=[[L]] is countable, since X has only countably many clopen sets and there are countably many finite clopen partitions and finite L-labelings. It is a full minimal subgroup of G, contains Γ, and its U-corner is a subgroup of G_U. Thus G_0 is the desired counterexample. ∎

This does not make the germ groupoid Hausdorff. Hausdorff-groupoid theorems cannot silently replace the full scope of (Q).

**Boundary example A (fullness matters).** There is a minimal action of the nonamenable free group F_2 on a Cantor space K such that its rigid subgroup on every proper clopen U is trivial. To see existence without assuming an unspecified action, construct a faithful dense embedding of F_2 into a countable product of finite groups. For each L, take the finite ball B_L of reduced words. Left multiplication by a, respectively b, defines a partial bijection of B_L wherever its value stays in B_L; complete each to a permutation of B_L. The resulting homomorphism into Sym(B_L) sends every nontrivial reduced word of length at most L to a permutation moving the empty word, because its evaluation follows successive suffixes entirely within B_L. The product of these homomorphisms is injective. Let K be its closure. K is an infinite compact metrizable zero-dimensional group. It has no isolated point, since a compact group with an isolated point is discrete and finite. Thus K is a Cantor space. Left translation by the dense F_2 subgroup is free and minimal. A nonidentity translation fixes no point, so cannot be supported in a proper U.

This F_2-action is not full: a swap of two suitably small disjoint translated clopen sets, extended by the identity on a nonempty clopen complement, belongs to its full closure and has fixed points. The construction is therefore not a counterexample to (Q). F_2 is nonamenable by its usual four-cylinder paradoxical decomposition, or the Cayley-tree Følner obstruction.

**Boundary example B (minimality matters).** Let K be the preceding Cantor space, D a disjoint Cantor space, and F=[[F_2 acting on K]]. On X=K disjoint union D let G act by F on K and trivially on D. Then G is full: any map locally G fixes D pointwise and restricts to a member of F on K. G is nonamenable since it contains F_2, but G_D is trivial. The action is not minimal. Thus deleting minimality also invalidates (Q).

## 8. Scope and next mathematical step

The proved statements are Lemmas 1–2, Propositions 3–5 and 7, Theorem 6, and the two explicitly weakened-hypothesis counterexamples. The elementary local and measure results are credited, not promoted as discoveries. Historical novelty of the exact formulation in Theorem 6 is unverified.

The remaining task is to prove binary stability (B), or exhibit a full minimal amenable H for which Amp_2(H) is nonamenable. Equivalently, for a would-be counterexample, Proposition 4 locates the missing invariant mean on G.P. Neither the invariant probability on X nor amenable atom stabilizers supplies that mean. The finite computations accompanying this packet check algebraic formulas and boundary constructions only; they cannot decide amenability of the infinite groups in (Q).

**Original disposition: unsolved by this investigation.** No full proof, original-hypothesis counterexample, global openness certification, or independent-review verdict is claimed here.
