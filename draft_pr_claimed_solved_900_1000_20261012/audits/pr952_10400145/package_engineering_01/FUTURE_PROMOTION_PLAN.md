# Checked future promotion plan — service adapters remain to be implemented

The finite verifier/profile and pure observation checks are complete implementation support. This plan defines the remaining executable adapter contracts and exact acceptance schemas. It is not an acceptance receipt. Root must implement, freeze and adversarially test the actual future wrappers after constructing the paper, findings register and descriptors. No current seal authorizes any future mutation. No GitHub releases are used.

## 1. Capture and independently seal all authority

Create one whole-package freeze that closes the paper sources/PDF, exact public verification tree/ZIP, descriptor, finding dispositions, four actual cold receipts, build receipt, original33 identity evidence, all source/review anchors, all mathematical/priority seals, and the exact operations inventory. Root supplies its own complete current finding ID set; neither old50 IDs nor an old candidate01 is a requirement. Every candidate created later receives its own immutable historical freeze, files, operation source bytes and evidence snapshot; no historical lookup may fall back to mutable live data.

The externally supplied operation inventory must close every entry wrapper, core, helper and the unchanged `zenodo_deposit_tool/zenodo.py` SHA `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca`. Authenticate that inventory hash before reading its file map. Capture all dependency bytes before worker execution, validate strict scalar types/paths/size bounds and compile the captured core at optimization0 in an isolated worker. A wrapper must not declare PASS by trusting hashes from its own mutable colocated files. Externally pin wrapper bytes too. Inspect/close private evidence separately; private source bodies never enter public allowlists/ZIPs.

`SETTINGS.example.json` names fixed target/service constants and intentionally contains null seals. Null, empty arrays or absent mandatory evidence reject promotion. Fill the independently supplied hashes and actual findings/reviews only after root freezes them; do not transform absence into historical0 or synthesize author proof events.

## 2. Review-chain acceptance schema

Enumerate the actual review directory before and after acceptance and each mutation boundary. It must contain exactly every consecutively numbered `full_package_01`…`full_package_NN` supplied through external seal arguments; retain failed, incomplete, interrupted and adverse rounds. Reject missing numbers, hidden additional numbered directories, duplicate reviewer IDs, reversed/overlapping chronology, or a review beginning before its candidate freeze. No acceptance may rely solely on declared booleans.

Each reviewer seal uses `files` (complete exact byte/hash map) and `explicit_public_allowlist` (same unique set), excluding its own `MANIFEST.json`. Authenticate the external review manifest SHA before reading any sealed member. Mandatory nonempty artifacts: `RESULT.json`, `FULL_AUDIT.md`, `RESEARCH_LOG.md`, `AUTHENTICATION_START.json`, `AUTHENTICATION_END.json`, `COLD_REPLAY.json`. The exact actual START/END/cold schemas below are adapted from the current tested PR948 core. They need to be integrated and tested against the real PR952 review output, not relaxed after a failed round.

RESULT required types:

```
pr:int=952; problem_id:str="10400145"; original_pr_head:str=HEAD;
reviewer_agent_id:nonempty str; clean_context:bool;
full_reproducer_completed:bool; entire_package_review:bool;
started_utc:UTC str; completed_utc:UTC str; candidate_revision:positive int;
candidate_pins:{freeze:sha256, manifest:sha256, pdf:sha256};
inspected_helper_hashes:exact complete operation helper map for completed reviews;
required_issues:list; optional_issues:list; clean_for_preprint:bool;
strongest_verified_theorem:nonempty str;
mathematical_remaining_gap_for_stated_theorem:explicit null-or-str;
prior_issue_resolution:dict; inherited_finding_dispositions:dict.
```

Every issue has a stable nonempty ID; required and optional IDs both accumulate. Each clean reviewer independently verifies all inherited IDs and every earlier required/optional finding via `{verified:true,evidence:nonempty-str}` and actual cited artifacts. Missing/waived/declined conditions are explicit dispositions root must assess; the algorithm cannot erase them. Clean means complete, no current issues, explicit null mathematical gap, valid whole START/END/cold evidence and current exact freeze. Any adverse/incomplete/failed/old-freeze round resets the clean streak. Final acceptance requires the two **latest, distinct, sequential, complete ENTIRE current-freeze reviews** clean, with no later unfinished directory.

