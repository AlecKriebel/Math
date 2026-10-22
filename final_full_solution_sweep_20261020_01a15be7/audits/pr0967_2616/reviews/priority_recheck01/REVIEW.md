# Independent adversarial priority/source recheck: PR #967 / record 2616

Audit date: 21 October 2026 (UTC). Target: KOU-21.107. Original head: `b356dec5cb01e5f536b9cfeece56ad08844c03cb`. This review is confined to its own folder. No original scripts were executed, no historical audit reports were read, and no original scientific files were changed. The independent initial comparison was saved before the historical/provenance checks; its later visual correction is explicitly recorded.

## Decision

**The full same result and proof mechanism genuinely preexisted this PR's public creation, within the strength of the directly retrieved Internet Archive evidence. There is no unresolved exact-result/date gap between the 2 October archived paper and the 8 October PR.** The overlap is the complete ordinary-free-ultrafilter Boolean counterexample, including countable dense resolvability and failure of every disjoint finite-block expansive sequence, not merely prior use of the underlying topology.

The current and archived [Results on problems from the Kourovka Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf) are actually byte-identical PDFs: 598,093 bytes, SHA-256 `eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7`. Section 3.44, printed/PDF page 60, contains the full proof. The title page credits Codex gpt-6-astra, Michael Kinyon, and Josef Urban and displays Version 4, 19 September 2026. The independent date bound supported here is **publicly archived by 2026-10-02 01:45:49 UTC**. This review does not promote the internal September date into an independently established publication date.

Fresh authenticated GitHub metadata gives PR creation `2026-10-08T04:43:18Z`; it remains closed and unmerged, at the frozen original head. The October 16 closure's essential content-equivalence and pre-PR-archive claims survive this recheck. This establishes earlier accessible exact content, not ultimate first discovery, personal knowledge, copying, human referee acceptance, or editorial confirmation. The original package's mathematical correctness and finite verification can remain valid while the same theorem ceases to be a new contribution at the PR's publication point.

## Exact theorem and independent derivation

The meaningful target asks whether every countable topological group partitionable into countably infinitely many dense sets has pairwise disjoint finite blocks meeting each nonempty open set eventually. Each open set has its own eventual threshold. Neither first countability nor metrizability is imposed. Dense pieces are not required to be subgroups; blocks are not required to cover the group. The example below is Hausdorff and nondiscrete, so possible separation conventions do not narrow its applicability. The primary Notebook wording omits the word nonempty; both proofs address the customary substantive interpretation and do not exploit the empty open set.

Let U be a free ultrafilter on N, available in ZFC by extension of the cofinite filter, and let G be the group of finite subsets of N under symmetric difference. For A in U, let H_A be its finite subsets. The groups H_A form a neighborhood base because H_A intersect H_B equals H_(A intersect B). A subgroup neighborhood base makes addition continuous; inversion is the identity. Deleting a coordinate where two finite supports differ gives disjoint cosets, hence Hausdorffness. Every A is infinite, so every basic neighborhood is infinite. G is countably infinite and Boolean abelian.

For k >= 0, color a support s by v_2(|s|+1). Each color class D_k contains arbitrarily large support sizes, namely 2^k(2q+1)-1. Given a coset x symmetric-difference H_A, choose such a size at least |x| and append enough distinct coordinates from A minus x. The resulting finite support is in that coset and D_k. Thus the D_k form exactly countably infinitely many disjoint dense sets.

Now take arbitrary pairwise disjoint finite blocks F_n. Infinitely many empty blocks defeat expansiveness immediately. Otherwise discard an initial segment including all empty blocks and the unique possible block containing the identity. Every remaining block contains finitely many nonempty supports. Define M_n as their maxima. For each bound r, only finitely many supports have maximum at most r; since the blocks are disjoint, only finitely many M_n meet that initial interval. Therefore select increasing indices n_j with max M_(n_j) < min M_(n_(j+1)). Form E from the union of even-indexed maximum sets. If E is in U, E misses all odd maximum sets. If E is not in U, its complement is in U and misses all even maximum sets. Call the selected U-member A. For infinitely many selected blocks, every support has its maximum outside A, so that block misses H_A. Since H_A is nonempty and open, the original arbitrary sequence is not expansive.

This deduction uses only freeness, the filter intersection law, and the ultrafilter decision property. It uses no selective or rapid ultrafilter, CH, formal mechanization, or finite simulation of an ultrafilter. The finite-preimage maxima argument establishes the needed subsequence and does not transfer the central difficulty into an unsupported claim.

## Construction-by-construction comparison

