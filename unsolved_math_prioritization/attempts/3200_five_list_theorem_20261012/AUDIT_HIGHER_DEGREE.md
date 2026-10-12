# Independent audit: five exceptional lists in every degree at least four

Date: 12 October 2026 UTC.

## Verdict

**Accepted.** The frozen candidate proves the stated restricted theorem for every actual maximum degree Δ≥4. No mathematical correction is required. Its universal nonstar five-edge partial-coloring lemma is valid, including the cap-at-four reduction, every symbolic case, and the special incident-pair completion at Δ=4.

The proof is symbolic. Enumeration and full-graph coloring tests below are independent safeguards, not assumptions in the theorem. Acceptance does not extend to Δ=3, the unrestricted nonconstant-list conjecture, or any historical-priority claim.

The complete audited candidate is distributed as [HIGHER_DEGREE.md](HIGHER_DEGREE.md). The auditor read the complete candidate, both author checkers, their reported outputs and certificates, and the complete relevant first-round arguments and acceptance report. Source integrity was verified. Private original-input identities, hashes, sizes and coordination records are excluded from this prose edition.

## Exact accepted theorem

Let G be a finite simple graph with actual maximum degree Δ≥4. Assume:

1. G has no proper edge coloring with Δ colors.
2. For every edge e, G−e has a proper edge coloring with Δ colors.
3. Every list L(e) is a set of exactly Δ colors.
4. The assignment L is nonconstant.
5. There exists a Δ-element set A such that at most five edges e satisfy L(e)≠A.

Then G admits a proper edge coloring c with c(e)∈L(e) for every edge e.

The palette A need not be a specifically designated edge's list. The proof only uses the displayed common-palette condition. Isolated vertices do not affect the conclusion. The exceptional lists may have arbitrary overlaps and may be disjoint from A.

A consequence within Δ≥4 is that a hypothetical bad nonconstant assignment must differ from every Δ-element palette on at least six edges. In particular, it must differ from each Δ-set occurring as one of its lists on at least six edges. This is a necessary condition on a hypothetical counterexample, not evidence that one exists.

The new auxiliary statement is also accepted independently of criticality:

> If X is a set of five edges of a finite simple graph and the five edges do not all share one endpoint, assign each e∈X an arbitrary nonempty finite set O(e), and let d(e)=|O(e)|. There is a nonempty F⊆X that is properly colorable from O such that either the residual total ∑_{e∈X\F}d(e) is at most three, or X\F consists of two incident edges, both with d(e)=2.

## Hypotheses and inherited inputs

Set X={e:L(e)≠A}. Equal cardinalities give

|L(e)\A|=|A\L(e)|=d(e).

Consequently every exceptional edge has a nonempty exterior list O(e)=L(e)\A. Exact cardinality is doing mathematical work: it identifies the exterior-list size with the number of forbidden palette colors. Nonconstancy ensures X is nonempty. Constant lists are deliberately outside the theorem.

For each nonempty F⊆X, an ordinary Δ-edge-coloring of G−F exists: choose f∈F and restrict the given coloring of G−f. This remains valid if some ordinary labels are unused. No claim of ordinary Δ-edge-colorability is made when F is empty.

The at-most-four branch and the five-edge-star branch depend on the accepted first-round [four-exception theorem](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md) and [arbitrary-star proof](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md). The complete [first-round structural audit](../3200_critical_list_partials_20261012/AUDIT_NEAR_CONSTANT.md) records acceptance and statement qualifications.

The older candidate contained zero-exception wording needing the qualifications recorded in its accepted audit. The present theorem already states nonconstancy explicitly and does not reintroduce that defect.

For completeness, the star dependency was checked directly. In the bipartite incidence graph between exceptional edges and their exterior colors, take an inclusion-maximal matching of size r≥1. It properly exterior-colors r star edges with distinct colors. Every remaining exterior list is contained in those r matched colors, so every remaining allowed palette set has size at least Δ−r. The remaining t star edges have distinct ordinary labels and satisfy t≤Δ−r, since a star has at most Δ edges. Greedy distinct representatives on those t palette sets extend to a permutation of all Δ labels. This handles arbitrary list overlaps, including a maximal matching that is not maximum. A five-edge star is impossible when Δ=4, and is covered by this argument for Δ≥5.

