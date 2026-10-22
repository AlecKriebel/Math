# Complete package adversary 02 — PR399

**REPAIR REQUIRED.** The independent analytic reconstruction found no material mathematical gap, and the frozen manuscript, archive, metadata, source scope and reproduction checks passed. The completed publication operations package has two reproducible preservation failures: equivalent target DOI spellings can evade full-sheet deduplication and lead to a duplicate append falsely reported unique; an unlisted empty subtree inside the selected problem can pass the purported exact Git overlay verifier. These operational findings prevent a clean complete-package verdict. No publication, merge, DOI allocation or spreadsheet mutation is authorized by this review.

The assigned review is complete. The remaining work is repair by root and a new independent review of the repaired binding, rather than further work silently folded into this verdict.

## Binding and independence

This review is bound to PR399, problem30001179 / OWR-3392-005, original head `08fc8833a56358d505e0b33ae1debe44ec320add` and comparison parent `28519ba7648c003d4e1212dd315005c93a21a9d6`. All eleven actual original snapshot files matched their byte lengths, SHA256 and read-only local Git objects at that head. No fetch, checkout, branch, index, ref or provider mutation was performed.

The exact frozen release manifest has SHA256 `9d9bca984bcbd5134028513db8b3294bae6f77c7994ec378053e60655af03fcb`. Its five payload bindings are:

| Payload | Bytes | SHA256 |
| --- | ---: | --- |
| PDF | 109650 | f1fb805eacd68f455fc7d3afa1b08ac1e10592f91adfd2321be7151f7994d972 |
| TeX | 36969 | c2de3539519e80a5f036574555f93883df5fe7143d6ddb84077d73fb8ed6b463 |
| Verification ZIP | 174397 | 0ef1597827ca03882cd374b745088aed7e0af74f9d0f31aaaacce56de984191a |
| Canonical deposit metadata | 6170 | c2ed5ff739b45dd5dae451dae7bb838bf1e84be24a514fe78fdfd890025a871c |
| README | 1901 | e477adf75f5578a538d982926ac0efdf31b37f9143bd2afb29fc79f6bb4dfcf6 |

The final operations preparation manifest is `publication_operations_preparation/MANIFEST.json`, SHA256 `ad5c2339d915d8fe33f4ffbdab2d528d9258a394e70a66437d2b615ab70a3e9d`: all 42 authored entries and 26 immutable inputs verified. The current root identity reconciliation has SHA256 `af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39`. All seven completed helper bodies were read, and their actual functions were challenged with offline fixtures. `INPUT_AND_SEAL_VERIFICATION.json` binds the exact bodies and root file.

The task briefing supplied mechanisms, source leads and earlier outcome summaries, so this is not content-blind review. Before opening older opinion bodies or root acceptances I read the entire original contribution, original candidate, additive exposition and frozen TeX and saved my own reconstruction/checkpoint at 2026-10-21T08:55:36Z. Later scientific-family and historical reports were cross-checks, not proof premises. Root subsequently supplied the independently discovered case-variant lead from another task; I independently reproduced it using the actual399 functions and extended the challenge to URL encoding. I did not contact that reviewer or any outside person.

## Material finding P399-02-OPS-01: equivalent DOI spellings bypass deduplication

The collector uses a case-sensitive `zenodo[./]<ID>` search at `prepublication_check.py:78–80`. Reconciliation recognizes only a lowercase literal DOI at `publication_live_gates.py:109–110`. The append helper repeats that case-sensitive extraction before appending and during its claimed uniqueness readback at `record_publication_ledger.py:81`,118–123. The broad problem-keyword pattern cannot repair this when the same DOI appears in an otherwise unrelated four-column row, including only in Notes.

