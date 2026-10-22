# Independent mathematical audit: proportional bipartite factors

## Verdict and immutable subject

**ACCEPT the restricted theorem and the two stated obstructions. No mathematical correction is required. The unrestricted target remains unresolved by this work.**

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete general mathematical proofs are retained, including the integer-circulation argument, multiplicity-aware core structure, alternating-path proof of the matching decomposition, tree propagation, and boundary-preserving rational-cell lemma. This is not a computational reproduction package. Explicit finite witness lists, edge and coordinate packages, indexed constraint rows, matrix certificates, raw certificates, and executable code are omitted. The two finite obstructions retain their authored logical arguments conditional on explicitly stated, historically checked finite premises; this edition does not independently reconstruct those omitted premises. Neither obstruction is used to prove the regular-core theorem.

The candidate's unretained full generated stream hash is authenticated author-reported metadata only. The independent audit constructed and checked its own valid partitions; it did not recreate the candidate stream and does not claim byte-identical reproduction.

The unrestricted same-partition proportional-factor target remains unresolved by this work. No novelty, priority, exhaustive later-literature survey, or certification of current global problem status is claimed.

The accepted original result is 19,632 bytes, SHA-256 `ec7aa57d680537f478b6a8454deb2be62f8b4daf71f43230e13aef411209939b`. Its 28-member candidate package has a 6,112-byte manifest with SHA-256 `9b7da8e140951ac445f94672839a613bc9b52679cb7d027116e7f5cc083ddb47`. The original audit is 15,464 bytes, SHA-256 `49cbd7f1c2673c8a3a688894f8f963a173d99415613d35598ba8dbc2c34bbefa`; its 20-member package manifest has SHA-256 `06caca28a8e758b2238230bcb620c071e2f67fb7cc74112e13c7075d8bdd58d8`. The auditor checked the complete candidate inventory and every listed byte count and digest. These identify the accepted originals, not the edited public files, whose bindings appear in ACCEPTANCE.json.

The accepted theorem covers every finite loopless bipartite multigraph for which each connected component has either empty 2-core or a regular nonempty 2-core; the regular degree may vary across components. It holds for every positive real fraction vector summing to one. It includes all forests and bipartite pseudoforests, regular bipartite multigraph cores with arbitrary attached trees, disconnected unions, isolated vertices, the null graph, and the one-color case. It does not assert a theorem for arbitrary irregular 2-cores, or graphs obtained by joining otherwise regular blocks in ways that create an irregular surviving core.

Neither obstruction disproves the original conjecture. No novelty claim, later-literature completeness claim, or certification that the original conjecture is currently open is accepted or needed.

## 1. Finite quota words for genuinely real fractions

The directed construction in Lemma 1 is correct. At every slot node exactly one unit enters. Sending the original real number c_i to its color-chain node supplies a feasible real circulation: the chain flow after slot t is t c_i, which lies between its own floor and ceiling. At the source and sink, the return arc has the required flow D. Every lower and upper capacity is an integer, even when c_i is irrational.

Subtracting lower bounds leaves integer node imbalances and nonnegative integer residual capacities. Introduce a super-source and super-sink to balance them. Real feasibility implies that the total required supply is achievable. An augmenting-path flow starting from zero is integral throughout and increases by a positive integer on every augmentation. Total supply is a finite integer, so the process terminates; a nonsaturating terminal flow would have a residual reachable-set cut contradicting real feasibility. Restoring lower bounds yields an integral circulation.

Therefore each slot chooses one color, and chain conservation gives exactly the corresponding prefix counts. The asserted monotonicity is a consequence of the word, rather than an independently rounded choice at each degree. This distinction is essential when extending from a regular core to vertices of differing total degree.

No rational approximation is used in this proof. The D=0 case is explicitly empty. With k=1, the sole fraction is one and all prefix counts equal their lengths. A single global finite word up to the maximum degree is sufficient; no infinite-word theorem is required.

## 2. A prescribed incident edge and tree propagation

Lemma 2 correctly handles an arbitrarily chosen prescribed color j. If its lower quota already reaches one, nothing changes. Otherwise positivity gives 0<c_j d<1, hence upper quota one; the sum of fractional parts is a positive integer, so at least one unit remains after the lower quotas. Allocating that unit to j is legal. The sum of upper quotas is at least d, ensuring the other units can be distributed without exceeding any upper quota.

Thus every vertex with at most one precolored incident edge has a valid completion. In a rooted tree, only its parent edge was colored earlier. When one selected tree edge is prescribed in advance, using its endpoints as the two initial roots preserves the same invariant on both sides. This argument never assumes extension of arbitrary multiple-edge precolorings.

At degree one, every positive color remains allowed because its ceiling is one. Isolated vertices impose zero counts. The one-color case presents no exception.

## 3. Multiplicity-aware 2-core structure

