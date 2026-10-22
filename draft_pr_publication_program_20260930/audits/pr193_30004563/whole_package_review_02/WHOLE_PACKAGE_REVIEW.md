# Independent whole-publication-package review 02

Review date: 15 October 2026 UTC. Target: PR193 / problem30004563, frozen `publication_package_v2`, package-seal SHA-256 `fe7b6c7abda9d04f35d6b07f5524e023320df9d8c399bc01cd4fb797c630301d`.

**Terminal verdict: CLEAN PASS for the complete frozen qualified-note package. No substantive issue or required repair was identified.** The mathematical existence claim, its source interpretation, exact verification, actual PDF/TeX, historical evidence, archive integrity, intended deposit metadata, attribution, and limitations withstand this review. This verdict does not establish historical firstness or authorize a stronger proper-embedding, exact-count, or global-maximum claim.

The strongest independently verified statement is: one fixed six-point algebraic boundary, with six distinct points and both alternating triples noncollinear, admits an incoming alpha=16 realization and at least five distinct outgoing realization centers, all nonboundary. Its fixed boundary crosses. This contradicts the published at-most-three expectation in its crossing-permitted setting.

## Independence and protocol

The published MRT definitions/target and OWR p.1785 were read before the manuscript, code, certificate, archive contents, or earlier reviews. `source_first_assessment.md` was sealed at 2026-10-15T10:06:56.506201+00:00, SHA-256 `4316f5868c15f61c884d9276c04aea278c955f0188cb4875d4d0adabd09f2e0d`. It fixes the exact source setting, six face orders, success criterion, and attacks.

After reading the current note and verifier, I wrote a new exact checker without importing the author code or loading its certificate. It uses triple integer-square-root floors on a decimal grid, rather than the current verifier's binary eighth-power search; 45-place radical bounds rather than 36; 150 boundary bisections from [-16,16] rather than 128 from [-8,8]; direct elimination for outgoing y; and absolute-coordinate reconstruction of incoming Z rather than the translated Y implementation. Every decision is an integer or Fraction predicate. Floats occur only in explanatory displays in the independent result. Each radical cell is explicitly checked by eighth powers.

`first_principles_assessment.md` and its code/result hashes were sealed before earlier review contents were read. The assessment SHA-256 is `caba9e69e4be961b68de8acc64efdc243a9796959a7c2bcdfee02d4627e25ccf`. All four early seals still match. The mathematical conclusion below therefore precedes the historical audit comparisons; earlier verdicts were not an oracle.

Writes were confined to this new review folder. No local Git/index/ref/branch/checkout commands, remote writes, PR operations, publication, messaging of outside individuals, or UI changes occurred. The unrelated open document was not accessed or modified.

## Source setting and exact target

