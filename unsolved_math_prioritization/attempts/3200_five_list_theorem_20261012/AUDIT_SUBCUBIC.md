# Independent audit: five exceptional lists in subcubic edge-critical graphs

Date: 12 October 2026 UTC.

## Verdict and exact scope

**Accepted. No mathematical correction is required to the frozen candidate.** The proof establishes the five-exception theorem by a complete symbolic case split. It does not depend on the earlier 72.7-million-case exterior-certificate classification, a bounded exterior palette, a list of support representatives, or the complementary boundary enumeration.

The exact new statement accepted here is:

Let G be finite and simple, with maximum degree three, with no proper three-edge-coloring, and with a proper three-edge-coloring of G−e for every edge e. Fix a three-element color set A and give every edge a list of exactly three colors. If exactly five lists differ from A, then G has a proper list-edge-coloring.

Combining this with the previously accepted one-through-four-exception theorem gives the candidate's stated range 1≤|X|≤5. The one-through-four result is used in this combination, not in the proof of the exactly-five result. The prior acceptance record is [the first-round structural audit](../3200_critical_list_partials_20261012/AUDIT_NEAR_CONSTANT.md); this audit read that record, rather than claiming a fresh repetition of all of its proofs and computations.

The result applies to arbitrary finite color names and arbitrary orders of G under the stated hypotheses. It does not settle assignments with more than five exceptions, graphs of maximum degree greater than three, or the unrestricted conjecture. No historical novelty or comprehensive literature-status conclusion is made.

### Audited mathematical inputs

The complete principal mathematical text, including every case and preliminary lemma, is distributed as [SUBCUBIC.md](SUBCUBIC.md). The auditor verified the integrity of the complete principal packet and a complementary five-exception analysis. The original source-file identities, inventories and coordination records are excluded from this prose edition. The complementary material is not an additional premise of the theorem.

The complementary packet's symbolic support lemmas, matching-recoloring proof, and h≥4 proofs were also checked directly. Their arguments agree with the principal proof. The complementary boundary enumeration is not a dependency of the accepted theorem; its published numerical counts were not independently rerun by this audit. Independent computations described below were newly written without importing either author's programs, results, or support tables.

## 1. Basic reduction and equality cases

Exact list size is essential: from |L(e)|=|A|=3 one obtains d(e)=|L(e)∖A|=|A∖L(e)|. Each exceptional edge therefore has a nonempty exterior list, and each deficit is 1, 2, or 3.

For every nonempty F⊆X, criticality supplies an ordinary coloring of G−F by restricting a coloring of G−f for any f∈F. This uses no extension theorem and does not require G−F to be critical. Every exterior set used by the proof is nonempty. Isolated vertices and unused ordinary labels cause no problem.

A proper exterior coloring of F has no color conflicts with a permuted ordinary coloring of G−F because their palettes are disjoint. The only remaining constraints are membership in the lists of residual exceptional edges. Under a uniform permutation, an edge of deficit d excludes probability d/3. The strict union-bound argument is correct without independence of the bad events.

Both equality criteria are exact for this specified completion method:

- Three unit deficits forbid at most three cells of a 3×3 label-to-color matching problem. Hall failure on one row requires all three cells of that row to be forbidden: one ordinary label and three distinct omissions. Failure on two rows would require at least four forbidden cells. Failure on all three rows requires one entire column missing: three distinct ordinary labels with one common omission. Repeated constraints cannot create additional forbidden cells.
- For a residual deficit-two edge retaining a and a unit-deficit edge omitting b, equal ordinary labels fail precisely when a=b. With different labels, fixing the first image to a leaves at least one permissible image for the other label. Incident residual edges always have different labels.

These criteria assert necessity only for a fixed ordinary coloring and a single palette permutation. The proof correctly changes deletion colorings where a fixed coloring need not work.

## 2. Structural and list lemmas

### Incidence geometry

Four pairwise-incident distinct edges of a simple graph form a star: once a pairwise-incident family is not a star, it is confined to a triangle. The maximum-degree-three hypothesis therefore makes H K4-free.

For incident uv and uw, an additional edge meeting both either uses u or is vw. At most one further edge uses u, giving at most two common neighbors in H.

A pairwise-incident triple is a three-star or a triangle. Its center is saturated in the star case; an outside edge meeting two specified star edges must join their two leaves, so simplicity makes it unique. In the triangle case, an outside edge meeting a specified pair uses their shared vertex; two such outside edges would create degree four. No outside edge can meet all three. These observations justify both the h=2 selection and the more restrictive h=4 eligibility argument.

