# Proportional bipartite factors: a regular-core theorem and two obstructions

## Status and exact question

**Restricted theorem accepted without mathematical correction; the unrestricted target remains unresolved by this work.**

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete general mathematical proofs are retained, including the integer-circulation argument, multiplicity-aware core structure, alternating-path proof of the matching decomposition, tree propagation, and boundary-preserving rational-cell lemma. This is not a computational reproduction package. Explicit finite witness lists, edge and coordinate packages, indexed constraint rows, matrix certificates, raw certificates, and executable code are omitted. The two finite obstructions retain their authored logical arguments conditional on explicitly stated, historically checked finite premises; this edition does not independently reconstruct those omitted premises. Neither obstruction is used to prove the regular-core theorem.

The candidate's unretained full generated stream hash is authenticated author-reported metadata only. The independent audit constructed and checked its own valid partitions; it did not recreate the candidate stream and does not claim byte-identical reproduction.

The unrestricted same-partition proportional-factor target remains unresolved by this work. No novelty, priority, exhaustive later-literature survey, or certification of current global problem status is claimed.

The target asks whether every finite bipartite graph, positive integer k, and positive **real** vector c = (c_1,...,c_k) with sum 1 admits a partition of the **same** edge set into E_1,...,E_k satisfying

    floor(c_i d_G(v)) <= d_{E_i}(v) <= ceil(c_i d_G(v))

for every vertex v and every color i simultaneously. Rounded choices are not prescribed. All positive results below also allow parallel edges; loops are excluded. Vertices of degree zero cause no difficulty. For k = 1 all edges receive the sole color.

### Theorem

The target holds for every finite bipartite multigraph G such that the nonempty 2-core of each connected component is regular. The regular degree may differ between components. In particular, it holds for:

- every forest;
- every bipartite pseudoforest (at most one cycle per connected component, counting a parallel pair as a cycle);
- any disjoint union of regular bipartite multigraphs with arbitrary finite trees attached at their vertices.

The theorem permits arbitrary unequal positive real fractions and unbounded degrees. It is not inferred from enumeration. A complete construction and proof follow.

Two further exact results explain why tempting general arguments fail:

1. A legitimate first proportional factor can be impossible to complete, even on a ten-vertex tree.
2. The natural joint-color linear program has a fractional vertex and a determinant-2 constraint minor even on a six-cycle with three equal fractions.

Neither obstruction is a counterexample to the target. Both underlying graphs have valid full partitions.

## 1. Finite monotone quota sequences

**Lemma 1.** Let c_i > 0 sum to 1 and let D be a nonnegative integer. There is a word w_1,...,w_D over colors 1,...,k such that its prefix counts

    q_i(t) = |{s <= t : w_s = i}|

satisfy floor(c_i t) <= q_i(t) <= ceil(c_i t) for every 0 <= t <= D and every i. Consequently q_i(t) is nondecreasing in t and sum_i q_i(t) = t.

**Proof.** The case D = 0 is empty. For D > 0 construct a directed network with source s, sink z, slot nodes p_t, and color nodes a_{i,t}, for 1 <= t <= D. Give the following arcs integer lower and upper bounds:

- s -> p_t has bounds [1,1].
- p_t -> a_{i,t} has bounds [0,1].
- a_{i,t} -> a_{i,t+1}, for t < D, has bounds [floor(c_i t), ceil(c_i t)].
- a_{i,D} -> z has bounds [floor(c_i D), ceil(c_i D)].
- z -> s has bounds [D,D].

A real feasible circulation sends c_i on p_t -> a_{i,t}, c_i t on each corresponding outgoing color-chain arc, 1 on s -> p_t, and D on z -> s. Thus the integer-bounded network has a feasible circulation.

For completeness, integer feasibility follows by the usual lower-bound reduction. Subtract every lower bound from its arc; each node then has an integer imbalance. Add a super-source and super-sink with integer capacities encoding these imbalances. The real feasible circulation supplies a flow saturating all super-source arcs. Starting from zero, a residual-path maximum-flow algorithm uses only integral augmentations, each increasing the flow by at least one, and terminates because the total super-source capacity is a finite integer. If it could not saturate that capacity, the vertices reachable in its residual graph would give a cut smaller than the real feasible flow, a contradiction. Restoring lower bounds gives an integral circulation.

At each slot exactly one outgoing arc therefore carries 1. Set w_t to its color. Flow conservation along the color chains makes the t-th chain flow equal to q_i(t), so its bounds give the claimed quotas. All arguments use the original real c_i: only their floors and ceilings are integer capacities. No approximation or rationality assumption has been made. QED.

## 2. One precolored incident edge