The primary published source is [Melotti–Ramassamy–Thévenin, DOI10.4171/AIHPD/163](https://doi.org/10.4171/AIHPD/163). Definitions2.1,2.4,2.5,2.7 give the opposite-side power equation, explicitly permit nonproper quads/realizations, require six distinct boundary points with the alternating triples noncollinear, and define construction curves by that equation. The incoming faces read directly from Figure6 are A1A2A3Z, A3A4A5Z, A5A6A1Z; the outgoing faces are A2A3A4X, A4A5A6X, A6A1A2X. I later visually checked complete published pages788,789,790,792,811, including Figures6–7 and Remark4.8. The note uses precisely these orders.

Remark4.8, printed p.811, proposes at most three shared-focus construction-curve intersections when alpha>1 without adding an embedding restriction. [OWR35/2020, DOI10.4171/OWR/2020/35](https://doi.org/10.4171/OWR/2020/35), printed p.1785, expressly allows edge crossings and conjectures three as the maximal possible number of potential centers. Its complete page was also visually checked. The note's result addresses that stated crossing-permitted setting. A stronger oriented surface-immersion assumption is not being imported from the informal word immersion.

The current theorem does not require or claim proper embeddings. The independent strict boundary crossing alone rules out an embedding for every central choice. The source allows this crossing, so it is a limitation of the stronger interpretation, not a defect in the actual counterexample.

## Scalar reduction, branch and existence audit

For alpha=16, a squared Euclidean distance is raised to the eighth power. With A=(0,0), B=(2073/10000,0), C=(4719/10000,64/10000), lambda=27/1250, the focus equations are

`|X-B|^16-|X-A|^16=lambda`, `|X-C|^16-|X-A|^16=1`.

Put s=|X-A|^16. The nonnegative eighth roots u,v,w recover squared distances, and the coordinate equations have determinant4bd>0. At a zero of G=x²+y²-u, the recovered three squared distances are exactly u,v,w; taking eighth powers gives the original equations. Conversely every actual solution recovers these same principal roots and this same linear system. There is no elimination through a sign-ambiguous square, extraneous branch, lost denominator, or reliance on a numerical root solver. Distinct s values give distinct X because s is a fixed function of X.

Independent strict Fraction bounds reproduce every current Table1 entry:

| s | strict containing interval for G(s) |
|---|---|
| 9/10000 | (0.38,0.39) |
| 11/10000 | (-0.28,-0.27) |
| 13/10000 | (0.51,0.52) |
| 1/2 | (-0.91,-0.90) |
| 1 | (9,10) |
| 10^16 | (-4.766,-4.765) |

G is continuous on [0,infinity), including s=0; none of the chosen intervals meets zero. The five successive open sign-change intervals are disjoint. IVT supplies a zero in each, so there are at least five distinct centers. The proof and current code do not assume uniqueness within an interval or that the list exhausts all roots. An independent 100-step refinement retains strict endpoint signs in all five brackets.

The analytic large-endpoint argument was separately reconstructed. At s=10^16, u=100 exactly. Concavity bounds the two radical increments above by lambda/(8·10^14) and 1/(8·10^14). Substitution into the coordinate system gives the stated positive rational x/y boxes around

`(x0,y0)=(2073/20000,1249057/128000)`.

Their squared norm is exactly39007985196121/409600000000. Squaring the boxes and subtracting100 proves the last strict table row. A fresh direct radical enclosure also agrees. Thus no floating-point cancellation manufactures the remote sign. At infinity the coordinate function approaches this circumcenter while u diverges, and G tends to negative infinity. The fifth center is finite and nondegenerate even though it is close to the limiting coordinate value.

## Fixed algebraic boundary and incoming center

For each of the three boundary parameters, q is nonzero and h is nonzero. The displayed g''=16(t²+h²)^6(h²+15t²) is strictly positive. Therefore g(t-1)-g(t) strictly decreases; its degree15 leading term is -16t^15, with opposite infinite limits. Multiplication by |q|^16>0 preserves these facts. The polynomial has rational coefficients, is nonzero, and has exactly one real root. Independent strict rational endpoint signs isolate that root. T is an unambiguous algebraic constant, not a parameter selected afresh at each endpoint.

The root equations yield the three boundary power differences exactly. The six cyclic edge powers are `(a,f,f+lambda,g,g+1-lambda,a+1)` and both alternating sums are a+f+g+1. This is an exact identity from the definitions, rather than an interval residual merely containing zero.

The independent computation verifies the printed coordinate bounds, all15 pairwise distinctness conditions, and all20 noncollinear boundary triples. The required determinants are exactly0.00132672 for the even triple and in (6.37,6.39) for the odd triple. The independent strict crossing orientations for A1A2 against A3A4 are [-,+,+,-]. Consequently the fixed boundary really is crossed.

For the incoming problem, the levels L=g-f-lambda and M=a-f are positive fixed algebraic constants. The odd determinant is nonzero. I reconstructed the incoming point directly in absolute coordinates by subtracting squared distances from the A3-focus equation. This recovers the same H without sharing the current translated-coordinate implementation. Exact intervals give

`H(1/100) in (0.00037,0.00038)`,

`H(11/1000) in (-0.00081,-0.00080)`.

All radical arguments remain positive and the coordinate denominator excludes zero throughout the interval. Thus H is continuous for the same fixed boundary, and IVT supplies the incoming realization. The full incoming box lies in (0.1677,0.1717)×(-0.0036,-0.0026). It is disjoint from every boundary point and every line through a boundary pair.

Coefficient interval arithmetic correctly contains the values associated with those same unique T roots. Repeated occurrences losing correlation enlarge enclosures; they do not change the fixed-boundary quantifier. All signs survive that enlargement. No boundary value is chosen separately to force either H endpoint.

## All six faces and nondegeneracy

I independently checked the six opposite-side identities as sparse exact integer coefficient vectors in the basis `[a,f,g,lambda,1,r3,qA]`. Using

`r1=r3+a-f`, `r5=r3+g-f-lambda`,

`qB=qA+lambda`, `qC=qA+1`,

the three incoming residuals and three outgoing residuals all cancel identically. In particular the third incoming face uses M-L=a-g+lambda, an exact consequence of the boundary construction. No face equality is inferred from an interval around zero, and no flip-existence theorem is used to conceal a missing incoming construction.

All five retained outgoing intervals are pairwise disjoint. Their coordinate boxes are nonboundary; each selected center and the full incoming box avoids every line through two boundary points. Together with the20 boundary triples, these strict checks exclude collapsed edges, repeated face vertices, and collinear face triples for every required face. The outgoing nonboundary argument in the text also independently works: lambda>0 forces x<b/2; A1,A5 are on the other side; A fails b^16=lambda; B,C fail positive-level equations; and A3 has the second residual strictly in (0.98,0.99).

The inversion would fail for collinear focus triples; none occurs here. The T argument needs nonzero q and the stated h values; they are checked. Claims at alpha=1,2, nonpositive alpha or infinite alpha do not follow from this integer-power construction and are not made. Exact total counts, any universal maximum and proper-embedding multiplicity remain open within this package's evidence.

## Primary verifier and count semantics

The entire10631-byte current verifier was read before execution. It imports only standard-library modules and no project code. The interval operations, reciprocal behavior for denominators of either sign, square crossing zero, nonnegative powers and eighth-root endpoint bounds are correct for the arguments used. The integer search's initial upper bound and final rational eighth powers are explicitly checked. Every validity failure uses an explicit exception; Python optimization does not disable it.

In owned copies, default execution and `python3 -O` both recomputed exactly the recorded certificate and reproduced the archived stdout. File inventories/hashes before and after were unchanged. A Python audit hook prohibiting file mutation and network/process events allowed the verifier to finish successfully. Changing the certificate alpha field to15 was rejected in both execution modes, proving that the default certificate comparison remains active under optimization. The deliberate write flag is accurately described as opt-in regeneration; the default has no write.

A dynamic trace found exactly17472 successful `require` calls. Of these,12552 are four recurring root checks for3138 radical endpoint evaluations;4200 are interval-order checks;500 are bisection midpoint-sign checks; the remainder includes the geometric, strict-margin and retained-bracket predicates. The package correctly labels this count as bookkeeping, not independent mathematical propositions. Its proof is the stated exact identities, enclosures and IVT, not the integer17472.

## Complete archive, provenance and intended upload

All15 outer files are exactly allowlisted and mode0444. Every recorded outer byte count/hash matches. The input PACKAGE_SEAL itself has the required hash. The ZIP has exactly64 unique, safe relative regular-file members and passes its CRC integrity check. Every member matches ARCHIVE_INVENTORY. Its self-excluded MANIFEST covers exactly the other63 files and every listed byte count/hash matches.

The ZIP PDF, TeX, current verifier, current certificate, stdout, README, license and source-reference JSON are byte-identical to their outer counterparts. Its `zenodo-metadata.json` equals the complete `metadata` object in the intended outer deposit JSON. LOCAL_DEPOSIT_CHECK's three intended upload sizes/hashes match the actual PDF, TeX and ZIP. Thus the concrete intended uploads faithfully contain the reviewed science and metadata.

All49 nested historical safe-manifest entries match their actual archived bytes. The three recorded original-submission inputs still hash to their historical values; all144 private priority-cache file hashes also match their safe hash-only record. The archive includes only the original note as a PDF body, not third-party PDFs, OCR, rendered source images, full source extractions or private API/account snapshots. The public evidence matrices contain scoped source/search metadata and summaries. The unrelated open work is absent.

After the independent first-principles seal, I inspected the historical reports, code and records. All three independently replayable historical mathematical checkers reproduce their complete recorded certificates (apart from the geometry audit's fresh run timestamp). The old submitted replay and count wrapper reproduce6987 successful calls; its comparison script reproduces the containment records when given the documented original certificate in an owned private relative-path copy. The older submitted verifier requires ordinary Python assertions, and the historical count wrapper explicitly rejects optimized Python. That limitation is disclosed and does not apply to the current primary verifier.

The original10^17 cutpoint remains in appropriate historical evidence. Both READMEs explicitly label that history and explain the separate10^16 analytic improvement. The current note, current verifier, current certificate and stdout consistently use10^16. Different final endpoints in those explicitly historical records do not create a current mathematical contradiction. Their original bytes have been preserved, not rewritten to conceal chronology.

## PDF, attribution, metadata and priority

The six current PDF pages were rendered and visually inspected in full. The title, author/ORCID, date, unrefereed status, theorem, coordinate equations, strict sign table, boundary specification, incoming construction, six face identities, crossing table, disclosures and bibliography match the current TeX. There are no missing symbols, overlapping table cells, clipped formulas, bad reference placeholders or unreadable material. No separate rebuilt PDF is substituted for the actual intended-upload PDF.

The older curve-family attribution was checked against primary content. Ash–Bolker's scanned equations1.6–1.8 at pp209–210 describe weighted phi-distance comparisons; pp241–242 separately discuss pure t^4 and an oscillatory non-power example. Those pages were visually inspected. BPR's author manuscript Definition4.12 explicitly gives the p-power-cell comparisons. BR's accepted manuscript generalization gives the same family. The linked arXiv1409.2786v1 was independently retrieved because its section locator initially looked different from the accepted cache: it really does have Section1.7 Generalizations containing the p-power family, so the package locator is correct. These older equation families are fully credited in the note and intended description.

Official publisher pages independently confirm the older bibliography metadata: [Ash–Bolker](https://link.springer.com/article/10.1007/BF00164401), [Bourne–Peletier–Roper](https://epubs.siam.org/doi/10.1137/130922732), [Bourne–Roper](https://epubs.siam.org/doi/10.1137/141000993). The exact common-cost equivalence is correct with p=16 and minus-convention weights0,lambda,1; the plus-convention Ash weights are their negatives. The note makes no new-curve-family claim.

An oscillatory phi example with many components is not automatically a >=4 pure-power shared-focus witness. Neither generic three-cell valence nor four intersections of full alpha1 conics proves this alpha>1 count. The package distinguishes these mechanisms correctly. The archived priority search has an explicit >=4 threshold and discloses bounded results, incomplete indexes and access failures. I independently checked the closest older primary families; I do not transform the broader recorded search into an exhaustive literature proof.

The manuscript, README and intended deposit description expressly leave historical priority unestablished and avoid firstness, independence from unknown work and public-awareness claims. That qualified route is supported. No proof of unknown literature absence is required for the bounded mathematical note. AI assistance is disclosed as extensive; the note and metadata explicitly say unrefereed and without conventional human peer review. The author name and ORCID match the provided research metadata. The note/support license is CC BY4.0 with third-party rights retained. Preparation records still say publication_ready=false and review pending, accurately reflecting the frozen package's pre-review preparation stage rather than pretending a publication has occurred.

## Findings, remaining gaps and handoff

Severity-critical/high/medium substantive findings: **none**. Required scientific or publication-content repairs: **none**. No silent repair was made to the frozen package.

Verified package scope: a qualified, unrefereed exact counterexample note demonstrating at least five outgoing centers for a fixed admissible incoming alpha16 realization. Remaining unsupported stronger claims are exact total number of centers, universal maximum, proper-embedding multiplicity, and historical firstness/unknown awareness. The package already identifies these limits. This review supplies no conventional human peer review or DOI, tracker, publication or merge action.

Completion estimate: **100% of this assigned whole-package adversarial review**, including source-first reconstruction, actual upload-byte fidelity and complete publication QA. This is not a percentage estimate of historical firstness.

Reproduction: `independent_exact_check.py` writes its owned `independent_exact_result.json`; rerun it only in a writable copy after this review is sealed. The other safe JSON records preserve current/historical verifier replay, count trace, archive/member content coverage, nested provenance, and source-inspection results. SAFE_ALLOWLIST.json and SHA256_MANIFEST.json define the final public handoff. `private_work/` is excluded in full, including licensed sources, OCR/text, source/note renders, extracted archive copies, mutation controls and wrappers. All safe handoff files are mode0444.