### At most four vertices with lists of size at least two

The claimed equivalence is correct: a K4-free graph on at most four vertices is uncolorable precisely when it contains a triangle with one identical two-element list at all three vertices.

Forests, an isolated extension of a triangle, a pendant extension of a triangle, and C4 cover all cases except the diamond. A triangle has an SDR unless its total list union has size two. An even cycle's nonconstant-two-list greedy argument handles the final edge because the initial color is absent from its list; constant lists alternate.

In the diamond, any proper color pair on the adjacent degree-three vertices blocks a tip only if that tip's whole list is exactly this two-set. The two tips therefore block at most two unordered pairs. Unless both central lists are the same two-set, distinct central choices realize at least three unordered pairs. To see this explicitly, two unequal two-subsets have either three cross pairs when they overlap or four when disjoint; an additional color beyond a common two-subset creates a third pair. In the sole one-pair case, an uncolorable tip is exactly a bad triangle. Tips are nonadjacent and can be extended independently.

Larger lists introduce no hidden exception. In particular, lists of size at least three cannot themselves be the obstructing common two-set.

### Five-vertex triangle transversal and three-choosability

For a universal vertex, any triangle avoiding it would create K4. Otherwise maximum degree is at most three, so two distinct triangles cannot intersect in just one vertex and cannot be disjoint on five vertices. If their common edge is 12 and the triangles are 123 and 124, vertices 1 and 2 are saturated and cannot meet vertex 5. Any triangle avoiding 1 would require 34, creating K4 on 1234. Thus some vertex lies in every triangle.

For three-choosability, a vertex of degree at most two can be restored after coloring the remaining four vertices by the preceding lemma. Otherwise the complement has maximum degree one. K4-freeness forces exactly two disjoint complement edges, giving a four-cycle with a universal hub. Color the hub first; every rim list retains at least two colors, so C4 completes. The complementary packet's parity-based derivation of the same wheel is also sound.

This proves a graph-theoretic fact, not merely a finite tested classification. As a side consequence, no graph satisfying the principal criticality hypotheses can have at most five edges: its whole line graph would be three-colorable. Thus a positive exceptional set of size at most five really is a nonconstant assignment under these hypotheses.

## 3. Exhaustive symbolic case audit

Let h count the five exceptional edges with deficit at least two.

### h=0

When omissions are not all equal, a matching of size three immediately leaves residual deficit two. Otherwise the maximum matching has size two. After removing any particular edge, the remaining four edges are not pairwise incident, so some two-edge matching avoids the removed edge. Consequently complements of two-edge matchings cover X. These three-subsets of a five-set intersect pairwise; if each had constant omissions, their intersections and covering property would force all five omissions equal. Hence a complementary triple with nonconstant omissions exists. It cannot have one ordinary label, since that would itself be a matching of size three. Both three-unit equality obstructions are excluded.

For a common omitted color a, an exceptional edge with at most two exceptional neighbors permits a label t absent from those neighbors in a coloring of G−e. Adding e to the exceptional edges colored t produces a matching. Giving those edges their own exterior colors is proper even when the exterior colors coincide. Mapping t to a leaves every residual exceptional edge with one of the other two, permitted base colors. This recoloring lemma is valid for any number of exceptions when its local hypothesis holds.

If all five vertices of H have degree at least three, H is the wheel already established. A rim vertex e has a unique nonneighbor f adjacent to every neighbor of e. In a coloring of G−e, φ(f) is therefore absent from all exceptional neighbors of e. The same matching construction applies. It is legitimate to select a deletion coloring here; the proof never claims that an arbitrary prior coloring of G−X has this property.

### h=1

If the large deficit is three, some pair of small edges can be exterior-colored: failure for every pair would make the four small edges a clique with one common singleton exterior color, violating K4-freeness. The large edge then avoids at most two used colors, leaving two residual unit deficits.

For large deficit two, suppose it misses a small edge f and no strict certificate exists. A colorable pair consisting of f and another small edge would allow the large edge to be added, since it sees at most the other small edge. Therefore f meets all three other small edges and all four singleton exterior colors agree. Those three others contain a disjoint pair, or together with f they would form K4. Color that pair with its common exterior color and give the large edge its other exterior color. This is a strict certificate, a contradiction. Hence the large edge is universal whenever the strict method has failed.

