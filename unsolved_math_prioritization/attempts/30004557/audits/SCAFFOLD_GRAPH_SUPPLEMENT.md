# Independent narrow check: common scaffolds and graph compactness

Date: 2026-10-03 UTC. This is a supplementary review of the frozen author packet and of Sections 4, 5 and 7 of `CONSTRUCTIVE_PROOF_AUDIT.md`. It is not an additional author attempt, an original-scope resolution, or a proof of the missing constructive semantic comparison.

## Verdict

The main audit's proposed repairs are mathematically valid under its explicit raw-presentation and effective-operation hypotheses. Attempt 3's original prose is under-specified as a standalone internal-language proof: its original-symbol links and two comparison families must be actual axiom schemas. Their omission is repairable by the lemma below; it does not furnish a counterexample to the conditional common-extension theorem. Attempt 5's graph step follows from precisely its existing compact-kernel hypothesis, by a combined finite cover. No additional assertion that all subobjects are compact is needed.

Nothing here establishes that the original semantic premise supplies those effective hypotheses. The original-scope disposition remains unresolved.

## 1. Effective inverse hom maps without triangle identities

Suppose raw-data functors F:Q→P and G:P→Q and natural isomorphisms δ:FG→id_P and ε:GF→id_Q are supplied, with their inverses and equality witnesses. No triangle identity is assumed. Set

    a_B = F(ε_B) δ_(FB)^(-1) : FB→FB.

For r:FB→FB', set t=a_B'^(-1) r a_B and define

    L_F(r)=ε_B' G(t) ε_B^(-1).

