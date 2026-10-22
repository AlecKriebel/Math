# Approach 3: a complete all-defect-pair model family

## Aim and scope

Prove the full local square-root formula for the standard group realizing an arbitrary index-two pair of 2-groups. This covers all abstract pairs, but only these particular blocks.

Let D be an index-two subgroup of the finite 2-group E, let A=⟨a⟩≅C₃, and let

G=A⋊E,

where D centralizes A and E\D inverts A. Let θ be a nontrivial linear character of A. The orbit {θ,bar θ} determines a unique real nonprincipal 2-block B with defect pair (D,E) and one simple module. This is the standard realization in Sambale's papers; it is not a new realization theorem.

For completeness, D is a normal 2-subgroup and G/D≅S₃. The simple module over the nontrivial A-character orbit has dimension 2 and is unique in this block. The class {a,a⁻¹} is a real defect class with centralizer A×D and extended centralizer G, giving the claimed pair.

## Local block and projective character

Fix x∈D and put P=C_D(x), Q=C_E(x). Since A commutes with x,

H=C_G(x)=A⋊Q.

If Q>P, the local block over {θ,bar θ} is real with one simple module. Its unique projective indecomposable character is

Φ=Ind_A^H θ,

with values

Φ(1)=|Q|=2|P|,
Φ(a)=Φ(a⁻¹)=−|P|,
Φ(h)=0 for h∉A.

One way to verify projective indecomposability is to induce the simple projective kA-module θ. Its head contains the unique corresponding simple kH-module once, by Frobenius reciprocity; no other simple occurs. The character values follow from the ordinary induction formula.

If Q=P, H=A×P and the corresponding local block is nonreal. Each choice θ or bar θ has unique projective character Φ=Ind_A^H θ, equal to |P|θ on A and zero elsewhere. Both choices give the zero answer below.

## Roots lying in D

Write a root as y=a^i e, e∈E. If e∈D, then A and e commute, so y²=a^{2i}e². The equation y²=x∈D forces i=0. Thus y=e∈D.

Its centralizer contains A. Since Φ is supported on A and sums to zero on A,

⟨Φ_{C_G(y)},1⟩ = 0.

The subgroup D is normal in G, so y^H⊆D, and the right-hand intersection with E\D is empty. The formula holds.

## Roots outside D

Suppose e∈E\D. Then (a^i e)²=e². All three elements a^i e are conjugate under A, because inversion acts without nonidentity fixed points on C₃. Conjugation by A fixes x, so we can take y=e∈E\D without changing either side.

Necessarily e²=x and e∈Q. Hence Q>P and the real local formula for Φ applies. As e inverts A, its centralizer in G has no nonidentity element of A. Direct multiplication shows

C_G(e)=C_E(e)≤Q.

The character Φ is supported on A, so only the identity contributes to the inner product:

⟨Φ_{C_G(e)},1⟩ = |Q|/|C_E(e)|.

On the other hand, conjugating e by H=A⋊Q gives Q-conjugates in E and two additional A-translates for each of them. A nontrivial A-conjugation of any outside-D element does not stay in E. Consequently

e^H∩(E\D)=e^Q,

and its size is |Q:C_Q(e)|=|Q|/|C_E(e)|. This is exactly the left side.

## Outcome and limit

The proposed identity holds for every root, every subsection, and every pair D<E in this model family, including nonsplit extensions and nonreal local blocks. No assumption that D is abelian was used.

The missing general step is not the realization of possible pairs. The same abstract (D,E) does not itself provide a correspondence between an arbitrary block's orbit permutation modules and those in this model. The calculation therefore gives a large exact positive family, not a proof of the universal assertion.
