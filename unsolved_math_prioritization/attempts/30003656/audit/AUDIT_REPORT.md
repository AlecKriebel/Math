# Independent adversarial audit: Wraith redundancy for algebraic theories

Problem **30003656 / OWR-15958-003**, rank 506  
Audit date: **3 October 2026**  
Frozen input: `FROZEN_AUTHOR_MANIFEST.json`, frozen at 17:18:05 UTC

## Verdict

**PASS_FULL_SCOPED_COUNTEREXAMPLE.** The frozen candidate proves a negative answer to the literal consequence-based statement printed in the target sources. No mathematical correction is required for its principal theorem:

> Let T have one sort, one constant c, and no nonlogical axioms. The sentence α = ¬∀x ¬¬(x=c) adds no geometric consequences to T, but the generic T-model validates ¬α.

This verdict covers geometric sequents with equality and arbitrary small set-indexed disjunctions in the original signature. It is not limited to atomic consequences, finite models, finite disjunctions, or the computer-tested fragment.

**The scope qualification must travel with the result.** This audit does not certify historical priority, novelty, the absence of earlier algebraic counterexamples, or a solution of any additional intended restriction that has not been stated. In particular, a later 2019 paper announces a negative answer to Wraith's question, and its full text was not obtained in this audit. Its relationship to this particular algebraic example remains unverified. An unqualified announcement of a newly solved longstanding open problem would exceed the evidence.

All six frozen author files retain their recorded hashes. The author's checker was replayed from a temporary copy and reproduced its recorded JSON byte for byte. Independently written controls pass **312,413 assertions**, including **seven rejected mutations**. The audit made no remote changes.

## 1. Source and target verification

The supplied original report was inspected in text and as a page image. Buchholtz's contribution ends on internal page 16 by leaving the algebraic case open; the preceding page defines redundancy by geometric consequences. It does not introduce a second restriction on sentences in that final paragraph. [Oberwolfach Report 53/2017](https://doi.org/10.4171/owr/2017/53).

The Bezem–Buchholtz–Coquand preprint explicitly gives the consequence-based definition in its introduction, includes equality in the consequences, and identifies the algebraic refinement with purely equational theories in Section 7. The audit inspected the relevant definitions, equality-completeness discussion, and a rendered image of page 26. The candidate theory is within that printed class. The paper's more general syntactic-forcing machinery is prior work; the present audit independently checks the special model rather than assuming its genericity from a name. [Primary preprint](https://arxiv.org/abs/1712.07743).

Blechschmidt's author-hosted draft explicitly points out excluded-middle counterexamples to the bare question and indicates that care is needed to exclude them. The checked paragraph supplies no precise replacement definition to apply here. The candidate α is not classically valid, but that fact alone would not certify compliance with every possible intended restriction. [Author source](https://github.com/iblech/internal-methods/blob/master/paper-qcoh.tex).

