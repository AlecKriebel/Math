# PR399 bounded record URL identity repair

This is a local operations repair for P399-03-OPS-01. It closes the reproduced record URL duplicate-append gap in the finite offline controls. It is not scientific clearance, publication authorization, or a live publication outcome. `publication_ready` remains false. Root must verify this new seal, replay the controls, obtain NEW complete history-free package review04, and decide the next step. No `ROOT_PUBLICATION_CLEARANCE.json` was created or edited.

Only two of the seven canonical helpers changed: `ops_binding.py` and `record_publication_ledger.py`. The other five helpers retain their exact previous bytes. `CURRENT_HELPER_BINDING.json` binds all seven. `REPAIR.diff` gives the entire difference from the preserved156 generation. The final parser SHA256 is `a2bed4d6a5d5634d9a449b8ff88124c199b650aff6ee2b5dbba93741b9d6f358`; the final ledger helper SHA256 is `ed820c9a9b37c667f821555542f78b8084f870f3d5c0516eeb125e8cda01bffd`.

## Exact defect and preserved counterexamples

Complete final reviewer03 REPORT (32,994 bytes), VERDICT, the actual `novel_identity_controls.py`, and its results/public route evidence were read. All26 entries of its seal `e797d9c8580b3dbaf64ca568e1a7516346269f9248eb1fdbeefb0562a06cfbbb` were checked. Reviewer03 found no additional mathematical repair and resolved the earlier DOI-case/family/directory findings, but identified a material operations gap. Its full report SHA256 is `fafe18788d7a4dd1510b545db935213a4c5ed95c9624c29fdc8e47d3aee49b6e`.

The frozen156 helpers silently missed official record URL variations involving singular/plural routes, default ports, dot segments, trailing separators, query/fragment suffixes and export subresources. The actual collector→gate→append→readback pipeline appended a second semantic target row and returned false uniqueness for nine combinations in each of four cells, with or without a contradictory non-target row digest:72 failures per mode. The exact frozen reviewer program was newly replayed against preserved old helper bytes in normal and optimized Python, reproducing72 false-unique cases plus7 recognized rejections per mode. This old evidence is retained under `old_counterexamples_normal` and `old_counterexamples_optimized`; it has not been rewritten as successful current behavior.

The old program adaptation changes only output/scratch custody, exact frozen-loader selection, and the receipt lookup for frozen helper hashes. Its provider/network/process traps remain active. The original reviewer program is copied unchanged under `review03_evidence`; its SHA256 is `d7241cf5c680600093f5399df33ce8551bfcfbf61f4386d40c9f0e33735f9791`.

Reviewer public evidence records nine authenticated GET combinations for unrelated record23333353. I read that evidence JSON and root's selected body/identity-field verification receipt. I did not newly download or inspect those HTTP bodies. This repair's larger lexical benchmark is not a count of authenticated HTTP duplicates. Some plural/API slash HEAD and DOI-dot-segment routes were reported404; those observations are not converted into generic URI-equivalence claims.

## Shared mechanism and exact row semantics

The existing embedded `ops_binding` identity mechanism now classifies complete URI authority and route components. It recognizes strict official `zenodo.org` and `www.zenodo.org` authorities, ASCII host/path case, HTTP/HTTPS default ports (including leading-zero spellings), protocol-relative/bare forms, dot segments, repeated separators, bounded whole ASCII positive record IDs, query/fragment tails and explicit record subresources. File descendants, export formats, draft/version and other enumerated record subresources produce conservative parent-record review leads. Unknown recognized official routes, malformed authorities/ports, userinfo, trailing-dot hosts, unsupported transports, encoded authorities, impossible IDs and unknown subresources require root identity review and stop processing. Oversized recognized URIs stop processing. Whole-token and authority parsing avoid matching official-looking substrings inside a different host, path or query. Bare-host suffix lookalikes and Unicode lookalikes do not become target IDs. Long bare userinfo is checked as a whole authority; URI lexical prefixes are bounded rather than using an unbounded prefix expression.

These record URL classifications are conservative blockers. They do not certify that a route exists, redirects, or represents mathematical identity. ASCII DOI equivalence and valid unreserved percent decoding remain separate from reserved/nested encodings, record URLs and family leads. DOI suffix leading zeros remain literal: `10.5281/zenodo.0999` is not numerically cast into `10.5281/zenodo.999`. Leading-zero record URL IDs may be review leads only. There is no Unicode casefold or arbitrary hostname capture.

Existing typed target/concept/version-parent extraction remains unchanged and conservative; it does not assert that every version proves the same result. Existing exact eleven-source/five-payload and QUEUE/branch/main/merge bindings, selected recursive directory inventory (including empty trees), durable exclusive fsync intents, and no-blind-retry behavior remain unchanged. All530 earlier regressions pass against the final canonical bodies.

