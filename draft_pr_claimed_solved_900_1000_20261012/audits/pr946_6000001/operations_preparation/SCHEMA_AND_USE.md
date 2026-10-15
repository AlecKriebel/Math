# PR946 operation preparation contract

This document describes prepared helpers. It authorizes no action and records no
acceptance, merge, upload, tracker write, native event, or additional proof turn.
The root research agent must freeze and independently review the complete paper,
package, and these helper bytes before invoking an operation.

## Trust and invocation

All six entry points require Python `-I` or `-P` **before** any nonbuiltin import.
`-I` is preferred for operations. On Python 3.11+, `-P` is available for measuring
actual `PYTHONOPTIMIZE=2` outer behavior. The first builtin `sys` guard rejects an
unsafe entry before a neighboring `argparse.py` can execute. This requirement
does not claim that arbitrary environment variables or installed Python runtimes
are untrusted-safe. The invoking interpreter, standard library, Git, GitHub CLI,
Google Workspace CLI, supplied external pins, and original entry point are trust
roots. The checks are provenance controls, not an operating-system sandbox.

Every helper requires `--operations-sha256` with the externally authenticated
SHA-256 of `audits/pr946_6000001/OPERATIONS_INVENTORY.json`. Acceptance additionally
requires `--freeze` and a complete consecutive sequence of `--review` values
`01:SHA256`, `02:SHA256`, and so forth. The Zenodo helper additionally requires
one action: `stage`, `publish`, or `inspect`. Other helpers have no action switch.
No helper performs an operation on import. Every operational core executes
captured, authenticated bytes in an actual `-I -S -B` subprocess, optimization0.

The root should invoke these entry points only after deciding that their named
action is ready. The preparation tests do not invoke them against the real
repository or external services.

## Operations inventory

The inventory is a JSON object with these exact identity values:

- `schema`: `pr946-operations-v1`.
- `pr`: integer946; `problem_id`: string`6000001`.
- `original_pr_head`: `7d3adb0e500b0414a49a449e7981d34ade329427`.
- `files`: repository-relative names mapped to exact `{"bytes":integer,"sha256":hex}`.

There must be exactly seven names: the six prepared helpers under
`draft_pr_claimed_solved_900_1000_20261012/` and
`zenodo_deposit_tool/zenodo.py`. The kit stage/publish/inspect path is standard
library only; the kit's separate metadata-update import path is never used.
All seven files are authenticated before **any** captured dependency executes.
Every ancestor is opened from the repository descriptor with directory/nofollow
flags, and final reads use `O_NOFOLLOW|O_NONBLOCK`, `fstat` regular-file checks,
declared-size and growth caps. Captured bytes are executed without reopening the
checked code path. The standalone kit receives the same captured-code treatment.

## Freeze

Canonical location: `audits/pr946_6000001/preprint/FREEZE.json`. Fields:

- `pr`, `problem_id`, and `original_pr_head` as above.
- `revision_candidate`: positive integer.
- `operations_inventory_sha256`: externally pinned operations inventory.
- `future_helpers`: all six basenames mapped to fingerprints matching inventory.
- `files`: explicit preprint-relative fingerprint map, excluding `FREEZE.json`.
- `evidence_files`: explicit repository-relative fingerprint map. It must include
  `ORIGINAL_SNAPSHOT.json`, `TARGET_IDENTITY_PREFLIGHT.json`, and
  `PRIORITY_DISPOSITION.json` beneath this PR's audit folder. More immutable root
  evidence may be included.
- `package_manifest_sha256`: inner package manifest SHA-256.
- `archive_manifest_sha256`: outer archive manifest SHA-256.
- `pr_description_sha256`: SHA-256 of the **original live PR body** to remain
  unchanged through acceptance and merge. This is independent of a frozen
  `preprint/PR_DESCRIPTION.md` publication draft. No preacceptance edit is needed.
- `replay_normalization_ignored`: exactly the empty list. Stable canonical
  receipts are compared without silent version, path, timing, or mathematical
  field deletion.
