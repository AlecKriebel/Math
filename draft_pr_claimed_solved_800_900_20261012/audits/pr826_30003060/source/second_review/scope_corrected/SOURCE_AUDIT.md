# Source and scope audit

Checked 6 October 2026 UTC. This is a bounded investigation, not an exhaustive literature review.

## Original question and surrounding conventions

The original source is *Hochschild Cohomology in Algebra, Geometry, and Topology*, Oberwolfach Reports 13 (2016), 449-506, DOI [10.4171/owr/2016/10](https://doi.org/10.4171/owr/2016/10). Andrea Solotar's contribution, *Koszul Calculus*, jointly with Roland Berger and Thierry Lambre, occupies printed pp. 479-481. The question occurs near the end on p. 481 and asks for the equivalence between Koszulness and positive-degree higher Koszul homology vanishing.

The entire contribution was read, including its opening definition of quadratic algebras and its coefficient conventions. It does not impose a characteristic-zero restriction. It first discusses bimodule coefficients and then specializes to coefficients A. The preceding and following contributions are different talks; their assumptions must not be imported into Solotar's contribution. In particular, the next talk's introduction begins after Solotar's references on p. 481. The report title is a workshop title, not a unified paper imposing one common field convention on all contributions.

The requested [unsolvedmath page](https://unsolvedmath.com/problems/30003060) could not be retrieved: the web tool reported it inaccessible and direct retrieval returned HTTP 403. No access restriction was bypassed. The complete cached problem record and associated reports were checked instead, with exact dataset, statement and pair hashes. Its short statement also has no field restriction. Cached content is not asserted to be a fresh live-page observation.

## Exact definition and characteristic-zero theorem

The primary detailed reference is Berger-Lambre-Solotar, [*Koszul calculus*, Glasgow Mathematical Journal 60 (2018), 361-399](https://doi.org/10.1017/S0017089517000167), also [arXiv:1512.00183v3](https://arxiv.org/abs/1512.00183v3). Both the publisher PDF and v3 PDF were retrieved and inspected at the relevant sections.

Section 2 permits arbitrary relation subspaces, including R=0. Section 5.2 defines the fundamental-cocycle higher homology in all characteristics. Section 6.2 explicitly assumes characteristic zero for Theorem 6.4; there HK^hi_0(A)=k holds for every quadratic A, and Koszulness implies positive-degree vanishing. The subsequent Conjecture 6.5 displays both these conditions, without an explicit characteristic hypothesis in its statement. Its preceding discussion asks about removing the characteristic restriction and about a converse. Hence a source-faithful report must distinguish the literal unrestricted statement from the characteristic-zero converse motivated by the theorem. This distinction already appears in [arXiv:1512.00183v1](https://arxiv.org/abs/1512.00183v1), dated 1 December 2015, before the February 2016 workshop: printed p. 24 has the characteristic-zero Theorem 6.4, the proposed removal of that hypothesis, and the displayed Conjecture 6.5 without it. Thus a characteristic-zero reading is a plausible research motivation, not a verified exclusive historical intention. A reviewer may accept the unrestricted counterexample without claiming to have settled the characteristic-zero converse.

The [2019 addendum](https://doi.org/10.1017/S0017089518000137), published online 22 April 2018, was retrieved completely. It is a dedication to Jean-Louis Koszul, not a mathematical correction or a solution of this conjecture.

## Later literature checked

- Berger-Taillefer, [*Koszul calculus of preprojective algebras*, arXiv:1905.07906v2](https://arxiv.org/abs/1905.07906v2), published in J. London Math. Soc. 102 (2020), 1241-1292. Relevant introduction, higher-calculus definitions, and Remark 6.25 were inspected. Its computations and multi-vertex setting do not supply a solution of the one-vertex characteristic-zero target.
- Berger-Maillard, [*Calabi-Yau property in derived Koszul calculus*, arXiv:2505.19921v1](https://arxiv.org/abs/2505.19921v1), a May 2025 preprint. The introduction and Sections 4.2-4.3 were inspected. The result concerns derived functors and strong Kc-Calabi-Yau duality, including polynomial algebras. It does not establish the requested general converse.
- Berger, [*Koszul calculus for N-homogeneous algebras*, arXiv:1610.01035v2](https://arxiv.org/abs/1610.01035v2): abstract/version metadata inspected only, not used for a mathematical conclusion. The ScienceDirect URL in the cached triage was inaccessible and was not treated as a verified separate paper.
- The author's publication/preprint pages and targeted searches for the title, Conjecture 6.5, higher Koszul homology, positive characteristic, free algebras, converse, and counterexample were checked. No attributable prior publication of this exact free-algebra counterexample or general characteristic-zero resolution was located. Search silence proves neither novelty nor current universal open status.

## Disposition

The proof here concerns the literal unrestricted-field equivalence and its characteristic obstruction. It does not disprove a characteristic-zero conjecture or answer the characteristic-zero vanishing-to-Koszulness implication. A broad label such as "Koszulness conjecture solved" would be misleading. Independent review should retain this distinction when assigning any queue status.
