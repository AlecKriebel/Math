# Independent audit of the six-unit palette-repair frontier

12 October 2026 UTC

## Decision and exact scope

**Accepted at the corrected, method-only scope.** The six-unit classification, its remaining patterns, the actual critical-graph examples, the uniform-omission boundary argument, and the explicit failure of the extension inference all pass independent mathematical and finite verification. No mathematical correction to the complete accepted method text in [METHODS.md](METHODS.md) is required.

The hypotheses are essential: the graph is finite and simple, has maximum degree three, is not ordinarily three-edge-colorable, and becomes ordinarily three-edge-colorable after every single-edge deletion. A fixed ordinary palette is (A), with three colors. Exactly six exceptional edges have lists

\[
L(f)=(A\setminus\{a_f\})\cup\{x_f\},\qquad a_f\in A,\quad x_f\notin A.
\]

All remaining lists are (A). Exterior singleton colors may agree in any pattern. The main enumeration excludes constant omission patterns; those are handled separately by an argument covering all six-edge supports.

The result classifies three sufficient repair methods. The residual records are **not** uncolorable assignments, are not counterexamples to the original conjecture, and do not establish that an exceptional edge cannot receive its exterior color. The six exhaustive negative examples refer to the selected edge and the deletion-derived construction only. There are three underlying critical fixtures, not six distinct critical graphs. No novelty claim or resolution of the unrestricted conjecture is accepted.

## Why the three methods are sufficient

For any nonempty exceptional set (F), criticality supplies an ordinary coloring of (G-F): delete one edge of (F), color the resulting graph, and restrict the coloring. A proper exterior coloring of (F) can then be combined with a suitable global permutation of this ordinary coloring, because the exterior and ordinary palettes are disjoint.

If at least four exceptional edges can be exterior-colored, at most two unit omissions remain. Each remaining omission forbids at most two of the six global palette permutations. Two such restrictions cannot forbid all six permutations. This proves the strict-deficit certificate.

For a residual triple, a fixed ordinary color word fails to admit a palette permutation precisely in either of two cases: its labels are all equal while its omissions are all distinct, or its labels are all distinct while its omissions are all equal. If precisely two ordinary labels occur, the twice-used label still has at least one available image, and the other label has at least two, so a permutation exists. If three labels occur, the three permitted-image sets each have size two; Hall fails exactly when all three omit the same color. The one-label case is immediate.

Consequently, universal residual completion holds precisely when the omissions use two colors, or when they use three colors and the residual triple contains an incident pair. For distinct omissions, that incident pair rules out the only bad, constant ordinary word. For constant omissions, assigning three distinct ordinary labels always supplies a proper bad word. For a matching with distinct omissions, a constant ordinary word supplies a bad word. This criterion was independently tested on all eight labeled graphs on three vertices and all 27 omission words, with all proper ordinary words and all six permutations checked directly.

For deletion-adaptive repair, the accepted quantifiers are

\[
\exists e\in X\;\forall\phi\in\operatorname{Col}_3(H-e)\;\exists\pi\in S_3:
\quad F(e,\phi,\pi)\text{ is exterior-colorable},
\]

where (H) is the support line graph and

\[
F(e,\phi,\pi)=\{e\}\cup\{f\in X\setminus\{e\}:\pi(\phi(f))=a_f\}.
\]

Any ordinary coloring of the actual deletion graph restricts to such a local coloring. Every edge of the displayed set must be exterior if that ordinary coloring and permutation are retained elsewhere. An exterior conflict within this required set cannot be repaired by enlarging the set. Thus the local certificate is sufficient. Its negation is (orall e\,\exists\phi\,\forall\pi), not universal failure of all local or global colorings.

## Exhaustive finite coverage

The support enumeration is complete at the level on which the methods depend: six-vertex line graphs of simple subcubic six-edge supports. Independent verification established all of the following:

