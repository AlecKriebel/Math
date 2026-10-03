# Attempt 5/5: finite-cover reconstruction, and the remaining constructive obstruction

**Corrected release, 3 October 2026.** This revises substantive attempt 5/5 after independent review; it is not a new attempt. All claims use [DATA_CONVENTIONS.md](DATA_CONVENTIONS.md). The frozen original remains unchanged. See [CHANGE_MAP.md](CHANGE_MAP.md) and the full audits in `audits/`.

Date: 2026-10-03 UTC. The last substantive attempt tries to recover the explicit presentation equivalence from constructive classifying-topos semantics, instead of imposing the stronger all-pretoposes premise of attempt 4. The original question is not fully resolved by this attempt.

## 1. Conditional reconstruction with a uniform effective interface

Suppose E is a presented sheaf category on a supplied small finitary coherent site C. Assume the following interface for the objects and arrows under consideration. Every operation acts on raw presentation and equality evidence as in DATA_CONVENTIONS; bare classical existence assertions are insufficient.

1. A subcanonical finite-limit/coherent Yoneda functor y:C→E is supplied on presentations, with preservation comparisons and an effective inverse on hom-setoids. For literal Yoneda this lift evaluates a natural transformation y(c)→y(d) at id_c. For setoid-valued presentations it is an extensional operation on presented elements, not selection from quotient classes. Faithfulness reflects equality witnesses.
2. The section cover of X is supplied, indexed by the dependent sum of site-object records c and section records s in X(c). The smallness of this index family and its action on equality evidence are included. A finite-subcover operation takes the particular section cover of each relevant coherent object and returns a finite subfamily with cover and local-surjectivity evidence. More generally the operation applies to given covers where used below.
3. For every supplied finite jointly covering family of representables into a relevant target X, each kernel component y(c_i)×_X y(c_j) has the corresponding compactness/finite-subcover operation, uniformly with its pullback and equality data. This applies to any such supplied covering family, including the combined family used for arrow graphs below. No general assertion that all subobjects are compact is assumed.
4. Specified pullbacks, images, finite unions, finite sums, effective quotients and their factorization operations are available, with local-surjectivity evidence for covers. Yoneda preserves the coherent operations used in C. Equality and factorization reflection through its hom-lifts supplies C equality records and, for a syntactic C, the required derivation records for subobject inclusions. These operations are uniform on the supplied records and respect their equality evidence.

Choose the output of the finite-cover operation once for each object record under consideration. The construction of an arrow uses those assigned source and target covers. Its outputs and equality witnesses must form the extensional object/arrow operations of the interface, not a separate bare assertion that some finite presentation exists for each object.

### Object reconstruction

Apply the finite-subcover operation to X's section cover. It returns a finite family

    e_i:y(c_i)→X

whose copairing e is regular epic, with its evidence. This extracts a finite witness from a particular cover; it is not a choice of representatives of X's elements.

For each i,j, form the kernel component

    R_ij := y(c_i) ×_X y(c_j) → y(c_i×c_j).

Clause 3 supplies compactness for this component. Cover R_ij by its sections and use its finite-subcover operation to obtain finitely many y(d_k)→R_ij. Their composites into y(c_i×c_j) lift effectively to C arrows d_k→c_i×c_j. Take their images and finite union in C, obtaining a subobject r_ij. Preservation of images/unions and the cover of R_ij identify y(r_ij) with R_ij, with the displayed comparison data.

The kernel's reflexivity, symmetry and transitivity transfer through the finite constructions and the effective hom-lifts. For a syntactic C, subobject inclusions are represented by their factorization maps and derivation witnesses; no test for theoremhood occurs. Thus e presents X as the effective quotient of the finite sum of y(c_i) by the definable equivalence matrix r_ij. The quotient universal operation gives the comparison and inverse comparison to X, without a section of e.

If C is the coherent syntactic category of S, each c_i is an S-formula in an old-sort context, and r_ij is an S-definable relation. This is exactly a proof-carrying object of P_S from Attempt 1. The formula and its proof records are extracted from the raw syntactic-category output, with no inhabited-sort condition.

### Graph compactness from a combined finite cover

Let f:X→Y be supplied, and use the assigned finite covers e_i:y(c_i)→X and d_j:y(b_j)→Y. Consider the finite family into Y consisting of ALL f e_i and ALL d_j. It covers Y because its d_j subfamily already does. The cross kernel component between f e_i and d_j is

    G_ij = y(c_i) ×_Y y(b_j).

It is precisely the pullback of the graph of f along e_i×d_j. Therefore clause 3 supplies compactness for G_ij. This inference uses a kernel component of a supplied finite cover, not an unsupported claim about arbitrary graph subobjects.

Apply the section-cover and finite-subcover operations to G_ij. Compose its finite representable cover into y(c_i×b_j), lift to C arrows using the effective Yoneda inverse, and take their images and finite union in C. As in the object argument this gives a finite definable graph matrix g_ij with explicit comparison to G_ij.

Totality follows locally: for a source representative u, the Y-cover supplies, in a branch j, a v with d_j(v)=f(e_i(u)). Functionality modulo Y's kernel follows because two such representatives have the same image. Source and target saturation follow because equality of those images preserves that equation. For composition, a local intermediate representative exists by the intermediate cover, yielding exactly the existential relational composition of Attempt 1. Identity gives the source kernel. These are local witness arguments, with no chosen section.

