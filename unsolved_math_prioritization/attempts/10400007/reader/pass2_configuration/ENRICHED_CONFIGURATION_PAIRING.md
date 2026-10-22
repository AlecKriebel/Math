# A knot-sensitive secondary pairing from complement local systems

PASS2, 14 October 2026. This approach preserves the accepted PASS1 theorems and the distinction between the valid PASS1 transported construction and the later direct geometric PASS2 construction. The construction below is classical Blanchfield theory, presented as an explicit tractable enrichment of the complementary-particle route. No novelty is claimed.

## Outcome

There is a genuinely intrinsic, knot-sensitive operation that the PASS1 field-level acyclicity results discard: the Laurent-coefficient Alexander module together with its secondary equivariant linking pairing. We specify its spaces, local systems, maps, naturality, and exact trefoil/mirror calculation. It distinguishes those two knots even though their unadorned Alexander modules agree.

The operation retains classical Alexander–Blanchfield information, which is richer than the Alexander polynomial or its unadorned module. It does not retain the full knot or determine Jones. In particular, the entire module and pairing vanish for Alexander-one knots, whereas an explicit eleven-crossing example has nontrivial Jones polynomial. Thus a full Jones extraction from this particular enriched datum is impossible; this is a restriction on the specified datum, not on Roberts's construction problem.

A separate exact computation of the first nonminimal neutral configuration `(1,1,−1,−1)` gives ordinary Betti numbers `2,4,8,6` in degrees `4,5,6,7`. Its collision filtration is natural, but the collapse does not supply a canonical direct-sum splitting or determine every additional operation. That calculation is in `NONMINIMAL_NEUTRAL_FOUR_PARTICLES.md`.

## 1. Intrinsic input and coefficient data

For an oriented smooth/tame knot `K⊂S³`, let `E=S³\int(νK)` be its oriented compact exterior. The positive meridian fixes `ℓ:π₁(E)→Z`. Let

`Λ=Q[u,u⁻¹]`, `Q=Q(u)`, and `bar(u)=u⁻¹`.

Write `Λ_ℓ`, `Q_ℓ`, and `(Q/Λ)_ℓ` for the genuine local systems with monodromy multiplication by `u^{ℓ(g)}`. Here `Λ_ℓ` is rank one over the Laurent ring. It is not being treated as a finite-dimensional constant rational system.

Define the Alexander module

`A_K=H₁(E;Λ_ℓ)`.

It is finitely generated and Λ-torsion; over the PID Λ it has a square Seifert presentation. Thus localizing to Q gives the zero first homology seen in PASS1, but does not erase `A_K` or its linking form.

## 2. The homological operation

The coefficient sequence

`0 → Λ_ℓ → Q_ℓ → (Q/Λ)_ℓ → 0`

gives a Bockstein map. Use the following intrinsic maps, with the involution on dual coefficient modules understood:

1. `H₁(E;Λ_ℓ) → H₁(E,∂E;Λ_ℓ)`;
2. inverse Poincaré–Lefschetz duality, from relative first homology to conjugate second cohomology;
3. inverse Bockstein `H²(E;Λ_ℓ) → H¹(E;(Q/Λ)_ℓ)`;
4. Kronecker evaluation on `H₁(E;Λ_ℓ)`.

The Bockstein is invertible in these degrees because the Q-coefficient complex is acyclic. The absolute-to-relative map is an isomorphism for a knot exterior: the boundary longitude class maps to zero because it bounds the lifted Seifert surface, and the map of zeroth Λ-homology from boundary to exterior is an isomorphism. Over the PID Λ, `Q/Λ` is injective, so the evaluation map has no obstructing Ext term.

Their composite defines the nonsingular Hermitian pairing

`β_K : A_K × A_K → Q/Λ`,

using the convention conjugate-linear in the first argument and linear in the second:

`β_K(a x,b y)=bar(a) β_K(x,y)b`.

This is the transpose convention for the Blanchfield pairing used by Friedl–Powell. Its invariant meaning is unchanged, but the matrix formula must be transposed accordingly; the sign and presentation-side issue are not suppressed.

### Why this is natural

An orientation-preserving diffeomorphism of oriented knot pairs preserves the positive meridian and hence the coefficient sequence. Its induced maps commute with relative homology, cap product with the fundamental class, the connecting map, and evaluation. Therefore it induces an isometry of `β_K`. Tubular-neighborhood changes only replace the exterior by a canonically isotopic model. A Seifert surface or a matrix is used to calculate the already defined pairing, not to define its intrinsic isometry class.

