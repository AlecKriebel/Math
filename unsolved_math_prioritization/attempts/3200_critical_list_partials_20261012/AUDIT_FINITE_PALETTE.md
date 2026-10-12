# Independent audit: finite-palette reductions and OPG-388 certificates

## Decision and exact scope

**ACCEPT AS PARTIAL MATHEMATICAL AND COMPUTATIONAL EVIDENCE. No full conjecture resolution, counterexample, or novelty claim is accepted.**

The complete finite-palette candidate and its supporting finite checks were independently audited. The complete input inventory was checked before and after substantive verification and was unchanged. Original input identities and excluded-file metadata are not distributed here.

Accepted results are:

1. A bad nonconstant k-list assignment on a (k+1)-vertex-critical graph with n vertices can be replaced by a bad nonconstant assignment using at most n−1 colors.
2. A minimum-palette bad nonconstant assignment with q≥k+2 has every color pair co-occurring in some list; hence q(q−1)≤nk(k−1).
3. Every nonconstant 3-edge-list assignment colors the graph obtained by subdividing one edge of K4 once, including arbitrary color palettes. The sole constant obstruction has an elementary structural proof. This special case is already implied by a published theorem.
4. The exhaustive simple-graph census through seven nonisolated vertices and its five 3-edge-critical isomorphism types are correct within the stated scope.
5. For those five representatives and Petersen minus one vertex, every nonconstant assignment from a palette of at most four colors is colorable. This does not prove arbitrary-list colorability of the larger five graphs.
6. All six graphs are genuinely 3-edge-critical, with independently checked deletion witnesses and structural or exhaustive-tree noncolorability proofs.

The target remains the finite simple-graph formulation recorded by [Open Problem Garden](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs): a Δ-edge-critical graph should be colorable from every nonconstant exact Δ-list assignment. The target does not permit treating the obvious constant obstruction as a counterexample.

## Mathematical audit

### Hall reduction preserves nonconstancy

The proof passes without an added hypothesis. If the original palette size q is already below n, it is already an acceptable witness. Otherwise an SDR would give a coloring irrespective of the graph's edges; badness therefore forces a positive Hall deficiency.

Choosing S with maximum deficiency, rather than merely choosing an arbitrary Hall-deficient set, is essential and is done correctly. Since q≥n, the full vertex set has nonpositive deficiency, so S is proper. If the outside lists after removing B=∪L(S) had a Hall-deficient subfamily T, then the exact disjoint-union identity

|∪L(S∪T)| = |B| + |∪(L(v)\B : v∈T)|

would increase the deficiency. Thus the outside family has an SDR. Its distinct colors all avoid B, so any coloring on S would extend across every crossing and outside edge. Consequently the restricted assignment is bad.

Vertex-criticality is used exactly where needed: a proper induced subgraph is k-colorable, so a bad restriction on S cannot have all lists equal to one k-set. This supplies genuine nonconstancy inside S. Replacing all outside lists by any k-subset of B leaves that bad nonconstant restriction intact and gives a palette of size |B|<|S|<n. The transformed case in fact has at most n−2 colors; the original q<n case accounts for the final n−1 bound.

For a Δ-edge-critical graph with m edges, its line graph has chromatic number exactly Δ+1. An edge-deleted Δ-coloring plus one fresh color establishes the upper bound, and the original obstruction establishes the lower bound. Deleting any line-graph vertex, and then any further vertices, leaves a Δ-colorable graph. No use of Vizing's theorem is needed.

### Minimum-palette compression

The separate minimum argument also passes. All lists have size k, so nonconstancy implies q>k. If a pair a,b never occurs together, identifying it leaves every list's cardinality unchanged. A coloring after identification lifts vertex by vertex, because adjacent vertices cannot both use the identified color. The original assignment's badness therefore implies badness after merging.

For q≥k+2 the resulting palette has q−1>k colors and cannot be constant. That contradicts minimality. The exceptional q=k+1 case is necessary: a merge there may make the assignment constant, and no compression conclusion is claimed for that case.

Counting all unordered color pairs against the n lists gives the claimed inequality. Choosing a minimum-palette witness also permits the Hall bound simultaneously, since the Hall argument first establishes that some witness has palette at most n−1. This is not an iteration that assumes unjustified preservation of criticality.