| Component | Frozen original REPORT.md | Earlier archived section 3.44 | Finding |
|---|---|---|---|
| Group and topology | Finite subsets, symmetric difference, H_A for ordinary free U | Same | Exact same construction |
| Topological hypotheses | Countably infinite, Hausdorff, nondiscrete | Same | Same target coverage |
| Dense partition | v_2(|s|+1), append coordinates in A minus s | Same | Same explicit countable partition |
| Arbitrary block obstruction | Maximum sets are point-finite; select disjoint sets; parity-union complement | Finite-preimage maximum sets; select separated sets; parity choice | Same mechanism; separated sets are a stronger harmless selection |
| Boundary cases | Empty blocks and identity-containing block removed | Same | Same universal block scope |
| Choice strength | Ordinary free ultrafilter in ZFC | Same, selectivity explicitly unnecessary | No stronger assumption in earlier proof |

The source count 2^r-1 in the rendered paper is correct for nonempty subsets of {1,...,r}. A provisional initial note misread the web extraction as a counting typo. Direct rendering corrected that observation before sealing. No mathematical defect was found.

## Actual-byte and chronology controls

The acquisition receipts record request URLs, final URLs, HTTP status, headers, local retrieval times, exact byte lengths and SHA-256 values. Source bodies, page extracts, images, and raw connector responses remain only in ignored `private/`; public artifacts contain short derived conclusions and hashes.

