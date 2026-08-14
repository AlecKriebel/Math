# Definitions lock

Status: **VERIFIED AFTER CORRECTION by independent convention review**

## Rooted networks

An LSA-valid rooted binary phylogenetic network on a finite labelled taxon set
`X` is a finite directed acyclic graph with no parallel arcs in which the root
has bidegree `(0,2)`, a tree vertex has `(1,2)`, a reticulation has `(2,1)`,
and a labelled leaf has `(1,0)`.  Every vertex is reachable from the root.
The root is the lowest stable ancestor of `X`: it lies on every root-to-leaf
path and no proper descendant does so for every labelled leaf.

A rooted presentation is tree-child when every internal vertex has a child
that is a tree vertex or a leaf.  Equivalently in this binary setting, no
reticulation has a reticulation child and no tree/root vertex has two
reticulation children.

## Reticulation-preserving semi-deorientation `sd_0`

The map `sd_0` marks every arc entering a reticulation, undirects every other
arc, deletes the binary root, and replaces its two incident edges by one edge
between its children while retaining at either endpoint exactly the arrowhead
present before deletion.  A rooted presentation is admissible only when this
single suppression already produces a simple binary mixed graph: no loop or
parallel edge is created and every reticulation and retained incoming
arrowhead survives.  No later degree-two or parallel cleanup is part of
`sd_0`.

This is the already-simple semi-deorientation convention of Englander et al.
and the binary LSA-valid specialization of Holtgrefe et al.  It is not the
broader exhaustive-cleanup map used by Brits et al.; no theorem below
quantifies over every rooted preimage of that broader map.

An admissible rooting of a mixed graph is an LSA-valid rooted binary network
whose `sd_0` image is exactly that graph.  Compatible insertion on an edge
entering a reticulation is allowed when suppression recovers the retained
arrowhead.

Broader reduction after taking a marginal or induced subnetwork is denoted
`red_*`.  It may suppress ordinary unlabelled degree-two vertices and resolve
specified parallel artifacts, but it never defines the rooting universe or
membership in `S_TC`.

## Tree-child classes

- `R_TC`: a chosen rooted presentation is tree-child.
- `W_TC`: a standard semi-directed topology has at least one admissible
  tree-child rooting.
- `S_TC`: the standard semi-directed topology has at least one admissible
  rooting, and every admissible rooting is tree-child.  The existence clause
  prevents vacuous membership of a mixed graph with no valid rooting.

No membership statement transfers between these classes without an explicit
rooting census or a proved local criterion.

For a simple binary mixed graph admitting at least one rooting, the criterion
used below is exact: it is in `S_TC` if and only if it has no *omnian*,
equivalently every tail of a retained reticulation edge is incident with two
undirected edges.  Necessity follows
because a tail with two reticulation edges has two reticulation children in
every compatible rooting.  For sufficiency, a tail with one reticulation edge
has one of its two undirected incidences as a parent and the other as a
nonreticulation child.  A vertex with no outgoing reticulation edge has no
reticulation child, and a reticulation's unique child cannot be a
reticulation, since an edge entering that child would carry an arrowhead.
An inserted root has at most one reticulation child.  Thus every compatible
rooting is tree-child.  The primary implementation checks this local
criterion and independently exhausts all rootings on the primitive cores.

Thus the positive theorem's exact topology class is: simple binary
LSA-rootable semi-directed mixed graphs obtained under reticulation-preserving
`sd_0`, of level at most two, with no omnians.

## Graphs, blobs, and level

Isomorphisms preserve leaf labels, undirected edges, directed retained
arrowheads, and vertex roles.  A cut edge is an edge whose deletion disconnects
the underlying graph.  A blob is a maximal nontrivial biconnected block of the
underlying simple graph.  Equivalently in this binary setting, the nontrivial
blobs are the non-bridge blocks in the bridge decomposition.  A topology is
level two when each blob contains at most two reticulations.

The literal prior-work term *2-sub-blob* means a connected induced subgraph
with no globally cut edge and exactly two vertices adjacent outside.  This is
not automatically a degree-two suppressible object.  An *operational
two-terminal suppressible factor* additionally has exactly two external
incident edges in total, at distinct boundary vertices.  These notions are
kept separate.  The latter cannot occur as a nontrivial factor in `S_TC` at
level two; its only simple whole-blob core is `K4-e`, whose complete LSA-valid
rooting census has no tree-child rooting.

## Ordinary triangle redirection

An ordinary triangle redirection `T` changes only which triangle vertex is a
reticulation and the two arrowheads entering it.  It leaves the labelled
underlying graph, all pendant-component placements, and every arrowhead
outside the triangle unchanged.  `T` denotes the generated local relation;
it does not assert equality of complete stochastic images.

## JC model and observational relations

Every edge has one nontrivial Fourier multiplier `x_e` with `0 < x_e < 1`.
Every reticulation inheritance probability satisfies `0 < lambda_r < 1`.
The root distribution is uniform on `Z_2 x Z_2`.  No boundary multiplier or
inheritance probability is permitted.

Write `M_N^reg` for the distributions having a parameter preimage at which
the network parameterization has rank `dim(M_N)`.  `N bowtie_JC N'` means
that a common distribution lies in both regular loci and has neighborhoods
there whose intersection has the full local dimension of both images.

`N preceq_JC N'` means that there is a source-regular common point and a
relatively open neighborhood of it in the regular source-model locus that is
contained in the target image; the target may have larger dimension.
This is distinct from equality of complex closures, equality of complete open
images, lower-dimensional intersection, and boundary-only relations.
