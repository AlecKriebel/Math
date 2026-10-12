# Authoritative v2 PR73 preparation

Use only the `_v2.py` operators and `_V2.json` schemas/templates. Unsuffixed
v1 preparation is preserved as dated incomplete work and is superseded. No
operational phase is authorized or executed by this preparation. ROOT must
separately review final v2 bytes and provide a fresh scientific gate, versioned
frozen packet/plan, and actual shared-writer windows.

The target is PR73, record 2985, immutable submitted head
`6f82e81631fd43abc0140a831acfb43c150f4210`. No scope interpretation is supplied
by the operators. Gate, plan, and acceptance fields must contain the same
explicit, nonempty `scope_interpretation` object, with an ID, text, and excluded
scopes. `historical_classification_certified` means exactly the bounded
classification ROOT certifies; it never implies prior resolution of a stronger
target. Its meaning field is fixed to
`precise_bounded_classification_without_inferred_prior_target_resolution`.

The templates are intentionally invalid, leave disposition unset, and are
rejected by filename and stage. Create fresh versioned gate/plan files within
the PR73 audit. Runtime additionally validates every whole-byte pin and all
cross-file identities; passing a JSON schema alone does not confer clearance.

The plan binds one versioned four-file packet: `CURRENT_RESULT.md`,
`CURRENT_PRIORITY.md`, `PR_BODY.md`, and `DISPOSITION_PROPOSAL.json`. ROOT
separately supplies exact `acceptance_scientific_fields` in the frozen plan.
The operator copies accepted report bytes unchanged and never derives status
or scope from prose. Proposal status/accepted-as must agree with the explicit
fields. The exact current-main base, current target-row digest, complete target
replacement row as base64, original PR metadata digest, final PR title, commit
messages, and a fresh `execution_id` UUID are also required.

Three mutually exclusive paths are supported:

- `claimed_solved` requires pinned successful publication, tracker, and
  whole-package gates, matching exact scope, accepted-as, DOI, packet pins, and
  canonical scientific-fields digest. Each receipt has `status=PASS`, PR73,
  exact `reviewed_head`, `ROOT_verified=true`, and the corresponding `gate_kind`.
  The DOI must match the scientific fields and target QUEUE row. These operators
  create no paper and perform no editor/upload/tracker actions.
- `already_solved` requires its own ROOT-certified precise credited-prior
  disposition, matching scope and accepted-as. Novelty clearance, new paper,
  publication DOI, and tracker append are absent/false as specified by the
  schema. No stronger prior-resolution interpretation is inferred.
- `partial` requires a separate pinned receipt with `status=PASS`, PR73,
  exact `reviewed_head`, `ROOT_certified_attributed_partial_disposition=true`,
  the exact scope and accepted-as, `novelty_clearance=false`,
  `no_prior_target_resolution_inferred=true`, `new_paper=false`,
  `publication_DOI=null`, `tracker_append=false`, and the exact `frozen_packet`
  pins. The gate sets each partial no-paper/no-novelty flag true. Scientific
  fields reference that receipt in `attributed_partial_disposition`; the
  credited-prior receipt field is null. A partial import remains `partial`.

ROOT must separately pin current readiness evidence with `status=PASS`, PR73,
exact `reviewed_head`, `mathematics_validated=true`, the selected
`native_current_status`, `original_readiness_preserved=true`, `original_budget`
equal to `1/5`, integer `new_original_proof_turns=0`, exact current catalog
`review_hash`, exact scope, and the selected novelty-clearance boolean. This
is current review evidence and never rewrites original `readiness.json`.
The present-day state/event binds it and records `readiness_review_hash` without
inventing historical lifecycle transitions or another proof turn.

The gate must bind all three v2 Python operators, both v2 schemas, original
authentication/report/manifest/sourcepair authority, original candidate,
source wrapper, readiness and ledger, and current native manifest/catalog/
queue code/policy plus both full raw files and full SQLite body. Runtime
checks current raw/SQL whole bodies against completed original authentication,
not merely a self-consistent replacement manifest. Full source pins are checked
before mutations and during readback. Native `exact_separate_prior_report`
remains present JSON null; raw lookup remains absent; SQL report remains `{}`.
Only the catalog fingerprint uses SQL normalization.

Run actual phases from `/Users/alec/Documents/Math`, using absolute or
repository-relative operator paths, with `python3 -E -B` and without optimization.
The operator verifies actual controller cwd before any action. During preparation, only
read-only structural phases are allowed:

```sh
python3 -E -B ROOT_native_integration_v2.py structural-preflight
python3 -E -B structural_checks_v2.py
```

After final ROOT review, actual phases are strictly sequential:

1. Integration `pr-metadata`.
2. Integration `merge`, using the actual metadata receipt.
3. Readback `merge-readback`, using the actual merge receipt.
4. Integration `accept`, using the actual merge-readback receipt.
5. Readback `acceptance-readback`, using the actual acceptance receipt.
6. Integration `checkpoint`, using the actual acceptance-readback receipt.
7. Readback `checkpoint-readback`, using the actual checkpoint receipt.

Each integration command requires `--gate GATE --execute-root-reviewed`;
after the first it also requires `--predecessor ACTUAL_RECEIPT`. Each readback
requires `--gate GATE --predecessor ACTUAL_RECEIPT`. Every actual command also
requires `--writer-ack-nonce UUID` matching its actual fresh acknowledgment.
Use actual `operations/<phase>_<timestamp>/RECEIPT.json` outputs. The next phase
authenticates the preceding controller, pinned source snapshots, complete
child-command metadata, full stdout/stderr hashes, and acknowledgment linkage.

The actual shared-writer status must have `paused_for` exactly
`PR73 native integration v2 20261004:<phase>`, current equal local/remote main,
empty shared index, frozen tracked dirty bodies/modes, and UTC after the ROOT
minimum-ack time and predecessor receipt, and not in the future. It must carry
the matching `ack_nonce`, frozen `execution_id`, `ROOT_gate_sha256`, and
`frozen_plan_sha256`. Operators read this evidence; they never manufacture or
reuse PR66/PR73 checkpoint acknowledgments. Canonical origin fetch and push
URLs must identify `AlecKriebel/Math` before mutations and throughout stability
checks. No force, reset, stash, branch switch, or externally addressed message
is used.

Merge only the submitted head, with exactly two parents `[frozen_base, head]`.
Incoming scope is exactly 19 original attempt files plus QUEUE. Only QUEUE may
conflict, and only its reviewed target row changes; every other current row
and byte is preserved. Dirty QUEUE causes a stop. Foreign tracked dirty bodies,
modes, deletion states, and index entries are captured and checked before any
restoration. Unexpected foreign drift stops instead of being overwritten.

Native acceptance is a separate exact five-path commit: `CURRENT_RESULT.md`,
`CURRENT_PRIORITY.md`, `acceptance.json`, current global state, and current
global history. The fresh current globals must be committed and are checked
again, including modes, immediately before insertion. Their complete expected
post-write bytes are checked, and complete native acceptance is verified before
push. State adds one member while retaining every prior byte; history appends
one present-day event. Its deterministic ID binds exact head, merge, outcome,
gate digest, and plan digest. An immediately repeated completed acceptance
verifies the whole acceptance and appends no second event; conflicting or later
incompatible state stops. Original globals being `{}`/empty is a historical
fact and never the replacement baseline for current globals.

Every original attempt byte, filesystem mode, Git blob/mode, readiness field,
budget, and ledger event is preserved: exactly 19 files, absent `status.json`,
`candidate_independently_reviewed`, 1/5, exactly one turn1 event. No readiness
or ledger rewrite, status-file invention, historical event reconstruction, or
new central proof search occurs.

The final audit checkpoint requires ROOT's exact public-safe allowlist, whole
file pins, and explicit Git modes. Both staged and committed bodies/blobs/modes
must match. Raw datasets, private retained originals, PDFs, pixels, SQLite,
command streams, foreign snapshots, and operational directories are excluded.
ROOT's content certification is required: path filters alone cannot detect
copyright or private content renamed to an allowed suffix. Referenced manifests
inventory local evidence and do not claim all private members were uploaded.

Any discrepancy stops, preserves partial state and actual streams, and confers
no completion. There is no automatic rollback. No existing PR50 editor,
publication, or tracker operation is part of this preparation. Initial tool
inspection launcher metadata is unobservable as disclosed in the evidence;
file-backed dry preflight/checks retain actual cwd/PID/argv/UTC/exit/fullstreams
and source prelaunch pins. No unavailable launcher values are invented.

The exact control file
`draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json` is
phase-specific coordination evidence. Its legitimate fresh body is permitted
to differ between consecutive phases. The predecessor receipt pins and
authenticates the complete prior ACK against its retained whole-body inventory
and dirty-body snapshot; the fresh WriterWindow independently pins and checks
the actual new ACK. Prior/fresh comparisons retain its existence, regular type,
filesystem mode, logical index entry, and ordinary index flags. Only this exact
file's between-phase body equality is excepted; every other foreign body/mode
remains fully compared. Within a phase, its complete body/mode/index/flags remain
frozen and checked. Operators never stage, restore, overwrite, or change the
ACK. It must not be included as a frozen scientific or packet input. Its prior
timestamp and baseline are checked against actual predecessor command evidence.
