# Intrinsic complement configuration spaces: a scoped obstruction and two escape routes

Authored mathematical investigation, 14 October 2026. This is a partial result for the operational version of Roberts's Problem 1.7, not a Jones construction, a novelty claim, or an impossibility theorem for the original problem.

## Result first

1. The fundamental groups of ordinary point configurations in a three-dimensional knot complement are products and wreath products of the knot group. Local exchanges are involutions. Thus Bigelow's generic moving-particle exchange local system does not extend unchanged from a punctured disc to these configuration spaces.
2. For every positive particle number, the natural uniform generic rank-one meridional system has zero absolute ordinary and Borel–Moore homology over `Q(u)`, for every knot. The assertion holds with either unordered exchange sign. More generally, the same vanishing holds for ordered integer charges whenever the total charge is nonzero.
3. This does not eliminate torsion, Laurent-polynomial modules, relative homology, specializations, nonabelian/higher-rank systems, or more elaborate spaces. Even before these qualifications, a plain finite-rank twisted Euler characteristic is zero on these configuration spaces.
4. A concrete escape from generic acyclicity is an ordered positive/negative pair. Its homology is nonzero, but is canonically just the ordinary homology of the complement shifted by two. Nonabelian representation families and relative charged configurations remain legitimate research routes; neither is completed here.

## 1. Conventions and naturality

Let `K` be a smooth/tame oriented knot in oriented `S³`, and put

- `M = S³ \ K`, an open oriented three-manifold;
- `E = S³ \ int(νK)`, a compact exterior, with `M` diffeomorphic to `int(E)` and homotopy equivalent to `E`;
- `G = π₁(M)`;
- `ℓ : G → Z`, positive meridional linking number, so `H₁(M;Z)=Z`;
- `F_n(M) = {(x₁,…,x_n)∈Mⁿ : x_i≠x_j for i≠j}`;
- `C_n(M) = F_n(M)/S_n`.

All particles lie in the open complement. We are not using configurations in a manifold with boundary, and are not identifying the punctured disc with `M`. Let `k=Q(u)`, with `u` transcendental. For `r∈Z`, `L_r` denotes the rank-one `k` local system on `M` with monodromy `g↦u^{rℓ(g)}`. In particular `L₀=k` and `L_r^∨=L_{−r}`.

For an ordered charge vector `w=(w₁,…,w_n)`, let

`A_w = (L_{w₁} ⊠ ⋯ ⊠ L_{w_n})|_{F_n(M)}`.

These spaces and systems are natural under orientation-preserving diffeomorphisms of oriented knot pairs: the induced complement diffeomorphism preserves positive linking number and hence pulls back the indicated local systems. Basepoints and choices of paths only express the usual isomorphism/conjugacy ambiguity of local systems. No Jones polynomial is used in their definition.

The results below concern all ordinary knots. No extension to arbitrary ambient three-manifolds or all oriented links is claimed for the acyclicity theorem.

## 2. Fundamental groups and all possible monodromies

### Proposition 2.1

For `n≥1`,

`π₁(F_n(M)) ≅ Gⁿ`.

For `n≥2`,

`π₁(C_n(M)) ≅ Gⁿ ⋊ S_n = G wr S_n`,

where `S_n` permutes the factors. Consequently

`H₁(C_n(M);Z) ≅ Z ⊕ Z/2`.

For `n=1`, the second summand is absent.

### Proof

The forbidden diagonals in `Mⁿ` have codimension at least three. A loop can be perturbed off this finite stratified union, as can a homotopy of loops, relative to endpoints, because its domain has dimension at most two. Thus inclusion `F_n(M)→Mⁿ` induces an isomorphism on fundamental groups.

The free `S_n` covering gives an exact sequence

`1 → Gⁿ → π₁(C_n(M)) → S_n → 1`.