**Lemma 2.** Fix a degree d >= 1 and any color j. There are nonnegative integers n_i summing to d, each in [floor(c_i d), ceil(c_i d)], with n_j >= 1. Thus one incident edge of any prescribed color can always be completed locally.

**Proof.** Put l_i = floor(c_i d), u_i = ceil(c_i d), and m = sum_i l_i <= d. If l_j >= 1, the lower-bound vector already accommodates the prescribed edge. If l_j = 0, positivity gives 0 < c_j d < 1, hence u_j = 1. Also

    d - m = sum_i (c_i d - floor(c_i d))

is a positive integer, so m <= d - 1. Raising l_j from zero to one therefore still leaves the sum at most d. In either case the adjusted lower vector is coordinatewise at most u and has sum at most d. Since sum_i u_i >= sum_i c_i d = d, increase coordinates within their upper bounds until their sum is d. QED.

**Forest corollary.** Root each nontrivial tree. At the root, choose any integer vector between its lower and upper quotas with the correct sum, and color its child edges accordingly. At every subsequent vertex the parent edge is the only precolored edge; apply Lemma 2 and assign the remaining local counts to the child edges. This produces a full partition. The same proof extends any prescribed color on one selected edge of a tree: use its two endpoints as initial roots and proceed away from that edge. It does not extend arbitrary precolorings of many edges.

## 3. Coloring a regular core and its attached trees

We spell out both the graph structure and the coloring step.

The 2-core H is the maximal subgraph obtained by repeatedly deleting vertices of current degree less than two. Multiplicity contributes to degree. Any subgraph of minimum degree at least two survives the deletion procedure: inductively, none of its vertices can be the first deleted vertex. In particular, every cycle survives.

For a connected G with nonempty H, every component T of G - V(H) is a tree. Otherwise a cycle in T would survive. Moreover, T has exactly one attachment edge to H. At least one follows from connectedness. If it had two, the path within T between their outside endpoints, together with the two attachment edges and H, would contain a subgraph of minimum degree at least two. The path's internal vertices have degree two, its endpoints have their path and attachment edges, and core vertices retain degree at least two. If both attachments have the same outside endpoint, that endpoint already has degree two in this subgraph. This contradicts that those outside vertices were deleted. Thus G is precisely H with rooted trees attached. The same argument shows the 2-core of a connected graph, if nonempty, is connected: a path joining two purported core components would also survive.

Suppose H is r-regular and bipartite, with r >= 2. It decomposes into r perfect matchings M_1,...,M_r. Here is a proof including multiplicities. If A,B are its two sides, r|A| = |E(H)| = r|B|, so their sizes agree. For every S subset A, its r|S| incident edges end in N(S), which has at most r|N(S)| incident edges; hence |N(S)| >= |S|. To see directly why a perfect matching exists, choose a maximum matching and suppose it leaves some vertex of A unmatched. Explore alternating paths from all unmatched vertices of A, using nonmatching edges from A to B and matching edges back. No reached B vertex can be unmatched, or such a path would augment the matching. If S is the reached subset of A, every neighbor of S is reached in B: the matched neighbor of a reached matched A vertex was already used to reach it, and all other edges are explored outward. Every reached B vertex is matched to a vertex in S, while at least one vertex in S is unmatched. Thus |N(S)| < |S|, contradicting the counting inequality. The matching covers A and hence B. Remove it and repeat with the (r-1)-regular graph, stopping after r steps. Parallel edges do not affect this argument.

Choose the quota word of Lemma 1 for D = max_v d_G(v). Color all edges of M_t by w_t. Every core vertex now has exactly q_i(r) incident core edges of color i.

At a core vertex v, prescribe q_i(d_G(v)) as its final color counts. Since d_G(v) >= r and q_i is nondecreasing,

    q_i(d_G(v)) - q_i(r) >= 0,
    sum_i [q_i(d_G(v)) - q_i(r)] = d_G(v) - r.

Assign exactly these numbers of attachment edges at v to each color. No attachment edge has two core endpoints, and each outside tree has only one such edge, so these assignments never conflict. The final counts at v meet its original quotas by Lemma 1.

Now work outward along each attached tree. Each outside vertex has just its parent edge precolored; Lemma 2 completes its local counts. There is no edge between different attached trees and no cycle outside the core, so all edges receive exactly one color, and all quotas hold simultaneously. Components with empty core are forests and were handled above. This proves the theorem. QED.

The hypothesis concerns regularity of the entire surviving 2-core in each connected component. It does not cover arbitrary graphs formed by joining different regular blocks at cut vertices or by bridges that survive in the 2-core.

## 4. An exact dead end for arbitrary first-factor extraction

