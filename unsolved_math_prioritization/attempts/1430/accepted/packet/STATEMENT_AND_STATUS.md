# GRAPH-043 / problem 1430: statement and disposition

Research checkpoint: 2026-10-08 UTC. Queue rank 1015.

## Recovered question

Authored paraphrase of the question in Section 9 of Sergey Kitaev's 2017 survey: does some word-representable graph G have R(G)>floor(|V(G)|/2)?

Source: [A Comprehensive Introduction to the Theory of Word-Representable Graphs](https://arxiv.org/abs/1705.05924), Section 9, printed page 35. The author-hosted copy inspected through the web interface is dated May 30, 2017; it is not a newly written 2026 survey.

Throughout the relevant theory, graphs are finite, simple, undirected, and the question concerns graphs admitting a word representation. Each vertex must occur. Distinct vertices are adjacent exactly when their two-letter projection has no equal consecutive letters. A k-uniform word contains exactly k occurrences of every vertex. R(G) is the least positive such k. N below always means the total number of vertices, to distinguish it from a part size in a bipartite graph.

The question is not about the minimum unrestricted total word length, the permutation-representation number, the dimension of an arbitrarily selected orientation's reachability poset, the representation number of a fixed orientation, or generalized k-11/multi-word representations. Treating non-word-representable graphs as having R=infinity would supply irrelevant examples and defeat the question's intended domain.

## An actual defect in the unqualified wording

The source question does not state a lower cutoff for N. Literally, its answer is affirmative:

* R(K1)=1>floor(1/2)=0.
* The two-vertex edgeless graph has R=2>floor(2/2)=1: 0011 represents it, and any 1-uniform word represents a complete graph.
* The connected three-vertex path has R=2>floor(3/2)=1: 010212 represents edges 01 and 12, and the graph is not complete.

These elementary exceptions are not a resolution of the intended extremal research question. We investigate the explicitly repaired nontrivial regime N>=4. That restriction is our statement clarification, not wording silently attributed to the source. All labeled graphs on 4 and 5 vertices are 2-representable; the packet supplies and checks a witness for every one.

## Conservative status

**Unsolved here; five substantive mathematical approaches completed.** No graph in the nontrivial regime with R(G)>floor(N/2) is supplied, and no universal floor(N/2) upper bound is proved. Literal small-order exceptions are proved, separately classified as a wording defect. No novelty, global-openness, peer-review, or formal-certification claim is made.

The exact retained gap is whether a finite simple word-representable graph with N>=4 can have R(G)>floor(N/2). Equivalently, prove R(G)<=floor(N/2) for all such graphs or exhibit a word-representable counterexample with a rigorous lower bound on R. A word alone gives an upper bound, not a lower bound.

## Bounds and indexing

The corrected general literature upper bound is R(G)<=2N-4 for N>=3, with the clique-sensitive 2(N-omega(G)) bound for noncomplete graphs. The preliminary assertion R<=N must not be used. For the crown-plus-apex construction, a crown has two parts of size m and the added apex gives **N=2m+1**, while R=m for m>=2. This proves equality with floor(N/2) at these odd orders; it does not prove the maximum equals floor(N/2) at every order.

The new primary preprint [Colbrook–Drysdale, arXiv:2609.35842v1](https://arxiv.org/abs/2609.35842), dated 24 September 2026, proves the stronger bipartite bound R<=ceil(N/4) for N>=9. Its even-order extremality corollary includes the exceptional crown values: 2 for part sizes 1,2,3; 3 for part size 4; ceil(m/2) for m>=5. This is a bipartite result and does not resolve the general question. The preprint's Lean/certificate statements are the authors' reports; this packet does not reproduce or certify them.
