# Milestone 4D: every nonroot level-2 generator is JC-identifiable modulo `T`

## Main theorem

Let `B` and `B'` be finite port-labelled, strongly tree-child, nonroot
level-2 blobs with the same distinguished incoming state port and the same
labelled outgoing ports. Ports may occur in arbitrary number and arbitrary
order on directed core segments.

**PROVED.** Under the Jukes--Cantor model,

\[
\boxed{
B\bowtie_{\rm JC}B'
\quad\Longleftrightarrow\quad
B,B'\text{ have the same generator and differ only by labelled
isomorphism and triangle redirection }T.
}
\]

By the generator theorem of Milestone 2, the only possible nontrivial
level-2 generators are a cycle or a theta. Milestone 4C proved the theorem
for arbitrary theta blobs. This milestone proves it for arbitrary cycle
blobs and proves that cycle and theta blobs are mutually separated.

Consequently `T` is the complete full-dimensional regular JC ambiguity move
for every finite strongly tree-child **nonroot** level-2 blob. The result is
local: recovery of the global blob tree and exclusion of coordinated changes
between blobs remain unresolved.

## Cycle expansions and bounded support

A nonroot cycle core has a source `S`, a path-sink reticulation `X`, and two
internally disjoint directed `S`-to-`X` sides. Every ordinary port is carried
by a tree subdivision vertex on one side, and the sink child is a port at
`X`. The incoming state port enters `S`.

**PROVED.** Every strong binary cycle expansion has this form. Its sink port
together with any ordinary port is a strong, core-preserving two-outgoing
support. Relative to an anchored support port:

- a support-plus-one restriction determines which side contains an extra
  port and, on the anchored side, whether it lies above or below the anchor;
- a support-plus-two restriction determines the relative order of any pair
  of extra ports on the same side.

The resulting pairwise side and order relations reconstruct both complete
ordered side words. Swapping the two sides is a graph automorphism. If the
complete cycle itself is a triangle, the remaining local reticulation choice
is precisely `T`; otherwise the reconstructed subdivision has no triangle on
which an additional `T` can act.

Thus restrictions on at most four outgoing ports reconstruct every arbitrary
finite ported cycle topology modulo isomorphism and `T`.

## Exact strong cycle atlas

The verifier generates every weak composition of the ordinary port count
over the two directed sides, quotients the side-swap automorphism, applies
every relative outgoing-label permutation, and compares exact canonical
semi-directed graph codes modulo `T`.

**EXACTLY COMPUTED.** The complete bounded strong atlas is:

| outgoing ports | role candidates | relative labelled presentations | structural classes modulo `T` | exact invariant signatures |
|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 1 | one exact `T` class |
| 3 | 2 | 12 | 9 | 9 |
| 4 | 3 | 72 | 48 | 48 |

The two-outgoing case is the ordinary three-port triangle tensor and is
covered by the inherited exact `T` correspondence. At three and four
outgoing ports, every structural class has a distinct exact signature. The
number of non-`T` collisions is zero.

## Exact tensor reduction

For a quartet marginal and one reticulation, associate to every edge the pair
of descendant masks obtained from the two parent choices. Edges with equal
mask pairs enter every JC Fourier coordinate only through the product of
their multipliers. Swapping the two parent choices flips all mask pairs and
replaces the inheritance parameter by its complement; this is an
open-parameter automorphism.

**PROVED.** The reduced mask tensor therefore has exactly the same open
stochastic image as the original marginal tensor after the corresponding
edge-product reparameterization.

**EXACTLY COMPUTED.** Every strong and weak cycle restriction through six
outgoing ports uses only four reduced quartet tensor types. Pulling back all
sixty root-atlas invariants over exact rational polynomial rings gives

\[
4\cdot60=240
\]

recorded symbolic identities. No modular, floating-point, or randomized
identity test is used.

## Weak cycle restrictions and cross-support closure

A selected restriction of a competing full strong cycle need not retain the
sink port. The exhaustive weak target generator therefore allows either:

1. the selected labels include the sink child; or
2. an unobserved dummy leaf supplies the sink child.

All selected ordinary labels are distributed over the two sides. Conversely
every such presentation extends to a full strong cycle, so the enumeration
is exhaustive.

**EXACTLY COMPUTED.** The weak cycle census is:

