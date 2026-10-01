# Recovered author turn 4: internally coded targets and a rich-admissible test

## Route tested

After the finite-cover barrier, try the opposite strategy: seek a counterexample
to the conjecture among rich admissibles H_kappa. Such structures contain
many complete codes for smaller structures, so their interpretation-closure
property could conceivably hold without a jump fixed point. The required two
claims must both be proved, not inferred from abundance of parameters.

## 1. All internally set-coded targets already reduce strongly

**Proposition.** Suppose an admissible A contains a nonempty internal set D and
internal relations R_1,...,R_m on finite powers of D. Let B be the external
relational structure represented by this set-sized code. Then B is strongly
Sigma-reducible to A, whenever the source's Sigma predicates on B are the
stated first-order set-theoretic formulas. Indeed all first-order relations of
B pull back to Delta_0 relations over A with these code parameters.

**Proof.** Choose d_0 in D. Map a in |A| to itself if a is a member of D, and
to d_0 otherwise. This is a surjection onto D whose graph is bounded definable
with parameters D,d_0. Replace each atomic B-relation by membership in its
internal code R_i, and replace **every** quantifier of a fixed B-formula by a
quantifier bounded to D. Equality is ordinary equality on D. Finite tuple
coding can be bounded by the appropriate finite power of D, an internal A-set.
The resulting formula is Delta_0 over A, including arbitrary originally
unbounded B-quantifiers. Substitution of the displayed surjection preserves
bounded definability. Induction on the formula proves truth equivalence.
The same surjection serves all formulas. QED.

The proposition does not say that B's code belongs to A merely because B is
atomically interpretable in A. Internal set coding is an additional hypothesis.

## 2. Consequence for H_kappa

**Corollary.** In ambient ZFC, if kappa is an uncountable regular cardinal, then
every nonempty structure B of cardinality less than kappa in a finite relational
language is strongly reducible to H_kappa in the sense above.

**Proof.** H_kappa is admissible: transitive closure, pairing, union and bounded
separation are preserved; for collection, an internal indexing set has size
less than kappa, and choice followed by regularity bounds the hereditary size
of a selected witness family below kappa. Choose a copy of B with domain an
ordinal lambda of cardinality less than kappa. The domain and each finite-arity
relation on it have hereditary size less than kappa, so their codes are elements
of H_kappa. Apply the proposition. QED.

No satisfaction-set parameter or model-theoretic completeness theorem is
needed for this corollary. Each fixed formula is directly relativized to the
internal domain. It strengthens the countable-target observation of turn 3.

## 3. Testing the prospective counterexample

For A=H_kappa the corollary discharges the source's global implication only for
targets smaller than kappa. An atomically interpretable B is bounded in size
by |H_kappa|, not necessarily by a cardinal below kappa. The identity
interpretation B=A already shows that such a small-target restriction cannot
be silently imposed. No CH or cardinal-arithmetic equality is assumed here.

The attempted repair was to use small elementary substructures of B and combine
their internally coded diagrams. There are two independent problems:

1. A small elementary substructure need not be isomorphic to B; mapping onto
   it does not produce a surjection onto B.
2. A family of small abstract codes does not specify compatible embeddings into
   the prescribed B. The atomic A-presentation by itself does not provide a
   Delta(A) test that a local code has the correct complete elementary type.

A parameter-free theory is only one set of sentences. Replacing it by the full
elementary diagram with a constant for every element of a large B can exceed
the hereditary-size bound. Hence the earlier real-parameter argument for
countable B cannot be extended by changing its notation.

The other required half of the prospective counterexample, that H_kappa is
not strongly equivalent to its jump, also has not been established. Ordinary
Turing-jump strictness or a difference of internal ordinal heights would not
prove it. This route supplies no counterexample to the original conjecture.

## Outcome and next step

Internal set coding gives an explicit strong reduction, and the small-target
corollary is proved. But the rich-admissible counterexample strategy has neither
verified the full closure property nor excluded a structural jump fixed point.
The missing compatibility for large targets is precise. This is recovered
author turn 4, not a final unsolved disposition. Turn 5 must return to a
presentation-independent construction or obstruction for the actual converse.
The new propositions require independent review before publication.
