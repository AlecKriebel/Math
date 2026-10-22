# Erdős Problem 156: source and status gate

Checked 2026-10-21 UTC. Literature recovery only; no new mathematical result or solution claim.

## Decision

**OPEN; no full resolution located.** The source matches the integer-interval small maximal Sidon problem. The available evidence does not justify treating its open classification as stale. A recent fixed-cardinality computational preprint is additional partial information, not an asymptotic solution. Direct retrieval of the official problem page returned HTTP 403; the indexed official page was accessible and said OPEN, but its crawl was four months old. Thus this is not a verified live-page status as of today, nor an exhaustive guarantee against unindexed later work.

## Exact target

For an integer N≥1, let g(N) be the least cardinality of an inclusion-maximal Sidon subset of {1,…,N}. Sidon here means that a+b=c+d, with all four entries in A, forces equality of the unordered pairs, including repeated entries. Inclusion-maximal means A∪{x} is not Sidon for every x∈{1,…,N}\A.

The question is whether there are absolute C and N₀ such that for **every** integer N≥N₀ there exists such an A with |A|≤C N^(1/3). A can depend on N. An estimate for only selected N, a single example, or a bound whose constant grows with N does not establish this target. There is no requirement that the choices for successive N be nested.

Original source: Erdős, Sárközy and Sós, *On Sum Sets of Sidon Sets, I*, Journal of Number Theory 47 (1994), 329–347, DOI https://doi.org/10.1006/jnth.1994.1040. Problem 7 on printed p.346 asks precisely this small inclusion-maximal-set question. The scanned page was visually inspected: its size symbol is ≪, not the ≤ sometimes produced by text extraction. The Sidon convention on p.329 includes equal summands. Public repository: https://real.mtak.hu/110604/ .

## Established bounds

Ruzsa, *A Small Maximal Sidon Set*, The Ramanujan Journal 2 (1998), 55–58, https://doi.org/10.1023/A:1009757824153, proves g(N)=O((N log N)^(1/3)). The theorem, proof and closing remark were inspected in the author-hosted DVI, converted locally to a readable PDF; that manuscript has five pages and a 1999 print stamp, so its pagination is not the published four-page pagination. Its closing bound is N^(1/3)≪g(N)≪(N log N)^(1/3). It uses random lifts of a modular Singer set, controls blocking outside selected residue classes, and then bounds the cost of extending to maximality. The logarithm is present in the theorem, not merely a notation artifact. Author source: https://www.renyi.hu/~ruzsa/cikkek/sidmax.dvi .

## Variant guards

- Maximal does not mean maximum cardinality. Large Sidon-set constructions, whose size is of square-root order, do not provide the requested small maximal sets.
- Integer saturation must include both x=a+b−c and 2x=a+b obstructions. The Ruzsa source explicitly lists both. Requiring only A+A−A to cover the interval is a stronger sufficient condition, not an equivalent formulation without additional argument.
- Redman, Rose and Walker, *A Small Maximal Sidon Set in Z₂ⁿ*, https://arxiv.org/abs/2109.00292 (v3, 2022), Theorem 3.1, gives O((n·2ⁿ)^(1/3)) in an elementary abelian 2-group. It changes both the ambient group and the convention to distinct summands, and retains a logarithmic factor when written in terms of the group size. This is not a resolution over integer intervals.
- Dias da Silva and Nathanson, *Maximal Sidon Sets and Matroids*, https://arxiv.org/abs/math/0504226, concerns special generalized-Sidon ambient sets and equal sizes of maximal subsets, not an O(N^(1/3)) interval construction.
- Thornburgh, *Uniform exclude distributions of Sidon sets*, https://arxiv.org/abs/2407.11783, concerns APN-function graphs over characteristic-two vector spaces, not the integer target.
- Riblet and Schehr, *Existence of a Sidon set for the distinct distance constant*, https://arxiv.org/abs/2505.20851, concerns maximization of reciprocal-power sums over infinite Sidon sets. Its existence theorem does not give the small saturated finite intervals required here.
- The neighboring original Problem 8 concerns an infinite Sidon asymptotic basis of order three. Results resolving that question must not be transferred to original Problem 7.

## Recent finite-cardinality result, limited inspection

Felix Huber's 2026 preprint *Saturated Sidon Sets in Consecutive Intervals: The Eight-Mark Threshold Is 144*, linked from the author's OEIS A399118 entry, states in Theorem 1.1 that the largest interval length admitting a saturated eight-element set is 144. Its convention [n]={0,…,n−1} is translation-equivalent to the target. The theorem, explicit example, blocker criterion, and claimed computer-assisted proof scope were read through the public PDF: https://oeis.org/A399118/a399118.pdf . The attached computation was not independently replayed. Record this as a preprint theorem claim with fixed-cardinality scope, not a verified full solution. Finite values cannot remove the asymptotic logarithmic gap.

## Search and access limits

Searches covered the exact title/problem, “maximal Sidon” with 2025/2026 and integer/logarithmic terms, cited papers, author-hosted sources, and relevant group analogues. No matching all-N O(N^(1/3)) theorem or contrary unbounded-factor lower bound was found. Discussion posts, AI-generated research pages and search summaries were used only to discover sources, not as mathematical proof. Public-source access outcomes and file fingerprints are recorded separately.
