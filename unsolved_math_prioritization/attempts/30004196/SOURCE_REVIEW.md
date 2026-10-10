# Sources and scope: ancient oval limits

Problem 30004196 / OWR-17130-012. Historical source checks: 10 October 2026.

The original question asks for an ancient oval as a moving-center blowup of one
flow from a smooth closed embedded surface in R^3, at a limiting time strictly
after its first singular time. It remains OPEN in this work. The accepted main
arrival-time theorem is restricted to globally mean-convex initial surfaces;
this does not narrow the original problem. The full source and hypothesis
review below is preserved from the independent audit.

During the independent audit, all nine source PDFs listed by the candidate were retrieved from their primary public URLs on 10 October 2026. Every retrieved PDF matched both the candidate's recorded byte count and SHA-256 hash. The historical retrieval times, exact versioned URLs, match results, and precise text and visual inspection locations are retained in [SOURCE_METADATA.json](SOURCE_METADATA.json). Source PDFs, extracted text and rendered pages are not distributed.

### 3.1 Original question

The contribution in [Oberwolfach Report 34/2019](https://ems.press/content/serial-article-files/46813), PDF pages 40–42, begins with smooth closed embedded surfaces in R^3, discusses both mean-convex and general initial surfaces, and places the later-singularity question in the footnote on PDF page 41, printed page 2073. That page was inspected visually. The candidate's broader original-class interpretation is faithful. A full negative answer cannot follow from the mean-convex arrival-time argument alone. Beyond singularities, a legitimate specified continuation is needed; the candidate preserves the canonical outer/inner-flow distinction.

### 3.2 CHH: accumulation and compact component extraction

[Beomjun Choi, Haslhofer, and Hershkovits, arXiv:1910.02341v1](https://arxiv.org/pdf/1910.02341v1), pages 1–4, were checked, with pages 2–3 also inspected visually. Theorem 1.3 and Corollary 1.4 concern a smooth closed embedded mean-convex surface. Proposition 2.2 uses the compact strictly convex oval slice to obtain a genuine convex component and then spherical extinction centers. The proof of the global theorem identifies an accumulation point as cylindrical. Theorem 1.5 is a local result for inward/outward neck singularities with the corresponding outer/inner flow. Its neck and continuation hypotheses must be retained in broader applications. The candidate does so. The relevant first author is Beomjun Choi, distinct from Kyeongsu Choi in the OWR contribution.

### 3.3 CM: arrival time and actual gradient differentiability

[Colding and Minicozzi, arXiv:1501.07899v3](https://arxiv.org/pdf/1501.07899v3), especially Theorem 0.2, Corollary 1.12, and Proposition 2.2, were checked. The setting is a closed smooth mean-convex initial hypersurface and its compact swept-out domain. Corollary 1.12 supplies C^{1,1} regularity and identifies the singular and critical sets. Proposition 2.2 derives gradient difference quotients and the tangent-cylinder Hessian; pages 7–8 were inspected visually. In R^3 the cylinder gives diag(-1,-1,0), up to rotation, while the sphere gives -I/2. The candidate correctly uses surface dimension two, rather than ambient dimension three, in this normalization. No Hessian-continuity conclusion is imported.

### 3.4 SWX: the extra nondegeneracy condition

[Sun, Wang, and Xue, arXiv:2501.16678v1](https://arxiv.org/pdf/2501.16678v1), introduction, Theorem 1.1(i), and Corollary 1.3 were inspected, including a visual check of page 3. The flow in Theorem 1.1 is a unit-regular cyclic mod-2 Brakke flow on a time interval extending to both sides of the point. Nondegeneracy means the full-rank quadratic normal-form condition stated before the theorem. Part (i) gives a two-sided spacetime neighborhood with no other singularity. A cylindrical tangent alone does not establish this condition. The candidate's Corollary 3.3 is valid with the specified hypotheses, not a universal neck-exclusion theorem. Definitions of nondegeneracy from other papers are not silently substituted.

### 3.5 Construction-route and current-scope sources

- [Angenent, Daskalopoulos, and Sesum, arXiv:2512.05077v2](https://arxiv.org/pdf/2512.05077v2), revised 31 August 2026: Theorems 1.3–1.4 and Section 10, PDF pages 52–54, were checked; pages 4 and 53 were inspected visually. The theorem applies to the stated perturbation families of a 4-peanut. The flow varies with the sequence index. Section 10 starts with members whose first singularity is spherical and uses their earlier convexity. It supplies no simultaneous infinitely many episodes in one fixed flow.
- [Miura, arXiv:1411.6249v4](https://arxiv.org/pdf/1411.6249v4), dated 30 January 2016: pages 1–3, including Theorem 2.1, were checked; page 3 was inspected visually. The initial connected compact axisymmetric hypersurface is smooth except at one point. The exhibited singular epochs accumulate toward the initial time. This is not smooth initial data of the original class.
- [Haslhofer's author manuscript](https://www.math.toronto.edu/roberth/papers/haslhofer_icm2026.pdf) is dated 1 October 2025 on its first page. Pages 15–16 retain Problem 5.5 and the oval/accumulation discussion. The [published ICM 2026 chapter](https://epubs.siam.org/doi/10.1137/25M1803383) was independently checked and still presents this selfsimilarity problem as open. Its basic properties and Theorem 1.1 also support the compact convex evolution and enclosing-sphere normalization used here. This is a bounded literature/status check, not proof of absence of every later or unindexed result.
- [Choi, Du, and Zhu, arXiv:2504.09741v1](https://arxiv.org/pdf/2504.09741v1), pages 1–4: the relevant scope is classification of ancient solutions with specified noncollapsing and cylindrical-asymptotic hypotheses. It does not produce one smooth initial surface realizing an oval as a later-time blowup.
- [Sun and Xue, arXiv:2609.19390v1](https://arxiv.org/pdf/2609.19390v1), pages 1–5: stability and perturbation theorems do not make every existing cylindrical singularity nondegenerate. In particular, the denseness theorem has a type-I hypothesis. This manuscript is not a dependency of the candidate's main theorem. Its arXiv version date is 16 September 2026, while the PDF also prints a manuscript date of 18 September 2026; these dates are not interchangeable.

The long external PDE proofs are imported. No claim is made to have independently reproved the entire peanut perturbation analysis, the arrival-time theorem, Brakke regularity theory, or the nondegenerate-neck isolation theorem. An attempted extra opening of Huisken's 1984 DOI failed; no direct inspection of that original paper is claimed. The verified CHH mechanism and Haslhofer exposition suffice to identify the standard convex-flow dependency actually used.

## Attribution and inspection limits

Kyeongsu Choi's Oberwolfach contribution and Beomjun Choi's later joint work
are distinct sources with distinct first authors. The CHH equivalence, CM
arrival-time regularity/Hessian identification, SWX nondegenerate-neck isolation,
ADS perturbation theorem, Miura example and ancient-solution classifications
retain their primary credit. The deductions assembled in the proof have no
established novelty or priority claim.

SOURCE_METADATA.json preserves all nine historical candidate source identities
and the complete independent audit retrieval and inspection records, including
the failed extra retrieval. The review above retains the manuscript/publication
date distinctions. Edition preparation verified the frozen authored records;
it did not rehash source PDFs,
retrieve sources, inspect source text or conduct a new literature search.
No copied source bodies, extracted text or rendered images are distributed.