The deletion characterization used in the candidate is valid for multigraph degree. Any subgraph of minimum degree at least two survives: there cannot be a first deleted vertex from that subgraph. Consequently an outside component contains no cycle, including a two-edge parallel cycle, and hence is a tree.

For a connected graph with nonempty core, each outside tree has an attachment by connectivity. If it had two attachment edges, take the unique outside path between their outside endpoints and unite it with the core and those edges. All added outside vertices have degree at least two in this subgraph. This remains true if both outside endpoints coincide, if the two core endpoints coincide, or if the attachment edges are parallel. The core vertices retain their original core degrees. The resulting minimum-degree-two subgraph contradicts deletion of the outside vertices. Thus exactly one attachment is possible.

Similarly, a path joining two hypothetical distinct core components would survive, proving core connectivity inside a connected graph. Bridges joining cyclic portions can survive in a 2-core; the report correctly excludes the unjustified inference that all graphs made of regular blocks satisfy its hypothesis.

## 4. Matching decomposition and simultaneous extension

For an r-regular bipartite multigraph with r>0, equality of the side sizes follows by counting edges. Counting the r|S| edges incident to S proves Hall's inequality because their endpoints have total incident capacity r|N(S)|. The candidate's alternating-path proof then establishes a perfect matching without relying on simplicity. Removing its edge copies leaves an (r-1)-regular bipartite multigraph. Repetition produces precisely r disjoint perfect matchings, including the final degree-one stage.

Assigning the t-th matching the t-th quota-word color gives every core vertex the same count q_i(r). At a vertex of original total degree d, monotonicity makes q_i(d)-q_i(r) nonnegative, and the differences sum exactly to the number d-r of attachment edges. The final target q_i(d) meets the quotas at the original degree, not at a residual degree. Since each outside tree has exactly one core attachment, assignments made at different core vertices cannot conflict.

Propagation by Lemma 2 then colors every edge outside the core once, with no later modification of a completed vertex. Different graph components have disjoint edge sets; they may use different r values while sharing the same fraction vector and, if desired, the same finite word. Empty-core components are exactly forests. This proves the complete stated restricted theorem, without reliance on a bounded search.

## 5. Ten-vertex arbitrary-first-factor obstruction

The historically checked graph has nine edges, is connected, and is acyclic. Its explicit edge and factor-membership lists are omitted, so these facts are finite premises rather than a self-contained reconstruction here. Its nonleaf degrees are 4,4,3. At c=(3/5,3/10,1/10), the selected first factor has degrees 3,3,1 at those vertices and one at every leaf, so all its quotas are valid. Its two-edge complement also meets the aggregate 2/5 quotas.

Nevertheless both degree-four vertices need at least one color-2 edge. Since each has only its edge to r left, both residual edges must get color 2, whereas the degree-three vertex r allows at most one. This is a failure of completion by any residual assignment, not merely by a particular rescaling method. Exhaustive inspection of the four residual two-color assignments independently confirms the contradiction.

The alternative full coloring checked in the accepted original is valid; its explicit witness is omitted. The forest corollary independently proves existence of a full partition. Thus this is not a counterexample to simultaneous proportional factorization.

The entire advertised real region is also valid. If 1/2<c_1<2/3, the degree-four first-factor count three and degree-three count one are both admissible. If 1/4<=c_2<=1/3, the degree-four color-2 lower quota is one and the degree-three color-2 upper quota is one, including both c_2 endpoints. Finally c_1+c_2<1, so c_3 is positive automatically. The two strict c_1 endpoints cannot be added for this first factor: at c_1=1/2 its degree-four count is too high, and at c_1=2/3 its degree-three count is too low.

This refutes “every valid first factor extends.” It does not say “no first factor extends,” and does not rule out a globally informed choice of the first factor.

## 6. Six-cycle LP obstruction

The historically checked point satisfies every edge equation and every nonnegative degree quota. The explicit coordinate assignment and indexed row/column and matrix certificates are omitted; feasibility and realization of the tight blocks below are finite premises, not self-contained reconstructions in this edition. Its support has twelve coordinates, all equal to one half, and the other six coordinates vanish. The independent historical reconstruction of row coefficients from graph and color labels gave the nine-by-nine cyclic matrix I+P, where P is a nine-cycle permutation matrix. Its only nonzero determinant terms are the identity and the full cycle, both positive, so its determinant is two. The natural joint-color constraint matrix is therefore not totally unimodular.

This alone would not prove that the supplied point is a vertex. The additional argument in the candidate is necessary and correct: on the twelve-coordinate support, the nine tight rows form the determinant-two block; three remaining edge equations provide an identity block for the remaining coordinates. The resulting twelve-by-twelve determinant is two. Adjoining the six independent tight zero-coordinate equations yields full rank eighteen, uniquely identifying the feasible point. It is a genuine fractional extreme point.

