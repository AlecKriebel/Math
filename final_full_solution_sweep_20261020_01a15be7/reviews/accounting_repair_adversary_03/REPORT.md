# Independent second accounting-repair review 03

Review date: 2026-10-21 UTC. Bounded review completion: **100%**. The overall sweep remains incomplete; its captured estimate is36%.

## Verdict

**The second repair fixes every previously demonstrated case, preserves the correct four-publication baseline, but still has material counterfactual acceptance gaps.** This is a local structural consistency finding. It does not identify an incorrect actual publication or ledger row and does not authorize publication, provider writes, package changes, proof clearance, priority clearance, worldwide novelty claims, or a new live uniqueness certificate.

The captured implementation is SHA256 `8771f7efc9d48edc8fcc2b2d186442b7b3cd739255426b105f31d1bb93f66aba`. I read its complete source, the complete first-to-second repair diff, all four root publication receipts, all four ledger receipts, and all three separate modern public-file receipts. The exact source and predecessor versions, source diff, root replay claim, captured inputs, per-case mutations and outputs are retained here.

The strongest verified actual result is a coherent captured numerical prefix **PR9–520**, **512** journal entries, **next_pr521**, inventory maximum1444 and1436 actual PR nodes, with exactly four distinct own completed publications. Direct independent accounting agrees with ordinary and optimized validator baseline output. The actual original PR280 historical decision remains preserved and correctly overridden once. No canonical identity or material contradiction was found in this captured baseline.

## Custody and reproduction

Before testing, I independently rehashed every entry in the prior output seals: **1395/1395** and **2934/2934** matched. Both old review directories were only read. The complete recursively captured input tree from review02 was copied into `inputs/prior02/`; neither prior harness nor prior output was changed. The exact review02 `controls.py` and `supplementary.py` were copied unchanged into `replay/`. Only the current implementation was mounted into their separate copied current input fixture. The historical21 controls retain the full recursively copied original inputs. Both replay groups reset from complete recursive copies for every case.

The current mutable STATE, journal and inventory were each captured as exact individual byte reads, then reread for equality and checked for numerical-prefix coherence. All512 captured saved dispositions equal their journal entries. The capture happened around17:22UTC. This is not a globally atomic snapshot of all files or any provider; current canonical files may advance. No assertion is made that the canonical STATE, journal, checkpoint source or inventory stayed frozen throughout the review. `INPUT_MANIFEST.json` records1522 individual source captures, timestamps, byte counts and SHA256 values. The captured source and evidence used in the tests are immutable review inputs.

`independent_accounting.py` computes the baseline directly without importing the reviewed validator. `new_controls.py` runs103 fresh cases in both ordinary Python and `-O`; each starts from a complete current captured fixture. Every altered file, creation, deletion or symlink is described in that case's `MUTATIONS.json`, and normal/optimized stdout and stderr are retained. A nonzero exit is a rejection, including malformed-type exceptions. A successful emitted snapshot is acceptance. Python bytecode writes were disabled, and `GIT_OPTIONAL_LOCKS=0` was set. `finalize.py` rechecks custody and creates the output seal.

## Execution results

| Family | Cases per mode | Expected outcomes matched per mode | Negative cases accepted per mode | Valid cases rejected |
|---|---:|---:|---:|---:|
| Original preserved controls |21|21|0|0|
| Review02 main controls |163|163|0|0|
| Review02 supplementary controls |10|10|0|0|
| New asserted controls |98|72|26|0|
| New exploratory scope probes |5|Not adjudicated|Not counted|Not counted|

There are **388** prior-control executions, **206** new-case executions and **2** additional direct baseline executions: **596** validator executions in total. Outcomes are identical between ordinary and optimized modes. All29 failures reported by review02 are now rejected. Among the new98 asserted controls, nine intended-valid cases pass,63 intended-negative cases reject, and26 intended-negative cases accept. Those26 are concrete test cases, not26 independent root causes. I separate the strongest primary defects below from optional-field and redundant-declaration observations; an unqualified count of26 equally important defects would overstate the evidence.

