# Milestone 5A: generic JC data reconstruct every cut split

## Main theorem

Let `N` be any binary strongly tree-child level-2 network on leaf set `X`.
No restriction on the number of blobs or on the number of triangles in one
blob is needed. For a nontrivial bipartition `A|B` of `X`, let
`Flat_{A|B}(p)` be the ordinary pattern flattening, or equivalently its
Fourier transform by independent four-state Hadamard changes of basis on the
two sides.

**PROVED.** There is a proper algebraic exceptional subset of the JC
parameter space such that, outside it,

\[
\boxed{
A|B\text{ is induced by a cut edge of }N
\quad\Longleftrightarrow\quad
\operatorname{rank}\operatorname{Flat}_{A|B}(p)\leq4.
}
\]

Consequently an exact generic JC distribution determines every nontrivial cut
split and therefore the leaf-labelled tree obtained by contracting each
nontrivial blob to one vertex and suppressing unlabelled degree-two vertices.

**PROVED.** If `N bowtie_JC N'`, their homeomorphism-reduced
bridge-contraction trees are leaf-labelled isomorphic. Thus a
full-dimensional global ambiguity cannot change the nontrivial cut-split
system or the reduced arrangement of blobs.

An unlabelled degree-two factor is invisible to a split system. In this class,
the relevant unresolved case is a minimal two-port root-containing cycle
blob. Its detection or collapse is explicitly deferred to the root-factor
atlas; it is not silently treated as reconstructed here.

This milestone does not yet extract every local blob tensor or complete the
root-blob atlas.

## The easy direction: a cut gives rank at most four

Suppose a directed cut edge separates downstream leaves `A` from the other
leaves `B`. Conditional on the four-state variable at the cut, all random
parent choices, substitutions, and leaf states on the two sides are
independent. Hence the pattern flattening factors as

\[
\operatorname{Flat}_{A|B}(p)=LDR^{\mathsf T},
\]

where the middle state index has size four. Therefore its rank is at most
four for every stochastic parameter point, not merely generically.

The Fourier transform acts by invertible matrices on the rows and columns, so
it preserves this rank. In Fourier coordinates the same statement is visible
as four total-character blocks, each an outer product.

## Switching lemma for one blob

Contract every component beyond a cut edge to a port. Colour each incident
port `0` or `1`, with each colour occurring on at least two distinct ports.

**PROVED.** For every root-containing or nonroot strongly tree-child level-2
blob, at least one parent-choice switching gives a tree in which the two port
colour classes are not separated by one edge.

By Milestone 2, the blob generator is a cycle or theta. Every ordinary port
lies in an ordered word on a directed core segment, while every path-sink
reticulation has one sink port. A nonroot blob has one additional incoming
port.

If a segment word contains `0...1...0` or `1...0...1`, the middle-colour port
lies on the path between two opposite-colour ports in every switching. No
tree edge can then separate the colours. Thus a hypothetical common split has
at most one colour transition on each segment.

Delete redundant ports within each monochromatic run. Taking subsets of the
two colour classes preserves any tree split. One representative per run is
therefore sufficient unless one colour occurs in only one run globally; in
that case retain two representatives from that run. Empty versus occupied
segments do not change, so strong tree-child validity and all minimum repair
conditions are preserved.

This reduces arbitrary port words to a finite exact census.

## Exhaustive compressed census

The four theta orientation cores have five or six directed segments. Every
segment is assigned one of

\[
\varnothing,\quad 0,\quad1,\quad01,\quad10.
\]

The singleton-run audit separately doubles the unique occurrence of a colour
when needed. Sink ports and, in the nonroot case, the incoming port receive
both possible colours. Every strong occupancy and every parent-choice
switching is replayed exactly.

**EXACTLY COMPUTED.** The theta census is:

| blob position | valid run-compressed occupancies | colourings | both colours at least twice | singleton-run doubled | false common splits |
|---|---:|---:|---:|---:|---:|
| root | 1,512 | 127,200 | 124,368 | 2,232 | 0 |
| nonroot | 1,512 | 254,400 | 251,352 | 2,232 | 0 |

For each position, the occupancy counts by theta core are

\[
(648,576,144,144).
\]

**EXACTLY COMPUTED.** The cycle census is:

| blob position | valid run-compressed occupancies | colourings | both colours at least twice | singleton-run doubled | false common splits |
|---|---:|---:|---:|---:|---:|
| root | 8 | 48 | 16 | 20 | 0 |
| nonroot | 8 | 96 | 54 | 24 | 0 |

This proves the switching lemma for arbitrarily long port words, rather than
only for blobs below a chosen size.

## From a non-cut split to a crossing switching

Contract every nontrivial blob in the underlying undirected network. Retain
all bridges and suppress the degree-two root artifact. The result `K_N` is a
leaf-labelled tree. Every edge of `K_N` corresponds to one cut edge of `N`.

Consider a nontrivial leaf split `A|B` that is not an edge split of `K_N`.
The elementary tree-split criterion gives leaves

