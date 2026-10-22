# PR399 DOI identity and selected-tree preservation repair

Implementation completion estimate: **100%**. Both reviewer02 findings have bounded local repairs and passing normal/optimized actual-function controls. **A new history-free complete package review03 and affirmative root clearance are still required.** No mathematical result, publication authorization, merge, stage, DOI allocation, publication, ledger append or live success is asserted. No provider, network, Git/index/ref/branch, PR, Zenodo, GWS, global progress or unrelated-effort mutation was performed.

Root first authorized proposal-only work in this new subtree, then expressly authorized canonical repair after completed reviewer02 seal `87ccb1871311c3090953d304faed6e19819d1c40fd5be1ef21713380ba3cb3a1`. Canonical installation occurred only after preservation and proposed-copy tests. Five helpers changed: `ops_binding.py`, `prepublication_check.py`, `publication_live_gates.py`, `repository_integration.py`, and `record_publication_ledger.py`. Lifecycle execution and public-file verification helpers are byte-identical. `CANONICAL_INSTALLATION.json` records the first installation, `PARENT_CONSISTENCY_INSTALLATION.json` records the subsequent stricter field-consistency refinement, and authoritative `CURRENT_HELPER_BINDING.json` pins all seven final old/current identities; `REPAIR.diff` is the complete change.

## Historical preservation and read status

Before canonical edits, every one of the **42 authored/captured preparation artifacts and 26 immutable inputs** was verified against preparation manifest SHA-256 `ad5c2339d915d8fe33f4ffbdab2d528d9258a394e70a66437d2b615ab70a3e9d` and copied with audit-relative paths into `pre_review02_binding/`. The historical manifest, checksum and root lead reconciliation were also copied. The old verifier freshly passes against this complete preserved snapshot with its 42+26 inventory. The original historical preparation report/results/seal remain unchanged; that seal is now historical and must not be represented as a seal of repaired canonical helpers.

All eleven originals, the exact five publication files, three preparation notices, frozen release manifest and root lead reconciliation remain unchanged. The frozen release SHA is `9d9bca984bcbd5134028513db8b3294bae6f77c7994ec378053e60655af03fcb`. Root reconciliation remains SHA `af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39`. No exemption was added, copied or reclassified. The actual flat canonical `.zenodo-state/*.json` inventory stayed at241 files with aggregate SHA `f8c5f53d35ceba5e654fd05769dbebd11878512c54c6750cb1f60f400cc4e1f2`; only counts/digest, no filenames or bodies, are disclosed.

Reviewer02's complete report, verdict, actual operations-control program, result files and final seal were read. All23 final sealed review artifacts were verified read-only. Captured evidence is in `review02_evidence/`. Current root read-status bodies were also read and pinned:

- `ROOT_OPERATIONAL_PREPARATION_REVIEW.json`: SHA `5914ace5592f4ad81128027af878bfff8178bcfe45869edcad2b88b2789447bb`.
- `ROOT_PACKAGE_REVIEW02_ACCEPTANCE.json`: SHA `161e348efd6ec6d732011182930c8b3639a89424154485e15e7ee23cef4872f6`.

These are read-time bindings, not future clearance. `ROOT_READ_STATUS_BINDING.json` records them. Root's expired historical195-record/176-row collector is not a current mutation gate.

A bounded PR280 working proposal was read and captured before adaptation. It was not finally frozen or accepted when captured. Its exact copied source hashes and final read-only change observations are preserved. No PR280 file was edited and no PR280 agent was contacted. All builds use the captured own copies, not mutable sibling files.

## Old failures remain reproduced failures

`replay_counterexamples.py` loads exact preserved old helper bytes and executes the preserved reviewer02 actual-function program. Only scratch/output custody and the deliberate missing-clearance fixture location change. Every external boundary is synthetic or trapped. Both normal and optimized replay preserve:

- Eight DOI variants, including **five actual old duplicate-append/false-unique failures** per mode.
- The42 independent guard/control outcomes.
- The full old selected-subtree verifier accepting an unlisted empty tree despite exact eleven-original/five-publication leaf matches.

