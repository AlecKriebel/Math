# Root replay collector: review and execution contract

This folder is **STATIC PREPARATION ONLY**. Its preparer did not import or
execute either collector source, a closed writer helper, or any mathematical
checking program. The root must read both complete Python sources and this
contract, then execute and assess the actual receipts. AST parsing and hashing
of source bytes during preparation are not replay evidence.

Root execution from the repository uses:

```text
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr37_3009/root_replay_preparation_family/collect_root_replays.py --recurrence-closure-manifest draft_pr_publication_program_20260930/audits/pr37_3009/RECURRENCE_FAMILY_ROOT_CLOSURE.json --hamilton-complete-three-page-proof-read-by-root
```

The Hamilton flag is an explicit attestation of root's **actual** complete
reading of printed pp522–524. Preparation does not supply that attestation or
infer it from a sibling report. Without this flag the collector stops before
making output or private copies. The default output is the audit-root
`ROOT_THREE_CLOSED_FAMILY_REPLAY.json`; complete first-party output streams and
fresh JSON go in `root_three_closed_family_replay_support/`. Both destinations
must be new. Failed receipts are preserved. Use fresh audit-root names via
`--output` and `--support-directory` for a reviewed retry, preserving earlier
failures and source revisions.

For the current builder, root creates audit-root
`reproduce_root_closed_families.py` as its actual entrypoint and passes that
path through `--root-script-path`. The collector binds and preserves its
complete source, checks it before/after, reports that wrapper's exact SHA as
`root_script_sha256`, and separately reports `executed_collector_sha256`.
Every outer run provides the actual `exit_code`, `exit`, and `returncode`.

Root may pass `--root-dated-input-rebase-manifest` for an explicit newer
administrative preimage. This audit-root regular JSON file requires
`approved_by_root: true`, a nonempty `reason`, and `files` rows with exact
repository-relative `path`, `size`, `sha256`. Only inventory, root's scope
certificate, and native QUEUE/state/history/catalog/assessments are admitted;
frozen science, family members, corpus, SQL, queue source and policy remain
immutable. The old and new pins and manifest hash are recorded verbatim.
Actual structured differences must be exactly the admitted whole-file ledger
hashes/lengths or native preimage hashes. The3009 target structures still must
match. A changed Git main HEAD is separately captured before execution,
retained as the exact dated `current_main_head` difference and its ledger
stdout hash, and checked unchanged after execution. Original head/base,
blobs, modes, full diff, current3009 queue row and source science still match.

The root closure manifest must be an audit-root regular file with
`family: recurrence_orientation_family` and exactly 21 `files` rows. Every
row has the family-relative `path`, `sha256`, and `size` (or `bytes`). Rows
must match the exact original 21-member allowlist, **including its original
authored_manifest.json and dated manifest_verification.json**. The collector
accepts this root-owned closure manifest; it does not reinterpret the family's
allowlist as a self-excluding digest manifest. Its final `family_manifests`
map uses this exact external closure path/hash/count for recurrence.

`INPUT_PINS.json` binds 37 source/runtime inputs and the 48 authored members
of the three closed families: planar10, primary17, recurrence21. It separately
binds the self-excluded planar and primary manifest bytes, the recurrence
self-included manifest bytes, the complete original13 source snapshot and
14-path diff, native queue/policy/catalog/assessment/state/history inputs,
related groups, inventory, raw149,266,659-byte corpus, readonly SQL, and the
exact cached historical PR metadata. The queue module has only standard
library imports; those source/runtime dependencies are inspected, and
SymPy1.14.0 must already be available through `/usr/bin/python3`. No dependency
installation occurs. macOS dispatches that command to Xcode Python3.9.6;
its actual `sys.executable` is pinned explicitly.

