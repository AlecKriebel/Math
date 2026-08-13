# Adversarial gap analysis for the quarnet-and-repair route

Status: **CLOSURE REJECTED; PRECISE GAPS ISOLATED**

This review attempts to break the argument in `PROOF_ATTEMPT.md` at each
logical promotion.

## 1. Exact quarnet encoding is not model-equivalence encoding

**Finding: VALID OBJECTION.**

Huber et al., Theorem 6.2 assumes equality of the exact labelled induced
quarnet deck.  The desired premise would only say that corresponding quarnet
models fail to be distinguishable, or at best that the quarnets are related
by ordinary `T`.  Neither premise satisfies the theorem's hypothesis.

The implication

```text
every quarnet is isomorphic or T-related
    => the complete networks are globally T-related
```

is a new triangle-quotient encoding theorem.  No statement read here proves
it.  In particular, choosing a separate `T` orientation on each four-set may
be inconsistent on overlaps.

Required repair: prove TQ, including global triangle matching, overlap
coherence, and admissible rootability.

## 2. The published small-network list is not exhaustive

**Finding: VALID OBJECTION.**

The Englander results give implications for named type pairs; they never
claim a complete sixteen-type, all-labellings stochastic atlas.  Theorem 3.2
uses those implications inside a longer triangle-free structural proof and
also needs a five-leaf comparison.  It does not imply the four-leaf dichotomy
Q in the presence of triangles.

Required repair: prove Q exactly.  A proof must keep apart disjoint open
images, distinguishability, lower-dimensional intersection, and ordinary `T`
common germs.  Equal ideals or equal displayed quartet sets do not establish
overlap.

There is a further scope trap: an induced quarnet of a network in `S_TC`
need not itself be strong.  Marginal suppression can shorten cycles and can
create precisely the weak local configurations excluded from the parent.
Therefore Q must cover every level-at-most-two quarnet that can arise under
`red_*`, not merely the standard-strong four-leaf members of the parent
class.  Restricting Q to strong quarnets would be circular.

## 3. Strongness of the parent does not pass to a marginal

**Finding: VALID OBJECTION.**

The weak-Theta quarnet is itself the counterexample: it is induced from a
hypothetical strong extension only after the repair taxon is omitted and the
repair vertex suppressed.  Therefore one cannot apply the strong or
triangle-free theorem directly to the four-leaf restriction.

Required repair: use one or two omitted repair witnesses and prove R.  Merely
asserting that a repair exists somewhere is insufficient.

## 4. The two minimal repairs are not the complete arbitrary-extension proof

**Finding: VALID OBJECTION.**

The `2 x 2` verifier proves exactly what it says: a common fifth label at the
minimal A-C or A-F repair vertex.  It does not cover:

* different repair labels in source and target;
* placement of the source repair label in the target and vice versa;
* longer side words and pendant descendant blocks;
* a repair exposed only after a 2-blob or parallel-artifact reduction; or
* compatibility of the selected local lifts with the same four-label weak-
  Theta identification.

Required repair: the aligned-or-separated repair lemma.  A satisfactory proof
may use only the two outgoing side families, but it must show that every
other placement yields an exact displayed-quartet/tree-of-blobs/sign witness.

## 5. A-C versus A-F is closed only in the aligned minimal case

**Finding: VERIFIED IN THAT SCOPE.**

All four aligned minimal comparisons have different displayed quartet sets
on `{0,1,2,3}`.  Since all inheritance weights are strictly positive,
Englander et al., Theorem 2.11 gives disjoint open images.  This includes both
cross-repair directions and is stronger than a generic separator.

Mutation checks that must remain true:

1. swapping source and target preserves the conclusion;
2. changing A-C to A-F changes the certified cycle multiset;
3. removing the repair leaf destroys the displayed-quartet witness and
   recovers the weak four-leaf ambiguity;
4. equality of displayed decks is never treated as evidence of model
   equality.

## 6. Proposition 2.8 is sufficient for directed containment obstruction

**Finding: VERIFIED.**

If an induced pair is distinguishable in Englander's symmetric measure-zero
sense, Proposition 2.8 makes the full pair distinguishable in the same sense.
A source-open regular containment would give a non-measure-zero source
preimage and therefore contradict distinguishability.  No continuous target
parameter selection is needed for this contrapositive.

Scope: this only helps after an induced pair has actually been proved
distinguishable.  It does not promote a zero/nonzero signature or unequal
topology by itself.

## 7. Convention compatibility needs an explicit lemma

**Finding: SMALL BUT REAL GAP.**

The locked `sd_0` operation defines standard topology and does not perform
later cleanup.  Englander and Huber restrictions do perform degree-two,
parallel, and 2-blob suppression.  The proof attempt uses `red_*` for that
reason, but a final theorem must prove that the induced quarnets used by
Huber's encoding are exactly the same objects as the induced subnetworks to
which Englander Proposition 2.8 applies under the locked convention.

The source definitions are visibly aligned in intent, but convention
compatibility must not be left implicit at the root/parallel/2-blob edge
cases.

## 8. Bound six is conditional, not established

**Finding: CORRECTLY LABELLED CONDITIONAL.**

Four labels locate a non-`T` quarnet if TQ holds.  At most one repair witness
from each network gives six labels if R holds.  Without TQ and R, there is no
proved universal witness bound.

## 9. Final adversarial verdict

The route does not close the landmark theorem from the currently cited
ingredients.  It does, however, replace a vague "remaining atlas" with three
specific mathematical obligations:

1. Q — an exhaustive four-leaf JC dichotomy modulo `T` and weak Theta;
2. R — a six-leaf strong-repair lift for weak Theta; and
3. TQ — quarnet encoding modulo coherent ordinary triangle redirection.

The aligned minimal repair algebra is no longer an obstacle.  The first
unproved promotion is the claim that an arbitrary weak-Theta marginal of two
strong networks admits one of those aligned minimal witnesses.  Any final
positive theorem that omits Q, R, or TQ should be rejected.
