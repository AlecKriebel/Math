# PR662 operation helpers: scope and use

These are proposed operational helpers, not an acceptance, DOI reservation, upload, tracker append or merge. This author run made no live API or network calls. Independent whole-package/operational review is required before production use. All operation receipts are outside the uploaded ZIP to avoid self-reference.

The original `unsolved_math_prioritization/attempts/2306086/` verifier requires exactly 24 files. It rejects added files, bytecode caches and empty directories. Integration therefore preserves **every original attempt file and byte**, including both manifests and the verifier, and places the publication in sibling `unsolved_math_prioritization/publications/2306086/`. The selected queue finding links both directories. The actual proposed-layout control copies the complete publication sibling and untouched native attempt, then runs the original verifier with replay/self-test and the supplement verifier with replay from temporary copies.

The scoped mathematical claim remains qualitative `claimed_solved`, `5/5`: strict improvement at every fixed nonreal point, compact nonreal uniformity, and sharpness on the real diameter, with the source expression at zero handled separately. No explicit upper gap, sharp radius, general extremizer, full variability region, historical firstness or current-openness certification is promoted. Classical credit and the Jenkins (1960)/Aleksandrov–Popova (1973) original-source limits remain in queue text, publication notice, tracker notes, metadata and the description template. Extensive AI use and unrefereed status remain explicit.

## Accepted-input file

The parent must create `ACCEPTED_PUBLICATION_INPUTS.json` only after final review. Its schema is:

```json
{
  "schema": "pr662-accepted-publication-inputs-v1",
  "pr": 662,
  "problem_id": "2306086",
  "original_head": "e31701151c331a6eed9224fb37a75a374ea1043e",
  "ready_for_publication": true,
  "files": {
    "real_schlicht_preschwarzian.pdf": {"bytes": 0, "sha256": "actual 64-character lowercase SHA-256"}
  },
  "whole_package_review_rounds": [
    {
      "reviewer_id": "distinct fresh agent identity",
      "report_path": "reviews/actual-round/VERDICT.json",
      "report_sha256": "actual report SHA-256",
      "mandatory_findings": 0,
      "optional_findings": 0
    }
  ]
}
```

This example is incomplete and deliberately cannot pass. The `files` object must have **exactly all eleven** keys below, each with its actual byte count and hash:

- `real_schlicht_preschwarzian.pdf`
- `real_schlicht_preschwarzian.tex`
- `real_schlicht_verification.zip`
- `zenodo-deposit.json`
- `PACKAGE_README.md`
- `CURRENT_PRIORITY_AND_STATUS.md`
- `CLAIM_SCOPE.json`
- `requirements.txt`
- `requirements_numerical.txt`
- `verify_package.py`
- `build_package.py`

At least two entries in `whole_package_review_rounds` are required, with distinct reviewer identities and report paths, zero integer mandatory/optional counts, and the SHA-256 of each preserved report. Reports are read relative to the audit root, captured, and copied into the publication sibling. This gate is the parent's review attestation; hashes and counters alone do not prove the independence or correctness of a review. The parent must read and adjudicate those reports.

The code accepts only the original open draft head/branch/base and exact selected `claimed_solved`, `5/5` row before reading candidate or publication contents. A head change requires fresh adjudication. It checks the 24 local native files against the immutable snapshot and the original Git blob inventory. Remote main must lack both selected directories and retain the queued `0/5` target row with all other original fields unchanged. Integration restores the reviewed status/turns and replaces only its finding; every unselected queue byte and all unrelated tree entries are preserved. The blank DOI cell and other semantic fields are retained; the DOI is in the finding and publication notice.

## Publication receipts and metadata

Both `ZENODO_PUBLICATION_RECEIPT.json` and a distinct `ZENODO_POST_PUBLICATION_INSPECTION.json` must exist after production publication. The kit receipt and independent inspection must agree on production/published state, title, DOI/record identity, exact two-file inventory, byte sizes and SHA-256 values, and successful DOI resolution. Metadata normalization must be empty; a nonempty normalization requires explicit adjudication and code review, not silent acceptance.

The kit's normalized receipt is an attestation produced after its metadata-verification routine; it does not itself embed a full copy or byte hash of the remote metadata. The parent must therefore run the kit against the exact accepted `zenodo-deposit.json` and independently inspect that remote metadata. The helpers bind the exact local metadata bytes, creator/ORCID, scope/disclosures and archive copy, and record its SHA-256. They do not replace the kit's remote metadata verification or the independent inspection.

