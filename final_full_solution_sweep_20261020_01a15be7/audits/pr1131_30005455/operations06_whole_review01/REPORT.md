# PR1131 operations06 whole operational review: HOLD

**Do not execute this frozen edition.** The actual checked operations06 parser reproduced six ledger-edge counterexamples, four tracker response-validation counterexamples, and one publication-certification counterexample in each of normal Python, `-O`, and `-OO`. The first finding alone is sufficient for HOLD. This review issues no operational or scientific clearance and does not repair the frozen source.

The reviewed source manifest is `4d491443d4be4d07ef9abb45c0ce6f9c56bf77c20dd7a2254ae43dce2638ab79`; bootstrap is `e8c7f35bc6d60318146ae9794fe84c7c8a18e99e818a350bb78298fd85bd9852`. The complete preparation manifest is `cde78679a06a8ec0954f9af1785cd339762a5cc57b3154661c3313706677852b`. All 18,931 files and 2,850 directory metadata entries were independently checked against that manifest at entry and at final adjudication. The original immutable05 manifest remains `eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00`.

## Claim and falsifiable criteria

The hypothesis under review was that this concrete source edition safely permits exactly one known-unattempted allocation under the original manifest identity, followed by exact existing-ID publication and ledger operations. Required conditions include source/adoption/old-intent/reconciliation validity after long guards and immediately at every write edge, durable single-attempt intents, fresh consistent account/native record-concept families, strict tracker response preservation, and no blind retry after an ambiguous outcome. A permitted write or operational verified receipt under deliberately invalidated prerequisites falsifies the corresponding claim. Conservative references must trigger reconciliation rather than automatically establish mathematical duplication.

The accepted scientific manuscript and actual merge are inherited context, not hypotheses newly proved by this operational review. There was no actual Zenodo allocation, DOI reservation, upload, publication or tracker append in this review.

## F1 — The ledger mutation bypasses the new final write-edge checks (P1)

`lifecycle06.py:202` replaces the inherited `GuardedClient` and `require_action`. At `lifecycle06.py:214`, ledger still calls the inherited `append_ledger` directly. Its sole append at `operations/publish_and_ledger.py:160` is a direct GWS command, outside `EdgeDelegate`.

The last approval and freshness checks in that function are at line153. They precede the exclusive synchronized `LEDGER_APPEND_INTENT.json` writer at line154. There is no approval/context/source or time check after that writer and before the command. There is also no postappend local-context check before `LEDGER_VERIFIED.json` at line166.

Fresh cases `ledger_after_fsync_approval_revoked`, `ledger_after_fsync_old_intent_changed`, `ledger_after_fsync_source_changed`, and `ledger_after_fsync_clock_expired` hook only **after the real durable intent writer and its directory synchronization return**. Respectively they rename the fake approval away, change the preserved original stage intent ID to999, change the checked06 source copy, or advance the test clock181seconds. Each actual parsed ledger call then delegates exactly one fake append, returns `verified: true`, and saves `LEDGER_VERIFIED.json` with no exception. All three Python modes reproduce all four cases.

The control `ledger_revoked_after_complete_gate` correctly stops before append: it revokes earlier, before the final inherited `require_action`. The five native-edge controls also stop their next create/upload/update/publish when approval is revoked after their synchronized per-write intents. Thus the fault is the missing ledger edge adapter, not an inert approval test or an unexercised gate. The source drift counterexample changes only owned fixture source, never the frozen production source.

## F2 — Ledger does not refresh its native family after the long collector (P1)

`append_ledger` obtains the native target in `verify_public` at line111, then runs the full account/ledger collector at line132. The family comparison at lines133–134 uses that earlier snapshot. Later freshness checks use `public['at']`, stamped after the public file/DOI work, with the default180second bound; they do not check the native snapshot's `observed_at` with its30second bound. There is no new native observation after the collector.

In `ledger_native31seconds_after_complete_gate`, the virtual clock advances31seconds after the full collector returns. This makes the native observation older than its30second bound while the inherited180second checks remain satisfied. The parsed ledger action appends once and writes verified.

