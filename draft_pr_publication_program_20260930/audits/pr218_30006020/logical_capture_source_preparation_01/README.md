# PR218 read-only logical capture preparation

This frozen source-only preparation is not an executed capture, accepted packet, candidate admission, or checkpoint. Preparation is 100%; PR218 completion remains a separate Root decision. The accepted ascending baseline remains54 completed/38 published-or-adopted,last214. Proposed55/39,last218,cursor219 is conditional on the future native checkpoint, five-file synchronization, and separate actual Root terminal.

`capture_logical_packet.py` is a single inactive entry point. Importing it does not construct Seed, Runtime, an API, or the original writer lock. It reuses the exact frozen PR218 model/primitives/core, plus only the raw-commit authentication helper from the pinned read-only custody source. It never constructs Seed/Runtime, opens the stable lock, writes the actual five, posts objects, changes refs or PR state, publishes, appends a tracker row, or authorizes219.

The Root-only future command requires a new explicit source acceptance, exact externally supplied selection pin, and fresh private output names. This preparation contains no such acceptance or actual input selection. An independent exact packet review remains necessary after any successful capture. The source gate authorizes only native GETs and new private conditional staging. It does not replace the engine's later source, logical packet, admission, candidate, CAS, sync or terminal gates.

## Finite input contract

The selection JSON has exactly these six keys:

```json
{"schema":"pr218-root-positive-public-selection-v1","PR":218,"operational_authority":false,"files":[],"total_files":0,"total_bytes":0}
```

`files` must be nonempty; each row has exactly eight keys: `path`, `origin`, `bytes`, `sha256`, `git_blob`, `observed_source_mode`, `role`, `selection_basis`. `path` is a repository-relative destination accepted by frozen `h.public_path`, or one of the exact21 carry paths. `origin` is the explicit absolute checkout-owned readonly file. `observed_source_mode` is strictly integer292 (0444), not a string or float. Byte/SHA256 and native Git blob SHA1 are verified against descriptor-read local bytes. Empty sealed text is allowed. No recursive filesystem discovery or implicit expansion of another manifest occurs. The five views are generated separately and cannot be selected as input. Every exact21 carry file is required, unchanged.

Header totals are strict integers. The final selected+five overlay is bounded by frozen engine limits:600 files,8,000,000 bytes total,4,000,000 bytes per file, UTF-8 without NUL. No `.gitignore` rule is broadened: Root must record the two ancillary omissions in a separately selected boundary file. Private evidence, raw API journals and operational namespaces remain excluded.

Pinned fixed inputs are the native-identity02, case-ready02 and prior-carry02 Root receipts in `REFERENCE_PINS.json`. They establish35 protected native bodies, two opaque protected nodes, exact current PR identity, existing publication and exact21 prior operational carry files. The capture requires their referenced current acceptance/evidence/drift bodies and the complete frozen16 engine source closure plus its manifest in the positive selection. Selection of a file is data custody, not a new approval of its contents.

The future separate capture-source acceptance has these required exact typed bindings (the implementation allows additional Root documentary fields):

```text
schema = pr218-root-logical-capture-source-acceptance-v1
evidence_scope = ACTUAL_ROOT_RECEIPT_SOURCE_ONLY
PR = 218
accepted = true
selection_reference = {path, bytes, sha256} of the exact final Root selection
capture_source_pin = {bytes, sha256} of capture_logical_packet.py
capture_source_manifest_pin = {bytes, sha256} of this SOURCE_MANIFEST.json
engine_source_manifest_pin = the frozen engine manifest pin
Root_full_source_read = true
readonly_native_GET_and_private_conditional_staging_authorized = true
externally_pinned_finite_selection_required = true
Seed_Runtime_original_lock_actual_five_or_native_POST_authorized = false
```

Root creates the source acceptance only after the final positive selection. The source acceptance itself is excluded from that selection, preventing a content-pin cycle. Its exact `selection_reference` must match the externally supplied CLI path/length/SHA256; the guard rereads both pinned files and the resulting factual capture receipt binds both complete references. This gate cannot authorize another selection or any checkpoint effect.

## Future invocation; not executed here

Use `/opt/homebrew/bin/python3.11 -E -S -B -P` without optimization. The following placeholders must be replaced by Root after review:

