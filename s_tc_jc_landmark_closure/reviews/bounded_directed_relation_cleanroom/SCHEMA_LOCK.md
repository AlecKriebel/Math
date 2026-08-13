# Clean-room schema and theorem lock

## Allowed inputs

The verifier may read only:

1. inert primitive rooted-graph encodings contained in certificate streams;
2. `primary/certificates/support_universe.json`;
3. the six inert invariant templates in
   `strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py`;
4. `primary/seventh_invariant.json` and inert invariant metadata;
5. declared final bounded-relation streams and summaries;
6. declared, already verified fixed-full hard-cover streams and summaries.

It never imports project modules.  In particular, it neither reads nor imports
the primary relation compiler, merger, graph canonicalizer, separator selector,
or relation/hard-cover crosswalk implementation.

## Directed retention theorem

For a fixed ordered quartet deck and invariant family, define the nonzero
signature of a model `M` by

```
S(M) = {i : invariant i has a nonzero pullback on M}.
```

If a relatively open subset of the source model is contained in the target
model, every polynomial identity of the target is an identity of the source.
Consequently

```
source <= target  implies  S(source) subseteq S(target).
```

This direction is necessary only; it is not sufficient.  A stream that drops
a target with `S(source) subseteq S(target)`, or retains one violating the
inclusion, fails the directed prefilter audit.

Every graph/port use is bound to this predicate through an independently
regenerated effective descriptor deck.  For a zero-total quartet assignment
`g`, a split mask `A` and its complement have equal character sums because

```
xor(g_i : i in A) = xor(g_i : i not in A).
```

Accordingly each switching mask is replaced by
`min(mask, 15 xor mask)`.  Physical arcs having equal normalized rows enter
every Fourier monomial with equal exponents, so their multipliers occur only
through their product.  The map

```
(x_1,...,x_k) -> x_1...x_k
```

is onto `(0,1)` and has nonzero differential there.  Zipping duplicate rows
therefore gives the exact effective positive JC image, not a boundary or
diagonal specialization.  Reticulation permutations and parent flips merely
permute inheritance variables or apply `lambda -> 1-lambda`.  The reviewer
minimizes over those operations, groups every graph by the resulting exact
descriptor deck, and recomputes the full invariant signature once per exact
descriptor class.  Thus no second graph can inherit a stored signature solely
because it shares an unverified cache identifier.

The bounded-atlas physical convention of retaining complementary root arcs as
separate variables is also sound for zero/nonzero/sign classification.  The
tensor depends on those variables through their positive product, and the
same product map is a surjective submersion on the open cube.  The clean-room
comparison performs the product quotient only after regenerating each
graph-specific pullback.

## Graph-derived separator requirement

A stored strict separator is accepted only if this reviewer regenerates both
rooted displayed-tree tensors from the two bound graph encodings, pulls back
the named invariant at the named marginal, obtains zero identically on the
source, and obtains the stored strictly signed polynomial on the target (up to
the explicitly certified effective positive path-product coordinate change).
A valid polynomial attached to a different graph relation is rejected.

Every graph record is also revalidated as an LSA-rooted binary DAG, strongly
tree-child at every internal vertex, with at most two reticulations, no
parallel artifact after standard mixed reduction, and at most one triangle in
the bounded local component.  Stored `rooted_valid` and
`standard_strong_local` flags are checked only after these properties are
independently recomputed.

## Isomorphism / ordinary-T requirement

An `isomorphism_or_T` record is accepted only if independently reduced labelled
mixed graphs are isomorphic after retaining all reticulation arrowheads, or
after erasing only the arrowheads internal to an ordinary triangle.  Rooted
presentation equality and a shared target identifier are not substitutes.

## Hard-cover binding requirement

Each pending raw relation must match exactly one fixed-full hard-cover root and
each in-scope root must match exactly one pending raw relation under the
independently reconstructed key consisting of primitive IDs, selected-position
maps, and full source/target provenance.  Graph-only or target-only keys are
insufficient.

The clean-room primitive IDs are hashes of the full inert provenance records;
they do not trust the primary IDs.  It separately proves a bijection between
primary and independently reconstructed IDs, reconstructs every source graph
from `support_universe.json` and its position map, and proves that each target
provenance/position pair names a unique completion graph before building the
pending/root bijection.

## Source-core exhaustiveness

The declared source shards must form an exact, disjoint partition of the core
families and primitive supports for the relevant outgoing count in
`support_universe.json`.  Missing and duplicated core partitions both fail.
