# Milestone 2: complete reduced level-2 generator atlas

## Conventions

Fix a nontrivial blob `B`.  Delete every component beyond a cut edge but mark
its attachment at `B` as a port.  Suppress only ordinary tree vertices that
carry no port.  Reticulations, the unique entry/source, and all branch vertices
are retained.

An ordinary side vertex has degree two inside `B` and one outgoing cut-edge
port.  A branch vertex has degree three inside `B` and no port.  The global
root has degree two and is retained during the rooted orientation census; it
is suppressed only when the final semi-directed topology is formed.

## Unique entry and reticulation count

**PROVED.** Every non-root blob has exactly one incoming cut edge.  Indeed, the
bridges and blobs form a tree after contraction.  The unique bridge on the
path toward the global root must point into the blob; any other incoming
bridge would give two paths toward the root, while an outward bridge pointing
back into the blob would contradict reachability or acyclicity.

The head of that incoming bridge is a tree vertex.  If it were a reticulation,
its other parent would lie inside the blob.  A root-to-that-parent path would
have to enter through the reticulation and later return to it, creating a
directed cycle.

**PROVED.** The cyclomatic number of a blob equals the number of its
reticulations.  For a non-root blob with `t` tree vertices, `r`
reticulations, `v=t+r`, and one incoming bridge, summing internal indegrees
gives

\[
e=t+2r-1=v+r-1,
\qquad
e-v+1=r.
\]

The same formula holds for a root-containing blob: the root contributes
indegree zero and there is no incoming bridge.

## Undirected cores

**PROVED.** There are exactly two reduced undirected level-2 templates.

- Cyclomatic number one gives a cycle.
- Cyclomatic number two gives a theta graph: two branch vertices joined by
  three side paths.

For the second claim, suppress all degree-two side vertices temporarily.  A
remaining core vertex has degree three.  With `mu=2`,

\[
e=v+1,
\qquad
3v\le 2e=2v+2,
\]

so `v<=2`.  The one-vertex loop possibility is incompatible with degree three
and the original binary structure.  Hence `v=2,e=3`, which is precisely the
three-edge theta multigraph.  Unsuppressing its sides recovers every binary
blob.

The uncoloured template automorphism groups have orders four for the
two-sided cycle template and twelve for theta (`S_2` on branch vertices and
`S_3` on sides).

## Orientation events on a theta

Retain only these special vertices on the three paths:

- `S`: the unique degree-two source, either the global root before suppression
  or the tree vertex receiving the incoming bridge;
- `X`: a degree-two reticulation sink whose outgoing cut edge leaves the blob;
- `T`: a tree branch;
- `R`: a reticulation branch.

**PROVED.** A path reticulation must be an `X`.  It cannot receive an incoming
cut edge by the entry argument above, so its two path edges are its two parent
edges and its child edge leaves the blob.

**PROVED.** At most one branch is a reticulation.  If both branches were
reticulations, every internal vertex would have positive outdegree, so the
finite internal DAG would have no sink.

Along a path, orientations can change only at `S` (two arrows outward) and at
`X` (two arrows inward), so the event word must alternate.  Up to reversal of
the two branches and permutation of the three paths, exhaustive case analysis
gives exactly four theta orientation cores:

| ID | Branches | Three path-event words | Automorphisms | Minimum strong ports |
|---|---:|---|---:|---:|
| `theta-TT-nested` | `T,T` | `empty ; SX ; X` | 1 | 1 |
| `theta-TT-separated` | `T,T` | `S ; X ; X` | 4 | 2 |
| `theta-TR-nested` | `T,R` | `empty ; empty ; SX` | 2 | 2 |
| `theta-TR-separated` | `T,R` | `empty ; S ; X` | 1 | 2 |

Here a word is read from branch `U` to branch `V`; reversing both branches
reverses every word.  The only additional alternating allocation is
`XSX ; empty ; empty` in the `T,T` case.  Its two empty paths must orient in
opposite directions to meet the branch degrees, producing a directed cycle.
It is therefore inadmissible.

**EXACTLY COMPUTED.** Direct enumeration produces 24 valid oriented labelled
templates before quotienting by branch and path symmetries and exactly the
four rows above afterward.  The executable census also reconstructs every
directed segment and checks acyclicity and reachability from `S`.

## Cycle orientation

**PROVED.** The cycle has one source `S` and one sink reticulation `X`; both
sides orient from `S` to `X`.  This is the unique cycle orientation core up to
interchanging the two sides.  Its oriented template automorphism group has
order two.

## Strong tree-child expansions

**PROVED.** Every full binary strongly tree-child blob is obtained from one of
the five oriented cores by subdividing directed segments with ordered chains
of ordinary tree port vertices, subject to:

1. every tree vertex has a tree/leaf child;
2. a branch reticulation's child is not a reticulation;
3. no two unsubdivided sides create parallel arcs or a directed 2-cycle.

Every inserted ordinary side vertex has an outgoing cut-edge child.  That
child must be a tree vertex or leaf by the same unique-entry argument, so the
inserted vertex automatically satisfies tree-childness.

The exact enumerator computes the minimum number of mandatory tree-port
subdivisions as `1,1,2,2,2` for the cycle and the four theta rows in table
order.  It also lists every minimum repair set, rather than only the count.

Conversely, contracting all ordinary port chains in any strongly tree-child
level-2 blob leaves its unique `S`, its reticulations, and its branch vertices,
and therefore lands in exactly one table row modulo its stated automorphism
group.  This proves exhaustiveness and reconstruction of all subdivisions.

## Finiteness qualification

**PROVED.** There is no finite list of fully port-labelled blobs if individual
ports are retained: an arbitrary number of leaf-bearing ordinary vertices may
be inserted along any side.  The finite object is the five-row orientation
core atlas together with the regular-language expansion rule by ordered port
chains.  This is the precise finite-generator statement used in subsequent
local classification.

## Triangle count

**PROVED.** For a theta with side lengths `l1,l2,l3`, the three cycle lengths
are `l1+l2`, `l1+l3`, and `l2+l3`.  A triangle is therefore exactly a pair of
sides of lengths one and two.  This arithmetic detects the subclasses with
zero, one, or multiple triangles directly from the port-chain lengths.

## Certificate boundary

**EXACTLY COMPUTED.** `src/enumerate_theta_orientation_cores.py` performs the
complete finite event allocation, orientation, acyclicity, reachability,
automorphism, and minimum-repair census.

**EXACTLY COMPUTED.** `src/verify_generator_atlas.py` checks the census against
the machine-readable atlas and replays the reduced-core degree bound.

**UNRESOLVED.** This generator theorem is combinatorial.  The JC stochastic
atlas comparing every port placement and every pair of these orientation
families is Milestone 3 and is not implied by the present census.

