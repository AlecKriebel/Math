# PR421 final administrative integration

Prepared offline for `AlecKriebel/Math`, PR421, branch `research/20001515-explicit-cubulation`, and exact selected ID `20001515`. No live plan, publication, Sheet write, ref update, readiness transition, merge, comment, release, credential read, checkout, or index operation occurred during preparation.

`finalize_pr421.py` has two explicit phases. `queue` integrates the accepted selected case and its published DOI into the latest caller-bound main tree on the PR branch. `merge` checks the original integration receipt, marks the accepted head ready if explicitly expected draft, and requests an ordinary GitHub merge with the exact expected head SHA. The default in both phases is a GET-only plan.

## Evidence and immutable package contract

The root must inspect the two actual full-package reviews, the original production publication tool receipt and tool source, the actual verified native Sheet readback, and the approved metadata before supplying bindings. This helper validates the specified evidence and byte bindings; it does not independently establish mathematical correctness, reviewer independence, tool execution provenance, or Sheet authentication. Root inspection of the original evidence is the remaining trust boundary. There is no newly invented trusted-true flag.

All original documents are case-relative regular files, opened through directory file descriptors without following symlinks. Their SHA256 values are positive caller bindings. The binding JSON itself is pinned by `--bindings-sha256`. RFC6901 JSON pointers name actual fields of original receipts; documents are not rewritten merely to fit a hypothetical receipt format.

The package references the three actual immutable native documents; no replacement reviewed manifest is created:

```json
{
  "candidate": {"path": "PREPRINT_PACKAGE_CANDIDATE.json", "sha256": "EXACT_ORIGINAL_CANDIDATE_SHA256"},
  "update_manifest": {"path": "global_candidate/packet-update-manifest.json", "sha256": "EXACT_ORIGINAL_UPDATE_MANIFEST_SHA256"},
  "application": {"path": "ROOT_DRAFT_PACKET_UPDATE_RECEIPT.json", "sha256": "EXACT_ORIGINAL_ACTUAL_APPLICATION_RECEIPT_SHA256"},
  "payloads": [
    {"name": "ACTUAL_PUBLISHED_FILENAME", "remote_path": "ACTUAL_SELECTED_BRANCH_PATH", "size": 123, "sha256": "EXACT_SHA256", "md5": "EXACT_MD5"}
  ],
  "findings_path": "unsolved_math_prioritization/attempts/20001515/publication/README.md"
}
```

This is a schema illustration, not executable evidence. The original candidate's native `/candidate_files` object maps local case-relative paths to SHA256 values; `/original_source_head` names the original source and `/candidate_update_manifest_sha256` pins the original update manifest. The update manifest's native `/entries` array contains `{local_path, remote_path, sha256}`, with `/expected_head` and `/expected_branch`. The helper joins the two exact complete inventories without reading unrelated files.

The original actual application receipt must natively report `/current_packet_verified`, `/manifest_sha256`, `/readback/actual_head`, `/readback/queue_selected_row/Status`, and every `/readback/files` mapping and actual blob/hash/mode result. These are authentic fields of the existing application helper, not newly invented true flags. Every original candidate path and hash must agree with both original update and actual application records; native expected/actual modes must be `100644`. The actual selected subtree is independently checked against these same complete byte pins and application Git blob SHAs. The `payloads` list contains exactly the deposited PDF and two ZIPs and joins their names, sizes, SHA256 and MD5 values to the original file pins. The Findings README is already an accepted file. No payload or README content is edited.

The binding document has these exact top-level fields:

```json
{
  "format": "pr421-original-evidence-bindings-v1",
  "reviewed_head": "EXACT_ORIGINAL_REVIEWED_PR_HEAD",
  "package": {"candidate": {"path": "PREPRINT_PACKAGE_CANDIDATE.json", "sha256": "EXACT_ORIGINAL_CANDIDATE_SHA256"}, "update_manifest": {"path": "global_candidate/packet-update-manifest.json", "sha256": "EXACT_ORIGINAL_UPDATE_MANIFEST_SHA256"}, "application": {"path": "ROOT_DRAFT_PACKET_UPDATE_RECEIPT.json", "sha256": "EXACT_APPLICATION_RECEIPT_SHA256"}, "payloads": [], "findings_path": "ACTUAL_ACCEPTED_PUBLICATION_README_PATH"},
  "reviews": [
    {
      "document": {"path": "ACTUAL_ORIGINAL_REVIEW.json", "sha256": "EXACT_SHA256"},
      "reviewer_family": "ROOT_INSPECTED_INDEPENDENT_FAMILY",
      "expected_review_head": "EXACT_HEAD_THIS_ORIGINAL_REVIEW_ACTUALLY_OBSERVED",
      "head_pointer": "/ACTUAL_REVIEW_HEAD_FIELD",
      "package_pointer": "/ACTUAL_ORIGINAL_CANDIDATE_SHA256_FIELD",
      "verdict_pointer": "/ACTUAL_VERDICT_FIELD",
      "accepted_value": "PASS"
    }
  ],
  "publication": {
    "document": {"path": "ACTUAL_ORIGINAL_TOOL_RECEIPT.json", "sha256": "EXACT_SHA256"},
    "tool": {"path": "BYTE_EXACT_CASE_RELATIVE_COPY_OF_ORIGINAL_TOOL.py", "sha256": "EXACT_ORIGINAL_TOOL_SHA256"},
    "record_id_pointer": "/ACTUAL_ID_FIELD",
    "doi_pointer": "/ACTUAL_DOI_FIELD",
    "state_pointer": "/state",
    "environment_pointer": "/environment",
    "verified_utc_pointer": "/verified_utc",
    "receipt_payloads": [
      {"name": "ACTUAL_PUBLISHED_FILENAME", "sha256_pointer": "/filesSHA256/ACTUAL_PUBLISHED_FILENAME"}
    ],
    "production_constraints": [
      {"pointer": "/metadata/title", "value": "EXACT_ACCEPTED_PRODUCTION_TITLE"},
      {"pointer": "/metadata/creators", "value": [{"name": "EXACT_ACCEPTED_CREATOR_REPRESENTATION"}]}
    ]
  },
  "sheet": {
    "document": {"path": "ACTUAL_VERIFIED_NATIVE_SHEET_READBACK.json", "sha256": "EXACT_SHA256"},
    "spreadsheet_id_pointer": "/spreadsheetId",
    "range_pointer": "/valueRanges/0/range",
    "values_pointer": "/valueRanges/0/values",
    "id_column": 3,
    "doi_column": 2
  }
}
```

Exactly two distinct original review hashes and distinct inspected reviewer families are required. Both bind the same original candidate SHA256. Each must bind the exact head it actually reviewed: either the original candidate source or the later actual reviewed head, and at least one must bind that actual updated head. A GET ancestry check proves that the later head descends from the original source; the native application receipt and independently read actual case bytes prove that the same original 53-file candidate occupies the later head. The first review is never represented as having observed a later head or a reshaped manifest. The verdict must match the inspected original string; supported acceptance strings, case-insensitively, are `accept`, `accepted`, `pass`, `passed`, `accepted_full_package`, and `accept_full_package`.

The original production tool's actual receipt must report `state == published`, `environment == production`, and a UTC verification timestamp. The pinned original tool source is for inspected provenance; the root must establish that its published-state interface checked server submitted state. No nonexistent submitted field is demanded in the tool receipt or public records API. Three distinct native payload SHA256 pointers join the original receipt to the manifest bytes. Optional `size_pointer` and `md5_pointer` fields are supported for each payload when those native fields exist. MD5 pointers may resolve to bare lowercase MD5 or `md5:`-prefixed MD5.

