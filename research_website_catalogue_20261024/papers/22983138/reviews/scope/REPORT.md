# Source and scope review — Zenodo 22983138

Completed 2026-10-25 UTC. Assigned source/scope review: 100%. Verdict: PASS for authenticated source custody, original-source match, and the theorem as actually stated. No material scientific defect was found. Global priority and the live catalogue's current version remain unverified; neither is claimed by this verdict. This is an independent AI review of an unrefereed preprint.

## Exact selected work and custody

Queue row 87, work Z-22983137, record 22983138: *Equality in the Fradelizi–Paouris–Schütt second-moment inequality*, Alec Kriebel, version 1.0.0, declared publication date 23 September 2026, DOI [10.5281/zenodo.22983138](https://doi.org/10.5281/zenodo.22983138). Fresh actual Zenodo API gives created 2026-09-26T21:12:54.068503+00:00 and updated 2026-10-10T21:32:40.057077+00:00. These are different date fields; none is a certificate of firstness. Fresh versions/latest resolves to this record, and versions lists one version. Full original metadata, description, file objects, and HTTP receipts are retained in sources/.

All three actual public files were downloaded through ordinary public URLs and authenticated against the fresh API MD5 values. The actual published SHA256SUMS also validates both named payloads.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| paper.pdf | 63,494 | 62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c |
| source-and-verification.zip | 133,155 | 738ccb98e973b71f642f83a8abdb05559ad58073b7a2dde79e785f869e6a567c |
| SHA256SUMS | 170 | 36a4cffe10d992ebb321dfb09990e139387253b6b7de0a301fad18a432c93edd |

The selected PDF has four actual pages and equals both the specified local candidate and the sole PDF inside the archive. The ZIP has 29 safe unique file members; every member was decompressed/CRC checked and given an individual hash. There is one 11,101-byte TeX manuscript, SHA-256 ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29, with no local input/include/bibliography/image dependency. All 28 entries of its embedded SOURCE_SHA256SUMS validate. Metadata copies and deposition wrapper agree semantically. Historical upload instructions say the deposit was not yet made; the fresh actual API governs present DOI/version facts. Nothing was repaired or repacked.

SOURCE_READY.json and SOURCE_READY_SEAL.json were sealed and sent promptly to the parent and the two independent lanes. The early source seal binds 37 files. The entire actual four-page PDF was read in text and as all four raw rendered pages; the entire TeX was read. INITIAL_INDEPENDENCE_SEAL.json then froze the initial claim/dependency reconstruction before any archived review or sibling opinion was read. Archived reports were subsequently read as original support, without adopting their verdicts as premises. No current sibling opinion was read. The original full abstract is preserved in INITIAL_INDEPENDENT_CLAIM_DEPENDENCY_SCOPE.json.

## Exact claim and proof coverage

For every integer n>=1, every r>0, and every compact convex K in R^n with nonempty interior, assume each extreme point v satisfies ||v||_2>=r. With n-dimensional Lebesgue volume, g_K=|K|^-1 integral_K x and C2(K)=|K|^-1 integral_K ||x||_2^2, the claim is

C2(K) >= [r^2+(n+1)||g_K||_2^2]/(n+2),

with equality exactly when K is a nondegenerate n-simplex whose vertices all have norm r. The origin is fixed by the radius condition. No zero centroid, origin containment, regular simplex, smoothness, closed extreme-point set, or finite extreme set is required. There is no iteration, kernel, stochastic model, support law, or asymptotic parameter in this theorem. The only limiting operation is exhaustion by nested finite extreme-point hulls. Convergence of their volume moments is justified for bounded integrands, with volumes bounded below by the initial simplex volume.

The weaker bound omitting the centroid term additionally requires centroid zero for equality. Nonregular inscribed triangles can attain the strengthened inequality. Under a strictly greater extreme-point norm condition equality is impossible, including when no uniform radial margin exists. Degenerate bodies are excluded by the positive-volume definitions. The explicit n=1 interval case is valid. The positive retained-pair witness is body dependent and has units of squared length; it does not establish a uniform shape stability theorem.

ANALYTIC_CHECK.md records the independently checked deduction. The manuscript proves its load-bearing partition, rather than assuming a triangulation theorem for arbitrary bodies. Strictly visible finite-facet shells retain all earlier simplices. A dense convex union contains int K; its omitted boundary is null. The countable weighted moment identities converge absolutely on bounded K. Nonnegative radial and centroid-variance terms retain exact equality information. Equal simplex centroids then force only one positive-volume simplex. The alternative finite proof retains the same two positive-volume simplices, producing a fixed strictly positive deficit before passing to the limit. This avoids assuming strict inequalities survive limits automatically.

The only substantive standard geometric import is finite-dimensional extreme-point representation. A fresh author-hosted proof of the stronger K=conv(ext K) theorem was read in [Bertsekas, Convex Optimization Theory](https://web.mit.edu/dimitrib/www/Convex_Theory_Entire_Book.pdf), Exercise 2.2 and solution, PDF pages 343–344. Compact finite-dimensional hypotheses fit exactly. Countable separability, null convex boundary, barycentric integration, and bounded countable summation are explicitly justified in the checkable reconstruction. No numerical evidence is used to infer an all-dimensional analytic claim.

## Primary-source match and bounded literature check

The fresh actual [FPS journal PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE65A193C3EE743DF0EA834A8405026E/S0008439500021561a.pdf/simplices_in_the_euclidean_ball.pdf) was read in full. Its Theorem 1.1, following paragraph, Lemma 3.2, and Section 3 identify the inequality, polytope equality result, simplex formula, and general-body conjecture. Those earlier results must retain FPS attribution; the selected contribution is the extension of equality to general bodies.

The actual [Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3154/OWR_2009_53.pdf?isAllowed=y&sequence=1), contribution on printed pages 2907–2909, records the same question. Both originals use strict prose alongside an on-sphere equality clause. The selected manuscript explicitly uses the non-strict hypothesis, consistent with the source simplex discussion. The original setting starts at n>=2; the current interval argument adds n=1. The distinct John/Löwner-position results are outside this contribution.

The live UnsolvedMath URL returned HTTP 429 in this lane. I did not bypass the restriction or use UI. The archive's historical v1.7/n>2 catalogue description is a historical assertion, not a fresh live-page authentication. The original mathematical target is directly authenticated through FPS and OWR; no current catalogue status, wording, or version is certified here.

Fresh OpenAlex lists five citing records: four other works plus this preprint's concept DOI. Fresh Crossref was also retrieved. Four primary citing bodies were acquired anew. Alonso-Gutiérrez's five-page article was read in full, including Remark 2.2; it concerns isotropy bounds and a John-position application. Selected actual introduction and citation contexts were read in Paouris–Werner (PDF pp. 1–2,6–8,39–41), Fradelizi–Meyer–Yaskin (pp. 1–2,5–7,13), and Huang v4 (pp. 1–2,18–21). Those inspected contexts concern centroid bodies, directional support/moment estimates, and John ellipsoids. They do not furnish the target equality proof in the inspected passages. Entire-body exclusion claims for the longer citing papers are not made.

Additional current searches screened the exact title, DOI/problem identifier, equality/conjecture terminology, and countable extreme-point simplex decompositions. The search ledger records the bounded queries and limitations. No earlier general-body equality proof was identified within the material actually inspected. This is not evidence of global absence and does not certify firstness, originality of incremental triangulation, or completeness of citation indexes. The archived September priority audit is supplemental historical evidence; its search count and full-text coverage are not presented as freshly reproduced here.

## Reproduction, preservation, and exact limits

The entire standard-library verifier was read before execution. Both normal and optimized runs exit zero with byte-identical JSON, also identical to the archived result: 298 exact rational checks in 18 cases, including n=1–6 simplex examples, planar shells, coplanar support-line control, and retained-pair bounds. Polynomial simplex integration and independent polygon moments support finite identities. These computations establish neither the arbitrary-body partition nor uniform analytic equality; the written proof supplies those steps.

All scientific support, metadata, original manifests, code, and archived review bodies were read after the independence seal. The archive's site/index.html received byte custody and checksum verification only: its content and the corresponding old article are deliberately withheld until the parent-authorized later live gate. No article, deployment, redirect, publication configuration, shared script, native Sheet, source manuscript, Git state, release, or external individual communication was changed. No builder was executed. Only this record's source/custody/review namespace was written. Third-party full text and raw reading copies remain solely in the ignored cache, established before fetching; public receipts contain locations, hashes, and summaries.

The strongest verified scientific result is the complete stated equality classification and its positive finite witness. No theorem gap or necessary source correction was found in this lane. Remaining limits are the inaccessible live catalogue, bounded bibliographic coverage, unread parts of longer citing bodies, absence of formal proof-assistant certification and external human refereeing, and the intentionally deferred old article inspection. Source and original-preservation receipts, read ledger, final manifests, and seals make those bounds checkable.
