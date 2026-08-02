# Milestone 3H: complete JC atlas for nonroot theta blobs with three outgoing ports

## Why this case is necessary

Milestones 3E--3G classify every reduced nonroot theta tensor having four
outgoing ports and one distinguished incoming port.  Strong theta blobs need
not have four outgoing ports: three of the four orientation cores admit
strong expansions with only three.

With three outgoing ports, the incoming state gives only a four-port tensor.
There is no spare outgoing block on which to apply the five-port witness
theorem.  This is therefore the smallest remaining place where a stackable
non-triangle ambiguity could have survived.

## Exhaustive construction

Start from the four exact oriented theta cores of Milestone 2.  If a core has
`s` path-sink reticulations, those sinks already provide `s` outgoing ports.
Distribute exactly `3-s` ordinary tree-port vertices among all directed core
segments, preserving their order, and retain precisely the strong binary
expansions.

Turn the core source into a nonroot tree vertex by adding an incoming edge.
For finite tensor encoding, subdivide that incoming edge by a new global root
and attach incoming leaf `4` as its other child.  Label the three outgoing
ports by `1,2,3` in every possible way and quotient by rooted labelled graph
isomorphism.

**PROVED.** This generates every binary strongly tree-child nonroot level-2
theta blob with exactly three outgoing ports.  Milestone 2 proves that every
such blob contracts to exactly one orientation core and that every ordinary
port lies on one directed core segment.  Fixing the total port count forces
the weak-composition enumeration above; no additional local vertex type is
possible.

**EXACTLY COMPUTED.** The enumeration has 42 raw core-subdivision
distributions and 30 labelled rooted isomorphism classes.  Their 30 labelled
semi-directed topologies are pairwise distinct.

| core index | labelled candidates |
|---:|---:|
| 0, `TT-nested` | 12 |
| 1, `TT-separated` | 0 |
| 2, `TR-nested` | 6 |
| 3, `TR-separated` | 12 |

The absent core requires at least four outgoing ports under strong
tree-childness.  Of the 30 candidates, 18 have one triangle and 12 are
triangle-free.

## Exact reduction to the root atlas

Suppress the degree-two artifact at the added global root while retaining
the reticulation directions.  Incoming leaf `4` then becomes an ordinary
labelled port at the old core source.

**EXACTLY COMPUTED.** Canonical coloured-graph comparison maps every one of
the 30 candidates to a unique semi-directed topology in the complete
four-leaf root-spanning atlas.  No topology is missing and no two of the 30
candidates map to the same labelled semi-directed graph.

**PROVED.** This graph correspondence gives equality of complete open JC
images under reversible root relocation.  On any edge carrying effective
multiplier `z in (0,1)`, the rational split

\[
u=\frac{1+z}{2},
\qquad
v=\frac{2z}{1+z}
\]

lies in `(0,1)^2` and satisfies `uv=z`.  Fourier contraction depends only on
that product.  Conversely, two open split multipliers contract to their open
product.  Reticulation directions and inheritance parameters are unchanged.

Thus the certified root-atlas dimensions, invariants, and overlap maps apply
to the present port tensors without an inference from topology alone.

## Observational components

**EXACTLY COMPUTED.** The 30 topologies map to exactly 21 root-atlas
observational components:

| component size | number | generic dimension | relation |
|---:|---:|---:|---|
| 2 | 9 | 8 | ordinary triangle redirection `T` |
| 1 | 12 | 9 | singleton |

Direct semi-directed graph comparison finds exactly nine `T` pairs, and they
are precisely the nine size-two observational components.  No larger class
occurs.

**PROVED.** Every `T` pair has a full-dimensional regular stochastic overlap
by the exact triangle port-tensor map and reversible root relocation.  Every
distinct equal-dimensional component has a different exact root-atlas
signature, so its irreducible closure is different.  Hence

\[
N\bowtie_{\rm JC}N'
\quad\Longleftrightarrow\quad
N,N'\text{ are labelled-isomorphic or differ by }T
\]

throughout this complete three-outgoing-port atlas.

## Unequal-dimensional pairs

There are `9*12=108` ordered dimension-eight-to-dimension-nine component
pairs.  The outgoing-label group `S_3`, fixing incoming label `4`, partitions
them into 18 free orbits of size six.

**EXACTLY COMPUTED.** For every orbit representative, an existing root-atlas
invariant has zero pullback on the smaller model and a completely factored
nonzero pullback on the larger model.  The selected invariant degrees are two
or three, except that no higher-degree identity is needed.

Seventeen target factors consist only of positive monomials and factors of
the forms

\[
x-1,\qquad x+1,\qquad xy-1.
\]

The remaining target has one additional factor

\[
x\bigl(\lambda y+(1-\lambda)z\bigr)-1,
\]

which is strictly negative on the open cube.

**PROVED.** Every selected target pullback is nonzero throughout its complete
open JC parameter space.  All 108 unequal-dimensional stochastic image pairs
are therefore disjoint, and no one-sided generic stochastic containment
occurs.

## Primary theorem

Let `A_3` denote the complete class of reduced binary strongly tree-child
nonroot level-2 theta blobs with exactly three labelled outgoing state ports
and one distinguished incoming state port.

**PROVED.** For `N,N' in A_3` under JC:

1. `N bowtie_JC N'` if and only if they are labelled-isomorphic or differ by
   ordinary triangle redirection `T`;
2. distinct unequal-dimensional models have disjoint complete open
   stochastic images;
3. no non-triangle local move or one-sided stochastic containment occurs.

Together with Milestones 3E--3G, `T` is now the complete generic move system
for both possible reduced nonroot witness sizes, three and four outgoing
ports.

The port leaves may be replaced by identical positive external components:
the Fourier gluing theorem preserves every overlap, while its analytic inverse
recovers the local tensors on a regular open set.

## Machine replay

- `src/verify_jc_three_outgoing_nonroot_atlas.py` regenerates the 42 raw
  expansions, all 30 labelled candidates, every graph correspondence, all
  `T` pairs, all component dimensions, and all 18 strict directed
  certificates.
- `certificates/jc_three_outgoing_nonroot_atlas.json` stores every complete
  network encoding, root-atlas assignment, observational component, selected
  invariant, and exact target factorization.
- The root-relocation and triangle-redirection correspondences are replayed
  independently by the earlier exact verifiers consumed by the full suite.

No numerical optimization, approximate algebra, external generator
catalogue, specialized phylogenetic software, or literature search is used.

## Next step

**PROVED.** The reduced nonroot local atlas is now closed at both minimal
port counts relevant to a bounded-witness argument.

**UNRESOLVED.** The next theorem must show that every arbitrary longer port
chain has a three- or four-outgoing-port induced restriction preserving any
putative non-`T` ambiguity.  That combinatorial/statistical subdivision
reduction, followed by blob-tree recovery, is the remaining bridge to `L_1`.
