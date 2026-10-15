# Recovered author turn 2: bounded truth and presentation changes

Started October 1, 2026 after the conditional-cover review. This is substantive
work on the missing converse. It does not close the original problem. The
pre-interruption count remains unknown; the recovered continuation is separately
numbered. Source lookup, memory maintenance and review are not extra turns.

## Route tested

Try to prove the converse by expressing strong reducibility as preservation of
bounded truth, then compressing the missing jump information into the bounded
truth of one atomically interpretable admissible structure. This avoids assuming
that the already semidecidable jump predicate has a decidable pullback.

## 1. Exact same-map criterion

Let nu: |A| -> |B| be an atomic Delta interpretation as in the frozen partial
lemma, with the same parameter-allowing relational KPU convention.

**Proposition.** The following are equivalent for this fixed nu:

1. Every Sigma(B) relation has Sigma(A) pullback along nu.
2. Every Delta_0(B) relation has Delta(A) pullback along nu.

**Proof.** If (1) holds, apply it to a Delta_0 formula delta and its negation;
both are Sigma over B. Their pullbacks are complementary Sigma predicates,
giving (2). Conversely, normalize a Sigma formula over B to
`exists y delta(x,y,p)` with delta Delta_0, using KPU in B. Fix representatives
of the finite parameter tuple p. By (2) the pullback of delta is Delta(A),
hence Sigma(A). Existentially quantify the representative y in A. Surjectivity
of nu makes this exactly the pullback of the original relation. The same nu
works for every formula; no change of interpretation is made. QED.

Thus the extra cover condition in the frozen theorem is a sufficient way of
obtaining all bounded-truth pullbacks. It has not been shown necessary.

## 2. What naive translation actually bounds

There is nevertheless a finite hierarchy bound without covers. For a fixed
first-order B-formula phi, replace each atomic relation by its Delta(A)
pullback. Expand a bounded B-existential into an unbounded existential with
the pulled-back membership condition, and a bounded B-universal into an
unbounded universal with the corresponding implication. Ordinary unbounded
quantifiers are translated over all of |A|. Surjectivity proves correctness
by induction for arbitrary first-order formulas.

Let q be the maximum number of B-quantifiers nested in phi, counting both
bounded and unbounded ones. The translated relation is Delta_(q+1) over A in
the following safe prenex sense: it has both a Sigma_(q+1) and a Pi_(q+1)
definition with a Delta_0(A) matrix.

To prove this bound, atomic pullbacks are Delta_1. Finite conjunction and
disjunction preserve the class of relations admitting both prenex definitions
at a given level. The extra membership guard is also Delta_1. If a relation
has both Sigma_n and Pi_n definitions, adding one existential or universal
quantifier gives both definitions at level n+1, by using the suitable existing
definition and padding with an unused quantifier when needed. Domains are
nonempty. Induction on quantifier nesting proves the bound.

This argument uses only ordinary finite prenex manipulations after the
B-bounds have been expanded. It does not assume higher Sigma_n-Collection
in A. Its conclusion is formula-by-formula finite definability, **not** a
uniform Sigma_1 bound. Bounded B-formulas can have unbounded nesting depth.
Consequently this bound alone does not give either condition of Proposition 1.

## 3. A presentation-invariance fact

Let C(A) denote the source's global property: every admissible B atomically
interpretable in A admits some strong Sigma reduction to A.

**Proposition.** If A and A' are strongly Sigma-equivalent, then C(A) and C(A')
are equivalent.

**Proof.** Strong reductions compose, because successive inverse images of
Sigma predicates are Sigma. They also preserve Delta predicates: apply the
definition separately to a predicate and its complement. If B is atomically
interpretable in A', compose that surjection with a strong reduction from A
onto A'. Its atomic pullbacks are Delta over A, so C(A) supplies a strong
reduction of B to A. Compose with a strong reduction of A to A' to obtain
B <=_Sigma A'. Reverse the roles of A and A' for the other implication. QED.

There is an important existential distinction: C(A) supplies **some** strong
surjection, not necessarily the original atomic surjection nu. It therefore
does not assert Proposition 1 for every initial presentation. An argument
which derives a cover family for an arbitrary given nu from C(A) needs a
separate presentation-rigidity theorem.

## 4. Attempted jump-compression step

The intended final step would build, for each A, one admissible B such that
B is atomically interpretable in A while J(A) is strongly reducible to B.
Then C(A) would give J(A) <=_Sigma A by transitivity; the reverse comparison
is the usual reduct comparison in the source's jump setup.

The proposed coding device was to make all possible witnesses of the universal
Sigma(A) predicate into members of an internal B-set. Bounded quantification
over that set could then test absence of a witness. This is precisely where
the attempt fails: the external A-domain is not automatically an internal
B-set in an A-decidable presentation. Adding a formal node for that domain
does not produce an admissible B. Closing under KPU can add objects and
relations whose atomic diagram is no longer shown Delta-definable in A.

Taking HF of the atomic A-structure only gives finite internal sets and does
not provide a bound for all witnesses. Taking an admissible closure such as
HYP instead does not automatically provide the required A-decidable atomic
presentation. Ordinary compactness/Henkin constructions also do not certify
well-foundedness. No one of these missing conditions is assumed here.

## Outcome and next route

The same-map criterion and presentation-invariance propositions are proved;
the finite quantifier-rank bound is proved but insufficient. The attempted
compression lacks an A-decidable, well-founded admissible target. The converse
is neither proved nor refuted.

The next substantive route is to test whether the published nonstandard-
computability construction for HYP models admits the needed generalized
relativization. Merely citing its classical example will not count as that
construction or as a full converse proof. This continuation remains active;
no final unsolved disposition or publication is requested here.
