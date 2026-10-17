# Relative center and the inclusion carried by the wall

**Shared PASS1, row 1787. 14 October 2026 UTC.**

## Result

Fix a full strong monoidal inclusion `i: D → C` of fusion categories over the complex numbers. For the oriented-interface application, retain the spherical structure of C on D and the inherited trace on `M_i = _D C_C`. The algebraic identifications below do not themselves require sphericality.

With tensor product of endofunctors defined by **F ⊗ G = F ◦ G**, there are monoidal equivalences

`End_C(C_C) ≃ C`,

`E_i := Fun_{D|C}(M_i,M_i) ≃ Z_D(C)`.

The left action `D → End_C(C_C)` becomes exactly i, including its tensor constraints. The relative center uses pairs `(x,σ)` with

`σ_d: x ⊗ i(d) → i(d) ⊗ x` for d in D.

The two bulks act centrally on E_i, with a necessary orientation convention:

`overline{Z(D)} ⊠ Z(C) → Z(E_i)`.

Here the overline reverses the **braiding**, not the tensor product or morphisms. This canonical braided functor is an equivalence by the known center theorem of Kong–Zheng, specialized as checked below. The underlying tensor functors form the useful diagram

`Z(D) → Z_D(C) ← Z(C)`.

There is no asserted functor `Z(D) → Z(C)` obtained by extending half-braidings, nor a functor `Z(C) → Z(D)` obtained by discarding underlying objects. An arbitrary relative center is not braided. The middle category, together with its two specified central actions, is the inclusion-dependent algebraic comparison.

These facts strengthen the previously verified restricted-regular interface. The full oriented defect functor and its normalized TVBW bulk restrictions remain the application of Carqueville–Müller in the interface/defect lanes; the present result does not replace that functor-level theorem by a statement about centers.

## 1. Conventions and exact regular-module equivalence

All categories and functors are complex-linear. Module functors are additive/exact in this finite semisimple setting. Associators, unitors, and the strong monoidal constraints of i are inserted by coherence; formulas below use strict notation only to keep their types readable.

Write `C^{rev⊗}` for tensor reversal, `C^{op}` for reversal of arrows, and `overline B` for a braided category with the same tensor product and braiding `bar(c)_{a,b}=c_{b,a}^{−1}`. These are different operations. A center half-braiding always points `x⊗y → y⊗x` in this report.

Let F be a right-C-module endofunctor, with structural maps

`r_{m,c}: F(m⊗c) → F(m)⊗c`.

Set `x=F(1)`. Its right-module structure gives a natural right-module isomorphism

`F(c) ≅ F(1⊗c) → F(1)⊗c = x⊗c`.

Conversely `L_x(c)=x⊗c` is a right-C-module endofunctor. A right-module natural transformation `L_x → L_y` is exactly `f⊗id_c`, for a unique morphism `f:x→y`, obtained by evaluating at 1. Thus evaluation at 1 is fully faithful and essentially surjective.

Since `L_x ◦ L_y ≅ L_{x⊗y}`, this is a **monoidal** equivalence for the stated composition convention. Equivalently, its tensor constraint uses `F(G(1)) ≅ F(1)⊗G(1)`. This is not the reversed-tensor identification that one obtains from endofunctors of a regular **left** module.

The left action sends d to `L_{i(d)}`. Evaluation at 1 returns i(d), and the action comparison between d followed by e and d⊗e returns precisely the given tensorator of i. Therefore the specified regular right module, with its identification and distinguished unit object, remembers the original monoidal inclusion, not merely its image on simple labels or its fusion ring.

## 2. Wall endomorphisms are the relative center

A (D,C)-bimodule endofunctor is a right-module F together with left-module constraints

`l_{d,m}: F(i(d)⊗m) → i(d)⊗F(m)`

compatible with the right action. Replace F by `L_x` using Section 1. The mixed compatibility forces

`l_{d,m} = σ_d ⊗ id_m`,

where `σ_d = l_{d,1}: x⊗i(d) → i(d)⊗x`.

Indeed, apply the mixed module-functor diagram to `i(d)⊗(1⊗m)`: its two right-module constraints remove the m-factor, leaving the displayed formula. Naturality in d is inherited from l. The left-module associativity and unit axioms become

