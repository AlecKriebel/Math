# PR210 prepared release-helper source adversary

Review sealed 2026-10-15 UTC. Supporting source review only: **not one of the required whole-manuscript reviews**. The review task is 100% complete; the parent research checkpoint remains approximately 70%. **Disposition: repair before any helper executes.** Six mandatory findings and three additional guard findings remain open in the reviewed versions. Under this assignment both categories require resolution, followed by independent verification of the repaired source.

No helper was imported or executed, including its top level. No provider calls, installations, credential/environment reads, Git/index/ref writes, shared SQL writes, or external communications occurred. Authored files are confined to this review directory. The probes compile source without executing it, inspect ASTs, validate local bytes, and use explicitly labelled independent predicate models.

## Exact reviewed versions

All four files were read in full, including 528 total source lines. Paths below are relative to the case `publication/` directory.

| Helper | Bytes | SHA-256 |
|---|---:|---|
| `publish_preprint.py` | 6741 | `c9495a7f357abf7571562de5ccdae4e48ce5674343f0ec0300a2025e9285f055` |
| `append_verified_tracker.py` | 5610 | `686997ff4b8a002b684bcc4418ea7f348ce9eff9ccbb87b23ebade1a38c65b39` |
| `integrate_reviewed_pr.py` | 17133 | `c46bf4a2693931b7000e221cf126b111e2d9c510a4d07047b8f4acf839227bce` |
| `verify_and_merge.py` | 6811 | `25bb4dc4ef417977444d851536db7f30393446ea7f61f08c747a9d6e9d615459` |

The reviewed PDF is 90,186 bytes, SHA-256 `efa4617d9b3ce2091afe472eb35b5144ec30f3117ffac22dc201498f95a0b731`. The 180-entry ZIP is 603,403 bytes, SHA-256 `53ad3f542b43ea6ac4aaaaa5224f70b0bc867abe2ccf61faaf973f4fd8d64c87`. `PACKAGE_MANIFEST.json` matches those bytes. `metadata.json` is SHA-256 `3b382df7e7ecc4f4b5d91a3945c0a6704675ba649c5796da62a0b24e73ff4909`; the metadata object in `deposit.json` is equal. Other exact input hashes, including the kit README/tool source, Intake and adaptation notes, are in `PROBE_RESULTS.json`.

At review time `FINAL_CLEARANCE.json` is absent and the second new whole-manuscript family has no sealed authored manifest. In normal Python mode every helper fails before an action in this current state. Prepared strings describing completed reviews are future payloads, not current actual claims. Nothing in this review authorizes publication or merge.

## Mandatory findings

### F1 — Cleared files are not bound to the files sent to Zenodo

**Severity: high.** `publish_preprint.py:22–26` validates the files listed in clearance and metadata equality. Line 67 separately checks only that the kit reports two files. Lines 72, 75 and 84 compare kit results with one another. No check connects the kit's file paths/names/size/SHA-256 to the clearance's submission-file set or `PACKAGE_MANIFEST.json`.

Concrete counterexample: leave the cleared PDF and ZIP unchanged, but change `deposit.json.files` to point at two different local payloads, retaining the desired upload names and identical metadata. The cleared-file hash loop passes. The kit's check, stage, inspect, publish and optional public downloads can all consistently verify the different payloads. Line 104 then records `exact_reviewed_frozen_files_published: true`, incorrectly. This does not require a race, provider malfunction or fabricated clearance.

**Repair:** require the exact expected two-entry path/name mapping and prove the kit's size/SHA-256 set equals the cleared package set before staging and again before publishing. Pin the manifest itself or stage from a sealed immutable local payload. Reject changed or missing entries, path escapes, duplicated logical paths, mismatched names and any unexpected file. Preserve the exact release fingerprint in publication receipts.

### F2 — Later stages accept stale receipts for a different cleared release

**Severity: high.** Tracker lines 24–29 check current clearance counters and only two booleans in the publication receipt. Integration lines 24–34 validate current cleared files but accept the old publication receipt by flags and the tracker by its DOI. Merge lines 18–25 similarly accept flags. None compares publication receipt metadata/files against the current clearance and package mapping, or binds the tracker/prepared-native receipt to the same release fingerprint.