The higher-degree four-exception proof was also rechecked. If at most one of four deficits exceeds one, deleting a maximum-deficit edge leaves three unit deficits. Two large deficits can be exterior-colored together. With three large deficits, either a 2,2,3 triple can be exterior-colored or two size-two exterior lists leave residual total three. With four large deficits, all-two lists use a nontriangle triple unless the support is a star; a mixed profile leaves a minimum deficit below Δ and colors a 2,2,3 triple; when the minimum equals Δ, all four exterior lists have at least four colors. Every branch has strict residual total below Δ or invokes the accepted star argument. No stronger statement is being silently assumed.

## Elementary facts and support structure

### Greedy bounds and short cycles

A noncomplete graph on four vertices is 2-degenerate: the full graph has a vertex of degree at most two and smaller induced subgraphs have maximum degree at most two. The corresponding noncomplete five-vertex graph is 3-degenerate. These yield universal list-colorability from lists of size at least three and four, respectively.

Three lists with lower bounds 2,2,3 admit distinct representatives: select different representatives from the first two and then avoid both in the third. A nontriangle on three vertices is a forest. It is two-list-colorable, and it is also colorable with bounds 1,2,2 in any placement: start at the singleton-list vertex in its tree component and continue away from it. This does not make an unsupported claim about a triangle with three two-element lists.

A triangle-free graph on at most four vertices is a forest or a four-cycle. The four-cycle proof correctly reduces to two-element lists. If the lists are not all identical, connectedness gives adjacent vertices with different lists; equal cardinality permits orienting the pair so the first has a color absent from the last. Starting with that color and traversing the cycle toward the last vertex removes the closing conflict. Identical lists are handled by alternation.

### Four-vertex 2,2,3,3 lemma

Let x,y be the lower-bound-two vertices and p,q the others.

If x and y are adjacent, any missing edge touches p or q. That endpoint has degree at most two and can be removed. The remaining lists have lower bounds 2,2,3 and admit distinct representatives. Restoring the removed vertex is safe from its at-least-three list.

If x and y are nonadjacent, reduce their lists to size two and the other two lists to size three. There are at least three unordered pairs that can be realized by distinct representatives on p,q. To verify the count, fix a∈L(p), yielding at least two pairs {a,b}; then choose a different a′∈L(p) and b′∈L(q)\{a,a′}, yielding a pair not containing a. At most two such pairs equal L(x) or L(y). Choose another pair. Neither x nor y is blocked even if each is adjacent to both p and q, and x,y may reuse a color because they are nonadjacent. The argument is valid for every placement of the lower bounds.

### Triangle transversal

The K4-free hypothesis is essential and correctly used. On at most five vertices, two disjoint triangles cannot occur. If two triangles intersect in exactly one vertex v, they use all five vertices and v is adjacent to the other four. A triangle avoiding v would make a K4 with v. Otherwise distinct triangles meet in edges. Given abc and abd, a triangle avoiding a must intersect each in two vertices, forcing it to be bcd, which again supplies K4 on a,b,c,d. Hence some vertex belongs to every triangle. Cases with no triangles or one triangle are immediate.

### Property (S)

Let H be the line graph induced by the five exceptional edges. In a simple graph, four pairwise incident edges share one endpoint. Starting with uv,uw, an edge avoiding u but meeting both must be vw; there is no fourth distinct edge meeting all three unless the supposed triangle description is abandoned. Thus four-cliques in H come from four-edge stars.

Once the five-edge-star case is excluded, H≠K5. If C is a four-clique, its four support edges share a center and the fifth edge z avoids that center. Its two endpoints can meet at most two distinct star leaves. Therefore z has at most two neighbors in C. This is precisely property (S); it is stronger than merely saying H is noncomplete. In particular, K5 minus one adjacency cannot occur as the line graph of a simple five-edge support.

## Complete audit of the universal partial-coloring lemma

### Cap-at-four reduction

Replace O(e) by an arbitrary subset of size a(e)=min(d(e),4). A proper coloring from these smaller lists also respects the originals. Under either asserted conclusion, no residual vertex can have a(e)=4: the strict alternative has residual sum at most three, and the other alternative has exactly two residual weights equal to two. Thus every residual edge satisfies d(e)=a(e). The reduction preserves the original residual total exactly; it is not merely a bound on truncated data.

