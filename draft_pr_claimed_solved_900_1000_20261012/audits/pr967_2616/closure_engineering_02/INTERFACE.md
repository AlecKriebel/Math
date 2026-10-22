# Proposed PR967 closure interface (engineering; not execution approval)

Both entrypoints require an independently trusted interpreter launched with `-I -S -B`, after the human/root independently authenticates BOTH complete entrypoint files against the external operations inventory. An entrypoint cannot authenticate its own bytes before execution. The helpers additionally authenticate both files and compile captured core bytes in a child whose actual optimization level is zero.

Required arguments: `--operations-sha256 SHA --disposition-sha256 SHA`. Default prints read-only validation. `--execute` additionally requires `--approval-sha256 SHA` for a separate root approval produced after the fresh entire closure-package review. This third external pin avoids a circular decision/review dependency. These are proposed files; no live operation has run in engineering.

All relative evidence paths below are repository-root relative, starting `draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/`. A fingerprint is exactly `{bytes: nonnegative integer, sha256: lowercase64hex}`. A reference is exactly `{path, sha256}` and must have a matching fingerprint in the decision's `evidence_files`. JSON has unique keys and finite values.

## Operations inventory

`A/CLOSURE_OPERATIONS_INVENTORY.json`, exact keys:

- `schema: pr967-closure-operations-v1`, `pr: 967`, `problem_id: "2616"`, `original_pr_head: b356dec5cb01e5f536b9cfeece56ad08844c03cb`.
- `files`: exactly the two repository-relative helper paths, each with an exact fingerprint.

## Decision

`A/PRIORITY_DISPOSITION.json`, exact keys:

- `schema: pr967-priority-closure-decision-v1`, `utc`, `pr: 967`, `problem_id: "2616"`, `original_pr_head`, `disposition: CLOSE_WITHOUT_MERGE_ESTABLISHED_PRIORITY`.
- `operations_inventory_sha256`, `closure_comment_sha256`, `proposed_comment_sha256`. The latter two equal the exact UTF-8 bytes of `A/CLOSURE_COMMENT_DRAFT.md` including final newline.
- `families`: exactly the six actual family names. Each value is `{manifest: reference, authentication: reference}`. All authentication references can point to the concrete combined `ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json`. The existing root component-list selector and explicitly declared allowlist-field schema is accepted without alteration. All manifest members are freshly authenticated; exact falsifier uses its explicitly declared `explicit_allowlist`.
- `evidence_files`: closed fingerprint map containing every referenced manifest, combined normalization, original root authentication, actual full-intake record, readiness support, authorization, individual finding dispositions, historical qualification/addendum and any other cited evidence. Raw private sources must stay private; the helper privately checks the separately fixed source record itself.
- `readiness`: reference to a new root readiness record described below.
- `operation_authorization`: reference to separate root actor authorization described below.
- `finding_dispositions`: reference to the actual `ROOT_INDIVIDUAL_FAMILY_FINDING_DISPOSITIONS.json`. Its present schema is accepted directly, including identifier-origin disclaimers and sealed-file/section sources. All 35 separate entries are required: structural4/topology8/computational7/classical6/recent5/exact5. No invented claim that root narrative IDs were original-family IDs.
- `reason: mathematically_correct_rediscovery`.
- `scope`: exactly `{original_declared_turns: "1/5", historical_native_turn_count: "UNKNOWN", new_author_proof_responses: 0, proof_search_turns_added_by_audit: 0, no_ultimate_discovery_or_misconduct_adjudication: true, strict_historical_linked_body_hash_available: BOOLEAN, strict_historical_linked_body_hash_qualification_retained: true, credit_alone_restores_original_target_novelty: false}`.
- `historical_evidence`: exactly `{status, original_qualification: reference, archival_addendum: reference-or-null}`. Status is `PINNED_PREPR_ARCHIVE_BODY` when the boolean above is true, requiring a distinct pinned addendum; otherwise `NOT_AVAILABLE_QUALIFIED` and null addendum. The original qualified evidence remains immutable either way.

The exact reviewed comment must contain this marker once (root may append it as a final HTML comment before obtaining its final hash):

`<!-- PR967-PRIORITY-CLOSURE-v1:b356dec5cb01e5f536b9cfeece56ad08844c03cb -->`

## Root readiness

