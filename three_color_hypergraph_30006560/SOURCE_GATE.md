# Source and scope assessment

Checked 3 October 2026.

## Primary statement

Hans Yu, Question 8 and Theorem 9, in *Combinatorics*, Oberwolfach Report 1/2026, printed pp. 71–72 (PDF pages 67–68).

- Official report landing page: https://publications.mfo.de/handle/mfo/4435
- Publisher DOI: https://doi.org/10.4171/OWR/2026/1
- Official PDF: https://publications.mfo.de/bitstream/handle/mfo/4435/OWR_2026_01.pdf?isAllowed=y&sequence=1
- Catalogue page: https://www.unsolvedmath.com/problems/30006560

The official PDF was downloaded for local inspection and its statement page was rendered and visually checked. The exact catalogue URL returned HTTP 403, including in the cloud browser; its current problem body was not independently read. The mathematical statement used in these notes is grounded in the official report.

The question fixes r≥3 and counts r-sets containing at least one hyperedge of each of three colors in an (r−1)-uniform hypergraph. It is not a minimum hitting-set problem. The report gives √(6RGB) as the known all-r upper bound and √(2RGB) as the known r=3 bound and conjectural all-r upper bound. The square-root placement was checked on the rendered page.

These notes use the ordinary finite simple, one-color-per-edge interpretation. This is explicit in the graph primary papers and consistent with the report's bounds. Allowing the same underlying edge to carry all three colors would change the problem radically: one such edge plus arbitrarily many extra vertices would already violate any fixed bound on the r-set count with R=G=B=1. There is no proper edge-coloring assumption in the question.

## Current primary literature examined

1. T.-W. Chao and H.-H. Hans Yu, *Kruskal–Katona-type problems via the entropy method*, J. Combin. Theory Ser. B 169 (2024), 480–506; arXiv:2307.15379. Theorem 1.1 proves T²≤2RGB for simple three-edge-colored graphs. Its higher-uniformity rainbow-clique problem has the number of colors growing with uniformity; that is different from the fixed-three-color partial-shadow problem here. https://arxiv.org/abs/2307.15379
2. T.-W. Chao and H.-H. Hans Yu, *A Purely Entropic Approach to the Rainbow Triangle Problem*, arXiv:2407.14084. This supplies another proof of the graph bound; it does not justify applying the sharp constant independently of core overlap in arbitrary hypergraphs. https://arxiv.org/abs/2407.14084
3. T.-W. Chao and H.-H. Hans Yu, *When Joints Meet Extremal Graph Theory: Hypergraph Joints*, arXiv:2410.06498v1, especially §§1.2–1.5. This develops the partial-shadow/projected-generically-induced-joints connection and uniformity-independent bounds. It was not found to supply the desired sharp √2 constant for the present question. https://arxiv.org/abs/2410.06498
4. J. Balogh, P. Bradshaw, R. I. Garcia and B. Lidický, *Density of rainbow triangles and properly colored K4's*, arXiv:2511.21061. Its triangle and properly colored clique results concern ordinary graphs and do not settle this all-uniformity question. https://arxiv.org/abs/2511.21061
5. T.-W. Chao, M. Sankar and H.-H. Hans Yu, *On Colorful Kruskal–Katona Theorems*, arXiv:2610.02165v1, posted 1 October 2026. Sections 7.1 and 7.5 discuss unequal graph color-class counts and higher-uniformity rainbow cliques. These are pertinent distinctions but do not provide a resolution of the fixed-three-color question in this report. https://arxiv.org/abs/2610.02165

No primary-source full resolution was located in this bounded literature check. That is not a certification that no such result exists. The package records an unresolved outcome and makes no first-resolution claim. No source PDFs, screenshots, or third-party document bodies are included in the package.