| outgoing ports | weak role presentations | base tensor decks | all relative-label signatures | selected-strong | genuinely weak |
|---:|---:|---:|---:|---:|---:|
| 3 | 7 | 4 | 12 | 9 | 3 |
| 4 | 9 | 6 | 63 | 48 | 15 |
| 5 | 11 | 8 | 390 | 300 | 90 |
| 6 | 13 | 10 | 2,790 | 2,160 | 630 |

Strength status never mixes inside an exact signature.

At four outgoing ports, the 48 strong signatures intersect the 63 weak
signatures in exactly the same 48 signatures. Every intersecting weak target
retains the sink and is therefore selected-strong.

**EXACTLY COMPUTED.** Exact canonical graph replay checks all 96 intersecting
labelled target presentations and finds zero non-`T` targets.

As in Milestone 4C, Fourier marginalization is a dominant edge-product map:
unselected leaves carry character zero, distinct descendant-mask classes use
disjoint original edges, and every product of open edge multipliers ranges
over `(0,1)`. Hence equality of full blob closures implies equality of each
selected marginal closure.

**PROVED.** A full-dimensional regular overlap between two arbitrary cycle
blobs forces every support-plus-two restriction to agree modulo `T`. The
bounded reconstruction above then forces the complete cycle blobs to agree
modulo `T`. Conversely, isomorphism is trivial and the exact `T` tensor map
gives a nonempty full-dimensional regular stochastic overlap.

## Cycle--theta separation

For a theta blob, choose a labelled core-preserving strong support. It has
three or four outgoing ports by Milestone 4A. A restriction of a competing
full cycle blob to those labels can be weak, so it must be compared with the
complete weak cycle atlas rather than only the strong cycle atlas.

**EXACTLY COMPUTED.** The exact signature intersections are:

| outgoing labels | strong theta signatures | weak cycle signatures | intersection |
|---:|---:|---:|---:|
| 3 | 21 | 12 | 0 |
| 4 | 516 | 63 | 0 |
| 5 | 8,520 | 390 | 0 |
| 6 | 10,980 | 2,790 | 0 |

The three- and four-outgoing rows already prove separation from a minimal
theta support; the five- and six-outgoing rows independently certify every
bounded support-augmented deck used in Milestone 4B.

**PROVED.** A cycle blob and a theta blob cannot have a full-dimensional
regular JC intersection. If they did, their irreducible closures would be
equal, as would the closure of every corresponding marginal. The selected
theta support and weak cycle target would then have identical polynomial
vanishing sets, contradicting one of the explicitly recorded exact quartet
invariants.

There is a useful asymmetry. Every strong cycle signature at sizes three and
four occurs among weak theta restrictions, but none occurs among
selected-strong theta restrictions. A theta marginal can therefore hide one
reticulation and look like a cycle. This does not create a full-blob
ambiguity because choosing the support in the theta blob prevents the
reticulation from disappearing.

## Consequences and scope

**PROVED.** The local JC move system for every arbitrary finite strongly
tree-child nonroot level-2 blob is exactly

\[
R_{\rm JC}^{\rm nonroot}=\{T\}.
\]

In particular, the root-local moves `Theta`, `Psi`, and `Omega` cannot occur
in a nonroot cycle or theta blob, and changing the level-2 generator type is
generically detectable.

**UNRESOLVED.** This milestone does not yet:

- classify every one-sided containment among arbitrary weak restrictions;
- prove that a global distribution identifies all cut splits and the blob
  tree;
- extract each nonroot local port tensor from the global distribution;
- exclude coordinated nonlocal changes between several blobs;
- classify root-adjacent blobs of arbitrary size;
- complete `L_1`, `L_*`, or `S_2` globally.

## Machine replay

- `src/verify_jc_cycle_cross_generator_atlas.py` generates every bounded
  strong and weak cycle restriction, computes the four exact tensor types and
  240 invariant pullbacks, transports every relative labelling, replays the
  cycle cross-support topology checks, and proves all four theta--cycle
  signature intersections empty.
- `certificates/jc_cycle_cross_generator_atlas.json` records the exact tensor
  types, all census counts, signature counts, cross-support intersections,
  and theorem status.

No external generator catalogue, specialized phylogenetic software,
numerical optimization, or literature search is used.