For the particular bounded examples, the two reductions limit a hypothetical witness to at most six colors when m=7, at most eight when m=10, and at most nine when m=12. The four-color scans on the larger graphs do not exhaust these bounds.

## Full seven-edge certificate audit

The seven original edges were checked directly. Vertex 0 is the subdivision vertex between vertices 1 and 2; suppressing it produces K4. Its maximum degree is three. Any color class is a matching of size at most two on five vertices, so seven edges cannot be colored with three colors. This is a proof of the constant obstruction, independent of a search result or sentinel.

All seven deletion vectors in the candidate itself match the corresponding verified data, have the correct deleted position, use only the three permitted colors, and give different colors to each pair of incident surviving edges. These facts prove 3-edge-criticality.

### Coverage and normalization

Relabeling the first list to {0,1,2} is valid. At each later list, new colors can receive the next unused labels; retained colors keep their already assigned labels. The resulting used-color set is always an initial segment. This describes a global bijective renaming of the original palette, not separate incompatible renamings per list. Every assignment with palette at most six has at least one such representation. Multiple representations are harmless, and no uniqueness assumption enters the proof.

The independent checker enumerates all 6-color masks with exactly three bits whose union with the previously seen initial segment remains an initial segment. It orders these choices by the old-color mask only to align them with the frozen byte stream. This differs from the generator's construction of old subsets and appended fresh blocks. The independent histogram recurrence counts choices by the number of retained colors.

The resulting complete histogram is:

- 3 colors: 1 assignment
- 4 colors: 4,095 assignments
- 5 colors: 662,571 assignments
- 6 colors: 19,124,343 assignments
- Total: 19,791,010 assignments

The raw coloring-witness collection is not distributed with this edition. Its exact identity and storage size are omitted.

An independently authored checker decoded every record. It checked every list membership, used endpoint-local color sets to reject every incident-edge conflict, rejected nonzero reserved bits, required the bad sentinel to represent a constant assignment, matched the complete histogram, and required exact end of file. **All 19,791,009 positive records passed, and there was exactly one constant sentinel.** This was a full check, not a sample. It was repeated with the independent C++ checker compiled using `-DNDEBUG`; the same output was obtained because this checker uses explicit runtime checks rather than removable assertions.

Combining exhaustive normalized coverage with the Hall reduction proves this special graph's arbitrary-palette assertion. Added isolated vertices have no effect on edge lists or edge coloring.

## Published-theorem boundary