\[
a_1,a_2\in A,\qquad b_1,b_2\in B
\]

whose induced quartet in `K_N` does not display
`a_1a_2|b_1b_2`. To see this directly, take the minimal subtrees spanning
`A` and `B`. If the proposed split is not an edge split, these subtrees meet;
paths from an intersection point to suitable leaves give the required
quartet.

If that quartet is resolved in `K_N`, its displayed split crosses the
proposed split. The corresponding bridge remains in every switching, so the
incompatible proposed split cannot occur.

If the quartet is unresolved, its four branches meet at a vertex of degree at
least four. Ordinary tree vertices have degree three, so this vertex is a
contracted nontrivial blob. Its incident ports have colours `0,0,1,1`; the
local switching lemma chooses a switching that does not display the proposed
split. Extend it by arbitrary switchings in all other blobs.

Thus every non-cut split fails to be displayed by at least one complete
displayed tree of `N`.

## Exact JC rank witness

Specialize the inheritance probabilities to the boundary values selecting
that crossing displayed tree. Marginalize to the witness quartet. After
suppressing degree-two vertices, the true quartet split is either

\[
13|24\qquad\text{or}\qquad14|23
\]

while the tested flattening is `12|34`.

Set all five effective JC edge multipliers of the quartet tree to `1/2`.
Rows and columns are indexed lexicographically by pairs of characters in
`Z_2 x Z_2`. The upper-left `5 x 5` minors are:

\[
\det M_{13|24}=\frac{3}{1024},
\qquad
\det M_{14|23}=-\frac{3}{4096}.
\]

**EXACTLY COMPUTED.** Both complete wrong-split Fourier flattenings have rank
`16`. The two displayed determinant calculations use exact rational
arithmetic.

Effective quartet edges are products over five disjoint paths, so the value
`1/2` can be realized independently on each path. The boundary choice of
inheritance parameters is legitimate for proving that the corresponding
minor is a nonzero polynomial. Therefore that minor remains nonzero on a
nonempty interior open set and is nonzero generically outside a proper
algebraic hypersurface.

Marginalization is a linear operation on the rows and columns of the full
flattening. A quartet marginal of rank greater than four forces the full
flattening to have rank greater than four. This proves the converse.

There are finitely many leaf splits. The union of their nonzero-minor
exceptional hypersurfaces is still proper, giving one simultaneous generic
set on which every cut split is recovered correctly.

## Reconstructing the reduced bridge-contraction tree

**PROVED.** The recovered cut splits are pairwise compatible. Choose a
reference leaf and orient every split by the side not containing it. These
sides form a laminar family. Ordering them by inclusion and connecting every
set to its least strict superset reconstructs the unique homeomorphism-reduced
leaf-labelled tree whose edges realize exactly those splits. Adding the
trivial pendant splits places every labelled leaf.

The word "reduced" is essential: split systems never record unlabelled
degree-two vertices. All nonroot blobs in the strong level-2 class have at
least three incident ports, but a minimal root-containing cycle can have two.
That possible root factor must be classified from its local stochastic tensor,
not from cut ranks.

For data known to arise from the class, this gives a finite exact algorithm:

1. test every nontrivial leaf bipartition by exact flattening rank;
2. retain exactly those of rank at most four;
3. reconstruct the laminar split tree;
4. mark its internal vertices as candidate contracted blobs or ordinary tree
   vertices for the next local-tensor phase.

The direct split enumeration is exponential in the number of leaves. No
polynomial-time claim is made at this milestone.

## Consequence for observational overlap

Let `N bowtie_JC N'`. A full-dimensional regular common neighborhood cannot
be contained in either network's proper algebraic exceptional set. Choose a
common point outside both sets. Its flattening ranks recover both cut-split
systems, so those systems and their unique reduced bridge trees agree.

**PROVED.** Any remaining full-dimensional JC ambiguity preserves the reduced
bridge tree. In particular, networks with different nontrivial cut-split
systems cannot be observationally equivalent. This statement does not rule
out inserting or deleting a statistically absorbable degree-two root factor.

**UNRESOLVED.** To turn this into the full `L_1`, `L_*`, or `S_2`
if-and-only-if theorem, the next steps are:

- analytically extract the local port tensor at each recovered internal
  vertex, modulo the cut-edge scalar gauges;
- distinguish an ordinary tree vertex from a contracted cycle or theta blob;
- extend the local atlas across different choices of incoming port;
- complete arbitrary root-containing cycle and theta blob classifications;
- classify one-sided global containments.

## Machine replay

- `src/verify_jc_cut_split_reconstruction.py` exhausts every compressed root
  and nonroot cycle/theta two-colouring, every parent-choice switching, and
  both exact crossing-quartet flattenings.
- `certificates/jc_cut_split_reconstruction.json` records all census counts,
  exact ranks, determinants, and theorem status.

No external theorem, generator catalogue, specialized phylogenetic software,
randomized computation, numerical optimization, or literature search is
used.
