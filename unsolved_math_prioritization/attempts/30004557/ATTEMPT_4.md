# Attempt 4/5: reconstructing a common extension from indexed constructive semantics

**Corrected release, 3 October 2026.** This revises substantive attempt 4/5 after independent review; it is not a new attempt. All claims use [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The frozen original remains unchanged. See [CHANGE_MAP.md](CHANGE_MAP.md) and the full audits in `audits/`.

Date: 2026-10-03 UTC. This attempt replaces a supplied syntactic-category equivalence by a semantic premise and tests exactly where that premise exceeds what the source explicitly specifies.

## 1. A constructive universal property

Let E be a locally small presented pretopos with specified finite limits, images, finite disjoint coproducts and effective quotients, including their universal-property operations. A pretopos functor acts on the raw presentation and equality records and supplies these structure-preservation comparisons and their evidence, in the sense of DATA_CONVENTIONS. Merely asserting preservation or fullness on quotient classes does not supply the operations used below. These data assumptions avoid selecting operations from bare existence assertions for a family of objects.

Given a T-model M in E, interpret each coherent formula in an old-sort context by a subobject of the context product. Conjunction is intersection, disjunction is finite union and existential quantification is image. For an object A=(sum_i phi_i)/E_A of P_T, take the finite sum of the interpreted carriers and its specified effective quotient by the interpreted relation E_A. This is a formula-recursive assignment on presentations.

For an arrow matrix R:A→B, take the subobject it defines on the two tagged carriers, map it into the product of the two quotients, and take its image. Saturation proves that this relation on quotient objects is independent of representatives. Totality makes its first projection regular epic. Functionality makes that projection monic. It is therefore invertible, and its other projection gives a unique arrow from the interpretation of A to that of B.

The inverse in this step does not use a global splitting axiom. If e:R→A is monic and a specified coequalizer of its kernel pair, its kernel pair is diagonal. The identity on R coequalizes it. The coequalizer factorization operation returns g:A→R with ge=id_R; epimorphy then gives eg=id_A. Thus the inverse is constructed from the existing universal-property data.

Interpreting the identity and composition matrices from attempt 1 gives the identity and composite arrows by uniqueness. Interpreting their finite-limit/image/sum/quotient formulas shows that the resulting functor Mbar:P_T→E is a pretopos functor.

A homomorphism h:M→N of T-models extends uniquely to a natural transformation Mbar→Nbar. On tuple products it is componentwise; on formula subobjects it is induced by preservation of coherent formulas; on finite sums it is a copairing; on quotients it descends by the quotient universal property. The covering maps onto the presentation quotients show uniqueness, since equal arrows after these regular epimorphisms are equal. Naturality holds first for graph matrices, then for every arrow represented by one.

Conversely, restricting a pretopos functor P_T→E to the generic T-model gives a T-model. The reconstruction just given is naturally isomorphic to the original functor because the latter preserves each finite presentation. Similarly, natural transformations are determined by restriction. We obtain an explicitly implemented equivalence

  Pretopos(P_T,E) ≃ Mod_T(E),

natural, up to the canonical comparison isomorphisms, in pretopos functors E→E'. No classifying Grothendieck topos has been constructed or assumed.

## 2. An independently semantic sufficient hypothesis

Consider the following hypothesis, stated in model language rather than by declaring two syntactic categories equivalent:

  For every presented constructive pretopos E, there is a supplied equivalence
  alpha_E:Mod_T(E)→Mod_S(E), with a supplied inverse beta_E and natural
  inverse isomorphisms. These equivalences commute pseudonaturally with
  transport of models along pretopos functors.

The word “supplied” is part of the constructive data requirement. No set of all pretoposes is postulated: the hypothesis can be a schematic construction valid for each such E and each functor. For the proof below only two particular E's and two particular functors are eventually used.

Let U_T and U_S be the generic models in P_T and P_S. The S-model alpha_(P_T)(U_T) corresponds by §1 to a functor

  F:P_S→P_T.

The T-model beta_(P_S)(U_S) similarly gives

  G:P_T→P_S.

Apply pseudonaturality of alpha to G. There is a model isomorphism

  (G F)_* U_S ≅ G_* alpha_(P_T)(U_T)
                 ≅ alpha_(P_S)(G_* U_T)
                 ≅ alpha_(P_S) beta_(P_S)(U_S)
                 ≅ U_S.

The fully faithful restriction equivalence in §1 lifts this to an explicit natural isomorphism GF≅id_(P_S). Apply pseudonaturality of beta to F to obtain FG≅id_(P_T). These are operations on supplied model isomorphisms and presentation data; no inverse functor is selected from essential surjectivity.

The corrected Attempt 3 now constructs a common finite-chain extension of T and S, with its explicit original-symbol graph axioms, normalized hom-lifts, and both scaffold comparison equations. No triangle identities need be postulated for the two recovered natural isomorphisms. This proves the reverse implication for the displayed indexed-semantics hypothesis. The forward implication follows by canonical expansion of models under the source's generators, with quotient-map descent on homomorphisms. Because pretopos functors preserve the constructions, these expansions are pseudonatural. Thus the source's generators and this precise constructive indexed-semantics relation coincide under the data assumptions given above.

## 3. Why this is substantial progress but not an unconditional answer

The sufficient hypothesis is not syntactic Morita equivalence in disguise: it speaks of model categories in independent target categories and their change of ambient category. The reconstruction proves the connection. It is a natural constructive categorical notion of Morita equivalence.

Nevertheless the original workshop sentence does not state that the intended constructive environments range over all presented pretoposes, nor that this particular pseudonatural data package is given. The usual topological version speaks of Grothendieck toposes. A small presented pretopos P_T is generally not itself a Grothendieck topos. Consequently the crucial evaluation alpha_(P_T)(U_T) cannot be made from a premise quantified only over Grothendieck toposes.

Classically one uses the coherent classifying topos, its generic model and recovery of the coherent/pretopos presentation. The earlier source gate specifically held the constructive justification of that step. The present attempt avoids it by enlarging the range of test categories, which makes the semantic hypothesis stronger. It does not prove that the original constructive premise implies the enlarged one.

Nor does a bare equivalence of Bishop-set model categories suffice as the input to this proof. That gives no value of alpha on P_T and no change-of-environment naturality. Same models or same rules alone do not furnish the generic-model argument.

## Result of attempt 4

A conditional constructive finite-presentation theorem is obtained under the supplied raw-operation and pseudonatural-equivalence hypotheses for model semantics in presented pretoposes. The remaining original-scope issue is now narrower and concrete: connect the source-intended constructive semantic Morita relation to these test categories, or reconstruct the required presented-pretopos equivalence from its allowed constructive classifying-topos semantics without unaccounted choice or impredicative constructions. No answer to that step has yet been established.
