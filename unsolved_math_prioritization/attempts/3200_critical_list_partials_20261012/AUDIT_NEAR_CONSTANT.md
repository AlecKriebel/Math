# Independent audit of near-constant edge-list-coloring results

Date: 12 October 2026 UTC. Target: row 1751, problem 3200, the nonconstant-list conjecture for finite simple edge-critical graphs.

## Verdict and scope

The corrected mathematical packet is accepted as a collection of restricted theorems. The accepted structural text requires the two explicit nonconstant-assignment qualifications in STATEMENT_CLARIFICATIONS.md; the proofs themselves already have the required nonempty exceptional set. The additional-cases proof and the four-exception proof have no mathematical gap found in this audit.

The accepted conclusions are:

- An exact Hall condition for completing a specified exterior coloring by a single permutation of a specified ordinary coloring.
- Arbitrary exceptional lists on a nonempty star, or on a pairwise-incident edge family of size at most the maximum degree.
- A strict residual-deficit sufficient condition, including a largest-single-deficit corollary.
- The full maximum-degree-two case, including the reduction to one odd cycle apart from isolated vertices.
- Arbitrary exceptional lists that become a matching after deleting one exceptional edge.
- At most four arbitrary exceptions, provided the assignment is nonconstant.
- At most Δ+1 one-color substitutions, provided at least one list changes.

These results do not resolve the unrestricted conjecture and are not claimed novel. A failed palette-permutation attempt is not a counterexample to the conjecture. Finite checks below corroborate the arguments but are not substitutes for their general proofs.

The independent auditor read the complete structural proof, additional cases, four-exception proof, and required statement clarifications. This edition incorporates both corrections in NEAR_CONSTANT.md and retains their explanation in STATEMENT_CLARIFICATIONS.md. The acceptance is of the corrected statements, never of a zero-exception corollary.

## Exact hypotheses and low-degree boundaries

Let G be finite and simple, let Δ be its actual maximum degree, assume G has no proper edge coloring with Δ colors, and assume G−e has such a coloring for every edge e. Lists are finite sets, each of cardinality exactly Δ. Fix any Δ-element palette A. An exceptional edge is one whose list differs from A; write X for all such edges, O(e)=L(e)\A, and d(e)=|O(e)|.

The identity d(e)=|A\L(e)| uses equality of the two list cardinalities. For each e in X it also proves d(e)≥1, so an exceptional edge has an available exterior color. This is not an innocuous assumption that can be silently removed. A negative control below shows how an undersized nonconstant assignment can fail even on a triangle.

The hypotheses have no example with Δ=0 or Δ=1: an edgeless graph has its empty coloring and a graph of maximum degree one is a matching together with isolated vertices. Thus divisions by Δ and the later Δ≥2 case split never involve a genuine degree-zero instance.

There is exactly one component containing edges. Indeed, some component must fail Δ-edge-colorability, since colorings of all components with the same Δ labels would combine into a coloring of G. If any edge lay outside that component, deleting it would leave the noncolorable component and violate criticality. Isolated vertices are unrestricted and do not affect lists, edge colorings, or nonconstancy. All references to a connected critical graph should be understood with this harmless isolated-vertex qualification.

For every nonempty edge set F, a proper Δ-edge-coloring of G−F exists: choose f in F, take the promised coloring of G−f, and restrict it. No stronger deletion theorem is needed. If F is all of E(G), the restriction is simply the empty coloring. Conversely, F must not be allowed to be empty as a universal construction, because G itself has no such ordinary coloring.

## Palette permutation and Hall audit

Suppose nonempty F has a proper coloring ψ using O(f) at every f. The existence of ψ already implies F⊆X. Fix any proper ordinary coloring φ of G−F with labels 1 through Δ, allowing unused labels. For each label i intersect A with the lists of exceptional edges of label i, obtaining B_i; if there are none, set B_i=A.

For a bijection π from the labels to A, the recolored edge e of G−F respects its list exactly when π(φ(e)) lies in L(e). Common-list edges impose no additional constraint. Therefore π works exactly when π(i)∈B_i for every i. A system of distinct representatives for all Δ sets is precisely such a bijection, because both sides have cardinality Δ. Unused ordinary labels have B_i=A and create no spurious obstruction: any injective assignment on used labels extends across the unused ones.