This justification is uniform in arbitrarily large original exterior lists. It does not suppose that all original deficits are at most four, and it does not need an exhaustive search over large color universes.

Use the reduced weights for the following cases, and call a vertex large when its weight is at least two.

### Zero through three large vertices

- h=0: H≠K5 gives a nonadjacent pair. Its singleton lists can be used independently, leaving three unit weights.
- h=1: color a unit vertex first and then the large vertex, avoiding that color if needed. Three unit weights remain.
- h=2: the two large lists permit distinct colors if adjacent. Again three unit weights remain.
- h=3 with a weight at least three: the large triple has bounds 2,2,3 and can be colored, leaving two unit weights.
- h=3 with all three large weights two: there is a triple consisting of two large vertices and one unit vertex that is not a triangle. Otherwise every pair of large vertices would be adjacent, and both unit vertices would meet all three large vertices. The three large vertices plus one unit vertex form K4, with the other unit vertex adjacent to three members, contradicting (S). The chosen nontriangle has bounds 1,2,2. Coloring it leaves one weight two and one weight one.

The last branch does not accidentally rely on three common two-element lists coloring a triangle. Its unit-vertex escape is necessary to the stated construction.

### Four large vertices

These cases are exhaustive: either a weight two occurs together with a larger weight, all four weights equal two, or all four are at least three.

- In the mixed case, omit a weight-two large vertex. The other three large lists retain bounds 2,2,3. The residual weights are two and one.
- If all four weights equal two and their induced graph is not complete, select a nonadjacent pair and any third large vertex. The triple is a nontriangle, leaving weights two and one.
- If the all-two large graph is K4, the unit vertex z has at least two nonneighbors in that clique. Color z and two such clique vertices, using distinct colors on the clique pair. The remaining two clique vertices are incident and each has weight two. This is a genuine use of the second conclusion, not a strict-budget certificate.
- If all four large weights are at least three and their graph is not K4, 2-degeneracy colors all four, leaving only the unit vertex.
- If those vertices form K4 and some weight equals three, omit such a vertex. Color z first. Of the three selected clique vertices, at most two lose a color because of z, giving bounds 2,2,3. Distinct representatives color them and leave residual weight three.
- If all four clique weights equal four, color z and then the clique from remaining bounds 3,3,4,4. In that order the fourth choice has four options and sees at most three used colors; all four distinct colors can be selected. Nothing remains.

### Five large vertices, H K4-free

If every weight is at most three, choose a triangle-transversal vertex v. H−v is triangle-free on four vertices and is two-list-colorable, leaving weight at most three.

Otherwise let q be the number of weight-four vertices.

- q=1: omit a triangle-transversal vertex v of H−u, where u is the unique weight-four vertex. The remaining three vertices form a forest and have lists of size at least two. Color them and restore u, which avoids at most three colors. The omitted v has weight at most three.
- 2≤q≤4: omit any vertex of weight at most three. At most two remaining vertices have weight below four. Color those first, using distinct colors if they are adjacent; then each weight-four vertex sees at most three preceding colors. The sole residual weight is at most three.
- q=5: H≠K5 is 3-degenerate, so all five vertices can be colored from their four-element lists.

The q=1 branch uses the transversal lemma on four vertices, a permitted smaller order. The q=2 branch still works when the two smaller lists both have size two and their vertices are adjacent.

### Five large vertices, H contains K4

Fix such a clique C and let z be the fifth vertex. The alternatives s=0,1,2,3,4 count the weight-two vertices in C and exhaust the possibilities.

- s=0: if a clique weight equals three, omit it, color z first, and color the remaining clique triple using bounds 2,2,3. If all four clique weights equal four, color z first and then use 3,3,4,4. The residual sum is three or zero.
- s=1 or s=2: omit a weight-two clique vertex. The remaining four-vertex graph is noncomplete because z has at most two neighbors in C. Its lists dominate the bounds 2,2,3,3, so the four-vertex lemma applies. The residual weight is two.
- s=3: omit a weight-two neighbor of z if one exists; otherwise omit any weight-two clique vertex. Color the remaining clique triple with distinct representatives using 2,2,3. By (S), deleting a neighbor leaves at most one neighbor of z. If no weight-two neighbor existed, z could only meet the unique larger clique vertex anyway. Thus z can be restored from its at-least-two list. The residual weight is two.
- s=4: choose two clique vertices nonadjacent to z and color them distinctly, together with z. The two residual clique vertices are incident and both have weight two.

