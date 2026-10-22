# Independent adversarial whole-package review, round 2

**Verdict: mathematics, model, exact reproduction, current priority framing, PDF, archive integrity and privacy checks PASS; one P3 documentation repair is required. This frozen candidate is not a clean whole-package pass.** No mathematical repair was found. The sole actionable finding is a pair of stale current-evidence report hashes in `audit/ROOT_PRIORITY_DECISION.md:25` inside the source archive. The root was informed while files remained frozen. This review is complete at100%; release clearance remains conditional on repair and the parent's required fresh reviews.

## 1. Independent scope and custody

This is a new full review of the supplied candidate, without taking the earlier acceptance, priority disposition or package review as a premise. Work was confined to `reviews/package_02`. Its `.gitignore` excluded `sources/private/` and `tmp/` before retrieval. No live root/publication files, other review folders, Git index/refs/branches/remotes, PRs/comments, deposits, trackers or unrelated shards were changed or contacted. Only the parent was messaged. The observed branch is `main`.

The six operative files and `PACKAGE_RECEIPT.json`, plus all ten source-PR inputs, were pinned at start. Full live-publication inventory and both archive member inventories include byte counts and SHA256 fingerprints. Source ZIP125 entries and kit5 entries have unique safe relative names and valid CRCs; no symlink or path traversal member is present. The source archive was extracted into an ignored local mirror. Only that mirror's builder was executed. The full standalone build, including seven programs in normal and optimized modes, succeeds. All six regenerated operative files and the regenerated receipt match the live bytes exactly under Python3.14.6 and its compression runtime. There was no live builder run and no LaTeX compilation.

Read scope: complete `main.tex`, source `inputs/PROOF.md`, all ten historical source documents, complete three mathematical and three priority reports, their relevant supplementary source/classification notes, complete root mathematical/Fourier/priority notes, all seven checker programs, portable runner and builder, README/license/provenance/metadata, full manifests and mechanical pin/reference/privacy scans. Mathematical results were reconstructed from the defining model. Fresh source inspection and boundaries are in `SOURCE_NOTES.md`; this report does not pretend every inaccessible literature body was read.

## 2. Actionable finding

### P3 — current priority summary cites two superseded report fingerprints

Location: `audit/ROOT_PRIORITY_DECISION.md:25` in the125-member source archive (live counterpart `ROOT_PRIORITY_DECISION.md:25`). It states that its evidence is the current `reviews/priority_01/REPORT.md` with SHA256 `12178b4cf259b1615c2da2c1694657677537e9d6d1cafc9c59158769dc0d1e2a` and current `reviews/priority_classification_01/REPORT.md` with SHA256 `990b9a8be39a71c0140489d6203d0bda5f7ac1a27f7f2e3fe08a5dd63bf5b719`.

The actual frozen packaged reports have, respectively:

- `d1512faf115c8a7ce1a8d98b1c16bc4360ad1eea586d1139e43c880fb1d42c10`;
- `3bc62a76571a2ecdcd851676a8a52a57bd8afa0e4ae7baa7c2b19aa34932a77c`.

These current values agree with their manifests, `PRIORITY_FINGERPRINT_CHECK.json`, and `PACKAGE_EDITORIAL_FIX.json`. The prose hashes identify earlier editions, but are not labeled historical in this paragraph. A reader following the expressly current evidence citation cannot reproduce those hashes. This is a provenance/documentation inconsistency, not a failed proof, altered source input, invalid executable result, or evidence of substitution.

Required repair: replace the two literal current-evidence hashes (or remove redundant literal hashes and explicitly point to the current manifests), then rebuild both archives and regenerate release receipts. Preserve genuinely historical hashes in `HEADER_CLARITY_REVISION.json`, `ROOT_FOURIER_REPLAY.json`'s `previous_code_sha256`, `PACKAGE_EDITORIAL_FIX.json`, and original acceptance-edition records. Refresh the candidate pins and repeat whatever clean-review sequence the parent requires.

I found no additional actionable issue after the complete pass. In particular, the corrected Fourier-note title/opening/closing language and checker headers consistently describe a new model-specific application of older formulas. The supplied materials do not now characterize that argument as a documented2007 solution.

## 3. Original target reauthenticated