`σ_{d⊗e} = (id_{i(d)}⊗σ_e)(σ_d⊗id_{i(e)})`, and `σ_1=id_x`,

after inserting the constraints of i. Conversely these identities define coherent left-module maps `σ_d⊗id_m` on `L_x`, and their compatibility with the right action is immediate from the associator. This gives an equivalence on objects and structures.

A map `f:x→y` is a bimodule natural transformation exactly when

`(id_{i(d)}⊗f) σ^x_d = σ^y_d (f⊗id_{i(d)})`

for every d. This is precisely the morphism condition in the relative center, so the equivalence is fully faithful as well.

Composition gives the following tensor product:

`(x,σ^x) ⊗ (y,σ^y) = (x⊗y,σ^{xy})`,

`σ^{xy}_d = (σ^x_d⊗id_y)(id_x⊗σ^y_d)`.

The first step moves d left past y, the second past x. Hence the equivalence identifies composition, tensor unit, tensor constraints, and morphisms; it is not only an equivalence of linear categories.

This is the standard relative-center construction. Gelaki–Naidu–Nikshych, Definition 2.1 and Section 2.2, pp. 3–5 of the inspected preprint, use the opposite direction for the displayed central structure; replace their γ by σ inverse. Their Remark 2.4 establishes that the relative center of **any** fusion-subcategory inclusion is fusion and has

`FPdim(E_i) = FPdim(D) FPdim(C)`.

