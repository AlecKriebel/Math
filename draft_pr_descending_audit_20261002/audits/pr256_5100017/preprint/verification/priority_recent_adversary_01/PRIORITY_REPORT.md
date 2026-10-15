# Independent recent-priority audit: PR256 / 5100017 / k307

Audit completed 2026-10-13 UTC. This is a bounded independent priority audit, not a mathematical re-review, a literature-absence proof, or an absolute-firstness certificate.

## Finding and disposition

**No independently verifiable earlier public proof covering the exact submitted k307 theorem was located in the searched corpus. No verified priority blocker was identified.** The evidence supports continuing with a credited, cautiously worded k307 result. It does not support “first proof,” “novel method,” “still open everywhere before our work,” or exclusive-priority wording.

The most defensible wording is: “The k307 invariant was observed by Reznik, Garcia and Koiller. We give an explicit signed-area centroid formula on its natural nonzero-area domain, including primitive even star orbits, and identify the exceptional zero-area circle. A bounded primary-source search completed on 13 October 2026 found no earlier covering proof.”

This wording separates the original observation from the proposed proof and does not claim that every ingredient is new. Standard signed moments, support coordinates, even-period symmetry, radial pedal-area dependence, and Poncelet trace techniques are prior mathematics. The precise remaining historical gap is an equivalent earlier specialization or unindexed proof supplying the all-even-period first-area-moment identity, its explicit centroid, or its zero-area domain. None was found here.

## Exact target and chronology boundary

The target is the signed shoelace area centroid of the ordered perpendicular feet from an arbitrary fixed point M to the tangent lines of the outer ellipse at the billiard impacts. The outer tangent intersections themselves are not the foot vertices. The submitted theorem assumes a>b>0, a strictly confocal elliptic caustic 0<lambda<b², and least even period N>=4. It includes primitive stars wherever signed area is nonzero, an explicit centroid formula, and the exact zero-area circle when d<0. It distinguishes repeated even primitive cycles from padded odd cycles.

The supplied pre-publication boundary is the PR creation time **2026-10-01T11:54:40Z**, corroborated by the parent folder's original provider metadata. The submitted PROOF.md SHA256 is **d072c6ecf0f398753382603bbd00b4a950e50881d1fd3aa70526fc8889c12584**. TARGET_SNAPSHOT.json retains these exact identifiers and hashes.

A day-only “1 October 2026” date cannot establish that a proof preceded 11:54:40Z. Provider record creation timestamps establish the deposit chronology used below; they are not a universal certificate of the first time a document appeared anywhere.

## Primary-source comparisons