These outcomes are retained in `old_replay_normal/` and `old_replay_optimized/`, never relabeled as passing repaired behavior. The independent reference program SHA is `27c7b4810b7ca7db391e2b59f89211a85ffd255af1f10528ad21f4ce700df8b7`.

## P399-02-OPS-01: shared bounded identity recognition

One recognizer is defined in `ops_binding.py` and consumed by the collector, reconciliation, independent append checks and readback. `doi_identity.py` is its standalone pure-function development source; no eighth canonical helper dependency was introduced.

**Supported narrow normalization:** ASCII letters are mapped explicitly to ASCII lowercase; Unicode casefolding is not applied. Literal Zenodo DOI suffix digits remain text. Valid percent-encoded **unreserved ASCII** characters are normalized once for narrow comparison. Uppercase/mixed-case `ZENODO`, encoded unreserved periods/letters/digits and ordinary DOI resolver representations therefore cannot silently evade target checks. Numeric boundaries reject longer IDs, different prefixes and extra suffix characters. `10.5281/zenodo.0999` remains distinct from `10.5281/zenodo.999`; no DOI suffix is automatically integer-cast.

**Conservative review leads only:** reserved or nested encodings, recognizable `zenodo.<ID>` fragments, Zenodo record URLs, and concept/version-parent IDs are blocking leads. They are not asserted to be general URI equivalences or proofs of identical mathematics. A bounded eight-step review-only decode exposes reserved/nested forms; unresolved depth/malformed DOI encoding stops. Recognized shortDOI aliases such as `10/abc` or resolver short aliases stop for root read-only resolution, including before a target ID exists. No row digest exemption can conceal an unresolved alias. There is no automatic bypass or resolver request in these helpers.

