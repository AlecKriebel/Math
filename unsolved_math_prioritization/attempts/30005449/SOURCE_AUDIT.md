# Source gate: trace-reinforced ant walks, 30005449

The exact OWR contribution is Kious–Schapira, joint with Mailler, “Finding geodesics on graphs using reinforcement learning algorithms,” OWR 12/2023, pp. 645–646, DOI 10.4171/owr/2023/12. The deterministic-limit question is the second, trace-reinforcement model; its several-food-sources sentence is a further modeling question, with no specified optimization or limit criterion.

The primary full paper is Kious–Mailler–Schapira, *The trace-reinforced ants process does not find shortest paths*, Journal de l'École polytechnique — Mathématiques 9 (2022), 505–536. The linked author PDF is a February 2022 proof copy; the final Numdam PDF was separately retrieved and is the definitive edition for page references.

Model: a finite undirected graph, two distinct vertices N (nest) and F (food), and W_e(0)=1. Walk n+1 starts at N, uses transition probabilities proportional to W(n), and stops on first hitting F. Weights are frozen during each walk. After stopping, each edge visited at least once gains exactly one, regardless of traversal count. This is neither ordinary edge-reinforced random walk nor the backward loop-erased/geodesic return model.

The paper's statement preceding Conjecture 1.1 excludes multiple edges incident to F. Its discussion after Theorem 1.3 explicitly records the Dirichlet random limit for parallel N–F edges. That excluded example is credited known behavior, not a counterexample to the intended conjecture. Components inaccessible from N before hitting F have constant weights and zero normalized limits; they can be discarded for analysis.

The exact target retained here is almost-sure convergence to deterministic normalized weights for all admissible finite graphs, together with a mathematically specified several-food extension. No result about shortest-path selection will be substituted. The stronger positivity clause in the paper is not part of the imported target.

The known paper proves examples and graph families and gives the general stochastic-approximation representation X(n)=W(n)/(n+1), drift p(w)-w, where p_e(w) is the edge-trace probability. Proposition 2.7 provides a Lipschitz drift on a suitable compact invariant set. These are established inputs, not new results of this attempt.

Current literature check: Mailler–Varin, arXiv:2601.22855 (2026), treats two nests with one food source and backward loop-erased reinforcement on triangle-series-parallel graphs. It is a relevant neighboring model but does not resolve this trace-reinforced target or its several-food version. No exact general deterministic-limit proof was found in the bounded source search; this is not a novelty guarantee.

Primary sources:
- https://doi.org/10.4171/owr/2023/12
- https://publications.mfo.de/bitstream/handle/mfo/4033/OWR_2023_12.pdf?sequence=4
- https://www.numdam.org/item/JEP_2022__9__505_0.pdf
- https://math.univ-lyon1.fr/~schapira/articlespdf/antsJEP.pdf
- https://arxiv.org/abs/2601.22855

No prior exact campaign PR, target branch, or committed target path was found. No separate research_results entry is joined by OWR-12697708-002; the full pinned problem record contains the earlier dated source triage. Source retrieval consumes no proof turn.
