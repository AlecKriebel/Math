# Milestone 4C: arbitrary nonroot theta blobs are JC-identifiable modulo `T`

## Main theorem

Let `B` and `B'` be finite port-labelled, strongly tree-child, nonroot theta
blobs with the same distinguished incoming state port and the same labelled
outgoing ports.  Ports may occur in arbitrary number and arbitrary order on
the directed core segments.

**PROVED.** Under the Jukes--Cantor model,

\[
\boxed{
B\bowtie_{\rm JC} B'
\quad\Longleftrightarrow\quad
B,B'\text{ are related by labelled isomorphism and triangle redirection }T.
}
\]

Thus the inherited nontriangle moves `Theta`, `Psi`, and `Omega` are all
root-local on the theta generator.  No stackable nontriangle ambiguity exists
in any arbitrarily subdivided strongly tree-child nonroot theta blob.

This is a complete arbitrary-size local theorem for theta blobs.  It is not
yet a global `L_1` theorem: recovery of the blob tree, comparison with cycle
generators, and exclusion of coordinated changes between blobs remain open.

## Why a further atlas was necessary

Milestone 4A chooses a labelled strong support `Q` in `B`.  Even if `B'` is a
full strong blob, the restriction of `B'` to the same labels may omit a
path-sink child or all selected repair ports on a required segment.  Hence
`B'|Q` need not be strong or core-preserving, and Milestone 4B alone could not
be applied symmetrically.

The remaining task is finite.  If a selected restriction has `k` outgoing
labels, every selected ordinary label occupies one directed core segment and
at most one selected label occupies each path-sink port.  Any omitted sink
child can be supplied by an unobserved leaf.  Any missing tree-child repair
can be supplied by an unobserved ordinary port on a minimal repair segment.
Characters on those unobserved leaves are zero.

Conversely, every such occupancy extends to a full strongly tree-child blob
by exactly this construction.  Therefore it enumerates all weak restrictions
that can be induced from a strong competitor.

## Exhaustive weak-target census

For each oriented core, every subset of selected path-sink ports and every
weak composition of the remaining selected ports over the directed core
segments is generated.  All minimal dummy repairs are replayed.

**PROVED.** The selected marginal is independent of which compatible dummy
repair is used.  A dummy subdivision on one segment has the same four
displayed-tree descendant masks as the other edges in its signature class and
therefore enters only through their product.

**EXACTLY COMPUTED.** The role-presentation census is:

| outgoing ports | `TT` presentations per core | `TR` presentations per core | total |
|---:|---:|---:|---:|
| 5 | 560 | 196 | 1,512 |
| 6 | 1,092 | 336 | 2,856 |

The 1,512 five-port presentations reduce to 427 exact base tensor decks:
92 have a selected pattern that is itself strong and 335 are genuinely weak.
The 2,856 six-port presentations reduce to 1,027 decks: 233 selected-strong
and 794 genuinely weak.  No exact tensor deck is shared between the two
status classes.

## Exact tensor and invariant calculation

The edge-descendant-mask reduction of Milestone 4B applies without change to
dummy leaves.  Across all 4,368 weak role presentations there are only 50
quartet tensor types.  Ten already occur in the strong support atlas; forty
are new.

**EXACTLY COMPUTED.** All sixty root-atlas invariants are pulled back over an
exact rational polynomial ring on every new type, giving

\[
40\cdot60=2{,}400
\]

new symbolic identities.  Together with the inherited 5,400 pullbacks, the
calculation uses 130 explicitly recorded tensor types.  No modular or random
identity test enters the certificate.

Apply all `5!` or `6!` relative outgoing-label permutations and transport the
sixty identities by their exact `S_4` action.

**EXACTLY COMPUTED.** The complete zero/nonzero signature census is:

| outgoing ports | all weak-atlas signatures | selected-strong signatures | genuinely weak signatures |
|---:|---:|---:|---:|
| 5 | 16,470 | 8,520 | 7,950 |
| 6 | 218,205 | 127,260 | 90,945 |

Every signature has a unique strength status; there is no signature produced
by both a selected-strong and a genuinely weak pattern.

Intersect these sets with the exact strong-support signatures from Milestone
4B.

**EXACTLY COMPUTED.** The intersections have sizes 8,520 and 10,980,
respectively--exactly the complete five- and six-outgoing strong source
atlases.  Every intersecting weak-atlas signature has selected-strong status.
No genuinely weak signature intersects the strong atlas.

Finally, the verifier reconstructs the selected strong graph in every
intersecting presentation and compares its exact canonical mixed-graph code
with the source code.

