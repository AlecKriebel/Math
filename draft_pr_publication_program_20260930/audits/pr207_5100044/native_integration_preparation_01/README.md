# PR207 native integration preparation

Status: PREPARATION ONLY. Root must independently review this helper, supply actual event receipts and frozen sources, and authorize any later execution. No operational manifest or actual acceptance is supplied. This preparation executed no Git command, network request, object POST, ref update, PR operation, publication operation, tracker operation, or real local-five sync.

`native207.py` supports exactly two phases. `merge95` constructs a tree overlay on fresh MAIN, then a commit with parents `[fresh_MAIN, a7f8486548122c7d545430821afeedbccf48b3e7]`. `completion100` constructs a single-parent checkpoint on fresh MAIN after GitHub actually reports the original ready PR207 merged. No ref mutation route exists. Root alone may perform an external expected-SHA, force=false CAS after independent GET-only verification.

## Frozen inputs

All operational manifests and sources must be canonical paths beneath this folder, ordinary regular files mode 0444, with no symlink components. Pass the manifest's actual byte count and SHA256 separately; merely naming a manifest does not authorize an action. Root may create an owned `phase_merge95_sources/` directory here after review. Every selected source uses a relative path within this preparation folder. The bounded manifest has schema `pr207-native-integration-inputs-v1` and fields:

- `PR`: integer 207; `phase`: `merge95` or `completion100`.
- `anchor`: `063dd13ada2e9fc004f2fcb919f1ccefbbb895a9`; `original_head`: `a7f8486548122c7d545430821afeedbccf48b3e7`; `original_head_tree`: `d5711f92b999c72068a38726ae552e894b350c1a`.
- `expected_parent`: Root's fresh actual MAIN SHA; `helper_pin` and `core_pin`: exact `{bytes,sha256}` pins.
- `facts`: exactly the phase object in `CONTRACT.json` (integer/bool types are checked).
- `files`: explicit rows `{path,source,bytes,sha256,git_blob,preimage}`. `path` is native; `source` is owned relative; `preimage` is null for fresh MAIN absence, otherwise exactly `{mode:"100644",type:"blob",sha:<actual old blob>}`. A preimage is checked even when selected bytes are unchanged. There are no deletions, selected symlinks, selected gitlinks, or selected executable conversions.
- `total_files` and `total_bytes`: exact counts; at most 1500 files, 8MB per body, 40MB total.
- `local_views`: exactly five `{path,preimage}` rows; each local preimage is null for absence or `{bytes,sha256}`. These describe actual local old bytes separately from native preimages.
- `gate_receipt`: a selected native case path containing the actual Root gate envelope below; `commit_message`: explicit bounded message.

Native paths are restricted to the PR207 case prefix, `unsolved_math_prioritization/attempts/5100044/`, the three existing program views, and the custody-confirmed `unsolved_math_prioritization/QUEUE.md`. No root-level QUEUE alias is allowed. Native attempt paths must be exactly the twenty custody names plus `requirements.txt` and `current_execution_receipt.json`. All twenty original archive bodies must also be selected at the existing case `submitted_snapshot/` paths, with the exact custody byte/SHA256/blob identities (20 files, 61,131 bytes). No original archive file is executed.

The five selected views are the case `CURRENT_CASE_STATUS.json`, case `RESEARCH_LOG.md`, program `CURRENT_PROGRESS.json`, program `CURRENT_PROGRESS.md`, and program `RESEARCH_LOG.md`. Both JSON views must contain every phase fact. Existing percent/readiness aliases, when present, must agree. The program JSON requires 34 unique published PR IDs including 207, 49/50 unique completed PR IDs excluding/including 207, and the unchanged dated denominator 99; a fraction alias, if present, must agree. Root remains responsible for preserving all prior membership IDs. Each Markdown view must include exactly one whole line:

`<!-- PR207_NATIVE_PHASE_FACTS {compact sorted JSON facts} -->`

Use `json.dumps(facts,sort_keys=True,separators=(",",":"),allow_nan=False)` for that JSON. Do not include a second historical marker of this prefix in the same file. Root may retain ordinary historical log entries.

## Actual gate envelope

`gate_receipt` must identify a selected file with schema `pr207-root-native-phase-gates-v1`, `evidence_scope:"ACTUAL_ROOT_RECEIPT"`, integer `PR:207`, matching `phase`, `accepted:true`, exact `original_head`, exact `facts`, and all of `scientific_accepted`, `whole_package_accepted`, `actual_publication_verified`, `actual_tracker_verified`, `ready_for_merge` true.

Its `receipts` dictionary has exactly `scientific`, `whole_package_review`, `publication`, `tracker`, plus `ready_PR_merge` only for completion100. Each role is `{path,bytes,sha256}` referencing a selected event file other than the gate itself. Root must supply actual review/publication/tracker/merge event evidence, not preparation reports. The helper byte-binds those event files and trusts the externally pinned Root envelope's interpretation of heterogeneous service receipts; it does not independently interpret the Zenodo or tracker response schema. Actual original PR head, draft/state/merged status, original head tree, and native ancestry are additionally fetched from GitHub. Completion requires original HEAD to be an ancestor of its fresh parent. No self-hash of the gate is inside the gate, avoiding a pin cycle.