Every branch explicitly selects a nonempty exterior-colored set. Every weight-four vertex is selected, as also follows abstractly from the two allowable outcomes. This completes the symbolic proof, with no dependence on which colors overlap across lists.

## Completion at all Δ≥4

Fix a proper exterior coloring of the nonempty selected F and any ordinary Δ-edge-coloring φ of G−F. For a uniformly random permutation π of its labels onto A, the probability that an exceptional residual edge e violates its list is d(e)/Δ. Repeated ordinary labels and dependent events do not affect the union bound. If the residual sum is at most three, the union bound is strictly below one for every Δ≥4, giving a suitable permutation.

In the second outcome the residual sum is four, which is strictly below Δ when Δ≥5.

When Δ=4, the residual edges e,f are incident, so φ(e) and φ(f) are distinct labels. Each allowed palette set A∩L(e), A∩L(f) has exactly two elements. Choose one representative for the first and a different one for the second, which is possible because the second set has two elements. These assignments of two distinct labels to two distinct colors extend to a bijection between the four labels and A. There are no other residual exceptional edges. All other edges of G−F have the full list A.

The exterior part uses only colors outside A and the permuted ordinary part uses only A. Thus they cannot conflict across their boundary, even where edges from the two parts meet. Both parts are proper internally and all lists are respected.

The equality case is not asserted for two arbitrary nonincident edges with possibly identical ordinary labels. The incidence condition supplies exactly the distinct-label fact needed at Δ=4.

## Independent computational safeguards

A new audit program was written without importing or calling either author program. It uses explicit failure exceptions, not Python `assert`. The checking strategies were deliberately different:

1. **Support completeness by direct simple-graph generation.** Every simple graph with exactly five edges and no isolated vertices was generated on orders four through ten. Five edges have at most ten endpoints, so this covers every support after deleting irrelevant isolated vertices. The numbers of labeled graphs were 6, 222, 1,581, 4,410, 5,880, 3,780, and 945, totaling 16,824. Their line graphs give exactly 24 isomorphism types, including one K5 star type. The 23 other types satisfy (S). The support set and the minimum possible support maximum degrees agree with the author-generated data. This generation is independent of both the author's endpoint partitions and the second checker's clique partitions.
2. **Fresh profile certificates.** A forward subset dynamic program determines which vertex sets have a universal greedy order: a newly colored vertex must see fewer preceding neighbors than its guaranteed list size. A separate connected-component check recognizes forests and small even cycles. Every one of the 23×4⁵=23,552 profiles has a valid certificate: 23,538 strict greedy, 2 strict two-list, and 12 incident-pair certificates.
3. **Exact author-certificate validation.** Every author-generated record was independently checked for support, weight range, nonempty selected set, residual budget or incident pair, and complete unique coverage. For greedy certificates the author-recorded order itself was checked step by step, not merely replaced with another order that happened to work. Every two-list certificate was checked structurally. All 23,552 records pass.
4. **Greedy-only frontier.** The independent strict-greedy test fails in exactly the same fourteen profiles. Twelve belong to K4 plus a vertex having zero, one, or two clique neighbors, with the four clique weights two and the fifth weight one through four. The other two are the four-wheel with all rim weights two and hub weight two or three. The twelve are repaired by the incident-pair certificates; the other two by the even rim. None is labeled an uncolorable complete list assignment.
5. **Cap preservation.** Every profile with original weights in {1,…,8} on the 23 support types was checked against an independently found capped certificate: 753,664 cases. Every residual original weight equals its capped weight. This finite check corroborates the proof for all finite original weights, but does not replace that proof.
6. **Final palette step.** All 12 ordered pairs of distinct four-palette labels and all 6×6 ordered allowed-two-subset choices were tested against all 24 permutations: 432 cases. Each succeeds; the smallest number of successful permutations is four.
7. **Small-lemma finite tests.** All 958 labeled K4-free graphs on five vertices satisfy the transversal property. An independent exact list-coloring solver, followed by separate solution validation, passes 36,288 tests of the 2,2,3,3 lemma on all 63 noncomplete labeled four-vertex graphs using a four-color universe. It also passes 53,136 two-list placements on all triangle-free labeled four-vertex graphs. These are finite palette checks, not an enumeration of every arbitrary color universe.
8. **End-to-end critical-graph tests.** The exact solver verifies that K5 minus one edge has actual maximum degree four, is not four-edge-colorable, and becomes four-edge-colorable after each of its nine edge deletions. For every one of its 126 five-edge supports, every one of the 4⁵ deficit profiles, and two specified exterior/interior palette placements, the audit constructs an exterior coloring, obtains an ordinary coloring after deletion, finds a valid permutation, and independently validates the resulting full nine-edge list coloring. All 258,048 constructions pass. The two placements include heavily overlapping nested exterior lists and cyclically shifted lists; they are systematic samples, not arbitrary-list exhaustion. There are 372 distinct cached ordinary colorings.