The source rules were provided by root after its reported actual readings of [DOI Handbook September2025](https://www.doi.org/doi-handbook/DOIHandbook_2025.pdf), §4.3.4 printed37–38 and §4.7 printed40; [RFC3986 §2.3](https://www.rfc-editor.org/rfc/rfc3986#section-2.3) and [§6.2.2.2](https://www.rfc-editor.org/rfc/rfc3986#section-6.2.2.2); and [DOI resolver documentation §2](https://doi.org/help.html). This repair made no network source retrieval and does not claim another independent full-body reading. Its checkable implementation distinguishes unreserved normalization from conservative reserved/nested/record aliases.

When an expected target ID exists, the collector reads its actual complete account record. It derives typed family leads from `conceptrecid`, narrow `conceptdoi`, `metadata.relations.version[*].parent` with `pid_type: recid`, and a recognized parent record ID. The observed195-record local API snapshot establishes that `conceptrecid` strings and typed version parents are present in that API contract; no raw record bodies are copied here. The gate independently derives the family from its hash-bound complete account receipt and rejects changed identity evidence. Collector receipts gain `expected_identity_record_ids`, a sorted list; this is evidence of conservative identity leads, not a declaration that all versions solve the same mathematical problem. Unexpected recognized types or contradictory recognized parent/concept IDs fail closed.

Target/family identity is checked before non-target exemptions. A changed or aliased row always rejects for root inspection/repair of the existing situation. **Only exact literal `desired_row(ID)` equality** permits idempotent success. The append helper independently scans every returned cell, even when its upstream gate is stubbed in a test. Readback likewise scans every cell and preserves target aliases before exemption filtering. A duplicate introduced at readback produces rejection, never a false uniqueness certificate. The correct exact row stays idempotent with zero append calls; verified absence permits one intent-bound append.

## P399-02-OPS-02: exact directory topology

The full verifier still compares exact leaf paths, modes, types and blob IDs, exact own QUEUE bytes, other QUEUE bytes, root/nested siblings, current-main/test-merge/actual-merge parents and preservation. It now also compares the selected subtree's **actual recursive directory paths and mode/type pairs**.

The permitted directory inventory is exactly:

```text
base recursive directories
union original pinned recursive directories
union every ancestor directory required by the eleven originals and five additions
```

For the branch publication overlay, it is the original directory inventory union ancestors of the five selected additions. Directory SHA values are not required to remain equal when approved descendant files change; exact paths and `040000/tree` identities are. Existing empty and nested empty trees are preserved. Unlisted added, removed, renamed, moved or malformed-mode empty trees reject. Both the branch object check and full test/actual merge check use this mechanism. No Git object or ref was created in testing.

## Verification of installed current bytes

Each mode passes **530 current-implementation controls**, with zero actual provider access attempts:

| Suite | Controls per mode | Evidence |
| --- | ---: | --- |
| Complete identity collector/gate/append/readback pipelines |123|`CURRENT_CONTROLS*.json`|
| Independent append/readback, short aliases, typed family and full tree controls |83|`TARGETED_CONTROLS*.json`|
| Original complete regression logic |324|`REGRESSION_CANONICAL*.json` and nested receipts|

Targeted tests call actual current helper bodies, including the full integrated-tree function, not a duplicate imitation. They challenge canonical/case/encoded aliases alone and with contradictory exemptions, alias-plus-exact rows, aliases introduced after append, numeric/Unicode/leading-zero boundaries, malformed or short aliases, literal idempotence, verified absence, typed concept/version families from the actual synthetic target record structure, and existing/added/deleted/nested/renamed/moved empty trees.

The original324-control source remains byte-identical in both canonical historical custody and the preserved snapshot. Its old mocks omitted selected-tree directory entries entirely. The replay enriches only those synthetic recursive-tree fixtures using the same original/selected leaf paths, with no changed expected outcomes and no bypass of the new guard. `REGRESSION_FIXTURE_ADAPTATION.diff` makes this adjustment fully inspectable. All original158+73+93 controls pass against installed repaired helpers, normal and optimized. Proposed-copy runs and old failures are retained separately; no historical receipt/seal was regenerated.

All seven current helpers parse, and no production guard uses `assert`. `PARSE_CHECK.json` records checks. `CURRENT_HELPER_BINDING.json` and the new repair manifest are the current byte bindings. Old scientific/frozen package inputs remain unchanged, so no new mathematical result or package repair is inferred.

## Reproduction and remaining root work

From the PR399 audit directory, first verify the delivered new repair seal, then use separate reviewer custody for reruns:

```text
PYTHONDONTWRITEBYTECODE=1 python3 ops_identity_repair_20261021/seal_repair.py --verify
PYTHONDONTWRITEBYTECODE=1 python3 ops_identity_repair_20261021/replay_counterexamples.py
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_identity_repair_20261021/replay_counterexamples.py
PYTHONDONTWRITEBYTECODE=1 python3 ops_identity_repair_20261021/integrated_controls.py --canonical
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_identity_repair_20261021/integrated_controls.py --canonical
PYTHONDONTWRITEBYTECODE=1 python3 ops_identity_repair_20261021/repair_controls.py --canonical
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_identity_repair_20261021/repair_controls.py --canonical
PYTHONDONTWRITEBYTECODE=1 python3 ops_identity_repair_20261021/replay_regressions.py --canonical
PYTHONDONTWRITEBYTECODE=1 python3 -O ops_identity_repair_20261021/replay_regressions.py --canonical
```

These commands write only owned new test receipts. Rerunning changes seal inputs; preserve the delivered checkpoint before any new output or use a separate copy. The original42/26 seal can be verified using its saved verifier under `pre_review02_binding/publication_operations_preparation/`.

Root must inspect the complete diff/report and sealed evidence, reproduce independently, and obtain a **new complete package03 review** over the exact frozen scientific package and all seven current helpers. Only later root clearance may bind these current bytes, actual root reconciliation, final report/seal evidence and frozen release. The unchanged root reconciliation is not newly accepted merely because its bytes survived. Immediately fresh account/sheet/local-state/head/main gates and all lifecycle/public verification safeguards remain mandatory. Durable intents still prohibit blind retries. No clearance, new exemption or live lifecycle outcome was created here.