The primary [Kaul–Mudrock paper, arXiv:1805.02147v2](https://arxiv.org/pdf/1805.02147v2) was inspected directly. Lemma 3 on printed page 8 and Conjecture 6 on printed page 11 support the candidate's cited scope. Lemma 3 starts from a strong k-chromatic-choosable graph and adds two independent vertices with neighborhood sets A,B covering the base. It requires both sets to properly contain their nonempty intersection, with intersection size at most four for odd k, and requires the resulting chromatic number to exceed k.

The claimed map (v1,v2,v3,v4,v5,u,s)↦(e0,e2,e6,e5,e1,e3,e4) was independently checked for equality of the entire 13-edge graph, including the missing u–s edge and absence of extra base edges. The base is C5; the two neighborhoods each have size four, their intersection has size three, and the resulting chromatic number is four. Thus Lemma 3 applies exactly. C5's required strong property also has an elementary proof: for a nonconstant 2-list assignment choose adjacent differing lists, color their first endpoint with a color absent from the second, and greedily follow the cycle the other way. The last endpoint then has only one relevant forbidden color.

No upward-monotonicity inference under arbitrary edge addition is used or reinstated. The computation independently confirms an already-covered special case and carries no novelty conclusion.

## Independent bounded computations

### Complete graph census within the stated order bound

A fresh C++ program enumerated all edge-subset bit masks of complete graphs for 3≤n≤7, selected the stated edge-count range, and independently checked degrees, connectedness, exact three-edge-colorability and every edge deletion. Its coloring routine uses fixed original edge order and endpoint color occupancy, rather than the candidate's minimum-domain recursion. Isomorphism classes were identified by minimization over all degree-compatible vertex permutations.

Every census count matched:

- n=3: 1 edge-count candidate; 0 connected degree-filtered candidates; 0 critical graphs
- n=4: 22; 7; 0
- n=5: 582; 100; 30 labeled critical graphs in 1 isomorphism type
- n=6: 22,880; 1,690; 0
- n=7: 966,416; 34,440; 5,670 labeled critical graphs in 4 isomorphism types

The independent canonical representatives match the candidate's five exact edge sets. A separate permutation/isomorphism check found automorphism-group sizes 4 for the five-vertex graph and 4,2,4,8 for the four seven-vertex representatives. Orbit-stabilizer gives labeled orbit sizes 30 and 1,260+2,520+1,260+630=5,670, respectively.

The filter is mathematically adequate for nonisolated 3-edge-critical graphs. A leaf edge could always be restored after deletion, contradicting noncolorability. There cannot be another nontrivial component besides an obstructing component, since deleting an edge outside it would leave the obstruction. Minimum degree two forces m≥n, and maximum degree three forces m≤floor(3n/2). No larger-order classification is claimed.

### Six independent four-palette searches

The fresh fixed-order solver separately exhausted all four-color-palette assignments after fixing the first list to {0,1,2}. All successful colorings were independently checked in memory. The complete totals were 4,096 for m=7; 262,144 for each of the four m=10 graphs; and 4,194,304 for m=12. Each scan had exactly one bad assignment, the constant one. This is 5,246,976 assignments in total and 5,246,970 checked positive witnesses.

Each graph input was independently reconciled to its frozen edge data. The three-subset-of-four model and first-list relabeling cover exactly the claimed four-palette domain. Nothing in these scans implies colorability from an arbitrary larger palette on the m=10 or m=12 graphs.

### Petersen obstruction and all deletion witnesses

A direct graph-isomorphism check verified that the nine-vertex input is Petersen minus one vertex. Its twelve edges equal the capacity 3 floor(9/2), so overfullness cannot prove its noncolorability.

The supplied negative tree was verified independently from its root. At every node the checker confirmed an unassigned valid edge, recomputed the legal colors from endpoint occupancy, and required exactly one child for every legal color and no others. No root color or later legal branch was factored out or omitted. Empty children were accepted only for empty legal domains. A branch reaching a complete coloring would be rejected. The verified tree has exactly 232 nodes and 36 dead-end leaves, proving noncolorability.

All 59 deletion witnesses across the six graphs passed. The other five graphs have independent overfullness obstructions; Petersen has the exhaustive negative tree. Together these are complete criticality certificates for the six displayed graphs.

## Negative controls and verification robustness

All twelve deliberately invalid controls were rejected by explicit runtime checks:

- A color outside its list
- A nonzero reserved record bit
- An incident-edge color collision while list membership remains valid
- A bad sentinel on a nonconstant assignment
- A truncated final record
- A trailing byte after the final record
- An incorrect deletion marker
- A collision in a deletion witness
- A missing legal Petersen root branch
- An added illegal Petersen root color
- Reusing an already assigned tree edge
- Fabricating a continuation from a dead-end leaf

The Python packet checks and reconciliation were run normally, with `-O`, and with `-OO`; all passed, with the same results. The independent C++ checker passed normally and with `-DNDEBUG`. The source packet's supplied assertion-based checkers must retain assertions if used directly; the audit acceptance does not depend on disabling or trusting those checkers.

## What was and was not rerun

Performed independently: every binary-record check; all counts and normalization checks; every deletion witness; the complete Petersen negative-tree validation; Petersen identity; exact published-construction equality; the complete bounded labeled-graph census; representative/automorphism checks; and all six full four-palette scans. The complete input inventory was rechecked afterward.

Not rerun: the original certificate-generating coloring search for all six-color normalized assignments, the original programs as programs, or the original Petersen tree-generation procedure. Those are unnecessary for acceptance because every positive certificate record and every negative-tree branch was independently checked. No all-palette search for the larger graphs, graph search beyond seven vertices, general-Δ classification, or exhaustive literature/novelty survey was undertaken.

This edition distributes authored proof and aggregate audit prose, not programs, raw certificate collections, or copied source documents. The large witness collection and Petersen decision tree cannot be reconstructed from the prose alone. The known Lemma 3 argument in FINITE_PALETTE.md separately proves the subdivided-K4 case; the larger-graph computational claims retain only their stated finite coverage.
