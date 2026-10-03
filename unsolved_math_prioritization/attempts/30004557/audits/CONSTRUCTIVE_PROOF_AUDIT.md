# Constructive Morita proof audit

Problem 30004557, rank 452. Audit date: 2026-10-03 UTC.

Frozen packet: `attempts_author_v1/AUTHOR_MANIFEST.json`, SHA-256 `6e9c9a13a7dffa99b3e790ab4de28fdd098e564b87b5d31bce79d819ddeca647`.

## Decision

**HOLD for a resolution of the original constructive Morita question. PASS for retaining the five-attempt packet with its original-scope disposition `unsolved`.** The missing implication from the source-intended semantic premise to the explicit comparison data remains missing. The packet correctly says so and supplies no counterexample to the original claim.

**The conditional mathematical constructions pass, with the precise data conventions and three presentation clarifications below.** No false finite-matrix identity, empty-sort failure, quotient section, common-skeleton choice, or unbounded-stage collapse was found. This is an informal mathematical audit, not a proof-assistant certificate or a validation in every possible formal interpretation of Bishop mathematics.

The shared-language step in Attempt 3 must be read as an explicit coherent diagram presentation. The words “with their generic interpretations” alone are not axioms. Before quoting its theorem independently, spell out the old-symbol graph axioms and the comparison equations for both scaffold families. Section 5 below supplies the required specification and checks why it works. Likewise, the sheaf lemma needs an effective Yoneda hom-lift and its stated uniform compactness interface; bare classical existence statements are insufficient. These are bounded clarifications of the conditional arguments, not a solution of the remaining semantic comparison.

## Evidence and integrity

All five attempts, RESULT, STATUS, attempt log, matrix controls, the verification program, and both the current and earlier manifests were inspected. All ten current manifest entries match their recorded SHA-256 and byte count. The current manifest itself matches the hash above. No frozen author file was edited.

The matrix program was inspected and rerun. It reproduces exactly 626 controls: 18 identity checks, 90 composition checks, 466 associativity checks, 34 equalizer-predicate checks, and 18 image/kernel checks. Its four objects have underlying carrier size at most two, including the empty carrier. These are finite-set checks of selected formulas. They do not prove a universal property, construct a syntactic category in a foundation, establish conservativity, implement an internal language, or reconstruct semantics.

This is a new proof audit, distinct from the earlier source-applicability audit. The earlier report and relevant local primary-source passage were consulted to keep the original scope and nullary conventions fixed. The ordinary Tsementzis result is not used as a substitute for the constructive arguments under audit. No remote write, external communication, source retrieval retry, or sixth author attempt was performed.

## 1 Required constructive data conventions

The conditional statements require the following common convention throughout.

1. Syntax, finite contexts, formula records, and finite proof records form sets in the working constructive framework. Signature and axiom families are supplied sets. If their equalities are setoid equalities, the syntax construction carries those equalities and their witnesses. Neither a decision procedure nor enumeration of theoremhood is required.
2. An admissible object, arrow, diagram, or sequent is a record containing its finite proof data. The collection is obtained from these records, not by a decision test for provability. Equality of arrow records is a setoid relation witnessed by derivations. The statement “small presented pretopos” refers to this presented/setoid category; it does not require first selecting a raw representative from every hom-equivalence class.
3. A construction or functor acts on the raw presentation records and on the supplied equality evidence. A preservation assertion supplies its universal-property comparisons and proofs. The inverse-functor data in Attempt 3 are actual functors and natural isomorphisms, with inverse components, rather than a bare essential-surjectivity proposition.
4. Finite products include the nullary product. Empty subsorts and empty finite sums are permitted. If empty sums are omitted as a primitive, the empty object is a false subsort of the terminal object.
5. A stage may introduce a set-indexed family of independent definitions, of unbounded finite arities and formula lengths. A finite number of stages is required globally. No conclusion about a finite-total-signature version follows from this convention.
6. Target pretoposes have specified finite-limit, image, finite-sum, and quotient operations, including factorization operations for their universal properties. Change-of-environment functors are pretopos functors, not merely regular or Barr-exact functors.

These conventions are substantial hypotheses. They are stated or directly intended in the packet, and must remain attached to any theorem extracted from it. The audit does not prove that a chosen formal foundation supplies every one of these data structures automatically.

## 2 Attempt 1 finite quotient presentations

**PASS under Section 1.**

The objects are finite tagged families of old coherent definable carriers with a proof-carrying equivalence matrix. Arrows are supported, saturated, total, functional matrices. Entrywise provable equivalence gives a hom-setoid; identities and existential matrix composition respect it. Saturation is essential: functionality alone would not support the same-representative equalizer and kernel formulas used later.

