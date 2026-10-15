# Independent audit: five-edge strict residual-certificate classification

Audit date: 12 October 2026 UTC.

## Verdict and exact accepted scope

**ACCEPTED as a bounded method-classification packet, with no mathematical correction required.** The entire candidate, distributed here as METHOD_CLASSIFICATION.md, was read and its original research inputs were independently checked for integrity. Original input identities and inventory metadata are omitted. MANIFEST.json identifies only the actual distributed authored files. No remote state was changed.

The accepted conclusions are:

1. Complete classification of the **strict residual-deficit certificate** on five-edge supports of finite simple graphs of maximum degree at most three, with arbitrary nonempty exterior lists of sizes one through three.
2. Exactly 20 line-graph support types, 3,635,009 generated normalized list families per support, and 72,700,180 support/family decisions.
3. Exactly the supplied 65 raw normalized failures, reducing to exactly the supplied 34 support/color orbits, including their multiplicities. This is equality of the complete failure records and orbit representatives, not merely agreement of counts.
4. Every failure has matching number two, exterior palette size at most three, and exact minimum residual deficit three. The raw profile counts are 20 for 11111, 8 for 11112, and 37 for 11222. The orbit counts are respectively 15, 3, and 16.
5. Both equality-Hall lemmas, and their use to overcome 14 of the 16 profile-11222 classes for every interior-list choice and every critical supergraph containing that edge-incidence support.
6. The two remaining profile-11222 classes have edge-adjacency graph K3 disjoint union K2, with a common two-color exterior list on K3 and a common singleton exterior list on K2. The singleton is either in or outside the two-color list. The two orbits are distinguished by whether the singleton exterior color belongs to the common two-color exterior list.
7. The stated five-vertex, seven-edge graph is actually maximum-degree-three and edge-critical for three-edge-colorability. Its stated five-cycle exceptional support has no strict certificate. The stated fixed ordinary coloring fails all six palette permutations, and the single stated Kempe switch followed by the stated permutation produces the supplied valid full list coloring.

This is **not** acceptance of the unrestricted finite-simple critical-edge-list conjecture, a five-arbitrary-exception theorem, or a counterexample. Failure of this numerical method is not uncolorability. The separate constructive five-cycle theorem is outside this audit's acceptance boundary.

## 1. Why the certificate is sufficient

Let A have three colors and let d(e)=|L(e) minus A|. Since every list has exactly three colors and every exceptional list differs from A, d(e) is in {1,2,3}, and exactly d(e) colors of A are forbidden at that edge.

For a nonempty exterior-colored set F, choose an edge f in F. Criticality supplies a three-edge-coloring of G minus f, whose restriction supplies an ordinary coloring of G minus F. A uniformly random permutation of its labels into A violates the list at residual exceptional edge e with probability d(e)/3. If the total residual deficit is less than three, the union bound is strictly less than one. Some permutation respects all residual lists. Exterior colors are disjoint from A, so combining the two proper colorings introduces no cross-conflict.

Conversely, any full list coloring partitions into its exterior-colored edges and its A-colored edges. In an uncolorable-for-A critical graph the exterior set is nonempty. Therefore an obstruction to every such exterior set and every ordinary complement coloring would itself be a genuine counterexample; the packet correctly avoids claiming this from failure of a strict certificate or a selected ordinary coloring.

## 2. Independent support coverage

The audit independently constructed five-edge supports **edge by edge**, without importing either author support generator. Vertex labels are introduced at their first appearance. The next unordered edge is either:

- between two previously introduced vertices;
- between a previously introduced vertex and one new vertex;
- between two new vertices.

Loops, repeated edges, and degrees above three are excluded. These three alternatives exhaust the possibilities for the next edge of every simple subcubic graph after relabeling vertices by first appearance. Thus coverage is complete, including disconnected supports. Isolated vertices outside the support are irrelevant.

There are 2,385 resulting unoriented constructions. Canonicalizing their five-vertex edge-adjacency graphs under all 120 edge permutations gives precisely 20 line-graph types, exactly equal to the supplied support set. The raw canonical-mask collection is not distributed.

For comparison with the packet's ordered-endpoint enumeration, every edge touching a previously introduced vertex has two endpoint orientations; an edge introducing two vertices has one restricted-growth orientation. Summing these weights over the independently constructed supports gives exactly 18,745 endpoint partitions, confirming the stated count by a different traversal.

Every stored reconstructed support was separately checked for simplicity, degree bound, edge-adjacency mask, adjacency array, and matching number. The C++ solver's text input was checked for exact equality with these validated support records.

