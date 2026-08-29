# Static audit of the portable runner and Git-bound release suite

Audit time: 2026-08-29T16:32:13Z
Delivered package: `/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`
Declared proof/source commit: `738b662aa9c4e6201277f60b249afd4de9bcd9d6`

## Scope and method

This is a static, adversarial review. I did **not** execute `RUN_REVIEW.sh`, any
delivered Python module, any verifier, or any release/mutation command. I read
the entry points and their imported release helpers, parsed the command lists
with an independent AST reader, independently hashed the delivered files, and
queried Git objects read-only.

Package reports, `PASS` fields, prompts, and stored hashes were treated as
claims. The independent byte census below did not import or invoke package
code.

## Verdict

| Target | Static verdict | Reason |
|---|---|---|
| Direct execution on the ordinary host | **NO-GO** | The package deliberately does not enforce network, credential, host-read, or process-tree isolation. Setting an environment variable is only an attestation. |
| Portable `plan`, `verify`, `regenerate`, or `all` in a genuinely external, offline, credential-free disposable boundary | **CONDITIONAL GO** | The command plan is exact and fail-closed, the copied-workspace runner is materially hardened, and delivered bytes are internally consistent. The external boundary, dependency environment, supervisor, and evidence capture must first satisfy the gates below. |
| Execution with the currently staged `logs/offline_credential_free.sb` and `tools/isolated_supervisor.py` | **NO-GO as presently written** | The profile permits broad host reads and all Mach lookups; the supervisor lacks a hard wall timeout, complete signal handling, externally captured evidence, and an inode-bound lock. Exact fixes are listed below. |
| Excluded 32-case Git-bound release-engineering mutation command in a self-contained exact checkout | **CONDITIONAL GO; reproducible** | The declared commit exists locally; the necessary one-commit object closure is known; all 14 directly relevant delivered scripts/policies match that commit byte-for-byte. It must not run in the live source repository or a shared/alternates-based clone. |

This is an execution-safety and reproducibility verdict, not a theorem verdict.

## Exact command census

The static AST reconstruction agrees exactly, in order, with
`referee_tools/ACTIVE_VERIFIER_PLAN.json`.

| Plan | Top-level command count | Composition |
|---|---:|---|
| Native `quick_commands` | 2 | release inputs; integrated artifact binding |
| Native `full_commands` | 4 | release inputs; integrated fresh replay; classification mutations; release-engineering mutations |
| Native `regeneration_commands` | 56 | 52 explicit producer/verifier commands plus the 4 native full commands |
| Portable `verify` | 4 | the four rows at `ACTIVE_VERIFIER_PLAN.json:3-45` |
| Portable `regenerate` | 55 | native 56 minus exactly `release_engineering_mutations` |
| Portable `all` | 59 | 4 verification commands, then 55 regeneration commands, in two separately copied workspaces |
| Excluded release command | 1 | `test_release_engineering_mutations.py --no-write-report`: 32 hostile mutations and 11 positive controls |

The native construction is visible at
`proof_package/reproducibility/run_release_suite.py:78-116` and
`:116-289`. The active plan declares 56, excludes one named command, and
requires 55 names at `referee_tools/ACTIVE_VERIFIER_PLAN.json:46-112`. The
portable runner reconstructs the native objects and refuses any count or order
drift at `referee_tools/run_active_verifiers.py:368-410`.

Two counting qualifications matter:

1. `all` means 59 top-level subprocess invocations, not 59 distinct logical
   checks. The verification and regeneration phases repeat the integrated
   fresh replay and classification mutation command; the release-input check is
   also repeated under slightly different top-level names. They run in separate
   workspace copies.
2. Each integrated fresh replay is one top-level command but binds 20 nested
   child replays. The runner checks the exact child count and statuses at
   `referee_tools/run_active_verifiers.py:484-511`. Those 20 children must not
   be added to a claimed *top-level* command count.

`plan` launches no verifier subprocess, but it is not a static-only operation:
it executes the delivered runner and imports/executes the top level of
`run_release_suite.py` (`run_active_verifiers.py:368-387,755-770`). It must be
run inside the same external boundary as every other package mode.

