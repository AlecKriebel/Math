# Source and literature audit

## Original statement

[Oberwolfach Report 31/2012, full PDF](https://ems.press/doi/pdf/10.4171/OWR/2012/31), *Learning Theory and Approximation*, 1895–1948. Ulrike von Luxburg's contribution occupies pp. 1914–1915; its setting and both questions were visually verified on p. 1914. The report says undirected and unweighted. The edge rule gives the union-symmetrization of directed neighbor relations. The qualitative density regularity, growth of k, loss, and convergence mode are not formalized. The imported citation's 2013 date does not match the report identifier and header.

## Later primary sources, all recovered in full

- [von Luxburg–Alamgir, NIPS 2013](https://proceedings.neurips.cc/paper_files/paper/2013/file/eae27d77ca20db309e056e3d2dcd7d69-Paper.pdf), nine pages. Section 2 defines directed observations and connected-core/positive-density assumptions. Theorem 4 concerns the preceding hypothetical geometric statistic. Section 5 explicitly withholds a proof of the final graph-only statistic, while §7 sketches direction recovery using common neighbors. The affirmative abstract does not erase these qualifications.
- [Terada–von Luxburg, ICML 2014](https://proceedings.mlr.press/v32/terada14.pdf), nine pages. Theorem 3 and Proposition 4 use directed neighborhoods and compact connected convex full-dimensional support, smooth boundary and positive C¹ density. The existence of a global optimum in the asserted theorem is not replaced here by an assertion that a numerical local optimizer finds it. This paper is credited but its published consistency proof is not newly certified by this package.
- [Hashimoto–Sun–Jaakkola, AISTATS 2015](https://proceedings.mlr.press/v38/hashimoto15.pdf), nine pages. Theorem 2.1, Corollaries 2.2–2.3 and all of condition (⋆) were inspected. The stationary equicontinuity condition is an explicit hypothesis, conjectured automatic. The paper explicitly limits disconnected calibration to each component. The original undirected adjacency is not silently promoted to its directed input.
- [Cucuringu–Woodworth, arXiv:1504.00722v2](https://arxiv.org/abs/1504.00722v2), full 2015 author manuscript. It uses directed ordinal constraints, with symmetrization only at a clustering stage. Its scalable synchronization and empirical density results are credited; the observations and statistical guarantees are not expanded.

Bounded searches through 30 September 2026 for undirected kNN density recovery, ordinal embedding and directed metric recovery did not establish a complete current theorem for the exact original observation model. No claim of exhaustive literature coverage is made. Unrelated spectral-density estimation on abstract graphs was excluded: that uses a different meaning of density.

The two-component obstruction is an explicit proof of a standard identifiability issue, not a novelty claim. The source's undefined phrase about a nice density could implicitly intend connected support. For that reason the campaign disposition remains unsolved rather than promoting the disconnected example to a full answer.

Source PDFs, extracted text and page images are retained for checking, but are not included in the repository package. The pinned numeric record and the absent exact-code report entry are represented in `source_record.json` and `prior_imported_report.json`, respectively.