Naturality gives FG(t)=δ_(FB')^(-1) t δ_(FB), hence

    F(L_F(r))=a_B' t a_B^(-1)=r.

If F(h)=F(k), applying G and conjugating by ε gives h=k. Thus F is faithful and L_F is an actual inverse on hom-setoids. The displayed expressions also turn supplied equality evidence into equality evidence. Interchanging P,Q and δ,ε gives L_G. This verifies the main audit's formula; the naive expression ε_B' G(r) ε_B^(-1) can miss the a-conjugations.

For the two-copy category, K(r)=θ_Y G(r) θ_X^(-1). A hom-lift of s:KX→KY is simply

    L_K(s)=L_G(θ_Y^(-1) s θ_X),

viewed as an arrow HX→HY, hence an arrow X→Y in C. It is an inverse on hom-setoids. Consequently transported cones, images and quotient diagrams can be obtained on raw records without choosing representatives of hom-equivalence classes.

There is a useful normalization for S-presentation diagrams. Let J:Q→C be the Q-copy inclusion; KJ=id_Q. For X in C define ν_X:JKX→X to be the K-hom-lift of id_(KX). It is an isomorphism, natural in X, and K(ν_X)=id. Transporting an S-presentation through J and then ν_X therefore has exactly the desired K-image. Using an arbitrary supplied counit without this normalization could instead insert an unnoticed automorphism. This normalization uses only the hom-lift above.

## 2. Explicit original-symbol schemas

Fix an original T or S function f:σ_1×…×σ_n→τ. In C choose the tuple object A with projections π_i to the designated original sorts, and its interpreted arrow f̄:A→τ. The internal language must include the two coherent implications expressing

    f(x_1,…,x_n)=y  ↔  ∃t:A (∧_i π_i(t)=x_i ∧ f̄(t)=y).

For an original relation R of that arity, with designated subobject name P_R on A, include

    R(x_1,…,x_n)  ↔  ∃t:A (∧_i π_i(t)=x_i ∧ P_R(t)).

These are actual axioms, not merely an external interpretation of symbols. When n=0, A is the chosen terminal object and the empty conjunction is true. Its existence and uniqueness axioms make the same formulas work for constants and nullary predicates. A constant in an old sort is linked only if that constant was already an original symbol; no inhabitant is created in an arbitrary old sort.

For each mono m:M→A whose relation name occurs, include P_m(t)↔∃v:M(m(v)=t). Add equality, composition, and structural diagram schemas with their proof-record indices. A nonchosen presentation diagram is related to a chosen one by its named comparison isomorphism and equations.

These schemas yield, by finite structural induction, the interpretation of every original formula: equality and function graphs handle terms; pullback handles conjunction; finite union handles disjunction; image handles existential quantification. Each induction step produces a coherent derivation. The original theory's axioms follow from their supplied syntactic proof records and the corresponding subobject-inclusion diagrams.

The need for the original-symbol schemas is genuine. If a unary original predicate R and its alleged diagram predicate P_R are unrelated symbols, a model with an inhabited sort can change R while leaving the whole diagram structure fixed. The structural axioms alone do not prove R↔P_R. This diagnoses an omission in the literal axiom specification, not a counterexample after the specified repair.

## 3. Canonical comparison lemma

In coherent logic suppose c:U→X and q:U→Q are supplied covers, with a supplied common kernel relation:

    c(u)=c(v)  ↔  q(u)=q(v).

Define

    B(x,z) := ∃u:U (c(u)=x ∧ q(u)=z).

Then B is total in x: use the cover c locally, and take q(u). It is single-valued in z: two witnesses u,v have c(u)=c(v), so q(u)=q(v). It is total in z by the cover q, and single-valued in x by the reverse kernel implication. Thus a unique-function definition adds b:X→Q, and a further unique-function definition can add its inverse. Both composites are identities by the same witness calculation. Moreover b c=q.

Conversely, if a previously supplied isomorphism p:X→Q satisfies p c=q, then its graph is B. The forward implication uses a local c-preimage of x; the backward implication uses the equation p c=q. Therefore p=b, with a coherent derivation. This uniqueness clause is what identifies a pre-existing copy projection with the canonical comparison subsequently added from the other endpoint.

For a finite sum U of carriers U_i the formula is, explicitly,

    B(x,z) := OR_i ∃u:U_i (c_i(u)=x ∧ q_i(u)=z).

All witnesses remain inside their own disjunct. For an empty family, both covers make X and Q empty, the formula is false, and the totality/functionality sequents hold vacuously. No global choice and no section of c or q occurs.

## 4. The same upper theory from both endpoints

Retain disjoint fresh T- and S-library signatures. For each C-object X let Q_X^T and Q_X^S be the corresponding library quotients. Let U_X^T and U_X^S be their finite carrier sums. The internal-language induction and transported presentation diagrams supply covers c_X^T:U_X^T→X and c_X^S:U_X^S→X. Their kernels agree, respectively, with the kernels of the library quotient maps q_X^T and q_X^S.

The covers are not justified by calling a fresh library sort a C-sort. For each branch, construct its map to the named C formula-object by its coordinates and original-formula graph equivalence, then compose with the named presentation cover into X. The tuple uniqueness and subsort axioms prove this branch graph total and single-valued. The finite disjunction of branch graphs constructs c_X^T or c_X^S, with the common-kernel proof supplied by the quotient diagram. Existing graph predicates may be expanded directly in these formulas so that no same-stage dependency is required.

The shared upper signature includes both libraries, the C language, and BOTH comparison families

    p_X^T:X→Q_X^T,       p_X^S:X→Q_X^S.

Its axioms include both equations

    p_X^T c_X^T=q_X^T,   p_X^S c_X^S=q_X^S,

and assert each comparison is the isomorphism with the canonical graph of Section 3. If a comparison symbol is already the projection of the endpoint's unary-product copy definition, use the last clause of Section 3 to identify it with that graph; do not add a competing definition to an old symbol.

From the T endpoint, build its own library and C-copy/graph definitions as in the author construction. The defining matrix graphs prove I(C), including the explicit original T and S symbol schemas. Their coordinate computation also proves p_X^T c_X^T=q_X^T. Now build the S library using the S symbols already present. Add the S comparison family using Section 3. I(C)'s formula/arrow induction then proves the S-side definitions of every already present C symbol. These are theorems, not newly imposed restrictions on old symbols. Conversely the common axioms imply the original T-side copy and graph definitions by transport through p_X^T. Hence the common axiom presentation is logically equivalent to this allowed definitional extension of the T endpoint.

The same construction from S proves the symmetric statement, this time using Section 3 to add p_X^T. It is the same upper signature and same canonical comparison equations. An arbitrary unexplained isomorphism between the two presentations would not suffice for this identification.

The additional constructions use a fixed finite number of graph-name stages after the two bounded libraries: coordinate/branch maps, comparison graphs, and (if desired) inverse names. Inlining already specified graph formulas removes apparent dependencies. All schemas are indexed by existing syntax, diagram and proof records. No enumeration or decidability of derivability and no choice of one proof per theorem is used. The set-existence of these record families remains an explicit foundational hypothesis; this argument does not prove it in every interpretation of Bishop mathematics.

## 5. Graph compactness from the combined cover

Use precisely Attempt 5's effective interface: a supplied finite-subcover operation for the relevant coherent objects, including every kernel component of a supplied finite jointly covering family of representables; coherent finite-limit Yoneda with effective hom-lifts; images/unions; and effective quotients with local cover evidence.

Let e_i:y(c_i)→X and d_j:y(b_j)→Y be finite covers, and f:X→Y. The finite family into Y consisting of all f e_i and all d_j is jointly covering, because its d_j subfamily already covers Y. The cross kernel component indexed by f e_i and d_j is

    R_ij = y(c_i) ×_Y y(b_j).

It is exactly the pullback of the graph of f along e_i×d_j. The assumed compact-kernel operation therefore applies to R_ij. Cover R_ij by its sections and extract a finite representable subcover. Compose into y(c_i×b_j), lift the finite family of arrows effectively into C, and take their images and finite union in C. Preservation of these operations identifies the resulting definable subobject with R_ij. No general compactness claim about arbitrary subobjects has been used.

The matrix is total because for a local source representative u, the Y-cover supplies locally a v with d_j(v)=f(e_i(u)). It is functional modulo the Y kernel because any two such representatives have the same image. Source and target saturation follow because equality of their images preserves that equation. Composition is existential relational composition: a local representative of an intermediate value is supplied by the intermediate cover, not by a chosen section. Faithfulness and effective hom-lifting turn the corresponding commuting/factorization diagrams into the required C equality and derivation witnesses.

If one cover is empty, the same formulas remain correct. An empty X-cover means X is initial. An empty Y-cover means Y is initial, and the supplied map f and local-cover evidence give the necessary vacuity. The combined-family argument never demands an element of either object.

The section-cover indices form the dependent sum of the site's object records and the section sets. Its smallness, the finite-subcover operations, and their action on presentation/equality evidence must be part of the effective interface. For literal subcanonical Yoneda, a hom-lift is evaluation at the identity; if representable values are setoids, this means an extensional map on their presented elements, not selection from quotient classes. These requirements validate the conditional lemma but do not establish the missing sheaf-comparison theorem.

## Conclusion

The main audit's proposed clarifications pass this independent narrow check. The repair is explicit and bounded. No invalid graph-compactness inference remains once the combined cover is written down. No quotient representative, common skeleton, unproved triangle identity, inhabited-sort assumption, or per-symbol-depth substitute for a uniform finite stage is required.
