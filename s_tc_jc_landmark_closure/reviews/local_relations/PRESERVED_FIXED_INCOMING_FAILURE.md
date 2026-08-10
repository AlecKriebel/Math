# Preserved failure: fixed incoming boundary

Status: **FALSE DESIGN, QUARANTINED BEFORE ALGEBRA**

The first clean-room draft fixed the structural incoming boundary on both
sides and permuted only outgoing ports.  Its source hash was
`ecf97bb4e6cf4ef4e140c27b29c9c7c5244cc58dc8bd290d3b40c3529dde451b`.
No theorem-level comparison was run with that draft.

This quotient is not the standard semi-directed relation universe.  A rooted
incoming role is provenance used to validate and parameterize a rooted
presentation; it is not a colour preserved by a labelled semi-directed
isomorphism or containment relation.  With `p` complete real boundaries, the
relative target action is the full symmetric group `S_p`, not the subgroup
`S_{p-1}` fixing the rooted incoming position.

An exact four-boundary TT-nested witness has source structural roles mapped to
physical labels as

```text
incoming -> A, repair -> B, sink X1 -> C, sink X2 -> D,
```

and target roles mapped as

```text
incoming -> C, repair -> D, sink X1 -> A, sink X2 -> B.
```

The relative permutation is `(2,3,0,1)`.  It is in `S_4` and outside the
six-element incoming-fixed subgroup.  The two sides are the same labelled
standard-strong mixed graph, but no physical boundary is rootable on both
presentations.  Thus a common-rooted-incoming reduction cannot repair the
omission.

The rebuilt reviewer:

1. anchors all `p` source boundaries once;
2. enumerates all `p!` relative target boundary permutations;
3. removes rooted incoming status from relation graph colours;
4. retains incoming roles only in raw presentation provenance;
5. explicitly compares the fixed-incoming and full-`S_p` equal-signature
   survivor sets.