The new positive cases preserve the baseline, reorder the completed list, reorder each modern public-file list, and use bare DOI text in the actual DOI ledger cell. These all pass. All42 new explicit root/nested destination and status contradictions reject. So do tested missing public receipts, duplicate public filenames, duplicate/float inventory identities, evidence symlinks, source identifiers changed to a longer integer, mismatching modern archive counts, override path/PR/hash corruption, and even whitespace-only alteration of the historical legacy root when it remains on its original no-public-receipt route.

## Primary remaining gaps

### R1 — Legacy validation is not restricted to the pinned historical receipt

`public_files()` chooses the legacy branch for any entry containing `download_verified`. It has no publication identity or qualified schema parameter. The exact historical byte pin is checked later only when the root has no `evidence.public_files` key.

For PR397, PR399 and reopened PR280, I changed only the ZIP entry in the root and corresponding public-file receipt to the legacy representation: preserve its filename, positive size, reviewed SHA256 and MD5; use `download_verified=true`, `zip_crc_ok=true`, and `members=['arbitrary/a','arbitrary/b']`; remove the modern download/CRC/manifest-count fields. The PDF remains modern and the required separate public receipt remains present. Both artifacts agree, yet there is no manifest member or modern manifest-payload verification evidence. All three cases emit a four-publication snapshot in both modes. Cases are `modern_archive_legacy_schema_without_manifest_<pr>`.

A fourth case changes PR292's ZIP member list similarly and adds a canonical bound public-file receipt with matching identity and file evidence. The mere presence of that receipt skips the historical byte-pin branch, so the altered historical root is accepted. Case: `historical_pin_avoided_by_injected_public_receipt`.

These are schema-qualification counterexamples, not a claim that the reviewer can detect arbitrary simultaneous replacement of all unkeyed evidence. They preserve the published material hashes, publication identities and all other direct evidence. They show that the required supporting-archive evidence can be weakened by selecting another supported representation. The exact gap is to qualify legacy file validation by the immutable historical identity, including the path through a separate public receipt; modern files should continue to satisfy their required manifest evidence. The actual legacy292 baseline remains valid and includes its real manifest member.

### R2 — An existing actual ledger range can contradict the verified row

The ledger check binds `row_number`, configured spreadsheet/gid, actual DOI cell, source-ID token and PR token, but never examines its existing `range` field. For PR292, changing only `'Math Puzzles'!A174:D174` to `'Math Puzzles'!A175:D175` is accepted. For PR397, changing only A176:D176 to A177:D177 is accepted. The summary wrapper and completed publication still name174 and176 respectively; the local read-back range now names a different actual row. Cases: `ledger_range_wrong_row_292` and `_397`.

These two controls use fields already present in the actual receipts and are sufficient to demonstrate the row-binding gap. The remaining gap is consistency between a present structured read-back range and its declared row. No new provider read or whole-sheet uniqueness proof is needed. Additional worksheet-label and injected-range tests are reported separately below because sheet-title history and optional-field policy need care.

### R3 — The actual PR URL check accepts a nonexistent PR path

The PR search requires only a nondigit after the expected number. In each of the four actual ledger D cells, replacing the only expected PR URL by `/pull/<expected>evil` is accepted. Thus `/pull/397evil` is treated as evidence of PR397 even though that URL path does not identify numeric PR397. All other ledger values and wrappers are untouched. Cases: `ledger_nonexistent_pr_url_suffix_292`, `_397`, `_399`, `_280`.

This concerns the required PR identity token, not general prose quality. Longer numerical suffixes are correctly rejected by other controls; alphabetic suffixes pass. A valid numeric PR URL token needs a complete path boundary, with an explicit policy for permitted URL suffixes and surrounding sentence punctuation. These four cases and R1/R2 give **10 primary accepted negative cases per mode**.

## Supplemental consistency observations and scope probes

The remaining16 accepted asserted-negative cases deserve distinct treatment:

