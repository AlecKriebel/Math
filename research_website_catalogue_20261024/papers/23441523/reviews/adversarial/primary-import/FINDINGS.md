# Limited primary-theorem import check: Alon–Shapira

**Conclusion: the requested adaptive, two-sided, dense-model triangle-freeness lower bound is supported.** Its order is `exp(Ω(log²(1/ε)))`. The source counts inspected vertices; converting to adjacency queries requires a linear endpoint-count argument, not squaring the lower bound. The bound concerns sufficiently small proximity and sufficiently large graph order depending on proximity, not every graph order.

This is a limited external-theorem check for 23441523. I have not read that paper or any current/archived opinions about it, and this is not a verdict on its reduction or main result.

## Source and exact locations

The requested `https://www.math.tau.ac.il/~asafico/subdir.pdf` failed DNS in the shell and timed out through the web tool. The same author's `subdir.pdf` was acquired from [the accessible CS host](https://www.cs.tau.ac.il/~asafico/subdir.pdf). It is a 32-page February 2004 author manuscript. SHA-256:

`4a3281bbbd041392d814f07c2745d4c600ee9f20aa97fd781db0d8f94ac98641`.

An older 30-page [Alon-hosted manuscript](https://www.cs.tau.ac.il/~nogaa/PDFS/testdig5.pdf) was initially inspected, but the final conclusions use the 32-page `subdir.pdf`. The older copy has a different Section 7 presentation and is not silently treated as identical. Both files, extraction, and relevant rendered pages are saved. `source-receipt.json` records provenance.

| Printed page(s) in the 32-page source | Relevant content |
|---|---|
| 2, §1.1 | Tester knows `n`; may ask adjacency of a desired vertex pair; success at least 2/3; edit distance normalized by `n²`. |
| 4 | Complexity convention: number of sampled/inspected vertices, with all their induced adjacencies available. |
| 4–5, Theorem 4(ii) | For a core outside the easy classes, two-sided lower bound `(1/ε)^{c log(1/ε)}`, with `c>0` depending only on the forbidden graph. |
| 5 and 24, opening of §7 | Explicit application of the same lower bound to undirected non-bipartite forbidden graphs. In particular, this covers `K₃`. |
| 6, last paragraph of §2.1 | Small-ε and sufficiently-large-n convention. |
| 20–23, Lemmas 6.1–6.4 and (7)–(10) | Behrend-type construction; for each sufficiently small ε and every sufficiently large n depending on ε; construction parameter `m ≥ (1/ε)^{c log(1/ε)}`. |
| 26–27, proof of Theorem 4(ii) | Randomly relabelled YES/NO distributions, matching small views and collision bound `O(|S|³/m)`; Yao argument. |
| 27–28 | Alternative distribution construction making the NO support always far, rather than far with probability tending to one. |

The displayed exponent on page 5 and collision argument on page 27 were also checked visually, not only by extracted text.

## Exact usable consequence

For undirected simple labelled graphs, let the promise distinguish triangle-free graphs from graphs requiring at least `ε n²` edge deletions to become triangle-free. There are positive constants `a, ε₀`, and a threshold `n₀(ε)`, such that for `0<ε<ε₀` and sufficiently large `n≥n₀(ε)`, bounded-error randomized testers require worst-case adjacency-query cost at least

`exp(a [log(1/ε)]²)`.

Changing constant success probabilities above one-half or fixed constant factors in the distance normalization does not change this asymptotic order. The conclusion is a worst-case lower bound for a tester required to handle every graph satisfying the promise. It is not a lower bound for each individual input.

The source's theorem and §6 construction give a statement for every sufficiently small ε, not merely an unspecified sparse sequence of ε values. The large-n hypothesis matters: exhaustive inspection costs `O(n²)`, so no positive lower bound depending only on ε at the above order can hold for all small n. Equivalently, any query bound uniform in n must have this dependence on ε.

## Oracle and adaptivity check

The definition on page 2 is not a model in which the algorithm is forced to request anonymous random vertices or to forget n. It allows named-pair adjacency requests with n supplied. Section 7 uses random relabelling as an adversarial input distribution, not as a restriction on algorithms.

Here is the explicit adaptive interpretation of its collision argument. After conditioning on all latent positions assigned to previously inspected names and on all answers so far, every uninspected name still occupies a uniformly random unused position under the random relabelling. A deterministic adaptive algorithm may choose its next name from its transcript, but cannot bias that unused position. The first two distinct projected vertices of a designated arithmetic-progression cycle determine that cycle. The chance a fresh inspected name lands in its remaining vertices is at most `O(1/m)`, with the harmless without-replacement correction absorbed when n is sufficiently large and the inspected set has size at most n/2. A union bound over at most `O(k³)` ordered triples gives bad-view probability `O(k³/m)`. Thus named adaptive choices do not evade the argument. Yao then covers randomized choices.

For the triangle specialization, the YES distribution deletes one uniformly chosen edge from each designated edge-disjoint triangle, while the simpler NO distribution retains an entire triangle with probability 2/3 and deletes it otherwise. Before two edges of the same designated triangle are observed, the exposed edge bits have the same independent Bernoulli-2/3 law. Two such edges require three projected vertices. This directly realizes the undirected version; one need not assume that forgetting directions in an arbitrary hard directed instance preserves triangle distance. The source's §7 expressly states the undirected corollary.

The stronger vertex-inspection oracle reveals only the subgraph induced by inspected vertices. It does **not** reveal a vertex's complete neighbourhood in the uninspected graph and does not supply a neighbour-sampling oracle.

A q-query adjacency tester mentions at most 2q vertices. A vertex-inspection tester can simulate it by inspecting an endpoint the first time it appears, remembering all induced edges, and then returning the requested bits. Thus a k-vertex lower bound gives `q ≥ k/2`, retaining `exp(Ω(log²(1/ε)))`. It would be incorrect to infer a squared adjacency lower bound merely because a canonical induced-subgraph tester can use `Θ(k²)` adjacency queries.

## Normalization and quantitative algebra

Triangle-freeness is monotone, so additions cannot improve the optimum editing cost: it equals minimum edge deletions. For unordered-edge normalization `d/binom(n,2)`, the exact conversion to `d/n²` is multiplication by `(n−1)/(2n)`. Constant-factor proximity rescaling therefore handles either convention. If an undirected edge is encoded as two opposite directed arcs, that convention adds another factor two; it should not be silently omitted when stating an exact threshold, though it does not alter the asymptotic lower bound.

The source gives `k(ε) ≥ (1/ε)^{c log(1/ε)}`. Taking logarithms yields `log k ≥ c [log(1/ε)]²`, up to the fixed change of log base. The collision proof may reduce c by a fixed factor (approximately one third, then a further margin), and the endpoint simulation introduces a factor one-half. These losses still give a positive constant in `exp(Ω(log²(1/ε)))`.

The simpler NO distribution is far with probability `1−o(1)` as ε tends to zero. Conditioning it on the far event changes the transcript distribution by at most `o(1)` in total variation, so it supports the promised-input lower bound. The source also outlines an always-far paired-cycle variant on pages 27–28. No one-sided-only argument is being substituted for a two-sided one.

## Mismatch assessment

No mismatch was found with the limited import requested here: adaptive, two-sided, n-known, arbitrary named adjacency queries, dense triangle-freeness, and the quasipolynomial dependence on inverse proximity. An application must preserve the sufficiently-large-n quantifier and convert its own proximity and query units explicitly. This check does not determine whether 23441523 does so; that comparison belongs to its main reviewer.
