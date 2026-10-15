# Independent syntactic adversarial review: PR 480 / problem 30003656

Review checkpoint: 2026-10-11 20:47:57 America/Los_Angeles (2026-10-12 03:47:57 UTC).
Candidate identified by parent: `cd9025795f40bd9ebc2b32de50917d73ca0f2bfa`.
Reviewer scope: mathematical verification and exact original-source alignment;
historical priority and publication readiness are separate gates.

**Verdict: mathematical PASS for the literal consequence-based question.**
No central proof gap, counterexample, circular step, or hidden extra algebraic
axiom was found. The finite-presentation argument gives full intuitionistic
geometric conservativity, not merely a result for equational conclusions or
finitary coherent formulas. The asserted counterexample is in the original
one-constant signature and is consistent. This verdict does not certify novelty.

Completion estimate: 100% of this assigned mathematical/source-scope audit;
approximately 80% toward promotion of this PR's result, because the historical
priority and final-package gates remain outside this review. These estimates
are judgments, not mathematical probabilities.

## Independence and checked inputs

I read `PROOF.md`, `SOURCE_GATE.md`, and `check_exact.py` from the isolated
source snapshot. I did not read the frozen author audit, other agents' reports,
or prior review verdicts before reaching the verdict. No Git, index, queue,
PR, or publication mutations were performed. No individual was contacted.

I reconstructed the quotient completeness and forcing arguments rather than
treating the supplied proof as a certificate. An independently authored finite
witness extractor and certificate checker are saved beside this report. Its
test result is evidence for the local mechanism only; the unbounded and
infinitary claims are justified below by induction.

## Strongest verified theorem

Let `T` have one sort, one constant `c`, logical equality, and no nonlogical
axioms. Let

```
β = ∀x ¬¬(x=c),      α = ¬β.
```

In intuitionistic logic, for every geometric sequent `φ ⊢_X ψ` over this
signature (finite variable context and arbitrary small set-indexed
disjunctions),

```
T+α ⊢ φ ⊢_X ψ    implies    T ⊢ φ ⊢_X ψ.
```

The generic pointed object in `[FinPointed, Set]` validates `β` and therefore
`¬α`. The pointed-object functor on finite pointed sets and injections
validates `α`. Both toposes are nondegenerate. Thus the generic model fails
to validate a `T`-redundant sentence for a purely equational theory.

## 1. Finite equality presentations and witness extraction

Fix a finite context `X=(x1,...,xn)` and a finite conjunction `E` of equations.
The only terms are `c,x1,...,xn`. Regard `E` as the edge list of a finite graph
on these terms and close its edges under equivalence. The quotient `Q_E`
is a finite pointed set, with the class of `c` as its point. For every pair
of terms `s,t`, equality of their classes is witnessed by a finite path in
this graph, so `E ⊢ s=t` follows using ordinary equality rules. Conversely,
the quotient assignment itself refutes every equality outside that closure.

The quotient need not be an injective image of the free stage. This is not a
defect: `Q_E` is an object of the injection category, and validity of a sequent
must be tested at every stage and every tuple of that stage. Tuples may have
repeated entries. The proof never requires the noninjective quotient map to
be an arrow in the injection category.

For each quotient class select the least indexed representative in the fixed
list `(c,x1,...,xn)`. This is a canonical finite computation, not an application
of a choice principle. Every element of `Q_E` consequently has an available
term in the original context.

Now let `ψ` be geometric and true at `Q_E` under its quotient tuple. Structural
induction gives `E ⊢ ψ`:

* An equality is discharged by its finite equivalence path.
* `⊤` is immediate. `⊥` cannot be true in this nonempty ordinary set.
* A finite conjunction supplies proofs of each conjunct.
* Membership in a set-indexed union supplies a particular index and truth of
  that disjunct; the induction hypothesis and that disjunction-introduction
  rule suffice. There is no simultaneous selection across the whole index set.
* An existential supplies one quotient element. Replace its bound variable
  by the canonical representative term, apply the induction hypothesis, and
  introduce that existential. Nested existentials repeat this process.

Auxiliary variables introduced inside `ψ` are handled by extending the
substitution with their chosen representative terms. Original context
variables remain the original variables: any true atom involving such a
variable and a representative still follows from the same equivalence closure.
The proof does not assume that an existential witness is a fresh generator.

This establishes the exact local lemma used by the candidate, with logical
equality included. It also explains why a constant is useful at the empty
context: the quotient is the singleton pointed set and `c` is still a witness.