The finite Hall inequalities are thus necessary and sufficient for this fixed completion method. They are only sufficient for list-colorability of G, since another ordinary coloring, another exterior set, different exterior colors, or a coloring not of this two-palette form may succeed.

The palettes A and its complement are disjoint. That fact, not any lack of adjacency between F and G−F, removes all cross-part conflicts. The exterior coloring must itself be proper. No argument here assumes that arbitrary choices of exterior colors on incident edges are proper.

## Star and pairwise-incident support audit

The auxiliary bipartite graph has exceptional edges on the left and exterior colors on the right. A maximal matching is sufficient. After choosing it, an unmatched exceptional edge has no unmatched exterior-color neighbor: such an edge of the bipartite graph could otherwise be added to the matching. This is exactly the maximality property needed; an augmenting-path or maximum-cardinality argument is unnecessary.

Let r be the number of matched exceptional edges. Because X is nonempty and every exterior list is nonempty, r≥1. The matched exterior colors are distinct, so they properly color F even when every edge in F meets every other. Every unmatched exceptional edge has at most r exterior colors, hence at least Δ−r colors in A.

In a star, or any pairwise-incident family, the t remaining exceptional edges receive distinct ordinary labels. Since |X|≤Δ, t≤Δ−r. Any t sets each of size at least t have distinct representatives, by greedy selection or Hall. The selected representatives therefore give compatible, distinct images of these t ordinary labels, and extending to a permutation of all labels completes the coloring. The boundary t=0 is harmless.

Simplicity is used in the star-or-triangle classification. If two incident edges are uv and uw, an edge meeting both but not through u must be vw. A further distinct edge meeting all three is already a triangle edge. Thus a pairwise-incident family is a star or has at most the three edges of a triangle. A triangle fits |X|≤Δ when Δ≥3. The Δ=2 triangle belongs to the separately proved odd-cycle case.

A concrete maximal-but-not-maximum auxiliary matching is checked below. It shows that replacing maximal by maximum is unnecessary, while dropping maximality altogether would invalidate the bound on the unmatched exterior lists.

## Residual deficit audit

For a uniformly random permutation π of the Δ ordinary labels onto A, the image of a fixed label is uniform on A. Thus the bad-list event for a remaining exceptional edge e has probability |A\L(e)|/Δ=d(e)/Δ. The ordinary labels of different edges may coincide, and their bad events need not be independent. The union bound uses only the individual probabilities, so the proof remains valid with arbitrary dependence and arbitrary exceptional-edge positions.

If the sum of the residual deficits is strictly less than Δ, the probability of at least one violation is strictly less than one. Some permutation respects every remaining list. Combining it with the proper exterior coloring establishes the theorem.

Choosing a single edge of maximum deficit is legitimate because X must be nonempty and every exceptional edge has an exterior color. The resulting sufficient condition is Σ_X d(e)−max_X d(e)<Δ. In particular r genuinely changed one-color-substitution lists give r−1<Δ whenever 1≤r≤Δ.

This last lower bound is essential wording. The original candidate also states an at-most-two-exceptions corollary without explicitly saying nonconstant. Taken alone, both original sentences would include zero changes, which is false. The frozen clarification file correctly adds the missing qualification to the first and changes the substitution range to between one and Δ. No proof for a positive number of exceptions is altered.

## Odd-cycle and matching-plus-one audit

For Δ=2, each edge-containing component is a path or cycle. Paths and even cycles have a proper two-edge-coloring. A noncolorable graph therefore has an odd-cycle component. Criticality forbids every edge outside that component, proving the reduction to a single odd cycle plus isolates without assuming connectedness in advance.

For a nonconstant two-list assignment around that cycle, some adjacent pair of lists differs. Equal cardinalities give a color in the first list and not in the preceding last list. Start with this color and greedily proceed around the cycle. Each edge has two choices and must avoid just its predecessor. The final edge cannot use the initial color because its own list excludes it, so the closing adjacency is automatically proper. This proof is independent of any earlier screening calculation. It also makes clear why list nonconstancy matters: a common pair of colors fails on an odd cycle.

For the matching-plus-one theorem, write X=M∪{f} with M a matching. If M is empty, use an exterior color on f and color G−f from A. Otherwise color M from its exterior lists; arbitrary choices are proper because its edges are disjoint.

If L(f) meets A, choose an ordinary coloring of G−M, which exists by restricting a coloring of G−m for some m in M. One global permutation can send the label of f to any prescribed color of L(f)∩A. Every other edge outside M has list A. The exterior palette on M prevents cross-conflicts even where f meets M.