Concrete counterexample: a valid earlier publication receipt remains while later mathematical repairs produce a new PDF/ZIP and a new legitimate clearance. The new local file checks pass, the old publication flags remain true, and its DOI matches its old tracker receipt. Integration can build the revised scientific tree while presenting the old DOI as the exact reviewed submission. F1 can be fixed without fixing this independent cross-stage problem.

**Repair:** every stage must cross-check a canonical release identity containing the exact metadata, submitted filenames/sizes/SHA-256, original PR/head/problem identity and review seals. Require actual all-four-cell tracker evidence and the expected spreadsheet/tab/row/payload, not just `verified`. Before merge bind `PR_PREPARED`, current native payload, clearance, publication and tracker to that same identity. Changed bytes require a new reviewed release plan, never silent reuse of an old DOI receipt.

### F3 — Failed public SHA readback and unresolved DOI still permit promotion

**Severity: high.** Publisher lines 85–96 catch every exception from the two actual public downloads, including a SHA-256 mismatch, and continue. Lines 97–104 nevertheless set `metadata_and_files_verified` and `exact_reviewed_frozen_files_published` true. The download list can be empty or contain only one file. The kit `verify()` checks provider-reported MD5 and size; its summary's SHA-256 comes from the local files, not from public-download bytes. The current helper therefore does not establish the stronger public SHA claim when this caught error occurs.

The kit deliberately reports DOI status separately; a confirmed publication can have `not_resolved`, `unavailable`, `not_assigned` or an invalid/absent DOI. Publisher and later stages do not require a valid nonempty DOI URL or successful resolution before putting that DOI into the tracker and native release. This is a progression/link-resolution gap, not a claim that resolver failure invalidates an otherwise confirmed deposit.

**Repair:** preserve confirmed publication durably even if supplementary verification fails, but mark it pending verification and stop promotion. Require both expected public downloads with exact SHA-256/size matches and an actual resolved DOI to the expected record before a receipt is usable by tracker/native stages. Recover only through read-only inspection/download/resolver checks; do not stage or publish again. Do not set stronger success flags after catching a verification error.

### F4 — Uncertain merge outcome is not a durable reentry barrier

**Severity: high.** `verify_and_merge.py:15` checks only `PR_MERGED.json`. Lines 134–135 persist `NATIVE_MERGE_REQUEST.json` before the PUT, but a subsequent invocation never checks that marker. If the PUT succeeds remotely and its response or subsequent PR read fails, `PR_MERGED.json` is absent. Under stale PR reads reporting open/unmerged with the expected head, the next invocation can reach another PUT. Even when the provider safely rejects the repeat, the promised no-repeat uncertain-mutation policy has been violated.

**Repair:** create a durable exclusive attempt record before the first merge mutation and refuse all further mutating entry when it exists, until a separate read-only reconciliation proves the outcome. Preserve requests, expected head and any response. A stale API state must never authorize a repeated PUT. Apply the same explicit recovery discipline to an uncertain ready-for-review mutation if that action is to be retried.

### F5 — Append-time duplicate check is only by the new DOI

**Severity: medium.** Publisher lines 45–50 check problem IDs before publication. That check can be separated from append by staging, publication and readbacks. Tracker lines 38–48 re-read the sheet, but look only for `z['doi']`, not the problem's identity.

Concrete counterexample: after publication's early preflight, an existing row for `AMR-050-0033 / 5100033` appears with another DOI. The append-time read sees it, but `existing` is empty under the DOI-only predicate, so the helper appends a second problem row. The independent model in `PROBE_RESULTS.json` uses this exact shape.

**Repair:** immediately before the one authorized append, reject any conflicting row for the exact problem identity as well as any conflicting DOI row. Read-only recovery is allowed only for one exact four-cell row matching the durably recorded attempt payload and release identity. Preserve the existing strict header, sheet-ID/title, returned update and exact four-cell readback checks.

### F6 — Python optimization removes the release guards