Normal Python, `-O`, and `-OO` runs completed successfully and agree byte for byte in the audit checks. Programs and raw data remain private verification artifacts; the authored mathematical acceptance and aggregate metadata are sufficient to state the result.

## Explicit boundary and negative controls

The audit's independent decision routine verifies the following controls. They distinguish a valid restricted theorem from overstatements of the local method.

1. **The nonstar exclusion matters to the local lemma.** On H=K5 give all five vertices the same singleton exterior list. A proper exterior-colored subset has size at most one, so at least four unit weights remain. Neither lemma outcome is available. The theorem handles star supports by its separate star argument.
2. **Residual total four is genuinely needed in some local profiles.** Let H=K4 plus an isolated fifth vertex. Give all clique vertices the common exterior list {0,1} and the fifth vertex {0}. At most two clique vertices can be colored. Thus no proper exterior-colored subset leaves residual total at most three. Coloring the fifth vertex and two clique vertices succeeds and leaves an incident weight-two pair, exactly as claimed.
3. **Distinct ordinary labels matter at Δ=4.** Two residual edges having the same ordinary label and allowed sets {0,1} and {2,3} cannot be completed by any four-palette permutation. This is a fixed-method obstruction, not a counterexample to the theorem. Incidence excludes this repeated-label situation.
4. **The four-vertex lemma needs noncompleteness.** On K4, lists {0,1}, {0,1}, {0,1,2}, {0,1,2} cannot supply four distinct colors. Removing the noncomplete hypothesis would be false.
5. **The triangle-transversal lemma needs K4-freeness.** No vertex of K4 meets all four of its triangles; deleting any vertex leaves a triangle.
6. **A triangle is not universally two-list-colorable.** Three identical exterior lists {0,1} fail on K3. The forest and even-cycle arguments must not be replaced with a claim covering every small graph.
7. **Capping at three would not justify the same lifting argument.** On K4 plus an isolate, original weights (4,4,4,4,1) become (3,3,3,3,1) under a cap of three. A colorable subset consisting of three clique vertices and the isolate leaves capped weight three but original weight four. Capping at four avoids precisely this unselected-large-weight defect.
8. **A forbidden structural graph is rejected.** K5 minus one adjacency is absent from the independently generated simple-support line graphs, agreeing with (S).
9. **Nonconstancy is necessary already at degree four.** The independently verified critical fixture K5 minus one edge has no coloring when every list is the same four-set.
10. **Exact list cardinality cannot be discarded.** On that fixture, shrink one common four-set to a three-subset and leave the others unchanged. The assignment is nonconstant but still uses only four colors and remains uncolorable.
11. **Criticality cannot be discarded.** Add a disjoint edge to that degree-four fixture, keep the same common four-set on the core, and give only the new edge the list {0,1,2,4}. This is a nonconstant exact-four-list assignment with one exception and remains uncolorable. Deleting the new edge leaves the obstructed core, so the required criticality hypothesis fails.

## Acceptance boundary

This audit accepts the exact Δ≥4 theorem and the universal five-edge lemma stated above, together with their symbolic proofs and the expressly identified prior inputs. It imposes no new mathematical qualification on the candidate. Presentations should preserve finite simplicity, actual maximum degree, both criticality conditions, exact list cardinality, nonconstancy, the nonempty exterior set, and the incident-pair qualification at Δ=4.

The candidate is a new five-edge argument supported by previously accepted four-exception and star arguments; a standalone presentation of the whole theorem should include those dependencies or state them clearly. This audit does not treat external problem pages as proofs of the new result, does not establish historical priority, and makes no claim about a separate Δ=3 packet.