`operations_controls.py` executes the **actual** collector, reconciliation and `append_verified` functions in sequence. External account, PR, GWS and public-download boundaries are replaced by explicitly synthetic fixtures in my private directory. Missing affirmative root clearance is deliberately bypassed only to test the downstream append mechanism; that bypass is not claimed to be a reachable live publication state or authorization. The actual reconciliation remains active in the end-to-end fixture. No provider command is executed.

For synthetic target29999991, an existing unrelated row containing any of the following is sufficient:

- `https://doi.org/10.5281/ZENODO.29999991`
- A Notes reference using `ZeNoDo.29999991`
- `https://doi.org/10.5281/zenodo%2E29999991`

The collector emits no matching row, reconciliation accepts, and the append helper makes one synthetic append of its canonical target row. There are then two semantically identical DOI rows, while its returned receipt says `unique_target_and_DOI: true`. All three failures occur in normal and optimized Python.

I also tested contradictory root digest exemptions. Canonical lowercase target DOI recognition correctly takes precedence and blocks the exemption. Uppercase DOI still escapes. An encoded-slash form `10.5281%2Fzenodo.29999991` is detected as a broad lead and rejected without exemption, but **is accepted when its row digest is marked non-target**, because current-DOI recognition happens before URL decoding. It then produces the same false uniqueness result. The controls preserve all 8 variants:5 duplicate-append failures and3 correctly rejected controls in each mode. Complete outcomes are in `OPERATIONS_CONTROLS.normal.json` and `.optimized.json`.

