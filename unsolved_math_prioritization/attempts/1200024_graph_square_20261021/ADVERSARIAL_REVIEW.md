# Independent adversarial audit: grandparent graph versus its square

Date: 21 October 2026 UTC.
Verdict: PASS for the mathematical counterexample under the explicitly stated convention b_F(G)=E[deg_FUSF(G)(o)]/2−1. No publication or queue edit was performed. The verdict is bound to the exact input hashes below; it does not certify an altered package or a literature novelty claim.

## Audited conclusion

For the binary grandparent graph G and its simple graph square H=G²,

E[deg_FUSF(G)(o)] = (24−√2)/7 > 161/50,

E[deg_FUSF(H)(o)] ≤ 3208526010913748780/10^18 < 321/100.

Thus the expected degrees differ, and b_F(G)−b_F(H)>1/200. The result does not depend on a floating-point lower bound, wired boundary approximation, unimodular trace identity, or a conjectured exact value for H.

## Adversarial checks and findings

1. Target scope and normalization. I read SOURCE_GATE.md and independently inspected Abért's author-hosted Question 24 and adjacent Cayley-graph comment through web PDF text. The question is about arbitrary vertex-transitive graphs and does not print a unimodularity restriction. The source itself does not print the normalization formula; the package appropriately states b_F=Edeg/2−1 as its convention. A strict difference of expected degrees gives a strict difference under this convention. No graph-cycle rank or clique-complex invariant was substituted.

2. Graph, transitivity, and full automorphism group. G is simple, connected, infinite, locally finite, and degree 8. The stabilizer of the selected tree end is transitive. Parent-type edges occur in exactly three triangles; grandparent-type edges occur in exactly one. These counts recover the underlying tree from G. The graph induced on the three recovered tree-neighbors is K_(1,2), whose center is the parent. Thus the parent relation is invariant under the full automorphism group, not merely a preferred subgroup. The paired stabilizer orbit sizes for a child-parent pair are 1 and 2. This establishes genuine nonunimodularity, while G² remains vertex transitive under the same end-preserving action.

3. Original-graph lower bound. I checked every step of grandparent_proof.md. Each finite descendant branch attaches at precisely its parent and grandparent, with no other exit. The branch recurrence k_(m+1)=(1+qk_m)/(2+qk_m), k_0=1/2, uses free truncation. Its positive limit is unique. The two-parameter finite networks are increasing and their diagonal exhausts every vertex and edge. Successive upper-ray elimination produces B_(m,n)=T_(c_m)^(n−2)(c_m), with T_c(t)=c+t/(1+t). Its uniform contraction on the relevant interval justifies the diagonal limit, not merely an unjustified exchange of limits. The final triangle resistances yield R_parent=(3√2−2)/7 and R_grandparent=(6−2√2)/7. At the root there are three edges of the first type and five of the second. Their sum is the claimed expectation. The rational inequality √2<73/50 gives the strict 161/50 bound.

4. Independent finite reduction replay. I wrote check_finite_reductions.py without importing the candidate's graph generator or recurrence code. It builds each finite graph from its ancestor relations and solves its grounded Laplacian using exact Fraction Gaussian elimination with two right-hand sides. All 18 cases q∈{2,3}, m∈{0,1,2}, n∈{2,3,4} agree exactly with both claimed resistance formulas. This is a check on the finite identities and boundary indexing, not a substitute for the infinite-limit proof. I also read the independent induced-exhaustion proof grandparent_exact_resistance.md and found its terminal-branch treatment, coefficient indices, contraction estimate, and limits consistent with the main proof.

5. Finite square graph embedding. The certificate graph is the square J=K² of the grandparent graph induced on the radius-10 underlying-tree ball. Every J edge is an H edge; paths in K cannot create spurious square edges. Conversely, a root H-neighbor is reached by at most two grandparent-graph steps, each spanning at most two tree edges. The entire witnessing tree walk is within the radius-4 ball, so J contains every H edge incident at the root. Exact full enumeration gives 40, not merely a chosen subset. One combinatorial count is four strict ancestors, 30 descendants at depths one through four, one sibling, one uncle, two children of the sibling, and two children of the uncle.

6. Independent graph and flow replay. I wrote independent_replay.py using undirected breadth-first tree adjacency and geodesic distance toward a vertex at tree distance 14 to determine the end direction. It does not import the candidate verifier, constructor, or numerical generator and does not use their word-parent implementation. Its radius-10 graph has 3,070 vertices and 6,137 original edges. Its square has 19,931 edges and exactly the complete 40-element root neighborhood found separately in the larger graph. It exactly matches the supplied edge order. The checker validates all 797,240 integer flow entries, terminal and interior balance, each energy numerator, the total denominator, and the strict inequality. Both normal and optimized Python executions pass. The supplied standard-library checker also passes in both modes.

7. Boundary condition and variational direction. The supplied flows are finite-support unit flows from each root neighbor to the root. Reversing source and sink has no effect on resistance. In J, Thomson's principle bounds resistance above by each energy. In every sufficiently large free finite exhaustion of H, the same flow is feasible and Rayleigh monotonicity gives R_Hn≤R_J. The decreasing free limit therefore satisfies R_H^F≤R_J. Kirchhoff's marginal identity then gives each FUSF edge probability, and summing over all 40 neighbors gives an upper bound on expected degree. This does not improperly replace free resistance by wired resistance. The energy sums each undirected edge once; there is no hidden factor of two. Division by two occurs only in the explicitly defined b_F normalization.

8. Corruption resistance and trust boundary. I replayed the supplied optimized mutation tests: all eight corruptions are rejected, covering a flow imbalance, wrong graph edge, omitted root neighbor, omitted flow, wrong energy, wrong denominator, wrong q, and noninteger flow. The NumPy/SciPy constructor was inspected, but neither its floating solves nor its reported decimal values are trusted proof steps. Exact corrected flows and integer replay are sufficient. No claim is made here that the numerical constructor was rerun.

9. Supplementary comparison arguments. The projection comparison's energy estimate, polar isometry, squared-kernel mass transport, and half-incidence normalization check. Its use of unimodularity is explicit. The zero-invariance explanation is consistent with equivalent Dirichlet norms, the common closure of finitely supported functions, the harmonic projection, and the wired expected-degree theorem for transitive networks. These supplementary statements are not needed for the counterexample's strict gap.

## Source inspection and limits

I independently used web PDF text to inspect the following primary material on this date:

- Miklós Abért, Some questions (2 November 2010), printed p. 4, Question 24 and its adjacent comment: https://www.renyi.hu/~abert/questions.pdf .
- Benjamini, Lyons, Peres and Schramm, Uniform Spanning Forests, corrected author-hosted version dated 27 January 2009: https://rdlyons.pages.iu.edu/pdf/usf.pdf . Theorem 4.1 and its surrounding electrical discussion support the finite marginal/energy identity; Section 5 gives the free-exhaustion construction; the proof of Theorem 7.3 gives free versus wired edge marginals; Theorem 7.8 gives the projection formulation; Theorem 6.4 covers wired expected degree 2 without requiring unimodularity.

The author-hosted Lyons–Peres full book could not be fetched by the web tool because of its content-size limit. This audit does not claim full-book inspection, valid local scholarly-PDF bytes, or a scholarly-PDF SHA-256. The source gate's failed HTML downloads are not treated as papers. No external source text, dataset content, private source, or private coordination material was published. The audit establishes the stated mathematical separation, not whether the result is new or was previously unknown.


Packaging note: this is the mathematical and source-inspection portion of the accepted audit. Original input inventories and coordination paths are omitted; code provenance is supplied separately.
