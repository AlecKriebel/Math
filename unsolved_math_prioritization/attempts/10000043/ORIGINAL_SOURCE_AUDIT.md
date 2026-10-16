# Source audit: infinite-cluster intersections with vertical fibers

Checked 30 September 2026. The exact source is Itai Benjamini, *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013, Open Problem 9.49 on p. 76. The direct [author URL](https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf) currently returned 404. The complete PDF was recovered from the [preserved author-site snapshot](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), read locally, and checked against a rendering of p. 76.

## Model and scope

The standing graph conventions on p. 5 specify simple, countable, locally finite graphs. Section 4.1 on p. 32 defines independent Bernoulli bond percolation. Section 4.2 on p. 33 adopts infinite connected graphs and defines the Cartesian product. No bounded-degree hypothesis is imposed on the target. Section 9.6, pp. 75–76, provides the relevant context and ends with the fiber-intersection question.

The target hypothesis is p_c(G)=1 for bond percolation on the base graph. The product uses the same fixed retention probability p for each horizontal and vertical edge. The parameter can lie anywhere in [0,1], including the product's critical value. The two endpoints are trivial, as recorded in the partial note.

The original wording asks about infinite intersections with fibers; the pinned formulation explicitly restricts to fibers that the cluster meets. Section 1 of `PARTIAL.md` shows that any infinite intersection propagates to all fibers on a connected base. The submission therefore preserves the meaningful finite-nonempty-intersection target and does not exploit an empty fiber as a counterexample.

## Prior attempt and duplicate gate

The main-branch queue row was rank 49, queued, with 0/5 turns. Searches of the state, assessment/reset histories, related-target groups, attempt-path tree and commits, all-state PR titles and bodies, and the problem-specific remote branch found no prior project attempt. A full pinned-dataset title/statement search found no duplicate.

The pinned research-results dictionary has an `OPEN-TRIAGE` note for AMR-099-0043. It records only a web/arXiv literature check without a proof, counterexample, or substantive proof attempt. It was read before this attempt and is not treated as mathematical evidence.

`source_record.json` preserves the catalogue entry from [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), CC BY 4.0, pinned revision `37e53eabe540fb458758e198be61634bd02ee008`. Upstream PDF files are used for source inspection and are not included in the repository package.

## Exact prior theorem and its limitation

The section cites Itai Benjamini and Gady Kozma, [*Uniqueness of percolation on products with Z*](https://alea.math.cnrs.fr/articles/v10/10-02.pdf), ALEA 10(1) (2013), 15–25. The complete paper was retrieved and read. Theorem 2 assumes a single uniform bound K on the number of edges needed to separate any finite base set from infinity. Under that hypothesis it proves absence of infinitely many infinite product clusters. Published Lemma 7 gives the desired infinite-fiber conclusion within that proof. In [arXiv version 2](https://arxiv.org/abs/1105.2638), this same lemma is numbered 5; the manuscript uses the published numbering.

The example in their Theorem 1 has a strongly amenable, subexponential-growth base but contains copies of a high-dimensional integer lattice. Its base critical probability is strictly below 1. It is therefore not a counterexample satisfying the present hypothesis.

The elementary stretched-tree construction in `PARTIAL.md` shows why the uniform cutset assumption cannot simply be substituted for p_c(G)=1. It has bounded degree and critical probability 1 but no uniform cutset bound. No conclusion about the original fiber question on that example is asserted.

## Later literature check

A targeted primary-source search checked the source paper's current arXiv and journal versions and related work on uniqueness, products, and fiber intersections. [Hutchcroft–Pan, *Percolation at the uniqueness threshold via subgroup relativization*](https://arxiv.org/abs/2409.12283), 2024, gives relative Burton–Keane theorems, including Theorems 1.7 and 3.1. Those theorems control the number of clusters with infinite intersection with an amenable subgroup or a suitable marked set. They do not state that every infinite cluster has infinite intersection with such a set, which is the issue remaining here. No unproved transfer from their relative uniqueness results is used.

No complete primary-source resolution of the exact target was located in this bounded search. This is not an exhaustive literature certification. The capped-exploration result is stated as a partial deduction with no historical-priority claim, and the original universal question remains unresolved in this attempt.
