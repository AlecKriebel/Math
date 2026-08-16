# Independent root/cut gate review

Status: **MIXED — Gate 1 unresolved/partly false; Gate 3 verified under the
locked literal convention**

This report summarizes the independent implementation in
`repair/independent/root_cut/`.  That implementation did not import the
discovery graph reducer, tensor engine, polynomial arithmetic, or sign code.
Its failures are preserved rather than repaired in place.

## Root atlas (Gate 1)

**FALSE — finite class-membership claim.**  Of 1,493 unique serialized root
records, 247 do not produce a standard simple semi-directed mixed graph under
literal one-step root suppression.  Every one of those 247 has both a
parallel mixed-edge artifact and failure of the local strong-tail condition.
The historical broad reducer subsequently merged the parallel pair and in
doing so lowered the reticulation count.  Its later `no_parallel` check was
therefore tautological.

The exact offending records are preserved in
`repair/independent/root_cut/failures/gate1_nonstandard_root_suppression_failures.json`.

**EXACTLY COMPUTED — surviving serialized collisions.**  Five common
signature representatives were stored.  Three are literal-standard strong
pairs and are ordinary triangle-redirection pairs.  The other two become
isomorphic/triangle-related only after the invalid broad cleanup and are
outside the locked standard class.

**EXACTLY COMPUTED but insufficient for closure.**  Fifty stored
source-vanishing/target-strict invariant witnesses were independently
expanded and sign-certified without a failure.  This validates those frozen
directions, not the claimed quantified atlas: the final nine-port JSON omits
the nonmatching network encodings, and the long-word routine reconstructs
from self-generated oracle comparisons rather than from an independent
observational deck.  Arbitrary-subdivision promotion and the end-to-end
topology-to-polynomial binding remain **UNRESOLVED**.

Consequently the root-collision lemma used by the withdrawn positive
manuscript is not submission-safe.

## Cut preservation (Gate 3)

**PROVED under the locked literal standard core convention.**  The
independent implementation regenerated the finite endpoint and one-active
crossing calculations and supplied the omitted two-active argument.

- 293 three-port structural endpoint types were regenerated; 261 have the
  strict `F` sign and the remaining 32 have `F=0` with strict auxiliary `G`.
- 359 four-port tensor records yielded 981 independently refactored crossing
  minors and no algebraic/sign failure.
- In the two-active case, the rank-one equations give
  `aA=zTt`, `abc=t^2`, and `ABC=T^2`.  The strict endpoint inequalities imply
  `aA > z^2bcBC` for `0<z<1`, contradicting the remaining zero minor.  No
  boundary specialization is used.

This result is conditional on the literal core convention and does not
repair Gate 1, the finite local atlas, or arbitrary-subdivision promotion.
It therefore cannot resurrect the global positive theorem by itself.

## Effect on the active sharpness paper

**NONE.**  The active `W_TC \ S_TC` sharpness proof uses neither the root
atlas nor cut preservation.  Its graphs and semi-directed reductions are
checked directly by the independent sharpness verifier.  These root/cut
artifacts remain forensic evidence for why the former positive manuscript is
quarantined.
