# Independent derivation lock

Timestamp: 2026-08-09 21:32 PDT

This file records the reviewer's mathematical model **before** reading any
primary implementation.  Subsequent comparisons may not silently alter these
definitions; any alteration must be logged as a correction to this lock.

## 1. Clean graph model

A rooted binary network has roles

- root `(0,2)`,
- tree `(1,2)`,
- reticulation `(2,1)`, and
- labelled leaf `(1,0)`.

It is checked directly for simplicity, reachability, acyclicity, the LSA
condition, and tree-childness.  Its narrow semi-directed image deletes and
suppresses only the root, retains an arrowhead exactly at each reticulation
endpoint of an incoming arc, and otherwise forgets arc directions.  A mixed
graph is standard-strong only if it has an admissible rooting and **every**
admissible rooting is tree-child.  The independent implementation will census
rootings; it will not assume the local arrow-tail criterion.

## 2. Root-move derivation

Let `r=v_0 -> v_1 -> ... -> v_k -> leaf` be a path obtained by always taking
a tree/leaf child.  Every traversed edge is ordinary.  Rerooting on the final
real leaf-bearing cut edge reverses this chain, suppresses the old bivalent
root, and preserves every reticulation parent edge.

Potential cycle obstruction: a new cycle would need an old forward path
between two chain vertices in addition to the chain edge(s).  Its first
re-entry into a chain tree vertex would be a second old parent, impossible;
re-entry into an ancestor would already give an old directed cycle.  Thus the
move is acyclic.  The selected cut side and its complement both contain a
labelled leaf; otherwise a proper descendant on the selected chain would be a
stable ancestor of all leaves.  Hence the new root is again the LSA.  The old
root suppression is exactly the original narrow suppression, including an
arrowhead on its off-path reticulate child if present.

For each displayed-tree choice the parent choices are unchanged.  The old two
root-adjacent multipliers are replaced by their product, and the new root site
multiplier is split into two factors.  Uniform JC is reversible, so the
unrooted displayed split monomial is unchanged.  For every `0<x<1`, the exact
choice `sqrt(x),sqrt(x)` remains open, and products of open multipliers remain
open.  This predicts that the graph and JC portions of root reduction are
true; exhaustive finite root-site tests and a symbolic displayed-tree check
remain required.

## 3. Primitive-kernel derivation

For a nonroot factor with one incoming boundary, internal indegree counting
gives `e=t+2r-1=v+r-1`, hence blob cycle rank `r`.  A biconnected subcubic
rank-two graph, after suppressing ordinary unported degree-two vertices, has
two degree-three branch vertices joined by three internally disjoint paths:
a theta kernel.  Rank one gives a cycle kernel.

After choosing the incoming boundary, contract ordinary port-word vertices
but retain:

- `S`: the degree-two-in-the-blob tree vertex with the incoming boundary;
- `X`: a degree-two-in-the-blob reticulation whose child is an outgoing port;
- a reticulate branch vertex, if present.

With two reticulations, either both branch vertices are trees and the event
multiset is `{S,X,X}`, or one branch is reticulate and the path-event multiset
is `{S,X}`.  Two reticulate branches are to be rejected by direct orientation
exhaustion.  Exhausting event distributions and edge orientations, modulo
branch/path symmetry, is predicted to give two classes in each case
(`nested` and `separated`), hence four theta cores.  The rank-one analogue is
one cycle class with events `{S,X}`.

## 4. Strong repairs and rigidity

In the narrow mixed graph, each reticulation has two incoming arrowheads.  A
reticulation-edge tail is strong exactly when its other two incidences are
undirected.  Subdividing a directed core segment immediately before its
reticulate endpoint by a tree vertex carrying an outgoing port repairs that
tail.  Minimal repairs are therefore computed as inclusion-minimal occupied
segment sets satisfying the tail condition, not read from a table.

The expected support is the incoming port (distinguished but not counted),
all path-sink child ports, and one distinctly labelled port on each segment
of a minimal repair.  The verifier will construct every minimal repair and
enumerate every mixed-graph automorphism fixing all port labels pointwise.
The claim passes only if every admissible primitive has a support of outgoing
size at most four with trivial pointwise stabilizer.

For arbitrary added labels, one-port decks need not determine pair order.
The verifier must record those ambiguities honestly and test that explicit
support-plus-two parent transports fix every same-segment pair order.

## 5. Marginal-submersion criterion

For a fixed displayed-choice indexing, restrict every edge's descendant mask
to the selected ports.  Normalize every complete switching row by sending
the empty and full masks to zero and identifying a nontrivial split mask with
its complement.  Edges with identical nonzero normalized zero-sum JC
indicator rows form a partition, and each surviving effective edge coordinate
is the product of one signature class; all-zero rows are tensor-invisible.
Together with retained/permuted inheritance
coordinates, this map is a product of maps on disjoint variable blocks.  Its
Jacobian has full row rank everywhere in the open cube, and every effective
multiplier has an open positive root factorization.