Every ledger row cell is evaluated. The collector and gate already performed the stricter all-row identity scan before target-ID shortcuts; that contract was retained. The independent appender still checks identities separately before append and on readback. Standalone `matches()` now evaluates `target_in_row` before its model-term shortcut, so a recognized lead in an early cell cannot hide an ambiguous URL in a later cell. Target/family matches and ambiguities take precedence over purported non-target row-digest exemptions. Unknown recognized official URLs reject even before a target deposit ID exists.

Idempotence still requires the exact desired literal four-cell row. An alias row or a changed row requires reconciliation/repair of the existing row and never authorizes append or a normalized rewrite. The controls cover exact canonical idempotence, genuine absence with one intended append, duplicate aliases, combined aliases, family aliases, independent upstream-gate bypass and aliases introduced during readback. No actual row was changed during preparation.

## Cached OWR bibliography compatibility

The root-observed actual ledger contains an unrelated bibliography of the form `OWR 10/2016 pp.479–481` with the same-cell source DOI `10.4171/OWR/2016/10`. A broad bare shortDOI detector interpreted the report-number/year text as an unresolved shortDOI. The repair narrowly recognizes this lexical role only when report10/year, a bounded non-reversed page interval, and the exact matching primary OWR source DOI occur in the same cell. Only that report-number/year span is masked for short-name ambiguity detection. This is a citation-role rule, not a trusted row digest, a numeric-code blanket exemption, or a mathematical audit of PR826.

A mismatched source year/report, a DOI suffix extension, reversed pages, absent source DOI, bare `10/2016`, an explicit shortDOI resolver link, or a second unresolved short name still rejects. Explicit three-part dates and unambiguous parenthesized/TeX fractions remain ordinary text. Genuine target URLs in the same bibliographic row retain precedence over exemptions. All25 bibliography/short-name controls pass, including those negative cases. The narrower rule preserves uncertainty for an isolated ambiguous numeric shortDOI rather than guessing its identity.

All176 rows of the exact cached whole-sheet response SHA256 `d513b4cfef1ca47f654a6f677693ae7186f3f193f6d892c5e043ad318c0061b3` were evaluated in both modes against the final helper and parse without ambiguity. Only aggregate compatibility receipts are public here; the account/ledger full bodies remain in ignored private custody. This is cached-data compatibility, not a fresh live collector/gate, root row reconciliation, or proof that the cached rows remain current. No spreadsheet data or unrelated metadata was rewritten to accommodate the parser.

## Meaningful controls and replay custody

All final canonical controls pass in both normal Python and `-O`, with zero actual provider attempts:

| Current suite | Count per mode | Evidence |
| --- | ---: | --- |
| New actual-function pipeline/independent appender controls |818| `CURRENT_CONTROLS*.json` |
| Previous identity pipeline controls |123| `prior530_canonical_*/integrated_controls` |
| Previous targeted identity/directory controls |83| `prior530_canonical_*/repair_controls` |
| Original regression families |324| `prior530_canonical_*/replay_regressions` |
| Exact unchanged root metamorphic benchmark |303| `ROOT_BENCHMARK_canonical_*.json` |
| Total current obligations |1651| `TEST_SUMMARY.json` |

The new818 controls consist of442 recognized-alias pipeline/independent/readback cases;324 malformed or ambiguous official-URL cases, including preallocation and independent/readback checks;21 nearby identity/foreign-host negatives; and31 exact-row, family, bibliography and short-circuit controls. The original9×4×2=72 complete pipeline counterexamples are an explicit subset. Services, account metadata and clearance/public-file prerequisites are synthetic. The collector, account pagination, gate reconciliation, independent appender, literal row logic and readback functions themselves are actual canonical functions. Socket/process/Zenodo access is trapped, and the synthetic append stub requires the actual durable intent before the one intended append. Negative cases verify no append and no false uniqueness receipt.

The old530 test program bytes and expected outcomes remain unchanged. The wrapper redirects output/scratch custody and current helper selection, while old frozen counterexamples keep their original source generation. The earlier sealed truthful recursive-directory fixture adapter is retained byte-for-byte. There is no new shape adaptation, production-guard bypass or relabeled expected verdict. Their exact sources are hash-checked against the preserved156 manifest before execution. `replay_530.py` documents this wrapper explicitly.

The unchanged root benchmark has296 positive conservative-lead-or-explicit-ambiguity obligations and7 nearby negatives. Final canonical results are294 leads,2 explicit ambiguity rejections,0 misses, with all7 negatives distinct. Frozen old results were27 leads and269 misses. Those269 are bounded lexical failures, not269 authenticated HTTP duplicate publications.

