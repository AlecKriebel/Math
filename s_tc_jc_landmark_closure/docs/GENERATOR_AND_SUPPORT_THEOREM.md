# Generator and bounded-support theorem

Status: **PROVED; independently regenerated finite files are regression
certificates, not premises**

## Theorem 1 — primitive universe

Every nontrivial blob of a binary standard semi-directed level-2 topology,
after deleting cut-edge components while retaining their attachment ports and
contracting ordinary port-free degree-two paths, has one of five directed
cores: one cycle core or one of four theta orientation cores.  Every full
factor is recovered by finite ordered port words on the directed core
segments and by one outgoing port at every path-sink reticulation.

### Proof

Choose an admissible rooting and expose the unique incoming boundary of a
nonroot factor.  That boundary cannot enter a reticulation: the two
root-to-parent paths of an incoming reticulation edge give an undirected
bypass, so such an edge is not a cut edge.  The boundary therefore meets the
unique local tree source.  If the factor has `t` tree vertices, `r`
reticulations, `v` internal vertices, and `e` internal edges, summing internal
indegrees gives

```
e = t + 2r - 1 = v + r - 1,
```

so its cyclomatic number is `r`.  The same calculation holds for a
root-containing factor before root suppression.  Cyclomatic number one gives
a cycle.  At cyclomatic number two, suppress every degree-two side vertex.
Every surviving core vertex has degree three.  Since `e=v+1`,
`3v <= 2e = 2v+2`, and hence `v<=2`.  Biconnectedness and the simple binary
lock exclude the one-vertex loop case, leaving two branch vertices joined by
three paths: a theta.

On a theta path, direction can change only at the unique local source event
`S` or at a path-sink reticulation `X`, so source and sink events alternate.
At most one pole is reticulate.  Indeed, if both poles were reticulations,
each would have two incoming path incidences and one outgoing path incidence.
The path carrying the outgoing incidence of the first pole must enter the
second pole, and symmetrically the outgoing incidence of the second must enter
the first.  Those two directed pole-to-pole paths form a directed cycle.

There are therefore two cases.  If one pole is reticulate and the other is a
tree pole, the second reticulation is an internal path sink and `S` is an
internal source.  Up to permuting the three paths and swapping the poles,
`S` and `X` lie on different paths (`theta-0`) or on the same path
(`theta-1`).  If both poles are tree poles, both reticulations are internal
path sinks.  Up to the same symmetries, `S` lies on the third path
(`theta-2`) or shares a path with one sink (`theta-3`).  These four cases are
mutually exclusive and exhaust the possible event incidences, proving the
four-core assertion without a topology census.

The minimum strong repairs are read directly from the four arc templates.
They remove a reticulation child of a reticulation, split a parallel core
pair, or give a nonreticulate child to an omnian tail, as applicable:

| core | directed segment indices | minimum repairs |
|---|---|---|
| cycle | `S->X`, `S->X` | `{0}`, `{1}` |
| `theta-0` | `S->U,S->V,U->X,V->X,U->V` | `{2,3}`, `{3,4}` |
| `theta-1` | `S->U,S->X,V->X,U->V,U->V` | `{2,3}`, `{2,4}` |
| `theta-2` | `S->U,S->V,U->X0,V->X0,U->X1,V->X1` | `{2,3}`, `{2,5}`, `{3,4}`, `{4,5}` |
| `theta-3` | `S->U,S->X0,V->X0,U->X1,V->X1,U->V` | `{2}`, `{4}` |

For example, in `theta-0` segment 3 separates the two reticulations, while
segment 2 or 4 supplies a nonreticulate child at the other offending tail.
The other rows follow by the same two local tests.  Occupancy is monotone, so
every strong word contains one listed minimum repair and every word
containing one is strong.

Every remaining side vertex has degree two inside the blob and one outgoing
cut-edge port.  Reading these vertices along each directed segment gives an
ordered word.  Contracting the words returns the core, and reinserting them
recovers the full factor uniquely.

## Theorem 2 — the one-triangle condition is automatic in `S_TC`

Every simple binary standard semi-directed strongly tree-child level-2 blob
contains at most one triangle.

### Proof

A cycle blob has only one simple cycle.  A theta with path lengths
`l_1,l_2,l_3` has cycle lengths `l_i+l_j`.  Two triangles force, up to order,
either `(1,1,2)` or `(1,2,2)`.  The first has two parallel branch edges and is
excluded by the simple standard lock.  The second is the graph `K_4-e`.

In a standard-strong mixed graph, one vertex cannot tail two edges entering
reticulations, and a reticulation cannot tail such an edge.  In the final
root-suppressed `K_4-e` mixed graph there are only two nonreticulate internal
vertices, fewer than the four distinct tails required by the two
reticulations.  Equivalently, if the count is made before root suppression,
the two ordinary vertices and the inserted root provide at most three
tree-child-compatible tails, still fewer than four.  This is impossible.