## 3. A direct secondary-intersection interpretation

Let `Ẽ→E` be the infinite cyclic cover, with deck generator `u`. Represent two module elements by compact one-cycles `x,y` in `Ẽ`, chosen disjoint after perturbation. Since the module is torsion, choose a nonzero `p(u)∈Λ` and a compact rational two-chain `C` with

`∂C=p(u)x`.

In the linear-first convention, the linking value is

`(1/p(u)) Σ_{j∈Z} (C · u^j y) u^j  mod Λ`.

The sum is finite because the chains are compact and the deck action is proper. Changing bounding chains or representatives changes the rational expression by a Laurent polynomial, which is precisely why the target is `Q/Λ`. Swapping the two arguments gives our conjugate-first `β_K`. The cohomological construction above establishes the choice-independence, Hermitian symmetry and nonsingularity.

This is closely tied to opposite-charge two-particle topology. In `Ẽ×Ẽ`, the three-chain `C×y` meets the lifted collision graphs

`D_j={(u^j z,z):z∈Ẽ}`

in isolated points. Their signed counts are the displayed equivariant intersections. Quotienting the product covering by simultaneous deck translation produces the difference-character cover: its monodromy is `u^{ℓ(g₁)−ℓ(g₂)}`, the `(1,−1)` coefficient system of PASS1. Thus this is a secondary diagonal-linking operation with boundary data, not an ordinary intersection form on the already localized absolute groups.

The division by `p(u)` and the quotient modulo Λ are essential. Forgetting these and retaining only the Q-vector-space homology loses the knot-sensitive information.

## 4. Exact Seifert-matrix computation and convention check

Let `S` be a Seifert surface and let `A=(lk(d_i,d_j⁺))` be its Seifert matrix in the convention of Friedl–Powell. Their presentation is

`A_K ≅ coker(M)`, where `M=uA−Aᵀ`.

Their linear-first form uses the matrix `(u−1)(A−uAᵀ)⁻¹`. Passing to our conjugate-first convention gives

`β_K([x],[y]) = bar(x)ᵀ B y mod Λ`,

`B=(1−u)(uA−Aᵀ)⁻¹=(1−u)M⁻¹`.

Two checks prevent a common transpose error:

- `BM=(1−u)I`;
- `bar(M)ᵀB=(u−1)u⁻¹I`.

Both are matrices over Λ. Hence replacing either representative by a presentation relation changes the value by an element of Λ. Also `bar(B)ᵀ=B`, so the displayed matrix is Hermitian over Q.