New JSON with exact keys `schema: pr967-root-closure-readiness-v1`, `utc`, `pr: 967`, `problem_id: "2616"`, `original_pr_head`, `checks`.

`checks` has exactly `source_identity`, `whole_proof`, `actual_reproduction`, `classical_priority_intake`, `recent_priority_intake`, `exact_priority_falsification`, `historical_date_qualification`, `finding_dispositions`. Every value is exactly `{status: "PASS", observed_utc, evidence: [reference,...]}`. Each list is nonempty and binds actual existing artifacts; these are root attestations after substantive intake, not manufactured execution receipts. Observed time <= readiness time <= decision time.

## Root actor authorization / lock

New JSON with exact keys `schema: pr967-root-operation-authorization-v1`, `utc`, `root_issued: true`, `pr: 967`, `problem_id: "2616"`, `original_pr_head`, `operations_inventory_sha256`, `closure_comment_sha256`, `operation_nonce: lowercase64hex`, `actor: {id: positive integer, login, node_id}`, `allowed_operations: ["comment","close","finalize"]`.

Current authenticated GitHub actor must match all three actor fields. Root supplies the actual identity after a read-only account check. The nonce binds a persistent exclusive filesystem lock. Runtime intents cannot predate authorization and must bind the separate current closure-package approval. Runtime files are private mode600 under a private mode700 directory; no previous receipt confers authority for another operation or target. This is a cooperating-process lock and provenance boundary, not protection against malicious replacement by the same OS user.

## Fresh closure-package review and approval

After engineering handoff, root assigns a fresh independent review of the entire current helpers, decision, exact comment and supporting evidence. It has a sealed manifest with exact equal unique `explicit_public_allowlist` and `files` map. Required members: `RESULT.json`, `AUTHENTICATION_START.json`, `AUTHENTICATION_END.json`, `FULL_AUDIT.md`, `RESEARCH_LOG.md`.

RESULT includes `pr`, `problem_id`, `original_pr_head`, `operations_inventory_sha256`, `decision_sha256`, `closure_comment_sha256`, `reviewer_agent_id`, explicit `started_utc`/`completed_utc`, and true `clean_context`, `entire_closure_package_review`, `full_reproducer_completed`, `clean_for_closure`, plus empty `required_issues` and `optional_issues`. This is distinct from the six specialized science families. Both authentication records bind those three exact pins with `status: PASS`, `utc`, and true `all26_original_bytes_and_modes_authenticated`, `all_six_family_members_authenticated`, `both_entire_helpers_authenticated`.

Root authenticates every review member before its substantive intake in a separate original root record with `utc`, `before_substantive_intake: true`, `all_members_authenticated: true`, `external_manifest_sha256`.

Then `A/CLOSURE_PACKAGE_APPROVAL.json` has exact keys `schema: pr967-root-closure-package-approval-v1`, `utc`, `root_issued: true`, `pr: 967`, `problem_id: "2616"`, `original_pr_head`, `decision_sha256`, `operations_inventory_sha256`, `closure_comment_sha256`, `reviewer_agent_id`, `status: PASS_ENTIRE_CURRENT_CLOSURE_PACKAGE`, `review_manifest`, `root_authentication`. Last two are exactly `{path, bytes, sha256}`. This approval's SHA is passed independently using `--approval-sha256` for any execute or existing-intent reconciliation. No current approval has been created by engineering.

## Operational limitations and recovery

Root approved a bounded immediate complete gate / one request / exact post-readback protocol. GitHub POST/PATCH does not offer atomic head/base/draft compare-and-act semantics. The helper records this limitation and stops on observed drift; it cannot promise no unobserved change in the request window. No automatic retarget, reopen, undo, repeated POST/PATCH, or blind uncertainty retry is permitted. A lost response is reconciled with GETs and full pagination against exact body, marker, authorized actor, target, pre-intent IDs and server timestamps. A closed target requires its known close intent and an actual matching actor closure event. A merged PR rejects.

Local finalization uses an exclusive cooperating operation lock, durable staged four-file intent, exact old/after byte reconciliation and atomic per-file replacement. POSIX rename is not a compare-and-swap against noncooperating writers. Observed foreign changes reject. A confirmed final receipt requires exact readback of state, inventory and both unique-marker logs. Later status scans are bounded to968..1000 and confer no whole-goal completion: root still requires two complete stable900..1000 final resweeps.