The alternating two-color integral coloring still satisfies the three-color instance, with the third class empty. Thus neither the fractional point nor the non-TU minor establishes infeasibility. The obstruction concerns this specific natural relaxation and automatic integral extreme-point rounding, not other formulations or the equal-fraction theorem.

## 7. Rational cells and threshold boundaries

Lemma 3 correctly treats each fixed finite degree set. If c_i d is integral for any positive degree d, then c_i itself is rational and must be fixed exactly. For each other coordinate, all relevant strict threshold inequalities determine a nonempty open interval with rational endpoints. Their intersection contains the original coordinate. Positivity and, for k>1, the strict upper bound one are preserved.

The remaining sum is rational. With no unfixed coordinates the claim is immediate; with one, the sum forces its original rational value. With at least two, rational approximations to all but the last can be chosen close enough that the last coordinate, defined by the exact sum, stays inside its open interval. The finite positive margin to the boundaries justifies this step. Degree zero contributes only the fixed quota zero; when all degrees vanish the uniform rational vector suffices.

Therefore both floors and ceilings, including equality cases, are preserved and the complete feasible-partition set is unchanged. This does not imply a universal bounded denominator, nor does checking any preselected finite denominator grid exhaust all real cells. The main theorem already handles real fractions directly, independently of this lemma.

## 8. Independent executable checks and limits

The audit program was written from the mathematical statements and raw certificates. No candidate program was read as implementation source, imported, or executed. It uses only the Python standard library, exact rational arithmetic, and exact comparisons in Q(sqrt(2)). Prefix words are generated by dynamic programming on quota count vectors rather than by the candidate's circulation algorithm; perfect matchings are found by a separate finite backtracking method. Every resulting partition is checked directly against the original vertex degrees and quotas.

The frozen normal, -O, and -OO outputs are identical. They verify:

- The complete 28-member candidate inventory at the externally supplied manifest pin.
- All six retained concrete partitions, with the parallel, cubic-core, disconnected mixed-core, isolated, and one-color cases represented.
- The first-factor obstruction, all four impossible residual assignments, and a different valid full partition.
- Both determinant-two certificates and full tight rank eighteen.
- All 461 in-scope subgraphs among the 512 labeled K_{3,3} subgraphs, at the same 34 three-color vectors, giving 15,674 independently constructed and checked partitions.
- All 1,441 labeled trees on two through six vertices, at three specified vectors, giving 4,323 independently constructed and checked partitions.
- Additional prefix, local prescribed-color, selected tree-edge, bounded multiplicity, exact irrational, real-region, rational-cell boundary, and endpoint controls. Aggregate counts and the historical receipt identity appear in VERIFICATION.json. Detailed inputs and output words are omitted.
- Ten semantic or integrity negative controls, plus the separate seal negative-control suite.

The exact irrational examples were checked through degree forty without floating point. A boundary-preserving rational-cell control also verified identical floors and ceilings while retaining an integer quota equality exactly. Explicit example vectors, degree lists, and output quota words are omitted; these finite controls are not reproducible from the public edition alone.

These computations are finite controls. The unbounded theorem and full real parameter region are accepted on their written proofs. The candidate's original full generated stream was not retained and was not recreated by executing its programs; its particular stream hash is therefore only an authenticated author-reported computation record. This audit generated independent valid partitions and does not claim byte identity with that stream.

## 9. Scholarly source scope

The target and contextual bounds agree with the retained Egres page, revision 2419, [Partitioning a bipartite graph into proportional factors](https://oldlemon.cs.elte.hu/egres/open/Partitioning_a_bipartite_graph_into_proportional_factors). The live web opening failed during this audit; the retained page and text were available and authenticated by the candidate inventory. This is not a live status certification.

Correa and Goemans, [Improved bounds on nonblocking 3-stage Clos networks](https://www.dii.uchile.cl/~jcorrea/papers/Journals/CG2007.pdf), SIAM Journal on Computing 37(3), 870–894 (2007), Section 2, printed pages 877–879, supplies the two-factor lemma and relaxed decomposition and distinguishes the sharper question. Its public PDF opened successfully during this audit. The retained PDF's byte count and SHA-256 were verified; the relevant source passages were inspected.

Feige and Singh, [Edge Coloring and Decompositions of Weighted Graphs](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf), June 25, 2008 preprint, Conjecture 1.4, Theorem 1.5, and Sections 1.1–1.2 and 3, supports the target, the relaxed simultaneous result, distinct one-sided decompositions, previously recorded special cases, and multigraph scope. The public PDF opened successfully; the retained PDF's byte count and SHA-256 were verified. Separate upper-only and lower-only partitions do not prove the same-partition target.

This audit inspected the passages needed for those scope claims. It did not survey all later literature or establish priority. No copied scholarly document or private coordination material is included in this public edition. Its preparation performed no new scholarly-source retrieval, text inspection, extraction, visual inspection, or later-literature search.