Choose a small open three-ball `B⊂M` containing the base configuration. The same general-position argument gives `π₁(F_n(B))=1`, so the covering `F_n(B)→C_n(B)` identifies `π₁(C_n(B))` with `S_n`. Inclusion `C_n(B)→C_n(M)` is a section of the displayed quotient: its composite with the quotient to `S_n` is precisely the covering monodromy isomorphism. Thus the section is injective and the extension splits. With paths in the simply connected ball identifying the coordinate basepoints, conjugation by this section permutes the `G` factors. The choices need not define a canonical section; their role is to establish the group isomorphism and the local exchange relations.

Abelianization identifies all coordinate copies of `G_ab=Z` under the symmetric-group action, leaving one `Z`; the symmetric group contributes its sign `Z/2`. ∎

### Rank-one consequence

Over a field of characteristic different from two, a rank-one system on `C_n(M)` has character

`(g₁,…,g_n;σ) ↦ a^{Σ_i ℓ(g_i)} ε^{parity(σ)}`,

where `a` is a nonzero field element and `ε∈{+1,−1}`. Thus the continuous/free parameter is total meridional winding. Local point exchange contributes only a sign. On ordered configurations, the coordinate meridional parameters may be chosen independently.

### Higher-rank consequence, without a rank-one restriction

Every finite-rank local system is a representation of the full wreath product, not merely its abelianization. Equivalently it specifies:

- representations `T_i:G→GL(W)`, whose images commute for distinct indices;
- operators `S_i` satisfying the Coxeter relations, in particular `S_i²=I`;
- compatibility `S_i T_j(g) S_i⁻¹ = T_{(i,i+1)j}(g)`.

This allows genuinely nonabelian monodromy within each `G` factor. A natural construction from any representation `ρ:G→GL(V)` is the external tensor system on `V^{⊗n}`, with `T_i(g)` acting by `ρ(g)` on the `i`th factor and `S_i` the adjacent factor flip. One may also tensor by a representation of `S_n`, and general wreath-product representations need not be reduced to this one example.

The missing ingredient is not the existence of higher-rank systems. It is a geometrically justified choice or family of them, together with an extraction and a proof of Jones agreement. An arbitrary choice of `ρ` is extra input. Pullback of representations under complement diffeomorphisms is natural, but does not select one representation for every knot.

## 3. The precise dimensional obstruction to transplanting Bigelow

In a small disc avoiding all fixed punctures, a moving-particle exchange is an Artin generator. In a surrounding three-ball disjoint from `K`, the same exchange has order two, by Proposition 2.1. Therefore any coefficient local system on `C_n(M)` restricts to a disc system whose local exchange matrix `R` satisfies `R²=I`.

Bigelow's coefficient character assigns an independent Laurent variable to a moving-particle half twist. Denote this variable by `d` here, to distinguish it from our meridional `u`. His Jones specialization is `d=−q⁻¹`; for generic `q`, `d²=q⁻²≠1`. Therefore this coefficient local system cannot be the restriction of an ordinary local system on `C_n(M)` with the same prescribed local exchange. This is already an obstruction before specifying homology classes.

This is a coefficient-system extension obstruction, not an assertion that every braid representation on homology factors through `S_n`. In particular, Bigelow's action of the braid group of the fixed punctures on twisted homology is different from the local moving-particle exchange loop considered here. Higher-rank coefficient matrices also obey the involution relation for this particular loop; they can still have nonabelian knot-group monodromy and nontrivial induced actions on homology.