ASCII DOI case equivalence is specified in the [DOI Handbook](https://www.doi.org/doi-handbook/html/), section3.3.4. Decoding a percent-encoded unreserved period preserves URI equivalence under [RFC3986 section6.2.2.2](https://www.rfc-editor.org/rfc/rfc3986#section-6.2.2.2). These are equivalent identifiers, not a demand to conflate genuinely different records.

**Required repair:** use one carefully scoped DOI/record identity recognizer across collector, reconciliation, pre-append and readback. Apply appropriate ASCII case handling and DOI URL decoding, scan every returned column, and recognize the current target before any non-target digest exemption. Preserve exact canonical-row equality as a separate requirement. Test aliases both alone and alongside the exact row, with and without contradictory exemptions, including final readback with the upstream gate bypassed. Merely fixing the collector leaves the independent append checks unsound.

## Material finding P399-02-OPS-02: exact tree verification ignores empty directories

`repository_integration.leaves` filters every tree entry out of the recursive result. `verify_integrated_tree` compares this leaf projection with the original11 plus publication5 overlay, while its sibling preservation checks stop at the selected problem boundary.

I constructed a synthetic read-only Git response in which every expected original and frozen publication blob has the correct actual mode/hash; the original parent and exact QUEUE replacement are valid; all unselected root, unsolved and attempts siblings are unchanged. The selected problem additionally contains `hidden_empty`, mode040000, type tree, SHA `4b825dc642cb6eb9a060e54bf8d69288fbee4904` (the empty Git tree). I then called the **full actual `verify_integrated_tree`**, rather than merely comparing my own leaf sets. It returns success with original_files11, publication_files5 and the preservation booleans true. This reproduces in both Python modes and is preserved in the same control receipts.

The precise limitation is within `unsolved_math_prioritization/attempts/30001179`: the verifier cannot distinguish an extra or removed empty nested tree from the expected directory topology if leaf payloads remain equal. Root-level or sibling tree changes outside the selected boundary are already checked by tree SHA and are not alleged to escape. No changed file bytes or live GitHub acceptance of a crafted tree was tested or claimed. Git object trees can represent the empty subtree, and the helper's exact-tree preservation claim does not rule it out.

**Required repair:** compare the selected subtree's directory/tree-entry inventory as well as its leaves, allowing only the parent directories required by the approved overlay and preserving pre-existing unselected empty trees. Add explicit extra/deleted/renamed/nested-empty-tree controls, while retaining mode/blob checks, exact parent/head QUEUE checks, sibling SHA preservation, current test-merge parents and actual post-merge verification. This is an exact-tree preservation gap, not a mathematical counterexample.

## Mathematical reconstruction and exact source question

I independently downloaded the official537,543byte [original report](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1), SHA256 `5121d8ec30d2c1346cbbdd68164915d5a24fb31e5a94a3a3215ba576954ee64d`, and read and visually inspected printed528–530. It defines associative pointed reduced free products of Hilbert bimodules with central unit vectors and canonical zero identifications, allowing explicit regularity choices. The generation question concerns the maximal ordered tensor intersection in an arbitrary supplied free system. The preceding cocycle questions and following forward-construction recovery question are separate. Specialization to scalar separable Hilbert spaces is valid.

`INDEPENDENT_RECONSTRUCTION.md` contains the checkable proof analysis. Attempts to falsify the following did not reveal a material gap:

- Recoverable location/scale give a standard Borel sigma-finite Gaussian mixture. Finite-prefix deletion scales d by2^-k; Tonelli and a finite Gaussian change of variables give the exact positive density, both null-set directions and the reciprocal square-root unitary.
- Concatenation for each fixed grade list retains every coordinate and has an inverse. Ordinal sums need not cancel across lists. Maximal finite monochromatic convex runs give unique disjoint charts, including changes at limit ordinals; their restricted measures are equivalent. Three-color flattening and the RN chain prove actual free associativity.
- Strongly continuous support projections, translations and grade dilation give the stated field. Fixed-pattern/grade maps plus the already proved uniform bound prove strong V continuity. Continuous final projections supply the exact adjoint norm identity and strong V* continuity, including zero times.
- Countably many rational cuts detect every rise. Infinite blocks have rises almost surely, so no infinite grade remains in the tensor core. Finite decreasing simplexes split onto tensor products and prove maximality. Countably many complete singleton support rectangles generate every finite sector. The closed finite-grade projection prevents completion from adding infinite words.
- The explicit grade-omega parameter box has finite positive mass at least(622/625)(t/3)log2 for each positive t. Its indicator is orthogonal to the generated hull. Thus the stated F, Hull(F)=K and K proper in E follow.

My own explicit-guard finite controls pass identically normal/-O:4096 coordinate association cases,4096 grade identities,147 scale-chain cases,5461 finite-grid core cases,326 finite-hull cases and4 wrong-rule witnesses. They supplement the analytic proof; they do not prove infinite probability, measure equivalence or strong continuity. No universal recovery/classification, arbitrary stronger regularity or human peer-review claim is inferred.

## Sources, priority and historical limits

`SOURCE_READING_AND_PRIORITY.json` records actual body scopes and seven fresh overlapping priority query inputs. I read actual2006§10.2, the2014arXivv4 classification front matter/pertinent paragraph/bibliography,2022§4/ref30, the full2026 institutional abstract and matching dated page entry, Attal–Nechita's Fock factorization/ambient and rectangle-density proof, Liebscher's tensor definition/Fock example, Tsirelson's tensor definition and measure-class half-density opening, Fowler's tensor/intertwiner identification, and Arici–Ge's discrete definition/free-product decomposition. Long monographs were not represented as wholly read. The two standard books were checked through primary publisher identity/edition metadata; their bodies were not retrieved. The theorem's standard probability/measure inputs were independently checked at their actual hypotheses.

The old forward mechanism cannot furnish this obstruction directly: T is contained in Core(Hull(T)), so hull monotonicity forces Hull(Core(Hull(T)))=Hull(T). Ordinary finite-Fock approximation has a specified finite-sector ambient; tensor nonclassical remainders do not automatically provide pointed-free run unitaries. Fowler and Arici–Ge use different structural categories. These are mechanism comparisons, not title-based deductions.

A fresh distinct institutional2011 lecture abstract about Hilbert modules and quantum dynamics was read in full through the web tool. It outlines tensor/noise and monotone-to-free relationships, with no authenticated universal generation converse or same negative construction. Two Wrocław conference PDF leads timed out; only their search snippets were seen and no full-body inference is made. The exact named in-preparation manuscript remains unrecovered; no2026 talk recording, slides or transcript was inspected. No earlier exact counterexample or contradicting positive theorem was authenticated in the actual bounded readings. This is not worldwide firstness or proof of current openness.

## Archive, reproduction, metadata and visual inspection

The ZIP has82 safe unique members and81 payloads plus its manifest. Every payload hash/length verified; all members are UTF8 source/metadata. All thirteen measure, fifteen continuity, fifteen priority and eleven prior package-review sealed artifacts verified; the 108 preparer entries and 42+26 operations entries also verified. The later root release manifest is intentionally outside the preparer-owned seal, not an unlisted preparer file.

Fresh extracted-bundle reproduction passes normal, optimized and inherited PYTHONOPTIMIZE=2 modes. Own hostile fixtures test22 integrity cases across normal/-O. Four semantic mutation runs update integrity manifests yet still fail: a deliberate false assertion in the historical nested density child, and altered guarded family output, each under both outer modes with inherited optimization. The wrapper correctly keeps nested historical assertions active. Self-manifests are not signatures; the frozen external archive hash remains the trust anchor.

The preparer's158 general,93 candidate-specific and73 repaired-guard controls were replayed against actual helpers in both modes with only HERE redirected into my private scope:648 passing control invocations, zero actual provider access attempts. Their missing alias/empty-tree cases explain why those suites pass despite the new findings. My independent operations script additionally records42 guard/control outcomes per mode, including full pagination failure controls, strict sheet schema, freshness, exact binding, exclusive intent, merged-state gating, each lifecycle mutation's fresh gate, every intended public metadata field, changed downloaded bytes, DOI200 and the exact PDF/ZIP payload verification.

All ten actual PDF pages were rendered and inspected at105dpi; original printed528–530 were also rendered and inspected. No clipping, overlapping text, broken symbols, unresolved references or pagination defect was observed. Title, author, ORCID, date/version, licenses, citation notice, editable TeX and intended deposit scope agree. Extensive AI assistance and unrefereed status, with no formal independent human peer review or proof-assistant certification, are explicit. No third-party full source body, rendered source image, raw provider record or credential pattern was found in the public ZIP. Four members retain local-path provenance references, accurately described as custody rather than promised bundled bodies.

## Root reconciliation and operational boundaries

I independently read the entire metadata and complete two-file projections of records23333353,23356540 and23444606, and all three corresponding full rows. The first concerns ambient extremal-exchangeable independence, the second GNS descent, and the third initial surreal groups. Their mathematical objects, exact targets and source references are distinct from this tensor-core question. All projection digests and row hashes match root's reconciliation. The one unrelated saved local state has the exact bound path, bytes and integer record23333353 and remains unchanged. No other published PDF/ZIP was downloaded or claimed fully read.

The historical account snapshot has195 records over8 pages and176 rows. Its age does not make the snapshot a current mutation gate. Gate expiry, preparation `publication_ready:false` and missing affirmative `ROOT_PUBLICATION_CLEARANCE.json` are intentional safeguards, not findings. No publication action has been started in this review. Correct existing helper mechanisms include exact frozen payload checks, full account pagination, metadata/entire-file projection binding, local-state path/hash/integer-ID restrictions, per-phase/head/ID short-lived gates, merged-state requirements, durable exclusive intents, no blind retry, and public byte/metadata/DOI verification. The two demonstrated gaps must be repaired before those mechanisms can support promotion.

Review completion estimate: 100%. Publication readiness: false. Unresolved material findings: P399-02-OPS-01 andP399-02-OPS-02. No external outreach was prepared or initiated. All authored artifacts remain in this review directory and its ignored private custody; canonical files and all historical seals are preserved.
