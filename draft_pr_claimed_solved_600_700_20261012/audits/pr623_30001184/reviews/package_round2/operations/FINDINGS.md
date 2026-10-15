# Independent operational findings, round 2

Verdict: mandatory repairs remain. Exact tested helper sources are preserved in reviewed_inputs/. The operational review is complete against the exact inputs recorded in INPUTS.json; it does not certify subsequent edited inputs.

## Mandatory P2 — Preserve immutable notice and receipt bytes

`prepare_integration.py:280` reads the source notice, and `publication_inputs` binds those bytes to the immutable ZIP at line 283. After this function returns at lines 417–419, `main` independently reads the source path again at line 420. These second-read bytes become `CURRENT_SOURCE_AUDIT.md` without a comparison against `publication_validation.current_source_notice_sha256`.

The full mocked integration reproducer changes the source path immediately after the real `publication_inputs` returns. The ZIP remains unchanged. Main integrates the changed notice, the real disposable integrity replay returns PASS, and the prepared integration receipt is saved. Its validation hash still describes the first notice. This breaks the promised binding between the published archive and the integrated current-source notice. The counterexample succeeds in normal Python and under `-O`; all its evidence checks use `require`, so optimization does not erase the controls.

Exact validated notice SHA-256: `0ab6254210d2464495927efe5f83d3b9cb0f46a375093ff0cfc4765109a731b5`.

Exact integrated notice suffix SHA-256: `f4043e003adb6deb0fba4ba158f4314e11695bacc9e0ee157d053f3d258a561a`.

Evidence: ADDITIONAL_ADVERSARIAL_RESULTS.json and ADDITIONAL_ADVERSARIAL_O1_RESULTS.json; reproducible driver additional_adversarial.py. The notice edit and all generated files stay inside this reviewer folder. Every Git/GitHub call is mocked; no push occurs.

Repair: retain one immutable notice byte string for both archive validation and current-file construction. Alternatively, compare the second read's hash to the validated notice hash before constructing files, and construct exclusively from that second-read byte string. The regression should either reject the demonstrated change or integrate the original validated bytes.

The same validation-to-hash issue affects both publication receipts. Line 261 reads and parses each receipt for validation; lines 284–285 read them again for the returned SHA-256 values. The pure receipt_binding.py probe changes each receipt's title before this second read. The function accepts, but its returned hash identifies the invalid wrong-title receipt. Fresh validation of exactly those changed bytes rejects. Both receipt variants reproduce in normal Python and under `-O`, with optimization-safe evidence checks. Evidence: RECEIPT_BINDING_O0_RESULTS.json and RECEIPT_BINDING_O1_RESULTS.json.

Initial validated receipt SHA-256: `8a5fc89ae85ed66d2821031248292fa5c49f0db7be5442d4549fd0d2d3122789`. Returned SHA-256 binding unvalidated wrong-title bytes: `bf848b26d6d9c2f854a7a378e13216b6462376e3456d6d2dfbcd28d7faea17db`.

The receipt repair should capture each receipt byte string once and derive both parsing/validation and evidence hashes from that same immutable value.

## Mandatory P3 — Require integer archive schema type

`prepare_integration.py:232` checks `manifest['schema'] == 1`, without checking its type. Python equality accepts JSON Boolean `true` and decimal `1.0` as schema 1. A valid copied fixture ZIP with only this schema field changed is accepted by `archive_binding` in both normal Python and under `-O`. Valid integer 1 is accepted; integer 2 and Boolean false are rejected, providing nearby positive and negative controls. All original candidate, PDF, TeX and notice bytes are unchanged, and the internal manifest file hashes remain coherent.

Evidence: SCHEMA_O0_RESULTS.json, SCHEMA_O1_RESULTS.json, and both ADDITIONAL_ADVERSARIAL result files. The independent schema_modes.py probe preserves checks under optimization.

Repair: require `type(manifest['schema']) is int and manifest['schema'] == 1` and retain the true/1.0 negative controls. This is a strict-format boundary failure rather than evidence of changed scientific content.

## Verified controls

All 14 supplied helper fixtures pass under normal Python and `-O`, using the unmodified supplied check_helpers.py source with all fixture temporary paths relocated to this reviewer folder. Seven independent control groups also pass in both modes. They cover an unknown head with and without an old receipt before any candidate/native/publication read, duplicate JSON keys and invalid DOI/path boundaries, queue line endings and duplicate/missing/status/turn cases, independent audit-byte and manifest tampering, exact published record/two-file/TeX/notice binding, tracker gid/title/header/range identity, and durable uncertainty markers after timeout, malformed response and incorrect readback. A retry after each uncertain append dispatches no new call when the exact DOI is absent.

Five additional mocked integration scenarios pass: a changed remote-main turn prevents publication preparation; local state drift after tree construction prevents prepared receipt and push; local state drift immediately before push leaves only the prepared receipt; a correct initial integration uses the historical original head as its second parent and a non-force push; an exact own successful same-DOI retry verifies the previous tree and uses that successful integration commit as its second parent. Shared-index mutations are zero, and all index-building calls use the alternate index.

Frozen inventory independently confirms 13 packet and 11 audit files. The supplied real wrapper replay and dishonest outer-rehash control preserve that boundary, including `-O` integrity checks.

## Optional findings and limits

No additional optional defect was verified. These findings use local data and mocked external operations; they do not assert current production publication, PR, main-branch or spreadsheet state. Concurrency beyond the tested local-state/head/main and second-read cases, and machine power-loss durability, were not certified. Package-round-1 findings or verdicts were not read.