1. The [raw Wayback replay](https://web.archive.org/web/20261002014549id_/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf) returned HTTP 200 at exactly the requested final URL, with PDF content, no redirect to a newer capture, and the same complete 598,093-byte payload as the fresh origin download. This was actual body comparison, not an inference from URL text or metadata.
2. Its `Memento-Datetime` is `Fri, 02 Oct 2026 01:45:49 GMT`; `x-archive-orig-date` is `Fri, 02 Oct 2026 01:45:38 GMT`. It identifies an archive source WARC, `archiveteam_urls_20261002014730_4e399779/urls_20261002014730_4e399779.1790730937.megawarc.warc.zst`. The raw WARC was not separately downloaded.
3. A fresh exact-URL [CDX query](https://web.archive.org/cdx/search/cdx?url=kourovkanotebookorg.wordpress.com%2Fwp-content%2Fuploads%2F2026%2F09%2Fkourovka-mathematics.pdf&output=json&filter=statuscode%3A200&filter=mimetype%3Aapplication%2Fpdf&collapse=digest) returns timestamp `20261002014549`, the correct original HTTPS URL, HTTP 200, PDF MIME type, and digest `D23DOIESSOEFBPQ4OTLTGP2BK44U6R6G`. Computing SHA-1 over the retrieved PDF and encoding it as Base32 gives exactly that digest. The CDX `length` field is 591,591; it is not used as the payload-size field. The actual body length is measured directly as 598,093.
4. The [archive timemap](https://web.archive.org/web/timemap/link/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf) independently repeats the original URL and same memento time. These are consistency controls from the same archival service, not three independent custodians.
5. Re-extraction and rendering of archived page 60 show the full target and proof; current page 60 is identical. The title page was rendered and inspected. The internal PDF creation date, title-page date, URL month, and origin Last-Modified are supplementary metadata, not the basis of priority.
6. Fresh authenticated metadata for [PR #967](https://github.com/AlecKriebel/Math/pull/967) pins its creation, closure/unmerged state, and original head. The archived memento precedes PR creation by more than six days. The closure comment was read only after the independent initial mathematical comparison.

The web-reading tool could not access the raw archive URL, but direct HTTPS retrieval did succeed. The first comments-connector call used the wrong repository parameter and returned a schema error; the corrected call succeeded. These are recorded acquisition limits/failures, not concealed gaps. CDX and replay evidence are archive service evidence, not an independent cryptographic timestamp attestation; the conclusion is explicitly bounded to that evidence. No date claim earlier than the observed October 2 memento is needed.

## Primary target and topology lineage reconciliation

The fresh [Notebook v48](https://arxiv.org/pdf/1401.0300v48), 1,476,795 bytes, SHA-256 `a646018b69344a06729ba0cfda50d3850e99fd6c04e798f58b6e82aef8c33462`, reproduces the author's pinned exact source. Printed/PDF page 193 has Problem 21.107 and explicitly restricts G to be countable. It has no solution annotation for 21.107. The immediately adjacent 21.106 annotation nevertheless links to the same multi-result mathematical paper. Absence of a per-problem note is compatible with an available proposed proof elsewhere and is not an exhaustive status certificate.

The predecessor 15.80 is on printed/PDF page 97 in v48. It imposes no countability restriction. Its first negative example is the real box product, which is uncountable and even lacks a countable dense subset. It cannot settle 21.107. The additional Zelenyuk remark supplies dense partitions for infinite abelian groups with finitely many order-two elements; that hypothesis excludes the present infinite Boolean group. As written, the remark supplies a density ingredient, not this complete nonexpansive countable construction. This review does not certify the full scope of Zelenyuk's book, which was not directly retrieved.

The fresh [Sipacheva v1](https://arxiv.org/pdf/1612.04878v1), 423,481 bytes, SHA-256 `dddf0ef8a2bd5caae99086b3c0023c7f5b1ce0bf8c65f9d6e6598cf1d73f1f25`, also exactly matches the original source pin. Section 8, page 25 explicitly identifies the Mathias topology with the free Boolean linear group topology and gives the subgroup base H_A. This settles the topology's prior lineage. Pages 26-28 discuss equality with other topologies, selectivity/Ramsey filters, and extremal disconnectedness. Those are different properties and assumptions; no full 21.107 density-plus-block obstruction statement was found in this inspected passage. This is a bounded scope observation, not a claim that no older theorem implies the result.

The fresh official [repository page](https://kourovkanotebookorg.wordpress.com/repository/) has zero literal 21.107 occurrences but includes a broad link to the same mathematical PDF. This reconciles the original author's negative identifier search with the demonstrably earlier full proof. An identifier-only search of a landing page can miss a solution in a multi-result paper. Attribution to Sipacheva repairs topology credit; attribution alone cannot create novelty for the same full theorem already present in the archived paper.

## Adversarial controls and limits

| Attempted falsification | Result |
|---|---|
| Earlier source only treats uncountable groups or weaker resolvability | Fails: section 3.44 states countable G and supplies an explicit countably infinite dense partition |
| Earlier proof assumes a special ultrafilter | Fails: ordinary free ultrafilter suffices and is explicitly stated |
| Earlier source proves only absence of a convergent sequence | Fails: its obstruction handles every sequence of disjoint finite blocks |
| Parity misses maxima but not supports | Fails: a maximum outside A prevents the entire support from lying in A |
| Maxima extraction smuggles selectivity or infinite choice beyond ZFC | Fails: finite-preimage point-finiteness and induction suffice |
| Empty blocks or identity invalidate the extraction | Fails: both sources explicitly dispose of them |
| Source dates are only retrospective metadata | Fails for the needed October bound: actual replay bytes, CDX digest and Memento receipt agree |
| Raw replay silently redirects to later content | Fails: exact final URL, memento time, archived headers, and actual CDX digest agree |
| Earlier paper is mathematically the same only at title level | Fails: every substantive component matches and has a checkable direct derivation above |
| No Notebook annotation proves the target was still unresolved | Fails: Notebook and repository already link broadly to the exact earlier paper |

Bounded web searches used quoted target identifiers, expansive-sequence/ultrafilter phrases, Protasov, and Mathias-topology/density phrases. They do not establish an exhaustive literature census. No secondary search-engine date or status snippet was used to prove priority. This recheck did not reacquire the user's GWS/Zenodo corpus: the parent audit reported fresh 178-row and 197-record/eight-page checks in its DUPLICATE_CHECK.json. Those checks are background supplied by the parent, not independent work claimed here, and are unnecessary for the positive earlier-source finding.

No original checker rerun was necessary to resolve this source audit. `identity_controls.py` is an independently written offline verifier of actual source hashes, PDF scope anchors, archive digest/date consistency, PR metadata, and immutability of all 26 original files. It does not mechanize the infinite proof or decide historical firstness. All controls passed. The complete original-snapshot hash comparison was repeated at the end.

## Disposition and reproduction

Retain the sound proof as a rediscovery/verification artifact with the explicit earlier full-result reference. Do not promote PR #967's same counterexample as a novel solution. The existing closure's narrow priority reason is supported; this recheck supplies no basis for reopening it as new mathematics. Ultimate firstness and referee/editor approval remain unassigned.

For offline replay, run `python3 -I -S -B identity_controls.py` from this folder with its private source evidence available; it writes only JSON to stdout. Before reacquisition, copy the entire review into a new directory and run `source_fetch.py` there, since fresh receipts must not mutate the sealed audit. The manifest pins all source evidence and public review artifacts by byte count and SHA-256. Private source bodies remain excluded from publication. No further outside input is required to settle this bounded overlap/date question, and no outreach was prepared.

Completion estimate for this assigned audit: 100%. The precise remaining limits are historical ultimate-firstness, independent raw-WARC acquisition, and human referee/editor approval, none of which are needed for the supported pre-PR exact-overlap conclusion.