Honest failed/incomplete RESULT includes `nonclean_history:{status:"failed"|"incomplete",explanation:nonempty-str,checks_not_passed:unique-nonempty-str-list}` and `clean_for_preprint:false`. Preserve actual subsets/observations rather than fabricating a successful completed result.

START and END required types:

```
status: "PASS"|"FAIL"|"INCOMPLETE"|"NOT_RUN"; utc:UTC str;
original_pr_head:HEAD; freeze_sha256:review freeze;
package_manifest_sha256:review manifest;
future_helpers:dict; candidate_files:dict; originals:dict.
```

PASS requires exact whole helper/file/original33 maps, including Git blob/mode, disk0644, matching disk/archive bytes. Non-PASS may contain only correctly bound observed subsets, with `explanation:str` and `observations:dict`; NOT_RUN has empty subsets. START/END times lie within RESULT start/end and bracket cold evidence. Do not invent authenticating observations to fill a missing record.

COLD required types:

```
status: "PASS"|"FAIL"|"INCOMPLETE"|"NOT_RUN"; utc:UTC str;
cold_extraction:bool; package_manifest_sha256:review manifest;
externally_pinned_verifier_sha256:exact review verifier;
normalized_fields_ignored:list; modes:list.
```

PASS requires cold extraction/snapshot from the exact ZIP, no ignored fields, and modes in exact order normal/O/OO/env2. Each has `mode:str`, `observed_outer_optimization:int` of0/1/2/0, `returncode:int=0`, and `receipt:dict` equal to the corresponding authentic fixed candidate cold receipt under its actual schema. Non-PASS retains actual typed null-or-observed fields plus explanation/observations, and never receives clean credit. NOT_RUN declares `cold_extraction:false,modes:[]`. Root must avoid requiring equality of unrelated clocks/host metadata by construction: use deterministic verifier receipts plus a separate actual observation envelope, as this driver does; never normalize after the fact.

## 3. Source/native/PR boundaries and merge

Before acceptance, ready, merge, each Zenodo call, append, native push and final metadata mutation, revalidate current operations, whole freeze, all reviews, exact original33, immutable submitted claimed_solved QUEUE row1/5, raw cache reconstruction, statement SHA87dd83734fc8c51eb132f501c5d05947ed7057268dfba61627fb78f53da10af8 and review SHA12e089388884a531bdc98f888e203ec0be06aa637e3ce342ac1e502a7af266f5, catalogue holds, related groups and target native absence. Private source record is checked privately against its separately sealed root hash. Capture every before/after observation and all differences on failure.

`observation_checks.py` implements the pure authority/observation split tested by `test_observations.py`. Use exact PR number/head/main/state/URL plus actual mergeCommit identity as authority. Retain computed `mergeable`, `mergeStateStatus`, associated `baseRefOid` and actual live base pointer as observations. Immediately before merge require fresh `MERGEABLE`; never weaken source/path eligibility. Complete changed-path pagination must bind the actual live `baseRef.target.oid`, every page count/cursor and canonical unique filename, and stable metadata across the bracket. For PR952 the complete changed set is exact original33 plus QUEUE; authenticate the unchanged other QUEUE bytes against the actual merge base. Draft readiness has its own exclusive intent and exact PR readback before merge intent.

After merging, verify an exact ordinary two-parent merge with second parentHEAD, the exact original33, unchanged unrelated QUEUE bytes, exact claimed row, and merge ancestor of **fresh actual main** before and after source/native gates. An unrelated advance of main does not alter the merged PR identity; computed status changes are retained without whole-dictionary identity rejection. A change of main inside a source/native/path eligibility bracket still requires a fresh bracket and checks; do not silently reuse an old source gate. Save the two-parent commit and every bracket.