No grading hypothesis is needed for that preliminary result. The later braided-crossed/equivariantization theorem does require a faithful grading, which is not assumed here. The formula above is a Frobenius–Perron formula and is not substituted for either spherical global dimension in the TVBW normalization. [GNN](https://arxiv.org/pdf/0905.3117v1#page=3)

For an additional simple-unit check, a natural endomorphism of the identity bimodule functor is already determined by its component at 1 as a right-module transformation. Since `End_C(1)=C`, the tensor unit of E_i is simple.

## 3. Both central functors, with the braiding sign checked

### 3.1 The D-side tensor functor

For `(a,c^a)∈Z(D)`, define

`J(a,c^a) = (i(a), {i(c^a_d)}_{d∈D}) ∈ E_i`.

The tensorators of i are understood in the second expression. This is a fully faithful tensor functor: fullness of i identifies its morphisms with exactly the morphisms of Z(D) satisfying those half-braiding equations.

For an arbitrary `(x,σ)∈E_i`, define a half-braiding of J(a) with x by

`β^J_{a,(x,σ)} := σ_a^{−1}: i(a)⊗x → x⊗i(a)`.

This is a morphism of E_i. To check the potentially nontrivial point, naturality of σ applied to the D-morphism `c^a_d:a⊗d→d⊗a` gives

`σ_{d⊗a}(id_x⊗i(c^a_d)) = (i(c^a_d)⊗id_x)σ_{a⊗d}`.

Expand both relative half-braidings using their product axiom, then move `σ_a` to the other side. The resulting equality is exactly the condition that `σ_a^{−1}` intertwines the relative D-half-braidings on `i(a)⊗x` and `x⊗i(a)`.

Naturality in `(x,σ)` follows from the morphism condition of the relative center. The half-braiding axiom in x follows by inverting

`σ^{xy}_a=(σ^x_a⊗id_y)(id_x⊗σ^y_a)`.

The product axiom in a follows by inverting the relative half-braiding axiom for `a⊗a′`. Thus J lifts monoidally to Z(E_i).

Its braiding on two objects from Z(D) is

`β^J_{a,J(a′)} = i(c^{a′}_a)^{−1}`.

Consequently the **braided** lift has domain `overline{Z(D)}`, not Z(D) with its original braiding. Forgetting the braiding on the domain, its underlying tensor functor is the J just defined.

### 3.2 The C-side tensor functor

Restriction of a full half-braiding gives

`R:Z(C)→E_i`,

`R(b,c^b) = (b,{c^b_{i(d)}}_{d∈D})`.

It has a central lift defined by

`β^R_{b,(x,σ)} := c^b_x: b⊗x → x⊗b`.

For completeness, naturality of `c^b` for `σ_d:x⊗i(d)→i(d)⊗x` gives

`c^b_{i(d)⊗x}(id_b⊗σ_d) = (σ_d⊗id_b)c^b_{x⊗i(d)}`.

Expand the two full half-braidings by their hexagon. The result says exactly that `c^b_x` is a relative-center morphism. Its remaining half-braiding, tensor, and braided-functor axioms are the full half-braiding axioms in C. On two C-center objects it is `c^b_{b′}`, so this lift has the original braiding of Z(C).

R is not in general fully faithful as a functor into E_i. For `D=Vec`, it is the usual forgetful tensor functor `Z(C)→C`. For example, in `C=Vec_{Z/2}`, the two center objects supported at the unit with the two different characters are nonisomorphic in Z(C) but both have underlying object 1 in C. Thus fullness must not be inferred from the word “restriction.”

### 3.3 The combined braided lift

The two lifts centralize one another in Z(E_i):

`β^J_{a,R(b)} = (c^b_{i(a)})^{−1}`,

`β^R_{b,J(a)} = c^b_{i(a)}`.

Their composites are identities in either order. Consequently tensoring their images defines a braided monoidal functor

`Φ_i: overline{Z(D)} ⊠ Z(C) → Z(E_i)`,

with underlying object `i(a)⊗b`. Its tensorator moves b past i(a′) using `c^b_{i(a′)}` before applying the two original tensorators. The centralizing identity is exactly what makes the two-factor product braided.

In fact Φ_i is a braided equivalence. Here is the exact prior-result application. Kong–Zheng, Definition 2.6.1 and Example 2.6.3, pp. 13–14, associate to an `(A,B)`-bimodule M the central action `overline{Z(A)}⊠Z(B)→Z(Fun_{A|B}(M,M))`. Their Theorem 3.3.7, proof's first paragraph on p. 23, states that this canonical functor is an equivalence for indecomposable multi-fusion A,B and any nonzero semisimple M. In our case A=D and B=C are fusion, hence indecomposable, and M_i is the nonzero finite semisimple category C. The central actions in that construction are left multiplication and right multiplication. Section 1 identifies the latter, for a central b, with `L_b` using its full half-braiding. The resulting central structures are exactly `σ_a^{−1}` and `c^b_x` above. This checks the actual functor and its signs rather than merely inferring an abstract equivalence from matching dimensions. [KZ, precise convention](https://arxiv.org/pdf/1507.00503v3#page=13); [KZ, equivalence](https://arxiv.org/pdf/1507.00503v3#page=23)

In KZ's exact convention the canonical equivalence is `Z(D^{rev⊗}⊠C) → Z(E_i)`, identified with the displayed Φ_i. Thus the relevant Morita statement is about E_i and `D^{rev⊗}⊠C`, not a Morita equivalence between D and C. The equivalence of Z(E_i) with the displayed product does not identify Z(D) and Z(C), and does not make the original wall invertible. This is a braided-monoidal assertion only. Compatibility of Φ_i with selected pivotal/ribbon structures is not asserted; no oriented RT amplitudes or trace-normalized defect comparison are inferred from Φ_i. Those are supplied separately by the checked CM/CRS construction.

## 4. What data the wall remembers, and what it can forget

Fix the two bulk categories, with no relabelling by bulk autoequivalences. Let `i,j:D→C` be full strong monoidal inclusions. Denote their underlying, untraced bimodules by M_i and M_j.

**Proposition.** M_i and M_j are equivalent as (D,C)-bimodule categories if and only if there are a tensor-invertible `u∈C` and coherent natural isomorphisms

`θ_d:u⊗i(d)→j(d)⊗u`.

In strict notation their coherence is

`θ_{d⊗e}=(id_{j(d)}⊗θ_e)(θ_d⊗id_{i(e)})`, with `θ_1=id_u`,

with the tensorators of i and j inserted in general. Equivalently, `j ≅ Ad_u ◦ i` as strong monoidal functors, where `Ad_u(x)=u⊗x⊗u^{-1}` uses coherent evaluation data for u.

**Proof.** Every right-module equivalence F is `L_u` by Section 1. If G is a right-module quasi-inverse, write it as `L_v`. Evaluating `F◦G≅id` and `G◦F≅id` at 1 gives `u⊗v≅1` and `v⊗u≅1`, so u is invertible. Evaluating the left D-linearity of F at 1 gives exactly θ; its module-functor coherence is the displayed equation. Conversely an invertible u with such θ defines a bimodule structure on the right-module equivalence L_u, and its inverse inherits a coherent D-module structure. Tensoring θ with an inverse of u translates the same equation into monoidal naturality of `Ad_u◦i→j`. This proves both directions.

If an equivalence is additionally required to preserve the chosen marking `1∈C`, then `u≅1`; the inclusion is recovered up to monoidal natural isomorphism. If markings are forgotten, inner conjugacy can identify distinct specified embeddings. If bulk categories themselves may be relabelled, there are additional autoequivalence identifications; the proposition deliberately fixes the bulk labels.

Kong–Zheng's fully faithful center functor, Theorem 3.3.7, further says that **E_i together with both specified central actions**, up to their notion of monoidal-bimodule equivalence, remembers this untraced bimodule equivalence class. The bare fusion category E_i without its two actions is not asserted to recover i. Neither result recovers a selected spherical trace from tensor-category data alone. [KZ](https://arxiv.org/pdf/1507.00503v3#page=23)

### Trace-normalization qualification

Now restore the inherited spherical traces on both walls. For an endomorphism f of m,

`tr_C(id_u⊗f) = dim_C(u) tr_C(f)`.

Thus the equivalence L_u in the proposition is an ordinary Calabi–Yau-trace-preserving equivalence if and only if `dim_C(u)=1`. Necessity already follows at `m=1,f=id_1`; sufficiency follows from the displayed multiplicativity for every endomorphism. Conjugating by the natural isomorphism that identifies F with L_u does not change traces.

Sphericality gives `dim(u)=dim(u*)` and invertibility gives `dim(u)dim(u*)=1`, so the possible values are `+1` and `−1`. The negative case occurs, for example, for the nontrivial invertible in `Vec_{Z/2}` equipped with the sign spherical structure. Left tensoring by it negates the inherited trace. Therefore the untraced conjugacy classification must not be advertised as a classification of normalized traced physical defects. The condition above concerns literal preservation of the stated Calabi–Yau trace; it does not claim a classification of all equivalences in an Euler-completed defect theory or modify CM's definition of bimodule-functor labels.

## 5. Reversal and algebraic fusion checks

An explicit admissible reverse-action bimodule is `N_i = _C C_D`. In the spherical setting the traced opposite of M_i identifies with N_i by dualization at the traced-bimodule level, as established in the interface lane. CM's actual orientation reversal, evaluation, coevaluation and Euler-adjusted adjunction maps remain those of its theorem; equality of all those maps with this algebraic presentation is not asserted. In particular, reversal is not inverse-wall cancellation.

There is a direct monoidal convention check on its endomorphisms. A left-C-linear endofunctor of N_i is `R_x(m)=m⊗x`. Its right-D-linearity is a family

`δ_d:i(d)⊗x→x⊗i(d)`.

Set `δ_d=σ_d^{−1}`. Then `(x,σ)↦R_x` identifies the underlying categories of E_i and `Fun_{C|D}(N_i,N_i)`, but

`R_x ◦ R_y = R_{y⊗x}`.

Accordingly

`Fun_{C|D}(N_i,N_i) ≃ E_i^{rev⊗}`.

This explicitly records tensor reversal and does not confuse it with arrow reversal or reversal of a braiding.

The relative tensor product has the algebraic equivalence

`M_i ⊠_C N_i ≃ _D C_D`,

induced by `x⊠y ↦ x⊗y`. It is C-balanced by the associator. Its inverse sends z to `1⊠z`; the balancing isomorphism identifies `x⊠y` with `1⊠(x⊗y)`. Left and right D-actions are the corresponding restrictions. The other product is `_C(C⊠_D C)_C`, with a balanced multiplication functor to `_C C_C`. Neither is automatically the identity bimodule. These formulas concern underlying bimodule tensor products; no equality of Euler-adjusted evaluation/coevaluation maps or their numerical trace normalization is being inferred.

For a composable chain `E --j→ D --i→ C`, the same balancing argument gives

`(_E D_D) ⊠_D (_D C_C) ≃ _E C_C`,

where the last left action is i◦j. This verifies functorial dependence on nested inclusions at the untraced bimodule level. A corresponding trace-normalized fusion assertion would require matching the chosen relative-product trace conventions and is not needed here.

The distinguished wall is invertible as an underlying bimodule **if and only if i is a tensor equivalence**. Sufficiency is the regular identity-wall case after transport. For necessity, an inverse bimodule would identify `End_C(M_i)` with `End_D(D_D)` by tensoring endofunctors with the inverse wall. Under that identification the left action `D→End_C(M_i)` is an equivalence, because on the identity D-wall it is left multiplication. Section 1 identifies this very functor with i. Hence i must be essentially surjective. This is also the action-equivalence argument used in Kong–Zheng's proof of Proposition 2.4.4, p. 10. A proper full fusion-subcategory inclusion therefore produces a noninvertible wall. [KZ](https://arxiv.org/pdf/1507.00503v3#page=10)

## 6. Adversarial limits and checks

- **Identity inclusion:** `Z_C(C)=Z(C)`. Φ becomes the usual factorization `overline{Z(C)}⊠Z(C)→Z(Z(C))`, with the inverse-braiding lift on the first factor. This checks the orientation sign.
- **Trivial subcategory:** `Z_Vec(C)=C`; R is the forgetful functor, and Φ identifies `Z(Vec)⊠Z(C)` with Z(C). This checks that no false full-faithfulness is imposed on R.
- **Relative center need not be braided:** choose `D=Vec`, `C=Vec_G` for a nonabelian finite group. If C were braided, simple objects g,h would have an isomorphism `gh→hg`, forcing all g,h to commute. Thus E_i=C is not braided in this example.
- **No naive extension of a half-braiding:** J(a) has only a D-half-braiding. Its central structure in Z(E_i) is defined against relative-central objects, using their σ; it is not a supplied half-braiding with every object of C.
- **No direct bulk equivalence:** the product-center equivalence in Section 3 is fully consistent with unequal TVBW invariants and unequal surface-state dimensions for D and C.
- **Trace matters separately:** abstract center functoriality and its full-faithfulness are tensor-category statements. They do not discard inherited spherical structures or normalize CM's defects for free.
- **No new stronger target:** no ordinary monoidal natural transformation between the bulk TQFTs, classification of all walls, equality of theories, or universal state-space injection is being made a requirement of the qualitative source problem.

## 7. Primary sources and inspection status

1. S. Gelaki, D. Naidu, D. Nikshych, *Centers of graded fusion categories*, Algebra & Number Theory 3 (2009), 959–990. Complete arXiv:0905.3117v1 inspected, especially pp. 3–5, Definition 2.1, equations (1)–(5), Remark 2.4. Pages 4–5 were also visually inspected. These preliminary statements concern arbitrary fusion subcategories. [Version inspected](https://arxiv.org/pdf/0905.3117v1)
2. L. Kong, H. Zheng, *The center functor is fully faithful*, Advances in Mathematics 339 (2018), 749–779. Complete arXiv:1507.00503v3 inspected, especially pp. 10, 13–14, 19, 22–24; Proposition 2.4.4, Definition 2.6.1, Example 2.6.3, Theorems 3.1.8/3.3.7. Pages 13 and 23 were additionally rendered and visually checked so that overlines lost in text extraction could not corrupt the braiding convention. [Version inspected](https://arxiv.org/pdf/1507.00503v3); [journal DOI](https://doi.org/10.1016/j.aim.2018.09.031)
3. N. Carqueville, L. Müller, *Orbifold Completion of 3-Categories*, Communications in Mathematical Physics 407, article 8 (2026). The retained published p. 54, Theorem 5.18, was independently crosschecked: line/junction labels are bimodule functors, with natural transformations one level higher. The full trace and TQFT application is established in the other PASS1 reports. [Published DOI](https://doi.org/10.1007/s00220-025-05434-y)

The two new source PDFs are inspected preprints of published works; no fresh version-of-record full-text verification is claimed for them. The regular-module, relative-center, central-lift, conjugacy and fusion proofs above are explicit reconstructions of standard structure, not novelty claims. The stronger center-equivalence and recovery assertions are explicitly attributed to the inspected Kong–Zheng theorem. Source copies and rendered pages are retained separately from this authored report.
