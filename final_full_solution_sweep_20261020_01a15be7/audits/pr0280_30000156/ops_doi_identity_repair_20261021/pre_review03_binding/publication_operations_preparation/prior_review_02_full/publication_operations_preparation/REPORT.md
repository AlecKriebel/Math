# PR280 publication operations preparation

Prepared and tested offline on 2026-10-21 UTC. Completion of this preparation task: **100%**. Scientific clearance, merge, staging, DOI allocation, publication, ledger append and publication success are **not asserted**. The root alone decides and executes lifecycle work after its reviews pass. No live API/provider/network access or branch, index, ref, PR or ledger mutation was performed in this preparation.

Seven new helpers sit at the PR280 audit root. The exact files and SHA-256 values are in `SOURCE_AND_HELPER_BINDING.json`; the complete adaptation diff is `TEMPLATE_ADAPTATION.diff`. All five PR397 source helpers, its root clearance, and the three relevant package03 operational tests were read completely and remain unchanged.

## Offline verification

`offline_controls.py` exercises actual imported helper functions with explicitly synthetic service boundaries. Generic process/network/provider access is prohibited during the tests. Both normal Python and `python -O` pass **158 controls: 22 acceptance cases and 136 rejection cases**, with **zero actual provider access attempts**. The results are `OFFLINE_CONTROLS.json` and `OFFLINE_CONTROLS_OPTIMIZED.json`. All eight authored Python files parse successfully. Operational checks use explicit exceptions; no production guard relies on `assert`.

Coverage includes exact 17-original/five-publication integration, the original parent and head queue rows including their different Notes, preservation of unselected repository-root, `unsolved_math_prioritization` and `attempts` siblings, other queue bytes, changed/missing/colliding original/publication files, duplicate/changed own queue rows, wrong PR head/state/destination, full account pagination and invariant totals, keyword-omitted drafts found by model or file checksum, fresh four-column ledger schema, malformed/expired gates, missing root clearance/reconciliation, changed metadata and every part of a reconciled full file projection, exact public metadata/DOI/version/files/downloads/internal archive payloads, durable intents before synthetic mutations, no blind lifecycle/append retries, whole-sheet DOI duplicates before append, and exact unique readback.

## Material differences from PR397

