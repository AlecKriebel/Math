# A set-cover condition for lifting an atomic interpretation

Problem 30004676 / OWR-7155442-010. **Status: unsolved.**

This reconstructs one interrupted partial route. It does not establish the
conjectured equivalence, prove the unproved implication, or claim novelty.
The pre-interruption attempt count is unavailable and has not been reset to zero.

## 1. Target and source boundary

Puzarenko's question in the [2021 Computability Theory report, printed
pp. 1181–1182](https://ems.press/content/serial-article-files/46899) compares
two conditions on an admissible structure A: equivalence to its structural
jump, and the assertion that every admissible B atomically interpretable in A
is strongly Sigma-reducible to A. The report explicitly credits the forward
implication and leaves the converse conjectural. The workshop was in 2021;
the report was published in 2022.

Here “atomic” requires a surjection nu from A onto B whose pullbacks of the
basic relations, including equality, are Delta over A. “Strong” requires one
surjection whose pullbacks of **all internal Sigma relations** of B are Sigma
over A. These are different requirements. We retain the report's admissible
context rather than treating an arbitrary relational structure as automatically
an admissible set.

The source constructs the jump by adding a universal semidecidable predicate
to an appropriate hereditarily finite presentation. Existing jump fixed-point
theorems are background, not a proof of this universal equivalence.

## 2. Conventions

Let A and B be well-founded models of Kripke–Platek set theory with urelements,
in finite relational signatures containing their set/urelement distinction and
membership relation. Additional relations are permitted, with KPU collection available for the
language used in (1) below. This is a conditional lemma in that relational setting, not an assertion that every possible signature
or coding convention has already been covered.

Write `|A|` and `|B|` for their external domains. If c is an internal A-set,
write

    el_A(c) = {z in |A| : A satisfies z in c}.

This is notation in the metatheory. It does not assert that an external subset
of |A| belongs to A. Use the analogous notation el_B(b), with no members for a
B-urelement. Let nu: |A| -> |B| be surjective. It is an external map; we do
not assume that its graph is a set or a definable relation in A.

Sigma formulas are generated from atomic and negated atomic formulas by finite
conjunction/disjunction, bounded set quantification and unbounded existential
quantification. Over KPU this agrees with the usual Sigma_1 convention. Delta
means that both a relation and its complement have Sigma definitions. Finitely
many parameters are allowed. For any fixed B-parameter tuple we choose an
A-representative tuple using surjectivity; no global choice function is assumed.

Assume that every basic B-relation, including equality, membership and the sort
predicate, has Delta pullback along nu. A finite list of positive and negative
Sigma definitions is fixed once and for all. Constants, if present, are handled
by chosen representatives and pullback equality.

## 3. Exact additional hypothesis

There is a **single Sigma-definable relation** C(y,c) over A satisfying:

1. **Internality:** C(y,c) implies c is an A-set.
2. **Totality:** for every y in |A|, some c in |A| satisfies C(y,c).
3. **Exact coverage:** whenever C(y,c),

       {nu(z) : z in el_A(c)} = el_B(nu(y)).              (Cover)

The image equality is an external mathematical condition on the definable
relation C. It is not being asserted to have a Sigma definition merely by
writing it. Both containments matter. C need not be functional; duplicate
representatives are allowed, and different valid covers may be used in
different subformulas. If nu(y) is a urelement or empty set, a valid cover is
the empty A-set.

The term “Sigma-selectable covers” below means precisely this total relation.
It does **not** claim a definable single-valued selector. Existence of individual
covers without one Sigma-definable family C is a weaker, insufficient hypothesis
for the following proof.

## 4. Conditional lifting theorem

**Theorem.** Under the assumptions in Sections 2–3, the same map nu pulls every
Sigma-definable relation of B back to a Sigma-definable relation of A.
Consequently it witnesses B <=_Sigma A in the report's strong sense, for the
specified relational/parameter convention. In addition, every Delta_0 formula
of B has Delta pullback.

### Closure fact in A

The only nontrivial closure needed is bounded universal quantification of a
Sigma predicate. In Sigma_1 normal form, let

    psi(z,p) <-> exists u theta(z,u,p)

with theta Delta_0. For every internal A-set c, KPU collection gives

    (forall z in c)(exists u) theta(z,u,p)
      <-> exists d [Set(d) and
                    (forall z in c)(exists u in d) theta(z,u,p)].    (1)

For the left-to-right implication, apply Delta_0-Collection to theta to obtain
an internal set of witnesses; the empty c case uses an empty witness set.
The reverse implication is immediate. The right side is Sigma_1. Finite tuples
of witnesses can be encoded as sets in KPU. Finite conjunction/disjunction and
existential quantification also preserve Sigma. Thus all closure steps below
are valid, whether one uses the generated Sigma class or Sigma_1 normal form.

### Formula translation

Put the B-formula into the stated positive Sigma syntax, renaming bound variables
to avoid capture. Define T recursively. A variable assignment in A denotes the
corresponding assignment in B after applying nu componentwise.

- For each atomic or negated atomic B-formula, use the fixed positive or negative
  Sigma definition of its pullback. In particular, equality is interpreted by
  equality of images under nu, not by literal equality of representatives.
- T commutes with conjunction and disjunction.
- For unbounded existential quantification, use

      T(exists x phi) := exists x T(phi).                       (2)

- For either bounded quantifier Q in {exists, forall}, use a fresh variable c:

      T((Q x in y) phi) :=
          exists c [C(y,c) and (Q x in c) T(phi)].              (3)

Every translated formula is Sigma over A. For (3), use that C is Sigma,
c is an internal A-set, and the closure fact (1). This is a syntactic
induction on one finite formula. It is not the unsupported claim that A has
a Sigma truth predicate for all formulas of B at once.

### Semantic induction

We prove, for every formula covered by the translation and every assignment a,

    A satisfies T(phi)[a]  iff  B satisfies phi[nu(a)].         (4)

The atomic cases hold by hypothesis. Boolean connectives preserve (4).
For (2), each A-witness supplies a B-witness, and surjectivity supplies an
A-representative for each B-witness.

For bounded existential quantification in (3), suppose the B-formula holds.
Take any valid cover c, whose existence follows from totality. Exact coverage
gives a member x of c representing the B-witness; induction proves T(phi) for
that x. Conversely, a witness x in a valid cover has nu(x) in el_B(nu(y)), by
the first containment in (Cover), and induction gives the required B-formula.

For bounded universal quantification, if the B-formula holds, every element
of any valid c represents a member of nu(y), so induction proves the A-universal
formula. Conversely, if the A-universal formula holds for one valid c, every
member of nu(y) has at least one representative in c, by the other containment
in (Cover). Applying induction to that representative proves the B-universal
formula. Neither injectivity nor a distinguished representative is used.
The empty/urelement case is covered by the ordinary vacuity rules.

This proves (4), and hence preservation of all Sigma relations, including
relations with fixed parameters. If delta is Delta_0, both delta and its
negation can be put in the same bounded positive syntax. Their translations
are complementary Sigma predicates by (4). The pullback of delta is therefore
Delta. This proves the theorem.

## 5. What the theorem does not establish

Atomic Delta pullbacks alone allow the naive translation

    (forall x in_B y) phi(x,y)
      -> forall x in |A| [E_nu(x,y) implies T(phi)(x,y)],       (5)

where E_nu is the pullback of B-membership. The quantifier on the right is
**unbounded in A**. Delta definability of E_nu does not turn its fiber into an
internal A-set, and does not change that quantifier into a bounded one.
Section 3 is the additional condition that avoids (5).

KPU collection cannot be applied to a class of representatives merely because
it is externally the inverse image of an internal B-set. An internal A-set
over which to apply collection must first be provided. Nor does writing
“c contains a representative of every B-member” yield a Sigma predicate:
the straightforward coverage test quantifies over all representatives in A.
No general construction of C is given here.

In particular:

- Pointwise existence of an external set of representatives is not internal
  set existence in A.
- Pointwise existence of internal covers is not a total Sigma-definable cover
  relation.
- A sufficient condition for one interpretation to be strong is not a proof
  that the global interpretation-closure property absorbs the jump.
- Substituting B = J(A) in that global property requires proving its antecedent:
  atomic interpretability of the jump in A. The new universal semidecidable
  predicate is not automatically Delta over A. Its negative atomic instances
  are exactly information one cannot insert for free.
- A Turing jump diagonalization does not decide this structural question.
  Structural fixed points already exist; the reduced objects and maps differ
  from the ordinary jump of one oracle set.

## 6. Precise remaining problem and stopping point

The original unproved implication remains: if **every** admissible B atomically
interpretable in A is strongly Sigma-reducible to A, must A be Sigma-equivalent
to its jump? No proof or admissible counterexample has been reconstructed.

For the recovered bounded-quantifier route, the missing ingredient is an
appropriate uniform, internally set-bounded representation theorem (or a
replacement mechanism) strong enough to connect that global hypothesis with
the jump. We have not shown the cover condition follows from atomic
interpretability, from the global hypothesis, or that it is necessary. The
route is stopped at this unsupported bridge; restating it is not additional
progress.

The finite diagnostic script checks the cover translation on small relational
models with redundant representatives and rejects defective covers. Those
models are not admissible sets, and the checks do not verify KPU, definability,
or the original conjecture. The proof above, rather than a check count, is the
conditional mathematical result. Independent adversarial review is required
before this partial package is published.
