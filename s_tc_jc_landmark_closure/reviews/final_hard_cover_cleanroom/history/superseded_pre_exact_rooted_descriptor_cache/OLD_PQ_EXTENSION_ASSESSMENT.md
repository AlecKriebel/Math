# Path-bound p/q extension assessment

Status: **VERIFIED AS A CONDITIONAL ENUMERATION LEMMA; VERIFIED END TO END FOR
THE SCHEMA-3 n=4 THETA-2 STREAM**

Fix one full labelled source-target relation and one restoration path ending at
an allowed terminal

```text
A = Q_s union Q_t.
```

Both terminal restrictions retain their primitive cores.  Every boundary
outside `A` is therefore an ordinary port attached at a subdivision vertex of
one directed blob segment on each side.  Subdividing every directed blob arc
by a tree vertex carrying the new label `p` enumerates every possible segment
and every position relative to the existing labels.  Starting from each such
path-bound `p` relation and repeating with `q` enumerates:

- different-segment placements;
- both same-segment orders; and
- placements on a triangle edge before or after an ordinary triangle
  redirection.

The construction carries the original root relation ID, restoration path,
and `Q_t` transport unchanged.  Consequently it cannot mix probe-dependent
support identifications.  With the audited support sizes and at most five
target restoration roles, `|A|+2 <= 12`.

The implementation deliberately distinguishes a canonical child state from
its path binding.  Every raw source/target insertion-arc pair is retained.
The second stage accepts an explicit set of already-classified `p` path IDs;
unapproved `p` states cannot reach `q`.  Canonicalization is performed on one
coloured disjoint union containing both mixed graphs and the complete port
matching, not on a target graph alone.

`verify_pq_extension.py` replays the construction on all eight `n=3` source
supports and all three omitted theta-2 `n=4` minimum supports.  It proves
exact Cartesian arc-pair coverage, both same-segment orders, immutable base
and parent bindings, complete matching, the twelve-port guard, and the locked
standard-strong local criterion.  Its certificate is
`certificates/pq_extension_certificate.json`.

For the corrected schema-3 n=4 theta-2 base terminals, the formerly
conditional algebraic step has now also been completed.  The actual primary
probe stream contains 12,906 p relations and 155,676 q relations.  The
clean-room replay regenerates every child set and classifies all 168,582
relations: 153,072 have exact graph-derived polynomial separators and 15,510
are labelled-isomorphic.  See `SCHEMA3_N4_THETA2_REVIEW.md`.

Every accepted base terminal in that actual stream is triangle-free.  Thus
the end-to-end verification does not certify the special case in which `p`
or `q` lies on an edge affected by a nontrivial ordinary T move.  The general
enumerator emits such positions when its fixed base has a triangle, but their
coherent T classification still requires a triangle-bearing base package.

For any other source/core stratum this remains only an enumeration lemma.  It
does not turn an unresolved base terminal into an allowed one, and it does not
substitute for the missing merged n=3 or unequal-signature classifications.