The accepted finite example is a ten-vertex simple tree with two degree-four vertices a,b, one degree-three vertex r, and seven leaves. The historical first-factor witness F_1 uses c = (3/5, 3/10, 1/10), leaves only the edges ar and br uncolored, and has first-factor degrees 3 at a,b, 1 at r, and 1 at every leaf. Its explicit edge list and factor-membership package are omitted. These graph and factor facts are historically checked finite premises for the authored argument below, not a reconstructed certificate in this edition.

At a and b its degree is 3, within [floor(12/5),ceil(12/5)] = [2,3]. At r it is 1, within [floor(9/5),ceil(9/5)] = [1,2]. At every leaf it is 1, within [0,1]. Thus F_1 is a valid first proportional factor. Its complement also meets the aggregate fraction 2/5 at every vertex, as expected from the two-factor theorem.

But each of a and b requires at least floor((3/10)4) = 1 edge of color 2. Their only remaining edges are ar and br, so both would have to receive color 2. At r, color 2 has upper bound ceil((3/10)3) = 1. Contradiction. The chosen F_1 cannot be completed, even if the remaining two colors are selected by an arbitrary method rather than proportional rescaling.

The historical audit also checked a different full partition; its explicit color-class witness is omitted. Independently of that omitted witness, the forest corollary already proves that the underlying tree admits a full partition. An empty color class is permitted: positivity of a fraction does not force a positive degree at small vertices.

The same dead end holds throughout the real parameter region

    1/2 < c_1 < 2/3,
    1/4 <= c_2 <= 1/3,
    c_3 = 1 - c_1 - c_2 > 0.

Indeed, F_1's degrees 3,1,1 remain permitted; both degree-four vertices require at least one color-2 edge while r permits at most one. The positivity condition is automatic under the displayed strict upper bound on c_1 and weak upper bound on c_2, but is written explicitly.

This refutes the universal extension assertion "any valid first factor can be completed." It does not refute an algorithm that chooses the first factor with additional global compatibility conditions, nor does it refute the original conjecture.

## 5. A fractional vertex of the natural simultaneous LP

Let G be a six-cycle, with k = 3 and c_i = 1/3. Every color quota at every vertex is [0,1]. The natural LP has variables x_{e,i} >= 0, edge equations sum_i x_{e,i} = 1, and degree inequalities sum_{e incident v} x_{e,i} <= 1.

Historical exact checks identified a feasible point with twelve nonzero coordinates equal to one half and six zero coordinates. They verified its feasibility and identified nine tight constraint rows on nine support columns with the odd-cycle pattern used below. The remaining three support coordinates are fixed by three further edge equations, forming the identity block described below. The explicit edge labeling, coordinate assignment, ordered row and column lists, and raw matrix certificates are omitted. Their realization in this LP is an explicitly stated finite premise, authenticated historically rather than independently reconstructed by this prose edition. The following authored determinant and vertex arguments are retained; no claim of a self-contained finite-witness reconstruction is made.

The checked 9 by 9 matrix has a 1 in columns j and j+1 of row j, with indices cyclically modulo nine, and zeros elsewhere. Its determinant is 2: in the determinant expansion the only nonzero permutations are the identity and the cyclic shift, both having positive sign because the cycle length is odd. Thus this integer matrix is not totally unimodular.

Conditional on these checked finite premises, the point is a fractional vertex, not merely an arbitrary fractional feasible point. Set its six zero coordinates to zero. Its twelve remaining coordinates consist of the nine selected variables and three additional support coordinates.

The nine selected tight constraints force each of the first nine variables to 1/2: the equations are z_j + z_{j+1} = 1 around an odd cycle. The three remaining edge equations force the other three coordinates to 1/2. In matrix form this 12 by 12 tight system is block triangular with the above determinant-2 block and a 3 by 3 identity block, so its determinant is 2. Together with the six tight nonnegativity constraints, it uniquely determines all eighteen coordinates. A feasible point uniquely determined by tight linear constraints is an extreme point, proving the claim.

The six-cycle plainly has integral feasible colorings, for example an alternating coloring using colors 1 and 2. Consequently a fractional LP vertex is not an infeasibility certificate. This result only blocks the assertion that the natural simultaneous constraint matrix is totally unimodular or that an arbitrary extreme point of this relaxation is automatically integral. It does not contradict alternative formulations or the already-known equal-fraction theorem.

## 6. Exact reduction of fixed-instance real fractions to rational cells

This is not needed for the theorem above, which directly treats real fractions, but identifies the correct scope of rational testing.

**Lemma 3.** For a fixed finite graph G and fixed k, every positive real vector c of sum 1 has a positive rational vector c' of sum 1 with exactly the same floor and ceiling values c_i d_G(v) at every vertex and color. Thus the set of feasible edge partitions is identical for c and c'.