If L(f) is disjoint from A, it has Δ exterior colors, not merely one. An edge meets at most two edges of a matching, including the case of one at each endpoint. Hence at most two used colors are forbidden on f. For Δ≥3 at least one color remains. All of X is then properly exterior-colored, and G−X can be colored from A. The nonempty-deletion justification applies because f∈X.

The Δ≥3 restriction is necessary for this particular fixed-exterior extension argument, though not for the full degree-two conclusion. A degree-two control below blocks a chosen pair of exterior colors at both endpoints while the entire assignment remains colorable by the odd-cycle argument.

The three-exception corollary correctly includes nonconstancy. If three exceptional edges contain a disjoint pair, that pair is M and the third is f. Otherwise the family is pairwise incident and is a star or triangle. Fewer exceptions follow by the same arguments. No case is omitted.

## Four-exception supplement audit

The supplement's auxiliary facts are sufficient and elementary. Three lists of sizes at least 2,2,3 have distinct representatives. The adjacency graph on three selected edges is a forest whenever they are not pairwise incident, so two-element exterior lists suffice there. A graph on four vertices other than K4 is 2-degenerate and is colorable from lists of size at least three. Four pairwise-incident edges of a simple graph form a star; in a subcubic graph this cannot occur.

For Δ=3, let h count deficits at least two among the four exceptional edges. The exceptional line graph is not K4.

- For h=0, a disjoint pair can be exterior-colored and the other two deficits sum to two.
- For h=1, the large list avoids the already chosen color of one small list, leaving two unit deficits.
- For h=2, the two large lists admit distinct colors if their edges meet, again leaving deficit two.
- For h=3, a deficit-three edge among the large triple gives list sizes at least 2,2,3. If all three deficits are two and their edges are not pairwise incident, their adjacency graph is a forest. Both alternatives leave deficit one.
- In the remaining h=3 branch, the three large edges are pairwise incident and the fourth edge a is disjoint from a large edge b. Choose a third large edge c distinct from b. Color a, then c avoiding a when necessary, then b avoiding c. Since b is disjoint from a, its two exterior colors suffice. The uncolored fourth edge has deficit two. This is the case in which merely choosing the large triple would have been invalid; the supplement handles it explicitly.
- For h=4 with all deficits two, choose a disjoint pair and one more edge; the selected triple is not a triangle. In the mixed two/three case, leave a deficit-two edge and color a 2,2,3 triple. If all deficits are three, color the entire non-K4 exceptional line graph from its three-element lists. Each residual sum is strictly below three.

For Δ≥4, the residual-deficit arithmetic is also correct. With h≤1, deleting a maximum-deficit edge leaves three unit deficits. With h=2 the two large edges leave residual two. With h=3, either a 2,2,3 triple can be colored leaving one, or two deficit-two edges can be colored leaving three. These are all strictly below Δ.

With h=4 and all deficits two, a pairwise-incident family is a star of size four and falls under the already proved star theorem; otherwise a nontriangle triple leaves deficit two. If some deficit is at least three and the minimum deficit is below Δ, leave a minimum-deficit edge. At least one edge remaining in the triple still has deficit at least three: if the minimum is two, deleting a minimum-deficit edge cannot remove an edge of deficit at least three; if the minimum is at least three, every remaining edge qualifies. The triple has sizes at least 2,2,3 and the residual minimum is strictly below Δ. If the minimum equals Δ, all four lists are fully exterior with at least four colors, so greedily assigning four distinct colors works.

Every branch either invokes a proved star theorem or supplies a nonempty properly exterior-colored F with residual sum less than Δ. Thus the four-exception theorem is established, including arbitrary list deficits and positions.

For Δ+1 one-color substitutions with Δ≥3, a pairwise-incident exceptional family could have at most Δ edges in a star or three in a triangle. Since Δ+1 exceeds both bounds, a disjoint pair exists. Exterior-color it and leave Δ−1 unit deficits. The strict deficit theorem applies. The Δ=2 case already follows from the complete odd-cycle proof, and Δ≤1 is vacuous. The assertion remains restricted to a nonconstant assignment.

## Independent finite verification

The audit code was written independently without importing the author's code or results. It uses an exact backtracking list-edge-coloring solver, separately validates every returned coloring, constructs the claimed exterior completions, and directly compares Hall inequalities with enumeration of label permutations. Checks use explicit failure exceptions rather than removable language assertions.

