# Turn1: a fixed-point-free cut isolates the Clo counterexample

30003659 / OWR-15958-006. 2026-10-02. **Original problem unresolved; one substantive proof-attempt turn completed.** The exact system and asymmetric transfer limitations are pinned in RULE_COMPARISON.md. This turn works in its conservative finite ordinary-induction core C. It does not rely on deep disjunction, strong induction, cyclic discharge, infinitary proofs or the invalidated completeness chain. No historical novelty claim.

## 1. Why this example matters

Kloibhofer2023 gives a valid sequent unprovable in the cyclic cut-free system Clo. That does not imply its unprovability in cut-free Kozen, whose ordinary induction is a different rule. We examine his exact formula as a concrete interface test for finite cut elimination.

For a propositional atom p set

    A=◇¬p,      B=□p=¬A,
    R(X,Y)=□X∨◇Y,
    V(X)=νy.□(p∧R(X,y)),
    U=νx.◇(¬p∧R(x,V(x))),      W=V(U).

The sequent Φ={U,W} is exactly Kloibhofer's sequent (his νx.φ,νy.ψ), with bound variables renamed as needed. Its validity and Clo-unprovability are **credited published results**, not new claims of this attempt.

## 2. Scoped result

There are finite **cut-free C proofs** of all four sequents

    {B,U},    {¬U,A},    {A,W},    {¬W,B}.                (1)

Thus each component of the example is cut-free provably equivalent to a simple modal formula: U↔A and W↔B, with each implication represented separately as a one-sided sequent. The final valid sequent {U,W} has a finite C+cut proof using **exactly one cut, on the fixed-point-free formula B=□p**.

This is a proof certificate, not a claim that the displayed cut is necessary. No cut-free proof of {U,W} or proof of its cut-free unprovability has been obtained in this turn. In particular, independently proved equivalences may not be composed by an unrecorded cut.

## 3. A reusable ordinary-induction constructor

Suppose π is a finite C proof of {X,B}, where X is any closed formula. The following finite construction T_X(π) proves {A,V(X)}.

1. Apply modal K with principal X to π, giving {□X,◇B}
2. Introduce disjunction, obtaining the singleton {R(X,B)}
3. Weaken by ¬p; combine with the atomic initial sequent {¬p,p} by conjunction to obtain {¬p,p∧R(X,B)}
4. Apply modal K with principal p∧R(X,B), obtaining {A,□(p∧R(X,B))}
5. Apply ordinary induction to the principal V(X), retaining side context {A}. The complement of that context is B, so the premise is exactly the sequent in step4

This is a literal rule-by-rule transformation. It does not use a semantic oracle or a generic monotonicity/composition rule. Closedness of X ensures capture-free substitution in V(X).

The initial sequent {A,B} has a modal K proof from {¬p,p}. Therefore T_A gives a finite C proof π0 of {A,V(A)}.

## 4. Deriving A→U, then B→W

Starting from π0:

1. Modal K with principal A gives {□A,◇V(A)}
2. Disjunction gives {R(A,V(A))}; weaken by p
3. Conjoin this with the atomic initial sequent {p,¬p}, obtaining {p,¬p∧R(A,V(A))}
4. Modal K with principal p gives {B,◇(¬p∧R(A,V(A)))}
5. Ordinary induction for U with side context {B} substitutes bar{B}=A into U's body, so its premise is exactly step4. Its conclusion is {B,U}

This proves the first sequent in(1) without cut. Apply the general constructor T_U to this existing finite proof; it gives {A,V(U)}={A,W}, the third sequent in(1), again without cut. The two ordinary inductions operate on finite closed formulas and finite derivations; no loop is being discharged.

## 5. The reverse implications

The least-fixed-point dual of U has the form

    ¬U = μx.□(p∨H(x))

for the explicitly determined positive formula H. Its unfolded body is □(p∨H(¬U)). Start from {¬p,p}, weaken by H(¬U), introduce p∨H(¬U), apply modal K, and fold μ once. This produces {A,¬U} using only C's atomic, structural, propositional, modal and μ-unfolding rules.

Likewise, W=νy.□(p∧R(U,y)) has dual

    ¬W = μy.◇(¬p∨J(y)).

Start from {p,¬p}, weaken by J(¬W), introduce the disjunction, apply modal K with principal p, and fold μ once. This produces {B,¬W}. The checker expands H and J from the actual syntax; they are not uninterpreted axioms or assumptions.

## 6. The only remaining explicit cut in this certificate

Weaken {B,U} by W and {A,W} by U. Since A=¬B, the two premises are

    U,W,B       U,W,¬B.

One cut on B yields U,W. The cut formula has modal depth1 and no fixed-point binder. This locates a concrete test for any prospective cut-free transformation: it must remove this application while respecting the exact ordinary-induction contexts. A general admissibility theorem for cuts of this shape would settle this example, but no such theorem is inferred merely from the example's semantics.

The failed shortcut is to argue that four separately cut-free equivalences to complementary formulas make U∨W cut-free provable by propositional reasoning. Combining those equivalences ordinarily uses cut; the certificate displays that use rather than hiding it. Similarly, Clo's unprovability cannot be transported to C without a proved embedding, and no such embedding is assumed.

## 7. Mechanical certificate and limits

`turn1/proof_certificate.py` constructs a finite DAG and validates every inference syntactically. Its `certificate.json` stores all formulas, sequents, premise IDs and principal formulas. The verifier checks closedness, capture-free substitution for these closed instances, literal context matching, acyclicity and exact rule shape.

There are36 stored nodes. The four cut-free proof roots use16,5,23 and5 ancestral nodes respectively. The final one-cut proof uses26 ancestral nodes. The receipt records223 assertions including a deliberately corrupted induction inference which must be rejected. Counts are finite certificate checks, not a proof-search exhaustiveness claim or an independent audit.

The proof uses no deep-disjunction rule, no strengthened induction, no cyclic or infinitary rule, no generalized fixed-point identity axiom and no ν-unfolding. Its only explicitly marked cut is the final □p cut. The actual2016 system's additional rules are recorded separately; any negative conclusion about a weaker core would require further work before addressing the original question.

## 8. What remains after turn1

The original completeness question remains unresolved. The newly pinned test case calls for either a cut-free construction of Φ in the ordinary-induction core or a rigorous account of why the specific premise-combination step cannot be transformed by a proposed method. A failed bounded search would not establish unprovability. More generally the old strong-induction completeness reduction cannot be invoked after the Clo correction without a repaired theorem.

This turn supplies scoped proof progress and an auditable target for subsequent attempts. It does not consume the remaining four turns with literature triage and does not justify a solved or incomplete-system disposition.

Sources: Kloibhofer, https://arxiv.org/abs/2307.06846 ; Afshari–Leigh2016, https://oa.tib.eu/renate/bitstreams/50824d0c-d5f5-4a10-8518-36ade258b3e3/download ; original report DOI10.4171/OWR/2017/53. Later-source corrections are recorded in SOURCE_GATE.md and ADDITIONAL_GATE_FINDINGS.md.
