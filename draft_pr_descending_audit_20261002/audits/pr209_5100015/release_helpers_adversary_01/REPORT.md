# Independent PR209 release-helper adversarial audit

Verdict: **REPAIRS_REQUIRED**. Seven mandatory findings and three optional actionable findings remain in the frozen candidate. None of this review grants publication, tracker, PR-ready, or merge authority. No live release action was performed. The case discovery estimate remains **45%**; this independent source audit is complete.

The review concerns the proposed guarded workflow, not an executed release and not a mathematical clearance of the separately reviewed scientific snapshot. `FINAL_CLEARANCE.json` did not exist in the actual case when assigned. All records called “clearance”, “publication”, “append”, “prepared”, or “merged” inside the probe archives are **synthetic fixtures**.

## Frozen inputs and independence

The six operative files were copied byte for byte before reading prior review material or parent judgments. `INITIAL_HYPOTHESES.md`, `FROZEN_SOURCES.json`, and the copied `HELPER_SOURCE_ADAPTATION.json` establish the baseline. The independent mechanisms initially targeted were stale review authority, missing source/helper bindings, ambiguous retry outcomes, tracker duplicates, native scope/main races, corrupted receipts, premature completion claims, and unsafe publication payload selection.

| Frozen source | Bytes | SHA256 |
| --- | ---: | --- |
| append_verified_tracker.py | 6075 | f7425b615ca762a0a580d1aa94774e067e7aea03add406c25cca7b6d2e127802 |
| integrate_reviewed_pr.py | 15791 | b5225c370524579a0b37b27117c71eb09ecb6219cc43bc9c89ec5fcf1e9552b7 |
| publish_preprint.py | 5335 | f8f4f354d3eb9e7d3428c8c40a9de9fd5244cba0c3db65e747fdea98849b5e34 |
| release_binding.py | 10449 | 98eb34be6f3fe3ff3d56386d0faa77f0a21d52ba0daef1ef0a33c591def14b2d |
| verify_and_merge.py | 8635 | 5bc6a7dbf3c031e5a2de11d399496b91a11a4184cbece71a9c039e851b1c5aa4 |
| verify_published_readonly.py | 4367 | 05b5e494de791a03fa876da2b777e8891cf145ff67fc78aac9fb9221ec774a8b |

`ADAPTATION_CHECK.json` independently hashes the five stated PR210 source files and records their actual diffs against the frozen PR209 sources. All five old/new provenance hashes match. The generic read-only verifier is unchanged; the other four are adapted. New authorship of the integration source is an intake assertion rather than something a byte comparison can authenticate. No operative PR210 number/problem/DOI residue was found in the six sources. The current PR209 wording correctly credits the exact contemporary Ferudun v1.1 full result, retains the original journal source-year 2021, and states the AI/unrefereed/no independent human review limitations. This does not independently certify the underlying mathematics or priority research.

## Method and reproducibility

`REPRODUCE.py` validates the frozen source hashes, runs `probes.py`, `additional_probes.py`, and `final_probes.py`, and saves every result and synthetic provider trace. **All 29 expected probe outcomes reproduced.** A PASS means the expected audit observation reproduced; several PASS entries demonstrate a candidate defect.

Each actual source is compiled directly from its exact frozen bytes. There is no rewritten implementation or simplified copy of its workflow. The harness substitutes imports of subprocess and public-download providers, assigns an owned synthetic `__file__`, and remaps the literal workspace `Path('/Users/alec/Documents/Math')` to an owned synthetic root. Local locks and intent fsyncs operate only on the owned synthetic fixtures. Native tree/blob/commit responses are in-memory objects whose file hashes are computed from fixture bytes. No `gh`, `gws`, Zenodo toolkit, network provider, or Git mutation is executed by the workflows.

To reproduce, use a fresh copy of this sealed audit folder and run `REPRODUCE.py` with the existing standard Python runtime and `-B`. The generated fixture trees are preserved byte for byte in `PROBE_FIXTURES_FINAL.zip`, then their uncompressed owned copies are removed. Individual stdout/stderr files and the three result JSON files remain alongside the harnesses. No new environment, installation, credentials, or cache is required.

The first harness version retained a stage lock between two in-process executions. That produced spurious “Another release stage is active” failures that do not occur between separate real Python invocations. `probes_v1.py`, `PROBE_RESULTS_v1.json`, and `PROBE_FIXTURES_INITIAL.zip` preserve the complete failed probes. The corrected harness explicitly closes candidate lock handles at its simulated process exit. A clean end-to-end prepare/merge baseline and all later cross-stage tests then passed their expected assertions. The initial shell here-document also failed before Python ran because the disk could not allocate its temporary file; the log records that failure and the direct `-c` correction.

