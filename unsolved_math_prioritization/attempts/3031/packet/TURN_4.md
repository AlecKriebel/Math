# Author turn 4: smaller residual gadget and saturation obstruction

2026-10-03 UTC. Status: partial; full-target completion estimate10%, reduced because padding creates an unavoidable secondary target size.

## A deficit 16 gadget avoiding induced deficit 4
Take the proper seven-color one-factorization of K8 from turn 3. In color 0's matching(0,7),(1,6),(2,5),(3,4), recolor the latter three edges to fresh colors7,8,9, making the matching fully rainbow. Recolor color 1's edges(0,1),(3,5) to fresh colors10,11. Exactly12 colors remain on 28 edges, giving total deficit 16.

An induced subset of≤5 vertices has deficit≤3: before the splits, deleting any three vertices leaves all seven original four-edge matching classes represented. Splitting cannot reduce color count, and deficit is monotone with vertex inclusion.

For six vertices, if the deleted pair is not an edge of color 0's matching, at most one of the three color 0 splitting increments remains, and at most two color 1 increments remain. If it is an edge of that matching, at most two color 0 increments remain, but at least one of the two distinguished color 1 edges is deleted: these two edges meet all four color 0 pairs. Thus at most three additional colors appear beyond the original seven, and deficit≥15−10=5. A seven-vertex subset has deficit 10 or11; the full gadget has deficit 16. Therefore induced deficit 4 is absent. The complete256-subset table in `padding_obstruction_checks.json` confirms the proof.

Placed inside a rainbow K22 with common spoke and tail colors, it gives an exact217-coloring avoiding43. At subset sizes10 and 11 the needed deficits are4 and 14, both absent; smaller sizes are too small and larger sizes exceed43. The exact multiplicity-weighted calculation covers all 2^22 subsets.

## Why this does not settle the next whole subfamily
The same gadget inside K24 has c=262. It does not avoid m=64: choose all 8 gadget vertices and 5 filler vertices. This13-vertex subset has palette2+binom(13,2)−16=64. The exact multiplicity-weighted calculation covers all 2^24 subsets and records that witness.

More generally, for any common-spoke rainbow-padding construction whose entire deficit p is supported on h core vertices, the infinite palette spectrum contains 2+binom(t,2)−p for every h≤t≤n. Thus a compact gadget can exclude the targeted k-vertex deficit q while still introducing the same forbidden m at a larger subset size. For(p,q,k)=(16,4,12), every such construction with h≤13 necessarily fails: t=13 gives m=64. A successful construction of this type must distribute its deficit over at least14 vertices; this packet has not produced one. The obstruction is scoped to this padding architecture and is not a proof that P(262,64) holds or that this pair is absent from all prior literature.

The fixed-size palette jump is the failure of the attempted shortcut. We do not promote local deficit avoidance into global m-avoidance.