A fresh download of the official [EMS OWR13/2004 PDF](https://ems.press/content/serial-article-files/45858) has445532 bytes and SHA256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`. I read Novak's complete contribution printed696–699 and visually inspected697–698. The exact object is normalized anchored Lp discrepancy; the displayed question averages its pth power over the full continuous generator/shift product cube and compares with iid points. Even p is specified in the surrounding definition. Indices are0 through n−1. No prime-n, discrete/rational-generator, selected-generator or no-collision conditioning is imposed. The final existence question on699 is separate.

Thus a single strict reversal at positive integers n3,d1,p4 answers the displayed universal question negatively. Neither expected norms nor good-generator existence follows. This conclusion uses the source formulas themselves, not the corpus title or another audit's scope declaration.

Fresh GitHub APIs authenticate the current PR head `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`. All ten files were independently fetched from that exact head. Every raw byte, SHA256, Git blob identity and current PR-body hash matches the frozen inputs. This authenticates source content now available at that head; it does not certify its public accessibility on10October.

## 4. Full analytic reconstruction

Let T_j={jZ+Delta}, with the stipulated independent continuous uniforms. Conditional on Z, each T_j is a translate of a uniform Delta, so (T_j,Z) has product uniform law. For j≠k, multiplication of Z by the nonzero integer k−j preserves circle measure. Therefore T_k={T_j+(k−j)Z} is uniform conditional on T_j. This proves each pair is product uniform. The same argument coordinatewise proves independence of vector pairs in every dimension; it does not establish independence of triples.

For n3 let U=T_0 and V=T_1. Their law is product uniform, and T_2={2V−U}. On U,V∈[0,x),0≤x≤1/2, a negative2V−U wraps to at least1−x≥x; a nonnegative value is below1 off null boundaries. Inclusion of the third point therefore requires0≤2V−U<x. At fixed U the allowed V interval is[U/2,(U+x)/2), entirely within[0,x), of length x/2. Its area is q(x)=x²/2.

Writing P_k=P(N_x=k), uniform marginals and pairwise independence give E N_x=3x and E binom(N_x,2)=3x². These and P_3=q determine

    (P0,P1,P2,P3)=(1−3x+3x²−q, 3x−6x²+3q, 3x²−3q, q).

The lower-half entries are nonnegative and sum to one. Expanding sum_k P_k(k/3−x)^4 gives

    F=x⁴−(2/3)x³+(2/27)x²+x/27+(4/9)(1−2x)q,
    F_lattice=x⁴−(10/9)x³+(8/27)x²+x/27.

The simultaneous torus reflection (Z,Delta)↦(−Z,−Delta) preserves law. For each fixed x it complements the point count at1−x, outside a finite union of endpoint events of probability zero, so F(1−x)=F(x). Tonelli applies to the bounded nonnegative defining integrand. Exact integration gives2∫_0^(1/2)F=19/1620.

An iid triple has the same general formula with q=x³. Thus the lower-half integrand gap is(2/9)x²(1−2x)², positive for0<x<1/2, and its reflected integral is1/540. The iid value is4/405 and ratio19/16. No approximate subtraction or assumption of triple independence is used. The lower-half q formula is not extended to1; the correct upper-half polynomial is1/2−2x+(5/2)x².

For every n, independently centered Bernoulli variables have fourth single-site moment a−3a², a=x(1−x). The surviving index patterns give[n(a−3a²)+3n(n−1)a²]/n⁴. Integrating a and a² yields(3n−1)/(30n³). I checked both this argument and an independent integration of the entire binomial distribution.

On the increasing no-wrap triangle0<Z<1/(n−1),0<Delta<1−(n−1)Z, empty outer intervals contribute[Delta⁵+(1−Delta−(n−1)Z)⁵]/5. Their unconditioned integral is1/[105(n−1)]. Reflection gives an equal decreasing triangle. For n≥3 their interiors are disjoint, including n3 where the generator closures meet at1/2 only. Omitted contributions are nonnegative. Hence the expectation is at least2/[105(n−1)]. At n4 the lower-bound margin above iid is5/8064. For every n=4+t,t≥0 the sign reduces to25+52t+27t²+4t³>0. This is a universal polynomial proof; finite specializations are supplementary. At n3 the tail bound alone is insufficient, exactly as stated.

For any anchored box of volume v, pairwise independence gives normalized count variance v(1−v)/n. Integration over the endpoint cube gives(2^−d−3^−d)/n for both ensembles and all positive n,d. For n1 the single point is uniform, and for n2 the entire ordered pair is iid uniform in all coordinates. Therefore all defined measurable point-functionals have identical laws/expectations at n≤2; this proves the minimum possible point count, rather than inferring minimum from a few exponents. Collisions remain indexed with weight1/n. Parameter boundaries, wrap/tie lines and fixed endpoint events are null. No positive-measure set is conditioned away.

The strongest verified result is the full negative answer with the exact n3 value/minimality and every-n≥4 second mechanism, together with the stated all-n,d equality controls. There is no remaining mathematical gap in those claims.

## 5. Newly authored independent exact control

`check_arrangement.py` was written afresh here without importing or copying another package control. It uses standard-library exact Fraction arithmetic and a different implementation from the supplied affine-strip antiderivative checker: start with the complete unit square, generically split convex polygons by all modular-wrap lines jZ+Delta=k and all possible ordering-change lines mZ=k, and keep positive-area pieces. Every split conserves exact area, and final areas sum to1. On each cell an interior rational witness identifies floors and order; affine vertex checks certify those inequalities throughout the convex cell.

For sorted points s_k, direct endpoint integration expresses discrepancy as a finite difference of affine(p+1)th powers divided by p+1. Each polygon is triangulated. If an affine L takes vertex values a,b,c on a triangle of area A, exact simplex integration is

    integral L^m = 2A/[(m+1)(m+2)] × sum_(i+j+k=m) a^i b^j c^k.

The code evaluates the complete homogeneous polynomial by its generating-product recurrence. There is no fitted polynomial degree, quadrature, Monte Carlo, symbolic library, external result file or target fraction used to generate the integrals. Expected target values are compared only after integration. Primitive monomial/constant checks test the simplex formula.

It produces15 full exact lattice/iid moment pairs for n1–5 and p2,4,6, with cell counts1,2,6,16,30 respectively. It independently obtains19/1620 and supplementary139/17280, the exact gap/ratio, all tested second moments, and n≤2 equalities. It separately integrates the empty-tail triangles using the same generic simplex primitive, checks rational margins at n2,3,4,5,10,234,1000 and the positivity polynomial. These finite calculations corroborate, and do not replace, the universal proofs above.

Both ordinary and optimized runs pass2778 explicit requirements with byte-identical JSON. Nine adverse controls distinguish a deleted positive cell, replacing the whole ensemble by one no-wrap region, normalization loss, a triple-iid substitution, a fixed zero generator, misuse of the weak n3 tail bound, double counting and invalid n/odd-power input. The explicit forced-failure mode exits1 for the intended mathematical failure in both modes. There are no Python assertions. Results and full cell tables are in `RESULTS.normal.json` and `RESULTS.optimized.json`; run/failure evidence is in `ADVERSE_AND_RUN_RECEIPT.json`.

## 6. Whole-package executable and archive review

All seven supplied programs were read in full. Their operations use exact standard-library arithmetic for the relevant finite checks. The runner pins input/checker/expected/auxiliary bytes, rejects assertion nodes and compares entire parsed result objects; only the declared two historical parent receipt wrappers select their `result` fields. It executes both ordinary and optimized modes and the designated real forced-failure switches. I found no mathematical result field silently discarded. The supplied checks substantiate the described algorithms; their success is not formal proof certification.

The extracted standalone builder reran all fourteen ordinary/optimized jobs, four designated failure guards per mode, authenticated the frozen six review manifests and72 authored files, checked the operative source/PDF QA pins, generated provenance/source manifest, and deterministically recreated both archives. Its fixed member lists exclude this and previous package reviews and future publication receipts. Rebuilt six-file hashes and the complete `PACKAGE_RECEIPT.json` are byte exact. All124 non-manifest source members match `SOURCE_MANIFEST.json` and the125-entry ZIP inventory. All ten source files match live and freshly fetched source bytes. The original nine-member input manifest matches. Kit payload PDF, source ZIP, metadata and README are identical; its portable deposit manifest differs only by flat file paths and has identical metadata. The operative PDF is an explicitly frozen input; source-to-PDF consistency was checked visually/textually rather than by silently compiling it.

New hostile tests in ignored mirrors reject input corruption, checker corruption, expected-result corruption, a re-pinned false expected result and a re-pinned checker containing an assertion in both ordinary and optimized modes. The first three fail hash checks; the latter two fail full result comparison and AST protection, respectively. The test restores every scratch mutation. All ten rejections are recorded. These checks test actual runner behavior, not just source inspection.

`ARCHIVE_INVENTORY.json`, `LIVE_INVENTORY.json`, `REBUILD_AND_INTEGRITY.json`, `CONTENT_SCAN.json` and `PIN_REFERENCE_SCAN.json` preserve inventories and checks. Of161 uniquely resolved nested JSON pin references, the ten apparent mismatches are six explicitly original acceptance editions, three explicitly previous checker/result editions, and one suffix-resolution ambiguity between release README and source-input README. Fresh remote authentication resolves the last in favor of the historical source README. None is an additional current-pin defect. Separately searching prose hashes found the single actionable current-evidence paragraph above and correctly labeled historical revision receipts.

## 7. Priority, attribution, chronology and limits

The [later Ferudun primary PDF](https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856) freshly matches182528 bytes and SHA256 `edb268431856eef5d6eb00e730d1a27a7e91a15d76186b506168f259dbbb174c`. I read the actual definitions, relevant gap formulas, n3/n4 theorem/proof and progression-event argument. The central n3 overlap and same rare-progression mechanism are valid. Its broader dimensions/exponents are accurately credited; I have not certified all its computer-assisted cases. Its PDF size/MD5 agree with the fresh canonical Zenodo file list. Current release abstract, related-work paragraph, bibliography, README, metadata and provenance prominently credit exact overlap and broader scope.

Fresh APIs confirm PR creation10October2026 11:34:20Z and sole reviewed commit11:33:05Z, and Zenodo record creation14October14:58:42.560423UTC with publication date14October, version1.0 and preprint type. The present note is dated17October. Current repository publicity does not certify historical visibility, and none of these timestamps establishes worldwide first discovery/publication, intellectual dependence or awareness. Current prose states those limits. Historical10October source files remain unchanged and explicitly superseded on current literature summaries. I found no improper continued-openness assertion or first-priority claim in the current release narrative.

I freshly checked [Su2000](https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf) at its nonzero cumulative-discrepancy coefficient identity, and [Anderson et al.2007](https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf) at the exact one-sided kernel definition and complete Lemma2.1 proof. The source uses a centering constant affecting only frequency0; its supremum-discrepancy theorem is not substituted for an L4 theorem. The new application directly integrates the anchored function's first coefficient, applies Hölder, cancels the shift phase and averages the continuous-generator Dirichlet fourth moment. Orthogonality counts a+b=c+d with0≤indices<n, giving(2n³+n)/3 and the lower bound(2n²+1)/(48π⁴n³). The rationalπ<22/7 certificate and shifted quadratic prove reversal for every n≥234. All constants/endpoints and the distinction from p2 were checked. No unsupported central lemma remains in this application.

These old generic formulas are method sources; the examined statements do not themselves present the target model's averaged fourth discrepancy comparison. The model-specific bridge is supplied by the new audit. That distinction is mathematically and historically coherent. I do not infer first recognition of the bridge or that no earlier covering theorem exists. The author-hosted11February2010 volume-II draft repeats the exact question as OpenProblem41 on69, visually confirmed, but that label does not certify current openness or the final book edition's content.

The supplied broad/focused/classification reports frankly retain inaccessible full bodies/final editions and incomplete citation coverage. This package-stage review performed three supplementary searches, including a noisy exact-fraction search; they are not added into a worldwide exclusion count. In particular I do not certify all of Hinrichs/Weyhausen2012, original Sugita/Takanobu2000, Sugita2002, Janson1988, Cesaratto/Vallée2012/2016 or unavailable final-publication comparisons. No exhaustive priority certificate is issued, and no older-source exclusion is inferred merely from an abstract/title or failed retrieval.

## 8. PDF, destinations, metadata, licensing and privacy

The PDF skill was read and its read-only render/inspect workflow applied. Every one of the four operative pages was rendered at110dpi and visually inspected individually. Text, mathematical symbols, fractions, headings, bibliography, page numbers and equation labels are legible. No clipping, overlap, missing glyph, extra page or broken reference placeholder was found. The last equation on page2 is low but fully visible and clear above its page number. The source and reading copy agree on title/author/ORCID/date/version, equations/claims and chronology/credit/AI-status prose.

The PDF has19 named destinations and10 links: six internal destinations all resolve and four outbound URLs match the intended ORCID, source DOI, overlapping-preprint DOI and PR. All annotation rectangles lie within their pages. Eight distinct metadata/ORCID destinations returned HTTP200 and correct primary destinations; `LINK_CHECK.json` records redirects rather than treating redirects as broken links. PDF metadata has the correct title/author/subject and no unintended personal filesystem path. `PDF_INSPECTION.json` records the detailed findings.

The README, Zenodo metadata/deposit metadata, kit metadata, provenance and note agree on the exact model, values, full-negative scope, minimality, all-n tail consequence, current overlap and release status. ORCID and author match the supplied user metadata; no affiliation or human review is invented. The external Ferudun DOI is a reference, not presented as this note's DOI. The source archive clearly distinguishes source-PR and operative-paper editions, and the changed8 inline delimiters/original acceptance hashes are preserved as history.

License terms cover original authored work under CC BY4.0 and explicitly retain third-party rights. The125-member archive contains the author's own reading PDF, authored TeX/Markdown/JSON/programs/manifests, and no third-party article PDF/body, HTML, raw API response, render, cache, source ZIP or downloaded dataset. The kit contains only its prescribed five payloads. Privacy scans of every textual member found no credential pattern, email address or local home path, and no forbidden private/tmp/Git/cache member. Source receipts provide bibliographic metadata and fingerprints, not copied source bodies. The package accurately discloses extensive AI use and unrefereed status; internal AI checks are never represented as human peer review or formal certification.

## 9. Conclusion and reproducible record

One P3 repair is required for the current-evidence hash paragraph. No other actionable finding was identified. The mathematical full-negative conclusion and all stated control/generalization claims survive independent adversarial reconstruction and exact computation. Archive integrity, portable rebuild, metadata, credit/priority limits and visual presentation otherwise pass. This is an independent AI package review, not journal acceptance, a proof-assistant certificate, historical novelty certification or authorization to publish.

Reproduce the new control with `python3 -B check_arrangement.py` and `python3 -B -O check_arrangement.py`; append `--force-failure` to exercise the deliberate rejection. `check_runner_guards.py` uses only ignored scratch copies. To replay the frozen package, extract its pinned source ZIP into a new ignored folder and run its `python3 -B build_package.py`; do not run the live builder during a review. `audit_package.py` checks the resulting mirror at `tmp/mirror` against the frozen live release and receipts. The review's own fingerprint manifest excludes itself and all ignored/private files.

The following end-custody table is generated after completing this report. Exact start/end custody, including all ten originals and the receipt, is in `END_PINS.json`.

| Operative file | Bytes | Start = end SHA256 |
|---|---:|---|
| main.tex | 11218 | `4e481ec84b1be42a9885df393e0fce065f489eea6f0f2e98ed0f84298f9e3d85` |
| output/pdf/random-lattice-counterexample.pdf | 63159 | `a731f3d7db3ffb3644bf6ab3898159e00508a922ce2ec8dd4e6283cf994e6810` |
| output/random-lattice-counterexample-source-and-verification.zip | 277715 | `7130b82f6b7860060d3fd1c2da9e6b6ede55be9c557929b79eaca8495c1e66a9` |
| output/zenodo-upload-kit.zip | 328480 | `b7d39755c57706b3b0d01fb7c7e02301123e62314383f73c88689197b3046daf` |
| zenodo-deposit.json | 4491 | `e815f916b925e670adb1233620a33df18a4caf64d046af69d8566268fb578d2a` |
| zenodo-metadata.json | 4160 | `2c89b91b761f6b2ca0f2f1e7c653ab69bd141e08c10e76be61801fd8e0226957` |

Receipt SHA256 `aa9b4bfe4bb4b65eca192d3221f00b998b768eb8b3ae7cc20be8e116eb7962f0` also remains unchanged. Every publication-directory file, all ten originals and branch main are unchanged at 2026-10-17T21:26:22.990665+00:00.