**Severity: high.** Clearance, once-only, checksum, original-head, status, ancestry and readback gates are `assert` statements throughout the helpers. Normal Python optimization, including an inherited optimization setting, removes these checks. For example, an existing clearance with `release_cleared: false` ceases to block publication in optimized mode. A missing clearance still causes a file-read failure; the counterexample concerns an existing uncleared or mismatched record.

AST/compilation-only probes find 19, 12, 35 and 25 asserts respectively, and show assertion bytecode removed under `optimize=1`. No helper bytecode was executed. The probe accounts for both older `LOAD_ASSERTION_ERROR` and newer `LOAD_COMMON_CONSTANT AssertionError` instructions.

**Repair:** refuse optimized execution before any action, or replace operational guard assertions with explicit checked exceptions. Verify that a false clearance and changed hashes still stop an optimized invocation before any mocked mutation.

## Additional guard findings — also resolve before action

### O1 — Once-only markers are not exclusive across processes

Publisher lines 20–21/68–70, tracker lines 42–52 and integration lines 22–23/193 use a separated existence test and ordinary overwritable `write_text`. No whole-run process lock or exclusive marker creation serializes two invocations. Two processes can both pass the absence check before either writes, then both enter a provider action. In particular, the kit's new-deposit stage path has no per-manifest creation lock; its documented metadata-edit lock does not cover creation. The pure interleaving is recorded in the probe results.

Use an exclusive creation/lock before the first relevant action and keep it across the critical workflow. A second invocation must reconcile read-only. This is a concrete limitation of the stated single-attempt guarantees, not an assertion that concurrent invocation occurred.

### O2 — Full collateral pin verification trusts the receipt's tree rather than rebinding it to the actual commit

`verify_and_merge.py:60–79` traverses `p['tree']`. It never fetches the commit object for the actual `head` to require that this tree and `[original_head, main_parent]` are its tree/parents. The explicit science/original archive/submission body reads do use `?ref=head` and are valuable. But other included audit/helper collateral is checked only against the receipt's independently supplied tree. The changed-path subset check at lines 111–114 does not compare bytes or modes. An inconsistent recovered receipt with head H2/tree T1 can therefore miscertify collateral within allowed paths. A normally successful integration creates a consistent receipt; this is the missing check when consuming it.

Fetch the actual commit by the expected head, require exact recorded tree/parents and original identity, then traverse that actual tree for every included pin. Keep the existing actual body readbacks as well.

### O3 — Expected native branch/repository identity is not enforced

Integration checks that PR210 is draft/open at the exact original SHA, but uses the returned `pr['head']['ref']` at lines 193–206 without requiring `dot/math-5100033` or the expected head repository. A renamed/rebound head at the same pinned commit can pass. The assignment specifically authorizes the sole existing PR branch; enforce its exact branch/repository identity at initial/fresh/ref/merge checks. This complements, rather than replaces, the exact-head and nonforce guards.

## Verified source walks and local facts