The release-engineering driver contains 32 literal `rejected(...)` cases at
`proof_package/reproducibility/test_release_engineering_mutations.py:917-985`.
Its controls are three deterministic archive/extraction controls at `:596-633`
plus eight appended controls at `:986-994`, for exactly 11. Its regeneration
control independently requires 56 unique native commands and checks the new
directed-inclusion command ordering at `:766-848`.

## Independent package byte census

An independent reader reproduced these facts without running the supplied
integrity checker:

- outer payload: 624 files, 160,624,411 bytes;
- missing/extra/different payload rows: 0/0/0;
- forbidden symlink or nonregular payload objects: 0;
- checksum ledger: 625 rows (624 payload files plus
  `PACKAGE_MANIFEST.json`), with the exact expected path set and zero hash
  mismatches;
- inner archive manifest: 595 declared members, zero byte/size/mode/hash
  mismatches;
- inner composition: 592 commit-selected files plus the three intentionally
  generated archive members (`REPRODUCIBILITY_README.txt` and two source ZIPs).

The supplied checker is appropriately fail-closed for its stated scope:

- canonical relative paths are required (`verify_package_integrity.py:43-52`);
- payload symlinks and nonregular objects are rejected (`:63-86`);
- the outer manifest has a strict field set, unique paths, byte counts, modes,
  and hashes (`:89-141`);
- the checksum ledger has an exact path set and binds the outer manifest
  (`:143-156`);
- declared inner members are checked for commit identity, bytes, sizes, modes,
  and hashes (`:165-203`).

Its limitations are real and accurately disclosed in the code and package
instructions:

- `.venv/` and `review_runs/`, including all descendants and their modes or
  symlink targets, are excluded (`verify_package_integrity.py:4-8,55-74`);
- the compressed canonical archive is absent and its claimed hash is only
  syntax-checked, not recomputed (`:107-113,217-222`);
- the inner check covers declared members; the outer manifest is what rejects
  undeclared delivered files;
- directory modes are not sealed; regular-file modes are;
- `PACKAGE_MANIFEST.json` plus `SHA256SUMS` is a self-consistency seal, not an
  external authenticity root. An attacker able to replace both can reseal
  altered payload bytes. A separately trusted archive hash, Git commit, or
  referee-captured hash is still needed.

The outer identity fields claim the same commit for package builder and proof
source (`PACKAGE_MANIFEST.json:3753`), and the proof manifest repeats it at
`proof_package/ARCHIVE_MANIFEST.json:3592`. The independently observed file
hashes of the portable entry points are:

| File | SHA-256 |
|---|---|
| `RUN_REVIEW.sh` | `60c4b7ec846d1aa9d27638cc483fb446d5736dd3e4feadb04e60408e0c256f35` |
| `referee_tools/verify_package_integrity.py` | `d01bc9e51328e75e3cfcb34533db2a85a7f70ddf79f441a68834fbfd2736d895` |
| `referee_tools/run_active_verifiers.py` | `728e432657f4d7f98ab18811fd91d3d310d7e1cdf8aee9d1b834a62de354dabb` |
| `referee_tools/ACTIVE_VERIFIER_PLAN.json` | `156f89c7bcb785e5559788459414ad3001f010dfb928ca8977075467d4fc22c7` |

## Portable-runner strengths

The revised runner has substantial reproducibility controls:

- `RUN_REVIEW.sh` refuses to proceed without an explicit sandbox
  acknowledgement and invokes both integrity and runner processes through
  `env -i` (`RUN_REVIEW.sh:10-15,31-37,46-54`).
- Children receive a fixed ten-variable environment and workspace-local
  `HOME`/`TMPDIR` (`run_active_verifiers.py:146-166`). The runner clears its own
  inherited environment before importing the release plan (`:742-754`).
- Every top-level command starts a new process group. Timeouts, handled
  interruptions, and unexpected surviving descendants lead to termination,
  kill, reap, and failure (`:240-304,307-356`).
- Each phase copies the proof tree, symlinks only the reviewed venv, and records
  full before/after inventories of workspace and actual venv bytes, modes,
  types, and symlink targets (`:514-537,579-611`).