- `archive_layout`: exactly `manifest`, `package_manifest`, `original_prefix`,
  `pdf`, and `verifier` keys, each naming an explicit safe archive path. The
  original prefix ends in `/`; its remaining suffixes are matched against all33
  immutable originals. Root's agreed values are `ARCHIVE_MANIFEST.json`,
  `package/PACKAGE_MANIFEST.json`,
  `package/original/unsolved_math_prioritization/attempts/6000001/`,
  `research_note.pdf`, and `package/verify_package.py`, respectively.

Required frozen files include `research_note.pdf`, `research_note.tex`,
`global_hessian_verification.zip`, `zenodo-deposit.json`,
`package/verify_package.py`, `BUILD_RECEIPT.json`, and four
`PACKAGE_REPLAY_normal.json`, `PACKAGE_REPLAY_O.json`, `PACKAGE_REPLAY_OO.json`,
`PACKAGE_REPLAY_env2.json` receipts. Extra regular preprint files may be frozen.
The archive's outer manifest has a `files` fingerprint dictionary of all members
except itself. The inner package manifest may additionally carry file modes,
allowlists, directories, and package-specific schema. The outer map is checked
independently. Archive members must be regular files; originals must have actual
Unix `100644` modes. `BUILD_RECEIPT.json` has integer `payload_files` and
`zip_members` counting the complete **outer** combined ZIP, including paper and
extra root metadata, rather than only the inner verification package.

Preserve each older reviewed candidate under
`preprint/reviewed_candidates/candidateNN/`: its `FREEZE.json`, every
`freeze.files` payload at the same relative name, `OPERATIONS_INVENTORY.json`,
and each historical inventory source under `operations/<repository-relative
name>`. This includes the historical kit bytes. Immutable root evidence remains
in its original audit location and is never overwritten to fit a newer review.

## Whole-package review records

Each round uses `audits/pr946_6000001/reviews/full_package_NN/`, starting01,
consecutively. The root supplies each MANIFEST SHA-256 externally at acceptance.
`MANIFEST.json` has a `files` fingerprint dictionary and
`explicit_public_allowlist` containing exactly the same names, excluding itself.
The following six files must be authenticated and nonempty:

- `RESULT.json`, `FULL_AUDIT.md`, `RESEARCH_LOG.md`.
- `AUTHENTICATION_START.json`, `AUTHENTICATION_END.json`, `COLD_REPLAY.json`.

RESULT contains integer`pr=946`, string`problem_id=6000001`, original head,
`reviewer_agent_id` (nonempty and distinct across rounds), `clean_context=true`,
`full_reproducer_completed=true`, `started_utc`, `completed_utc`,
`candidate_revision`, `candidate_pins={freeze,manifest,pdf}`,
`inspected_helper_hashes` (exact six-helper map), `required_issues`,
`optional_issues`, `clean_for_preprint`,
`mathematical_remaining_gap_for_stated_theorem`,
`strongest_verified_theorem` (nonempty prose), and `prior_issue_resolution`.
Every finding has a nonempty string`id`. Each older finding, including optional
ones, must appear in the latest resolution map with `verified=true`. The latest
round must clear the exact current freeze, contain no findings, declare no
remaining mathematical gap, and be clean for preprint. At least two sequential
NEW distinct reviews are required; a later round starts strictly after the prior
round completed. Real authentication/cold timestamps lie within its interval.

START and END each contain `status=PASS`, `utc`, `original_pr_head`,
`freeze_sha256`, `package_manifest_sha256`, exact `future_helpers`, exact
`candidate_files`, and integer`payloads`/`archive_members` for the combined ZIP.
`originals` maps every one of the33 full repository original names to:
`bytes`, `sha256`, actual`git_blob`, `git_mode=100644`, `disk_mode=0644`,
`archive_mode=100644`, `disk_and_archive_match=true`. The core independently
obtains actual Git blobs/modes and disk bytes before comparing these records.

COLD contains `status=PASS`, `utc`, `cold_extraction=true`,
`typed_float_policy_verified=true`, `historical_strict_failure_preserved=true`,
`package_manifest_sha256`, `externally_pinned_verifier_sha256` equal to
`freeze.files[freeze.archive_layout.verifier].sha256`,
`normalized_fields_ignored=[]`, and four `modes` entries in this order:

| mode | observed_outer_optimization | returncode |
|---|---:|---:|
| normal |0|0|
| O |1|0|
| OO |2|0|
| env2 |2|0|

Each entry contains `receipt`, exactly matching the corresponding frozen
`PACKAGE_REPLAY_<mode>.json` object. Its minimum fields are `status=PASS`,
integer`pr=946`, string`problem_id=6000001`, `package_manifest_sha256`,
integer`original_files_unchanged=33`, integer`worker_optimization=0`. Additional
stable diagnostics are compared exactly. The actual historical v2 probe that
used `-I` and ignored environment optimization remains historical0 evidence;
these fresh canonical outer-mode probes must actually observe env2=2.

## External action safeguards

Acceptance and merge recheck immutable live claimed_solved4/5, exact head/main,
original33 actual Git/disk/modes, only the target QUEUE row, current source hashes,
presence, no readiness holds, and unchanged selected related-membership. The
acceptance check repeats immediately after review-chain authentication. Merge
refreshes after marking ready and checks actual postmerge destination, exact
two-parent merge, main ancestry and unchanged other queue bytes. Already-merged
recovery receives the same exact destination/postmerge checks.

Zenodo uses only the two frozen descriptor files with exact names/metadata.
Stable private `operations_runtime/` readonly copies retain the same descriptor
bytes and relative names across kit stage/publish/inspect. The canonical reviewed
files stay unchanged. Kit state keys this stable runtime descriptor path.
Publishing requires the exact staged integer ID and kit `--confirm-id`; inspect
adds `--check-doi`. Kit metadata verification, title, production environment,
both file fingerprints, DOI, and record identity are cross-linked. Publication
intent records fresh actual merged-main/source/related readback and ancestry.
Action intents prevent automatic repetition after uncertainty.

Tracker writes use the Google Workspace CLI only after exact staged, published,
and inspected receipts. The precise destination is the user's spreadsheet,
gid1254632077, tab`Math Puzzles`, header `Original Problem / Solution Chat URL /
DOI / Notes`. Existing DOI rows are read first; an exactly identical row can be
recovered. The accepted returned/readback range must be **quoted**
`'Math Puzzles'!A<row>:D<same-row>`, row at least2, with one row and four cells.
An unresolved prior append intent blocks a fresh append.

Native publication updates only QUEUE/state/history via explicit remote-main
trees and nonforce commits. Every new CAS parent gets fresh actual merged-main,
ancestry, current source, holds, and related-membership checks. Other queue bytes,
literal state members, and old history prefix are preserved. Explicitly rejected
main races may rebuild up to six times; uncertain push errors stop immediately.
No checkout, index, local HEAD, branch, research CLI, or other target is mutated.

Native accounting is an honest audited import: original PR-declared4/5,
`turns_used=4`, `candidate_turn=4`, `turn_limit=5`,
`original_total_attempt_count_known=false`,
`author_native_history_authenticated=false`,
`proof_search_turns_added_by_audit=0`,
`turn_count_status=original_PR_declared_four_native_event_history_unavailable`.
No four historical CLI calls are fabricated and no verified four-turn event
history is asserted. Verification/publication adds no proof-search response.

Finalization independently checks native Git objects, exact tracker readback,
published receipt links and original33. It writes the authorized final PR
title/body only if the current body is still the reviewed original (or already
the exact final body), then reads it back. It records this workflow and scans
947 upward through1000 **status-only**, stopping at the first exact
claimed_solved immutable-head row. It never reads skipped proofs/sources or
creates a next problem snapshot. Root performs the next eligible intake.

## Preparation validation

`OFFLINE_CONTROLS.json` records synthetic guard checks and actual tiny local
bootstrap/FIFO/symlink/shadow tests. It is not a cold replay of the mathematical
package, independent whole-package review, or permission to publish. The suite
uses mocks for every Git/GitHub/Zenodo/GWS/native operation. No external mutation,
real external command, native event, or extra proof turn was performed.