The composition proof uses only finite disjunction elimination and local existential elimination. Given two composite witnesses, source functionality relates the intermediate representatives; saturation transports the second relation, and its functionality identifies the outputs. This is not a choice of a witness uniformly over source elements. Associativity is finite reassociation of conjunction, disjunction and existential quantification.

The terminal presentation has one empty-context component; the initial presentation has none. Products are pair-indexed carrier products. The equalizer predicate

`D_i(x) = OR_j EXISTS y (R_ij(x,y) AND S_ij(x,y))`

is correct: equality of the two quotient values can be represented by the same target witness because both graphs are target-saturated. No witness is required in an unused summand.

The image predicate and kernel matrix are likewise correct. For a mono, equality of the two kernel-pair projections entails `K <= E`. The reversed matrix from the image is then total and functional modulo E, and is an explicit inverse. This establishes the claimed description of all subobjects without choosing a subobject representative globally.

One short regularity link should be made explicit when presenting the proof separately. A locally surjective matrix R has kernel matrix K. Factor R through the quotient with relation K; the reverse matrix is then functional modulo K and gives an isomorphism of that quotient with the target. Consequently R is the coequalizer of its kernel pair. Together with the stated local-witness pullback argument, this proves pullback-stable regular epimorphisms. The packet's quotient and image calculations supply this link; no additional choice principle is needed.

For an internal equivalence relation, the image construction produces an invariant matrix H containing E. Replacing E by H produces its effective quotient. Coequalizing H is precisely the extra source saturation needed to descend an arrow. Again descent constructs a graph, not an elementwise section of the quotient map.

Concatenation with false cross blocks gives disjoint sums. For an arrow into a sum, the two image predicates in its source are disjoint and cover it; their sum reconstructs the source. This proves stability/extensivity rather than just a coproduct universal property.

No old empty sort becomes inhabited. The new terminal sort is a nullary product, not an element of an old sort. Contradictory theories and empty context-tag families cause no exception to the formulas.

## 3 Attempt 2 conservativity and finite stages

**PASS under Section 1.**

The translation correctly retains each context support. Function terms are replaced by their total functional graphs; invariance allows local quotient witnesses to be changed. Existential quantification is a finite disjunction of branch-local existential formulas. Moving all those witnesses outside the disjunction would be wrong with empty sorts, but the packet does not do so.

For a supplied finite proof, the translation recursively produces finite old-language proofs. Old sequents translate back to themselves under trivial presentations. This gives syntactic conservativity without Set-completeness or a model-selection argument. The availability of admissibility derivations for every definition is necessary and is explicitly included.

The five stages really are globally bounded: old-context products; old-formula subsorts; finite sums of those carriers; their specified quotients; graph and predicate names on the quotients. Stage 4 relations can be written in the stage-3 language using finite branch formulas. Stage 5 functions must use those expanded graph formulas directly; they need not depend on a graph predicate newly added in the same stage. Thus there is no hidden extra dependency or infinite-height argument.

All admissibility proofs can index fresh copies. There is no selection of one proof for each provable assertion, no common skeleton, and no test for whether an arbitrary formula is admissible. Adding infinitely many records in a stage is harmless only under the stated set-indexed-stage convention.

The seven-stage reconstruction of a translated finite extension is correctly limited: it gives a definitional presentation of the translated generic data, not yet a common extension over the original expanded theory. Attempt 3 is still needed for that comparison.

The finite-zigzag amalgamation is valid. Two finite extensions over the same base can be copied with disjoint new tags, and each sequence of definitions can be repeated over the other. At a reversed edge, chains concatenate. The construction keeps the shared base fixed and records endpoint renamings. It does not apply to an arbitrary infinite zigzag.

## 4 Attempt 3 two copies instead of a skeleton

**PASS for the two-copy categorical construction.**

Let P and Q be the presented pretoposes, with F:Q to P and G:P to Q and supplied natural inverse isomorphisms. The category with two object copies and homs inherited through H into P is a legitimate small presented category. H has a literal P-copy inverse and explicit identity-graph comparison on the Q-copy. This avoids skeleton selection.

The formula `K(r) = theta_Y G(r) theta_X^-1` is correctly typed and functorial. On an arrow F(f) in the Q-copy it is f by naturality of the supplied isomorphism GF to the identity. Its comparison with GH is theta. Transporting chosen operations from P gives the required pretopos structure and comparisons.

The two supplied natural isomorphisms need not initially satisfy adjoint-equivalence triangle identities. This does not invalidate the construction, but naive hom-lifting formulas may otherwise miss a conjugation. For completeness, write delta:FG to id_P and epsilon:GF to id_Q. For each B in Q put