## 2. Full geometric antecedents and arbitrary disjunctions

Here is the precise normal form implicit in the manuscript. For every geometric
formula `φ(X)`, structural recursion constructs a small set `I_φ`, and for
each `i∈I_φ` a finite fresh tuple `Y_i` and finite conjunction of atoms
`E_i(X,Y_i)`, such that intuitionistically

```
φ(X)  ↔  ⋁_{i∈I_φ} ∃Y_i E_i(X,Y_i).
```

The recursion is explicit:

* An equality has one branch, no bound variables, and that one atom.
* Truth has one branch and an empty conjunction; falsity has no branches.
* A disjunction has branch set the disjoint union of the branch sets of its
  disjuncts.
* A finite conjunction has branch set the finite Cartesian product of the
  conjuncts' branch sets. For one product tuple, concatenate its finite
  witness tuples and finite lists of atoms. Rename bound variables canonically
  to avoid collisions.
* An existential adds its variable to the finite witness tuple in each branch.

Only finite products occur. The branch sets may be infinite, and the finite
lengths of their witness tuples need not have a uniform bound. The standard
infinitary disjunction-elimination rule handles exactly such a family. This
is not an assertion of a single finitary proof for every arbitrary antecedent.
Empty disjunctions and empty products have their usual meanings, and give
the correct falsity/truth cases. No infinitary conjunction is admitted as a
geometric connective here.

Suppose the injection model validates `φ ⊢_X ψ`. Fix any normal-form branch.
At the stage `Q_{E_i}` use the tuple of classes of all variables in `X,Y_i`.
It satisfies `E_i`, hence satisfies `φ`; therefore it satisfies `ψ`. Section 1
gives `E_i ⊢_{X,Y_i} ψ`. Since `Y_i` was made fresh and is absent from `ψ`,
existential elimination gives `∃Y_i E_i ⊢_X ψ`. Disjunction elimination over
all branches and the normal-form equivalence give `φ ⊢_X ψ`.

This is full geometric completeness for the candidate injection model.
The argument remains valid when the antecedent has arbitrarily many branches
or branches with arbitrarily large finite contexts. There is no need to bound
the stage sizes globally and no transfer to an unproved stronger statement.

## 3. Presheaf variance, pointwise semantics, and reflection

Write `C=FinPointed` with all pointed maps and `D=FinPointed_inj` with the
same objects and pointed injections. The covariant functor categories are
presheaf toposes on `C^op` and `D^op`. Kripke successors are arrows going out
of a finite pointed set. Reversing them would break the construction.

At the trivial topology, geometric formulas are evaluated pointwise. Equality
is ordinary equality of stage elements; finite conjunction is intersection;
arbitrary disjunction is union; and existential quantification is a pointwise
image. The reason witnesses do not appear merely at a later stage is that
the only required cover is the identity cover.

The same stage sets and the same tuple valuations occur in both models.
Thus they agree on every geometric formula at every stage. A geometric
sequent is valid precisely when its interpreting subobject inclusion holds
at every stage; this also agrees in both models. Nongeometric formulas need
not agree because implication and universal quantification inspect arrows.

Equivalently, restriction along `D→C` preserves finite limits, images, and
all small joins, and reflects isomorphisms because it keeps every object.
The comparison mono from `[[φ]]∩[[ψ]]` to `[[φ]]` becomes an isomorphism iff
the sequent is valid. Conservativity therefore reflects its validity. There
is no illicit preservation of `∀`, `→`, or negation in this step.

## 4. The forcing calculations and falsification attempts

For every `a` at every stage in `C`, and every map to a successor stage,
that successor has a pointed collapse to the singleton. The image of `a`
then equals the point. Consequently no successor can force `¬(a=c)`, and
every stage forces `¬¬(a=c)`. Applying the universal clause to all successor
elements proves `β` globally in the generic model.

In `D`, an element distinct from the point stays distinct under every arrow,
so it forces `¬(a=c)` and cannot force its double negation. Every stage has
an injection into a stage with one additional nonpoint element. The new
element violates the instance required by `β`. Hence no stage of `D` forces
`β`; the same is true of every successor stage, giving `¬β` at every stage.

The following specific potential failures were checked:

* The singleton stage does not make the universal claim automatically true:
  universal quantification checks all future stages. It does make each local
  instance of equality true, as it should.
* The injection model validates `α` at the singleton stage, but does not
  validate `∃x¬(x=c)` there. The argument never replaces `¬∀` by `∃¬`.
