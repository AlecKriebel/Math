# Independent full review of 3242 / OPG-46575

**Verdict: PASS_SCOPED_PARTIALS. No mandatory mathematical correction. Original question remains unsolved5/5.**

Reviewed freeze: FINAL_AUTHOR_MANIFEST.json SHA2564b2241d609dce3e070c6d87d10635141628401263fa662b01d5ac3aaceb02fdd. The29 bound public files all match byte-for-byte, and all five author scripts reproduce their frozen JSON receipts exactly. The preserved first two-turn checkpoint manifest also matches. This is an independent AI mathematical/source audit, not human peer review or a historical-priority certification.

## Source and exact target

I read the complete live [Open Problem Garden source](https://www.openproblemgarden.org/op/melnikovs_valency_variety_problem) and independently inspected the downloaded formula image. The question uses a strict comparison, with an outer ceiling and an inner floor: chi(G)>ceil(floor(w(G)/2)/(n-w(G))). The intended finite simple loopless graph setting, n>=2, is consistent with the official Vizing1968 conventions. The image and prose agree.

The conversion to n-1<=(2chi(G)-1)(n-w(G)) is exact. The denominator is positive because degree0 and degree n-1 cannot both occur in a simple graph. The source's older formula-image retrieval limitations are preserved; the readable live OPG target is not replaced by an invented historical correction. The antiregular recursion agrees with Levit--Mandrescu2010, Theorems1.4--1.5; that classification is explicitly credited. Limited fresh searches found no decisive later source resolution, which is not a proof of openness or novelty.

## Mathematical audit

### Turn1: capacity and bipartite result

The sorted color-class capacity count correctly places every degree exceeding N-a_i in the earlier, smaller color classes. Positive degrees are essential and the no-isolate hypothesis is used at exactly that point. The induction gives the weaker exponential coefficient. Isolate removal correctly changes the degree variety by one, without changing chromatic number for a graph with an edge. The edgeless boundary is exact. For chi<=2 the exponential and desired linear coefficients coincide. The geometric class-size examples are marked non-graph relaxations; their failure is not misreported as a source counterexample.

### Turn2: independent-set cut lower bound

The exact cut identity cancels crossing edges. The signed representative minimum is correct when W>=S: choose all S negative weights and then the smallest W-S positive weights. Each of the D nonrepresentatives contributes at least-S, including repeated high degrees whose true contribution is positive. The quadratic specialization and the two excluded parameter shapes have the stated arithmetic. The surviving(2,4,6) relaxation is not asserted realizable. The deficit-one isolate-free slice follows from the complete sorted partition argument and does not silently restore isolates at this stage.

### Turn3: split graphs and graph operations

A maximum clique can be chosen as the clique part of a split partition, and coloring the independent part using missed clique colors proves chi equals clique size. The degree count W<=2k-1 is valid for the isolate-free core. In the critical D1,N2k case, equality forces disjoint degree-value ranges and the cut totals differ by exactly one; repeated-degree placement has not been ignored. Both disjoint-union and complete-join arguments preserve the stronger core property. The two-singleton join case is handled separately rather than dividing by a zero deficit. The result is for the stated composition-generated class, not a decomposition of arbitrary graphs.

### Turn4: local neighborhoods and classical deficit one

The maximum-degree neighborhood bound does not require outside vertices to be independent. Positivity gives Delta>=W and T<=D; the capacity iteration with T outside vertices yields the claimed power-of-two coefficient. The sufficient condition chi>=2^h is used exactly, leaving the chi3/h2 case open. Triangle-free neighborhoods are independent even when the graph is not bipartite, so the full triangle-free class is correctly covered. The antiregular endpoint deletion proof has unique isolated/universal vertices for n>=3, proper n2 bases, and the stated chromatic recurrences. Its classical credit is retained.

### Turn5: forced-neighbor three-color/deficit-two theorem

The six triples exhaust the sorted positive color-class sizes for D2,N>=11 under Turn1. Every class then has at least two vertices, so all degrees are at most N-2; having N-2 distinct positive degrees forces the exact interval1,...,N-2. Both quadratic exclusions are correct.

For(2,4,c), the two largest required degrees must occupy the size-two class. Their saturation forces the unique missed vertex to represent degree1. A required maximal-degree B vertex is saturated to C, forcing the degree1 and degree2 representatives into B. At most two B vertices can then meet C, so C degrees are at most4. Only one remaining B vertex cannot represent both degree5 and degree6. Every distinctness assertion used here follows from different required degree values.

For(2,3,6), both cases concerning a saturated degree8 B vertex are exhaustive. In the saturated case, the five required A-union-B degree values occupy all five vertices, and either location of the low vertex leaves C degrees at most4. In the nonsaturated case A has degrees8,9; the location of its single missing neighbor leads either directly to the same cap or forces the final B vertex to have degree2. The required degree5 is unavailable in every case. These are deductions from actual adjacency, not feasibility claims about a numerical relaxation.

Isolate restoration has exactly r1 or r2 since the core deficit is3-r>=1. The r2 case correctly uses the stronger isolate-free antiregular bound. The resulting chi3,d2 source slice is valid. Finally, the order<=15 corollary follows by splitting chi<=2, d1, chi3/d2, chi3/d>=3, and chi>=4/d>=2. It is not a graph scan through15. The n16,chi4,d2 residual is a parameter possibility, not a constructed graph.

## Independent controls

The independent script uses standard-library subset-partition dynamic programming for exact chromatic numbers; it imports no author helper. It checks all labeled graphs through6, all threshold-construction strings at orders7--9, and96 fixed-seed graphs at each of those latter orders. It independently tests source rounding, class capacity, cut identities/bounds, split and triangle-free core properties, antiregular chromatic values, neighborhood bounds, and union/join identities. All908224 assertions pass.

A second independent script builds12607 canonical actual graph completions after the stated forced-neighbor reductions. These include all remaining free edges in both saturated-B cases and the reduced nonsaturated cases. None has the forbidden degree variety. These are finite proof controls, not exhaustive enumeration of all graphs above6. The general class and small-order theorems rest on the written arguments audited above.

The five author receipts replay exactly:271471,532144,58870,83011,231 assertions. Repeated algebraic checks are not independent theorems. Source-file hashes match their recorded manifests, including the readable OPG formula and credited antiregular input.

## Disposition and publication limits

The scoped partial packet may be published as an unresolved five-turn research result after the parent gate. It must retain the original unsolved status, finite-diagnostic limits, classical antiregular credit, historical-source access qualifications, and absence of a novelty claim. No original full solution or counterexample is established. This review does not authorize a merge, release, outside contact, or further author research turn.