Primary baseline: Stephen Bigelow, *A homological definition of the Jones polynomial*, Geometry & Topology Monographs 4 (2002), 29–41, §2 and Theorem 2.8. [Author PDF](https://web.math.ucsb.edu/~bigelow/publications/06.pdf).

## 4. Generic meridional acyclicity on the complement

### Lemma 4.1

For every nonzero integer `r`,

`H_*(M;L_r)=0` and `H_c^*(M;L_r)=0`.

The same holds with `r` replaced by `−r`.

### Proof

The infinite cyclic Alexander module of a knot is torsion over `Q[z,z⁻¹]`. For clarity, a Seifert matrix `A` gives a square presentation with determinant, up to a unit, `det(zA−Aᵀ)`. At `z=1` this is `det(A−Aᵀ)=±1`, since the Seifert-surface intersection pairing is unimodular. Hence the determinant is a nonzero Laurent polynomial, including the genus-zero case, where the determinant is `1`.

Substitution `z=u^r` is injective for `r≠0`. After passing to `k=Q(u)`, that presentation matrix is invertible. Thus `H₁(E;L_r)=0`. Also `H₀(E;L_r)=0`, since a meridian acts by `u^r` and `u^r−1` is invertible. A compact knot exterior has a finite two-dimensional spine and Euler characteristic zero, so `H₂(E;L_r)=0`, and there is no higher homology. This also follows from twisted Poincaré–Lefschetz duality, using the acyclic meridional system on the boundary torus. Since `E≃M`, ordinary homology vanishes on `M`.

Poincaré duality for the oriented open three-manifold gives `H_c^j(M;L_r)≅H_{3−j}(M;L_r)`, proving the compact-support assertion. The same argument applies to the dual system `L_{−r}`. ∎

This argument uses classical Alexander homology only to analyze the proposed new coefficient system; it does not claim that the Jones polynomial equals the Alexander polynomial.

## 5. Acyclicity of all configurations with nonzero total charge

### Theorem 5.1

Suppose `w=(w₁,…,w_n)∈Zⁿ` has nonzero total charge:

`W=Σ_{i=1}^n w_i ≠ 0`.

Individual charges and proper subset sums are allowed to vanish.

Then

`H_*(F_n(M);A_w)=0`,

`H_c^*(F_n(M);A_w)=0`, and

`H_*^{BM}(F_n(M);A_w)=0`.

In particular, this holds for `w=(1,…,1)` for every finite `n≥1`. It also holds with every charge negated.

### Proof with every diagonal coefficient specified

Let `X=Mⁿ`, let `A=L_{w₁}⊠⋯⊠L_{w_n}`, and let `D=X\F_n(M)` be the union of pairwise diagonals `D_{ij}`.

An intersection of any nonempty collection of pairwise diagonals is a partial diagonal `D_π` indexed by a partition `π` of `{1,…,n}`. It is diffeomorphic to `M^{|π|}`. Its coefficient restriction is exactly

`A|_{D_π} ≅ ⊠_{B∈π} L_{w(B)}`, where `w(B)=Σ_{i∈B}w_i`.

Since the sum of all block charges equals `W≠0`, at least one block charge is nonzero in every partition. Lemma 4.1 makes that factor compact-support acyclic. The compact-support Künneth theorem over `k` then makes the entire product acyclic, even when other block charges vanish. Thus every `D_π` has zero compact-support cohomology with this restricted coefficient system. The same argument applies to `X`, the partition into singletons. This is why nonzero total charge suffices; one need not demand that every subset sum be nonzero.

Here is a precise justification of using the finite closed diagonal cover. For each finite intersection, take the restricted local-system sheaf pushed forward from that closed intersection to `D`. The augmented alternating Čech complex for the finite closed cover `{D_{ij}}` is exact stalkwise: at a point it is the augmented cochain complex of the simplex of diagonals containing that point, with a common coefficient stalk. Derived compactly supported sections give a finite Mayer–Vietoris spectral sequence whose terms are the compact-support cohomologies of the intersections. All terms vanish, so `H_c^*(D;A|_D)=0`. Equivalently, one can use a compatible triangulation of this finite diagonal arrangement.

The open/closed localization sequence for `F_n(M)⊂X` and `D⊂X` now gives `H_c^*(F_n(M);A_w)=0`. Since `F_n(M)` is oriented of dimension `3n`, Poincaré duality gives ordinary homology zero.

For Borel–Moore homology, do not identify it with ordinary homology. Apply the same argument to the dual system `A_w^∨=A_{−w}`. Finite-type linear duality over `k` gives `H^*(F_n(M);A_w)=0` from `H_*(F_n(M);A_{−w})=0`. Then open-manifold duality `H_i^{BM}(F_n(M);A_w)≅H^{3n−i}(F_n(M);A_w)` proves the stated Borel–Moore vanishing. ∎

### Corollary 5.2: unordered systems

Let `U_{u,ε}` be the rank-one system on `C_n(M)` whose meridional character is `u` and whose permutation character is `ε=±1`. For every `n≥1`,

`H_*(C_n(M);U_{u,ε})=H_*^{BM}(C_n(M);U_{u,ε})=0`.

Indeed, its pullback to the finite ordered cover is `A_(1,…,1)`. In characteristic zero, finite deck-group invariants/coinvariants are exact; equivalently, the chain complex downstairs is a direct summand of the pulled-back complex via averaging. The same assertion holds for locally finite chains because the covering is finite and proper. Thus both homologies vanish. For duality-based verification, the unordered orientation character in dimension three is the permutation sign; tensoring by it interchanges the two cases already included.

The conclusion remains true if `u` is replaced by any nonconstant rational function `a(u)`: each nonzero power is transcendental over `Q`, so the nonzero Alexander determinant remains nonzero after substitution. It does not cover every constant or root-of-unity specialization.

### Exact scope of the obstruction

A rule using only these absolute `k`-homology groups, or pairings on these zero absolute groups, cannot distinguish any two knots. Allowing all finite particle numbers, rather than fixing a universal `n`, does not help this specific rule: every positive-particle group still vanishes.

This does **not** say an acyclic chain complex has trivial Reidemeister torsion, nor that its homology over `Q[u,u⁻¹]` is zero. The one-particle Alexander example itself demonstrates that distinction. It does not exclude relative classes, chains with specified boundaries, finite specializations, nonabelian local systems, enriched operations, or other geometrically defined spaces.

## 6. A separate Euler-characteristic limitation

For every `n≥1`, `χ(F_n(M))=χ(C_n(M))=0`. One proof uses the Fadell–Neuwirth forgetful fibration. The fiber of `F_n(M)→F_{n−1}(M)` is `M` minus `n−1` points, a finite-type space. Since the induction begins with `χ(M)=0`, multiplicativity makes every ordered Euler characteristic zero. The finite `n!`-sheeted covering gives the unordered result.

The spaces have finite CW type; for example, use an appropriate configuration compactification of the finite-type manifold or a tame triangulated model. If `W` is any finite-rank local system over a field, cellular chain dimensions give

`χ(C_n(M);W)=rank(W)·χ(C_n(M))=0`,

and likewise for ordered configurations. Thus this Euler-characteristic limitation applies to arbitrary finite-rank nonabelian coefficients, unlike Theorem 5.1. Compactly supported/Borel–Moore Euler characteristics vanish as well by duality and the same rank argument. It is a statement about an ungraded Euler characteristic; it is not an obstruction to the full graded groups, torsion, relative theories, or a nontrivial intersection operation.

Primary source for the configuration-space fibration: Edward Fadell and Lee Neuwirth, *Configuration Spaces*, Mathematica Scandinavica 10 (1962), 111–118, Theorem 1. [Publisher page](https://journals.msp.org/mscand/article/view/2674), [DOI](https://doi.org/10.7146/math.scand.a-10517).

## 7. A worked escape: a positive/negative pair

The nonzero-total-charge hypothesis is substantive. Let

`A = (L₁⊠L₋₁)|_{F₂(M)}`.

The ambient product `X=M²` is acyclic with its external coefficient system, but the collision diagonal `D≅M` has coefficient `L₁⊗L₋₁≅k`. The canonical evaluation identifies the diagonal coefficient with the trivial system. Compact-support localization now gives

`H_c^j(F₂(M);A) ≅ H_c^{j−1}(M;k)`.

Applying oriented duality in dimensions six and three yields

`H_i(F₂(M);A) ≅ H_{i−2}(M;k)`.

Since a knot complement has ordinary `k`-homology `k` in degrees zero and one and zero elsewhere,

- `H₂(F₂(M);A)≅k`;
- `H₃(F₂(M);A)≅k`;
- all other ordinary groups vanish.

Applying the calculation to the dual coefficients and then Borel–Moore duality gives `k` in Borel–Moore degrees three and four, and zero in every other degree. These degree shifts can also be checked from the Thom isomorphism for the oriented codimension-three diagonal: its small normal linking sphere has dimension two.

This is a genuine intrinsic local-system construction, but these resulting graded vector spaces are the same for every knot, so the computation by itself does not extract Jones. It is useful because it identifies exactly where nontrivial classes enter: zero-total-charge collision strata. For more particles, one may use separately unordered positive and negative colors, quotienting by `S_p×S_m`; one cannot forget the colors and retain unequal charges in a rank-one system on the fully unordered space.

## 8. Higher-rank and relative replacements worth testing

### 8.1 Nonabelian families

The all-knots generic acyclicity statement is false if one simply replaces the rank-one character by arbitrary higher-rank representations. Friedl and Vidussi's Theorem 1.1 supplies, for a nonfibered knot exterior, a finite quotient whose associated twisted Alexander polynomial is zero. With the regular finite-group representation and meridional variable, the twisted first homology is then not torsion and survives over `Q(u)`. This is a concrete reason not to extend Theorem 5.1 to all representations. [Author PDF](https://friedl.app.uni-regensburg.de/papers/vanish-sw.pdf), [arXiv record](https://arxiv.org/abs/1205.2434).

A representation chosen from geometric holonomy covers only some knot complements and has choices. A choice-free alternative at the level of inputs is to retain the full groupoid of finite-rank local systems, or a universal representation family with peripheral data, rather than choosing one `ρ`. In a framed presentation, the representation scheme has a tautological representation; changing the framing acts by conjugation, so a genuinely intrinsic family must retain this equivariance or the representation groupoid/stack. This supplies an intrinsic family of coefficient complexes, not a Jones extraction. A canonical cycle, trace, integral, or pairing and exact polynomial identity remain missing.

A useful generalization of the diagonal argument is conditional: for an external tensor system `E^{⊠n}`, if every tensor power `E^{⊗r}` for `1≤r≤n` is compact-support acyclic on `M`, then the same closed-diagonal argument makes `F_n(M)` compact-support acyclic. If these tensor powers and their duals are acyclic, ordinary and Borel–Moore homology vanish. Thus a higher-rank proposal should explicitly identify which tensor-power collision strata carry its desired classes.

### 8.2 Relative charged configurations

A more directly geometric next object is a compactified configuration of positively and negatively charged points in the exterior, with boundary faces for collisions and approach to the peripheral torus. Charged external tensor local systems are already defined without a projection. Relative boundary conditions could retain classes that disappear in absolute homology. The knot orientation determines the positive meridian and preferred zero-linking longitude, so peripheral data are available intrinsically; a collar or tubular neighborhood can be auxiliary data whose transport must be proved.

A viable next theorem would need to specify, rather than assume:

1. the precise compactification and the exact union of boundary faces used in each relative pair;
2. the coefficient system, including extension or singular behavior at each zero-charge collision face;
3. distinguished classes or a canonical operation supplied by the knot pair, not by an unproved disc/plat choice;
4. transport and independence under changes of collar, compactification models, and any auxiliary decomposition;
5. a pairing and normalization equal to the full source-normalized `V_K(t)` for every knot.

Adding a framing to ordinary point particles alone does not automatically restore Bigelow's free braid exchange parameter. One must compute the fundamental group and the relevant collision/rotation monodromies for the proposed replacement space. Similarly, naming a derived or higher local system is not a substitute for constructing genuine coefficient data and the required extraction.

## 9. Acceptance outcome

The spaces, monodromies, support conventions, and natural transport above are well defined. Theorems 5.1 and 5.2 close the simplest generic rank-one absolute-homology route for every finite particle number, and Proposition 2.1 explains why a direct copy of Bigelow's exchange character fails in dimension three. Section 7 verifies a concrete way around one hypothesis. The accompanying `NEUTRAL_CHARGE_EXTENSION.md` computes an all-particle minimal-neutral family: its graded groups are nonzero but knot independent, with multiplicity `(n−1)!`. Neither these escapes nor the higher-rank/relative directions supply the distinguished classes and full Jones equality required by the operational contract.

**Outcome: partial structural result; original construction request unresolved by this approach.** No present-day general openness claim is made.