In the universal case, color G−f for a small f and retain the original label of the large edge before removing it. All three residual small edges avoid that label. At least two are incident, by their allocation to the two endpoints of the large edge, so their labels cannot all coincide. Their labels use exactly two colors. Neither equality obstruction is possible, regardless of omissions. This deletion-conditioned completion is valid.

### h=2

For nonincident large edges, color any small edge first and then each large edge avoiding at most the small color. For incident large edges, at most two edges meet both, so one of the three small edges meets at most one. The selected triple's adjacency graph is a forest rooted at the small edge. Each large edge has at least two colors and at most one already colored neighbor. Exactly two unit deficits remain.

### h=3

If the large triple fails to exterior-color, it must be a triangle in H with the same two-element exterior list at every vertex. A forest would color greedily, and a triangle with these list lower bounds has only the stated Hall obstruction. In particular every large deficit is exactly two.

If a small-large incidence exists, consider retaining such an incident pair. Its complementary set consists of the other two large edges and the other small edge. That exterior triple fails exactly when the small color belongs to the common two-set and the small edge meets both large edges. If every incident residual pair failed, beginning with e incident to s forces t to meet the other two large edges f,g and miss e. The residual pairs (f,t) and (g,t) would then force s to meet e,g and e,f, respectively, so s would meet all three large edges. This is impossible. A successful complementary exterior coloring therefore leaves an incident 2+1 residual pair.

If there are no small-large incidences, a retained large base color different from a retained small omission invokes the 2+1 equality criterion directly. If every such choice agrees, all three large retained colors and both small omissions equal one a. An ordinary coloring of G−s gives the large triple three distinct labels. Choose a large edge whose label differs from that of t, retain those two edges, and exterior-color the others. The residual labels differ, so completion succeeds. This is the most important use of a deliberately chosen deletion coloring in this branch.

### h=4

If the four large edges fail to exterior-color, the four-vertex lemma gives a bad triangle T with common exterior list {x,y}. Color the small edge s with z, and the fourth large edge h with w≠z. For each of x and y, at most one precolored edge can block it, and that edge meets at most two members of T; each eligibility set is nonempty.

Two nonempty eligibility sets fail to have distinct representatives only when both are the same singleton. That would force {z,w}={x,y} and both outside edges to meet exactly the same other two members of T. The simple-subcubic incidence uniqueness lemma excludes this. Coloring two different eligible T-members leaves its third member with residual deficit two. All selected colors are proper, including conflicts with both precolored outside edges.

### h=5

If all deficits are three, the five-vertex three-choosability lemma colors all exterior lists. Otherwise choose a deficit-two edge. With no bad triangle it may simply be deleted before applying the four-vertex list lemma. With bad triangles, choose a vertex meeting every triangle. Because at least one bad triangle exists, this chosen vertex lies in a bad triangle and has deficit two. Its deletion destroys all bad triangles. The other four edges exterior-color and leave deficit two.

Every h is covered. Every completion either leaves strict residual deficit below three or invokes one of the proved equality criteria after a valid deletion-coloring choice.

## 4. Independent executable corroboration

The proof above is the acceptance basis. The following are separately checked, precisely bounded computational statements.

### List and equality lemmas

The independent C++ checker uses an exact recursive list-coloring solver. Returned colorings are checked separately for list membership and properness. Failures raise exceptions rather than relying on assertions that optimization could remove.

- For four ordered vertices, it independently generates all 30,865 first-occurrence-normalized list families of sizes two or three. The generator chooses previously seen colors and then introduces consecutive fresh names; this covers every such family up to color renaming, with no arbitrary bound on the total palette. On all 63 non-K4 labeled four-vertex graphs, all 1,944,495 tests agree with the bad-triangle criterion. Exactly 239 fail.
- All 958 K4-free labeled five-vertex graphs pass the triangle-transversal and low-degree-or-wheel tests. All 4^5 assignments of three-element sublists of a four-color set are colored on every such graph: 980,992 cases. This last check is a bounded-palette corroboration, not the proof for arbitrary lists.
- All 729 choices of three ordinary labels and three omissions, and all 81 choices for the 2+1 equality criterion, agree with direct enumeration of the six permutations.

### Independently generated incidence supports

