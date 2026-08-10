# Generator and bounded-support theorem

Status: **PRIMARY PROOF AND EXACT CENSUS COMPLETE; independent review pending**

## Theorem 1 — primitive universe

Every nontrivial blob of a binary standard semi-directed level-2 topology,
after deleting cut-edge components while retaining their attachment ports and
contracting ordinary port-free degree-two paths, has one of five directed
cores: one cycle core or one of four theta orientation cores.  Every full
factor is recovered by finite ordered port words on the directed core
segments and by one outgoing port at every path-sink reticulation.

### Proof

Choose an admissible rooting and expose the unique incoming boundary of a
nonroot factor.  If the factor has `t` tree vertices, `r` reticulations, `v`
internal vertices, and `e` internal edges, summing internal indegrees gives

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

On a theta path, direction can change only at the unique source event `S` or
at a path-sink reticulation `X`, so source and sink events alternate.  At most
one branch is reticulate, since two reticulate branches would leave the
finite internal DAG without a sink.  Exhausting the event multisets
`{S,X,X}` and `{S,X}`, all segment directions, bidegrees, acyclicity, and
reachability gives exactly four path-template classes.  The primary
enumerator derives 24 normalized branch-labelled presentations and four
classes; it does not read a frozen core list.

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

In a standard-strong mixed graph, the tail of an edge entering a reticulation
must have two other undirected incident edges.  Otherwise some admissible
rooting makes both of that vertex's tree-child alternatives reticulate.  In
particular, one vertex cannot be the tail of two reticulation edges, and a
reticulation cannot be such a tail.  The two reticulations of `K_4-e` require
four incoming arrowed edges with four distinct nonreticulate tails, but the
graph has only two nonreticulate vertices.  This is impossible.

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

throughout `(0,1)^k`.  The product of these maps is therefore a submersion;
inheritance coordinates are unchanged up to parent complementation.  It is
also onto the effective open cube because any effective multiplier has a
positive `k`th-root factorization.

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
does not change the underlying core or any port placement.  Because the core
has at most one triangle and every probe retains the complete core, all local
`T` choices refer to that same triangle.  Canonicalizing its orientation once
makes every probe identification literal and consistent.

## Exact primary artifacts

- `primary/core_universe.py` regenerates the primitive cores and repairs.
- `primary/completion_universe.py` regenerates every weak selected pattern
  induced by a full standard-strong completion.
- The exact completion counts for three through six selected outgoing ports
  are `831, 1983, 4155, 7909`; all generated full completions pass the locked
  rooted and standard-strong checks.
- `primary/support_universe.py` regenerates all rigid support/probe sources;
  it obtains 304 five-port and 216 six-port decorated source presentations.

No count in this note is a substitute for the pending graph-derived local
algebra or its independent normalized-record comparison.