| Primary original | Exact inspected content | Relation to k307 |
|---|---|---|
| Reznik–Garcia–Koiller, [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), 29 October 2020 11:37:49 UTC | Full PDF/text; Table4/Section3.4 PDFp6 visually checked | k307 is C'_2, even N, all M, with unknown value and proof. k306 is C'_0 and separately credited. Historical observation, not a proof. |
| Final Fifty New Invariants, [DOI10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y) | Full original publisher PDF/text; printedp346 visually checked | Same distinction and signed-area centroid quotient. Historical question marks do not certify current open status. |
| Bialy–Tabachnikov, [arXiv:2001.08469v2](https://arxiv.org/abs/2001.08469v2), 5 May 2020; final DOI10.1007/s40879-020-00428-7 | Entire original final text; Theorem4.1 and proof pp1348–1349; p1348 visually checked; Theorem4.3 discussion | Theorem4.1 explicitly concerns k306/k302: the arithmetic vertex mean and sum of squared distances. It contains no area first-moment quotient. Theorem4.3 gives classical symmetry/four-period background. |
| Schwartz–Tabachnikov, [arXiv:1607.04766v1](https://arxiv.org/abs/1607.04766v1), 16 July 2016 16:53:25 UTC | Full original PDF/text; Lemma2.1, Theorem1, Section3 proof and Remark3.1; theorem page visually checked | Establishes homothetic conic loci (possibly points) of vertex/area centroids for Poncelet polygons between nested conics. It does not identify the general pedal-foot family or give k307's explicit centroid/domain. |
| Chavez-Caliz, [arXiv:2004.05404v1](https://arxiv.org/abs/2004.05404v1), 11 April 2020 13:57:06 UTC | Full original PDF/text; Theorem6 and full proof; other centroid statements screened | Even-period product of original polygon area and outer tangent polygon area, and other centroid-locus results. No pedal-foot area moment. |
| Akopyan–Schwartz–Tabachnikov, [arXiv:2001.02934v2](https://arxiv.org/abs/2001.02934v2), PDFdated25January2020 | Full original PDF/text; Theorem5 and full proof | Circle/concentric-ellipse adjacent dot-product invariant. No k307 centroid theorem. Relevant trace methods are established prior art. |

A direct scope obstruction to substituting the generic Poncelet-centroid theorem is checkable: for a foot Q from M to a tangent of E, the tangent normal is proportional to Q-M, so
\[
 ((Q-M)\cdot Q)^2=a^2(Q_x-M_x)^2+b^2(Q_y-M_y)^2.
\]
The general foot locus is described by this quartic relation; it has not been shown in those older papers to be the required Poncelet polygon on a fixed conic. Applying their circle-or-point conclusion also requires establishing the stationary-point specialization and controlling the centroid denominator. The submitted doubled-normal and cubic-moment identities provide additional work. This comparison does not claim novelty for those identities.

Original primary PDF hashes independently match the supplied pinned hashes:

- arXivv11: c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da.
- FinalReznik: c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42.
- FinalBialy–Tabachnikov: 10fc931a9c0e8c656891872695157a88f21ec91860fd82b2308620518df53b0b.

## Recent automated-proof publication screen

The complete current EulerSolve research-paper index and sitemap were retrieved as originals. Both contain **21 AMR-050 manuscripts**, covering codes0001,0007,0012,0014,0019,0021,0023,0025,0026,0027,0029,0036,0041,0043,0044,0046,0048,0053,0062,0068,0069. There is no0017 entry. The exact /papers/amr-050-0017/ URL returns HTTP404.

All21 original source ZIPs, paper-page HTML, machine metadata and verification reports are saved locally with retrieval times, headers and SHA256. Archives were extracted only after rejecting unsafe paths. FULL_RECENT_THEOREM_SCOPE_MATRIX.json preserves all main.tex abstracts, theorem/proposition/corollary statements and full main.tex hashes. EXACT_TARGET_ARCHIVE_SCAN.json records a case-insensitive exact-target scan of **522 textual source/certificate files, zero hits**. The absence of identifiers is supplemented by theorem-scope comparisons; it is not used alone.

The nearest plausible competitors were compared against their actual originals:

| Recent original | Verified deposit time | Full content compared | Exact scope gap |
|---|---|---|---|
| Ferudun AMR-050-0025, DOI10.5281/zenodo.23068631 | 2026-09-30T19:09:33.719224Z, before cutoff | Complete original manuscript and verification report; deposited ZIP/PDF fetched; main.tex hash exactly matches current EulerSolve copy | Focus antipedal of a circumscribed rectangle, not an outer-side pedal polygon; proves k406,b. |
| Ferudun AMR-050-0026, DOI10.5281/zenodo.23071366 | 2026-09-30T22:04:12.260164Z, before cutoff | Complete original manuscript and trace proof; deposited ZIP/PDF fetched; main.tex hash exactly matches current copy | Outer-polygon focal antipedal vertex centroid k407; expressly no signed-area-centroid claim. Typeset date1October differs from provider date; deposit time governs this comparison. |
| Ferudun AMR-050-0014v1.0, DOI10.5281/zenodo.23087221 | 2026-10-01T16:56:14.316216Z, after cutoff | Original first-version ZIP/PDF/report fetched, compared against currentv1.1 | k303,a outer-pedal area product for N=2mod4. Contains radial area quadratic but no first-area moment or centroid formula. |
| Ferudun AMR-050-0014v1.1, DOI10.5281/zenodo.23088516 | 2026-10-01T18:12:36.529602Z, after cutoff | Complete current manuscript; exact version comparison retained | Adds centered k303,b scope; still an area-product theorem. |
| Ferudun0021/0023/0027/0029/0036 | Provider dates retained in receipts/metadata | Full main.tex originals retrieved; exact theorem/domain statements inspected | Respectively k403,b focal area products; k405 original antipedal vertex centroid; k501 odd Steiner-pedal ratio; k503 odd inner-Steiner ratio; k608 focal outer-antipedal area definedness. None supplies the k307 first moment. |

All nine fetched deposited files pass their exact provider MD5 checks. ZENODO_ORIGINAL_CONTENT_COMPARISON.json retains the original/current main.tex SHA256 comparisons. The two genuinely pre-cutoff centroid papers have authenticated unchanged contents and different constructions, so a current rewritten abstract has not been mistaken for an earlier proof.

This audit does **not** accept or reject the correctness of all21 external manuscripts. Their theorem scope suffices to exclude them as direct covering k307 proofs. Similar elementary or meromorphic mechanisms should continue to be credited if used.

## Other recent repository and citation leads

The public repository muralisubbarao2/Resolved-unsolved-math-problems-with-GPT-6-Astra is dated9September2026, with pinned commit d9a93e2bdc88ffe6926d613c15ecb2f0a9f17ffc at01:10:06Z. Its complete tree has exactly three solution-status PDFs, all58 pages retrieved/extracted. None mentions AMR-050, k307, pedal polygons or centroids. Its sole billiard entry is AMR-109-0209, billiards in general polygons, and explicitly retains major gaps. The reports are status catalogues, not public full proofs for every referenced local item. No exact target claim or certificate was found; unavailable local item reports cannot be assumed to cover this target.

The August2026 DannyExperiments/elliptic-billiard-antipedal-ratio-counterexample repository was pinned at tree4b4781c0c69cb65db6f1216161c5dad8246f311b. Its original manuscript, canonical claim and proof were retrieved. They prove focal original-antipedal area equality with an exact primitive8-period zero-area counterexample for k607. They neither concern tangent-foot centroid k307 nor classify its zero-area circle.

The arXiv query for billiard+invariants returns269 records; the newest100 metadata records were saved and screened, including recent2026 confocal commutation work. The focused pedal query returns the distinct2021 bicentric paper; exactk307 and focused centroid queries return zero metadata hits. Searches are of the service's indexed metadata, not a guaranteed full-text corpus.

The OpenAlex citation graph for the original DOI returns19 records. It was used only for discovery. Existing leads were followed to original PDFs: Stachel motion/geometry, Garcia–Reznik self-intersected invariants, average elliptic-billiard invariants, Bakiev–Molodyk2026 confocal-map commutation, Dragovic–Murad2025 Parable of the Parabola, and Berman–Gevay–Richter-Gebert–Tabachnikov2026 movable incidence configurations. Full originals and extracted texts are retained. Relevant centroid/pedal statements in the parabola paper concern circle/parabola Poncelet triangles and chord midpoints, with incompatible conics/periods. The others provide geometry, angular/perimeter traces, low-period constructions or incidence motion; no covering k307 first-moment proof was identified. Scan-only negative terms are not presented as proofs of impossibility.

## Search receipts and precise limitations

- Seven preserved web tool receipts contain exact identifier, exact mechanism, recent preprint and primary-source searches; complete returned text is retained.
- Three preserved GitHub connector receipts contain six code queries and three global issue queries. Broad code queries produce many unrelated token matches and have top100 limits. The exact AMR identifier code query returns zero. One exact issue query initially failed with a protocol error; the public REST retry succeeded with zero hits.
- Nine HTTP receipt sets preserve URLs, response status, retrieval timestamp, headers, exact source SHA256 and byte size. Original PDF extraction and visual-render receipts are retained.
- Zenodo exactAMR-050-0017 and k307+billiard searches return total0; broader centroid/pedal searches produce the distinct results above. First requests with size100 failed400 because unauthenticated searches support size25; successful retries and both failures are retained.
- UnsolvedMath exact target URLs returned429. Their live site cannot be claimed inspected. The imported target/source and public papers do not prove the absence of a solution posted there.
- Search indexes can omit repositories, PDFs, altered identifiers, general theorems, unpublished material and very recent deposits. A repository commit timestamp alone is not absolute first-publication evidence.
- No inaccessible manuscript, private proof, undisclosed certificate, external-person testimony, conventional human review or proof-assistant formalization was obtained or inferred. No external individual was contacted.

The assigned bounded audit is complete. Historical exclusivity remains unproved. The precise publication-safe outcome is **“no earlier covering proof found after the documented bounded audit”**, with source and mechanism credit preserved.