**Proof.** If every degree is zero, take c'_i = 1/k. Otherwise consider the finite set of positive degrees. Whenever c_i d is an integer for one of those degrees, retain the equality c'_i = c_i; that coordinate is rational. For every other coordinate, require it to stay in the intersection of the open intervals between its neighboring thresholds m/d and (m+1)/d, for all degrees d, and in (0,1) when k > 1. This is an open interval with rational endpoints containing c_i. For the unfixed coordinates their required sum is rational, because it is 1 minus the fixed rational coordinates.

If there are no unfixed coordinates, we are done. If there is one, its required sum already makes it rational and unchanged. If there are at least two, choose rational approximations to all but the last sufficiently near their original values, and define the last to make the sum exact. The finitely many positive distances to interval endpoints ensure that all these coordinates, including the last, remain within their prescribed open intervals. All original integer equalities and all original strict threshold inequalities are preserved, so both floor and ceiling values agree. QED.

This lemma does not give permission to replace all real vectors by a bounded denominator grid. The finite computations below check exactly the stated rational vectors; no exhaustive coverage of real cells is claimed.

## 7. Exact checks and their limits

The historical companion constructor used integer network flows and matching augmentations, with rational inputs for reproducible tests. The independent checker recomputes all vertex degrees and two-sided quotas directly using rational arithmetic. It checks the determinant witnesses by exact Gaussian elimination and verifies every tight basis row. No third-party package is imported by either program. There are no assertion-dependent mathematical checks.

The retained candidate normal, -O, and -OO receipts agree byte for byte. They report the following checks; the unretained full stream has only the author-reported status stated below:

- 15,674 constructed partitions: all 461 accepted subgraphs of the labeled K_{3,3}, each at 34 distinct positive three-color vectors obtained from denominators 3 through 7. The other 51 graphs are outside the stated regular-core hypothesis and are deliberately not inferred feasible or infeasible by this constructor.
- 4,323 constructed partitions of all labeled trees on 2 through 6 vertices, at three specified fraction vectors.
- 1,178 finite quota words, of lengths 0 through 30.
- 3,390 local extensions with one prescribed incident color.
- Six retained concrete partition certificates, including parallel-edge, cubic-core-with-trees, and disconnected mixed-core examples.
- The exact first-factor dead end, including rejection of all four possible residual two-color assignments and verification of a different full partition.
- The determinant-2 minor and twelve-variable tight basis of the fractional vertex.
- Eight negative controls: invalid partition, zero fraction, false determinant, dependent basis, invalid first factor, non-bipartite input, irregular-core input, and corrupted quota word.

The candidate-reported canonical generated partition-certificate stream has SHA-256:

    b628757d417447231c559c6370225c8e0bd2a2cb04b14b3f829d1788ad9bff83

The full finite stream was not retained; six individual partitions and both obstruction certificates were retained separately and are omitted here. The candidate's unretained full generated stream hash is authenticated author-reported metadata only. The independent audit constructed and checked its own valid partitions; it did not recreate the candidate stream and does not claim byte-identical reproduction. The historical controls validate implementations and concrete witnesses. The written proofs establish the unbounded real-fraction theorem independently of finite checks. Preparation of this edition performed byte-integrity and editorial checks only, with no new mathematical execution, scholarly-source retrieval, text extraction, or visual inspection.

## 8. Source boundaries

The original question is retained from Egres, "Partitioning a bipartite graph into proportional factors," revision 2419:

https://oldlemon.cs.elte.hu/egres/open/Partitioning_a_bipartite_graph_into_proportional_factors

The retained complete scholarly sources are:

1. J. R. Correa and M. X. Goemans, *Improved bounds on nonblocking 3-stage Clos networks*, SIAM Journal on Computing 37(3), 870-894 (2007), DOI https://doi.org/10.1137/060656413. Full author-linked PDF: http://www.dii.uchile.cl/~jcorrea/papers/Journals/CG2007.pdf. Section 2, printed pages 877-879, gives the two-factor lemma and relaxed decomposition, and explicitly leaves the sharper general question unsettled there.
2. U. Feige and M. Singh, *Edge Coloring and Decompositions of Weighted Graphs*, June 25, 2008 preprint, corresponding to ESA 2008, DOI https://doi.org/10.1007/978-3-540-87744-8_34. Full official research-site PDF: https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf. Conjecture 1.4 states the exact target; Theorem 1.5 and Section 3 give the simultaneous relaxed bounds and separate one-sided results. Section 1.2 explicitly includes bipartite multigraphs.

The already-recorded k = 2, equal-fraction, regular, and all-integral-target cases are not presented as new discoveries. The separate upper-only and lower-only partitions in Theorem 1.5 do not supply the same-partition target. This work does not claim a comprehensive later-literature or novelty search. Its regular-core theorem may be an elementary consequence already known elsewhere; only its proof and exact scope are claimed here.
