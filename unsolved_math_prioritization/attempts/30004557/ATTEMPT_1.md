# Attempt 1/5: an explicit constructive category of finite quotient presentations

**Corrected release, 3 October 2026.** This revises substantive attempt 1/5 after independent review; it is not a new attempt. All claims use [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The frozen original remains unchanged. See [CHANGE_MAP.md](CHANGE_MAP.md) and the full audits in `audits/`.

Date: 2026-10-03 UTC. This is the first substantive original attempt, after the frozen zero-turn applicability packet and its independent HOLD. The objective is to replace the unproved completion roadmap with finite, proof-carrying formulas that also work for empty sorts. No original-scope resolution is claimed at this turn.

## Constructive setting and input

Work informally with Bishop-style sets/setoids. Assume that a given many-sorted coherent theory T has a set of signature symbols with specified finite arities and a set of axiom presentations. Finite terms, formulas, and finite derivations form sets; evidence of axiom membership is included in a derivation. None of these sets must be finite or enumerable. No decision procedure for derivability is assumed. Functions on presented data come with extensionality proofs. When we say that T proves a sequent, its finite derivation is available as data.

These assumptions concern manipulation of the supplied syntax. They do not postulate a powerset, a set of all models, or a collection of all sheaves. Equality of arrows below is provable equivalence, with witnessing derivations, rather than a decision test or a chosen representative of an equivalence class.

## Objects and arrows

An object A is a finite list of coherent formulas in old-sort contexts, phi_i(x_i), together with coherent matrices E_ii'(x_i,x_i') and proofs that E is an equivalence relation on the tagged union of these definable carriers. Each E_ii' implies the two carrier formulas. Reflexivity is phi_i(x) entails E_ii(x,x); symmetry and transitivity run over the finitely many tags. Empty lists, empty contexts and contradictory carrier formulas are allowed. Think of A as (sum_i phi_i)/E, but do not assume a semantic quotient has already been constructed.

For B=(psi_j,F), an arrow R:A→B is a coherent matrix R_ij(x,y) with finite proof data for:

- support: R_ij(x,y) entails phi_i(x) and psi_j(y);
- saturation: E_ii'(x,x') and R_i'j'(x',y') and F_j'j(y',y) entail R_ij(x,y);
- totality: phi_i(x) entails the finite disjunction over j of exists y R_ij(x,y);
- functionality modulo F: R_ij(x,y) and R_ik(x,z) entail F_jk(y,z).

Two arrows are equal when their corresponding entries are T-provably equivalent. The proof objects establishing admissibility do not change arrow equality. In particular there is no requirement to choose one proof or one matrix representative globally.

The identity on A is E. Define composition by

  (S R)_ik(x,z) := disjunction_j exists y (R_ij(x,y) and S_jk(y,z)).

Support and saturation follow by conjunction elimination and the saturation proofs of R and S. For totality, use R-totality and branch on j; in that branch use S-totality. For functionality, two R-witnesses are F-related; saturation moves one S-witness to the other source representative, and S-functionality then gives equality in the target. The witness choices are local existential eliminations, never global selection functions. Associativity follows by associating the two existential witnesses and distributing the two finite disjunctions. Saturation and totality give E R=R=R F in the appropriate order. This constructs a category with hom-setoids.

## Terminal object, initial object, products and equalizers

The terminal object has a single empty context with carrier true and equality true. The unique arrow from A has entries phi_i(x). The initial object has zero components. The only matrix from it to any B is empty; an arrow into it exists precisely when every source carrier is contradictory. No old sort is made inhabited.

For A=(phi_i,E) and B=(psi_j,F), a product has components indexed by pairs (i,j), carriers phi_i(x) and psi_j(y), and equivalence matrix

  E_ii'(x,x') and F_jj'(y,y').

The two projections are the saturated coordinate relations. Given R:C→A and S:C→B, the pairing is R_ki(z,x) and S_kj(z,y). Its totality follows from the two totality proofs, and its functionality is coordinatewise. Every arrow with the specified projections equals this matrix, by saturation and functionality. This proves the product universal property, including empty factors.

For parallel R,S:A→B, define

  D_i(x) := disjunction_j exists y (R_ij(x,y) and S_ij(x,y)).