- Workspace drift outside `release/work/**` and any venv drift fail the phase;
  all permitted runtime drift remains in the report (`:593-637`).
- The runner binds the detailed 20-child integrated report and its logical
  payload (`:466-511`), retains location-dependent primary reports, checks
  semantic normalization, and restores canonical bytes (`:425-463`).
- The no-replace package lock is inode-bound on release
  (`:665-707`). Preflight and postflight integrity are required
  (`:650-662,742-759,783-804`).

These controls support a careful replay once an actual outer security boundary
exists.

## Remaining execution risks and required controls

### R1. The sandbox variable is an attestation, not enforcement

`RUN_REVIEW.sh:10-15` and `run_active_verifiers.py:727-737` only compare a
caller-provided string with `YES`. The report correctly says
`external_sandbox_enforced_by_runner: false` (`:621-627,784-790`). A caller can
self-set the variable on an unrestricted host. **Required:** launch only under
a separately verified OS/VM/container policy with network denial, no
credentials, constrained reads/writes, and full process-tree containment.

### R2. The currently staged macOS policy is broader than its description

The referee-owned profile first permits every file read
(`logs/offline_credential_free.sb:16`) and then denies most paths below
`/Users/alec` (`:18-42`). Consequently, paths outside that subtree—such as
mounted volumes, `/Users/Shared`, and non-user temporary locations—remain
readable. The entire audit folder is readable to package children, including
referee findings and future evidence. It also allows every Mach service lookup
(`:13`), which is too broad for a strong credential-isolation claim.

**Required:** preferably use a disposable VM/container with no network and no
host mounts beyond read-only package/venv inputs and an output handoff. If
Seatbelt is retained, replace global host reads with explicit system-runtime,
package-copy, and venv whitelists; deny the source repository, the rest of the
audit, credentials, cloud/browser stores, shared/mounted locations, and
non-session temporary roots; and restrict Mach services to a tested minimum.
Before launch, run harmless positive import/subprocess probes and negative
canary probes for network, source-repository reads, audit-result reads, mounted
or shared paths, and writes outside the session output.

### R3. Children can modify the runner's own evidence area

The staged profile permits writes to all of `package_copy/review_runs`
(`offline_credential_free.sb:44-46`). That is necessary for the current runner,
but copied verifier code runs below the same sandbox identity and can reach its
parent directories. It can therefore alter transcripts, inventories, or
reports before the trusted host seals them. In addition, the transcript is
opened read/write and passed directly as child stdout
(`run_active_verifiers.py:541-566,318-320`), so a hostile child can seek or
truncate the inherited descriptor.

Endpoint inventories also cannot detect a transient modification restored
before the final inventory. Regeneration intentionally writes many copied
artifacts, and all final differences below `release/work/**` are allowed and
only reported (`:593-605`).

**Required:** treat in-sandbox reports as evidence, not as tamperproof audit
logs. A trusted outer supervisor must capture console output to an exclusive
file outside all child-readable paths, independently inventory the immutable
package copy and actual venv before and after, and seal the completed session
immediately after process-tree exit. For a malicious-code threat model, use a
split-privilege harness or VM snapshot/overlay in which children cannot write
the referee-owned transcript or ledger.

### R4. The staged outer supervisor is not yet sufficient

`tools/isolated_supervisor.py:103-114` inherits stdout/stderr rather than
capturing them to an exclusive external evidence file and waits without a hard
wall timeout. It handles only `KeyboardInterrupt` (`:115-118`), not
SIGTERM/SIGHUP, and its lock cleanup unlinks by path without checking the inode
it created (`:93-101,119-123`). A supervisor termination can therefore leave a
live sandboxed descendant or delete a replaced lock.

**Required:** use an atomic `O_EXCL` lock whose `(device,inode)` is checked
before cleanup; handle INT/TERM/HUP; place the child in a VM/cgroup/job or
equivalent whole-tree containment; on timeout/interruption repeatedly enumerate,
terminate, kill, and reap the complete tree; impose phase-level wall limits;
and capture stdout/stderr and a supervisor summary outside the sandbox. Do not
remove the currently present outer lock until a read-only process check proves
that it is stale.

### R5. Process groups are not complete hostile-process containment