**EXACTLY COMPUTED.** All 12,720 five-outgoing and 43,920 six-outgoing
intersecting labelled target presentations are isomorphic or `T`-equivalent
to the corresponding source.  The number of non-`T` targets is zero.

## Cross-support separation theorem

Let `H` be a strong support-deck tensor from Milestone 4B and let `W` be any
restriction on the same five or six outgoing labels induced from an arbitrary
full strong theta blob.

**PROVED.** If

\[
V_H^{\rm JC}=V_W^{\rm JC},
\]

then the selected pattern of `W` is itself strong and `W` is labelled
isomorphic or `T`-equivalent to `H`.

Indeed, equal closures have the same polynomial vanishing set and hence the
same complete exact zero/nonzero signature.  The exhaustive intersection
census excludes every genuinely weak status and the canonical-graph replay
excludes every remaining non-`T` topology.

The contrapositive gives an explicit separating quartet invariant for every
genuinely weak target: one of the recorded identities vanishes on one closure
and not on the other.

## Marginal-closure lemma

For any selected outgoing-label set `Y`, let `pi_Y` denote marginalization of
all other outgoing components.

**PROVED.** For a theta blob `B`,

\[
\overline{\pi_Y(\mathcal M_B^{\rm JC})}^{\,Z}
=V_{B|Y}^{\rm JC},
\]

where `B|Y` is represented by any strong dummy extension used above.

In Fourier coordinates, unselected leaves carry character zero.  Every
original edge is therefore seen only through its displayed-tree descendant
mask on `Y`; equal masks combine by parameter products.  Different signature
classes use disjoint original edge sets, and each product map is dominant
(indeed surjective on `(0,1)`).  The inheritance parameters are unchanged up
to parent swaps.  The full parameter map onto the reduced marginal model is
therefore dominant.

Consequently, if two full blob models have a full-dimensional regular overlap,
their irreducible closures agree, and every corresponding selected marginal
closure agrees as well.

## Proof of the arbitrary-size theorem

Choose a minimal labelled strong support `Q` of `B`.  Its size is three or
four by Milestone 4A.  Canonicalize the orientation of any triangle.

If `|Q|=3` and there are at least two additional ports `p,q`, consider every
restriction

\[
Q\cup\{p,q\}.
\]

The source is a five-outgoing strong support-plus-two tensor.  Equality of the
full closures gives equality of this marginal closure.  The cross-support
theorem forces the corresponding restriction of `B'` to be strong and to
have the same canonical topology.

If `|Q|=4`, first use every five-outgoing restriction `Q+p`; when two extra
ports exist, also use every six-outgoing restriction `Q+p+q`.  The same
argument applies.

The cases with fewer extra ports are already complete full strong tensors in
the exact three- or four-outgoing atlases of Milestones 3H and 3E.

Thus every extra port has the same directed core segment in `B` and `B'`, and
every pair on one segment has the same order.  Milestone 4A's ordered-chain
reconstruction theorem now gives identical complete canonical port words on
all core segments.  Hence `B` and `B'` differ only by `T`.

Conversely, labelled isomorphism is observationally trivial and the exact
`T` port-tensor correspondence leaves every external port unchanged while
preserving a nonempty full-dimensional regular stochastic region.  This
proves both directions.

## Consequences and remaining work

**PROVED.** For the complete theta generator, the strong tree-child condition
eliminates every stackable non-orientational JC ambiguity.  In particular,
the known root `Theta`, `Psi`, and `Omega` phenomena cannot reappear merely by
adding more subdivisions or descendant components to a nonroot theta blob.

**UNRESOLVED.** This milestone does not yet:

- classify one-sided generic containments in the weak atlas;
- compare arbitrary theta blobs with cycle-generator blobs;
- recover cut splits or the global tree of blobs from a distribution;
- exclude coordinated changes in distinct blobs;
- complete `L_1`, `L_*`, or `S_2` globally.

## Machine replay

- `src/verify_jc_cross_support_weak_atlas.py` enumerates all weak targets,
  verifies dummy-repair independence, computes the forty new tensor types and
  2,400 exact pullbacks, transports every relative labelling, intersects the
  signature sets, and checks all 56,640 intersecting topology presentations.
- `certificates/jc_cross_support_weak_atlas.json` records all 130 tensor types,
  all 1,454 base tensor decks, status counts, signature counts, and exact
  intersection results.

No external generator catalogue, specialized phylogenetic software,
numerical optimization, or literature search is used.