All payloads, scope documents, receipts and reports are read once into immutable byte captures. The ZIP is checked for safe regular paths, duplicate members, manifest inventory/hash/size coverage, native24 binding, exact accepted PDF/TEX/metadata/current documents, and the immutable snapshot. Extraction/replay happens only after those checks, under the pinned interpreter. The archive's exact reviewed hash is also required by the acceptance gate; checksums are not signatures or formal proof certificates.

## Final commands

Run from the audit directory with the pinned environment, **preserving its executable symlink**. Do not substitute the system Python, which lacks required dependencies. Set `DOI` below to the actual confirmed DOI; do not use a fixture identifier.

```text
/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python -I -B prepare_integration.py --doi DOI
/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python -I -B prepare_integration.py --doi DOI --push
/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python -I -B record_tracker.py --doi DOI
/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python -I -B record_tracker.py --doi DOI --apply
```

These are invocation forms, not instructions to run them before the gates. The first integration command creates local objects and a prepared receipt only. The parent should inspect the prepared tree and receipt, then rebuild for `--push` if main has advanced. No whole-repository index is created: small trees are assembled with blobs/tree objects and spliced into latest remote main, forwarding all unrelated entries. Shared local HEAD/main/index remain untouched. Automatic GC/maintenance is disabled for the helper's Git commands. A known concurrent-fetch compare-and-swap error is reconciled only if the updated tracking SHA exactly equals advertised main; other errors abort without cleanup or an automatic fetch retry.

The explicit push is an ordinary non-force update of the existing research branch. A durable push intent precedes dispatch. A success receipt is saved before any GitHub metadata comparison. The actual remote branch must match the pushed commit; delayed GitHub PR metadata is marked pending rather than treating a successful push as unsent. The parent must separately confirm the new PR head and final queue status, update the description from the reviewed template with the real DOI, mark ready and merge. This helper does not merge or edit the PR description.

Any existing push intent or successful push receipt stops another invocation. An uncertain push requires read-only reconciliation against its exact recorded SHA. There is no helper retry/force/reset/cleanup option.

Tracker operations use the Google Workspace CLI on spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, gid `1254632077`, tab `Math Puzzles`, exact A:D headers `Original Problem`, `Solution Chat URL`, `DOI`, `Notes`. The chat URL is blank. The script captures `prepare_integration.py` as regular source bytes, compiles it in a fresh private module, ignores cached bytecode, and records the source hash in readiness/confirmation receipts.

`--apply` refreshes tab/header/DOI guards, records a durable append intent, and sends one RAW/INSERT_ROWS append with values echoed in the response. It checks response shape, exact target-row readback and global DOI uniqueness. A local exclusive operation lock prevents two local copies racing. A concurrent external writer cannot be locked by this client; post-write uniqueness detects such a collision and leaves an unconfirmed intent. Existing matching rows are confirmed with reads, without another append. Existing conflicting or duplicate DOI rows stop. Any prior dispatched intent with an absent DOI stops rather than retrying, even if a prior outcome had been confirmed. An exact existing row can reconcile an uncertain intent through read-only verification.

## Author controls and limits

`offline_controls.py` uses synthetic publication/service fixtures and a disposable real Git repository. It tests malformed/duplicate JSON, path escape, selected-status/head drift, acceptance/review-pin changes, scope inflation even with rebased outer pins, native mutation/inventory changes, receipt mismatches, ZIP duplicate/symlink/unsafe/unmanifested/native-substitution controls, fetch CAS races, both default no-write modes, subtree/mode preservation, explicit push intent/readback/sticky failures, header/gid/DOI conflicts, append uncertainty and reconciliation, echo/range/readback failures, local locking, and hostile timestamp/size-valid stale pyc exclusion. External services and costly replays are explicitly doubled only in the lifecycle tests.

`replay_proposed_tree.py` separately runs the real native verifier and the actual current supplement verifier from temporary copies of the proposed layout. Its synthetic DOI/receipt placeholders assert no real publication or acceptance. Its output binds the exact publication snapshot it tested. The parent must repeat the final accepted integration replay after any changed package or operation code.

No Zenodo/GWS/GitHub live state was checked by this author task, and no external write occurred. Independent review and live final gates remain necessary.