For Bezem and Coquand's *Skolem's Theorem in Coherent Logic* (2019), the publisher page verifies the authors, publication, and abstract-level negative-answer claim. Its page lists Altenkirch and Schubert as editors, not additional paper authors. Publisher full-text routes were inaccessible, and bounded author/institutional searches did not yield a readable copy. This is a **full-text evidence gap**, not evidence that the paper lacks the candidate or that the candidate is new. [Publisher record](https://journals.sagepub.com/doi/10.3233/FI-2019-1853).

The original question's explicit wording is enough to determine the mathematical scope audited here. The unverified later paper prevents a priority conclusion; it does not invalidate the independently proved theorem. No new repository-wide duplicate certification was undertaken, and the frozen author's bounded duplicate checks are not upgraded into exhaustive ones.

## 2. Signature, inhabitants, and the actual classifier

The signature has exactly the terms c and the variables. It has no primitive apartness predicate, inequality relation, disjointness axiom, injectivity axiom, or second constant. Negation in α is logical negation. Since c is a global element in every model, the sort is inhabited internally. The smallest object A₀ has one element; it is not an empty carrier.

Let C have objects Aₙ={0,...,n}, n≥0, and all maps preserving 0. Its finitely presented algebras are exactly its finite pointed sets. Every Aₙ is free on its n non-basepoint elements. The classifier is **[C,Set]**, with covariant evaluation U(A)=A; using [Cᵒᵖ,Set] instead would reverse the construction.

Here is a direct check beyond citing the general presheaf theorem. Put B=Cᵒᵖ. It is the Lawvere theory of pointed objects and has finite limits. For a pointed object (X,c) in a Grothendieck topos, define H(Aₙ)=Xⁿ, with morphisms given by substitutions of projections or c. Products are preserved. An equalizer of two term-tuples is a system of coordinate equalities or equalities to c. The equivalence classes not tied to c are the independent coordinates, so the equalizer is the corresponding finite power of X. Thus H is left exact. Conversely, a left-exact functor on B is determined by H(A₁) and the map H(A₀)=1→H(A₁) selecting c. The usual flat-functor description of geometric morphisms into a presheaf topos now classifies pointed objects.

Moreover, U is representable: Hom_C(A₁,A)≅A. Under the above geometric morphism its inverse image is H(A₁)=X, with the specified point. This identifies the claimed U as the genuine generic pointed object, not merely as some conservative model.

Let D be the identity-on-objects subcategory containing pointed injections, and let V(A)=A in [D,Set]. D is only used to obtain a conservative model. The manuscript correctly does not call V the generic T-model.

## 3. Forcing, covariance, and both opposite truth values

These functor categories are presheaf toposes with trivial site topology. Geometric operations have pointwise interpretations. Implication and universal quantification quantify over **outgoing** arrows A→B in C or D. In particular, universal quantification must inspect new elements at successor stages, and negation must inspect all successor stages, including identities.

### Generic model

At any stage B in C, every element b can be sent to 0 by the unique collapse B→A₀. Thus B cannot force ¬(b=c). This argument applies after every outgoing map from every starting stage. Therefore each stage forces ¬¬(b=c) for every possible future element b. It follows that every stage forces β=∀x¬¬(x=c).

Consequently every stage forces ¬α=¬¬β. This is a genuine refutation of α, not just failure to prove α. The presheaf topos is nondegenerate: the empty and singleton functors differ at every object. Ordinary equality has not collapsed internally; at A₁, its nonpoint element is unequal to c at that stage. Dropping the two negations is an invalid mutation.

### Injection model

A nonpoint b cannot be mapped to 0 by a pointed injection. Hence every stage with b≠0 forces ¬(b=c), and the identity arrow shows that it cannot force ¬¬(b=c).

For an arbitrary A, an injection A→A⊔{*} supplies a future nonpoint *. This contradicts the universal forcing requirement for β. Thus no stage forces β. The same statement at every successor stage is exactly the negation clause for α=¬β. Every stage therefore forces α.

The one-point stage is essential as a control. It forces α but fails ∃x¬(x=c), since its only current element is c. No invalid inference from a negated universal to an existential witness is used. As an additional logical cross-check, β is intuitionistically equivalent to ¬∃x¬(x=c), so α is equivalent to ¬¬∃x¬(x=c). This explains why eventual nonpoint witnesses suffice without a current witness.

The classical test is different: in a discrete Set-model, α fails on a singleton and holds on a two-element pointed set. Thus it is not a classically valid excluded-middle instance.

## 4. Full geometric-consequence conservativity

For i:D→C, restriction R=i*:[C,Set]→[D,Set] is an inverse-image functor. It preserves finite limits, arbitrary colimits, images, and hence arbitrary joins of subobjects. Its right adjoint is right Kan extension. It is conservative because i has exactly the same objects: a transformation whose restricted components are all isomorphisms already has all its components isomorphisms. Finally R(U)=V, including c.

For every geometric formula θ, including one with an arbitrary small disjunction, R carries its interpretation in U to its interpretation in V. Equality uses finite limits; finite conjunction uses intersections; existential quantification uses images; disjunction uses the image of a coproduct or, equivalently, a join. These operations are all preserved. This is a structural argument about arbitrary formulas, not an extrapolation from a finite collection of atoms.

For a sequent φ⊢ψ, validity is the assertion that the mono φ∩ψ→φ is an isomorphism. If V validates the sequent, its image under R is an isomorphism. Conservativity reflects that isomorphism, so U validates it. Therefore, if T+α proves a geometric sequent, soundness in V implies its validity in V; reflection implies validity in U; generic-model completeness gives its derivability in T.

This also handles false or otherwise inconsistent antecedents. No argument assumes that every premise has a valuation. Restriction is not asserted to preserve implication, negation, or universal quantification; the opposite values of β are a deliberate example of their nonpreservation.

## 5. Independent finite-presentation proof, including disjunctions

The manuscript's second proof is also sound. A geometric antecedent in a finite free-variable context has a disjunctive normal form whose branches are existentially quantified finite conjunctions of equations. This follows structurally: disjunction takes unions of branch sets; finite conjunction takes finite products and concatenates witness contexts; existential quantification appends a witness variable. Every individual branch has finitely many equations and variables even when the branch set is infinite. Falsity has no branches, truth has one empty branch, and conjunction with a false branch contributes none.

Eliminate the antecedent disjunction and move each branch's existential witnesses into the sequent context. For a resulting equality conjunction E, let Q be the quotient of {c,x₁,...,xₙ} by its generated equivalence relation. Q is finite, pointed, and nonempty. Every equality premise holds at the quotient valuation. There is no inconsistent conjunction consisting solely of equations in this particular signature: the singleton model satisfies every such conjunction. The genuinely inconsistent positive branches are the false branches already removed; they are discharged by falsity elimination.

If V validates E⊢ψ, pointwise geometric semantics makes ψ true at this Q. A structural induction extracts a derivation from E:

- Equality in Q is finite equivalence closure of E and is derived by equality rules.
- A finite conjunction combines its component derivations.
- A disjunction, including a set-indexed one, provides a true disjunct and the corresponding introduction step.
- An existential witness is a Q-element. Choose its representative from the finite list c,x₁,...,xₙ, substitute that term, and apply the induction hypothesis followed by existential introduction.
- Truth is immediate. Falsity is never true at Q.

Reassembling the antecedent gives the original geometric sequent. This directly establishes the needed completeness for all such sequents. Its witness extraction neither asserts decidability of arbitrary infinite disjunctions nor substitutes an external Boolean decision procedure for intuitionistic inference. All forcing calculations and finite-equality steps are constructive. As with the frozen manuscript, use of the full presheaf classifier is in the usual ambient categorical/set-theoretic framework; no machine-checked predicative foundational formalization is being certified.

## 6. Reproduction and independent controls

The author's recorded output is reproduced exactly, including 1,279 pointed maps and 89 pointed injections on five objects, 64 equality-premise sets, and 1,024 atomic consequence comparisons. The rerun did not write into the frozen input directory.

The new `audit_controls.py` is independently implemented. It uses actual carrier cardinalities, enumerates injections by permutations, uses a general implication clause for negation, and computes equality closure by Floyd–Warshall rather than the author's union-find. It contains a separate pointwise positive evaluator, a quotient witness extractor, and an independent verifier for the extracted derivation structure.

Its **312,413 passing assertions** include:

- Forcing calculations for all carrier bounds one through five, retaining the single-object truncation as a boundary control.
- **8,820** comparisons of geometric pointwise semantics against both functor-category interpretations.
- **296,916** homomorphism-preservation checks for true positive formulas.
- **2,352** quotient-witness extraction checks, **1,686** extracted-proof verifications, and **2,352** full-positive-formula consequence comparisons across finite valuations.
- Empty disjunction, empty conjunction, and false-antecedent controls.

The geometric sample contains **294 formulas**, including conjunctions, disjunctions, existential witnesses, and nested existentials. Its eight premise sets involve c and two free variables. Seven intentional mutations are rejected: evaluating ∀ only at the current stage; replacing α by a nonpoint existential; dropping double negation; removing proper transitions; using injections as the claimed classifier; eliminating growth altogether; and claiming classical validity of α.

These finite calculations are supplemental checks. They do not prove the unbounded classifier or arbitrary-geometric conservativity. Sections 2–5 supply those universal arguments. In particular, the actual program does not enumerate infinitely many disjuncts or all geometric formulas.

## 7. Disposition and portable files

Recommended mathematical classification: **verified negative answer to the literal displayed consequence-based algebraic statement**. Required accompanying caveats: historical priority unresolved; the 2019 full-text comparison unverified; no claim about an additional unstated refinement. No repair cycle is required for the frozen theorem, and the mathematical attempt count remains the author's recorded **2/5**.

Portable audit material consists only of this authored report, `audit_controls.py`, `audit_controls.json`, `author_rerun.json`, `FROZEN_INPUTS.json`, and `AUDIT_MANIFEST.json`. Source PDFs, full source extracts, rendered source pages, catalogue material, and unrelated research context are excluded. The author packet is unchanged and may be kept alongside these separately identified audit files.
