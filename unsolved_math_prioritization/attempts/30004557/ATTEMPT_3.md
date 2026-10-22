# Attempt 3/5, corrected: a common span from supplied pretopos equivalence

Date: 2026-10-03 UTC. This is a revision of the third substantive attempt after the full proof audit and independent supplement, not a sixth attempt. The frozen original remains unchanged. All claims include [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The corrections are mapped in [CHANGE_MAP.md](CHANGE_MAP.md); both full proof reviews are in `audits/`.

## Input and precise conditional target

Let P=P_T and Q=P_S be the proof-carrying presented pretoposes of Attempt 1. Suppose supplied pretopos functors F:Q→P and G:P→Q act extensionally on raw object, arrow and equality records, with structure-preservation comparisons and their proofs. Suppose natural isomorphisms δ:FG→id_P and ε:GF→id_Q, their inverse components, and naturality witnesses are supplied. No triangle identity is assumed. No inverse data are selected from a bare essential-surjectivity proposition.

The conditional target is a common finite definitional-extension span over T and a disjointly renamed S. Each stage permits a set-indexed family of independent definitions; nullary products and empty sorts are allowed. This does not identify the source-intended semantic premise with these data by definition.

## 1. Effective hom-lifts without triangle identities

For B in Q put

    a_B = F(ε_B) δ_(FB)^(-1) : FB→FB.

For r:FB→FB′ define t=a_B′^(-1) r a_B and

    L_F(r) = ε_B′ G(t) ε_B^(-1) : B→B′.

Naturality of δ gives FG(t)=δ_(FB′)^(-1) t δ_(FB). Applying F to the displayed lift therefore gives a_B′ t a_B^(-1)=r. If F(h)=F(k), applying G and conjugating by ε proves h=k. Consequently L_F is an inverse on hom-setoids. Each step acts on the supplied evidence, so equality of input records produces equality of output records. The naive lift ε_B′ G(r) ε_B^(-1) would give a_B′ r a_B^(-1), which need not be r without additional compatibility.

Interchanging P,Q and δ,ε gives an explicit lift for G: with

    b_A = G(δ_A) ε_(GA)^(-1) : GA→GA,
    L_G(s) = δ_A′ F(b_A′^(-1) s b_A) δ_A^(-1)

for s:GA→GA′, one has G(L_G(s))=s and G is faithful. These formulas provide operations; they do not choose hom representatives.

## 2. Two copies and a normalized comparison

Construct C with objects (0,A), A in P, and (1,B), B in Q. Put H(0,A)=A, H(1,B)=FB and

    Hom_C(X,Y) = Hom_P(HX,HY).

Identity, composition and hom equality are inherited literally from P. The functor H:C→P has the explicit P-copy inverse J_P, and the comparison J_P H X→X is the identity arrow on HX in this hom-setoid. Thus no skeleton is chosen.

Set K(0,A)=GA and K(1,B)=B. Let θ_X:GHX→KX be identity on the P-copy and ε_B on the Q-copy. Define

    K(r) = θ_Y G(r) θ_X^(-1).

Cancellation proves functoriality. Let J:Q→C be the Q-copy inclusion on objects and J(f)=F(f). Naturality of ε gives KJ=id_Q on hom-setoids. A lift of s:KX→KY is

    L_K(s) = L_G(θ_Y^(-1) s θ_X),

viewed as an arrow HX→HY and hence X→Y in C. It is an inverse on hom-setoids, by the already proved G-lift formula. In particular K is fully faithful with an actual inverse hom operation.

For X in C define ν_X:JKX→X to be L_K(id_(KX)), with the source and target just shown. Its inverse is the opposite-direction lift of the same identity. Applying K proves both inverse equations; faithfulness proves them in C. The same argument gives naturality of ν, and

    K(ν_X)=id_(KX).

This normalization matters: transporting an S-presentation through J and then ν_X gives exactly its desired K-image. An arbitrary supplied counit could insert an automorphism. The construction uses no unproved triangle identity.

Choose C's finite limits, images, sums and quotients by taking the specified operation in P and tagging the output with 0. Their factors are inherited through H. The supplied preservation data for G and the θ comparisons make K a pretopos functor. Conversely, diagrams transported from Q are equipped with named comparison isomorphisms to these chosen C diagrams. The hom-lifts provide all factors and equality evidence on raw records.

## 3. An actual coherent diagram theory

The language I(C) has a sort for each presented C object, unary function names for raw arrow records, and predicate names for presented subobjects. Original T and S sort names identify the designated objects in their respective copies. Keep their original finite-arity functions and predicates as well. Other C object sorts and arrow aliases receive fresh tags, including when different proof records denote the same arrow.

The following are actual axiom schemas, indexed by supplied diagram/equality proof records, not a truth oracle.

1. Identity, composition and equality equations for named arrows.
2. Coherent structural axioms for the chosen finite limits, images, finite unions, disjoint sums and effective quotients. A nonchosen presentation diagram is related to the chosen one by its named comparison isomorphisms and equations. Universal uniqueness is expressed as equality sequents; cover existence is expressed with local existential witnesses.
3. For each named mono m:M→A, the two implications for P_m(t) ↔ ∃v:M (m(v)=t).
4. The following original-symbol schemas, including every original T and S symbol.

For an original function f:σ_1×…×σ_n→τ, let A be the specified tuple object with projections π_i, and f̄:A→τ its designated C arrow. Include both coherent implications expressing

    f(x_1,…,x_n)=y ↔ ∃t:A (∧_i π_i(t)=x_i ∧ f̄(t)=y).

For an original n-ary relation R, with its designated subobject predicate P_R on A, include

    R(x_1,…,x_n) ↔ ∃t:A (∧_i π_i(t)=x_i ∧ P_R(t)).

For n=0 the tuple sort is terminal and the conjunction is true. Terminal existence and uniqueness make the same schemas apply to original constants and nullary predicates. This does not add a constant to an arbitrary old sort. A multi-ary function is linked to its unary tuple-arrow; mere external interpretation of its symbol would not impose that equation.

These schemas are essential. Structural diagrams alone would permit an unrelated original unary predicate to vary independently of its alleged designated subobject. The revised theory explicitly forbids that mismatch by its two implication axioms.

Interpret I(C) through H into P_T. Every C object, arrow and subobject has the explicit finite matrix presentation of Attempts 1–2. Each structural diagram axiom translates to the supplied T proof; the original-symbol axioms translate to the chosen graph/predicate interpretations. The five-stage T library, followed by needed object copies and graph definitions, consequently proves I(C). The same statement holds through K over S. On the Q-copy K is identity, with normalized transported presentation diagrams as in Section 2.

Conversely, a finite induction inside I(C) identifies each original coherent formula with its named C subobject: the displayed schemas handle atoms and function terms, pullback handles conjunction, finite union handles disjunction, and image handles existential quantification. Each step produces a coherent derivation. The original axioms follow from their proof-record-indexed subobject-inclusion diagrams. This is syntactic derivation, not the inference that axioms true in C must be derivable.

For each C object X, its T presentation is transported through J_P and the H-identity comparison; its S presentation is transported through J and ν_X. Include their quotient diagrams and named comparison maps in the schemas. They supply in I(C) the finite carrier formulas, covering families, kernels and arrow matrices in both original languages.

## 4. Literal fresh libraries and canonical comparison graphs

Retain disjoint T and S libraries L_T,L_S, each built in the five stages of Attempt 2. Their fresh sorts are not literally C sorts. Write Q_X^T and Q_X^S for the library quotients presenting a C object X, with finite carrier sums U_X^T,U_X^S and quotient maps q_X^T,q_X^S.

For either side A∈{T,S}, construct a map c_X^A:U_X^A→X as follows. On each fresh formula-carrier branch, coordinates and the original-formula equivalence of Section 3 give a total functional graph into the named C formula-object. Compose it with that branch's named presentation cover into X. Tuple uniqueness and subsort axioms prove that this is a function graph. The finite disjunction of branch graphs gives the map from the carrier sum. Graph predicates may be expanded directly, so simultaneous definitions need no same-stage name dependency.

The formula induction and the transported presentation diagram prove that c_X^A covers and has the same kernel as q_X^A. Nothing here rests on calling a fresh library sort a C sort. All map existence and kernel equalities have coherent derivations.

Use the following canonical comparison lemma. If c:U→X and q:U→Q cover and have the same kernel, put

    B(x,z) := ∃u:U (c(u)=x ∧ q(u)=z).

Cover c proves totality in x; its local preimage supplies z=q(u). Equal c-values of two witnesses imply equal q-values, proving uniqueness. Cover q and the reverse kernel implication prove the symmetric assertions. Thus a unique-function definition adds b:X→Q; the reverse graph may define b^(-1). The same witness calculation proves both inverse equations and bc=q. No section of either cover is chosen.

If an isomorphism p:X→Q is already supplied and satisfies pc=q, its graph equals B: one implication uses a local c-preimage, the other the equation pc=q. Therefore p=b by a coherent derivation. This identifies an existing copy projection with the canonical comparison without redefining an old symbol.

For a finite sum the formula is explicitly

    B(x,z) := OR_i ∃u:U_i (c_i(u)=x ∧ q_i(u)=z).

Each witness stays in its own disjunct. If the family is empty, both covers force X,Q empty and all totality/functionality sequents hold vacuously. No inhabited-sort assumption enters.

## 5. One upper theory, with both comparison families

The common upper signature includes I(C), both fresh libraries, and BOTH families

    p_X^T:X→Q_X^T,       p_X^S:X→Q_X^S.

Its axioms include the respective canonical graph definitions, isomorphism equations (with inverse names if used), and BOTH equations

    p_X^T c_X^T=q_X^T,   p_X^S c_X^S=q_X^S.

The graph formula for each comparison can inline the branch-map formulas. These are two specified canonical comparisons, not an unexplained isomorphism between old sorts.

Starting from T, first add L_T, then the C object copies and graph/predicate names as necessary. An original T sort is retained; a newly needed sort is a unary-product copy of its library presentation. Let D_T denote this finite extension. Its copy projection supplies p_X^T; for a retained original sort the corresponding canonical graph supplies it. The coordinate calculation proves p_X^T c_X^T=q_X^T. The definitions prove every I(C) schema, including the original S functions and predicates defined by their interpreted graphs.

Now add L_S using those S symbols. Add c_X^S by the branch formulas if map names are desired. Add p_X^S by the canonical comparison lemma. The same lemma identifies the pre-existing p_X^T with its required graph. The I(C) formula/arrow induction proves every opposite-side definition for C symbols already present in D_T; these are derived theorems, not newly imposed restrictions. Conversely the common axioms, transported through p_X^T, imply the T-side copy and graph definitions. Thus the one common axiom presentation is logically equivalent to an allowed definitional extension of D_T.

Starting from S, the symmetric construction first supplies p_X^S, then builds L_T and adds p_X^T by its canonical graph. Normalization of ν in Section 2 ensures the S-side diagrams have the intended interpretations; no counit twist is hidden. The construction obtains the same upper signature and both identical comparison equations. The canonical comparison uniqueness identifies the existing S-copy projection with its graph. Hence the same common theory is an allowed definitional extension from that endpoint as well.

There are globally finitely many stages: the two five-stage libraries, their object-copy and directly expanded arrow/predicate definitions, and a fixed finite number of coordinate/branch-map, comparison-map and optional inverse-map stages. Expand prior graph formulas to remove apparent same-stage dependencies. No minimum stage bound is asserted, but no iteration indexed by formula depth is required. Every family is indexed by the supplied set of syntax/diagram/proof records.

## Conditional result and remaining limitation

Under these explicit constructive presentation and operation hypotheses, supplied inverse pretopos-equivalence data P_T≃P_S yield a common finite chain of the source's definitions and standard sorts, including nullary and empty constructions. The proof selects neither quotient representatives nor a common skeleton, and imposes no triangle identities on the input.

Conversely, a supplied common span gives an explicit equivalence of presented pretoposes: translate presentations across each finite chain by Attempt 2, retain the generic expansions, and use the canonical graph comparisons for the natural inverse isomorphisms. This establishes the conditional syntactic/categorical characterization with precisely these data.

It does not prove that the source-intended constructive semantic Morita premise supplies the data. Attempt 4 gives a stronger sufficient indexed-model hypothesis; Attempt 5 isolates an effective sheaf interface. Neither is silently substituted for the original premise. Original-scope disposition remains unresolved after 5/5 substantive attempts.