The base run and an optimization-mode repeat agreed. The following are finite coverage statements, not universal conclusions:

- All 1,100 labeled simple graphs on zero through five vertices were tested for the exact criticality definition. The critical cases were one triangle at order three; four triangles with an isolate at order four; and at order five 22 degree-two cases, 30 degree-three cases, and 10 degree-four cases. Every degree-two case has the asserted odd-cycle edge component, and none has maximum degree below two or a second edge component.
- All two-element-list assignments from four colors were checked on C3, C5 and C7: 216, 7,776 and 279,936 assignments respectively. Exactly six constant assignments failed on each graph; all nonconstant assignments were colored both by the fresh greedy construction and by the independent decision solver.
- On K4 with one edge subdivided once, all 16,384 assignments of three-element lists from four colors were decided. Exactly the four constant assignments failed.
- On that degree-three fixture, all 27,279 assignments with one, two or three arbitrary exceptional lists from a five-color universe were constructed successfully.
- On K5 minus one edge, all 237,678 assignments with one, two or three arbitrary exceptional lists from a six-color universe were constructed successfully. All 561,480 assignments changing one color on between one and four edges, using either of two exterior colors, also passed.
- Petersen minus a vertex was independently verified to satisfy the criticality hypothesis. Every one of its 727 supports of size at most five that is a matching plus one edge was exercised by systematic exterior-list placements. In total 23,940 choices of the distinguished exceptional edge and list placements passed, including lists disjoint from A.
- The base constructions made 1,090,577 comparisons of Hall's condition with explicit permutations, with complete agreement. Separately, every family of Δ subsets of a Δ-set was tested for 1≤Δ≤4: 66,066 families, again with complete agreement.

The four-exception supplement received additional independent checks:

- All 2,420,208 choices of four nonempty exterior lists of sizes at most three from a four-color exterior universe, on every one of the 63 noncomplete labeled graphs on four vertices, passed the proposed Δ=3 exterior-set case split. This includes graphs that need not be line graphs, giving a superset of the required local adjacency cases.
- For Δ=4 through 8, every four-position deficit pattern and all 64 labeled four-vertex adjacency graphs were checked using two deterministic palette placements: 1,110,272 cases. The ten all-deficit-two complete-graph cases were correctly routed to the already proved star theorem; they were not reported as exterior-deficit certificates.
- On the degree-three subdivided-K4 fixture, every choice of four exceptional edges and every assignment of exceptional three-element lists from six colors was completed: 4,561,235 assignments. This includes completely exterior lists and every branch of the degree-three proof.
- On the degree-four K5-minus-an-edge fixture, all 4,128,768 one-color-substitution assignments on exactly Δ+1=5 exceptional edges, using either of two exterior colors, were completed by the disjoint-pair construction.
- These full-graph supplement checks contributed 8,690,003 additional exact Hall-versus-permutation comparisons. Branch counters confirm that every case in the four-exception proof, including its degree-three triangle-escape case and its higher-degree star fallback, was exercised.

Higher-degree palette placements were systematic finite tests, not an exhaustive enumeration of arbitrary exterior color universes. Complete-graph star fallback relies on the separately audited star theorem, rather than on a fabricated residual-deficit certificate.

## Explicit boundary and negative controls

The following small instances were constructed and checked independently. Edges of C_m below are listed cyclically as e0 through e(m−1).

