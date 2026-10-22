# A pointed-set counterexample to literal Wraith redundancy

Target: **30003656 / OWR-15958-003**, Wraith Redundancy for Algebraic Theories.
Author-stage candidate, 2026-10-03. Independent verification and historical-priority review are pending.

## 1. Exact claim and conventions

An algebraic theory here means a finitary, possibly many-sorted, purely equational theory with total operations, including allowed nullary operations. A one-sorted example suffices to refute a universal assertion over such theories. We use exactly one sort, one constant symbol `c`, no other operation or relation symbols, and no nonlogical axioms. Equality is the logical equality. Call this theory **T**. Its models are pointed objects. In particular the carrier is inhabited, because `c` is a global element; no convention about allowing empty sorts affects the construction.

The associated Lawvere theory has objects the finite powers of one sort. Its morphisms n → m are m-tuples of terms chosen from {c,x₁,…,xₙ}; composition is substitution. Thus its n-ary term operations are the n projections and the distinguished constant, and its nullary term set is {c}. No extra operation, order, apartness relation, injectivity axiom, or constructor-disjointness axiom is included in T.

A geometric formula is built from equality atoms, truth, falsity, finite conjunction, arbitrary set-indexed disjunction, and existential quantification, with finitely many free variables. A geometric sequent is φ ⊢ₓ ψ for geometric φ and ψ. Its sentence form is ∀x(φ → ψ). The consequence relation is intuitionistic. A sentence α is **T-redundant** if, for every geometric sequent σ in the original signature, T+α ⊢ σ implies T ⊢ σ. This is precisely the explicit consequence-based definition in the abstract and introduction of Bezem–Buchholtz–Coquand [BBC]. It is not redundancy of a generating operation, equational axiom, or presentation.

Put

    β := ∀x ¬¬(x=c),             α := ¬β.

**Theorem.** The sentence α is T-redundant, while the generic T-model validates β, hence validates ¬α. Consequently, the answer to the displayed consequence-based algebraic-theory question is negative.

The theorem concerns the literal stated definition. No claim is made to resolve an additional, unspecified strengthening of redundancy. Nor is a claim of historical priority made: [B] explicitly warns that the bare question already admits excluded-middle counterexamples. The present α is not itself classically valid: the singleton pointed set refutes it. Section 7 gives the exact scope limitations.

## 2. The two categories and their models

Let C be a small skeleton of the category of finite pointed sets and all point-preserving maps. Let D have the same objects but only injective point-preserving maps. We can take objects

    Aₙ = {0,1,…,n}, with distinguished point 0, for n ≥ 0.

Write E=[C,Set] and F=[D,Set], categories of **covariant** functors. They are presheaf toposes on Cᵒᵖ and Dᵒᵖ, respectively, with the trivial Grothendieck topology. Let U:C→Set and V:D→Set be the underlying-set functors, with the natural distinguished elements 0. They are internal T-models.

The topos E is the classifying topos for pointed objects, and U is its generic T-model. Here is a direct justification of this familiar presentation. Every finitely presented pointed set is finite, and every finite pointed set is free on its non-basepoint elements. Hence C is the category of finitely presented T-algebras, and the usual classifying presheaf model for an algebraic theory is the evaluation model in [C,Set]. Equivalently, Cᵒᵖ is the displayed Lawvere theory: finite coproducts of finite free pointed sets become finite products; a left-exact functor from Cᵒᵖ to a topos is determined by an object and one global element. The corresponding geometric morphism pulls U back to that pointed object. This is the standard presheaf classification, not a claim that U is a free Set-model.

The presheaf forcing clauses below use arrows **out of** a stage A, because the functors are covariant. For a tuple a∈U(A) and any formula θ:

- A ⊩ s=t iff the interpreted elements are equal at A.
- A ⊩ ⊥ never holds.
- A ⊩ θ∨η iff A ⊩ θ or A ⊩ η.
- A ⊩ ¬θ(a) iff for every f:A→B, B ⊩ θ(fa) implies B ⊩ ⊥.
- A ⊩ ∀x θ(x,a) iff for every f:A→B and b∈U(B), B ⊩ θ(b,fa).

The same clauses apply to V with arrows restricted to D. Infinite geometric disjunction and existential quantification are also evaluated pointwise. These are the usual Kripke–Joyal clauses for the trivial topology. Identity arrows are included.

## 3. The genuine generic model forces β