The portable runner correctly detects descendants remaining in the original
process group. A descendant that deliberately calls `setsid()` can escape that
group. The package documentation itself acknowledges this at
`START_HERE.md:58-70`. The native release wrapper has weaker cleanup: it kills
the group only on a command timeout, with no `BaseException` cleanup or
post-success survivor check
(`proof_package/reproducibility/run_release_suite.py:321-367`).

**Required:** an outer VM/container/cgroup/job boundary must own the whole
process tree. Never use process-group cleanup alone as the security boundary.

### R6. Runtime dependencies are outside the seal

The four Python package versions are pinned but wheel hashes are not
(`proof_package/reproducibility/requirements.txt:1-4` and
`START_HERE.md:33-56`). `.venv` is explicitly excluded from package integrity.
The runner records interpreter and imported top-level module hashes
(`run_active_verifiers.py:189-237`) but that does not establish wheel provenance
or hash every imported dependency file.

**Required:** construct the venv offline from a referee-reviewed wheel cache;
record wheel hashes, Python executable hash, complete installed distribution
metadata, and an external before/after venv inventory; mount it read-only during
execution. Explicitly set `K3P_REFEREE_TRUSTED_PYTHON` to a separately hashed
standard-library interpreter rather than accepting a caller-controlled value
(`RUN_REVIEW.sh:23-29`).

### R7. Native release code inherits its caller environment and Git policy

The native release environment starts with `dict(os.environ)`
(`run_release_suite.py:292-310`). Its Git helper invokes the first `git` on
`PATH` and inherits system/global configuration
(`reproducibility/release_common.py:142-149`). Global templates, hooks, filters,
fsmonitor settings, prompts, or lazy-fetch configuration can therefore affect
the Git-bound tests.

**Required:** launch the excluded release command with `env -i`, an absolute
reviewed Python, system-only `PATH`, controlled empty `HOME`/`TMPDIR`, and at
least:

```text
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_GLOBAL=/dev/null
GIT_OPTIONAL_LOCKS=0
GIT_NO_LAZY_FETCH=1
GIT_TERMINAL_PROMPT=0
GIT_ASKPASS=/usr/bin/false
SSH_ASKPASS=/usr/bin/false
GIT_CEILING_DIRECTORIES=<trusted-execution-parent>
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
PYTHONNOUSERSITE=1
LC_ALL=C
LANG=C
TZ=UTC
SOURCE_DATE_EPOCH=1788019048
```

### R8. Restart and exact-once claims need external session binding

The internal package lock prevents concurrent runner starts and is safely
inode-bound. SIGKILL or power loss can leave it stale
(`run_active_verifiers.py:665-707`; `START_HERE.md:72-75`). The native excluded
mutation report has no `source_commit` or total elapsed-time field
(`test_release_engineering_mutations.py:995-1027`).

**Required:** before every launch, record the absence of the relevant process
tree and locks; assign a referee session ID; capture start/end monotonic and UTC
times; bind command, commit, interpreter, environment, stdout, and all output
hashes in an external no-replace ledger. Monitor the same PID/session; do not
poll by relaunching. Credit an interrupted run as interrupted, never as a pass.

## Git-bound release suite: exact-checkout feasibility

At the audit instant, the source monorepo's current `HEAD` was exactly
`738b662aa9c4e6201277f60b249afd4de9bcd9d6`, the scoped project status was
empty, and the declared commit object existed. This is a read-only observation,
not permission to run in the live source tree; it must be rechecked during
trusted staging.

The minimum self-contained one-commit sparse repository has this independently
derived closure:

| Object/entry class | Count |
|---|---:|
| target project tracked rows | 623 |
| target project unique blobs | 618 |
| tree objects needed to traverse the commit | 2,959 |
| commit objects | 1 |
| total required Git objects | 3,578 |
| uncompressed Git object payload | 150,107,844 bytes |
| target modes | 601 mode-`100644`; 22 mode-`100755` |

The commit's root tree is
`03109872c54a2e944eab21c658e6981261bead01`, and the project subtree is
`3bc783818f09eb796477c32ea7f40b7c1bbc1600`. A source-independent checkout is
therefore feasible without an alternate or promisor remote. Current free space
was about 1.9 GiB; staging must recheck space and retain ample reserve for the
checkout, pack, temporary fixtures, and evidence.

