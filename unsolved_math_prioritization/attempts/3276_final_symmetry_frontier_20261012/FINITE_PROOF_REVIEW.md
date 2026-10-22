Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent proof review of the full twisted-rotation encoding

Queue row 1754, problem 3276. Fifth and final substantive pass, computational lane only. This audit is not an additional research pass.

## Exact object encoded

The vertex set is Z/nZ, where n is odd and divisible by three. A single global action sends each vertex x to x+1 and each color c to c+1 modulo three. The action must preserve every actual arc's orientation and color under this rule. Merely knowing the colors on one Hamilton cycle has period three does not imply this action on the remaining arcs.

Every unordered pair has a unique distance d in {1,...,(n-1)/2}, up to replacing d by n-d. The pairs {x,x+d}, as x varies, form its orbit. Such an orbit has n distinct pairs: a nontrivial stabilizer of an unordered pair would swap its endpoints, hence have order two on that pair; an odd-order cyclic action has no such stabilizer. Different distances in the displayed range produce disjoint orbits, together containing n(n-1)/2 pairs.

A distance orbit has exactly six possible assignments. States 0,1,2 assign x -> x+d color x+s modulo three. States 3,4,5 assign x+d -> x color x+(s modulo three) modulo three. The color base in the reverse case is still x; using the actual tail x+d would generally change the represented choice and conflict with the stated representative convention. A full n-step return is compatible because three divides n. Each representative orientation/color determines its entire orbit, and no second state vector produces the same labeled colored matrix.

Thus all state vectors enumerate precisely all tournaments with this specified full action. This is a labeled enumeration, not an isomorphism classification. There is no quotient by arbitrary rotations or color permutations whose orbit sizes would need compensating weights. The independent audit constructs the unordered-pair orbits directly from the group action rather than using the candidate's distance formula, and checks duplicate writes and every shifted arc.

## Distinguished cycle and normalization

In the fixed-cycle mode, the state for d=1 is fixed to zero. It supplies every actual cycle arc x -> x+1 with color x modulo three. This is justified for the intended hypothetical induced-minimal obstruction: its distinguished cycle fixes the vertex order, and a global color renaming makes the first arc color zero and its color action the displayed three-cycle. It is an extra named condition in the search mode, not silently claimed for an arbitrary already-labeled symmetric tournament.

The unrestricted-state mode retains all six choices at d=1. The raw and fixed-first counts are recorded separately. No universal division factor is assumed: at n=9 the triangle-only fixed count is 72 out of 432, whereas the predecessor-only fixed count is 18 out of 54. The predecessor condition itself forces the forward d=1 orientation; its three colors are equivalent by global renaming.

## Pruning soundness

A partial state specifies complete pair orbits. Consequently its actual-arc graph remains invariant under the full twisted shift. A directed cyclic rainbow triangle survives in every completion. Conversely, if any such triangle exists in the partial graph, shift one of its vertices to zero. The resulting cyclic triangle is still rainbow because a common color permutation preserves distinctness. It is therefore sound and complete for this partial predicate to inspect directed cyclic triples containing zero. A transitive rainbow triple is not forbidden.

For every color, the candidate starts a graph search at zero using only actual arcs of that color. Reaching n-1 is exactly a monochromatic directed path from zero to its predecessor. Shift invariance implies that this happens for one vertex if and only if some monochromatic predecessor path happens at every shifted vertex, with the path's color permuted. Testing zero suffices; testing the successor instead would be a different and incorrect condition. Arc additions cannot destroy an existing path, so rejecting such a partial state cannot remove a valid completion. The reachability search never mixes colors or treats a derived path as an actual triangle edge.

Only predecessor nonreachability is imposed. The additional induced-minimal requirement of reaching all other vertices is omitted, making the searched family a superset of the intended minimal obstructions. Its omission is safe for a zero conclusion. It cannot establish anything about relaxed positive models being induced-minimal counterexamples.

At each recursive call, the candidate tests every value of every remaining orbit and chooses an orbit with a smallest surviving domain. Empty domain rejects. Every value belonging to a real completion must survive the two monotone rejection predicates; branching over all surviving values preserves every such completion. The temporary assignment is reset after each tested domain and after each recursive branch family. Every recursion permanently assigns one further orbit until it returns. A leaf with no unassigned orbit is exactly a complete compatible tournament. The initial state is checked before recursion, which is essential at order three. Counters have explicit overflow guards.

The auditor's second complete search uses fixed numerical orbit order, literal triples on the whole graph, all-source/all-color reachability computed by repeated set unions, and direct group-action orbit generation. It does not call the candidate or its MRV recursion. Its node counters need not match the candidate's; its accepted-model counts must.

## Permitted conclusion and boundaries

A completed zero run at order n excludes the conjunction of the specified full twisted action, fixed distinguished first arc, no cyclic rainbow triangle, and predecessor nonreachability at that n. The audited exact orders are explicitly listed in the numerical report. This is no new general tournament bound, no result for arbitrary three-periodic obstruction-cycle words, and no all-order claim from finite samples.

Rainbow-free symmetric tournaments do exist. Independent literal enumeration at order nine produces 432, each with every vertex an outgoing universal monochromatic source. In particular, the zero result for the conjunction must not be paraphrased as absence of symmetric tournaments or absence of rainbow-free symmetric tournaments.

A separate structural proof lane may exclude symmetric induced-minimal counterexamples at every order. That theorem is not proved by these finite runs, and this audit does not certify it. Moreover, absence of symmetric induced-minimal counterexamples alone is not a hereditary argument settling all symmetric tournaments: a minimal induced counterexample inside a symmetric larger tournament need not inherit its symmetry. The unrestricted target remains unresolved by this packet.