In `ledger_native_family_changed_after_complete_gate`, the completed collector sees family[777,778], then the fake provider's legacy and native target are coherently changed to family[777,999]. A fresh native observation would expose that disagreement. The parsed ledger call makes no such observation, appends once and writes verified. Both cases reproduce in all three modes.

This is a bounded freshness and ordering failure. It does not claim an atomic lock across two remote services is possible. The newly guarded native mutation path already performs its target observation after the long collector; the inherited ledger path does not.

## F3 — Tracker validation is not recursively type-strict or full-metadata preserving (P2)

`operations/ops_common.py` compares the numeric response's `dataFilters` to the expected range by ordinary Python equality. At line206 it also compares the entire FORMULA and value responses by ordinary equality. JSON Booleanfalse and integer0 compare equal in those structures.

`boolean_grid_echo` returns `startColumnIndex: false` in both numeric responses. `formula_only_boolean_echo` returns integer0 in the value response and Booleanfalse only in FORMULA. Both complete parsed stage calls still perform create, two uploads and metadata update, and save stage-verified. These are malformed numeric range echoes, not changes to literal cell values.

At line210, metadata preservation compares only the reduced `sheet_identity` projection. `metadata_bool_drift` changes an added sheet `hidden` property from Booleanfalse to numeric0 between paired metadata GETs. `fullmetadata_hidden_changes_between_paired_gets` alternates that property between valid Booleantrue and Booleanfalse. Both complete stage calls still succeed in every mode. The complete raw metadata is captured but is not compared or recursively validated. Root should explicitly adjudicate the intended metadata contract; the demonstrated acceptance is narrower than the requested strict recursive/full-metadata condition.

The tested old-row protections do work: old numeric and Boolean cells stop before allocation, and an equivalent-value formula substituted into an old cell after append prevents verification. This finding does **not** assert a numeric-to-Boolean old-cell corruption bypass, which the existing string-only cell schema excludes.

## F4 — Publication can certify after revocation during postwrite verification (P2)

The EdgeDelegate checks context immediately after the native publish delegate returns. The inherited guard then performs its postpublication native observation, followed by further reads in the shared uploader. `operations/publish_and_ledger.py:99` writes the publication-verified receipt without one more context check.

`publication_revoked_during_postwrite_native_verification` renames the fake approval after the first real synchronized native `verified.json` with `published: true` is written. The publication POST preceded that revocation and is not counted as an unauthorized post-revocation mutation. However, the actual parsed publication call subsequently returns success and writes `ZENODO_PUBLISH_VERIFIED.json` while approval remains absent. All modes reproduce this.

The source therefore does not establish a final current-adoption check before this standard operational receipt. Confirmed service success and its known ID/intents must remain preserved even when operational certification is refused; this finding does not suggest retrying publication or hiding a successful outcome.

## What survived independent attacks

The legitimate original-manifest lifecycle succeeds with uploader and collector using exactly the same owned state directory: stage, publish, public native/metadata/file/DOI readback, and a single numeric-ID literal-string append. A second stage invocation refuses without writes. Saved-state ID, manifest, and environment corruption each stop publication before any new native write. This confirms no initial no-own-state condition is incorrectly rerun after the runner's own allocation, while the original absolute manifest/state identity remains binding.

The five native write edges reject approval revocation after the real synchronized per-write intent. The create gate rejects181second expiry there; upload rejects31second native expiry there. Direct EdgeDelegate use without a guard fails, and a successfully consumed guard cannot be reused for another delegation. Internally coherent account/native family splits stop at first upload, second upload, update, publish and ledger when the split exists during the tested collector/native comparison.

Fresh complete-collector routes detect spelled-out PR labels, leading zeroes, encoded/Unicode whitespace forms, account keys, nested source/result evidence, local-state keys and exact repository URLs. Nearby11310 and an embedded-word/suffix control remain distinct. An exact root-adopted distinct ledger-row hash containing an explicit PR1131 cross-reference is accepted: a reference is a reconciliation lead, not an automatic duplication verdict. These are finite boundary controls, not a claim to recognize arbitrary paraphrases or every Unicode spelling.