The primary matrix theorem and intrinsic Bockstein construction are Friedl–Powell, *A calculation of Blanchfield pairings of 3-manifolds and knots*, Theorem 1.3 and §2.4. [Primary manuscript](https://arxiv.org/pdf/1512.04603v2).

### Trefoil and mirror

Take the genus-one trefoil Seifert representative

`A = [[1,0],[-1,1]]`.

Then

`M = [[u−1,1],[-u,u−1]]`,

`Δ=u²−u+1`, and

`B=(1−u)/Δ · [[u−1,−1],[u,u−1]]`.

The unit entry in `M` gives `A_K≅Λ/(Δ)`. The class `e₁` generates: the first column relation gives `e₂=(u−1)u⁻¹e₁`, and the other relation gives precisely `Δe₁=0` up to a Laurent unit. Its self-pairing is

`β_K(e₁,e₁)=−(u−1)²/Δ ≡ u/Δ mod Λ`,

because the two rational expressions differ by `−1`.

A standard mirror matrix is `−Aᵀ`. Swapping the two basis vectors makes it `−A`, since the swap matrix `P` satisfies `PᵀAᵀP=A`. Thus the mirror has the same cyclic module and the negative form, with generator self-pairing `−u/Δ`. This conclusion is unchanged if one uses the reverse mirror to align peripheral orientation conventions; reversing the orientation of a knot does not alter its Jones polynomial.

### The forms are not isometric

Any Λ-module automorphism of `Λ/(Δ)` is multiplication by a nonzero element `f` of the field

`F=Q[u,u⁻¹]/(u²−u+1) ≅ Q(ζ₆)`.

An isometry between the two displayed forms would require

`f bar(f)=−1` in F.

Write `f=a+bζ₆`, with `a,b∈Q`. Then

`f bar(f)=a²+ab+b²=(a+b/2)²+3b²/4>0`

for `f≠0`, contradicting `−1`. This is a direct algebraic proof of the knot sensitivity of the pairing, without importing a signature theorem or the Jones values.

The accompanying exact checker verifies the presentation-side identities, Hermitian identity, generator residue, and sign reversal symbolically over Q(u).

## 5. Exact limit: this enriched datum cannot determine Jones

If `Δ_K=1`, the square Alexander presentation is invertible over Λ, so

`A_K=0`, and consequently `β_K=0`.

Thus every Alexander-one knot has exactly the same `(A_K,β_K)` datum as the unknot, including all operations that factor through this module-with-pairing alone.

An explicit example is the eleven-crossing PD identified in the shared validation replay from the Knot Atlas K11n42 record. The source-derived PD is an external input and is not redistributed in this authored packet. The 874-byte replay fixture, which also includes the calibration input, has SHA-256 `8902d73feb07f44aa1bc13a39e29e2ac0a9a2957254ab78132b99799c8e8a266`. Replaying the published checker requires obtaining that external source input separately.

The computed Knot Atlas record identifies this as an orientation choice for the Kinoshita–Terasaka knot or its mirror, records `Δ=1`, and gives a nonconstant Jones polynomial

`−t⁴+2t³−2t²+2t+t⁻²−2t⁻³+2t⁻⁴−2t⁻⁵+t⁻⁶`,

for the hash-identified PD. The record warns that the named knot and its mirror occur under competing conventions; the independently replayed PD-defined knot removes that ambiguity. Either mirror also has Jones polynomial different from the unknot's `1`. [Computed primary data and diagram](https://katlas.org/wiki/K11n42).

The independent validation replay computes all 2,048 bracket states for this exact PD, obtains writhe `−1` and exactly the displayed source-normalized Jones polynomial, and computes a 10×10 Fox–Alexander cofactor determinant `−u⁵`. That determinant is a Laurent unit, proving `Δ=1`. The computation is calibrated against the supplied negative-trefoil PD. Its authored script and replay are retained in the shared validation deliverable. No copied database collection is included in this artifact.

Consequently there is no function of the isometry class `(A_K,β_K)` alone that gives the full Jones polynomial for every knot. This is stronger than the PASS1 unadorned-module counterexample because the proposed knot-sensitive pairing has now also been included. It remains a restriction on one classical enriched datum.

## 6. What has and has not been retained

- The construction is genuinely intrinsic local-system homology plus a secondary operation on the complement. It detects more than the Alexander polynomial or the module alone, as the trefoil/mirror computation proves.
- It is determined by classical Seifert/Alexander–Blanchfield data. It does not retain all knot topology; the Alexander-one example proves a loss relevant even to Jones.
- The four-particle nonminimal-neutral calculation supplies a natural filtration and exact groups. It does not prove every product, secondary operation, or Laurent-level extension on those configurations factors through Blanchfield data.
- No conclusion is drawn about arbitrary neutral particle numbers, higher-rank coefficients, the full peripheral chain complex over the nonabelian knot group, or all homological constructions.

## 7. Precise remaining step toward Jones

For the particular datum `(A_K,β_K)`, no choice of normalization, trace or polynomial variable can repair the missing Jones information: it is identical for the unknot and the explicit Alexander-one example. A viable extension must first add data or an operation that is nontrivial on such examples.

One concrete next family would replace the rank-one cyclic system by unitary higher-rank knot-group representations and retain their relative Poincaré complexes and twisted Blanchfield pairings. These are genuine known constructions, rather than formal labels: Powell's symmetric-chain-complex construction supplies a pairing under explicit unitarity and acyclicity hypotheses. [Primary manuscript](https://arxiv.org/abs/1605.06800). However, a single arbitrary representation is extra input; using a whole representation groupoid requires natural comparison under changes of peripheral marking and bases.

The companion `HIGHER_RANK_FINITE_FIELD_TEST.md` makes one such escape completely concrete: a natural finite family of parabolic SL₂(F₇) local systems, with an exactly replayed nonabelian Kinoshita–Terasaka member, distinguishes that Alexander-one knot from the unknot by Laurent homology orders. It still supplies no Jones extraction.

The missing Jones bridge is then exact: define from the knot pair a specified class/operation in that enriched family and prove its contraction equals the source-normalized Jones polynomial, without selecting representations or weights by looking at Jones. Nothing in this approach supplies such a contraction, and no quantum trace or summation measure has been silently assumed. The accepted transported CFT/WRT theorem from PASS1 remains valid and separate.

**Disposition: explicit knot-sensitive intrinsic enrichment and exact scope boundary, not a full Jones construction.**