Faithfulness and the hom-lift operations transfer the corresponding equalities and subobject factorizations into C, hence provide the equality and admissibility derivations for the matrices when C is syntactic. The uniform assignments give functors on raw presentation records, not only a map on isomorphism classes. Applied to the two sides of a supplied semantic comparison, and with its preservation/inverse data transported through the same interface, they yield the explicit comparison functors and natural isomorphisms required in corrected Attempt 3. The interface and comparison data are hypotheses here, not consequences already established for the original premise.

If an X-cover is empty, X is initial and the matrix has no source branches. If a Y-cover is empty, Y is initial; the supplied f and local-cover evidence yield the requisite empty source sequents. The combined-family argument still applies and never asks for an element of either object.

## 2. Why the finitary topology is promising

There is a constructive-looking mechanism for hypothesis 2 on representables. To cover y(c), evaluate a covering epimorphism family at the identity section of c. Local surjectivity supplies a covering family of c and local preimages. If the topology is presented by finite covering families, only finitely many local preimages and family indices occur. They yield a finite subcover of y(c).

There is also a finite-presentation approach to sheafification. For a presheaf F and object c, a candidate for F-plus(c) is a matching family of sections on a specified finite covering family of c. Equate two such records if they agree on a common covering refinement. Pullbacks and composition of finite covers give finite common-refinement data. This suggests a sheafification built from sets of finite records and quotient setoids, rather than quantifying over a powerset of sieves.

However, neither observation alone proves everything needed. One must verify extensionality and restriction maps for these matching-family quotients, the plus-plus sheaf property and its universal property, the precise local-surjectivity criterion used above, preservation of the relevant coherence data by a supplied equivalence, and uniform extraction of the finite presentation/graph witnesses. The fact that each step has a plausible finite description does not license treating this collection of obligations as an already proved constructive comparison theorem.

In particular, “X is categorically compact” as a bare metatheoretic proposition is not automatically the supplied finite-subcover operation used in §1. A constructive reading of a proof of compactness can contain that operation, but a classical theorem assertion need not. The attempted route therefore narrows the gap to concrete cover/refinement data; it does not close it.

## 3. An actual choice obstruction to a tempting shortcut

Let P be any proposition for which the following two-element setoid relation is permitted. On the discrete set {0,1}, define

  a E_P b  iff  (a=b) or P.

This is an equivalence relation intuitionistically. Let Q be the quotient setoid and q:{0,1}→Q the quotient map. Suppose there were an extensional section s:Q→{0,1} with q s=id_Q.

Set a=s(q0) and b=s(q1). Equality on the two-element codomain is decidable, so either a=b or a differs from b.

- If a=b, the section equation gives q0=q(a)=q(b)=q1. Thus E_P(0,1), and since 0 differs from 1, P follows.
- If a differs from b, then P is impossible: P would imply q0=q1 and extensionality of s would force a=b.

Hence existence of such a section implies P or not P. A theorem supplying sections for every such quotient would imply excluded middle for all the admitted P. The quotient itself causes no problem; it is the extensional representative-selection function that does.

This rules out a shortcut that interprets effective quotient sorts by silently choosing representatives. It also warns against extracting inverse functors or common skeletons by a representative-choice argument. It does not refute the original Morita claim: none of the matrix constructions in attempts 1–4 chooses such sections, and a constructive proof of the missing cover theorem might avoid them too.

## 4. Final mathematical result after five attempts

The following conditional constructive results have been developed in written detail:

- finite proof-carrying quotient presentations form a presented pretopos, with empty sorts and nullary constructions;
- finite definition chains admit conservative coherent proof translations and a uniformly finite-stage normal-form library;
- finite zigzags normalize to common spans after explicit renaming;
- actual inverse equivalence data on presented pretoposes yield a finite common definitional extension;
- pseudonatural equivalence of model semantics in every presented constructive pretopos yields those inverse data by generic-model evaluation;
- an explicit uniform finite-cover/compact-kernel interface, with effective Yoneda hom-lifts and equality evidence, suffices to recover finite object and graph presentations in the stated constructive coherent sheaf environment.

The full proof audit and independent supplement pass these informal conditional constructions with the explicit repairs now incorporated; this corrected release awaits a narrow verification that the repairs are faithfully integrated. Their categorical content is closely related to established completion and Morita theory; no priority or publication-level novelty claim is made.

What is **not** established is that the original source's intended constructive Morita premise supplies the all-pretoposes semantic data of attempt 4 or the sheaf/finite-cover interface of this attempt. The source gives a Bishop-style external setting but does not formalize that premise enough to justify silently substituting either one. A complete constructive classifying-topos comparison has not been proved here, and no counterexample to the original claim has been found.

Accordingly the original-scope outcome is **unresolved after 5/5 substantive attempts**, with the ordinary coherent theorem credited as prior work and a precise conditional constructive bridge recorded. The prior zero-turn packet remains a preparation-stage artifact whose original-scope closure was rejected by the independent applicability gate. Neither its 0/5 count nor its proposed closure is overwritten retroactively.