For merge95 a selected QUEUE body must be derived from the exact fresh MAIN body. Every foreign line and its byte order must be unchanged. The own old row must be the exact captured 123-byte queued/0/5 row SHA256 `3f0adcd50022e57df962becd3fb600e0d1e59dc6ebeb2ddb5627ea7ea299a4d1`. Only own status, effort, findings and DOI cells may change; post status/effort must literally be `claimed_solved`, `1/5`, preserving submitted historical state without making it an eligibility inference. Completion100, if selecting QUEUE, requires the whole accepted claimed_solved/1/5 QUEUE body unchanged. Fresh native blob content is fetched and hashed before this proof; historical full QUEUE bytes are never substituted for current foreign lines.

## Execution after Root review

Ordinary Python flags are mandatory: `python3 -E -S -B -P native207.py ACTION --manifest /absolute/owned/manifest.json --manifest-bytes N --manifest-sha256 SHA`.

- `dry`: offline input/fact/source/local-preimage validation only. It infers no actual acceptance.
- `plan --journal UNIQUE`: GET-only fresh MAIN, ancestry, PR, exact native preimages, expected tree/scope. No object creation.
- `candidate --journal UNIQUE`: object-only POST allowed for binary blobs, tree, commit; no ref action. Fresh MAIN is checked before each POST. It returns selected modes/bytes/SHA256/blob IDs, parents, wanted tree and complete change scope after an independent GET verification.
- `verify --journal UNIQUE --parent SHA --candidate SHA`: GET-only reconstruction and full selected body/scope authentication; parent must still be fresh MAIN.
- `verify --journal UNIQUE --parent SHA --candidate SHA --after-cas`: explicitly lease-free GET-only audit of that historical parent/candidate; current MAIN is reported, not silently treated as parent. It does not authorize ref mutation or local sync.
- `sync --journal UNIQUE --acceptance /absolute/owned/acceptance.json --acceptance-bytes N --acceptance-sha256 SHA`: requires the actual Root receipt below, actual MAIN exactly candidate, and a fresh independent full tree/body verification before touching the five views.

Every journal is a fresh exclusive directory under this folder, fsynced along with its parent. Object POSTs have exclusive fsynced intent files before dispatch and durable SHA result records on success. Any API failure/uncertainty stops that attempt. There is no retry loop. After uncertain POST, Root must inspect that same attempt/object read-only; do not automatically submit the object again. Commit endpoint identities are checked by actual API association; raw commit-object SHA reconstruction is not claimed.

Binary files, including PDF/ZIP, use base64 `git/blobs` POST and tree entries by SHA. Equal binary blob SHAs are posted once in the attempt. UTF8 bodies without NUL are inline tree content. The expected tree is calculated entirely before posting. Foreign trees that retain their SHA remain opaque; unchanged empty trees, symlinks, gitlinks and executable modes survive exactly.

## Actual acceptance and five-file sync

Acceptance schema is `pr207-root-native-integration-acceptance-v1`, with `evidence_scope:"ACTUAL_ROOT_RECEIPT"`, integer `PR:207`, matching `phase`, `accepted:true`, `full_scope_verified:true`, `all_selected_native_bodies_verified:true`, exact `manifest_pin`, `helper_pin`, `facts`, `parent`=expected parent, `original_head`, `original_head_tree`, `candidate`, `tree`, and `actual_MAIN_observed`=candidate. `Root_ref_update` must contain `{expected_sha:parent,sha:candidate,force:false,success_confirmed_by_actual_native_readback:true}`. These describe an action already performed and read back by Root; this helper cannot produce that authority from candidate/preparation results.

The existing program `ROOT_GLOBAL_FIVE_WRITER.lock` must already be a canonical 0444 regular file with the historical stable payload. The helper opens it without creation and holds `flock` while checking its inode/payload before each per-file atomic install. The lock inode is never created, deleted or replaced. Local files must match their explicit old bytes or the accepted postimage, allowing a new sync attempt to resume partial success. Each installed file and its parent directory are fsynced. All five exact postimages and a fresh current-MAIN=candidate readback are required before the actual pointer is written inside this folder. This is per-file atomicity under a cooperating-writer lock, not a five-file atomic transaction or protection against arbitrary same-UID interference. Sync must not race a later phase's global writes.

`ROOT_ACTUAL_MERGE95_POINTER.json` and `ROOT_ACTUAL_COMPLETION100_POINTER.json` are exclusive local actual pointers, created only by a successful real sync. They do not exist in this preparation. Root may instead perform its separately reviewed sync.

## Validation and publication boundary

Run `python3 -E -S -B -P test_native207.py` for 23 offline tests. Temporary sources and local views exist only below this folder and are deleted. Native immediate trees and API responses are held in memory, with a deliberately unavailable opaque foreign subtree to detect accidental recursion. Tests exercise real owned temporary stable lock/file installs; no real global view is touched. Fixture Root receipts are generated only in temporary directories and are explicitly fictional. No fixture native trees or receipt bodies are in the public allowlist.

`PREPARATION_MANIFEST.json` is the explicit public artifact allowlist. `PREPARATION_SEAL.json` pins it and this frozen helper. Root must use only that allowlist when archiving this preparation, and must separately inspect/allowlist later operational sources and real journals. The exact remaining gap is independent adversarial review plus Root's actual frozen operational manifest/events; this preparation makes no publication, merge, current-case readiness, or research-novelty claim.