## Mandatory findings

### RH209-M01 — Review counters do not authenticate new sequential whole-package reviews

**Source:** `release_binding.py:46–71`, especially lines 50–52; every mutation caller trusts this context.

**Trigger:** A clearance contains integer counters `fresh_manuscript_reviews=2`, `final_frozen_clean_reviews=1`, empty finding lists, and valid file pins, but no review identities, reports, assessment seals, chronology, reviewed package digest, or prior-repair linkage. `context()` accepts it. The `counter_only_clearance` probe uses exactly this condition and has no review-evidence record whatsoever.

**Impact:** The checked facts establish only that someone wrote the counters. They do not enforce the required two new sequential whole-package clearances, a final clean frozen review, or the absence of mandatory and optional findings in the actual reports. The native public text then asserts these reviews and all global repairs completed.

**Fix:** Require structured, sealed review/assessment records bound to the exact final package and applicable helper sources. Validate the required fresh sequential review identities, completion order, final frozen clean record, and all finding dispositions. Changes requiring rereview must invalidate the applicable authority. Counters should be derived from those records, not replace them. Obtain a new source reviewer after repairs.

### RH209-M02 — Stored publication/tracker receipt acceptance omits once-intent lineage and tracker identity fields

**Source:** `release_binding.py:88–107` and `117–131`; `verify_published_readonly.py:12` returns the stored publication immediately.

**Trigger:** A structurally convincing publication receipt is accepted without either `STAGE_ATTEMPT.json` or `PUBLISH_ATTEMPT.json`; the read-only verifier performs zero provider reads in that state. Separately, `tracker()` accepts `append_count=9`, `updated_range='Other sheet!Z999'`, no `APPEND_ATTEMPT.json`, and a false reconciliation flag, as long as its currently checked fields match. See `missing_publication_lineage` and `tracker_unbound_intent`.

**Impact:** Downstream integration can assert one publication/one GWS append at a verified range using a copied, incomplete, or edited receipt with no retained once-intent ancestry. In particular, the destination IDs in the receipt do not establish that the range is on the verified tab, or that the claimed append count and recovery mode agree with an actual attempt. Mid-run hashing of the current receipt does not validate its initial history.

**Fix:** Require and validate the durable stage/publish/append attempt chain and its identities, release binding, exact payload, publication ID, and receipt digests. Validate the tracker row/range syntax and tab, the exact four-cell expected payload, the invocation's 0/1 append count and consistent reconciliation status. Preserve the distinction between one original append and a zero-write recovery invocation. Require complete recorded readbacks before accepting a final receipt; do not infer them only from booleans. This is completeness/corruption hardening, not a claim to defend against an adversary who can rewrite every trust anchor.

### RH209-M03 — Tracker duplicate detection occurs only before the append

**Source:** `append_verified_tracker.py:44–79`.

**Trigger:** The full A:D preflight contains no matching row. During the single authorized append, another matching row also appears. The candidate reads only the returned A2:D2 target afterward; both matching rows remain. `duplicate_race` reproduces a verified receipt with two problem rows and exactly one candidate append call.

**Impact:** The receipt and native public presentation assert a unique verified tracker entry although duplicate problem/DOI rows exist. The local release lock cannot serialize another tracker writer.

**Fix:** After the target's exact four-cell readback, perform a new full-sheet duplicate scan and require exactly one problem row and one exact DOI row at that target, with the exact expected payload. Bind that final uniqueness evidence into the receipt. A conflict must produce a pending/read-only reconciliation state, never another append. Repeat the applicable read-only uniqueness check before promoting a later receipt.

### RH209-M04 — Unsealed root files and private-looking `.env` files enter the native publication tree

**Source:** `integrate_reviewed_pr.py:23–26`, `79–85`, `105–114`.

**Trigger:** Add an unsealed `preprint/UNREVIEWED.txt` or a `publication/.env` containing an innocent synthetic private marker. Neither is in the cleared package/source/helper manifests. Both are selected, uploaded into the new tree, and included in the prepared pins. `unreviewed_payload` demonstrates both exact paths.

**Impact:** The selection called “explicit” is a broad enumeration of every top-level file. Its blacklist rejects names beginning `private` and a few exact directory names, but permits `.env` and arbitrary other files. Unreviewed content can therefore become public; a normal misplaced local private file could be exposed. Hashing the selected bytes afterward does not make them reviewed or public-authorized.

**Fix:** Derive the complete public payload from explicit cleared/sealed public manifests plus a narrowly specified set of newly generated administrative receipts. Require exact set equality and reject extra files before the first remote object mutation. Separate private transport/context/fixtures from the public manifest; use an explicit public-export manifest for reviewer outputs where needed. Do not solve this solely by expanding the filename blacklist. No real credential file was accessed for this test.

