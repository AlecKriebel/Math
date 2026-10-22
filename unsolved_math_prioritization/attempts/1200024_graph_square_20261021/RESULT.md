# A nonunimodular counterexample to graph-square invariance

## Result

Under the standard free-uniform-spanning-forest convention b_F(G)=E[deg_FUSF(G)(o)]/2−1, the unrestricted vertex-transitive assertion in Abért's Question 24 is false.

Take the binary grandparent graph G: fix an end of the 3-regular tree, retain its tree edges, and add an edge from every vertex to its grandparent toward that end. This is an infinite connected locally finite simple vertex-transitive graph, with degree 8 and nonunimodular full automorphism group. Its simple square joins distinct vertices at G-distance at most two.

The exact original expectation and a certified bound for the square are

E[deg_FUSF(G)(o)] = (24−√2)/7 > 3.22,
E[deg_FUSF(G²)(o)] ≤ 3208526010913748780/10^18 < 3.21.

Consequently b_F(G)=(10−√2)/14, whereas b_F(G²)<121/200=0.605. In particular b_F(G)−b_F(G²)>1/200.

The original value is proved by exact finite series-parallel reductions and a controlled free-exhaustion limit. The square inequality is proved by finitely supported rational unit flows on an explicit finite subgraph containing all 40 edges incident to the root in G². Integer arithmetic checks every divergence equation and every flow energy. Floating-point computation was used only to find feasible witnesses; it is not used in their verification or in the original-graph lower bound.

## Proof and replay map

1. grandparent_proof.md: full graph construction, transitivity and full-group nonunimodularity, exact two-terminal branch reductions, genuine free exhaustion, exact original expectation, and strict lower bound.
2. grandparent_exact_resistance.md: independently derived alternative induced-exhaustion calculation of the same original expectation.
3. SQUARE_BOUND.md: finite graph embedding, complete square-root neighborhood, and the precise Thomson/Rayleigh/Kirchhoff transfer yielding the upper bound.
4. square_flow_certificate.json.gz: the rational flow witnesses, including their exact graph edge order and energy numerators.
5. verify_square_certificate.py: standard-library-only exact replay. Run with Python normally or with -O. It reconstructs the graph from tree-word coordinates, checks the entire edge list, verifies all 40 flows, and proves the strict bound by integer comparison.
6. test_certificate_mutations.py: rejects eight deliberate corruption classes under optimized Python.
7. certify_square.py: optional numerical witness generator (NumPy and SciPy), not trusted for verification.
8. exact_replay.json, exact_replay_optimized.json, mutation_replay.json: observed exact replay reports.

## Research approaches and limitations

- Source/scope screen: the printed 2010 question is about arbitrary vertex-transitive graphs. Its Cayley case is already affirmed by the author. The source does not impose unimodularity. This report does not claim the question remained open through 2026, or that this counterexample is novel in the literature.
- Common-action projection method: square invariance holds for graphs with a common unimodular transitive action. The explicit polar-isometry/mass-transport argument is in unimodular_projection_comparison.md. This restricted affirmative statement does not apply to the counterexample.
- Energy/zero-invariant method: the Dirichlet energies of G and G² are equivalent, preserving the finite-energy quotient modulo the closure of finitely supported functions. Thus vanishing of b_F is invariant even without unimodularity. This does not imply equality of positive values.
- Determinantal comparison: operator_notes.md gives an exact graph-projection defect formula. Its two rooted diagonal terms cancel under a tracial/unimodular hypothesis; no such cancellation was assumed in the nonunimodular calculation.
- Explicit-family/electrical method: the Diestel–Leader zero case is not a counterexample. The grandparent family instead yields a positive original value and the strictly smaller square bound above. The exact gap ends the search without requiring a closed formula for the square expectation.

## Source record

All following inspections were performed through web text on 21 October 2026. No locally retrieved scholarly PDF hash is claimed.

- Miklós Abért, Some questions, 2 November 2010, printed p. 4, Question 24 and adjacent author comment: https://www.renyi.hu/~abert/research/questions.pdf . The original target and already-known Cayley case were checked. Its introduction warns that listed questions might later have been solved.
- Itai Benjamini, Russell Lyons, Yuval Peres, Oded Schramm, Uniform Spanning Forests, Annals of Probability 29 (2001), corrected author-hosted version 27 January 2009: https://rdlyons.pages.iu.edu/pdf/usf.pdf . The finite electrical marginal identity, free-exhaustion framework, and projection formulas are standard dependencies; Theorem 6.4 importantly gives wired expected degree 2 on every transitive network, not merely unimodular ones.
- Damien Gaboriau, Invariant Percolation and Harmonic Dirichlet Functions, arXiv:math/0405458v3: https://arxiv.org/pdf/math/0405458 . The harmonic projection invariant is developed with an explicitly unimodular transitive action; it was not used outside that scope.
- Pengfei Tang, Weights of uniform spanning forests on nonunimodular transitive graphs, arXiv:1908.09889v2: https://arxiv.org/pdf/1908.09889 . The grandparent family and Diestel–Leader comparison informed the candidate screen. Its connectivity/branching results do not supply the expectation comparison proved here.

The Lyons–Peres book URL https://rdlyons.pages.iu.edu/prbtree/book_corr.pdf returned a content-size error for a full web fetch; no claim of complete inspection is made. Earlier attempted shell retrievals of Abért's PDF produced HTML, not scholarly PDF bytes. They are not proof artifacts.

No public posting, repository action, or queue update is part of this result package. Acceptance is subject to the separately hash-bound adversarial audit.