| Source area | Strongest verified result and limit |
|---|---|
| Publication `16–26`, `39–50`, `66–84` | Current missing clearance stops normal execution. Existing original head/open/draft and target `claimed_solved` checks precede stage. An existing stage marker prevents sequential restaging. Kit check is production; publish uses exact returned deposit ID; no automatic helper publication retry. F1/F2/F3/F6/O1 remain. |
| Tracker `23–69` | Correct spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, sheet ID `1254632077`, title `Math Puzzles`, exact four-column header, RAW append payload, one row/four cells, returned payload and full four-cell readback. Exact DOI recovery requires one exact row and an existing attempt; an unresolved attempt otherwise blocks a second sequential write. F2/F5/F6/O1 remain. |
| Integration `56–99` | Correct old SHA `2180d64b648b81ac660a792f7823d0b715f9cf12`; original Queue blob is checked against Intake (`7a62a969eddd1b1b7a35f24de59acb5f868ea093`). Fresh main target must remain `claimed_solved`; existing scientific subtree causes refusal. Only the selected row is replaced; other queue bytes survive. Source year becomes 2020 and author turn stays 1/5. Independent queue model passes. |
| Integration `100–150` | Current native proof/control bytes and all archived originals are preserved while the explicit administrative files receive actual review/DOI/tracker facts. Actual readiness/turn-ledger fields exist; there are no assumptions of nonexistent PR211 metadata/source-record files. Release/acceptance/publication metadata receipts are actually created, then current manifests are regenerated. Existing dated history stays history. |
| Integration `151–207` | Fresh-main base-tree overlay, parents `[OLD, main]`, explicit post-creation parent/tree check, fresh original-head PR guard, `force: false` on the existing returned branch and a durable sequential ref attempt/receipt. No local Git/index/ref mutation. Foreign base paths omitted from the overlay, including already-published portable-preparation sidecars, remain in the base tree. Fixed family list must be extended if a later required review supersedes review 02. O1/O3 and F2/F6 remain. |
| Merge `47–120` | Expected PR head, untruncated hierarchical tree reads, every recorded collateral Git-blob identity, actual bodies for every native-current file and both submission files, exact full Queue bytes and target status/DOI. Compare-file count `<300` fails closed at GitHub's file-list cap, allowed-path subset excludes foreign paths, and removals are refused. O2 and cross-stage binding gap remain. |
| Merge `121–146` | Native ready transition and mergeability check; PUT supplies exact expected head SHA and merge method `merge`; final receipt requires actual merged/closed PR and returned merge SHA/head. Counts `[44,21,21,0]` are written only after those verified completion conditions. No pre-action code increments the parent checkpoint's `[43,20,20,0]`. F4/F6/O1 remain. |

Independent local validation additionally established:

- All 20 original Intake pins match byte-for-byte in the submitted capture, ZIP-native history and verification/original-submission copy: 60/60 comparisons passed.
- The prepared native tree has 42 files. Its path set and every byte match the ZIP's `pr_update/5100033/` subtree. Current `MANIFEST`, `PUBLICATION_MANIFEST` and `CURRENT_PACKET_MANIFEST` have respectively 14, 14 and 41 valid entries, with no mismatch.
- All six available family seals parse under the helper's `authored_files`/`files` handling. Authored entries are 9/7/6/16/11/14; all paths stay within the correct family and every declared byte/hash matches. Review 02 remains unsealed at this observation; the seven-family loop currently refuses it, as it should before clearance. A later clean review requires extending this set before use.
- Deposit metadata preserves Alec Kriebel's supplied name, independent-researcher affiliation and ORCID `0009-0001-9320-500X`. The kit verifies every supplied metadata key with its documented narrow representation exceptions and verifies exact provider file-name/MD5/size sets.
- Source-native Markdown link targets examined locally had no unresolved active relative links. The future Queue target `attempts/5100033/FINAL_DISPOSITION.md` does not yet exist in the frozen snapshot, but integration explicitly creates it before constructing the tree. `FINAL_ACCEPTANCE`, `PUBLICATION_METADATA`, `PUBLICATION_RECEIPT` and `RELEASE_RECEIPT` are also created. No actual new DOI or public release receipt yet exists to test remotely. The post-merge case receipt must be published in a later factual checkpoint; the merge event cannot be honestly pre-created.

## Remaining gap and exit criteria

The strongest result is that the current frozen scientific/provenance package is internally byte-consistent and the prepared helpers have identifiable, repairable release-control defects. This review makes no new theorem/priority determination and supplies no current release clearance.

Before actions: resolve F1–F6 and O1–O3; obtain the still-required clean final manuscript seal (extending the family set if needed); create a version-bound clearance from actual reports rather than prepared claims; obtain a distinct supporting adversary's review of all repaired helpers and recovery paths; and retain the reviewed PDF/ZIP unchanged unless a new mathematical review cycle explicitly supersedes them. Actual publication, DOI/public download verification, exactly one GWS append/all-four-cell readback, native ref integration/full readback and expected-head merge remain unperformed. No additional user permission is inferred necessary: the outstanding barriers are mathematical clearance and correctness checks, not authorization.

Replay the supporting audit with `python3 -B static_probes.py` in this directory. It writes only `PROBE_RESULTS.json` here. The JSON separates actual local checks from hypothetical predicate-model counterexamples; it is not a live provider test.