### RH209-M05 — The merge verifier makes the mutable prepared receipt its source and scope authority

**Source:** `verify_and_merge.py:21–34`, `58–62`, `87–117`, `123–128`.

**Trigger:** Replace the preparation record with a synthetic record describing an arbitrary matching-head commit. Retain the cleared PDF/ZIP and valid target row, but provide no `NATIVE_PREPARE_ATTEMPT.json`, no `native_current_source` directory, and no archived original files in the final scientific subtree. Put an unrelated foreign addition in `included_owned_pins`. `forged_prepared_no_science` passes the actual verifier through a merged receipt.

**Impact:** A missing directory makes the scientific-file loop empty. The verifier checks hashes of whatever pin list the receipt supplies, and its changed-scope check permits that same supplied list. It never establishes that the list is the complete authorized packet, that all 23 archived originals and proof files are present, or that the prepared head has the required durable preparation provenance. The recorded SHA of the current receipt detects later changes during the run; it does not establish authority for the receipt read at startup. The original commit remains an ancestor in this probe, which is distinct from retaining the required complete final archive presentation.

**Fix:** Require an authenticated complete preparation-intent/receipt chain and exact expected native path set. Independently derive scientific/archive pins from the frozen reviewed ZIP/source manifest and the narrowly documented administrative transform; require a nonempty complete native source packet and all 23 original pins. Recompute Git blob identity from expected bytes, verify native modes/types, and derive changed scope independently rather than accepting a receipt's list as its own allowlist. Seal and revalidate the completed preparation receipt after actual metadata and ref readbacks.

### RH209-M06 — PR title/body publication can fail or remain stale without preventing merge

**Source:** `integrate_reviewed_pr.py:119–122`; `verify_and_merge.py:58–59`, `137–167` never checks title/body.

**Trigger:** The body/title PATCH is ignored by the synthetic provider, or its result is uncertain after the ref update. `PR_PREPARED.json` has already been written. A subsequent actual verifier run merges successfully while the PR body still says “stale focal theorem; first proof claim.” Both `stale_body` and `body_patch_unknown` reproduce this; the latter preserves the preparation exception and subsequent successful merge trace.

**Impact:** A native PR can be made ready and merged with a scientifically stale or overclaiming public description. The preparation receipt is incorrectly usable as a completion receipt before its final metadata action succeeds.

**Fix:** Bind the exact expected title and body (or their bytes/hashes) into the reviewed administrative specification. Perform a readback after updating them, and check them again immediately before ready and merge. Write a completed `PR_PREPARED` receipt only after every required ref/tree/body readback succeeds. An uncertain body update must leave preparation pending with a read-only reconciliation path and must not authorize merge.

### RH209-M07 — Current main and the actual merged tree/queue are not checked before completion and counts

**Source:** `verify_and_merge.py:125–128` compares only the recorded main parent; lines 137–167 refresh PR/local receipts but never current main; lines 168–173 assert completion/counts without a merged-tree readback.

**Trigger:** After preparation, main gains a disjoint file under `unsolved_math_prioritization/attempts/5100015/`. A normal clean merge can combine that file with the reviewed candidate changes. `current_main_race` reaches `PR_MERGED.json` although the verifier never reads the new main or the resulting merge tree. Its trace and `EXPECTED_CLEAN_MERGE_PATHS.json` preserve the concrete disjoint-path construction.

**Impact:** The scientific subtree that was absent in the initial preparation main can gain unreviewed contents before merge. The final receipt then asserts 100% and `[45,22,22,0]` after only PR/API success checks; it has not verified the resulting native scientific/archive set, current-main foreign rows/paths, final target row, or actual program counts. Other concurrent changes may affect those counts even when the reviewed PR head is unchanged.

**Fix:** Establish and verify the current-main boundary immediately before the ready/merge stages, with explicit reconciliation for target subtree/row conflicts while preserving legitimate foreign updates. After successful merge, read the actual merge commit, its relevant parent identities, complete scientific subtree, exact QUEUE bytes/row, and foreign-main preservation. Compute or independently verify the counts from that resulting state before asserting 100% or recording the four counts as facts. A post-merge verification failure requires a pending completion record and read-only recovery, never a second merge request. The expected-SHA merge request already present should be retained.

## Optional actionable findings

All optional findings also require disposition/repair and fresh source review under this project's policy.

### RH209-O01 — The single-response 300-file cutoff limits valid larger native updates

