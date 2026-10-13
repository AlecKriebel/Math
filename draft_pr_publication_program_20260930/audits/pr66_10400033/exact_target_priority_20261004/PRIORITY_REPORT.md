# PR66 exact-target priority audit

Verdict: **prior_full_solution** for the original universal target, Ohtsuki Conjecture 2.11 (Willerton). Historical novelty of the candidate theorem must not be promoted. This finding does not adjudicate novelty of its tournament mechanism or its separate even-crossing refinement.

## Exact claim and decisive source

The authentic candidate claims, for every classical knot diagram with n crossings and primitive mirror-odd degree-three invariant normalized to 1 on the right trefoil,

\[
|v_3|\le\left\lfloor\frac{n(n^2-1)}{24}\right\rfloor.
\]

[Ohtsuki's publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed 403/PDF 31, fixes precisely this normalization and states that the image of (v2,v3) is Z². Conjecture 2.11 is printed 405/PDF 33. The titlepage printed 377/PDF 5 gives publication **1 June 2004**, although the volume is labelled 4 (2002).

The decisive earlier source is [Thomas Fiedler and Alexander Stoimenow, *New knot and link invariants*, author PDF](https://stoimenov.net/stoimeno/homepage/papers/inv.pdf). Its displayed estimate in §3.2, printed 7/PDF 7, is

\[
|vt_3|\le {n\choose2}+{n\choose3}\le n^3/6.
\]

Remark 3.1, printed 6/PDF 6, gives

\[
vt_3=4v_3=-\frac13V''(1)-\frac19V'''(1).
\]

This matches the candidate/Willerton Jones-derivative convention exactly. Retaining the **first** upper bound, rather than only its weakened n³/6 form, yields

\[
|v_3|\le\frac14\left({n\choose2}+{n\choose3}\right)
=\frac{n(n^2-1)}{24}.
\]

Integer-valued v3 then gives the exact floor. The arithmetic identity is a direct specialization of a displayed prior universal estimate. It neither assumes the conjecture nor transfers the main difficulty to a new unsupported extremal theorem.

## Hypotheses and validation of the match

The §3.2 display concerns a diagram with c crossings, uses an absolute value, and imposes no positivity, alternatingness, primeness, minimality, or torus hypothesis. The preceding Theorem 3.1 does concern reduced positive diagrams, but that distinct theorem supplies no hypothesis for §3.2. The formula and Gauss-sum definitions are for ordinary knots in S³.

Printed5/PDF 5 specifies distinct unordered crossing subsets and counts an automorphism only once. Formula(1) has two disjoint three-chord types and a two-chord term. Its triple contributions have magnitude at most1; the pair weight is (wp+wq)/2, with each writhe ±1, so also has magnitude at most1. Thus the displayed binomial estimate has an explicit checkable counting basis. Remark 3.1 removes the possible lower-degree ambiguity mentioned immediately before formula(1): the invariant used in the estimate is exactly4v3.

Pages5,6,7 and the original problem pages403,405 were visually inspected from privately rendered publisher/author PDFs. The actual inequality signs on page 7 are both ≤. Executable receipts record retrieval, extraction, rendering, and arithmetic validation. `verify_specialization.py` checks the polynomial coefficient identity universally and exact boundary arithmetic for n=0 through 100. The imported invariant formula is not re-proved by that arithmetic check.

The n=0,1 cases have bound0; n=2 gives1/4 before flooring and0 after flooring. The right trefoil n=3 gives1. Mirror normalization and absolute values prevent a sign-convention escape. The same bound for crossing-minimal diagrams would extend to larger n because the target grows with n, but that extension is unnecessary: the prior source is already diagram-based.

## Historical custody, publication, and limits

The full author PDF is 268871 bytes, SHA256 `193dfd4c993f2337ba17b48f524d8c71333f8717d520ba299f7b76a8cbd324b7`. Its titlepage says current version1 February2002, first version9 December1996, with minor updating relative to the printed paper. [The author's bibliography](https://stoimenov.net/stoimeno/homepage/papers.html) identifies the linked22-page version as31 January2002 and explicitly distinguishes its updates/corrections from print.

[Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1142/9789812792679_0006) identifies the chapter as *Knots in Hellas '98*, pp59–79, published September2000, DOI [10.1142/9789812792679_0006](https://doi.org/10.1142/9789812792679_0006). This independently verifies the bibliographic publication, **not the identical content of every printed page**. The 2000 printed chapter body could not be retrieved. Its publisher endpoint failed, the CiteSeer mirror of a1999 version timed out, and a Wayback CDX request failed. Receipts preserve those failures. No immutable pre2026 byte-history of the author PDF is asserted. Its scientific date is supported by its titlepage and author bibliography; exact earliest dissemination is outside this audit's goal.

The final paragraph of author page 8 asserts an even stronger maximization claim for T(2,2m−1) through2m crossings. That would give, for even n, n(n−1)(n−2)/24, stronger than the candidate's n(n²−4)/24. The paragraph supplies no displayed extremal proof. **The final verdict uses page 7, not page 8.** Novelty or complete prior proof of the separate even-n improvement remains unestablished in this audit.

## Other primary-source scope checks

| Source | Checked passage | What it establishes here |
|---|---|---|
| Willerton, *On the First Two Vassiliev Invariants*, arXiv math/0104061v1 (5 April2001); journal Experimental Mathematics11(2002),289–296 | Preprint printed 2/PDF 2; torus discussion printed 5 onward | Correct v3 normalization; a weaker universal n(n−1)(n−2)/4 bound; torus values and finite table evidence. It does not supply the exact constant by itself. |
| Willerton,1997 Edinburgh PhD thesis, *On the Vassiliev invariants for knots and for pure braids* | Theorem 16, printed 28/PDF 34; printed 32/PDF 38 | Coarse universal bound and finite data; no exact all-n resolution located there. |
| Abe, *On finite type invariants of knots and 3-manifolds*,2015 academic-year Saitama thesis | Conjecture 3.3 printed 18/PDF 19; Theorem 3.10 printed 21–22/PDF 22–23 | Exact formula with **torus-knot** hypothesis. The thesis explicitly limits the result. |
| Abe, *On Vassiliev Invariants of Degrees2 and3 for Torus Knots*, Tokyo J. Math.38(2015),331–337, DOI10.3836/tjm/1452806043 | Crossref publication/abstract metadata; thesis body substitute | Journal PDF URLs returned HTML, not successful body access. Journal theorem numbering/page mapping is not asserted. |
| Chmutov–Duzhin–Mostovoy, *Introduction to Vassiliev Knot Invariants*, full author submitted manuscript | §14.3, printed 417–418/PDF 425–426 | Universal \(|j_3|\le(3/2)c(c−1)(c−2)\), with j3=−6v3, gives only the weaker quarter-cubic bound. Its discussion of torus inequalities concerns the joint fish plot. |
| Stoimenow, *Gauss sum invariants, Vassiliev invariants and braiding sequences*, author1999 version / journal2000 | §8 printed 22–24; references printed 37 | Torus evaluations and polynomial families; references the earlier *New knot and link invariants* preprint. Not independently used as an exact universal proof. |
| Komendarczyk–Michaelides, *Ropelength, crossing number and finite type invariants of links*, arXiv1604.03870v3 (2018), journal2019 | Preprint printed 3/PDF 3, equation(1.16) | Repeats the quarter-cubic universal v3 estimate. Does not imply that no sharper result existed. |
| Taniyama, *Pairs of knot invariants*, arXiv2404.09283v3 (2024) | Printed29/PDF 29 and references31 | Describes Willerton fish as a crossing-number slice; no exact target claim in this checked passage. |
| Brooks–Komendarczyk, *From integrals to combinatorial formulas of finite type invariants—a case study*, arXiv2212.12792v2 (2024) | Introduction and target-related text screening | Degree-two Casson invariant, regular/multicrossing formulas; no degree-three exact-target proof used here. |
| Lanina–Sleptsov, *Algebraic structures of Vassiliev invariants for knot families*, arXiv2508.02385v2 (17 December2025) | Introduction/family scope; reference29, printed 20 | Relations inside parameterized knot families; no universal exact-target claim used here. |

The Okuda estimate printed in Ohtsuki equation(11), page 403, is n(n−1)(n−2)/15. Taken literally for all n it conflicts with the source's own trefoil/T(2,5) values at n=3,5. Its Japanese February2002 master-thesis body was not located. No corrected range or coefficient is silently assumed, and this reported estimate is not promoted as a validated universal theorem.

## Search coverage and independence

`SEARCH_COVERAGE.json` contains 33 captured query requests covering exact conjecture numbering, Willerton terminology, v3/j3 variants, degree-three crossing bounds, author names, torus restrictions, and recent titles. The initial3 queries were repeated for capture. OpenAlex citation queries returned 17 works citing Willerton2002 and 1 work citing Abe2015; publisher Crossref records and author repositories were also checked. `CITATION_NETWORK_METADATA.json` gives bibliographic coverage and body-access labels. These networks and search results are not exhaustive worldwide priority certificates.

`FIRST_CONCLUSION.md` was sealed at 2026-10-04T16:51:57.439439UTC with SHA256 `7d89628f4ebd20a4f1d7cc70c5bc13a0d40d8c6ba107ac3b4a3c5effa743d593`. That provisional scoped negative finding preceded the decisive inspection. The audit independently downloaded the Fiedler–Stoimenow PDF before sealing, but had not yet inspected its target-related pages. ROOT supplied its page 8 comparative lead after the seal; the exact page 7 specialization was then independently visually checked. Original SOURCES.md, containing appended review opinions, was opened only after the seal and those own decisive source reads, at 16:58:13.205340UTC. The exposure and conclusion change are recorded honestly in `RESEARCH_LOG.md`; FIRST is preserved unchanged.

All publication PDFs, extracted text, rendered pixels, raw web/API bodies, and raw process streams remain outside the repository in `/Users/alec/.cache/pr66_exact_target_priority_20261004`. This folder contains only audit code, reports, bibliographic metadata, hashes and receipts. No candidate/ledger edit, Git/index/ref/native-status command, upload, tracker/PR mutation, external human communication, or outreach occurred.

## Remaining material gaps

1. Identical2000 printed-chapter content and exact earlier1996/1999 availability remain unverified. A reproducible record of a dated author manuscript and independently checked publication metadata suffices to identify prior-result evidence, but must not be mislabeled as a checked2000 page.
2. The page 8even-crossing maximization assertion needs a demonstrated proof or another full-source antecedent before assessing the candidate's even-n refinement separately.
3. The candidate tournament-domination mechanism has not received an exhaustive mechanism-priority search in this exact-target audit. It may be useful exposition or a new proof, but that cannot restore novelty of the already displayed universal theorem.
4. Okuda's thesis and Abe's journal body remain inaccessible here. They cannot support stronger claims than the checked source passages.

The original exact-target priority question is resolved against a new-theorem claim. The remaining gaps limit finer attribution and the even-refinement/mechanism assessment; they do not erase the source's displayed exact-target bound.

## Final artifact and receipt readback

`BIBLIOGRAPHY.json` records precise primary URLs, versions, checked pages and hypotheses. `VERDICT.json` is the final machine-readable decision; `VERDICT_DRAFT.json` preserves an earlier draft. `MANIFEST.json` inventories public audit artifacts and private source/stream hashes, excluding its own bytes to avoid self-reference.

The final custody readback ran at 2026-10-04T17:12:37.472824UTC, recorder PID 78174, subprocess PID 78182, return code 0. Its actual stdout is 1435 bytes, SHA256 `382d99095ffbad45bf3a459fae94a7360d0b39c2d35d3462a084f1b40e7e538e`; stderr is empty. It verified 55 previously completed subprocess receipts and 9 web-tool receipts, original input hashes, unchanged FIRST seal, source-body custody and all recorded stream hashes. Web-tool PIDs are null because the tool does not expose one. The readback receipt itself brings the final inventory to 56 subprocess receipts and 9 web receipts. The four expected nonzero process outcomes remain explicitly recorded. Session bootstrap/read commands without a subprocess receipt are not retrospectively represented as recorded executions.