- Three modern root ZIP entries accept an explicit `zip_crc_ok=false` alongside `zip_crc_safe_unique_pass=true`; the same file's nested modern evidence stays positive. The field is a known legacy CRC assertion but is ignored on the modern route. Cases: `modern_explicit_negative_legacy_crc_<pr>`. This is a bounded negative safety-assertion ambiguity, separate from the manifest-schema bypass.
- Four D-cell descriptions accept a different explicit Zenodo record URL while the DOI cell and wrappers retain the intended record. Cases: `ledger_wrong_record_url_<pr>`. The required DOI remains correct; this is a narrower material-link consistency issue within prose, not a demand to validate every sentence.
- Six range cases supplement R2: two existing ranges accept a different worksheet label; four cases add a mismatching row/worksheet range to the PR399/280 receipts, which do not originally contain that field. All accept. The wrong-row relationship is mechanically checkable; a worksheet title alone should be adjudicated against an authoritative title/gid mapping rather than assumed immutable. These six do not strengthen the two existing wrong-row counterexamples.
- Three changes to the root PR280 receipt's redundant `historical_ordered_disposition_preserved` declaration are accepted: wrong path, wrong SHA or wrong old disposition. The actual STATE override and replacement still bind the correct historical bytes and remain coherent. Cases: `root_historical_preserved_wrong_<field>`. **No bypass of the effective historical hash binding was demonstrated.** These are redundant-declaration inconsistencies, not evidence that history was rewritten or the wrong override counted.

Five separate exploratory probes are deliberately excluded from the asserted-negative count: float representations of last-processed/count/gap values, a Windows-style backslash public filename, and a NUL-bearing public filename. All emit a snapshot in both modes. The NUL label cannot be a real ordinary filesystem filename, and backslash names have portability implications, but this validator does not dereference these labels. Their treatment should follow the agreed filename/schema contract. They do not imply actual unsafe access, archive extraction, execution, or a canonical unsafe filename. Exact integer publication/journal/inventory node identities are covered by passing rejection tests.

## Independently verified actual accounting

| Disposition | Historical | Effective after single280 override |
|---|---:|---:|
| skip_entirely_already_published |58|58|
| skip_explicit_non_claimed_solved |440|440|
| skip_priority_gate_not_met |3|2|
| reconcile_existing_publication_record |3|3|
| published_verified_full_solution |3|4|
| reconcile_existing_external_publication_record |1|1|
| skip_inferred_no_full_solution_claim |3|3|
| skip_missing_status_no_full_solution_claim |1|1|

| PR | Problem | Record | Ledger row | Root receipt |
|---|---|---:|---:|---|
|292|30001608|23524971|174|PR0292_PUBLICATION_VERIFICATION.json|
|397|9700002|23527793|176|PR0397_PUBLICATION_VERIFICATION.json|
|399|30001179|23539283|177|PR0399_PUBLICATION_VERIFICATION.json|
|280 reopened|30000156|23539734|178|PR0280_REOPENED_PUBLICATION_VERIFICATION.json|

Each DOI is exactly `10.5281/zenodo.<record>`. PR293 remains the separate external-author reconciliation, not a fifth own publication. The four root/ledger records, intended source IDs, DOI cells, PR URLs, merge commits, file hashes, actual existing ranges and modern nested material evidence agree in the captures. The historical PR280 artifact is still `skip_priority_gate_not_met`, SHA256 `12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1`; STATE and replacement bind that same hash. Its effective replacement accounts for exactly the one change from3 to4 publications and3 to2 priority skips. Complete exact cells and evidence are in `INDEPENDENT_ACCOUNTING.json`.

## Limits and remaining work

The falsifiable target was correct structural accounting of the existing local evidence plus rejection of material identity/evidence contradictions across its supported representations. The previous demonstrated failures are fixed; the primary counterexamples above prevent an unqualified fail-closed verdict. The review does not require arbitrary incidental prose validation and does not purport to authenticate a simultaneous consistent replacement of all unkeyed code and evidence. It also does not redo mathematical proofs, source/priority research, package reproducibility, actual public downloads, live lifecycle uniqueness, or final sweep reconciliation.

All writes are confined to this newly created review directory. No providers were invoked. No GWS command, ordinary Git status, Git index/ref/commit/push, PR/release/Zenodo modification, scientific package edit, canonical repair or external outreach occurred. Parent reporting is part of the explicitly authorized adversarial-review workflow. The parent decides how to repair the local validator and whether to release any findings. The bounded review is complete; the broader sweep and final live reconciliation are not certified complete.