The helper independently GETs only `https://zenodo.org/api/records/<actual-record-id>`, with redirects disabled. It verifies production record ID, DOI `10.5281/zenodo.<id>`, the exact three payload names, sizes, and MD5 values. It checks only the explicitly approved metadata JSON pointers, including title and creator pointers. Incidental generated fields such as views, downloads, links, update timestamps, and stats are not overcompared. The stable approved-field digest excludes them. The production tool receipt supplies submitted/published assurance; public record existence supplies a separate public-access check.

The Sheet illustration uses the actual `values.batchGet` native fields expected by the root: Notes column 3 starts `20001515 / ...`, and DOI column 2 holds the DOI. The original readback must identify one actual row and its document/range, with exact selected ID and the same actual DOI or DOI URL at the explicit columns. Its original receipt hash is preserved. The helper does not make a Sheet write or fabricate a Sheet-verification boolean; root inspection authenticates that native readback.

## QUEUE and main preservation

Before opening the binding, manifest, receipt, tool source, or selected case blob, every initial plan/apply reads fresh PR421 metadata, the exact branch ref, and QUEUE at the exact head. It derives cells from the header `Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI`, rather than fixed offsets. Exactly one selected ID row and an unambiguous header are required. Any status other than exact `claimed_solved` produces a skip before candidate/evidence reads. For a claimed row, the Contents blob SHA must also equal the actual QUEUE entry in the exact head commit's verified immediate Merkle tree before any evidence or candidate file is opened. Draft/open checks match the explicit phase. Current-main QUEUE reads are administrative and may contain the older `queued`, `Turns 0/5` selected row.

The integration uses the entire accepted branch selected row, preserving its `claimed_solved`, `Turns 1/5`, blank Chat, and all other accepted fields. Against that accepted row, only DOI and Findings change. The DOI cell is `[DOI](https://doi.org/<actual-doi>)`; Findings points to the actual accepted publication README. The resulting selected row is transplanted into current-main QUEUE. Every byte outside that one current-main row remains exactly unchanged. Duplicate IDs/headers, ambiguous unescaped pipes, missing cells, or differing table headers stop before mutation. Header reordering, escaped pipes and CRLF are covered offline.

The helper never calls the recursive tree endpoint. It verifies each traversed immediate tree by reconstructing the exact Git tree SHA. It traverses only QUEUE/selected-case ancestor directories and the selected case itself. Every untouched current-main subtree is preserved by its exact opaque SHA, including modes, symlinks, submodules, and empty trees. A restricted Merkle diff rejects every original PR change outside the selected subtree and QUEUE; the original PR QUEUE must preserve all bytes outside its selected row relative to the merge base. A current-main selected subtree conflicting with both merge base and accepted source stops before mutation.

Each replacement tree is computed from current-main immediate children, replacing only the accepted selected-subtree SHA and computed QUEUE blob SHA. Child trees are created before their parents; exact immediate tree responses and complete resulting root identity are verified. The integration commit has exact parents `[accepted-head, current-main]`, so both histories remain ancestors. It uses `Alec Kriebel <me@aleckriebel.com>` and a pinned UTC date. Exact predicted commit SHA, tree, parents and attribution remain mandatory. GitHub's observed JSON message representation may omit exactly one submitted terminal newline; no other whitespace normalization is accepted.

There is one non-force branch PATCH in the `queue` phase, after a third fresh exact-head/main/draft/status gate. Main is never directly updated by that phase. No checkout, index, branch switch, pull, reset, force push, PR title/body/comment/review request, status edit, close call, release, or publication API write exists.

## Commands and recovery

These templates are documentation only and were not executed against a live service:

```sh
python3 -B merge_preparation/finalize_pr421.py --phase queue \
  --expected-head EXACT_REVIEWED_HEAD --reviewed-head EXACT_REVIEWED_HEAD \
  --expected-main EXACT_CURRENT_MAIN \
  --bindings CASE_RELATIVE_BINDINGS.json --bindings-sha256 EXACT_BINDINGS_SHA256 \
  --run-id fresh-queue-plan
```

