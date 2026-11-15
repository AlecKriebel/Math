# Multiplicatively Weighted Centers of Median Graphs in Quasilinear Time

Alec Kriebel · 14 October 2026 · Zenodo version 1.0

The manuscript prints 14 October 2026 and no version number. Zenodo identifies this record as version 1.0; the record was created on 15 October 2026, separately from its declared publication date.

## Original abstract

We record a short reduction from multiplicatively weighted center thresholds to additively weighted eccentricities on a graph with bounded integral distances. Combining it with the algorithm of Bergé, Ducoffe and Habib and a known implicit optimization method gives a deterministic O(n log⁵(2n)) algorithm for a center, the optimum radius and all centers of every finite unit-edge median graph. This answers the finite algorithmic form of Open Problem 1 in Ducoffe’s Oberwolfach report, without a bound on cube dimension. The contribution is the threshold observation and its consequence; neither the additive algorithm nor the optimization mechanism is new. We specify the exact comparison model and give explicit corrections to two estimates in the public preprint proof of the imported algorithm.

## What the result means

A weighted center chooses a vertex that minimizes the worst weighted distance to every vertex of a graph. A larger weight makes distance to that vertex more costly. Median graphs include trees and hypercubes; every three vertices have a unique median on all three pairwise shortest-path intervals.

This note turns each multiplicative distance threshold into an additive arrival-time problem, then combines credited algorithms to find the exact optimum and every vertex attaining it. The graph may have arbitrarily large cube dimension, and no embedding is supplied.

## The full result

Let G=(V,E) be a finite, nonempty, connected, simple graph with unit edge lengths, n=|V| and shortest-path distance d. Each vertex u has a finite nonnegative real weight w(u). For a candidate vertex x define r_w(x)=max_{u∈V} w(u)d(x,u), the optimum ρ=min_{x∈V} r_w(x), and the full center set C_w={x∈V:r_w(x)=ρ}.

Theorem 1. Given G by adjacency lists, with the promise that G is median, and any such weight profile, a deterministic algorithm computes the exact radius ρ, one vertex in C_w and the entire set C_w in O(n log⁵(2n)) exact operations. No cube-dimension bound or supplied embedding is required. Operations on the original profile only compare bounded integer multiples k w(u), where 0≤k≤n−1.

Zero-weight vertices stay in both the graph and the candidate domain. If n=1 or all weights are zero, the radius is zero and every vertex is a center. The result concerns vertex centers with the original shortest-path distances.

## Why the reduction works

Put D=n−1. For a nonnegative trial radius R, define b_R(u)=max{k∈{0,…,D}:k w(u)≤R} and a_R(u)=D−b_R(u). When w(u)=0, the budget b_R(u) equals D. Bounded binary search finds each budget using comparisons, without a real-division or unbounded-floor primitive.

For every vertex x and every R≥0, w(u)d(x,u)≤R is equivalent to d(x,u)≤b_R(u), hence to d(x,u)+a_R(u)≤D. Taking all u gives the exact identity {x:r_w(x)≤R}={x:E_{a_R}(x)≤D}, where E_a(x)=max_u(d(x,u)+a(u)). This preserves the whole feasible set, rather than only deciding whether it is empty. Negative radii are infeasible.

The imported Bergé–Ducoffe–Habib algorithm computes all additive eccentricities for a nonnegative integer arrival profile on a median graph in O(n log⁴(2n)) time, including preprocessing. Here 0≤a_R(u)≤D. The short threshold identity works for bounded integral graph distances; the efficient median-graph conclusion uses this credited additive oracle.

The optimum is one of the products k w(u). A known implicit optimization mechanism, credited to Ducoffe, searches the n sorted product rows without materializing their n² entries. The note gives a self-contained comparison-only variant: active intervals include their endpoints, lower row middles are weighted by inclusive interval lengths, and feasible equality is saved in an incumbent with a witness before deletion. These rules cover ties and zero rows. Each step deletes at least one quarter of the active entries, so O(log(2n)) oracle calls suffice; a final query at ρ returns every center.

The already published appendix supplies consistent estimates for the recursion in the named author preprint arXiv:2410.10235v1. It uses f(s)=2⌈log₂s⌉ for s≥3, direct base cases for s≤2, and a fixed-root depth estimate. Both original-arrival and fiber-arrival slice calls are retained. Total child volume at each depth is at most the root order and depth is O(log²n), giving the required additive O(n log⁴(2n)) bound. The appendix credits BDH’s algorithm and structural discoveries; it makes no assertion that the inaccessible final SODA chapter contains the same proof errors.

## Exact comparisons and bit costs

