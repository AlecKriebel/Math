# Corrected all-primitive probe-coherence theorem

## Claim and scope

Work on the principal stochastic K2P domain

\[
\mathcal D_+=\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

For every physical labelled equality anchor supplied by a primitive tree,
cycle, or repaired theta support, attach one labelled probe on every edge of
the suppressed semi-directed mixed graph, on each side of the relation. Keep
only exact labelled isomorphisms and ordinary-triangle relations. Repeat the
complete attachment experiment once above every retained relation. The claim
is that every other one- or two-probe pair is separated, every retained map
restricts the unique parent map, every reversed one-probe marginal is present,
and all triangle maps transport the one triangle already present at the base.

The certificate is deliberately limited to the principal positive domain. It
does not claim a mixed-sign extension.

## Complete attachment-site universe

Suppressing the artificial root turns a rooted presentation into its physical
semi-directed mixed graph. Every mixed edge is an attachment site, including
pendant arms and edges entering a reticulation. If the mixed edge was created
by suppressing the root, its two rooted half-arcs give isomorphic insertions;
the input contract proves this exact equivalence and retains one
representative. Thus a physical `k`-port, `r`-reticulation graph has exactly

\[
2k+3r-3
\]

sites. This construction is invariant under admissible root movement and does
not privilege a rooted three-leaf restriction.

The frozen input contract reconstructs 176 physical equality-anchor records:
the ordinary tree, all physical cycle terminals, the corrected four-port
direct and restored terminals (including the four restored ordinary-triangle
records that the revoked topology-first classifier missed), and every
physical theta2 restoration path. It contains 2,206 sites on each side and
29,964 first-probe Cartesian pairs.

## Fail-closed classifier

Every child pair is classified in this order.

1. **Exact labelled relation.** Expand each semi-directed mixed graph to its
   incidence graph, retaining every arrowhead. For an isomorphism, match the
   expansions exactly. For an ordinary-triangle relation, enumerate only
   triangles with exactly two arrows entering one common reticulation and
   forget the three triangle-edge arrowheads. A retained witness must be
   unique, agree with the parent map on every old mixed vertex, carry the
   chosen source site to the chosen target site, and use the inherited
   triangle if it is a triangle witness.
2. **Displayed-quartet mismatch.** Enumerate every switching and compare the
   complete split sets. One unequal labelled quartet is an exact separator.
3. **Direct full-map `T_i` sign.** Search all triples and all three
   orientations directly on the original full graph Fourier maps. No rooted
   structural type is used as a finder or as proof.
4. **Unresolved.** Any remaining row is fatal. There is no heuristic or
   numerical fallback.

Deleting the newly inserted label from each child is independently required
to recover its concrete labelled parent mixed graph by exact isomorphism.
Those marginal transports are stored separately from the relation transport.

The exact-relation stage uses one proof-level prefilter. Any child relation
marginalizes to a parent relation. Since the parent transport is unique and
the new labelled leaf forces its incident subdivision, a child relation can
exist only when the unique parent edge map carries the chosen source site to
the chosen target site. Unmatched site pairs therefore need no graph-matcher
call; this is a deduction from uniqueness, not a topology cache.

The final exact census reflects this theorem with no slack. At one port all
27,758 site pairs incompatible with the unique parent edge map are
quartet-separated; the 2,206 compatible pairs split into 1,915 isomorphisms,
192 ordinary triangles, and 99 full-map `T_i` separations. At two ports all
511,266 incompatible pairs are quartet-separated; the 33,305 compatible pairs
split into 30,969 isomorphisms, 1,760 ordinary triangles, and 576 `T_i`
separations. Thus no exact relation is hidden behind the site prefilter.

## Full-map K2P sign separator

For distinct boundary labels `a,b,i`, let

\[
T_i=V^2X_g-X_s^2Y_gZ_g,
\]

where the five coordinates use character assignments

\[
V:(a,b,i)=(1,3,2),\quad X_s:(1,1,0),\quad X_g:(2,2,0),
\]

\[
Y_g:(2,0,2),\qquad Z_g:(0,2,2).
\]

The compiler expands every displayed switching of the original rooted graph,
keeps a separate `(s,g)` pair for each non-arm physical edge, and expands every
inheritance product into an exact integer sparse polynomial. A sign row is
accepted only when one pullback is coefficientwise zero and the other has a
strict exact tensor-Bernstein sign on the full open parameter cube after
stripping a common positive monomial. The full cube contains the physical
`D_+` subset, so the separation holds there.

Both monomials of `T_i` have the same boundary-incidence weights:

\[
a:s^2g,\qquad b:s^2g,\qquad i:g^2,
\]

and weight zero on every other arm. Hence zero versus strict nonzero survives
the complete two-sector K2P bridge torus.

## Two-probe order and arbitrary words

The second probe is enumerated only above exact one-probe equality survivors.
This loses nothing: any full relation would have an equality relation after
marginalizing its second label. Every mixed site of each surviving parent is
again enumerated on each side.

For every exact two-probe equality, the verifier then deletes the *first*
probe, renames the second probe to the standard one-probe label, and constructs
the reverse-order parent relation. Its exact graph-pair-plus-transport class
must already occur among the complete one-probe equality classes above the
same base anchor. Thus both adjacent positions and their order are fixed.
Induction along a maximal degree-two segment reconstructs an arbitrary ordered
attachment word.

An isomorphic base cannot acquire a triangle. A triangle child must use the
same three source edges, same three target edges, and same common reticulation
as its parent. An isomorphic child of a triangle parent is permitted, but its
stored global triangle remains the base triangle. Therefore the local maps
assemble with at most the single ordinary triangle already present in the
rigid-support anchor.

## Falsifiable success gates

Promotion requires all of the following simultaneously:

- complete raw one- and two-port ledgers with deterministic ordered hashes;
- exact agreement with the 176-anchor root-invariant input contract;
- zero unresolved rows and zero incoherent exact relations;
- exact concrete parent recovery on both sides of every insertion edge;
- strict Bernstein replay of every `T_i` polynomial;
- reversed-order coverage of every two-port equality;
- zero newly created or inconsistently transported ordinary triangles;
- independent regeneration under normal Python, explicit rejection under
  `python -O`, and targeted fail-closed mutations.

The numerical censuses and cryptographic hashes are intentionally stated only
in the generated certificate and research log so this proof document cannot
silently drift from a regenerated release.
