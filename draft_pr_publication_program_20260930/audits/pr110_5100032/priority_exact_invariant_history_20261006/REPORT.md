# PR110: independent exact-invariant historical priority audit

Audit cutoff: **2026-10-06**. Family: exact k603, source revisions, source-author updates, direct follow-ups and current citation discovery. This is a new independent review of the nonempty inherited triage. No other fresh priority-family reports were consulted. No outreach, paper preparation, Git mutation or publication was performed.

## Conclusion

**No earlier full proof or rigorously covering theorem for the literal ordinary-distance k603 claim was located in this family.** The strongest supported candidate contribution is the all-period, per-edge focal-distance difference identity and its closure telescope in the authenticated original proof. The inspected neighboring proofs do not establish this conclusion by substitution. The numerical observation itself is prior work and must be credited to Reznik, Garcia and Koiller.

This is a bounded literature finding, not an absolute first-in-history claim. It does **not** justify reclassification as `already_solved` on the evidence found here. It also does not, by itself, authorize publication or certify that every relevant source was read. The final published 2021 IMPA book and the source author's experimental video remain specific unread items; the book gap is partly reduced by authenticated author-source review, as detailed below. That gap does not erase the positive bounded substantive novelty assessment; it prevents an unqualified exclusion of the final book. Root must combine this report with the independent general-mechanism and modern-literature families and fresh adjudication before deciding priority clearance.

## Authenticated target and what would defeat novelty

PR head: `3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35`. Original `PROOF.md`: 6,990 bytes, SHA256 `8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d`. The root mathematical gate was read and respected: source and mathematics cleared; priority not cleared; original effort 2/5; new central-proof search turns 0. This family adds no proof-search turn.

For an outer ellipse with semiaxes a>b>0 and a fixed strictly nested confocal elliptical caustic 0<lambda<b², let Q(f,i) be the intersection of the supporting lines through consecutive billiard vertices perpendicular to their displacement from focus f. Let q(f,i)=|Q(f,i)-f| be its ordinary positive Euclidean norm. The claim is

    Σ q(f+,i) = Σ q(f-,i).

It covers every regular closed orbit, every admissible period and winding, stars, reversal and repeated traversal. It uses the original polygon, with no prime. Hyperbolic caustics and degenerate two-bounce limits are outside the target. Neither individual sum is asserted constant along a Poncelet family.

A defeating prior result must prove this equality in that scope, or have an explicit mathematically valid implication with the same construction, norm, branch and all-period coverage. A low-N computation, even-period central symmetry, a signed-length identity, a focus-inversive perimeter, an antipedal centroid, an area product, or a primed outer-polygon invariant is insufficient without that implication. Those distinctions were checked at the theorem level rather than inferred from keyword absence.

The authenticated proof's substantive candidate is its fixed-caustic identity

    q+ - q- = Gamma (y_next-y),
    Gamma = c/(ab sqrt(lambda))[-a²+b² lambda/(b²-lambda)].

Ordinary-norm sign control is part of the proof. The all-N conclusion follows from polygonal closure without a parity restriction. A generic antipedal distance formula or a generic telescoping idea is not claimed new by this review.

## Exact historical source and present revision check

