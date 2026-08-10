# Preserved rooting-census implementation failure

**Status: EXACTLY COMPUTED, corrected before use.**

On 2026-08-10 the independent incoming-boundary verifier failed with

```text
AssertionError: ('unexpected rooting census', (9, 0), (9, 0))
```

The cause was local to the review implementation: its final
`all_rooting_census` check imposed the tree-child child condition on every
vertex in `vertices0`, including boundary leaves.  Since leaves have no
children, this forced the strong-rooting count to zero for every graph.  The
separate `rootable_ports` implementation already restricted the check to
internal vertices and was unaffected.

The correction replaces the iteration domain by
`vertices0 - port_vertices`.  The failure is retained here so the original
discrepancy is not erased.  The corrected verifier must reproduce the expected
exact census `(9, 9)` on both sides before this review artifact is accepted.