- Originals are `SOURCE_SNAPSHOT.files[*].path/snapshot/bytes/git_blob/sha256`, exactly 17 files under `unsolved_math_prioritization/attempts/30000156`. Local snapshots are checked against both SHA-256 and the Git blob identity. PR397 used 24 files and a different directory/schema.
- The exact original commit is `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`; its sole parent is `c053681c57cb775eaa8782312e98db430e40b43b`. The parent’s `queued | 0/5` row has blank Notes; the head’s `claimed_solved | 1/5` row has the reviewed counterexample note. Both exact rows are derived from and checked against those commits. The helper never reconstructs the baseline by replacing a status string.
- Nested preservation compares immediate children at the repository root, `unsolved_math_prioritization`, and `unsolved_math_prioritization/attempts`. Exact candidate leaves and whole queue bytes are checked independently. The branch overlay uses GitHub’s exact-tree overlay and a non-forced fast-forward update; it never writes the local checkout, shared index, branch or ref.
- Frozen release SHA-256 is `548b7a4ae1f13a92029255fc9ef485002b7c33376b9dd9168ffcdb532fc4c20e`. Five publication files are copied into the PR as `preprint/` files; only the PDF and verification ZIP are uploaded. The PR280 ZIP manifest is a **list** of 64 payload entries; the archive has 65 safe, unique members, including its manifest and editable paper source.
- Root scientific clearance now binds every operational helper, the root lead reconciliation, every named reviewer report and seal, and the exact release manifest/five files. It requires at least two distinct sequential reviewer entries, no unresolved material findings, and the root’s affirmative statement that all full reports and seals were verified. It is a trusted root assertion with byte checks; these helpers do not infer scientific correctness from reviewer labels.
- Deduplication uses only PR280/problem/source/model terms: `30000156`, `OWR-768-006`, PR280, birational, cycle distribution, fixed triangular map, Vivaldi, primitive fibers and positive-density nonconvergence, plus upload checksums. No PR397 non-target record IDs or result claim are exempted. The generic authenticated-account known-record positive control remains Fibonacci record 23174283; that control is **not** a non-target exemption.
- Every phase collects fresh whole-sheet data and a complete authenticated account enumeration including drafts, with exact totals and pagination checks. Every matching existing non-target record requires root `distinct_non_target` disposition and the exact SHA-256 of **all metadata and the entire files projection**. Metadata-only exemptions are rejected. Changed/new ledger leads likewise fail closed. All live raw account and ledger bodies are confined to ignored `private/pr0280_ops/`.
- The historical PR280 ledger snapshot was inspected: it is `{checked_at,response}`, with values under `response.values`. The adapter explicitly accepts that wrapper or a direct provider values object and rejects other wrapper guesses. The fresh full-sheet read checks all returned data against the existing four-column schema; row counts are observed, never hardcoded to 176.
- Gates bind phase, exact head, release and expected allocated ID and expire after 180 seconds from collection start. Stage/publish/append require a closed merged PR. Stage/publish also require the actual verified merge preservation receipt. Initial staging has no assumed allocated ID; an existing draft/local state blocks an automatic new stage. Durable lifecycle intents stop blind retries after uncertain outcomes.
- Public verification checks every intended metadata field on both authenticated inspection and the public record, with exactly the cached public API’s structural `resource_type.type/subtype/title` and `license.id` representation projected to deposition fields; unexpected resource types, subtypes, titles, licenses, conflicting type fields or schema changes reject. It then checks the exact DOI with HTTP 200, both actual downloads against SHA-256/MD5/size, and every archive payload. The ledger helper performs this verification anew before the final account/sheet gate; saved success booleans alone do not permit an append. The final whole-sheet read must equal the gate’s full-sheet digest. Duplicate DOI/result rows block before append; one intent precedes one append and exact unique readback follows it.

## Required root-authored schemas

No root clearance or root lead reconciliation is authored by this task. The helpers fail closed until the root supplies both after its review. SHA-256 JSON projections use UTF-8 `json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))`.

`ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json` must contain:

```json
{
  "pr": 280,
  "root_identity_reconciliation_complete": true,
  "unresolved_leads": [],
  "release_manifest_sha256": "548b7a4ae1f13a92029255fc9ef485002b7c33376b9dd9168ffcdb532fc4c20e",
  "account_leads": [],
  "ledger_leads": []
}
```

For every matching account record cleared as distinct, `account_leads` contains `{ "record": <integer>, "disposition": "distinct_non_target", "metadata_and_files_sha256": <digest> }`, where the projection is `{ "metadata": record["metadata"], "files": record["files"] }`. Every matching ledger row cleared as distinct has `{ "values_sha256": <digest of full values array>, "disposition": "distinct_non_target" }`. Empty lists are valid only when fresh evidence has no such leads. The expected staged/published target ID may never be included among exempt non-target records. Root reconciliation is mandatory even if there are no leads.

`ROOT_PUBLICATION_CLEARANCE.json` must contain the following fields after actual root review:

```text
pr: 280
problem_id: "30000156"
original_head: "091bdecef6f84154f5d5c205a4b07eeb6391b8f8"
publication_ready: true
unresolved_material_findings: []
release_manifest_sha256: the exact frozen manifest SHA above
files: exactly RELEASE_FILES.json.files, in the same order
root_complete_reports_read_and_all_seals_verified: true
sequential_new_reviewers: at least two distinct entries, each with
  reviewer, report_path, seal_path (paths relative to this PR280 audit)
bound_review_artifacts: [{path, bytes, sha256}, ...] covering every report_path/seal_path
bound_operational_files: [{path, bytes, sha256}, ...] for exactly
  ops_binding.py
  prepublication_check.py
  publication_live_gates.py
  repository_integration.py
  publication_lifecycle.py
  record_publication_ledger.py
  verify_published_files.py
  ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json
```