This proves the stated submersion only when the selected reduction really is
represented by those signature classes and inherited choice coordinates.
If reduction merges displayed choices, an effective multiplier can instead
be a convex expression such as `lambda*a+(1-lambda)*b`; that map may still be
a submersion, but the published product-only proof would not cover it.  The
review must determine from the completion artifacts whether such mergers are
excluded, encoded with zero-character dummy ports, or left untreated.

## 6. Probe-coherence falsification criteria

Trivial pointwise stabilizer makes an isomorphism of the fixed labelled
support unique.  One-port overlaps must then agree on segment placement, and
two-port overlaps must agree on pair order.  This is sufficient only if:

1. every probe contains the same core-preserving support on both sides;
2. the atlas relation fixes the same labelled target support, rather than
   choosing different embeddings; and
3. triangle redirections created only after suppression cannot be chosen
   inconsistently.

For (3), if an added label subdivides an edge of the support triangle, that
probe has no triangle and must force literal orientation agreement.  If no
added label subdivides the triangle, the triangle persists in the full graph
and one global `T` remains legitimate.  The independent deck reconstruction
must explicitly test this case split; “at most one triangle” alone is not
accepted as a complete coherence proof.

## 7. Automatic one-triangle derivation

For a theta with positive integer path lengths, two triangular cycles require
`(1,1,2)` or `(1,2,2)` up to order.  The first has parallel branch edges and
violates simplicity.  The second is `K4-e`.  With two reticulations there are
four incoming reticulation incidences.  Tree-childness lets no tree vertex
tail two such edges and no reticulation tail one, so four distinct
nonreticulate tails are required.  `K4-e` has only two nonreticulate vertices.
Thus it has no tree-child admissible rooting.  A direct exact rooting census
will be the certificate.

## 8. Added audit obligation: intrinsic selected strength

Added 2026-08-09 21:39:19 PDT at the user's request.

For every selected port set, strength will be recomputed on the **intrinsic
selected restriction** after deleting unselected pendant components and
performing only the declared selected-restriction reduction.  The test is:

1. construct the reduced mixed graph without dummy leaves;
2. require at least one admissible rooting; and
3. enumerate every admissible rooting and require each to be tree-child.

No selected graph will be called strong because a particular completion can
place dummy leaves at missing roles.  The proposed combinatorial criterion

> all path-sink child ports are selected, and at least one complete
> inclusion-minimal repair set is occupied

will be compared bidirectionally with the intrinsic census.  The comparison
will range over every alternate minimal repair set, their supersets, patterns
that mix proper subsets of distinct repairs, and the rank-one cycle core.
Each mismatch will be serialized before any interpretation or correction.

## 9. Added audit obligation: simultaneous-label quotient

Added 2026-08-09 21:58:44 PDT at the user's request.

Let the outgoing-label symmetric group act simultaneously on a directed pair
`(source,target)`.  If the source support is fixed at the identity labelling,
then every orbit has a representative `(source_identity, sigma(target))`:
apply the inverse of the source labelling permutation to both sides.  This is
an exhaustive transversal for labelled directed relations provided that:

1. the source's **pointwise labelled** stabilizer is trivial;
2. all target permutations, not merely role-preserving permutations, are
   enumerated;
3. the incoming port is genuinely distinguished and is not included in the
   outgoing permutation action; and
4. canonicalization does not forget sink/repair labels or replace literal
   automorphisms by a larger `T` equivalence before the orbit is formed.

If the source has a nontrivial setwise stabilizer, identity anchoring remains
surjective but target permutations can be duplicated; if it has a nontrivial
pointwise stabilizer, graph transports may be nonunique and probe coherence
can fail even though the orbit coverage count looks complete.  The verifier
will compute the action and stabilizers directly for every primary support
record and compare the observed target permutation orbit with the full
factorial orbit.  Role labels will be treated as ordinary taxon labels: no
sink/repair partition is allowed to restrict the target permutation set.

## 10. Added audit obligation: incoming-role coverage

Added 2026-08-09 after the fixed-incoming objection, before re-inspecting the
implementation's label action for this issue.

Root reduction proves only

```text
R(H) != empty and R(H') != empty,
```

where `R(H)` is the set of real boundary ports whose pendant edge is an
admissible root site.  For a fixed physical boundary matching `pi`, using one
structural incoming position on both sides requires the stronger intersection

```text
R(H) intersect pi^{-1}(R(H')) != empty.
```

There is no set-theoretic implication from the first line to the second.
`S_TC` constrains every rooting that exists; it does not make every real
boundary rootable.

The clean census must therefore compute `R(H)` directly for every alternate
minimal support and every boundary bijection.  A predicted smallest
obstruction is a TT-nested support with one occupied minimum-repair segment:
its incoming and repair leaves are rootable, while its two path-sink child
leaves are not.  A second labelled copy can place the same four physical
labels so that its rootable pair is the first copy's sink pair.  If confirmed,
the outgoing-only quotient misses this relative role and the atlas must keep
the structural root port separate from physical port labels and enumerate the
full target boundary permutation group.
