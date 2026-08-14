# Theorem and proof map

## Exact theorem

Let `N,N'` be leaf-labelled binary, LSA-valid, already-simple,
reticulation-preserving semi-directed strongly tree-child level-2 networks.
Every edge multiplier and inheritance probability lies strictly in `(0,1)`.
Then

```text
N preceq_JC N'
  iff
the labelled reduced bridge trees agree and every corresponding nontrivial
blob is labelled-isomorphic or differs by ordinary triangle redirection T.
```

The same condition characterizes symmetric full-dimensional regular overlap.
Thus no proper one-sided generic containment exists. Outside a topology-
dependent proper algebraic exceptional set, an exact JC distribution
determines the standard semi-directed topology modulo `T`.

The boundary is sharp. For every `n >= 4`, two triangle-free networks in
`W_TC \ S_TC` have a common full-dimensional regular open JC germ of dimension
`2n+1`, while remaining labelled nonisomorphic. A second triangle-containing
family has common dimension `2n`.

## Convention lock

The semi-directed graph is formed once: retain arrowheads entering
reticulations, undirect all other arcs, delete the binary root, and join its
children. The result must already be a simple binary mixed graph and preserve
every reticulation. No iterative cleanup and no hidden rooted refinement is
used to enlarge the admissible-rooting set. Strong tree-childness means that
every admissible rooting of this fixed graph is tree-child; equivalently, the
fixed graph has no omnian.

## Necessity chain

1. **Primitive universe.** The exact excess-degree identity
   `sum(deg_B-2)=2(r-1)` reduces every biconnected subcubic level-2 blob to a
   cycle or theta without suppressing port-bearing vertices in the count.
   Source/sink events are retained and all other port subdivisions become
   ordered edge words. Four directed theta event patterns exhaust the strong
   presentations. Simplicity plus no omnians excludes two triangles in one
   blob.
2. **Pointwise cuts.** True bridges give rank-one blocks in four character
   sectors. A crossing-quartet lemma reduces every wrong full split to a
   quartet marginal with one active component or one effective bridge between
   two active endpoints; its Fourier flattening is a submatrix of the full
   one. Exact strict minors handle the one-active cases. In the two-active
   case, identities involving `abc=t^2`, `ABC=T^2`, and `Aa=Tt` force both
   endpoint trinet polynomials to vanish, contradicting the strict open-domain
   inequality.
3. **Projective peeling.** Positive rank-one uniqueness recovers local tensor
   orbits. The exact kernel is the full incidence action
   `P_v -> P_v product a_{v,e}` and
   `x_e -> x_e/(a_{u,e}a_{v,e})`.  The physical fibre is the ambient orbit
   intersected with the complete open physical realization locus, including
   all local-arm, bridge, and inheritance constraints.
   Local analytic slices live in the incidence-saturated tensor space; no
   physical bridge-length recovery is claimed.
4. **Local atlas.** Each theorem object binds the complete source graph,
   target graph, direction, incoming roles, port correspondence, and graph-to-
   polynomial transport. Primary and clean-room implementations regenerate
   displayed switchings, descendant masks, Fourier tensors, separators,
   signs, and Jacobian ranks. Every bounded relation is separated or is
   labelled isomorphism/`T`, in both containment directions.
5. **Arbitrary subdivisions.** Effective path products have nonzero
   differential on `(0,1)`. A common rigid anchor, one-port localization, and
   overlapping two-port comparisons reconstruct one coherent total word on
   every segment and one coherent triangle choice.
6. **Localization.** Intrinsic projective extraction maps any global
   source-open containment to one source-full local containment per
   corresponding blob. Finite semialgebraic stratification avoids assuming a
   continuous target parameter choice. Distant blobs cannot cancel a local
   projective separator.

## Sufficiency chain

Labelled isomorphisms use the identical local tensor germ. The three ordinary
triangle orientations have one exact strict common tensor point and nonzero
rank-four minors, hence a common local regular germ. Finitely many local germs
are shrunk simultaneously. Positive incidence representatives and common
effective bridge scales are then selected so that every physical bridge
multiplier remains in `(0,1)`. Because the bridge graph is a tree, the scaling
choices are independent and have no holonomy. Tensor contraction produces a
common global germ of full model dimension.

## Generic reconstruction

Fourier split tests recover the bridge tree. Positive block factorizations
recover projective local orbits. The bounded invariant deck selects one rigid
support, and coherent probes restore all port orders. The algorithm returns
the lexicographically least admissible `S_TC` member of the recovered `T`
class. It does not return physical bridge multipliers or assert that every
triangle orientation realizes every generic distribution.

## Sharpness certificates

The triangle-free Omega pair has cycle deck `[4,4,6]`, seven admissible
rootings and two tree-child rootings per fixed mixed graph, all 256 Fourier and
inverse-pattern coordinates equal at a strict rational point, and exact model
and intersection dimension nine. Identical cherry substitution adds two
dimensions per taxon, giving `2n+1`.

The Theta pair is a distinct triangle-containing pendant transfer. Its frozen
certificate verifies a strict quadratic common point, all 256 Fourier
coordinates, and rank eight. The same substitution gives dimension `2n`.

## Focus questions for a human specialist

1. Does the corrected excess-degree argument fully justify the cycle/theta
   universe while retaining directed source and reticulation-sink events?
2. Does the crossing-quartet lemma cover every noncut split and transfer the
   quartet rank obstruction correctly to the full flattening?
3. Does sectorwise rank-one peeling prove that the bridge fibre has no gauge
   beyond the full incidence action?
4. Is the Omega rank-nine upper bound transparent from the rank-six core,
   four pendant directions, and the displayed Euler dependency?

This packet records code-independent AI-assisted replay; it does not claim
that a human specialist has performed this review.