1. **Zero changes fail.** C3 with every list {0,1} is uncolorable. This rejects the unqualified zero-exception interpretation of both original corollary sentences and explains why the clarification must accompany them.
2. **Exact list cardinality matters.** C3 with lists {0}, {0,1}, {0,1} is nonconstant but uncolorable. It has an undersized first list and is outside the theorem.
3. **Criticality matters.** Take C3 together with a disjoint single edge. Give the triangle the common list {0,1} and the extra edge {0,2}. The whole assignment is nonconstant and has only one exception, but the triangle remains uncolorable. Deleting the extra edge shows precisely why this graph is not edge-critical.
4. **Exterior propriety matters.** On C3, lists {0,2}, {1,2}, {0,1} give the first two incident edges the same unique exterior color 2. Coloring both with 2 is improper. The full assignment is nevertheless colorable, for example with colors 0,2,1 around the triangle. The matching-only argument must not be extended to arbitrary incident edges without an additional argument.
5. **Nonempty allowed sets do not replace Hall.** B1={0}, B2={0}, B3={1,2} are all nonempty but have no distinct representatives; the first two sets already violate Hall.
6. **The strict bound can fail at equality for a fixed method.** On C5 take A={0,1}, lists ({0,3},{1,2},{0,1},{0,2},{0,1}), F={e0}, and exterior color ψ(e0)=3. Give e1,e2,e3,e4 ordinary labels 0,1,0,1. The two remaining exceptional edges each have deficit one, summing to Δ=2, but their common ordinary label must map simultaneously into {1} and {0}. Its allowed set is empty, so neither permutation works. The assignment is colorable: colors 0,1,0,2,1 around C5 form a proper full coloring. This realizes the method boundary inside the exact critical-graph setting; it makes no separate existence assertion for every fixed Δ.
7. **The bad events can be dependent.** In the preceding fixed-coloring example, the two bad events each have probability 1/2 and are mutually exclusive with union probability one. An independence calculation would wrongly give union probability 3/4. The valid union bound gives one, correctly withholding the strict guarantee.
8. **Maximal need not mean maximum.** In K4 with edge 01 subdivided by vertex 4, use A={0,1,2} and put exceptional lists {0,3,4}, {0,1,3}, {1,2,3} on the star edges 02,03,04. Greedily matching 02 to exterior color 3 leaves a maximal auxiliary matching of size one; a matching of size two exists by assigning 02 color 4 and 03 color 3. The size-one construction still passes the star proof, and its resulting complete coloring was validated.
9. **Degree two can block a fixed exterior extension.** On C5 use A={0,1}, lists ({2,3},{0,2},{0,1},{0,1},{1,3}). Edges e1 and e4 are a matching; precoloring them 2 and 3 blocks both available colors at e0. This demonstrates why the disjoint-from-A matching-plus-one branch uses Δ≥3. The full assignment is still colorable, with cyclic colors 2,0,1,0,1.
10. **Both endpoints were exercised at degree three.** In Petersen minus a vertex, choose f=12 and matching edges 23 and 16, with outside colors 3 and 4 respectively. Give f the fully exterior list {3,4,5}. The construction chooses 5 for f and successfully completes the coloring, testing the sharp two-forbidden-colors step rather than just a one-neighbor case.

## Source inspection and interpretation

The operational hypotheses and intended direction were directly checked against the [Open Problem Garden entry](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs), posted 12 June 2007. It states the nonconstant-list formulation and defines criticality using non-Δ-edge-colorability together with Δ-edge-colorability after every edge deletion.

[Mohar's July 2001 problem page](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html) was also directly inspected. Its displayed equivalence has the direction reversed: equal Δ-lists cannot color a graph assumed not Δ-edge-colorable. That wording discrepancy is not a mathematical counterexample to the intended problem and is not used as one here.

Kaul and Mudrock's [2018 paper, version 2](https://arxiv.org/pdf/1805.02147v2), *Criticality, The List Color Function, and List Coloring the Cartesian Product of Graphs*, was inspected at Conjecture 6 on PDF and printed page 11, together with its definitions. It supplies context for the line-graph formulation, not a proof of the present partial results. Its compressed edge-criticality sentence does not literally repeat the lower chromatic-index bound; the present explicit non-Δ-edge-colorability hypothesis must not be dropped on that basis. The clarification file records this qualification.

The accepted mathematical statements and their proofs can be understood from the distributed authored prose and cited public theorems. The computational checks are reported with explicit finite coverage; their undistributed raw collections are not reproduced by this text. The audit establishes neither historical priority nor the current literature status of the unrestricted problem.

## Acceptance conditions and remaining limits

The nonconstant-assignment corrections are incorporated in NEAR_CONSTANT.md and must be preserved in any quotation or reuse. Preserve the fixed-method qualification on Hall necessity and on the equality-case obstruction. Preserve finite simplicity, exact list size Δ, the full criticality hypotheses, and every nonempty-exterior-set requirement.

Under these conditions, the strongest accepted universal lower bound on exceptional support says that any hypothetical bad nonconstant assignment differs from every Δ-set occurring as one of its lists on at least five edges. The structural matching, matching-plus-one, star, triangle and residual-deficit exclusions also remain valid. None of these necessary conditions constructs a bad assignment or settles the unrestricted problem.