The operation count is an exact comparison model, not an encoding-independent bit-time bound. The optimum can be stored as a pair (k,u) representing k w(u). Overall the search uses O(n log²(2n)) comparisons of original-weight products, in addition to the imported graph operations.

For rational input w(u)=p_u/q_u with positive denominators and numerator and denominator components of at most B bits, comparing k w(u) with j w(v) compares k p_u q_v with j p_v q_u. These integers have O(B+log n) bits; their multiplication and comparison costs, and input reading, must be paid. The additive oracle’s bounded integer labels, including its internal updates, use O(log n) bits. The theorem does not promise unit-cost arbitrary-precision arithmetic or a linear-space oracle.

## Scope and limitations

The graph is finite, nonempty, connected, simple and unit-edge, supplied by adjacency lists and promised median. Recognition of median graphs, arbitrary edge lengths, continuous facilities along edges and an unspecified encoding of infinite median graphs are outside the theorem. The separate unimodality question in Ducoffe’s report is not settled by this global threshold algorithm.

The accompanying package includes exact reference controls, manuscript source and proof comparisons. Its all-pairs and brute-structure routines check finite cases; they are not a fast general implementation or an experimental proof of the asymptotic bound. Reproduction instructions require normal assertion-enabled execution.

The contribution is the short threshold observation and its consequence. The additive algorithm, implicit optimization mechanism and classical median preprocessing are credited prior work. The bounded literature assessment does not establish worldwide firstness or continued open status at a later date. The appendix’s corrections are explicitly limited to the named public author-v1 proof, whose log-base and product estimates it addresses; no claim about errors in the final SODA publication is made.

## Background and credit

Ducoffe’s Oberwolfach report asks the finite n-vertex weighted-center algorithmic question, within a discussion that also includes infinite graphs, edge lengths and unimodality. This note answers the finite unit-edge vertex-center form without a cube-dimension bound. It does not claim all the separate questions in that discussion.

Bergé, Ducoffe and Habib provide the additive all-eccentricities algorithm and its median-graph structure. Ducoffe’s ESA 2026 Lemma 2, and Lemma 2.2 of its full author-v1 preprint, already supply the decision-to-optimization mechanism. Classical median algorithms and preprocessing, including the work of Bénéteau, Chalopin, Chepoi and Vaxès, remain dependencies.

For cube-free median graphs, Chalopin, Chepoi, Dragan, Ducoffe and Vaxès already proved the stronger O(n log²n) bound. The present O(n log⁵(2n)) result does not improve that subclass. Algorithms using a supplied tree-product embedding have a stronger representation promise; the unweighted MFCS theorem and the later weighted consequence in the workshop report are not identified as the same statement.

## Contribution and collaboration

Substantive mathematical verification, extensions within a clearly stated model and collaboration toward journal submission are welcome. Authorship should reflect actual contributions. This is a passive invitation; no claim of an existing collaboration is implied.

## AI and review disclosure

Unrefereed preprint. AI tools were used extensively in solving, developing, writing, reproducing and adversarially verifying the work. Internal AI adversarial reviews are not human peer review; the manuscript has not received human peer review or proof-assistant certification.

## Read and download

Read the unchanged, searchable five-page manuscript below, or open or download the original PDF. The complete original verification ZIP is available alongside the citation.

- [Open original PDF](assets/weighted_centers.pdf)
- [Download complete original ZIP](assets/verification_package.zip)
- [Download BibTeX citation](assets/citation.bib)
- [Zenodo record](https://doi.org/10.5281/zenodo.23385145)

## Primary background

- [Ducoffe, Radius functions in median graphs — Oberwolfach report](https://doi.org/10.4171/OWR/2026/8)
- [Bergé, Ducoffe and Habib — additive median-graph algorithm](https://doi.org/10.1137/1.9781611978322.52)
- [Named author preprint arXiv:2410.10235v1 — appendix comparison target](https://arxiv.org/abs/2410.10235v1)
- [Ducoffe, ESA 2026 — prior decision-to-optimization mechanism](https://doi.org/10.4230/LIPIcs.ESA.2026.133)
- [Ducoffe, full author-v1 preprint](https://arxiv.org/abs/2607.04287v1)
- [Chalopin et al. — stronger cube-free result](https://arxiv.org/abs/2503.15011v1)
- [Ducoffe, MFCS 2021 — supplied tree-product embeddings](https://doi.org/10.4230/LIPIcs.MFCS.2021.43)
- [Bénéteau et al. — classical median algorithms](https://doi.org/10.1016/j.jcss.2022.01.001)

## Rights

The paper and authored supporting materials are released under Creative Commons Attribution 4.0 International (CC BY 4.0), as recorded by Zenodo and the package README. Cited third-party publications retain their own rights. No separate code-license grant is identified.