There are 20 **line-graph types**, not necessarily 20 underlying graph isomorphism types. In particular a triangle and a three-edge star have the same line graph. The packet uses the correct edge-adjacency equivalence for exterior-coloring decisions.

## 3. Arbitrary-palette normalization

At each of the five ordered lists, choose its size d in {1,2,3}, choose s old colors from the p already introduced colors, and introduce d minus s consecutive new names. Every original family can be renamed this way by naming colors when they first occur. Every generated family is a valid exterior-list family. Simultaneously introduced colors can create redundant representatives of a color-relabeling orbit; neither the candidate nor this audit assumes duplicate-free orbit generation.

The separately evaluated recurrence is

N(i+1,p+d-s) += N(i,p) times binomial(p,s), with N(0,0)=1.

It gives 3, 36, 960, 46,611, and 3,635,009 families after one through five lists. Fifteen colors is the logical maximum number of entries in five lists of size at most three, not a heuristic palette cutoff. The C++ generation uses explicit combinations of old colors and new blocks; its exact terminal count agrees with the recurrence.

## 4. Independent exact decisions on every case

The audit wrote a fresh C++ exact solver. No author code was imported or executed. The algorithm is independent-color-class dynamic programming, rather than either supplied full-scan backtracking algorithm.

For each exterior color c let V(c) be the edges whose lists contain c. A use of c is any independent subset I of the support line graph contained in V(c). Start with reachable covered set {empty}. Process colors one at a time, replacing reachable coverage R by all unions R union I. This is exact:

- Any proper partial coloring gives one independent color class for each color, hence its covered set is reached.
- Any reached union can be colored by the recorded color classes. If an edge appears in multiple classes, retain any one of its memberships. Removing memberships preserves independence, so the union is still properly colorable.

A strict certificate exists exactly when a reached nonempty covered set leaves deficit below three. All independent subsets, all covered subsets, and all colors are processed exactly; there are only 32 edge subsets. No timeout or search cutoff is converted into failure.

Two modes of this fresh implementation were run to completion:

- A shared-success mode first finds a certificate for the complete five-vertex conflict graph. Its 3,632,083 successful families certify every support; it explicitly evaluates the remaining 58,520 support cases.
- A direct mode disables that shortcut and explicitly evaluates **all 72,700,180 support/family cases**. Its actual support-decision counter is 72,700,180.

Both modes produce byte-identical complete failure outputs, and the failure set equals all 65 original obstruction records exactly. The per-support raw output collection is not distributed.

The direct run completed with exit status zero. Every original per-support case count, deficit-profile count, palette count, and supplied example was checked against the independent failures.

These are two executions of **one fresh decision implementation**, not a claim of two new independent full-scan algorithms. The supplied author executables were not rerun. Their stored results were checked against the independent direct run instead.

## 5. Exact minima and orbit classification

A separate Python Cartesian enumerator assigns to each edge either a listed exterior color or an omitted marker, rejects incident equal colors, and minimizes the sum of deficits of omitted edges. This is distinct from the full-scan DP. For every one of the 65 failures it exhausts all assignments and finds minimum exactly three, recording a witness.

Every failure lies on a support of matching number two. Exterior palette-size counts are 8 on one color, 45 on two colors, and 12 on three colors. On the five-cycle support, the sole raw failure is five identical singleton exterior lists.

Orbits were recomputed by directly applying **every support automorphism and every exterior-color permutation to ordered lists**, rather than using the packet's color-incidence-multiset canonical key. This confirms all 34 representatives and all multiplicities. The stored incidence arrays and deficit arrays were checked against the representative lists themselves. Thus orbit equality, representative validity, and the distinction between the two remaining profile-11222 classes are independently established.

## 6. Hall equality cases and universal 14-class escape

For three residual unit deficits, each constraint forbids one entry of the three-by-three palette permutation matrix and excludes exactly two of the six permutations. All permutations fail exactly when the three excluded two-element sets are pairwise disjoint. Two such constraints are incompatible exactly when they occupy the same row with different columns or the same column with different rows. A pairwise-incompatible triple must be a full row or a full column. Hence failure occurs exactly when either:

- all three ordinary labels agree and the omitted colors are all different; or
- all three ordinary labels are different and the omitted color is the same.

The audit independently constructed the three label domains and exhaustively tested all 729 input combinations. Exactly 36 fail, with exact agreement with this characterization.

For deficits two and one, let a be the sole allowed A-color of the first edge and b the forbidden A-color of the second. If their ordinary labels agree, their common image must equal a and differ from b. If their labels differ, assign a to the first label and choose an image different from b for the second among the other two colors. Thus failure is exactly equality of labels together with a=b. All 81 cases were tested, giving precisely nine failures.

