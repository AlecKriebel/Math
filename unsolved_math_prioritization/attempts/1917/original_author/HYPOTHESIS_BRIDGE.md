# Exact hypothesis and conclusion bridge

This is an authored implication check, not a new proof of the cited theorem.

Let cp(G) denote the minimum number of complete subgraphs with at least two vertices whose edge sets form a disjoint union equal to E(G). Let F(n) = floor(n(n+1)/6).

The source defines rooted simplicial defect zero by requiring that, in every induced subgraph H and outside each proper clique Q of H, at least one vertex has a clique neighbourhood. This condition follows from the standard Dirac simplicial-vertex theorem: a noncomplete chordal graph has two nonadjacent simplicial vertices, of which a clique contains at most one. If H is complete, any vertex outside Q works. Induced subgraphs of a chordal graph remain chordal. Conversely, an induced cycle of length at least four has no simplicial vertex, so the rooted condition excludes such a cycle. Thus the parameter-zero class is exactly the target class. Dirac's theorem is an imported standard result, not re-proved here.

Assume Theorem 1.1 of [Okechukwu v1](https://arxiv.org/html/2609.20871v1) is correct. Choose its fixed parameter s=0. Its constants K₀ and N₀ depend only on zero and therefore are absolute constants, independent of G and n. Its all-order assertion gives

cp(G) ≤ F(n) + K₀ ≤ n²/6 + n/6 + K₀.

For n≥1 and K₀≥0, the last quantity is at most n²/6 + (1/6+K₀)n. For n=0, cp(G)=0 separately. This is exactly the requested uniform O(n) upper bound. The source's eventual equality classification is unnecessary for this implication. There is no assumption of connectedness, splitness, a minimum degree, or a clique-drop hypothesis in the theorem being imported.

The manuscript introduces a minimum-degree condition in an intermediate rigidity proposition and derives it for minimal counterexamples before applying that proposition. Treating the intermediate condition as a hypothesis of the final theorem would misstate the source. Likewise, an o(n²) approximation alone would not give O(n); the finite construction and minimal-counterexample step must be valid.
