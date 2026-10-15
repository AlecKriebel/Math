# Sources, public identity metadata, and inspection limits

All dates below are UTC. No source PDF, extracted source text, or dataset records are distributed. The following hashes and byte counts identify public sources only, not excluded operational artifacts.

## Signed degree-choosability

Thomas Schweser and Michael Stiebitz, *Degree choosable signed graphs*, arXiv:1507.04569v1, submitted 16 July 2015 at 13:42:15 UTC.

- [Abstract and version](https://arxiv.org/abs/1507.04569v1)
- [Version-specific primary HTML](https://arxiv.org/html/1507.04569v1)
- [Version-specific PDF](https://arxiv.org/pdf/1507.04569v1): 21 pages, 202,056 bytes; SHA-256 `727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`
- Journal identity: *Discrete Mathematics* 340(5), 882–891 (2017); [DOI 10.1016/j.disc.2017.01.007](https://doi.org/10.1016/j.disc.2017.01.007), [publisher record](https://www.sciencedirect.com/science/article/pii/S0012365X17300079)

The exact dependency is Theorem 2.1(a),(e) in arXiv v1, with finite loopless signed multigraphs, multiplicity-counted degrees, integer lists, the zero-free eight-color palette, and the stated brick classes. The complete dependency application appears in SIGNED_DEPENDENCY_AUDIT.md. Conventions occur on pages 2–4, bricks on page 5, list definitions and Theorem 1.7 on pages 5–6, the uncolorable-pair definition and Theorem 2.1(a) on page 7, part (e) on page 8, its proof on pages 8–12, and Theorem 1.7's proof and Corollary 2.5 on page 14.

The dependency inspection read the complete 21-page primary manuscript, including the relevant proof, on 12 October 2026. The full-packet acceptance separately rechecked the conventions and exact theorem clauses, and independently checked the reduction. Reading the manuscript is not an independent reproof of its theorem. The publisher search result established the journal bibliographic identity; direct publisher/DOI access failed, so neither journal full text nor journal theorem numbering was checked.

### Public retrieval history on 12 October 2026

- 09:30:26 UTC: [web](https://arxiv.org/abs/1507.04569). Abstract and version identity retrieved.
- 09:30:26 UTC: [web](https://arxiv.org/pdf/1507.04569). Full 21-page primary PDF text available; content identifies v1.
- 09:31:11 UTC: [web](https://arxiv.org/abs/1507.04569v1). Version-specific submission metadata verified.
- 09:31:11 UTC: [web](https://arxiv.org/html/1507.04569v1). Version-specific primary full text retrieved.
- 09:31:23 UTC: [HTTP download](https://arxiv.org/pdf/1507.04569v1). 202056-byte PDF downloaded; SHA-256 recorded; all pages text-extracted locally.
- 09:31:23 UTC: [publisher search result](https://www.sciencedirect.com/science/article/pii/S0012365X17300079). Journal bibliographic identity verified; full text not retrieved.
- 09:31:33 UTC: [web direct open](https://www.sciencedirect.com/science/article/pii/S0012365X17300079). Internal tool error; no full-text inspection claimed.
- 09:32:23 UTC: [web direct open](https://doi.org/10.1016/j.disc.2017.01.007). URL inaccessible via tool; no full-text inspection claimed.

The earlier proof-author check had inspected primary HTML definitions and theorem statements without downloading the PDF; the later dependency audit downloaded and read it in full. An earlier direct publisher request returned HTTP 403; the later direct opens failed at the tool level. These distinct events do not establish journal full-text inspection. Three v1 typographical slips and why they do not affect the imported clauses are explicitly discussed in SIGNED_DEPENDENCY_AUDIT.md.

## Clebsch target and the global cut bound

Matt DeVos and Robert Šámal, *High-girth cubic graphs are homomorphic to the Clebsch graph*.

- [arXiv:math/0602580v2](https://arxiv.org/abs/math/0602580v2), identified as 23 October 2009
- [Version-specific PDF](https://arxiv.org/pdf/math/0602580v2): 284,638 bytes; SHA-256 `aaefc77c1421e5c56d733d12561e198333b73e612c10135aa1361bf462d2ccf2`
- [Public author manuscript](https://iuuk.mff.cuni.cz/~samal/papers/clebsch/clebsch.pdf)
- [Publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.20580)

The original target and standard cut-complement equivalences are cited by Proposition 1.1/3.2 and Conjecture 1.4 in the identified arXiv version. The retained primary source and the public author manuscript/publisher abstract were inspected for formulation and attribution, with the latter public URLs checked on 12 October 2026. The currently served author PDF is not claimed byte-identical to the identified arXiv-v2 PDF; reference numbering differs across versions.

The introduction gives the 4/5 edge-cut theorem for triangle-free maximum-degree-three graphs, attributing the historical results to Hopkins–Staton and Bondy–Locke. The maximum-degree-three formulation is attributed there to Bondy–Locke; no connectedness or bridgelessness restriction is introduced. For cubic graphs, |E|=3n/2 makes the corresponding global complement bound 3n/10. No full original proof of that cut theorem or of the high-girth homomorphism theorem was independently audited here.

J. Adrian Bondy and Stephen C. Locke, *Largest bipartite subgraphs in triangle-free graphs with maximum degree three*, Journal of Graph Theory 10 (1986), no. 4, 477–504. Bibliographic identity was checked in the DeVos–Šámal references, not against a separately retrieved complete original proof.

## Public catalog metadata for bounded corroboration

The [House of Graphs connected cubic catalog](https://houseofgraphs.org/Cubic) supplied already available inputs at orders 6, 8, 10, 12, and 14. Exact local bytes and their public identity metadata were checked. Completeness of catalog generation and nonisomorphism are not certified, and neither property is needed by any proof in this edition.

- Order 6: [public graph6 input](https://houseofgraphs.org/data/cubics/Generated_graphs.06.04.g6), 1 records, 5 bytes; SHA-256 `71f49f06c24df520ed960e6c438423ac3bc1bc06f89ba390f8b5e7ed0d9f36d4`.
- Order 8: [public graph6 input](https://houseofgraphs.org/data/cubics/Generated_graphs.08.04.g6), 2 records, 14 bytes; SHA-256 `6fea93e58c75b760f24e58ea93673a627075c42d7ef31f1125bfb25e8dec5ee4`.
- Order 10: [public graph6 input](https://houseofgraphs.org/data/cubics/Generated_graphs.10.04.g6), 6 records, 60 bytes; SHA-256 `01324766dc1dfd3b64a9ab130f4162684e9df86f7fee664e6c904e0471eff285`.
- Order 12: [public graph6 input](https://houseofgraphs.org/data/cubics/Generated_graphs.12.04.g6), 22 records, 286 bytes; SHA-256 `3b231b32b339de0a94f8c8237d58aeaac5a2844f8e6ff8c6c666d83b2f9e4803`.
- Order 14: [public graph6 input](https://houseofgraphs.org/data/cubics/Generated_graphs.14.04.g6), 110 records, 1980 bytes; SHA-256 `6eb7b8060b76eed5c4473bbdd8af330baa9dcbe541a59808691d0941fdd8fe99`.

All 141 supplied records were used only for bounded corroboration. The record contents are excluded. The programs, raw authored sample collections, runtime artifacts, and original proof/audit-file identities used during preparation are also excluded; their identities are not substituted for distributed source content.

## Literature scope

The elementary grid extension is proved in full and does not depend on an absolute-retract classification. Such literature was consulted during development but is not a premise. Public source inspection here establishes the identified theorem contract, formulation, bibliography, and bounded inspection history. It is not an exhaustive literature survey, novelty certification, or a claim about the present resolution status of the full conjecture in all literature.