Lost create, upload and update responses never authorize a second allocation or repeated write. Known IDs remain in failure receipts when observed; null IDs are expressly not treated as proof that no request was sent. Changing the preserved old intent inside update prevents stage verification. Lost append success is reconciled by exact GET readback and causes no second append. Source06 cache injection is rejected by the closed-source directory, project `sys.modules` poisoning does not select unverified project code, and direct unverified policy/lifecycle execution refuses.

## Method, counts and custody limits

The scenarios and their adjudications were authored in this review folder after reading the meaningful production paths. They invoke the actual checked06 `main` parser and inherited uploader/collector/native/GWS implementation. I read and reused the sealed `full_controls` provider transports and the preparation helper definitions, with explicit owned-path remapping and no change to frozen production algorithms. The exact helper prefix and all used original private seed fixtures are preserved with input hashes. The preparation's PASS decisions were not used as test verdicts.

There are48 designated actual-parsed scenario cases per mode,144 total. Explicit prerequisite and reentry callsites add up to82 parser invocations per mode,246 total. There are also two direct edge component cases and three source-loader component checks per mode,15 component checks total. The same11 counterexample scenarios recur in each mode,33 total. `REVIEW_RESULT.json` independently checks result counts, counterexample write/receipt conditions, per-mode counters, source bindings and all execution stderr files. It distinguishes subject-operation deltas from prerequisite fake writes.

All real network, process and credential execution paths are denied before lifecycle code loads; the fake token is a sentinel. All real escape counters and service/Git mutation counts are zero. No live service query was needed. Model writes are explicit counters and retained captures, not actual service effects. The source loader and every scenario use exact frozen source bytes. Normal, `-O`, and `-OO` executions completed without harness exceptions; no failed run was removed.

Current custody checks rehashed all196 immutable05 public payloads, the shared uploader dependency, all13 original runtime files and their inventory, all three wrapper files, six scientific release assets,44 current scientific source payloads,45 source-ZIP members, five upload-kit members and the frozen proposal. Original scientific clearance, freeze, old revoked clearance body, original stage intent and original manifest remain unchanged. Production06 runtime/authority is absent and readiness remains false. The known-no-attempt premise is inherited from the trusted root-observed pre-delegate traceback and preserved reconciliation, not independently inferred from absent local state.

I did not replay the historical approximately49.7GB logical custody archives or independently re-prove the scientific manuscript. Their previous whole05 review is preserved and source-bound context. I read the prior full05 report/decision, resumption HOLD report/decision, root HOLD adoption and relevant accepted-source constraints; no historical rejection was promoted to an acceptance. The eight preparation GitHub GET captures are sealed historical evidence of the accepted merge, not a fresh live lock. The real accepted merge/head remain the supplied identities, exercised by the current runner's GET-only checks in the model.

All work is inside this dedicated review directory. Identical completed owned evidence files are compacted by byte-and-mode-checked hardlinks; no original target/input inode is shared. The final recursive manifest includes every private capture, input copy, nested manifest, source, program, result and report with hashes, modes and nanosecond mtimes, excluding only its exact self path. Allocated size is checked against75MiB. No source repair, production approval, CASE/readiness write, Git action, external contact or service mutation was performed.

## Required disposition

Keep operations06 held. A separate source edition must protect the inherited ledger mutation at the actual post-intent delegation boundary, use fresh native/account family evidence there, and resolve the demonstrated response-validation and final publication-certification gaps. Preserve all old05/wrapper sources, runtime intents, known outcomes, revoked authority and scientific/merge identities. Any repair requires new exact source pins and a fresh independent whole-action review before root decides action authority. This report cannot supply that authority.

Review-family completion100%; overall sweep estimate80%. Decision: **HOLD**.