The frozen release manifest’s `publication_ready: false` records its preparation state and is left byte-identical. A future affirmative root clearance governs the operational gate. Any package change requires a new review and updated operation binding; changing that immutable manifest alone will deliberately block the helpers.

## Ordered root workflow, not executed here

Run from this PR280 audit folder, keeping the shared local checkout on main. `H` below means the exact head returned and verified by the branch overlay, not an invented ref; `ID` means the exact newly returned staged deposition ID. No DOI is preallocated or assumed.

1. Finish the scientific/package review loop. For initial fresh evidence, the standalone collector is read-only and does not itself grant clearance:

   `python3 prepublication_check.py --phase before_integration --expected-pr-head 091bdecef6f84154f5d5c205a4b07eeb6391b8f8`

   Read the returned ignored private receipt and raw full account/sheet bodies; reconcile all exact/model/file leads. Author the root reconciliation, then the fully hash-bound root clearance after independent operational review. Recheck the preparation seal and helper hashes.

2. Review the read-only overlay plan, then make the exact existing-branch overlay:

   `python3 repository_integration.py plan --expected-pr-head 091bdecef6f84154f5d5c205a4b07eeb6391b8f8`

   `python3 repository_integration.py commit --expected-pr-head 091bdecef6f84154f5d5c205a4b07eeb6391b8f8`

   This internally gates before object creation and refreshes again immediately before the non-forced ref update. Save the returned new commit as `H`. Reconcile an existing intent/outcome instead of replaying an overlay after a partial outcome.

3. Wait for GitHub’s clean current test merge, then verify it:

   `python3 repository_integration.py verify-test-merge --expected-pr-head H`

   After scientific clearance and the exact head check, the root may mark PR280 ready using `gh pr ready 280 --repo AlecKriebel/Math`. The helper does not silently change draft status. Then:

   `python3 repository_integration.py merge --expected-pr-head H`

   This checks the current test-merge parents/tree, gates afresh, saves a merge intent, sends the exact head to GitHub, and verifies the actual merge parents/tree before writing `PR_MERGE_VERIFIED.json`. Any concurrent-main discrepancy stops publication for reconciliation.

4. Stage exactly the two frozen upload files:

   `python3 publication_lifecycle.py stage --expected-pr-head H`

   Read the returned exact ID and record it as `ID`; do not substitute a guessed DOI/ID. The private full account gate must have no unreconciled draft lead before this action.

5. Immediately before publication the helper repeats the full live gate with that exact target ID:

   `python3 publication_lifecycle.py publish --expected-pr-head H --deposit-id ID`

   A prior stage/publish intent intentionally blocks blind repeats. Inspect the saved exact-ID record and account to resolve an uncertain outcome; do not create a replacement record automatically.

6. Download and verify the exact public record, metadata, DOI200, PDF/ZIP and all 64 hashed payloads:

   `python3 verify_published_files.py --deposit-id ID`

7. Append or idempotently verify exactly one ledger row:

   `python3 record_publication_ledger.py --expected-pr-head H --deposit-id ID`

   This performs a fresh public verification again, followed by the final full account/sheet gate, last whole-sheet equality/identity check, durable intent, one append and unique exact readback. It writes the existing four headers only, with the exact source URL, PR280, bounded-priority scope, extensive AI involvement, unrefereed status and no formal independent human peer review.

8. Root alone records global progress and checkpoints/pushes findings after verifying actual outcomes. This child did not touch global STATE, journal, logs, manuscript, frozen release, original snapshots, historical seals, shared index/refs, providers or unrelated efforts.

## Limits and remaining gate

These tests validate the local adapter mechanisms against meaningful fixtures; they do not certify a future live account’s schema, worldwide publication absence, scientific novelty, provider availability, or a lock spanning services. Fresh live checks and exact root reconciliation remain required. Provider uncertainty is handled by stopping with durable intent/evidence and inspecting the existing outcome, never by a blind second mutation. The parent must independently inspect and accept these helpers before binding them into root clearance.