The independent support checker generates first-occurrence-normalized partitions of ten edge-endpoint slots, rejecting loops, duplicate edges, and degrees above three when each edge closes. Every simple five-edge subcubic support, including disconnected supports using up to ten vertices, has such a representation. No supplied support table is read.

The 18,745 valid endpoint partitions produce 673 distinct labeled incidence graphs. On this full generated family the script verifies:

- 3,140 incident-pair common-neighbor bounds;
- 710 triangle-with-two-extra-edge incidence restrictions;
- 6,210 h=3 cross-incidence/color patterns;
- 8,520 h=4 distinct-precolor eligibility patterns;
- 70,080 nonconstant-omission patterns in the h=0 matching-number-two branch;
- 16,017 low-degree and 90 wheel ordinary-deletion-label patterns for uniform-omission matching recoloring.

The h=3 color check needs only whether each singleton color is x, y, or outside {x,y}. The h=4 check uses all distinct precolors from {x,y,z,w}, covering whether zero, one, or two precolors lie in the triangle palette. These are explicit symmetry reductions, rather than unsupported arbitrary-palette claims.

### Full-coloring constructions on critical fixtures

The two fixtures are K4 with one edge subdivided and the Petersen graph with a vertex removed. The independent solver verifies that neither is three-edge-colorable and that every edge deletion is three-edge-colorable. It caches valid ordinary deletion colorings, independently searches strict exterior certificates, and otherwise implements the proof's h=0, h=1, and h=3 deletion-coloring recipes. A second validation pass checks every completed coloring on the whole graph.

In total **1,841,454 full colorings** were constructed and validated:

- 1,240,029 cases exhaust every five-edge support of the seven-edge subdivided-K4 fixture and every exceptional three-list assignment from a five-color universe with fixed A={0,1,2}.
- 592,677 cases cover every five-edge support of both fixtures, every one of the 3^5 deficit profiles, and three deterministic exterior/base-palette placements. These are systematic tests, not exhaustive arbitrary-palette coverage.
- 8,748 targeted cases exercise all 243 interior-base choices on disconnected large-triangle/small-pair configurations with common exterior lists. These force the delicate equal-omission deletion branch as well as the mismatch branch.

Strict-certificate cases occur for every h=0,…,5. The non-strict construction counters include 22,660 nonconstant-unit cases, 252 uniform low-degree cases, 30 uniform wheel cases, 2,916 universal-large-edge cases, 17,593 cross-incidence h=3 cases, 4,338 disconnected-mismatch cases, and 54 disconnected-equal cases. Thus no principal non-strict proof branch was left unexercised by the full-coloring check. The separate incidence controls test h=4 eligibility directly rather than merely finding another certificate.

### Negative controls and hypothesis boundaries

The code checks explicit controls:

- K4 with one common three-list is uncolorable, so the K4-free hypothesis cannot be omitted from three-choosability.
- C5 with one common two-list is uncolorable and has no bad triangle, so the four-vertex lemma cannot be extended to arbitrary order as stated.
- For a triangle with edges 01,02,12, the two extra edges 03,04 meet the same pair 01,02; degree four violates the needed incidence uniqueness.
- For the three-star 01,02,03, two parallel copies of 12 also meet the same specified pair; simplicity is essential to that uniqueness assertion.
- The exhaustive equality tests include both three-unit Hall failures and the equal-label, equal-color 2+1 failure. They distinguish failure of a fixed completion method from failure of the theorem.

The C++ run was repeated under `-O3 -DNDEBUG` after the primary `-O2` run, with identical output. The Python support checks were repeated under normal, `-O`, and `-OO` execution, with identical output. These repetitions check reproducibility and optimization-independent guards; the symbolic proof does not depend on their success.

## 5. Acceptance limits and use

The exactly-five proof is self-contained apart from elementary finite matching/list-coloring facts that it proves directly. Its use of edge-criticality is controlled and explicit. Neither disconnected supports nor repeated exterior color names create an omitted case. The complementary symbolic arguments have also been checked, but its finite boundary counts are not being substituted for this proof.

The principal candidate may be used as written with its exact hypotheses and scope statements retained. No amendment or condition about a computational classification is necessary. Combining this acceptance with the earlier one-through-four acceptance gives the full stated at-most-five theorem in degree three.

This acceptance is of a restricted mathematical result. It is not acceptance of a resolution of the original conjecture, a historical-priority claim, a theorem for degree at least four, or the assertion that every arbitrary fixed boundary coloring extends.