Thus the final positive theorem, if established, applies to all of `S_TC`,
not merely to a separately imposed one-triangle-per-blob subclass.

## Theorem 3 — rigid bounded support

Every strong port-word expansion contains a labelled core-preserving rigid
support `Q`.  Its maximum outgoing size is four.  Support-plus-one and
support-plus-two restrictions reconstruct every complete ordered port word;
therefore every local topological distinction has a witness on at most six
outgoing ports (seven tensor ports including the incoming boundary).

### Proof

Strong tree-childness and simplicity impose a monotone family of occupied
segment constraints.  Every satisfying occupancy contains a minimal repair.
Select one port label on each segment of one minimal repair and every
path-sink child label.  The selected restriction retains the complete core
and remains strong.  The exact repair sizes are:

| Core | Sink ports | Repair ports | Support size |
|---|---:|---:|---:|
| cycle | 1 | 1 | 2 |
| theta TT-nested | 2 | 1 | 3 |
| theta TT-separated | 2 | 2 | 4 |
| theta TR-nested | 1 | 2 | 3 |
| theta TR-separated | 1 | 2 | 3 |

The distinct labels make every minimal support rigid.  Any apparent
path-template symmetry either moves a sink/repair label or exchanges
parallel empty template edges; the latter is absent after the simple repair.

Fix the resulting core identification.  A restriction `Q+p` determines the
directed segment containing `p` and its position relative to any support
anchor on that segment.  A restriction `Q+p+q` determines the order of every
pair on one segment.  These comparisons uniquely determine the total word on
each segment.  Since `|Q|<=4`, at most six outgoing labels are needed.

## Lemma 4 — marginal submersion

For every selected support/probe set, marginalization from the full positive
local model to its reduced selected model is a semialgebraic submersion on a
dense regular open set.

### Proof

Give each full edge its vector of descendant masks over all displayed-tree
choices after unselected ports receive character zero.  Edges with the same
vector occur only through their product.  Distinct signature classes use
disjoint edge sets, and each product map has nonzero differential

```
d(x_1...x_k) = sum_i (product_{j != i} x_j) dx_i
```

throughout `(0,1)^k`.  The product of these maps is therefore a submersion
from the physical parameter cube onto the effective descriptor-parameter
cube; inheritance coordinates are unchanged up to parent complementation.
It is also onto the effective open cube because any effective multiplier has
a positive `k`th-root factorization.  This does not assert that descriptor
coordinates are minimal coordinates on the tensor image.  After a selected
marginal collapses a core, switching columns and inheritance coordinates may
be tensor-redundant.  Only the source core-retaining parameter-cube
submersion is used below.

Hence a full-dimensional arbitrary-subdivision containment projects to a
full-dimensional bounded decorated relation.  This is stronger than the
older dominance-only argument.

## Lemma 5 — probe coherence

Assume the bounded directed atlas identifies every selected relation modulo
labelled isomorphism and ordinary `T`.  Then all support-plus-one/two probes
assemble to one global port-word isomorphism modulo one coherent `T` choice.

### Proof

The pointwise stabilizer of `Q` is trivial, so every probe identification
restricts to the same identification of the core.  Overlapping one-port
probes assign the same segment to each label.  Overlapping two-port probes
give the same pairwise comparisons; these comparisons are the restrictions
of total orders, so they assemble uniquely on every segment.  A `T` choice
does not change the underlying core or any port placement.  If an extra label
subdivides an edge of the support triangle, that one-port probe has no
triangle and forces literal orientation agreement.  Otherwise the same
unique triangle persists in the full graph and one global ordinary `T`
choice applies to every probe.  Canonicalizing that orientation makes all
probe identifications literal and consistent.

For the finite directed atlas one may fix the source support labels once and
enumerate every target port permutation.  Simultaneously relabelling any
decorated source-target relation by the inverse source assignment puts the
source into an anchored form and transports the complete port matching to
one of the enumerated target assignments.  Thus this convention is
surjective onto all labelled directed relations and loses none.  A setwise
source or `T`-quotient automorphism may produce duplicate anchored
representatives; the final decorated-relation canonicalizer removes those
duplicates.  Pointwise rigidity supplies the unique fixed-label core
transport needed by probe coherence, not uniqueness of the anchored
group-action representative.

## Exact primary artifacts

- `primary/core_universe.py` regenerates the primitive cores and repairs.
- `primary/completion_universe.py` regenerates every selected pattern induced
  by a full standard-strong completion and records whether it retains the
  original primitive core.  A nonretaining marginal may reduce to a smaller
  strong topology; it is not called intrinsically weak.
- The exact completion counts for three through six selected outgoing ports
  are `831, 1983, 4155, 7909`; these are implementation checksums of the
  completion grammar, not mathematical inputs.
- `primary/support_universe.py` regenerates all rigid support/probe sources;
  it obtains 304 five-port and 216 six-port decorated source presentations.

No count in this note is a substitute for the pending graph-derived local
algebra or its independent normalized-record comparison.