All 14 directly imported or hash-bound release inputs in the delivered package
matched their blobs at the declared commit byte-for-byte:

| Relative file | SHA-256 |
|---|---|
| `reproducibility/test_release_engineering_mutations.py` | `1910bfb73e32c25d0d1680bf850675033aa89b512d03567de9fae88d27de2fba` |
| `reproducibility/run_release_suite.py` | `39864d2e07531f92d0296b95063feae372bc6ee52985d701c25f15d0eef2c3d6` |
| `reproducibility/release_common.py` | `497340362bb93c46b6c9c00b2a6a85b52428a4f2c0f9ebf900f3df57360bf278` |
| `reproducibility/verify_release_inputs.py` | `8b8eb48e6ca7ac64f1e67bf5f3b717ffbc3f43af2551a5a89d090c39911054a7` |
| `release/archive_tools.py` | `3057074269c67450ea24edd896a8028769e49c1fcb629bc90f48a655e2e7cb24` |
| `release/build_release.py` | `0ab46c8bf325ba43fa83a0ada940fadcebfc35ef9341a07e9bfd7f2296f9ff71` |
| `release/verify_release.py` | `d7cf9d81700abb190e0e09268e496d72d2ad427424aa1a92626b2f0217892a80` |
| `release/verify_source_reproduction.py` | `a7980c81987ec697e49d699117f90bd2adaf9e844ac4e33a0ed9dea94b7bc2a9` |
| `tools/build_input_inventory.py` | `b3237afa81e9abc5d962e3ca475fb3aab7d4cbc677e7ac55e7b8c8d986fadc51` |
| `submission/validate_submission_packages.py` | `712e9831305584d3755e6e06bdc317a3be2cc7d77df9f82646137e5d12922af8` |
| `submission/test_submission_validators.py` | `a39accf6c5fc61d9afe51d29318b537c6fa8b7e79ebd1a9503a8501bb4913f02` |
| `probes/test_k3p_probe_mutations.py` | `36ac124f658d50c17eb6e39738ec38e46f8471fd24905fcc84e2045351f50660` |
| `cut_recovery/strong_crossbridge/search_cut_minor_signs.py` | `850fd782f2edc868086cb3bb277d261fe03d619105f3c69a82bf29f418fd9cd0` |
| `release/RELEASE_FILESET.json` | `21e1d660b048487722b871e0041873feaba2065977c3f513b7f54b430045e939` |

The stored release report claims payload
`9448e3a0904ef6103dee7de817336f1724523298cd6edb4499c6c57027d0f6c9`,
32/32 rejected and 0 survived with 11 controls. Those are prior claims; the
fresh isolated replay must establish them independently.

## Precise safe execution recommendation

### A. Trusted staging for the portable mathematical runner

1. Preserve the delivery read-only. Create a byte-for-byte package copy in the
   ignored audit execution area and independently verify all 624 payload rows,
   the 625 checksum rows, file modes, and absence of symlinks **before** adding
   runtime directories.
2. Build the dependency venv offline from reviewed wheels; record wheel,
   interpreter, package metadata, and complete venv inventory hashes. Mount the
   package payload and actual venv read-only to package children. Permit writes
   only to the disposable copied workspace/session output actually required.
3. Replace or harden the staged external boundary and supervisor as required by
   R2-R4. Prove the boundary with positive runtime probes and negative canaries
   before setting `K3P_REFEREE_EXTERNAL_SANDBOX=YES`.
4. Run `plan` only if dynamic-plan evidence is desired; it is package-code
   execution. The static plan is already independently matched.
5. Launch exactly one requested long phase under the outer no-replace session
   ledger. Recommended outer wall limits are at least the package's per-command
   maximum plus cleanup margin: approximately 75 minutes for `verify`, and four
   hours for `regenerate` or `all`. Do not infer health from silence and do not
   relaunch while the session/process tree exists.