Historical reproduction72+7 per mode is additional evidence and is not added to the1651 current passing obligations. Cached176-row observations are also counted separately. `READ_ONLY_REPLAY_*.json` records actual normal/optimized execution of the final replay runner in new private folders; it reran all1651 current obligations, old72+7 and cached176 compatibility checks without writing audit outputs. The runner checks the required counts from actual receipts.

During development, a synthetic independent-appender fixture lacked its private output directory; this was corrected by creating the fixture directory. An actual proposal gap for an empty official authority was caught by its new negative control and corrected without changing the expected rejection. Additional malformed bare-authority and foreign-host boundary checks were added before the final freeze. The first local installation and later refinement are both recorded; `CURRENT_HELPER_BINDING.json` and final tests bind the final bodies, rather than treating the initial installation receipt as the final source generation.

## Preservation and source provenance

Before canonical edits, all156 artifacts of seal `53aeb70604d4f28f4986cf2e30f5cb90ccd900de7fff96a2d60bb31c03be886f` were copied audit-relatively into `pre_record_url_binding`, along with that exact manifest and checksum. Those bytes remain unchanged. The old42/26 preparation lineage is preserved recursively;64 additional stable top-level paths restore the old verifier's exact context without overwriting its newer seven frozen helper bytes. The exact preserved156 verifier was actually run successfully: all156 verified and historical42+26 reconstructed. No old reports, tests, manifests, seals or canonical-looking historical copies were regenerated.

`IMMUTABLE_INPUT_BINDING.json` rechecks eleven originals against SOURCE_SNAPSHOT byte hashes and blob-form SHA1, the five exact repository/publication payloads plus three separate preparation notices and RELEASE, original preparation/repair seals, review03's26 artifacts and root receipts. It rechecks root lead reconciliation SHA256 `af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39`. This repair did not issue a new Git command or reread provider branch state; the earlier actual parent/head/QUEUE checks are preserved, and root's original399 head `08fc8833a56358d505e0b33ae1debe44ec320add` remains the pinned contract. No Git/index/ref/branch/PR operation was performed.

Root's current read-status receipt bytes are copied into this repair and bound by `ROOT_READ_STATUS_BINDING.json`. Parent-authored complete-read/replay claims are identified as such. They do not become a new scientific clearance for repaired bodies. Reviewer03's prior verdict continues to be repair-required for its old binding.

The optional frozen280 comparison was first verified at all390 entries under seal `b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d`, after the own399 proposal had already been built and benchmarked. Its full report/parser/four-helper diff were read; exact selected source bytes are copied read-only. The comparison suggested the standalone `matches()` ordering; the whole280 helper bodies and exemptions were not substituted. Own399's stricter collector/gate scans, family typing, bindings and intents were retained, with separately authored route/subresource and OWR-context handling. The final comparison receipt records any change in that optional source after initial verification. Source280 remains subject to its own fresh review and is not publication clearance. No280 file or unrelated agent was edited/contacted.

Local `.zenodo-state` scopes were separately inventoried before and after this repair:241 direct JSON files and314 recursive regular files. Both sorted path/size/SHA256 aggregate inventories are unchanged. Their respective digests are `1f67238497dbd8d275232e10dcdda23a03f151480d6c853c84d6fff720f57033` and `fe319e19f015bf2654598d4456551ba9a3a73b58c72738bf80fca8aa02aef5cc`. These are explicit distinct scopes; no unrelated local state was modified or deleted.

## Invocation and remaining boundary

From any directory, verify the new exact inventory with:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_record_url_repair_20261021/seal_repair.py --verify
```

For a fresh offline replay without altering sealed audit outputs, use a NEW absolute private output directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_record_url_repair_20261021/replay_read_only.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_record_url_repair/root_new_normal
PYTHONDONTWRITEBYTECODE=1 python3 -O /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_record_url_repair_20261021/replay_read_only.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_record_url_repair/root_new_optimized
```

The standalone read-only collector contract is unchanged: `prepublication_check.py --phase before_integration --expected-pr-head 08fc8833a56358d505e0b33ae1debe44ec320add`; later phases require the actual current expected head and, after allocation, exact deposit ID. I did not run this live command. Root alone authors fresh exact account/full-file, whole-sheet row and unrelated-local-state reconciliation after fresh authenticated reads. Exemptions are never copied automatically. No append/stage/publish/ref/lifecycle command was executed here.

The final manifest seals all authored regular files and the seven canonical helpers, with explicit immutable input bindings. It excludes only its own manifest/checksum and generated Python caches. A new complete independent history-free package04 and affirmative root decision remain necessary. Scientific claims, priority limitations, finite-computation limitations, extensive AI assistance and unrefereed/no formal human peer review status remain those of the unchanged paper. No provider mutation, public outcome, DOI allocation, row append, root clearance or external individual contact is claimed.
