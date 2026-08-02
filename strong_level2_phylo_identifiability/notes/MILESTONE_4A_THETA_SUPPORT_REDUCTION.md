# Milestone 4A: bounded support-deck reconstruction for arbitrary theta subdivisions

## Objective

The complete three- and four-outgoing-port nonroot atlases do not by
themselves cover a theta side carrying arbitrarily many ordered ports.  This
milestone proves that no unbounded combinatorial atlas is needed.

The result is deliberately separated into two layers:

1. the bounded combinatorial reduction proved here; and
2. the finite support-augmented JC stochastic atlas, which remains unresolved.

No observational theorem is inferred merely from the combinatorial deck.

## Port-word convention

Fix one of the four oriented theta cores.  Every directed core segment `e`
carries a finite ordered word

\[
W_e=(p_{e,1},\ldots,p_{e,k_e})
\]

of distinct ordinary port labels.  Each path-sink reticulation `X` carries
one additional distinguished outgoing port label.  These data reconstruct
the complete ported blob: insert the ordinary tree vertices in the order of
each word and attach the corresponding cut-edge components.

For any label subset `Y`, let `B|Y` be the ordinary induced restriction:
delete unselected outgoing components, prune vertices having no retained
descendant, and suppress resulting indegree-one/outdegree-one tree vertices.
When `Y` contains every path-sink label, this is core-preserving; on each
segment it simply replaces `W_e` by its subsequence on `Y`.

## Strong support theorem

The tree-child conditions on a fixed core are monotone in the set of occupied
segments.  Milestone 2 gives every minimal segment repair.

Let `O` be the occupied-segment set of a full strong expansion.  Since `O`
satisfies the monotone conditions, it contains at least one minimal repair
`R`.  Choose one ordinary port label from each segment in `R`, and include
every path-sink port label.  Call the resulting labelled set `Q`.

**PROVED.** `B|Q` retains the complete oriented theta core and is strongly
tree-child.  The sink labels retain every path reticulation, while the chosen
ordinary labels realize the repair `R`.  All other deleted ordinary vertices
have become suppressible degree-two vertices, so no additional event remains.

**EXACTLY COMPUTED.** The four support sizes are:

| core | sink ports | repair ports | support size |
|---|---:|---:|---:|
| `TT-nested` | 2 | 1 | 3 |
| `TT-separated` | 2 | 2 | 4 |
| `TR-nested` | 1 | 2 | 3 |
| `TR-separated` | 1 | 2 | 3 |

Thus every finite strong theta expansion has a core-preserving strong support
of at most four outgoing ports.

The exact occupancy census checks all `2^6` masks for each six-segment core
and all `2^5` masks for each five-segment core.  The numbers of strong masks
are respectively `48,36,12,12`, and every one contains a certified minimal
repair of the stated size.

## Ordered-chain reconstruction

Fix one labelled support `Q` as above.

For any ordinary port `p` outside `Q`, the exact labelled topology

\[
B|_{Q\cup\{p\}}
\]

reveals the directed core segment containing `p` and its order relative to
the support labels already on that segment.

For two ordinary ports `p,q` outside `Q` on the same segment, the restriction

\[
B|_{Q\cup\{p,q\}}
\]

reveals which one occurs first.  If they lie on different segments, their
relative order is irrelevant.  Hence these restrictions give:

1. the segment membership of every ordinary port;
2. every pairwise comparison within each segment; and therefore
3. the unique total ordered word `W_e` on every segment.

**PROVED.** The support-plus-two deck reconstructs the complete labelled
ported theta topology up to core isomorphism.  A core automorphism fixing the
labelled support merely yields the same labelled isomorphism class; the
pairwise order data remain consistent under that action.

The largest restriction has

\[
|Q|+2\le 6
\]

outgoing ports.  Counting the distinguished incoming state port of a nonroot
blob gives at most seven total tensor ports.

## Uniform witness corollary

Let `B,B'` be two ported strong theta topologies on the same outgoing labels.
Suppose their ordinary induced restrictions are labelled-isomorphic for every
subset of at most six outgoing labels.  Choose a support `Q` for `B`.  The
equal restriction on `Q` makes the same labels a core-preserving strong
support for `B'`.
Equality of all `Q+p` and `Q+p+q` restrictions then gives the same segment
memberships and pairwise orders in both blobs.

**PROVED.** `B` and `B'` are labelled-isomorphic.  Equivalently, every
combinatorial distinction between finite strong theta port expansions has an
induced witness on at most six outgoing ports.

The same argument applies after replacing exact orientations inside an
observationally quotiented triangle by a fixed canonical orientation.  It is
a statement about reconstruction of the canonical port words, not a proof
that JC identifies every required restricted topology.

## What this resolves—and what it does not

**PROVED.** Fully port-labelled theta blobs form an infinite family, but their
topological reconstruction reduces to a bounded deck.  Primitive
combinatorial distinctions of unbounded witness size do not occur for the
theta expansion language.

**UNRESOLVED.** To turn this into the desired `L_1` observational theorem, it
remains to prove that generic JC data identify the canonical topology of every
support-augmented restriction through six outgoing ports, modulo `T` and the
already certified root-local moves.  The three- and four-outgoing subatlases
are complete; restrictions of sizes five and six are not.

It also remains to reconstruct the blob tree and local port tensors from a
global distribution and to exclude coordinated changes between blobs.

## Machine replay

- `src/verify_theta_support_reduction.py` regenerates the four cores, every
  minimal repair, every occupied-segment mask, the support bounds, and the
  uniform size-six maximum.
- `certificates/theta_support_reduction.json` records every core, repair set,
  strong occupancy pattern, and canonical contained support repair.

No numerical algebra, external generator catalogue, specialized network
software, or literature search is used.