```text
/opt/homebrew/bin/python3.11 -E -S -B -P <absolute-owned-folder>/capture_logical_packet.py
  --selection <absolute-Root-positive-selection.json>
  --selection-bytes <exact-integer> --selection-sha256 <exact-sha256>
  --source-acceptance <absolute-Root-capture-source-acceptance.json>
  --source-acceptance-bytes <exact-integer> --source-acceptance-sha256 <exact-sha256>
  --output-name private_capture218_<unique-name>
  --stage-name private_packet218_<unique-name>
  --journal ROOT_COMPLETE218_READ_CAPTURE_<unique-name>
  --UTC <YYYY-MM-DDTHH:MM:SSZ>
  [--retired-candidate <exact-40hex-OID>] ...
```

The three one-use names have the regex bounds enforced in source. Output is a new child of this preparation folder. Stage and API journal are new private children of the frozen engine folder; existing frozen source files are never changed. This private staging location supplies engine-relative input paths without moving the original engine or modifying its globals. Any existing output/stage/journal stops; there is no resume, overwrite, rebind or automatic retry.

## Capture and conditional construction

Before effects, the source reads exact own/source/frozen-engine closures, source acceptance, fixed receipts and positive selection. The same pins are refreshed before each GET, before private capture starts, and again around staging; selected origins are independently reread. The no-follow descriptor reader is AST-identical to the accepted engine reader and enforces ordinary0444, stable ancestor and leaf identities. Existing local five are read separately from native five, including absent states. Their exact local identities/bytes are rechecked before staging.

Future API construction uses the frozen `e.API(..., mutate=False)`, explicit `--hostname github.com`, no retries, one current-invocation immutable cache only. Each fresh successful response is associated with its exact retained exit0 GET receipt, stdout, empty stderr and returned value. A deliberate immutable cache hit is accepted only with its matching current-invocation hit record and original successful raw receipt; it is not counted as a second wire response. Unknown missing provenance poisons the observer.

Limits are250 wrapper GET invocations (thus at most250 actual wire GETs),64,000,000 aggregate successful stdout bytes,32,000,000 unique decoded body bytes,300 seconds overall dispatch/acceptance deadline, and the inherited120-second bounded individual transport. A timed-out in-flight request can add its remaining transport cleanup time. There is no retry or fallback and no POST route. A single bounded envelope may temporarily exceed the aggregate remaining budget before refusal; all accepted wire data stay within the cap.

Fresh Main ref/commit/root and raw signed commit SHA1 are authenticated. Native comparisons require descent from the actual214 observation and the existing218 merge, without inferring a new CAS or completion. Targeted immediate-tree reads bind selected preimages, native five, the two opaque nodes, whole Main QUEUE and its exact unique own row; the current PR and current PR QUEUE are independently checked. The35 selected protected bodies are associated and decoded/native-SHA1/SHA256 verified. No unrelated foreign subtree is recursively expanded.

Native and local logs must be prefix-compatible. The longer exact prefix is preserved; divergence or an existing218 phase marker stops. Both native and local program JSON must retain the exact54/38 membership baseline and dated99 denominator. Generated conditional files add218 only, append the canonical phase marker last, retain skip history, and state no advance authority. The manifest records distinct native path tuples versus local byte/absence preimages. Nonview selected artifacts may only be absent or already exact; no differing existing artifact is overwritten.

Main must match at all capture brackets and the PR must match again before staging; any movement stops without rebind. A successful result is only a dated observation. Main may move after the final bracket: the result is not a lease, packet acceptance, current-at-write-time assertion or future checkpoint authority. Later engine admission must establish its own fresh native/local conditions.

Only new private0444/fsynced files/directories are written: raw GET journals, native/local five preimages, QUEUE, authenticated commit/trees, proposed source copies, `LOGICAL_MANIFEST_01.json`, and a qualified capture receipt. Failure can retain private partial outputs with `CAPTURE_STOPPED.json`; those are not a successful snapshot and must not be adopted silently. No Root gate is generated.

## Verification performed

`offline_controls.py` ran45 pure/owned synthetic controls, saved in `OFFLINE_CONTROLS.json`, against the exact source pin. They cover type/selection bounds, empty files, divergent prefixes, conditional memberships, opaque-tree validation, no foreign overwrite, actual-source manifest construction, fake retained receipt/cache-hit provenance, cap/deadline/POST/source-revocation refusals and constructor absence. The control transport is an owned fake created with `GET.__new__`; the production API constructor and `run()` were never called. The whole real capture/staging path, native origin validity on production responses, and a concrete future packet remain unexecuted and unaccepted.