An incident residual pair must have different ordinary labels. Consequently it always permits a palette permutation. Direct Cartesian enumeration of the profile-11222 representatives found the required exterior coloring in exactly 14 classes, with explicit independently found witnesses retained privately. The raw class-index collection is excluded from this prose edition.

The only two classes without this incident-pair escape are the common-list K3 disjoint union K2 line-graph classes described above. Their common-list and component-incidence descriptions were checked directly. Here K3 disjoint union K2 refers to the **line graph**, not an assertion that the original support contains a triangle rather than a star. The remaining classes are not claimed uncolorable.

The 14-class inference is universal: the selected exterior coloring uses three support edges, criticality colors its complement ordinarily, the incident residual pair has different labels, the Hall lemma permits the required palette permutation, and exterior/ordinary colors cannot conflict across the partition.

## 7. Actual-critical fixture and exact repair

The ordered edge list is (04,41,02,03,12,13,23). It is simple and has actual maximum degree three. Seven edges on five vertices cannot be covered by three matchings of size at most two, so it is not three-edge-colorable. Independently, exhaustive testing of all 3^7 ordinary assignments finds none. Every edge deletion has a proper three-edge-coloring, verified both by new exhaustive searches and by checking every supplied deletion witness.

For X={e0,e1,e3,e4,e6}, all exceptional lists are {0,1,3} and other lists are {0,1,2}. The support is C5, and its exterior lists are all {3}. Exterior-colored sets are matchings of size at most two, leaving at least three unit deficits. A two-edge matching attains three, so the strict criterion fails exactly at equality.

With F={e3,e4}, the supplied ordinary coloring (on e0,e1,e2,e5,e6) is (0,1,1,0,2). It is proper, and every one of the six palette permutations fails. The (0,2)-component containing e0 is exactly {e0}; at its endpoints, every remaining adjacent edge has color 1. Switching that component therefore preserves propriety. The palette permutation (2,0,1) then yields the full ordered coloring

(1,0,0,3,3,2,1).

Every edge's list membership and every incident edge pair were checked. The exterior set is held fixed throughout. This is an explicit repair of a method obstruction, not a proof that a single Kempe switch repairs all obstruction classes.

The exceptional-support-size minimality is also consistent with the independent classification, without importing the separate four-exception theorem. Pad any support of at most four edges to five with isolated fresh-singleton exterior edges. Such a padded support has matching number at least three: four pairwise-incident edges cannot occur in a simple subcubic graph, and smaller supports have enough isolated additions. No classified failure has matching number at least three. Restrict its certificate back to the original support; if the original colored set is empty, its total deficit is already below three and coloring one original edge exteriorly restores nonemptiness. Thus fewer than five exceptional edges cannot first obstruct this strict criterion.

## 8. Negative controls and limits

The independent validator rejected all seven deliberate negative controls:

1. deleting a genuine obstruction from the claimed complete failure set;
2. injecting a colorable family as an obstruction;
3. falsely declaring residual minimum three for five singleton lists on an edgeless conflict graph;
4. treating residual equality three on C5 as a strict certificate;
5. changing the fixture coloring to give incident edges equal colors;
6. changing a fixture color to a value outside its list;
7. merging the two genuinely different remaining profile-11222 orbits.

The complete validator also passed under Python's `-OO` optimization and produced identical output. Its critical checks are explicit exceptions, not removable assertions.

Limits: the two original author full-scan executables were not rerun; a fresh complete direct solver replaced that check. The audit verifies mathematical and finite-computational correctness of the supplied scoped conclusions. It does not establish novelty, inspect an external literature source, prove the unrestricted conjecture, prove all five-exception supports colorable, or classify arbitrary Kempe-reconfiguration behavior. It does not import acceptance of the separate constructive five-cycle theorem. Source code, raw certificates, and coordination material remain private; any publication of this audit should preserve the stated scope and exclude private reproduction material.

## Reproduction boundary of this prose edition

All explanatory proofs, normalization and support-generation arguments, exact decision-method descriptions, aggregate counts, finite domains, controls and optimization limits are retained. The complete support, failure and orbit collections, run outputs, executable programs and raw witnesses are excluded. In particular, this prose does not enumerate the 34 orbit representatives and cannot by itself reproduce their full records, multiplicities or the complete finite classification. Independent computational reproduction requires fresh implementation and new record generation. The separately audited symbolic C5 proof in FIVE_CYCLE.md is complete and does not use the omitted classification as a black-box premise.