* The generic model validates the double-negated equality, not the universal
  equality `∀x(x=c)`; the nonpoint of the two-element stage refutes the latter.
* All valuations are allowed, including repeated coordinates and coordinates
  equal to the point. Restricting them to distinct generators would be wrong.
* The finite quotient never needs an injective quotient arrow.
* There are no two distinct constants to which a constructor-disjointness
  axiom could apply. Injectivity of the nullary symbol has empty conclusion,
  and no cycle axiom is applicable. Thus no hidden constructor axiom enters.
* `T+α` is consistent even in ordinary Set: the two-element pointed set is a
  model. The singleton pointed set refutes `α`, so `α` is not a classical
  tautology. Classically, `α` says there exists an element different from `c`;
  this classical reading is not used in the conservativity proof.

Finally, `α` cannot be equivalent over `T` to a geometric formula or geometric
sequent: geometric truth is the same in the two candidate models, whereas
`α` is valid in the injection model and is refuted by its negation in the
generic model. Its nongeometric character is substantive, not just syntactic.

## 5. Genericity and the exact target

Finite pointed sets are precisely the finitely presented algebras of this
theory, and each is free on its nonpoint elements. The category `C^op` is the
displayed Lawvere theory, with finite limits obtained from finite pointed
colimits. The generic carrier is the representable `Hom_C(A1,-)`, canonically
the underlying-set functor. The distinguished point is induced by the pointed
collapse `A1→A0`. This identifies the exact generic model, rather than a free
Set algebra or a renaming model mistakenly called generic.

The independently opened [primary BBC preprint](https://arxiv.org/html/1712.07743)
defines redundancy by absence of new geometric consequences, including logical
equality. Its final algebraic question expressly identifies algebraic with
purely equational. Its theorem 5.11 uses constructor axioms; for this one
nullary symbol those add no nontrivial axioms. The empty-context witness and
small-index-set conventions also match the present reconstruction. Its broader
generalized-geometric fragment is not being silently substituted for the
ordinary geometric consequences defining redundancy.

The independently opened [original OWR report, pp. 3134–3136](https://ems.press/content/serial-article-files/46716?nt=1)
has the same consequence-based definition and ends by asking whether the
algebraic case has a positive answer. The exact target is therefore negated
by this construction. Neither of these displayed statements imposes an
additional stability, base-change, classical-validity, or predicate-free
restriction on the sentence beyond the chosen purely equational signature.
This source alignment does not establish whether the construction is new.

## 6. Foundations and recommended precision

For the mathematical theorem, use ordinary set foundations with a stated
small-set/universe convention and the standard infinitary intuitionistic
calculus. The normal form uses sets obtained by disjoint union and finite
products, and structural induction on well-founded formula syntax. Witness
extraction is constructive at the finite quotient and uses no excluded-middle
or choice step: equality closure is decidable, and representatives are canonical.
The categorical proof is also sufficient in the ordinary ambient foundations.

I recommend that a preprint explicitly state this ambient convention and give
the normal form in Section 2 above. This is clarification, not a mathematical
repair. If the paper additionally claims implementation in a specified weak
predicative foundation, that stronger metatheoretic claim needs a named formal
system and details for set-indexed syntax and derivations. The candidate does
not need such a claim to answer its literal target. It should avoid suggesting
that arbitrary infinitary antecedents always yield one finitary derivation.

## 7. Independent finite reproducibility check

`independent_witness_check.py` uses transitive-closure quotients independently
of the candidate's union-find checks. It constructs selected disjunct and
original-term existential certificates and validates them against all small
pointed assignments satisfying the premise. It includes empty disjunction,
empty conjunction, nested existentials, and equality-constrained witnesses.

The result was PASS for 64 equality presentations, 25 formula templates,
1,238 extracted certificates, and 9,136 checks of those certificates in
ordinary pointed models. It performs no floating-point operations and uses
only the standard library. This finite test cannot prove arbitrary-set
normalization, genericity, or unbounded forcing; those have separate proofs
above. I also inspected the candidate's finite-category script; its bounded
examples are appropriately described as sanity checks, not certificates for
the infinitary theorem.

## Promotion decision and exact remaining gap

No mathematical repair is required. I recommend advancing this candidate to
an independent historical-priority audit and concise-preprint preparation.
The exact remaining gap toward the user's publication goal is historical
priority/source relation (particularly the unobtained 2019 follow-up and the
draft scope warning), followed by adversarial review of the actual finished
paper and reproducibility package. This audit is not permission to claim a
first resolution or to publish without those gates.