The primary [arXiv source](https://arxiv.org/abs/2004.12497) is still **v11, revised 29 October 2020**, at this audit cutoff. Its recorded sequence is v1 26 April, v2 28 April, v3 30 April, v4 4 May, v5 24 June, v6 5 July, v7 24 August, v8 10 October, v9 21 October, v10 25 October and v11 29 October 2020. No later revision appears on the current canonical submission history. This verifies the current revision endpoint; it is not a full comparison of the bodies of v1–v10, which were not retrieved in this family.

Fresh extractions of both root-supplied primary PDFs were made. Their input pins agree with the root pin file: arXiv v11 SHA256 `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`; published companion SHA256 `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`.

In v11 §§3.5 and 3.7 and Table7, q* is explicitly the focus-to-antipedal-vertex norm, and k603 is the ratio of the two sums, value1, allN, discovery date May2020, proof entry a question mark. The published [*Fifty New Invariants of N-Periodics in the Elliptic Billiard*](https://doi.org/10.1007/s40598-021-00174-y), Arnold Mathematical Journal7 (2021),341–355, §3.7 and Table7 at p349, retains that exact k603 and unproved designation. This is strong historical evidence that the source authors had reported a conjectural observation, **not a certificate that the problem remained unproved in October2026**.

The inherited report was nonempty and explicitly open triage; its three immediate follow-up identifiers were independently retrieved and inspected here. Its earlier no-proof-found statement was not adopted as a finished current priority review.

## Follow-up theorem comparisons

| Primary source inspected | Actual result and scope | Why it does not cover literal k603 |
|---|---|---|
| [*Exploring self-intersected N-periodics in the elliptic billiard*](https://arxiv.org/abs/2011.06640), v3,19January2021; also [published2022](https://doi.org/10.33039/ami.2022.02.001),49–75 | Explicit low-period simple and self-intersected configurations and a selected invariant table. Published Table1 enumerates k101–k119 and selected k802–k807. | It does not list k603. Main low-N formulas, including inverse-focal quantities, give no general-N ordinary-antipedal norm equality. Some bowtie/hyperbolic examples are outside the target. |
| [*The Talented Mr. Inversive Triangle in the Elliptic Billiard*](https://arxiv.org/abs/2012.03020), v2,13July2021; [journal DOI](https://doi.org/10.1007/s40879-021-00489-2) | Triangular inverse polygons and invariants of reciprocals of focus-to-original-vertex distances and inverse perimeters. | Inversion sends a vertex to rho²(P-f)/|P-f|². It is not the intersection of endpoint-perpendicular antipedal lines. A sum of inverse focal radii or inverse side lengths does not equal the target sum without an additional proof, absent in the inspected main results. |
| [*New Invariants of Poncelet-Jacobi Bicentric Polygons*](https://arxiv.org/abs/2103.11260), v3,13July2021; [published DOI](https://doi.org/10.1007/s40598-021-00188-6) | Sum-of-cosines and limiting-point pedal perimeter results; corollary gives focus-inversive perimeter. The proof uses polarity between bicentric and elliptic families. | The perimeter is a sum of **side lengths** of a pedal or inverse polygon, not the distances from a focus to original antipedal vertices. Polarity does not preserve ordinary Euclidean norms. Signed hyperbolic perimeter conventions cannot substitute for positive elliptical focal q*. |
| [*Average Elliptic Billiard Invariants with Spatial Integrals*](https://arxiv.org/abs/2102.10899), v1,22February2021 | Weighted spatial averages of perimeter, angle cosines and the geometric mean of outer cosines. The author ledger lists the related2023 journal paper as *Estimating Elliptic Billiard Invariants with Spatial Integrals*. | Its declared examined quantities are not k603. Numerical matching of averages does not prove the focal-norm equality. The final2023 journal body was not inspected; this row is explicitly an arXiv-v1 main-result comparison. |
| [*Exploring the Dynamics of the Circumcenter Map*](https://arxiv.org/abs/2202.02551), v3,14May2022 | Review of Johnson and Stewart polygon-map results; Corollary1 identifies circumcenter polygon as a half-sized antipedal about its reference point. | This supplies a useful exact alias: q*=2 times the circumradius of triangle(f,P_i,P_next). The iteration/similarity theorem supplies no equality of sums for the two ellipse foci. Searches of that circumradius alias found no covering result. The classical map construction is prior; the target metric trace identity is not supplied. |

Main theorem/proof reading boundaries and uninspected appendices are enumerated in `SOURCE_COVERAGE.json`. Machine screening covered complete extracted bodies but is not represented as full line-by-line reading of each body.

## Source-author repositories, ledger, and the IMPA book gap

The [source author's experimental ledger](https://dan-reznik.github.io/Elliptical-Billiards-Triangular-Orbits/videos.html) explicitly lists the equal focal antipedal distance-sum experiment for N=3,4,5,6 and links [its video](https://youtu.be/6F7Y3UKJzdk). The ledger's displayed update is20February2021. The linked video itself was **not watched or transcribed**; no claim about its complete contents is made. The 2021 published question mark reduces, but does not logically eliminate, the possibility of a proof in accompanying material.

Current read-only GitHub metadata and a complete, nontruncated 507-entry tree inventory of the author's experimental repository were obtained. The specifically named pedal/antipedal notebooks are for **3-periodics**. Their bodies were not executed or inspected; filenames do not prove absence of an all-N argument. The repository's last push metadata is22April2021. Repository update timestamps were not confused with dates of new mathematical publication.

The [author's2022–present publication ledger](https://ronaldo.ime.ufg.br/p/59582-artigos-cientificos-2022-atual) was read in full; its displayed update is17February2026. No item named an exact k603 resolution. A finite author ledger is neither guaranteed comprehensive nor current through October, so current web and citation checks supplemented it.

The ledger's2021 book listing uses *Discovering Poncelet Invariants in the Plane*. The official [IMPA preview](https://coloquio33.impa.br/pdf/33CBM06-eBook-preview.pdf) identifies *Poncelet Surprises in the Euclidean Plane*, first printing July2021, ISBN978-65-89124-43-6. The retrieved official file is **15pages, not the complete book**. Its actual `pdfinfo` and extraction receipts are preserved. The plausible full URL returnedHTTP404. The author's repository compiled PDF,935,414bytes, matches Git blob `3c3d10637894bf2275e282d9c649054adf0b0581` but fails `pdftotext` with missing trailer/xref; this is an actual invalid/truncated repository blob, not a successfully read book.

To reduce that gap, the [author's book repository](https://github.com/dan-reznik/33CBM06-IMPA-Garcia-Reznik) was independently inventoried and pinned at commit `0b5b417fe2ba3185087979749bc8bcf8c702315d`, dated7June2021, tree `a63f06d0de59d16fdcae2564438f1ec58b1a0b55`. The pinned archive yielded145 `.tex`, `.bib` and `.md` files, **every selected file matched its Git blob OID**. Complete source bodies remain private. Exact/semantic terms were searched globally; all numeric603 false positives were inspected and are bibliography identifiers or drawing coordinates. The billiard-invariant chapter was read in full; the antipedal hits concern definitions, low-N triangle-centroid/area matters and interfaces. No general k603 proof was located in that author snapshot.

**Essential unread boundary:** the June source snapshot is not certified byte- or content-equivalent to the final July printed book. An addition between those versions cannot be excluded. The final book cannot honestly be marked fully read. This is a specific limitation for root's priority decision, not grounds for asserting `already_solved`.

## Current2026 primary neighbors and citation discovery

The current [EulerSolve index](https://eulersolve.org/) lists20 AMR-050 papers in its retrieved body; AMR-050-0032 is absent, and the exact prospective URL returnedHTTP404. This is merely a ledger observation, not proof that no unindexed or external paper exists. The three closest public primary notes were downloaded and read completely:

| Primary note, manuscript date, DOI | Earlier result mapping |
|---|---|
| *Original Antipedal Centroids in Elliptic Billiards*, Alper Ferudun,2October2026, [DOI10.5281/zenodo.23092466](https://doi.org/10.5281/zenodo.23092466) | k405, sums of antipedal **vectors**/centroids for even least period. It does use original endpoint antipedal intersection algebra, but it supplies no equality of the two sums of norms for allN. Vector trace cancellation does not imply norm trace cancellation. |
| *Stationary Focal Antipedal Centroids for Even Elliptic Billiard Periods*,1October2026, [DOI10.5281/zenodo.23071366](https://doi.org/10.5281/zenodo.23071366) | k407, antipedals of the **outer tangent polygon**, even least period. Wrong parent polygon and functional for k603. |
| *Focal Pedal-Antipedal Area Products in Elliptic Billiards*,1October2026, [DOI10.5281/zenodo.23079799](https://doi.org/10.5281/zenodo.23079799) | k403,b, signed same-focus pedal/antipedal **area product**, least period divisible by4. Its Jacobi quarter-period and even-area-product mechanism does not establish arbitraryN ordinary focal norms. |

These notes are genuine current public neighboring manuscripts and cannot be ignored because they appeared after the older survey. None is an earlier full solution to the audited exact statement. Their own priority qualifications do not waive this project's priority requirement.

OpenAlex was used **only for discovery metadata**, not as mathematical evidence. The retrieved cited-by filter for the published source returned17 records, all17 retained in the private metadata file and enumerated in the public coverage file. This is one finite index response, with duplicates/version effects and indexing delay possible. It is not an exhaustive citation network.

Two late citing sources were additionally checked against primary bodies. [*Parable of the Parabola*](https://arxiv.org/abs/2502.08656), v2,29May2025, [journal DOI10.1016/j.exmath.2025.125717](https://doi.org/10.1016/j.exmath.2025.125717), explicitly restricts its main discussion to triangles/quadrilaterals between a **circle and parabola**. Its introduction does not claim all-period focal antipedal sums. [*When Grünbaum meets Poncelet*](https://doi.org/10.1017/fms.2026.10254), Forum of Mathematics,Sigma14:e104 (2026), published14July2026, proves movable incidence configurations and join/meet operator identities. Its abstract/main statements and §§3.3.1 and3.3.3 were directly read: the confocal billiard discussion proves index-shift/incidence relations, not an ordinary-distance trace. The Chasles quadrilateral discussion warns about improperly formulated confocal/incircle statements; none is substituted for a proof of k603. Full extracted bodies were term-screened, but unread sections remain unread.

## Novelty assessment, required actions and honest uncertainty

There is substantive evidence for treating the candidate as an all-period proof contribution: the precise source statement was reported unproved in2020/2021; no subsequent source revision carries a proof; immediate follow-ups prove different observables; the exact circumradius alias does not reveal a covering result; current2026 antipedal neighbors have explicit functional/scope mismatches. Unlike an empty keyword search, these checks engage actual primary theorem statements and constructions.

The observation, the antipedal construction, elementary distance/circumcenter geometry, and even-period symmetry are prior ingredients. The defensible candidate novelty is the **general positive-distance per-edge reduction and all-N closure proof**, conditional on the finite audit and root's other independent families. A future note should say it proves the k603 observation of Reznik–Garcia–Koiller, acknowledge related ingredients, date its bounded literature search, and avoid claiming discovery of the observation or absolute priority.

Required before root calls this family's source coverage unrestricted: either obtain/read the final2021 book or explicitly retain the final-book version limitation. If root requires complete current priority for every named potentially relevant body, this report leaves that criterion unresolved. The experimental video/notebook bodies are also unread; their ledger/filenames support discovery attribution, not a negative theorem audit. No human contact or outreach draft is needed or authorized.

No identified earlier full covering result requires closure of PR110. No publication approval is given here. `VERDICT.json` keeps family-level priority clearance false and records both the positive bounded novelty evidence and these unread gaps.

## Custody and reproducibility

`INPUT_PINS.json`, `PRIVATE_SOURCE_PINS.json`, `IMPA_AUTHOR_SOURCE_CUSTODY.json`, `QUERY_LOG.json` and `SOURCE_COVERAGE.json` preserve authentication, discovery and reading limits. CLI downloads/extractions have actual argv/cwd, recorder/child PID, UTC endpoints, exit codes and complete stdout/stderr byte hashes under `actual_operations/`. A curl exit0 is not equated withHTTP200:404/500 responses and extraction failure are retained. One accidental no-op labelled `screen_primary_exact_terms_final` actually ran `/usr/bin/true`; it is not screening evidence. The real metadata-only whole-private-body screen is `screen_and_pin_private_final`.

Browser search tools do not expose an OS PID or an exact per-query UTC; `QUERY_LOG.json` records the actual calendar retrieval date and does not invent those values. Tool output truncations were addressed by rereading decisive theorem sections individually. Full extracted bodies, copyrighted PDFs, HTML/API bodies, invalid responses and book sources reside only in `private_sources/` or `private_review_materials/` and are excluded from the sealed public payload. The public files contain metadata, original audit analysis and minimal identifiers, not redistributed primary source bodies.

`OUTPUT_MANIFEST.json` and `SEAL_RECEIPT.json` record actual sealer PID/UTC and all public payload hashes. Their construction excludes private material and the seal operation's own evolving receipts; this avoids a self-referential manifest. The final seal is an audit artifact, not a Zenodo upload or publishing authorization.
