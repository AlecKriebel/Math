# Structural root reduction

Status: **CANDIDATE PROOF — awaiting independent adversarial review**

## Statement

Let `B` be the root-containing local factor of a standard semi-directed
topology in `S_TC`.  Choose any admissible root site `s` of `B`.  Split the
edge at `s`, retain one half-edge as a distinguished state port `i`, and view
the remaining mixed graph as a nonroot factor with incoming port `i`.

On the positive JC locus, the root-factor tensor and this incoming-port tensor
have the same germ after quotienting by positive port-incidence scalings.  The
construction and its inverse preserve the standard mixed graph after deleting
the artificial port.  The incoming lift is a rooted tree-child DAG.

Consequently a complete projective incoming-port atlas also classifies root
factors; no separate root-presentation atlas is required.

## Proof

Fix an admissible rooted presentation at `s`.  Parent choices at the
reticulations are unchanged when ordinary tree arcs are rerooted.  For every
choice, deleting one incoming reticulation arc gives the same unrooted
displayed tree before and after rerooting.  A JC tree with uniform stationary
root distribution is reversible, and its Fourier monomial depends only on
the displayed unrooted edge splits.  Hence moving the root along ordinary
edges changes no displayed-tree distribution.

If the chosen site lies in the interior of an edge with multiplier `x`, split
it into two positive multipliers `x_1,x_2` with `x_1x_2=x`; for example take
`x_1=x_2=sqrt(x)`.  Conversely, suppressing the inserted root replaces the
two multipliers by their product.  Both operations remain in `0<x<1`.

Attach an artificial boundary leaf `i` as the second root child.  For a
Fourier assignment on the genuine ports, its character is forced to be the
XOR of all genuine port characters.  The artificial arm therefore contributes
only a positive factor

```
a_i^[h_i != 0].
```

Changing the split of the original edge or the artificial-arm multiplier
changes precisely this factor and the reciprocal factor at the new incidence.
It is therefore the incidence-scaling gauge, not a change in the projective
local tensor.  Contracting the artificial port with the uniform root state
recovers the root factor, while exposing it recovers the incoming factor.

The mixed arrowheads are unchanged: only ordinary arcs are reversed, and an
admissible site on an edge entering a reticulation is split in the unique way
whose suppression restores that arrowhead.  Acyclicity, binary bidegrees, and
the LSA condition hold because `s` was admissible.  Finally, `S_TC` says that
every admissible rooting is tree-child, so the chosen incoming lift is
tree-child.  Deleting its artificial leaf and suppressing its root returns
the original standard semi-directed factor exactly.

## What the statement does not claim

- It does not identify a physical root location.
- It does not recover the two physical multipliers used to split one edge.
- It does not say that a merely rooted-tree-child or weakly tree-child factor
  may be lifted at an arbitrary site.
- It identifies root and incoming models only in the projective tensor
  quotient required by bridge peeling.

## Review obligations

The independent review must test ordinary root sites, sites on retained
reticulation edges, path endpoints, all primitive cycle/theta orientations,
and the inverse suppression.  It must reject the statement if any artificial
lift changes an arrowhead, admits a non-tree-child rooting, or introduces a
boundary multiplier `0` or `1`.