Fix A in C and a∈U(A). We show A ⊩ ¬¬(a=c). Let f:A→B be arbitrary. If B ⊩ ¬(f(a)=c), apply its negation clause to the unique point-preserving collapse q:B→A₀. At A₀ both qf(a) and c are 0, so A₀ ⊩ qf(a)=c. The assumed negation would therefore give A₀ ⊩ ⊥, impossible.

Thus no such B can force ¬(f(a)=c). This is exactly A ⊩ ¬¬(a=c). The same reasoning applies to every b at every successor stage B, so the universal-quantifier clause yields A ⊩ β for every A. Hence E ⊨ β.

Intuitionistic logic proves β→¬¬β. Since α=¬β, E ⊨ ¬α. In particular E does not validate α; E is nondegenerate since its initial and terminal functors differ at every object.

Important distinction: U does **not** validate ∀x(x=c). For example the element 1 at A₁ differs from c. It is precisely double negation that permits collapse maps to establish β.

## 4. The injection model forces α

If b≠c in a finite pointed set B, then every injective point-preserving map h:B→B′ preserves b≠c. Consequently B ⊩_V ¬(b=c), and B cannot force ¬¬(b=c).

Now fix any A in D. The inclusion j:A→A⊔{*}, where * is a fresh non-basepoint element, is an arrow of D. If A forced β, the universal clause applied to j and * would force ¬¬(*=c) at A⊔{*}. But the preceding paragraph forces ¬(*=c) there. This contradicts the forcing clauses. Thus no stage A forces β. This argument works at every successor stage as well; hence every A forces β→⊥. Therefore F ⊨ α.

The extension A⊔{*} is used only in the proof of failure of β. It is not an extra axiom of T, and no existential apartness sentence is asserted at every stage. In particular A₀ has no non-basepoint element, so V does not validate ∃x ¬(x=c). The logically invalid replacement of ¬∀ by ∃¬ would destroy the argument.

## 5. Redundancy: the conservative restriction proof

Let i:D→C be the inclusion. Restriction

    R : [C,Set] → [D,Set],       R(X)=X∘i,

preserves all limits and colimits, which are computed objectwise. It has a right adjoint (right Kan extension), so R is the inverse-image functor of a geometric morphism F→E. Moreover R is **conservative**: i is the identity on objects, and a natural transformation is an isomorphism exactly when each of its components is an isomorphism. Finally R(U)=V as T-models, including their distinguished constants.

For any geometric formula θ, geometric interpretation commutes with R. Explicitly, equality and finite conjunction use finite limits; disjunction uses joins; and existential quantification uses images. Restriction preserves all of these, including arbitrary set-indexed joins. Consequently it also reflects truth of geometric sequents in these models: if the subobject inclusion interpreting φ⊢ψ becomes valid after R, it was already valid before R, since its comparison monomorphism becomes an isomorphism and R is conservative.

Suppose T+α ⊢ σ, where σ is a geometric sequent. Soundness of intuitionistic logic in F and Section 4 give V ⊨ σ. Reflection gives U ⊨ σ. Generic-model completeness then gives T ⊢ σ. This proves the theorem.

There is no assertion that R preserves universal quantifiers, implication, negation, or arbitrary first-order sentences. Indeed Sections 3–4 prove that it fails to preserve β. There is also no claim that the injection category itself presents the generic model of T. Its role is a **geometrically conservative** model used to establish redundancy.

## 6. Independent explicit completeness proof

For readers who prefer not to use conservativity of a geometric morphism, the reflection step can be verified directly from finite equality presentations.

Every geometric sequent can be decomposed into sequents with antecedent a finite conjunction E of equality atoms: distribute finite conjunction over set-indexed disjunction and move existential witnesses in the antecedent into the finite variable context. Thus it is enough to consider

    E(x₁,…,xₙ) ⊢ ψ(x₁,…,xₙ),

where ψ is geometric. Terms are only c and the variables. Form the finite pointed quotient

    Q={c,x₁,…,xₙ}/∼E,

where ∼E is the equivalence relation generated by E; [c] is its point. Q is an object of D up to the harmless choice of a skeleton. Under the quotient valuation, E holds. If V validates the sequent, then ψ holds at Q. For geometric formulas this is pointwise truth.

Every element of Q has a representative among c,x₁,…,xₙ. Induct on a pointwise verification of ψ:

