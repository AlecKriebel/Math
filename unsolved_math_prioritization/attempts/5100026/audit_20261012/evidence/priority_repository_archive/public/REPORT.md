# Independent repository and archive priority audit: PR259 / 5100026 / k407

**Disposition: exact earlier-dated deposited solution located; submitted theorem's correctness and historical novelty are separate questions.** This audit found Alper Ferudun's [Stationary Focal Antipedal Centroids for Even Elliptic Billiard Periods](https://eulersolve.org/papers/amr-050-0026/), bound to [Zenodo record 23071366](https://zenodo.org/records/23071366), DOI [10.5281/zenodo.23071366](https://doi.org/10.5281/zenodo.23071366). Its full PDF and LaTeX were examined before this disposition. The matching construction uses the original focus, genuine outer tangent intersections, arithmetic vertex mean and every even least period, including stars. It proves regularity, phase constancy and axial location; focus reversal follows from its pair formula. The four-period zero value also follows by specialization.

## Scope and proof assessment

The audited target fixes a noncircular original ellipse, a strictly nested nondegenerate confocal elliptical caustic, and a least even period N>=4. Each antipedal sideline passes through the corresponding actual outer tangent intersection and is perpendicular to the vector to an original-ellipse focus. The statistic is the arithmetic mean of consecutive antipedal-line intersections. Self-intersection and zero signed area do not change this statistic.

The deposited argument uses an opposite-edge reduction, affine normalization of the outer conic to a circle, and a symmetric complex-bilinear trace on a compact Poncelet curve. I independently checked the pair identities, curve discriminant, finite-intersection determinant, exceptional infinity charts, global step extension, simultaneous-pole grouping and conjugation argument. No unresolved proof gap was found in this scope. [Own exact algebra replay](check_algebra.py) and [receipt](ALGEBRA_RECEIPT.json) check eight polynomial identities using rational arithmetic; they supplement the analytic inspection.

For least even N, coprime winding is odd and the half-orbit vertices are opposite. The [Stachel primary body](https://arxiv.org/pdf/2105.03624v2), Theorem 2 and pp10–12, supplies the parameter step and the needed sn/cn sign changes. Neither it nor a padded odd cycle supplies a new even primitive family.

Both original Table 5 cells literally say “even” (v11) / “Even” (final). Neither says least. Both k407 proof cells are question marks. The least-period restriction is a qualification required to make the target true, not a transcription of a source word. The source lists original-focus outer-antipedal vertex means separately from k405 and the N=4 k406,b case. Primary PDFs: [arXiv v11](https://arxiv.org/pdf/2004.12497v11), Section3.5/Table5, pp6–7; [final paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), pp347–348.

## File-to-record and date evidence

The deposited PDF is **main.pdf**, 82,690 bytes, SHA256 `317178430532655300d12aff19391751a3dc32ab6913b5062a4df803d56355b6`. Its actual MD5 equals the record MD5. The source ZIP and verification attachment also match the record sizes/checksums; all three are byte-for-byte identical to the website copies. [DEPOSIT_ASSOCIATION.json](DEPOSIT_ASSOCIATION.json) records exact file keys, record-owned download URLs, MD5/SHA256, sizes, DOI and concept DOI. Current version listing contains one record.

| Evidence | Recorded value | What it supports |
|---|---|---|
| Website and Zenodo publication date | 2026-09-30 | Present publication metadata |
| PDF and deposited main.tex printed date | 1 October 2026 | Present manuscript dating, one day later |
| Zenodo creation / modification UTC | 2026-09-30T22:04:12.260164 / 22:04:12.820855 | Present repository clocks |
| DataCite issued date | 2026-09-30 | Present DOI metadata |
| DataCite creation / registration UTC | 2026-09-30T22:04:13Z | DOI infrastructure clocks |
| Successful record-owned attachment GETs | 2026-10-12 | Observed accessibility of these exact bytes |
| Wayback CDX, landing page and record | Empty result arrays | No independent earlier capture obtained |

These establish a currently accessible exact solution with recorded dates earlier than this review and nominally before the submitted research log's 2026-10-01 source gate. They do **not** establish absolute first visibility of these exact bytes, resolve the printed-date discrepancy, or order private discoveries. The authenticated submitted turn ledger lacks an exact timestamp for the substantive proof turn. No causal claim is justified.

## Other primary bodies and exact non-implications

| Body actually inspected | Result and reason it does not already supply the target |
|---|---|
| [Akopyan–Schwartz–Tabachnikov, 2001.02934v2](https://arxiv.org/pdf/2001.02934v2), complete 12-page body | Theorems5/8 fix circle/concentric-ellipse adjacent or diagonal dot-product sums. My inference from the proof: its pole cancellation can be adapted to the needed bilinear trace. The focal outer-antipedal pair reduction remains necessary and is absent. This is established machinery, not a full explicit k407 solution. |
| [Schwartz–Tabachnikov, 1607.04766v1](https://arxiv.org/pdf/1607.04766v1), complete 14-page body | Vertex/area centroid loci of actual Poncelet polygons and a compact-curve method. The target antipedal was not shown to be such a Poncelet polygon. |
| [Bialy–Tabachnikov, NSF PAR10408490](https://par.nsf.gov/servlets/purl/10408490), Theorem4.1 and its proof | The stationary mean is of perpendicular feet onto original-ellipse tangents. Feet differ from intersections of perpendicular sidelines at outer vertices. |
| [Chavez-Caliz, 2004.05404](https://arxiv.org/pdf/2004.05404), definitions and Theorems2/3/6 including proof | Lamina/circumcenter-of-mass and even outer-polygon area invariants; no target arithmetic antipedal vertex mean. |
| [McDonald–Garcia–Reznik, 2202.02551](https://arxiv.org/pdf/2202.02551), definitions and Corollary1 | Circumcenter-map polygons are homothetic to antipedals about the reference point. This renames an equivalent construction but supplies no phase constancy for the required confocal family. |
| [Roitman–Garcia–Reznik, final bicentric paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), Theorems1/2 and Corollary1 proofs | Angle sums, limiting-point pedal perimeters and focal inversive perimeters. Its N=6 antipedal-video entry is experimental and concerns area, not this proof. |
| [Ferudun, AMR-050-0025](https://eulersolve.org/papers/amr-050-0025/), theorem and rectangle proof | N=4 only: focal vertex mean zero and area mean F/3. It explicitly separates k407. |
| [Ferudun, AMR-050-0023](https://eulersolve.org/papers/amr-050-0023/), theorem and construction | Antipedal of the original billiard polygon, k405, rather than its outer tangent polygon. |
| [Mitrea, 1008.0110v1](https://arxiv.org/pdf/1008.0110v1), definitions/Theorems1.1 and1.4 | Triangle pedal/antipedal area formulas; no even-period family or vertex-mean claim. |

This classification uses actual body statements and constructions. Numeric examples, metadata labels and search snippets were never accepted as a complete proof. A later aiXiv entry concerning a focal-antipedal distance sum was retained only as a metadata lead; its own-author paper and prior-case audit were not opened before freezing independence.

## Search coverage, remaining gap and release boundary

[SEARCH_LEDGER.json](SEARCH_LEDGER.json) records exact queries, archive requests, outcomes and limitations. Search families covered arXiv, Zenodo, HAL, NSF PAR, institutional repositories, OSF, Figshare, Preprints, aiXiv, Internet Archive, viXra and later literature under centroid, center-of-mass, bilinear trace, tangential/outer polygon and circumcenter-map terminology.

The exact positive deposit is decisive even though no search can certify nonexistence. General Zenodo search repeatedly returned504; the arXiv export query timed out, while its HTML all-field search succeeded; the Preprints lead body returned403. HAL returned zero antipedal records. Several full texts have no antipedal abstract keyword, so keyword-only negatives are intrinsically weak. Empty Wayback arrays prove no visibility date.

The strongest verified bibliographic result is this exact earlier-dated public deposit plus a complete matching proof. The unresolved gap is historical visibility and causal order, together with inherently bounded archive coverage. Treat any claim that PR259 is the first resolution of k407 as **unsupported pending correction and attribution**. This audit does not accuse copying or certify anyone's absolute priority.

Only derived artifacts in this public folder belong in the public packet. Downloaded PDFs, full texts, HTML, ZIPs, raw search outputs and source extractions remain in `../private_reading/` and are excluded. Their hashes, byte sizes, retrieval dates and source URLs are preserved as metadata in [SOURCE_PINS.json](SOURCE_PINS.json). No external communication, provider write, Git action, release or DOI mutation occurred. Independent search/analysis was frozen before any sibling-priority comparison; see [ANALYSIS_FREEZE.json](ANALYSIS_FREEZE.json).