**Source:** `verify_and_merge.py:125–128`. **Evidence:** `compare_limit` prepares 371 pins, receives 300 compare file entries, and rejects without a merge request. The guard fails closed but cannot validate a legitimately larger delta. Replace it with complete exact native tree comparison or a demonstrably complete equivalent scope check.

**Qualification/correction:** `ACTUAL_PAYLOAD_PATH_LOWER_BOUND.json` records 470 selected paths before new reviewers/receipts; this is not the number of remotely changed files. This shard initially inferred an actual package blockage from an empty local-main case listing. That inference was incorrect because the local Git refs are intentionally stale. The parent identified actual remote checkpoint `d03508747f8fefc94f18793909372c16c3cd4ba8`, 425 native readbacks, and 259 changed paths. The referenced checkpoint receipt was read only after the independent baseline; its SHA256 is `bf2b7dc77275ef98f71fe5c3c40d6c68e6b6fc91c21484c24f6a893aeffb2770`. No remote-main query was made by this shard. An actual present-package blockage is **not established**. This finding is the tested larger-delta limitation only.

### RH209-O02 — Remote object creation precedes a durable native preparation intent

**Source:** `integrate_reviewed_pr.py:108–118`. **Evidence:** the first binary `POST git/blobs` in `unreviewed_payload` has `prepare_intent_exists=false`; tree and commit POSTs also precede the intent written at line 117.

The branch ref has not moved yet, and the current on-disk `native_current_source` existence guard normally prevents a direct rerun. However, an uncertain object-creation outcome lacks a durable, complete native-intent record naming the intended parent/tree/payload set. Create and sync an object-preparation intent before the first remote mutation; retain the later separate exact-head ref-update intent. Keep all unknown-outcome recovery read-only. This is a durability/provenance improvement, not evidence that the current non-force ref guard loses a concurrent commit.

### RH209-O03 — Tracker version/date are hard-coded independently of cleared metadata

**Source:** `append_verified_tracker.py:41`; `release_binding.py:127–130` validates only title/problem substrings in notes.

**Evidence:** `version_drift` supplies an internally consistent, newly bound metadata version 1.1 dated 2026-10-17. The actual append workflow and `tracker()` still accept notes advertising `v1.0,2026-10-16`. Current actual metadata is 1.0 dated 2026-10-16, so no current mismatch is asserted. Derive these fields from the cleared metadata or explicitly require the fixed reviewed values before any append. Validate the exact expected notes when accepting a receipt.

## Positive controls and limits

The actual proposed publication lifecycle passes a synthetic baseline: check, stage, inspect, publish, read-only inspect, actual public-byte hashing, and DOI verification. Durable stage intent is flushed before staging; an injected parent-directory fsync failure prevents staging and retains the intent. Unknown stage/publish outcomes prevent a second publication mutation, with read-only recovery after unknown publication. An unknown tracker append reconciles the exact existing row with zero further append calls. A wrong fourth cell blocks a verified receipt. A wrong public download hash or pending DOI leaves pending verification and no final verified publication receipt; read-only recovery succeeds after correcting the public bytes. Metadata changed during inspect is rejected.

All six exact frozen sources reject optimized Python. Helper/PDF/metadata byte changes, a wrong original PR head, insufficient/boolean review counts, unresolved mandatory or optional findings, and a wrong DOI target record are rejected. The current directory fsync sequence durably links newly created intent ancestors in the tested filesystem. The merge request includes the expected head SHA; an unsuccessful or unknown merge does not write the completion/count receipt and its durable intent prevents a repeated mutation.

Integration accepts the exact untouched queued placeholder and retains 2021, the author 1/5 field, foreign queue rows and foreign main bytes in the baseline. A pre-existing scientific subtree and a changed source-year row both stop it before provider mutations. The operative source explicitly verifies ZIP/native packet equality and all 23 original archive pin bytes during preparation; the remaining native-verifier authority gap is RH209-M05.

Coverage is synthetic and source-level. It does not establish actual GitHub/Zenodo/GWS availability, permissions, deployed schema behavior, remote topology, the mathematical theorem, historical priority, or real publication status. The repository Zenodo toolkit's inspect/metadata verification contract was read to understand the caller, but its entire implementation and the CLI binaries/dependencies were not independently reaudited. No real provider, auth/credential file, private skill-context file, external individual, other audit shard, branch/index/ref write, or release action was used. The ready transition checks the expected head immediately before and after its PR-node mutation. No atomic expected-head property was established for that mutation; the observed checks bracket it, while the merge request itself includes the expected SHA. No premature merged completion was observed for a failed merge.

Every mandatory and optional finding above must be repaired and independently reviewed against **new exact source bytes** before any clearance can be considered. This report is not that subsequent review.
