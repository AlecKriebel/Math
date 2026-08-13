# Adversarial review of the locked conventions and triangle claim

## Status

- Narrow `sd_0` implementation: **EXACTLY COMPUTED** for the bounded census.
- Frozen weak-pair rooting census: **EXACTLY COMPUTED** and agrees with the
  certified release (five admissible rootings, two tree-child).
- Automatic at-most-one-triangle assertion for a standard weakly tree-child
  level-2 blob: **PROVED** under the locked simple-graph convention.

## Nonvacuity correction incorporated

The current definitions lock now says explicitly that an `S_TC` topology has
at least one admissible rooting and that every admissible rooting is
tree-child.  This removes the earlier possible vacuous reading.  The
clean-room census used that nonvacuous definition from its first run, so no
count or mathematical conclusion changed.  The audited lock has SHA-256
`c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09`.

The lock also records a local tail-incidence criterion for `S_TC`.  Exhaustive
rooting enumeration agrees with that criterion for every rootable mixed graph
through four leaves.  This is an exact bounded regression, not a substitute
for the criterion's structural proof.

A bidirected edge cannot occur in `W_TC` under `sd_0`.  Such an edge can be
recovered only by rooting on that edge, which gives the binary root two
reticulation children and violates tree-childness.  This gives a useful
local convention test.

## At most one triangle per blob

Let a nontrivial blob have cyclomatic number `c`.  In a rooted binary network
the total cyclomatic number is the number of reticulations, and cyclomatic
number is additive over blobs.  Every incoming edge of a reticulation lies on
an undirected cycle, so every reticulation lies in a unique nontrivial blob.
Deleting one incoming edge at every reticulation produces a displayed tree;
restricted to a blob containing `k` reticulations, those `k` deletions make
the blob acyclic.  Hence `c <= k` in every blob.  Summing over blobs gives
equality on both sides with the global reticulation count, so in fact `c=k`
blob by blob.  Thus a level-2 blob has `c=1` or `c=2`.

For `c=1`, the blob is a subdivided cycle and hence has at most one triangle.
For `c=2`, delete cut edges and suppress ordinary degree-two vertices in the
underlying graph solely for this combinatorial argument.  The resulting
biconnected multigraph has minimum degree three and

    sum_v (degree(v)-2) = 2(c-1) = 2.

It therefore has exactly two degree-three vertices and is the theta core:
three internally disjoint paths between two poles.  Write their positive
integer lengths as `a <= b <= c`.  Every simple cycle is the union of two of
the paths.  Two distinct triangles can occur only when

    a+b = a+c = 3,

so the lengths are `(1,2,2)`.  The unsuppressed simple blob is then `K4-e`:
two poles joined directly and through two distinct middle vertices.

It remains to rule out a tree-child rooting of this double-triangle blob.
The two reticulations cannot be adjacent: an oriented edge between them gives
a reticulation a reticulation child, while rooting on that edge gives the root
two reticulation children.  The only nonadjacent vertex pair in `K4-e` is the
pair of middle vertices, so those must be the two reticulations.

Let the poles be `A,C` and the reticulations be `B,D`.  Tree-childness permits
at most one of `B,D` to be a child of `A`, and at most one to be a child of
`C`.  If either reticulation sends its unique outgoing edge through its
external cut edge, it needs both `A` and `C` as parents; then the other
reticulation cannot acquire two parents without making `A` or `C` an omnian.
Hence both external cut incidences must enter their reticulations, and each
reticulation has exactly one pole parent and the other pole as its child.
The only way to give each pole at most one reticulation child is, up to
symmetry,

    A -> B -> C -> D -> A,

a directed cycle.  This contradicts acyclicity.  Therefore the `(1,2,2)`
theta has no tree-child rooting.  A `W_TC` level-2 blob consequently contains
at most one triangle.

Actual parallel edges are excluded by the locked simple `sd_0` convention.
Parallel edges appearing only after the degree-two suppression used in the
core argument are exactly the three theta paths just analyzed; they do not
create an additional case.

## Finite falsification result

The exhaustive simple mixed-graph census with three or four labelled leaves
found no `W_TC` graph having two triangles in one blob.  This is an
**EXACTLY COMPUTED** regression consistent with the proof, not the basis of
the proof.