- There are 156 unlabeled graphs on six vertices.
- Exactly 47 support line-graph types occur.
- All 47 supplied endpoint representations are simple, subcubic, and have exactly six edges; their line graphs and canonical masks match.
- Their permutation orbits are pairwise disjoint and contain exactly 9,463 labeled line graphs.
- An independently written enumeration partitions the twelve edge endpoints into vertex blocks of sizes at most three, rejects loops and repeated edges, and obtains exactly 508,285 valid endpoint partitions. Its set of labeled line graphs is exactly the preceding set.

This block-based enumeration differs from the original incremental endpoint-label enumeration. Every simple subcubic six-edge graph determines such an endpoint partition, and every accepted partition defines such a graph. Thus the comparison checks both validity and exhaustiveness. A support line graph need not determine its original support uniquely; that causes no loss because all three methods use only edge incidences and color equalities.

Exterior singleton equalities are exactly the 203 partitions of six positions. Omissions are exactly the 122 partitions into at most three blocks. Removing the constant partition leaves 121. Therefore the normalized variable-omission domain has exactly

\[
47\cdot203\cdot121=1,154,461
\]

cases. This is a complete equality-pattern normalization, not a bound on the exterior palette chosen for convenience.

A newly written third classifier reconstructed incidence from the support endpoints, generated normalized color patterns by normalizing complete Cartesian color words, enumerated all labeled ordinary words on each relevant residual or deletion support, and evaluated all six permutations. In particular, it did not use the shortcut Hall criterion. The two supplied programs were also rerun in an isolated writable copy. Instrumentation that only records each classification established **point-for-point agreement across all 1,154,461 cases**, rather than merely agreement of totals or residual lists.

The disjoint, ordered phase totals are:

- Strict deficit: 1,095,050
- Universal three-residual completion: 56,674 additional cases
- Deletion-adaptive repair: 2,725 additional cases
- Unsettled by those methods: 12

All enumerations completed. No timeout, heuristic cutoff, or interrupted search was treated as a negative result.

## Exact residual scope

All 12 residual records have a common exterior color. Independent checks validated every local deletion witness for propriety and a genuine exterior conflict under every permutation. Automorphism and omission-color normalization reproduce nine orbits. Four records comprise a single orbit on (K_4); the other eight records are eight distinct orbits on seven support types:

1. (C_6), with alternating two-color omissions
2. (C_6), with three omission colors repeated cyclically
3. (C_5) with a pendant edge
4. (C_4) with pendant edges at adjacent vertices
5. A triangle with one pendant edge at each vertex
6. (C_4) with pendant edges at opposite vertices
7. A theta graph with path lengths 1, 2, and 3
8. A diamond with a pendant edge at a degree-two vertex

The listed original-support shapes and the cyclic omission patterns were checked independently.

A critical graph has only one edge-containing component: an edge deletion in another component could not repair a noncolorable component. An embedded (K_4) support saturates all its vertices, so it is an isolated edge-containing component. Since (K_4) is ordinarily three-edge-colorable, that support cannot occur under the stated critical hypotheses. This removes the four (K_4) records from possible critical-supergraph instances. It does not prove the remaining eight assignments uncolorable or settle all their supergraph instances.

## Actual critical examples and the extension correction

The three supplied fixtures have respectively 5, 7, and 7 vertices and 7, 10, and 10 edges. Their maximum matching sizes were independently computed as 2, 3, and 3. In each case the edge count exceeds three times the matching number, proving ordinary three-edge-noncolorability. The graphs are simple and subcubic, and a complete independent Cartesian enumeration confirms ordinary colorings after every edge deletion.

Every non-(K_4) residual pattern is realized in the fixtures with the asserted omission pattern. For each selected deletion graph, the stored ordinary-coloring collection equals the entire independently enumerated labeled collection, with no omissions or duplicates. There are 72 such ordinary colorings across the eight selected examples and 432 coloring/permutation trials. Two examples have 12 successful trials each; the other six have none. All recorded conflict pairs were checked against the required exterior set.

The two Kempe examples were verified at the level of the actual two-color connected component: the chosen component is connected and closed, switching it gives a proper ordinary deletion coloring, and the recorded permutation and exterior set yield the recorded proper full list coloring.