6. Accept `verify` only with exactly four ordered command results, the final
   package sentinel, 20 passing integrated children, zero undeclared workspace
   drift, zero venv drift, and pre/post integrity passes. Accept `regenerate`
   only with exactly the 55 ordered plan names once each under that phase and
   the same drift/integrity conditions. Accept `all` only as 4 + 55 in two
   workspaces; describe repeated logical checks explicitly.
7. Independently hash and parse the console capture, phase transcripts,
   reports, supplemental reports, all four inventories per phase, summary, and
   full declared `release/work/**` drift. Seal them from outside the child
   boundary after all descendants have exited.

### B. Trusted construction for the excluded Git-bound command

1. Do not use the live monorepo, a linked worktree, `git clone --shared`, an
   alternates file, a promisor repository, a partial-clone remote, or hardlinks
   to mutable packfiles.
2. In trusted preparation, re-resolve the declared commit and independently
   enumerate: the single commit object, every tree object at that commit, and
   only the 618 blobs below `k3p_level2_identifiability_final/`. Pack those
   objects by value into a newly initialized staging repository. Mark the commit
   as a shallow boundary, detach `HEAD` at the exact 40-hex ID, and perform a
   non-cone sparse checkout containing only
   `/k3p_level2_identifiability_final/`.
3. Atomically publish the finished staging directory only after confirming:
   exact detached `HEAD`; empty scoped status; 623 tracked target rows; the
   3,578-object census above; exact tree IDs; all target bytes/modes; no
   `.git/objects/info/alternates`; no `.promisor` pack; no
   `extensions.partialClone`; no `remote.*.promisor`; and no configured remote.
   The intentional absence of unrelated monorepo blobs must be disclosed. Do
   not use a normal full-connectivity `git fsck` as a false gate for this
   intentionally sparse object store; verify the enumerated object set and
   target tree instead.
4. Place controlled empty `HOME` and `TMPDIR` outside the source/audit evidence
   but inside the disposable boundary. Apply the clean environment in R7,
   read-only-mount `.git`, all tracked checkout data, and the reviewed venv;
   permit writes only to fixture `TMPDIR`, project `release/work/**`, and
   `/dev/null`. Deny network and all reads of the live monorepo, original
   package, credentials, browser/cloud stores, and referee output.
5. From the exact checkout's project root, run exactly one top-level command:

   ```text
   <reviewed-venv>/bin/python \
     reproducibility/test_release_engineering_mutations.py \
     --no-write-report
   ```

   Use an external whole-tree supervisor with a 15-minute wall limit and
   exclusive stdout/stderr capture outside child-visible paths.
6. Accept only if the captured output contains one well-formed JSON report and
   exactly one `K3P_RELEASE_ENGINEERING_MUTATIONS_PASS` sentinel; the report
   recomputes its canonical payload hash; it has the exact 32 ordered mutation
   names, all `REJECTED`, `mutation_count = rejected = 32`, `survived = 0`, and
   the exact 11 control names; its 13 script/policy hash fields equal the
   corresponding reviewed commit bytes; the externally recorded hash of the
   fourteenth imported input, `tools/build_input_inventory.py`, also matches;
   and the TAR/ZIP double-build and safe-extraction mode controls pass. Record
   external wall/CPU time and archive hashes because the native report does not
   record total runtime or commit.
7. After complete process-tree exit, require the checkout still to be detached
   at the exact commit, scoped status empty, tracked fingerprint unchanged,
   object census unchanged, and alternates/promisor/remote checks still empty.
   Independently inventory the venv and read-only inputs again. Seal the
   transcript/result summary outside child-visible paths.

## Final static conclusion

The third-revision package has a coherent, exact portable plan and materially
improved fail-closed runner. Its static command counts are **4 verification,
56 native regeneration, 55 portable regeneration, and 59 portable `all`**; the
single excluded Git-bound command is **32 mutations plus 11 controls**. The
declared Git commit can support a self-contained exact replay, and relevant
delivered release code matches it byte-for-byte.

Execution is nevertheless **not approved under the currently staged boundary**.
Once the broad read/Mach permissions, supervisor/evidence weaknesses, dependency
provenance, and exact-checkout controls above are repaired and independently
probed, both the portable mathematical replay and separate Git-bound mutation
replay are reasonable conditional-GO executions.
