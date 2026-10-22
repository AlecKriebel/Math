# Independent review of ordered PR classifications #491–#581

Verdict: **PASS for the bounded classification and existing-publication coverage task, with the limits below.** No substantive classification correction, missing full-solution candidate, duplicate target publication, or required provider mutation was found. This is not a new mathematical or priority clearance, and it does not complete the repository-wide sweep.

The review checked all 91 numbers inclusively against actual pinned Git comparisons. The effective outcomes are 55 `unsolved`, 32 `already_solved` (including #523's later explicit withdrawal), and four already published results. Every PR has a usable corresponding explicit status; there are no missing-status cases in this interval. The review never inferred eligibility from titles alone.

## Evidence and independence

`capture_and_pin.py` captured a coherent STATE/journal/inventory prefix, all 91 individual dispositions and eligibility receipts, and required publication/withdrawal receipts. It independently computed every complete `base...head` path set, actual added QUEUE row, corresponding problem identity, file count and filename inventory. All equal the recorded scope. Each PR has exactly one actual added own-problem row. The 244 captured Git blobs include every changed scientific file for the six custom-folder cases and four publications, and each actual QUEUE head. `GIT_BLOB_INPUT_MANIFEST.json` records exact immutable commit/blob/digest custody.

A fresh authenticated GraphQL read checked all 91 live PRs, including current body, state, draft flag, head/base, timestamps and merge commit. There were **zero differences** from the captured inventory. This is a dated observation rather than protection against future changes. `final_input_recheck.json` separately lists later changes to mutable local cursor/journal inputs; immutable reviewed receipts remain unchanged.

The checking programs were written for this review. They do not invoke the root classification helper or treat earlier reviewers' verdicts as authority. No mathematical verifier was run for an excluded negative-status PR or an already published result: the user expressly requires those results to be skipped. Checks here concern scope, identity, supporting-material preservation and accounting.

## Explicit exclusions and adversarial cases

There are 86 ordinary own-problem explicit negative statuses: 55 `unsolved` and 31 `already_solved`. Their actual complete changed scopes belong to the corresponding problem. Under user rule 2 they are excluded even if a body contains a complete partial theorem, historical reconstruction, strong quantitative claim or an old pending-audit label. The negative status was not silently promoted to a novel full-solution claim.

Six nonstandard folders were checked through actual changed file bytes and their status/README entry points, rather than assumed to fit `attempts/<id>`:

- #493 /2302054: `function_theory_2302054`, explicit `already_solved`; a credited Toppila1983 reconstruction of Rubel2.54, no new-solution claim.
- #499 /2305039: `function_theory_2305039`, explicit `unsolved`; finite p>2 optimal radii remain unresolved despite exact smaller-p, monotonicity and asymptotic partial results.
- #508 /2914: `kirby_ribbon_asphericity_2914`, explicit `unsolved`; the universal Fox-boundary injectivity/certified-kernel gap remains.
- #538 /2302004: `function_theory_2302004`, explicit `already_solved`; the Julia-ray distinct-exception question is different from neighboring #491/2302005. A complete direct witness reconstruction is not a new-resolution claim.
- #548 /2304009: `function_theory_2304009`, explicit `already_solved`; known diameter counterexample, with later asymptotic questions outside scope.
- #555 /2306010: `function_theory_2306010`, explicit `already_solved`; credited prior Guo–Hu counterexample, with no novelty claim.

Each custom case changes only its exact own folder and the canonical QUEUE path, and each own row carries the recorded explicit negative status. No stray changed folder or second problem row was hidden by the cached classification.

### #523 withdrawal

#523 is the fifth historical `claimed_solved` row. It is not dismissed merely because the PR is closed. The independently recovered canonical QUEUE at immutable main `d6ca2e4dbb7355aec650ca17d3cb32575d8c64cf` has the exact `already_solved` correction for 30004064. Its whole SHA256 is `49caed98c5ac6c4fc6723e4a9aabd345331cabe922426a2dd8025386233f8073`, agreeing with the receipt. The fresh live PR remains CLOSED, unmerged, with unchanged head. The freshly fetched [correction comment](https://github.com/AlecKriebel/Math/pull/523#issuecomment-6138397305) has exactly the recorded body SHA256 `5cf11550be76d2f6cb8998dee772d06ccc7ca816839b24c6466ca84f508a0836`.

The correction administratively withdraws the novel full-solution claim on prior-work/scope grounds and explicitly separates numerical/auxiliary variants. The cited Ferudun DOI remains a documented prior-work lead for this review; its theorem and chronology have not been newly certified here. The current explicit exclusion is therefore supported without reopening substantive mathematics or inventing an additional publication obligation.

## Four existing publications

A fresh **Google Workspace CLI values get**, not a cached ledger or title-only search, read the actual four-column sheet. Each target has one unique primary-DOI row. Independently fetched public Zenodo records are published, all four DOI links resolve with HTTP200 to the exact canonical record, and all eight public files were downloaded. Byte sizes and MD5 checksums match the provider and SHA256 hashes match the root's captured public-download evidence.

All four ZIPs pass CRC, safe/unique member checks, and strict outer positive manifests. Every payload byte count and SHA256 was checked; no extra or omitted member is concealed by a checksum list. The combined totals are 448 members, including four manifests, hence **444 positively verified payloads**. Every archive contains actual TeX manuscript source and verification code. All **61 changed original scientific PR-head files** occur byte-identically in the corresponding archive's `original/` tree. This is stronger than accepting a README's statement that originals were preserved.

| PR | Problem | Public DOI | Ledger row | PDF | ZIP members/payloads |
|---|---|---|---:|---:|---:|
|521|30003571 / OWR-15582-005|[10.5281/zenodo.23331080](https://doi.org/10.5281/zenodo.23331080)|67|4 pages,72,986bytes|40/39|
|533|30001182 / OWR-3392-009|[10.5281/zenodo.23333353](https://doi.org/10.5281/zenodo.23333353)|78|3 pages,72,019bytes|60/59|
|563|2306072 / AMR-022-6072|[10.5281/zenodo.23383961](https://doi.org/10.5281/zenodo.23383961)|90|5 pages,92,949bytes|255/254|
|570|30006605 / OWR-14299911-007|[10.5281/zenodo.23385145](https://doi.org/10.5281/zenodo.23385145)|95|5 pages,72,287bytes|93/92|

The actual public PDFs were text-inspected for author, theorem, objects, parameters, scope and attribution. The archived current manuscript, original authored scope/proof entry points, public metadata and full four ledger cells were compared. Exact hashes and file-level evidence are in `publication_integrity_checks.json`, `public_pdf_identity_receipts.json` and `original_blob_comparisons.json`.

### Original-problem and result identity

Fresh official primary PDFs were independently recovered, hashed and read at the relevant statements; their full texts remain private review evidence. These were target-identity checks, not new proof or priority audits.

- **#521:** Naumann's [OWR39/2017 report](https://ems.press/content/serial-article-files/46702?nt=1), printed2440–2443, explicitly leaves total-space positivity preservation open at2443. The published result and row67 consistently specify the probability-normalized defining flow, E=O(1)⊕O(1) over P1, positive O(2,2) initial data, and curvature −1/96 at (log2)/2. The known flow construction and the Griffiths conjecture are not relabeled as solved new targets. The manuscript explicitly distinguishes its defining published equation13 from other displayed normalizations. This review does not newly verify that analytic normalization argument or its imported existence theorem.
- **#533:** Liebscher's [OWR09/2009 contribution](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1), printed540–541, defines unrestricted extremal-exchangeable independence and asks in item1 whether retaining the ambient algebra is necessary. Original PR, paper and row78 match the state-preserving C4-to-M4 coordinate-subalgebra counterexample. The separate algebraic nonextension issue is distinguished from C* lifting, and faithful/tracial/fixed-marginal/normal-W* variants are not silently included. This is a different mathematical target from tensor-core generation; shared quantum terminology does not establish duplication.
- **#563:** [Hayman–Lingham v2](https://arxiv.org/pdf/1809.07200v2), printed143, Problem6.72, asks two monotonicity questions about a support-point omitted arc. The record, note and row90 consistently address every actual global maximizer of Re[a2+i10^-24(a4−3a3)], with negative answers for argument and signed/unsigned radial angle. They do not merely produce arbitrary differential trajectories. The record and row expressly retain incomplete priority clearance for the Duren commentary and Hibschweiler1995. That unresolved literature limit is not suppressed by this coverage verdict.
- **#570:** Ducoffe's [OWR8/2026 contribution](https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1), printed504–507, defines multiplicative profiles at504 and asks OpenProblem1at505. The record, note and row95 consistently give the finite exact-operation O(n log^5(2n)) promised-unit-edge-median-graph algorithm for radius, a center and all centers. Additive algorithms and the optimization mechanism remain credited. The neighboring locality question, graph recognition, arbitrary edge lengths and infinite encodings are not bundled into the claimed resolution.

Broader semantic ledger searches were also examined. Other positivity rows concern graphical-model MTP2, SOS cones, moment certificates and wave control; other generic independence hits concern unrelated objects or priority disclaimers. The other slit-related row is FunctionTheory6.86, not6.72. The weighted-median-graph search finds only its target. Exact source IDs, mathematical objects and conclusions, public PR identifiers, canonical record/DOI and manifests establish identity; titles alone were insufficient. No outside-range result was substantively audited.

### Record details that do not require a new publication

Row67 lacks a PR URL in Notes. This is not a missing result or ambiguous publication: it has the exact original-problem URL, title, precise mathematical statement, DOI and public record. The public record's `isDerivedFrom` identifier explicitly names #521, and its manifest binds the problem/PR/head. The schema has no separate PR column, and 29 other existing Notes cells also omit PR markers. I find no required coverage repair on this evidence; adding a link would be optional enrichment, not a reason to manufacture a duplicate or reopen mathematics. The association is independently preserved in this review.

The #521 legacy archive does not contain `metadata.json`; its actual `paper/README.md`, `paper/positivity_loss.tex`, code, originals and complete manifest are present. Absence of that optional file is not absence of source/supporting materials. For #533, the archived and public descriptions differ only by the apostrophe in “Liebscher's”: the archive uses U+2019 and the public record uses ASCII. This explicit PR-specific comparison preserves all mathematical wording, qualifiers and disclosures and is recorded in `archive_metadata_comparison_pr0533.json`; exact byte equality is not falsely claimed. The other archived metadata comparisons pass exactly.

## Boundaries and preservation

No provider was changed; no PR was commented on, closed, merged or published, and no spreadsheet row was appended or updated. No outside individual, unrelated agent or other chat was contacted. No skills-generation command was invoked. Writes stayed in this new review directory. The canonical snapshot commit was fetched by exact SHA as a permitted immutable Git object with `--no-write-fetch-head`; no checkout, branch/index mutation, stash, reset, clean or ref rewrite was used.

Preparatory script failures and their narrow fixes are disclosed in `DEVELOPMENT_NOTES.md`. They produced no verdict or provider mutation. The final successful scripts/checks, exact inputs, raw private provider/source evidence, and all outputs are sealed. Public checkpoint projection should include reports, authored assessments, receipts, scripts and manifests, while leaving raw full ledger, third-party PDFs/extracts and public binary downloads in this local private review corpus.

There is no globally atomic provider snapshot or promise against later concurrent changes. The root must retain its final live-head/ledger/publication reconciliation. This verdict does not establish mathematical correctness or novelty afresh, certify worldwide firstness, authenticate cited unretrieved priority leads, or review PRs outside491–581. Within the requested bounded classification/publication-coverage task, no material objection remains.