All eight examples have verified proper full list colorings with the selected edge exterior. This is a positive disproof of the rejected inference, not merely an absence of evidence for it. An ordinary coloring on (G-F) obtained from a full list coloring need not extend to an ordinary coloring on (G-e).

The explicit seven-edge example was also checked directly. In the edge order

\[
01,02,13,14,23,24,34,
\]

with the specified six substitutions and selected edge (02), there are exactly six labeled ordinary deletion colorings, forming one palette-permutation orbit. All 36 ordinary-coloring/permutation trials fail deletion-derived repair. Nevertheless,

\[
(1,3,2,0,1,2,3)
\]

is a proper list coloring with the selected edge exterior. Its exterior set is ({02,34}). Keeping the ordinary colors on the other edges, the only available ordinary color at vertex 3 is 0 and the only available ordinary color at vertex 4 is 1. Hence the edge (34) cannot be restored ordinarily. The candidate's case-by-case permutation argument and its nonextension argument are both valid.

The precise accepted distinction is therefore:

- Local method failure: for every support edge, some local deletion coloring blocks every permutation.
- Six actual negative examples: for the selected edge, every ordinary coloring of the actual deletion graph blocks every permutation.
- Full list coloring: all eight examples remain colorable with that selected edge exterior.

## Uniform omissions and the six-edge structural boundary

The uniform-omission argument is valid for arbitrary exterior singleton equalities. If an exceptional edge has at most two exceptional neighbors, an ordinary deletion coloring has a color absent on those neighbors. Exterior-color the selected edge and all exceptional edges with that ordinary color. These edges form a matching. Mapping that ordinary color to the common omitted color makes every remaining exception valid.

If no edge of a six-edge simple subcubic support has at most two exceptional neighbors, each edge has endpoint-degree sum at least five. Thus there are no degree-one vertices and no adjacent degree-two vertices. Writing the degree counts as (n_2,n_3),

\[
2n_2+3n_3=12.
\]

The only possibilities are (K_{2,3}) and (K_4): for (n_3=2,n_2=3), every degree-two vertex joins the same two degree-three vertices; for (n_3=4,n_2=0), simplicity forces (K_4). The all-degree-two possibility contradicts the edge condition. The independent support enumeration confirms exactly these two dense types.

For (K_{2,3}), first ordinarily color the outside graph and pad the at-most-three leaf boundary labels. Send a most frequent boundary label to the common omitted color. Each remaining boundary color then occurs at most once. The prescribed missing colors at the three leaves can consequently be completed to a permutation of the two retained base colors and a temporary exterior color. Coloring the two stars by cyclic successors and predecessors gives a proper support coloring respecting the boundary. Edges with the temporary exterior color form a matching, so their individual exterior colors can be restored without conflict.

All 27 boundary words were checked, and restoration was additionally tested for all 203 exterior equality patterns for each word, giving 5,481 successful restoration checks. Thus the uniform six-unit conclusion is accepted. It does not dispose of the variable-omission residual patterns.

## Reproducibility and negative controls

The complete method-analysis input packet passed integrity verification. Eleven regenerated result files match the recorded outputs exactly. The independent verifier gives identical results under ordinary Python, `-O`, and `-OO`; its checks do not rely on removable assertions. Both new C++ enumerators also reproduce their exact outputs under undefined-behavior sanitization, with no sanitizer finding.

Eleven deliberate negative controls were rejected: a missing ordinary coloring, a duplicated coloring, a missing palette permutation, an erased genuine conflict, invalid list membership, loss of the selected edge's exterior color, an altered success count, reinstatement of the false extension property, a changed pointwise classification, an omitted exterior partition, and an incorrect residual count.

The accepted deliverable is the complete mathematical audit and its aggregate scope. Executable verifiers, raw finite collections and coordination material are excluded from this prose edition. Reproducing the bounded computational classification requires a fresh implementation and regenerated records; the complete symbolic arguments and explicit small examples are inspectable here. The accepted scope remains a complete bounded method classification and explicit examples of its limitation; no unrestricted conjectural conclusion is inferred.