`a_B = F(epsilon_B) delta_(FB)^-1 : FB to FB`.

For r:FB to FB', a genuine F-hom-lift is

`epsilon_B' G(a_B'^-1 r a_B) epsilon_B^-1`.

Naturality of delta and epsilon proves that applying F returns exactly r in the hom-setoid. Faithfulness follows by applying G and conjugating with epsilon. This is a uniform formula on supplied data, not a use of choice. The analogous construction supplies the hom-lifts needed for K.

## 5 Attempt 3 common scaffold and syntactic descent

**PASS with the following explicit presentation clarification.** A bare interpreted signature or the assertion that its axioms are true in C is insufficient. The intended I(C) must contain the following data as actual coherent axiom schemas.

1. Equations for identities, composition, and equal arrows, indexed by their equality proof records.
2. Coherent axioms for the chosen finite-limit, image, union, disjoint-sum, and effective-quotient diagrams. Nonchosen presentation diagrams are connected to these by their named comparison isomorphisms and equations.
3. For every original T or S predicate, an explicit equivalence with its designated mono/image predicate in the corresponding tuple object. For every original multi-ary function or constant, an explicit graph equivalence with its designated arrow out of that tuple object. Product projections and a local tuple witness express these equivalences in coherent syntax, including arity zero.
4. For each fresh library carrier and each C-object X, the comparison cover used below, written by its finite branch-local graph formula. A library sort is not literally a C-sort merely because they present isomorphic objects.

The original-symbol requirements in item 3 are essential. For example, if an original unary predicate R and the predicate naming its C-subobject are left unrelated, one can vary R in a model of the structural diagram axioms. The assertion that original formulas denote their designated subobjects then fails. The packet's statements that the original symbols retain their generic interpretations and that atomic predicates are designated subobject names should be expanded into these axioms, rather than cited without this interpretation.

With those axioms, the induction on original coherent formulas is valid: intersections represent conjunction, finite unions disjunction, and images existential quantification. Graph formulas handle function terms. Each C-object then has, internally to I(C), its T-presentation and its S-presentation, with specified covers and kernels. This is syntactic descent proved by coherent derivations, not an appeal to truth in a particular model.

Here is the crucial shared-scaffold check. Keep disjoint T and S auxiliary libraries. For X, take the S-library quotient q:U to Q_X^S and the I(C)-derived cover c:U to X, with the same kernel. If the literal U is a fresh library sort, construct c by its branch graphs using coordinates, the named formula-subobject comparisons and the C-arrow names. Its existence does not follow just from a change of notation.

The formula

`B_X(x,z) = EXISTS u (c(u)=x AND q(u)=z)`

is total both ways because both maps cover. It is single-valued both ways because their kernels coincide. The resulting unique-function graph supplies a canonical isomorphism X to Q_X^S. For a sum, write the displayed formula as the finite disjunction of its branch graphs. No arbitrary choice of an isomorphism is involved.

In one endpoint construction a copy projection X to Q_X^T is already present; in the other it is added by this canonical graph. For every copy projection, include the comparison equation with its presentation cover and quotient. These equations show that the projection supplied by a product-copy definition is the same canonical comparison used from the other side. The original-symbol graph induction then proves that every already present C-function and relation satisfies its opposite-side definition.

Thus the theory with I(C), both libraries, both comparison families and these equations is obtained by allowed definitions from each endpoint construction. One has not merely asserted an arbitrary isomorphism between old sorts, and one has not redefined an already present sort. All new maps use a bounded number of graph-name stages after the two five-stage libraries. The construction is globally finite-stage.

This check supports the conditional common-extension theorem. It also identifies exactly what must accompany it in a standalone presentation; without items 3 and 4 and the comparison equations, the written shared-language shortcut would be under-specified.

## 6 Attempt 4 generic-model reconstruction

**PASS under its explicitly stronger indexed-semantics hypothesis and the clarified Attempt 3.**

Interpretation of an object presentation in a specified pretopos E is formula-recursive. The image of an arrow graph on the quotient objects is a total single-valued relation. Its first projection is regular epic and monic. Its inverse is obtained from the specified coequalizer factorization, as the packet explains; no quotient-map section is assumed.

Homomorphisms preserve coherent formulas. They induce maps on tuple and formula carriers, then on sums and quotients by descent. Naturality for graph matrices follows from preservation of their defining formulas. Uniqueness follows from mono inclusions and the presentation covers. This gives the stated fully faithful restriction equivalence between pretopos functors P_T to E and T-models in E, including noninvertible model homomorphisms.

