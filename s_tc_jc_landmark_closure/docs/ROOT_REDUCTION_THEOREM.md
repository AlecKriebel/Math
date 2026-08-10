# Structural root reduction

Status: **CANDIDATE PROOF — awaiting independent adversarial review**

## Statement

Let `B` be the root-containing local factor of a standard semi-directed
topology in `S_TC`.  There is an existing leaf-bearing boundary port `i` at
which the topology has an admissible rooting.  Designate that real port as
the incoming port and view every other boundary as outgoing.

On the positive JC locus, the root-factor tensor and this incoming-port tensor
have the same germ after quotienting by positive port-incidence scalings.  No
fictitious boundary state is introduced.  The rerooted presentation is a
rooted tree-child DAG and has exactly the original standard mixed graph.

Consequently a complete projective incoming-port atlas also classifies root
factors; no separate root-presentation atlas is required.

## Proof

Start with any admissible tree-child rooting.  From the root, repeatedly
choose a child that is a tree vertex or leaf.  Finiteness produces a labelled
leaf without ever traversing a reticulation.  The resulting all-tree path
ends in an existing leaf-bearing boundary component of `B`; call its boundary
port `i`.

Move the root down this path to the cut/pendant edge representing `i`.
Only ordinary tree arcs on the path reverse.  At each path vertex the former
tree parent becomes a tree child, while every off-path reticulation edge keeps
its retained arrowhead.  Binary bidegrees, reachability, acyclicity, and the
reticulation arrows are therefore preserved.  The new site is admissible;
because the standard topology lies in `S_TC`, the rerooted presentation is
tree-child.

Parent choices at the reticulations are unchanged by this rerooting.  For
every choice, deleting one incoming reticulation arc gives the same unrooted
displayed tree.  A JC tree with uniform stationary root distribution is
reversible, and its Fourier monomial depends only on displayed unrooted edge
splits.  Hence rerooting changes no complete boundary tensor.

If the chosen site lies in the interior of an edge with multiplier `x`, split
it into two positive multipliers `x_1,x_2` with `x_1x_2=x`; for example take
`x_1=x_2=sqrt(x)`.  Conversely, suppressing the inserted root replaces the
two multipliers by their product.  Both operations remain in `0<x<1`.

The character at `i` is a genuine observable boundary character supplied by
the labelled component on that side.  The zero-sum condition merely determines
it from the other boundary characters; it does not force it to zero.  Moving
the root within the boundary arm refactors that arm multiplier and changes
only the positive incidence factor `a_i^[h_i != 0]`.  This is precisely the
bridge-incidence gauge.  Thus the root and incoming descriptions define the
same projective local tensor germ.

Suppressing the moved root returns the original standard semi-directed factor
exactly.  Conversely, forgetting which real boundary was designated incoming
returns the root-factor description.  No graph reduction beyond the locked
single root suppression is used.

## What the statement does not claim

- It does not identify a physical root location.
- It does not recover the two physical multipliers used to split one edge.
- It does not say that an arbitrary boundary is rootable.  Existence is proved
  by the all-tree child path; the chosen real boundary is part of the witness.
- It does not say that a merely rooted-tree-child or weakly tree-child factor
  may be rerooted at every compatible site.
- It identifies root and incoming models only in the projective tensor
  quotient required by bridge peeling.

## Review obligations

The independent review must test the all-tree-path construction, ordinary
root sites, path endpoints, all primitive cycle/theta orientations, and the
inverse suppression.  It must reject the statement if a chosen real boundary
cannot be rooted without changing an arrowhead or if any edge split leaves
the open parameter domain.