D is E-invariant. Equality of the two values of R and S permits use of the same target representative because both matrices are saturated under F. Restrict A's carriers to D_i and restrict E accordingly. Inclusion is the restricted E-matrix. An arrow H:C→A equalizing R and S has every image in D by totality of the common composite and saturation; hence H factors through the restriction. The factor is unique because the inclusion reflects E. Thus these presentations admit all finite limits.

## Images and subobjects

For R:A→B set

  I_j(y) := disjunction_i exists x R_ij(x,y).

This predicate is F-invariant. Restrict B to I to form Im(R), and factor R through it. The first arrow is surjective in the explicit sense that every I_j-representative is locally R-related to a source representative. The second is a mono. Pullback of this first arrow remains surjective: a pullback representative together with an I-witness supplies, locally, the required source witness. Again this is an existential argument, not a section of the map.

For completeness, why are these all subobjects? Define the kernel matrix of R by

  K_ii'(x,x') := disjunction_j exists y (R_ij(x,y) and R_i'j(x',y)).

This is the kernel pair obtained from the product/equalizer constructions. If R is mono, the two kernel-pair projections are equal, so K entails E. Therefore the converse relation R^op from Im(R) to A is functional modulo E. It is total by the definition of I and saturated by the axioms already proved. Its composites are the identity matrices. Thus every mono is isomorphic over B to an F-invariant coherent predicate restriction. This proof constructs the inverse matrix rather than extracting one from essential surjectivity.

The missing regularity link is explicit as follows. For a locally surjective matrix R:A→B, let K be its displayed kernel matrix. Factor R through the presentation with the same source carriers and relation K. The converse matrix is now total by local surjectivity and functional modulo K by the definition of K. The two composites are identity matrices, so this quotient presentation is explicitly isomorphic to B. The quotient universal property proved below therefore makes R the coequalizer of its kernel pair. The earlier local-witness pullback calculation makes these regular epimorphisms pullback-stable. This also justifies the regular epi–mono factorization asserted for every image. No section of R is obtained.

Finite unions of subobjects are obtained by entrywise disjunction of their invariant predicates; the empty union is false. Pullback preserves them because existential conjunction distributes over finite disjunction in coherent logic. Hence the category is coherent.

## Effective quotients

Let an internal equivalence relation on A be supplied as a mono into A×A together with reflexivity, symmetry and transitivity arrows. The preceding image construction turns this mono, explicitly and up to an isomorphism over A×A, into a coherent matrix H_ii'(x,x'). Its invariance under E×E and its internal equivalence proofs imply that H contains E and is a provable equivalence relation on the old tagged carrier.

Define A/H by retaining the phi_i and replacing E by H. The quotient map A→A/H is the matrix H. Its kernel pair is H, by the displayed matrix computation. If R:A→B coequalizes H, its entries are also H-saturated on the source: this follows by applying equality of the two composites from H and then functionality/saturation in B. The same matrix R therefore defines the unique arrow A/H→B factoring R. This proves effectiveness and the universal property with no representative selection. Stability under pullback follows from the local-surjectivity image argument.

## Disjoint stable finite coproducts

Concatenate the component lists for A and B. Use E on the first block, F on the second, and false in the two cross blocks. The injections are the corresponding diagonal matrices. Copairing is given by joining the two source-block arrow matrices. Its universal property is immediate entry by entry.

The pullbacks of the two injections have false intersection. For an arbitrary arrow R:C→A+B, its source carrier splits into the two invariant predicates obtained by existentially quantifying R over the first and second target blocks. Totality proves their union is all C; functionality and the false cross relation prove disjointness. The two inclusions reconstruct C as their coproduct. This supplies stability and extensivity, not just the universal property of a bare sum.

## Result of attempt 1

The displayed formula operations construct a small presented pretopos P_T with empty objects and empty old sorts allowed. Its operations are finite transformations of formulas and derivations. This avoids the inhabited-base-sort restriction in the accessible Tsementzis preprint, without asserting an inhabitant of any old sort.

This is a substantive constructive completion construction, not a claim that its formula-level content is historically new. The next obligations are: prove conservativity and a uniformly finite-stage presentation; derive a common extension from supplied equivalence data; and relate an independently specified constructive semantic Morita equivalence to this syntactic category. Merely defining Morita equivalence to be the desired conclusion would not answer the source question.

Terminology correction to the frozen preparation packet: functors preserving these constructions are called pretopos functors. A merely regular/Barr-exact functor need not preserve finite coproducts.