Add `--apply` with a fresh run ID only after root inspection of the concrete live plan and the actual evidence. The `merge` phase needs `--phase merge`, `--expected-head EXACT_INTEGRATED_HEAD`, the same original reviewed-head/evidence bindings, and `--integration-receipt CASE_RELATIVE_ORIGINAL_INTEGRATION_RECEIPT.json --integration-receipt-sha256 EXACT_RECEIPT_SHA256`. It refuses a changed main commit or a source tree requiring another integration. Its fresh gate must still be exact `claimed_solved`. Default `--expected-draft true` explicitly enables one readiness transition after the publication and Sheet proofs. If a previous readiness transition has already been read-only reconciled, explicitly use `--expected-draft false`; that run does not repeat readiness.

All run journals and receipts are private under `private_sources/merge_preparation/runs/<run-id>/`. Each intent is appended and fsync'd before its write. Exclusive durable action/head claims survive process death and prevent a new run ID from blindly repeating uncertain ref/readiness/merge actions. Existing journals and receipts are never overwritten. Content-addressed object response loss is checked by GET of the exact predicted object; it may continue only after that object's exact identity/content is established, without repeating its POST. Ref, readiness and merge response loss stop all further mutations in that run, even when a GET establishes the historical outcome. Reconciliation never resumes writes:

```sh
python3 -B merge_preparation/finalize_pr421.py --reconcile --run-id ORIGINAL_RUN_ID
```

Recovery reads a complete no-symlink journal and uses only GET calls. Do not remove durable claims or manually retry an action merely because its CLI response was lost. The root must independently establish the prior disposition. A lost readiness response cannot flow directly into a merge in that run. A lost merge response may yield a verified historical merge receipt, but never triggers another merge.

GitHub provides expected-head SHA binding for merge and a non-force update for refs, but neither an atomic main-ref compare-and-swap for the merge API nor a head-SHA condition for readiness. Exclusive control of the accepted branch and coordination of main during the short mutation window remain operational assumptions. The ready response must return the exact accepted `headRefOid`; a differing response records factual readiness history and stops merge. A sibling head advance rejects the sole non-force PATCH; any main advance detected before merge stops readiness/merge. A later unrelated main advance in the merge window is verified against the actual merge commit first parent, not a stale main snapshot. A concurrent conflicting selected-case or selected-row change cannot be certified; the helper stops and preserves historical mutation metadata. It never bypasses GitHub mergeability (`mergeable == true`, `mergeable_state == clean`).

Final receipts require actual PR merged/closed/non-draft metadata, the actual merge commit with exact accepted PR head as second parent, the resulting main equal to or descending from that merge, exact accepted selected subtree and published payload hashes, the actual DOI/Findings row, and full Merkle preservation of the actual main first parent's unrelated content. Before any case processing at a newly observed merged/current head, its selected QUEUE status is checked. A status or packet drift preserves truthful historical merge/ref response metadata while refusing current-packet verification.

## Offline evidence and public files

`private_sources/merge_preparation/test_offline.py` uses independently serialized synthetic Git objects and a fake API. It never executes gh or network calls. Tests cover main `queued`/branch `claimed_solved`, unrelated rows and tree leaves, empty trees and modes, exact immutable payloads, all three response-loss points, durable claims, head/main races, final ancestry, native receipt mismatch, ambiguity, no-symlink input, production MD5 prefixes and incidental metadata, and real GitHub terminal-newline representation. Normal and `-O` modes use explicit exception gates, with no bare assertions.

Use only `PUBLIC_OUTPUT_WHITELIST.json` for public preparation delivery. Original evidence, fixture sources, mock payloads, journals, recovery state, runtime directories and private source copies are excluded. The root owns any subsequent Git checkpoint, remote publication, Sheet operation and merge. This folder's preparation does not attest that those actions occurred.