An arbitrary natural transformation between the functors is determined on the generic sorts: projections determine its tuple components, monos its formula components, coproduct injections its sum components, and regular epimorphisms its quotient components. Thus full faithfulness here is not merely a claim about isomorphism classes of models.

Given supplied pseudonatural alpha and beta on the required presented pretoposes, generic-model evaluation yields F and G in the stated directions. Pseudonaturality at G identifies GF on the generic S-model with alpha beta, and full faithfulness of restriction lifts the supplied model isomorphism to GF isomorphic to the identity. The other side is symmetric. No essentially-surjective functor is turned into an inverse by selection.

It is enough to have the indicated evaluations and comparisons for the two generic pretoposes and resulting functors, but their existence cannot be inferred from a hypothesis only about Grothendieck toposes. A small pretopos is generally not such a topos. Equivalence of Bishop-set model categories alone likewise does not supply these components or pseudonaturality. The packet correctly leaves that implication unproved.

## 7 Attempt 5 finite-cover interface

**PASS as a conditional reconstruction lemma, with the effective interface kept explicit. HOLD as a derivation of that interface from the original semantic premise.**

The section cover of a coherent object X, followed by the supplied finite-subcover operation, gives a finite representable cover. The assumed compactness operation for the kernel components lets one cover each component by finitely many representables. Full faithfulness of Yoneda lifts their composites to C-arrows; coherent images and finite unions in C produce a definable subobject whose image is exactly the kernel component. The effective quotient is then X.

The hom-lifting in this argument must be an operation on presentations. For a literal subcanonical Yoneda embedding it is supplied by evaluation at the identity. If “fully faithful” has only been given as an unimplemented existence assertion on quotient hom-classes, write down this evaluator or include effective hom-lifts in the interface. The later phrase “uniform implementation” is material: independent bare existence assertions for every object and arrow do not themselves supply the functors required by Attempt 3.

There is a precise way to justify the compactness of graph pullbacks, which is compressed in the packet. Given finite covers e_i:y(c_i) to X and d_j:y(b_j) to Y and f:X to Y, use the combined finite cover of Y consisting of all f e_i and all d_j. It covers because the d_j already do. The cross kernel components of this cover are exactly

`y(c_i) ×_Y y(b_j)`

with the first map f e_i. These are the graph matrix components. The stated compact-kernel interface therefore supplies their compactness; an arbitrary extra assertion that every subobject is compact is unnecessary. The resulting matrices inherit totality, functionality, saturation and composition from the graph and the covers.

Reflection through effective Yoneda hom-lifts and the syntactic subobject order provides the derivation witnesses for the resulting relations. Uniform operations on the covers, equality evidence and graph presentations are required to turn these individually presented objects and arrows into extensional functors.

The proposed finite-record plus construction is explicitly only a possible route. It does not establish sheafification, its universal property, local surjectivity, coherence preservation or the uniform finite-cover extraction. Nothing in the audit fills that gap or treats a classical compactness assertion as constructive data automatically.

## 8 Representative selection obstruction

**PASS.**

For each admitted proposition P, the relation on two elements given by equality or P is intuitionistically an equivalence relation. An extensional section of its quotient map takes the two quotient values to two elements a and b of the decidable two-element set. If a=b, the section equations imply that the two original quotient values agree, hence P. If a differs from b, extensionality rules out P. Thus existence of such a section implies P or not P.

This does not require a global function selecting the sections for all P: a theorem that every such quotient admits a section is already enough to obtain the corresponding excluded-middle schema. The qualification “admitted P” correctly avoids claiming comprehension beyond the chosen framework. It is not a counterexample to quotient existence, to the graph-descent constructions, or to the original Morita statement.

## 9 Final disposition and required wording

Retain five substantive author attempts and the `unsolved` original-scope disposition. Retain the credited ordinary coherent theorem as prior work. Do not replace the original premise by equivalence of presented pretoposes or by the stronger all-pretoposes indexed semantics without proving that replacement applies.

The useful audited conditional result is this: with the stated syntax and operation data, nullary and empty constructions, and set-indexed finite stages, explicit inverse equivalence data on the presented pretoposes yield a common finite definitional extension; the stronger supplied indexed-model equivalence yields those data. The common-language proof must include the graph and scaffold specifications in Section 5. The finite-cover result remains conditional on its effective sheaf interface.

The original problem is not certified solved, disproved, or globally open. The audit certifies the packet's narrower mathematical progress and its honest failure to close the specified semantic bridge. Publication or a final PR should carry these qualifications and the presentation clarifications, rather than an unqualified “constructive Morita theorem proved” label.
