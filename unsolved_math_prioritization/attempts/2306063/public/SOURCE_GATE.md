# Source, identity, and scope gate

Checked 2026-10-04 UTC. Numeric identity: 2306063; code AMR-022-6063; queue rank 585.

## Exact target and correction

The primary question is fine-C0 openness of hyperbolic end type for admissible half-strip sewings. The tolerance is a positive **continuous function of x**, not a constant. The recovered prior report abbreviates it as a constant epsilon; the recovered complete problem record and primary source agree on the functional tolerance. This correction is not a change to the original problem, and no historical source record is overwritten.

The admissible competitor class is not assumed differentiable, quasisymmetric, uniformly quasiconformal, or uniquely weldable. Results needing such hypotheses are labeled restricted results. A hyperbolic end is also not the same assertion as the entire surface merely being hyperbolic in another conventional sense.

## Primary evidence checked

1. [Hayman–Lingham, Research Problems in Function Theory, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed pp.140–141, PDF pp.141–142. Both pages were rendered and visually inspected; Problem 6.63 and its update were read. The update reports no progress as of that edition.
2. [Anderson–Barth–Brannan, Research Problems in Complex Analysis (1977)](https://doi.org/10.1112/blms/9.2.129), Problem 6.63 in the original article. Publisher metadata verifies July 1977 and pp.129–162; an indexed scholarly full-text copy corroborates the question. No claim is made that every line of the original article was inspected.
3. [Jenkins, On a Type Problem (1959)](https://doi.org/10.4153/CJM-1959-043-7), pp.427–431, especially the hypotheses on pp.427–428 and the theorem/formula on p.430. Full PDF inspected, with p.430 visually checked. Its derivative-product criterion is sufficient under explicit sewing-chart hypotheses, not a general fine-C0 stability theorem.
4. [Huber, Über eine Vermutung von Vainio (1986)](https://www.math.purdue.edu/~eremenko/Pdf/huber1.pdf), pp.104–106. Its construction forces hyperbolicity under fine approximation; the opposite approximation conjecture is explicitly left open there. Reversing that direction would be invalid.
5. [Vainio, On the type of sewing functions with a singularity (1989)](https://www.acadsci.fi/mathematica/Vol14/vol14pp161-167.pdf), pp.161–167, especially local quasisymmetry/uniqueness and regularity hypotheses. [Properties of real sewing functions (1995)](https://www.acadsci.fi/mathematica/Vol20/vainio.pdf), pp.87–95, especially Section 3. These refine regular type criteria and do not give the target statement in the checked text.
6. [Bishop, Conformal welding and Koebe's theorem (2007)](https://annals.math.princeton.edu/2007/166-3/p01), Theorem 3, Remark 9, and Theorem 25. These supply the published log-singular interval-map construction used in Lemma 5B and the whole-circle welding result whose fixed-side hypothesis obstruction is proved in Lemma 5C.
7. [Preciso, Perturbation Analysis of the Conformal Sewing Problem and Related Problems (1998)](https://www.research.unipd.it/handle/11577/3425905). Institutional abstract only inspected. Its Schauder/Roumieu regularity setting is not treated as the value-only, singular-end target.

Targeted web searches for the exact number, named proposer, half-strip type stability, and singular welding produced no exact full solution. These findings do not prove the problem remains open in all literature as of 2026.

## Repository and corpus provenance

Live reads used main df9f2c05f61cad48f851c2d2ba7a63611a0acfa0, as observed at the start. The selected queue row was queued, 0/5. The selected-ID PR search returned total_count=0 with incomplete_results=false; the live attempts listing, state, and related-target groups had no selected-ID entry. Exact code and sewing/hyperbolic-or-strip searches in the recovered corpus identified only the selected record. Search/index omissions and later concurrent writes remain possible; a fresh duplicate and base-head check is required before publication.

The recovered research-results corpus exactly matches the repository manifest. The recovered problems corpus does **not**: observed 69,291,427 bytes versus manifest 68,931,837. Its selected record was independently matched to the primary statement. Exact pinned provenance of the recovered problems snapshot is not claimed. `SOURCE_MANIFEST.json` records both hashes rather than concealing the mismatch.

Catalogue direct request: HTTP 403. Web tool also reported inaccessible. No catalogue text was invented or treated as current evidence.

## Dependencies and result boundary

The package uses standard annular uniformization/extremal-length duality, quasiconformal modulus distortion, local quasisymmetric sewing/removability and ACL gluing, and basic logarithmic-capacity facts. The sole non-elementary construction in Lemma 5B is Bishop's published existence of log-singular interval homeomorphisms. These are external theorem dependencies, not formally verified within the supplied Python controls.

Full success would require an epsilon(x) proof for every admissible competitor at every hyperbolic alpha, or one fixed hyperbolic alpha together with an admissible parabolic competitor for every epsilon(x). Neither artifact has been produced. Status: unsolved, 5/5.

## Rights and release contents

Sources were downloaded only for scholarly inspection. All PDFs, source-page images, raw corpus, selected raw records, connector responses, and coordination data remain outside the public package. Public artifacts contain original exposition, bibliographic links, short factual descriptions, checksums, and reproducible code. No source PDF or bulk corpus is to be redistributed in this release.