Each mutation has an exclusive, flushed durable intent BEFORE the call, with frozen argument/target/ID/hash and no blind retry. Unknown response means GET the exact saved ID/commit/row/body and reconcile its observed outcome. Do not overwrite intent/failure files, create replacement deposits or blindly retry. Distinguish definitive precondition/CAS failure from unknown outcome. Preserve the full failure and observations; a new attempt is permitted only for a proven no-mutation outcome and newly revalidated authority.

## 4. Unchanged Zenodo kit and public verification

Capture the exact unchanged kit bytes through the external operations inventory and use that captured kit for **every** service call. Root must supply two exact names only: `habiro-rank-interpolation-v1.0.pdf` and `habiro-rank-interpolation-verification-v1.0.zip`, whose bytes match the approved freeze. Descriptor metadata matches final title/version/date/creator/license and explicit AI/unrefereed/human/formal/priority disclosures. Plain notes compare exactly; no generalized HTML or metadata normalization.

Use a stable private runtime descriptor path and the kit's saved same-ID state. Every wrapped client method repeats the entire source/acceptance/review/merge guard immediately before the call. Permit at most one create POST and one publish POST, with intent counters advanced before calling. Persist the returned ID immediately. Before publish, GET exact same ID, use kit validation for exact metadata and two files, confirm unchanged descriptor/file bytes, and require actual savedID. Lost create response with no ID requires explicit account reconciliation; never create a replacement. Lost publish response uses GET savedID only. Stage/inspect/publish receipts must have same ID, freeze, operations and merged commit. No arbitrary additional user-specified record is accepted.

After publish, independently request unauthenticated public record JSON, both exact public files and DOI URL. Verify same recordID, DOI, title and exact file set/size/SHA256, and DOI resolves to that record. Do not send the API token through public requests. Save observations and require readback both before native/tracker work and before final metadata.

## 5. Tracker, native CAS and final metadata

Use GWS CLI for spreadsheet1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20; verify gid1254632077 maps to `Math Puzzles` and four exact headers `Original Problem`, `Solution Chat URL`, `DOI`, `Notes`. The row is exactly four scalar strings, RAW input. Scan for duplicate target, PR anchor, title and DOI. One identical existing row is read back; any conflicting/multiple match stops. Keep all other rows private. Append at most one row through an exclusive intent. Check exact returned A:D single-row range, updatedRows1, updatedCells4, exact row GET, then repeat duplicate scan. A lost response is reconciled through exact row GET/duplicate scan without re-append.

For native publication use immutable blobs at fresh remote main, no local checkout/index/ref/config changes. Require target state and per-turn history absent immediately before computing changes; this means current absence only, historical countUNKNOWN. Import immutable PR declaration1/5 as turns_used1 with explicit unauthenticated imported basis; add0 audit proof turns and no candidate_turn. Edit only selected QUEUE cells, insert only selected state member while proving unrelated literal bytes survive, append one publication event preserving all old history bytes as a prefix. Construct explicit trees/commit with exactly QUEUE/state/history, save intent with exact parent/new commit, guard again, then narrow force-with-lease/CAS to main. On uncertainty test exact commit ancestor of fresh main; no blind repush. Definitive stale lease may generate a separately recorded fresh-parent attempt after source/native revalidation. Verify actual commit parents/paths/content, target event, unrelated bytes and merge ancestry afterward.

Only after public, tracker and native readbacks pass, write final local state and PR title/body containing actual DOI, merge commit, freeze and review seals. Bind metadata intent to the exact original reviewed body and intended new body; revalidate immediately before mutation, read back exact title/body and merged identity. Then status-gate later PRs in ascending order using only live metadata, complete canonical changed filenames at actual `baseRef.target` across all pages, and QUEUE fetched at the immutable candidate head. Never read excluded mathematical bodies or use associated baseRefOid as current branch pointer. A missing/ambiguous target rejects rather than guesses. Independent reviewers must attack these adapters before any real operation.

## Remaining gaps

Root must still implement the mutation adapters and whole freeze/review-chain validators, freeze candidate data, run supported target-level preflight with preserved raw observations, obtain two clean full-package reviews, and perform every actual mutation/readback. This assignment neither claims nor authorizes acceptance, ready, merge, service access, native append, metadata change, or publication readiness.
