# COMPLETE — fresh source intake and independent scope review

Record 23440119, work Z-23440118, spreadsheet row 83, inventory index 95. Completed 2026-10-25T05:28:52.736166+00:00. Model: GPT-6.1 Sol, Ultra; no child agents. Completion estimate: **100% of this assigned intake/scope task**. This percentage measures work completed, not correctness or novelty.

## Disposition

The public sources have been authenticated and preserved, the complete original manuscript scope has been mapped, the cited problem and principal attributions have been freshly checked, and a scholarly article candidate is held in `content.json`. **This scope lane assigns no mathematical pass and gives no page-promotion or publication permission.** The analytic and adversarial gates remain separate. The original theorem has not been weakened to make a narrower statement pass.

No substantive mismatch was identified between the manuscript's literal claims, its abstract, its stated boundary cases and its cited historical target. This is a scope finding. Polynomial identities and the universal theorem were not independently rerun or certified in this lane. The remaining scientific gate is the fresh mathematical validation of the full original theorem; historical priority, full novelty and worldwide current-open status remain unresolved.

## Public edition and custody

The selected public edition is *A negative-curvature normal barrier on an algebraic cone that is not a hyperbolicity cone*, Alec Kriebel, version 1.0.0, publication date 17 October 2026, DOI [10.5281/zenodo.23440119](https://doi.org/10.5281/zenodo.23440119). The [Zenodo API](https://zenodo.org/api/records/23440119) reports published/done/submitted, open access, preprint, CC BY 4.0. It lists Independent researcher and ORCID 0009-0001-9320-500X. API creation is 2026-10-17T17:44:20.489806+00:00 and modification is 2026-10-17T17:44:21.017669+00:00. These are deposit timestamps, distinct from the selected edition date. Public HTML title/date were cross-checked.

The actual public API response, record page, PDF and ZIP were freshly downloaded. `sources/receipt.json` retains request URLs, final URLs, HTTP status, retrieval times, raw response headers, sizes and hashes. `record-raw.json` preserves the exact API bytes; `record.json` is its separately serialized readable equivalent. Both deposited files match the current API and reconciliation queue:

| Deposited file | Bytes | MD5 | SHA-256 |
| --- | ---: | --- | --- |
| negative-curvature-cone.pdf | 73,062 | c664b4d2cbdf03da6d7f834c472e931a | ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0 |
| negative-curvature-cone-source-and-verification.zip | 134,250 | 23e2b648d17781a14378173566e6fe73 | d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e |

The ZIP was fully inventoried before extraction: 26 regular file members, 280,243 uncompressed bytes, no unsafe absolute/traversal/backslash paths, duplicate paths, links, special files, encryption or nested-archive magic. Safe member-by-member extraction is recorded in `sources/asset-inventory.json`. Its embedded PDF is byte-identical to the standalone PDF. All 25 entries in the deposited `SOURCE_MANIFEST.json` match the extracted bytes; the manifest excludes itself. No submitted programs were run or imported.

Local ignore rules were installed before the first checkpoint: deposited PDFs/ZIP, full support sources, third-party PDFs/text extractions/raw HTML/error responses and renders remain private ignored reading copies under `sources/`. Retained public-source provenance and review files carry checksums and exact extents. No source original was edited. `custody-before-after.json` and `SEAL.json` bind the final report to the preserved authorities.

## Literal claim and boundaries

Theorem 1 is the conjunction of four claims. First, K={(x,y,z)∈ℝ³:x,y,z≥0,xy²−z³≥0} is closed, pointed, convex and has nonempty interior, with homogeneous polynomial defining inequalities. Second, F=−25 log(z(xy²−z³)) is a parameter-100 normal barrier on the complete interior x,y,z>0, xy²>z³. Third, D³F(a)[h,u,u]≤0 for **every** a∈int K, h∈K and u∈ℝ³. Fourth, **no homogeneous polynomial of any degree in three variables** has K as its hyperbolicity cone.

The curvature claim includes h=0, the facet direction t=0, the exceptional t=1 rank-two matrix, and the e_x endpoint covering h_y=0. It does not assert strict definiteness everywhere. Base points on the boundary (s=0 after normalization) are outside the domain. The barrier's finite-boundary blow-up includes the z=0 facet, coordinate edges and origin. The −log z term is substantive; its omitted-term counterexample is a submitted analytic/computational control, not a fresh executed test here.

The proof mechanism is explicit: weighted-geometric-mean concavity; a Hessian norm decomposition and mixed self-concordance estimate scaled by 25; degree-four logarithmic homogeneity; fixed diagonal normalization; conic direction reduction; exact minor/square/endpoint certificates; then boundary divisibility and a nonreal quadratic root pair for every possible interior hyperbolicity direction. The claim is about the original three-dimensional cone, including invertible same-dimensional coordinate changes. Projections and higher-dimensional lifts are not excluded by this statement.

The manuscript gives an existential witness for the original historical question. It does not claim that all regular cones admit such a barrier, that the cone is new, that the parameter is optimal or improved, that the sign-symmetric power cone is handled, or that all exponents are covered. It explicitly disclaims exhaustive literature coverage and first-ever priority. See `claim-boundary-map.json` for claim-by-claim locators and edge cases.

## Fresh primary-source control and credit

[Tunçel's author contribution](https://www.math.uwaterloo.ca/~ltuncel/publications/OWR-2017-14.pdf) and the [official MFO report](https://publications.mfo.de/bitstream/handle/mfo/3578/OWR_2017_14.pdf?isAllowed=y&sequence=1) were independently acquired. The full contribution on printed pp. 797–800 was read; the complete physical page 29, printed 799, was rendered and visually inspected. Its Open Problem 1 is the exact existential algebraic-cone question described above. The historical question's wording does not establish its global current-open status.

The [Nesterov–Tunçel arXiv v1](https://arxiv.org/pdf/1412.1857v1) definitions on pp. 3–4 and §6 match normality and the cone-direction third-derivative convention; §9.2 and the conclusion were also read. The [Dahl–Tunçel–Vandenberghe v2 PDF](https://arxiv.org/pdf/2509.10263v2) and [separate HTML](https://arxiv.org/html/2509.10263v2) §§2.2,3.1,6 were read for the matrix self-concordance convention, directional-gradient concavity and broader universal question. Their date identities remain distinct: arXiv v2 record 12 June 2026; PDF internal revision 16 June; HTML internal revision 24 August. No full-edition identity is inferred.

[Hildebrand's Theorem 3.2, family 5](https://arxiv.org/pdf/1305.4814v1), pp. 4–5, already supplies this cone at p=3,q=3/2,(x1,x2,x3)=(x,z,y). [Roy–Xiao Theorem 2](https://optimization-online.org/wp-content/uploads/2018/01/6441.pdf), p. 3 and proof pp. 8–9, supplies the parameter-3 self-concordant barrier on the same cone. Those credits are explicit in the original manuscript and held candidate. Self-concordance alone does not state the additional mixed sign property; this comparison is not a proof of novel method priority.

A fresh targeted search also revisited the [2026 Hildebrand publisher record](https://link.springer.com/article/10.1007/s10957-026-02986-4) and its related institutional 2024 poster. The publisher abstract and bibliography were read; the journal full text remains a subscription preview. Ordinary [OpenReview prepublication](https://openreview.net/pdf?id=qEnyBmxVzt) retrieval returned HTTP 403 and the web page requested browser verification. No bypass was attempted. The one-page poster was fully read and viewed, but is a distinct work and does not close the journal/prepublication coverage gap. Other sources named in historical support ledgers were not silently counted as independently read. Exact extents, URLs, hashes, failures and gaps are in `primary-read-ledger.json` and acquisition receipts. No claim of exhaustive priority clearance is made.

## Read sequence, disclosure and held content

All five published pages were text-read and visually inspected, and all of `main.tex` was read. The literal claim, scope, mechanism and pending dependencies were sealed in `independent-scope-seal.json` **before** opening detailed submitted historical audit opinions. The manuscript itself incidentally disclosed accompanying AI reviews before that seal. Subsequently all 13 human-authored support text/source files and all metadata/provenance/source ledgers were read. Repetitive machine-generated 791-label result arrays were structurally inspected with all non-repetitive summaries and counts; no line-by-line full-array reading or rerun is claimed. Historical favorable opinions are submission material, not this lane's evidence of a fresh pass. `read-ledger.json` records each of the 26 support members separately.

`content.json` contains the full original one-paragraph abstract, exact TeX in `abstract-source.tex`, original dates and status, literal theorem, mechanism, limitations, primary credits, extensive-AI and unrefereed disclosure, and a passive professional collaboration statement. `follow_up` is null: no exceptionally strong additional question was established by this bounded primary review. Routine exponent variants or parameter optimization are not promoted to research questions solely because the note leaves them untreated. Candidate content is held pending the separate full mathematical gate.

No external individual was contacted and no outreach was prepared. No Git/branch/commit/push, deployment, spreadsheet, shared script/configuration, release or DOI action was performed. All writes are confined to this record's sources and scope review folder.