- an equality true in Q is derivable from E by reflexivity, symmetry and transitivity;
- conjunction combines the proofs;
- a disjunction supplies one true disjunct and its corresponding introduction rule, even when the disjunction is set-indexed;
- an existential supplies a Q-element, represented by a term among c and the variables, giving the required witness term;
- truth is immediate and falsity has no pointwise verification.

This yields an intuitionistic derivation E⊢ψ. Reassemble the original sequent using disjunction and existential elimination on its antecedent. Thus any geometric sequent valid in V is provable in T. Only finite quotients of finite sets of terms are needed; equality of terms in Q is decidable by finite equivalence closure. This is also a direct constructive verification of the special case of [BBC, Theorem 5.11] used here.

## 7. Scope, boundary cases, and prior-literature warning

1. **Same original language.** α uses only logical equality and the single constant already in T. It introduces no extra relation or sort.
2. **Constants allowed.** Nullary operations are standard in finitary algebraic theories; the Lawvere theory above makes this explicit. If constants were forbidden, the empty signature variant also works with β₀=∀x∀y¬¬(x=y), using finite sets/all maps versus finite sets/injections. The pointed version avoids all empty-carrier conventions.
3. **Constructive redundancy.** The finite-quotient argument proves the needed conservativity directly and does not invoke classical completeness, excluded middle, Boolean prime ideals, or choice. The standard ambient presheaf-topos presentation may be read in ordinary set theory; all forcing calculations are explicit.
4. **Not an excluded-middle tautology.** In classical Set-semantics β says that the pointed set is a singleton, while α says it has another element. Hence α is false in A₀ and true in A₁. This observation is a scope check, not the redundancy proof.
5. **The negation is not dropped.** The internal sentence α holds in V even at A₀. It does not imply ∃x¬(x=c) intuitionistically. Only the latter would visibly assert an extra element at every stage.
6. **Which problem is resolved?** The displayed consequence-based assertion in the cited OWR report and [BBC] is contradicted by the theorem. [B] warns about unstated care needed to exclude trivial examples; no precise stronger condition was located there. A reformulation involving preservation under all geometric base changes, a different consequence fragment, or restrictions on α would need to be stated and checked separately. This manuscript does not silently substitute such a reformulation or claim to settle it.
7. **Novelty.** No historical-priority claim is made. The essential machinery is present in [BBC], including geometric completeness of the renaming model. This package is an explicit consequence/scope analysis with a candidate counterexample, pending an independent mathematical and source audit.

## 8. Reproducible finite sanity checks

`check_exact.py` enumerates all basepoint-preserving maps and all basepoint-preserving injections among A₀,…,A₄. It computes equality, its negation and double negation, β, α, and the comparison sentence ∃x¬(x=c) directly from the finite-category forcing clauses. It also verifies finite equality-quotient closure against all small pointed-set assignments. The JSON output records the exact category sizes and test counts.

These finite computations are checks on the formulas, variance, and boundary cases. They do not prove an assertion over the unbounded categories or establish arbitrary-geometric conservativity. Those are proved in Sections 3–6. The checks use no floating-point arithmetic, numerical approximations, external libraries, or network access.

## References

- [BBC] M. Bezem, U. Buchholtz, T. Coquand, *Syntactic forcing models for coherent logic*, Indagationes Mathematicae 29 (2018), 1441–1464, [DOI](https://doi.org/10.1016/j.indag.2018.06.004). Checked primary preprint: [arXiv:1712.07743](https://arxiv.org/abs/1712.07743), especially Theorem 5.11, the following paragraph on decidable equality, and Section 7's algebraic-theory question.
- [OWR] U. Buchholtz, contribution *Syntactic Forcing Models for Coherent Logic*, Oberwolfach Report 53/2017, internal pp. 14–16, [DOI](https://doi.org/10.4171/owr/2017/53). The final paragraph asks about algebraic theories. [Institutional copy](https://oa.tib.eu/renate/server/api/core/bitstreams/f754efe0-f461-4dc6-8e01-be4de222b790/content).
- [B] I. Blechschmidt, *A general Nullstellensatz for generalized spaces*, author-hosted rough draft, Introduction, paragraph following Wraith's question, [author source](https://github.com/iblech/internal-methods/blob/master/paper-qcoh.tex). It explicitly discusses the excluded-middle caveat. No date or refereed-publication status is inferred from the current draft.