Execution checks all closed members, their manifest self bytes, exact live
file sets, root closure rows and all pinned inputs before copying. It runs
only the safe planar manifest verifier and primary `--verify-manifest`
interface live. The recurrence `verify_manifest.py` writes its own receipt,
so it is never run live. Root closure and exact pinned hashes provide its
read-only closure validation here. Every writer runs inside a fresh exact
repository hierarchy under this folder's ignored `tmp/`. Raw/SQL and native
read inputs are readonly regular copies. Snapshot copies retain original
modes so the primary helper's copytree mutation cases remain writable.
The snapshot itself is not modified. A private `.git` symlink points to the
live Git repository, with an allowlisted readonly Git wrapper and optional
locks disabled. The helper's `gh api` call is served the exact pinned cached
response locally by a strict command shim; it performs no network request.

The execution order is substantive. Planar9 manifest controls and608 complete
controls run in the private family. Primary6 manifest controls run **before**
its ordinary replay overwrites any copied historical manifest member. Then
the primary helper runs14 exact original/code/prose/source/accounting cases,
full raw/SQL/native-score/Git checks and a complete read/execution ledger.
Recurrence6 independent groups and11 counter-controls run, followed by its5
original/code cases under the system runtime. Finally the root original
integrity collector runs with exactly one hardcoded repository-root path
replacement. The complete revised first-party source and exact before/after
replacement record are retained. All checking statements remain unchanged.

The primary dated manifest-controls receipt tested15 files under manifest
`d12686d6d900c7587e45706d6301ef695bce9168668b7863d8ba14e10347d4ea`.
Its final closed manifest tests17 files under
`d53bc8be2de3767f25c5c1576628027750c787b319ff4935c6d1991164acc590`.
These are different inputs. The collector preserves the complete structural
differences, explicitly checks15 versus17 positive outputs and both manifest
hashes, and requires every rejection/pass predicate to agree. The old helper
saved only the final500 traceback characters; after private-root replacement,
the fresh complete failure streams must reproduce that exact old interface.

Full structured comparisons remove only named clock fields and replace
documented absolute path prefixes/interpreter paths. They retain every other
field, check name, value and scope statement. Runtime traceback underline
differences remain visible in recurrence's complete structural diff. Both
complete bodies must agree after removing only caret/tilde formatter lines,
and the exact intended AssertionError, exit1 and source statements must match.
Dependency failures never count as intended rejection. Primary failed-stream
hash/length changes are tied to complete retained streams that compare after
the private path replacement. Neither raw difference is presented as BYTE
equality. This explicit evidence supports a scoped replay PASS; it is not a
mathematical theorem or novelty certificate.

Every fresh full31 and8462-check output must be BYTE and fullJSON identical to
its frozen output. Original31 stdout must equal the full output bytes.
Original8462 stdout must equal the exact metadata serialization excluding
`checks`; it is never equated with the complete8462-check file. Historical
metadata is replayed as historical input, not freshly retrieved current data.
Any unapproved input change, corpus change, source change or closed-member
change causes a real failure; dated root-approved changes remain visible and
are never silently normalized away.

The collector checks all48 authored members and manifest/self bytes again,
as well as every live input and its own three source/pin files, even after an
execution failure. It retains complete outer/nested stdout/stderr, full fresh
JSON, explicit diffs, failure receipts and the root path revision. It removes
private scratch trees, raw corpus/SQL copies, copied original/family sources
and foreign metadata scratch. A self-excluding `ROOT_SUPPORT_MANIFEST.json`
binds only retained first-party evidence. No PDF or raw corpus is retained.

The final builder contract is statusPASS, closed_family_count3,
authored_members_verified_before_and_after48, original_substantive_turns1,
turn_limit5, new_substantive_attempts0, exact root_script_sha256, nonempty actual
outer runs with exit0, full structured comparisons and the exact three family
manifest paths/hashes/counts. Its Hamilton boolean originates solely in root's
required input flag. Root must assess the actual first-party receipt rather
than use this preparation document as proof that any run succeeded.
