# Fourth-revision release-engineering reaudit

Date: 2026-08-29 (America/Los_Angeles)

Package audited (no retained modification; transient audit caches are disclosed
in Section 1):

`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

This audit was confined to the prior mode-preservation finding (F1), the
manifest/mutation-metadata finding (F3), package sealing, the portable runner's
fail-closed controls, and the Git-bound release-engineering evidence.  I did
not invoke `RUN_REVIEW.sh verify`, `regenerate`, or `all`, and did not launch
any hour-scale producer.  All fresh executions described below were bounded
unit, integrity, selection, or release-mutation checks.

## Executive result

**Disposition: the prior blocking official-runner mode defect is repaired, and
the substantive F3 certificate metadata is repaired.  Package sealing and the
Git-bound release mutation suite pass fresh independent checks.  Two minor
release/documentation issues remain:**

1. A fourth public atomic JSON writer,
   `proof_package/reproducibility/verify_k3p_same_classification.py::atomic_json`,
   is omitted from the new mode control and still changes an existing or new
   report to mode `0600`.  The declared release/referee routes avoid a final
   sealed-payload drift by using `--no-write-report`, a declared runtime-area
   report, and canonical restoration, so this is not the former blocking
   runner failure and has no theorem effect.  It is nevertheless an incomplete
   portability repair and an overstated test name.
2. The sealed historical release ledger still opens with a “current targeted
   second-referee repair” section claiming 32 release mutations, although the
   present third-referee repair has 37 mutations and 12 controls.  The package
   explicitly labels this file a historical ledger and the active README gives
   the correct current counts, so this is documentary rather than evidentiary.

Subject to those two minor corrections, this release-engineering subaudit is a
PASS.  I found no route by which either residual issue changes the mathematical
classification or invalidates the supplied, internally consistent but unsealed
4-command/55-command run record.  This scoped PASS does not assess the
separately reported pre-existing `review_runs/` provenance and path-hardening
issue.

## 1. Package identity and fresh seal verification

The outer and proof-core identities agree:

- package-builder commit:
  `10bd695cc7b7e0fd98a187026059b043589244f0`;
- proof-source commit:
  `10bd695cc7b7e0fd98a187026059b043589244f0`;
- canonical archive SHA-256:
  `fecb2eda22bcb0558c02e14fdb7767b4229bde33471a4de2a764191f42d8d293`;
- sealed outer payload: 635 files, 161,122,700 bytes;
- canonical proof core: 597 declared members, 160,213,642 bytes;
- `PACKAGE_MANIFEST.json` SHA-256:
  `c67c1c524ef59217a2327e7dd4016cd82a9b8be1e8f188e6cc61a4fe1fd6c725`;
- outer `SHA256SUMS` SHA-256:
  `5bf8045cf745754092f0eb7e1a00bd7842ba475dc70d74091b099e135b974fa4`;
- `proof_package/ARCHIVE_MANIFEST.json` SHA-256:
  `7d665952289812fd4533c5c534b3f579eff5dd4abf35f1bb0c56a4b6c893f114`.

A fresh execution of `referee_tools/verify_package_integrity.py` returned
`K3P_REFEREE_PACKAGE_INTEGRITY_PASS`.  It checked all delivered payload bytes
and modes, all 597 declared core members and modes, both source archives, both
source-reproduction reports, four transcripts, the 725-file Tectonic cache
contract, and both delivered PDFs.  The relevant fail-closed implementation is
at:

- `referee_tools/verify_package_integrity.py:73-104` (runtime exclusions and
  no-follow payload traversal);
- `:107-180` (outer byte/mode/SHA seal);
- `:183-221` (inner core member byte/mode/SHA seal);
- `:224-293` (cache-manifest contract);
- `:369-482` (source-ZIP structural and source-byte checks);
- `:485-666` (closed source-reproduction evidence contract);
- `:669-696` (fail-closed entry point).

I then copied only the sealed payload into a temporary directory and performed
two independent hostile controls:

- changing `START_HERE.md` from `0644` to `0600` was rejected with exit 1 and
  `outer package payload mismatch`;
- adding an otherwise unsealed symlink was rejected with exit 1 and
  `symlink forbidden in sealed payload`.

After removing my temporary test fixtures, the original package passed the
seal again and contained no `__pycache__` or `.pyc` outside the explicitly
excluded runtime roots.

Audit-trace disclosure: two direct module-import controls briefly emitted
exactly three CPython cache files (two below
`proof_package/reproducibility/__pycache__/` and one below
`referee_tools/__pycache__/`).  I removed only those three audit-created cache
files and their now-empty directories, then reran the full package seal and the
no-cache search successfully.  No sealed source or evidence byte was changed.

The seal boundary is accurately disclosed.  Top-level `.venv/` and
`review_runs/` are intentionally excluded, and the compressed canonical TAR
container is not delivered or checked by this extracted-package verifier
(`START_HERE.md:20-25`; `verify_package_integrity.py:681-688`).  Accordingly,
stored `review_runs/` material is corroborating runtime evidence, not part of
the immutable payload seal.

## 2. Independent Git binding

The named source commit exists locally and is commit object
`10bd695cc7b7e0fd98a187026059b043589244f0` (“Reseal release engineering
controls”), with commit epoch `1788044340`, matching the archive manifest.

I independently reconstructed the full release selection from the Git tree,
without trusting the archive member list:

- the Git project tree has 626 tracked entries;
- the release policy selects exactly 594 committed files;
- the independently recomputed canonical selection-list SHA-256 is
  `4d0686fc43bc53bb76d61d056f78f72f9da585e743ae386016fc7d64ba12e67a`,
  exactly the policy lock;
- all 594 selected files, totaling 160,051,159 bytes, were read directly from
  Git objects at the named commit and compared byte-for-byte to the expanded
  proof package;
- every selected member's manifest hash, byte count, and canonical archive
  mode (`0755` for `.py`/`.sh`, otherwise `0644`) agreed;
- the archive manifest's exact 597-member set is those 594 committed files plus
  `REPRODUCIBILITY_README.txt` and the two generated source ZIPs.

I separately compared 29 outer or post-archive copied files directly against
the same Git commit: the three handoff documents/scripts, all four delivered
referee-tool files, both paper PDFs, the release ledger, and 19 work logs.  The
twentieth tracked work log is already included in the 594-file canonical
selection.  All comparisons passed.  The eight ignored source-reproduction
assets (two reports, four transcripts, two source ZIPs) are not Git blobs by
design; the package builder and the fresh integrity check instead bind their
paths, hashes, source semantics, commit, toolchain/cache contract, and PDF
outputs.

This closes the principal risk that a self-consistent package manifest might
merely *name* a commit without containing that commit's bytes.

## 3. Prior F1: official-runner mode preservation

### Repaired sites

All three sites named in the prior report now set the temporary file to
`0644` before atomic replacement:

- `proof_package/reproducibility/verify_primary.py:79-89`;
- `proof_package/cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py:185-195`;
- `proof_package/reproducibility/strong_cut_transfer_gate.py:395-404`.

The new focused control at
`referee_tools/test_output_mode_preservation.py:48-78` loads and exercises all
three writers for both an existing and a new target.  My fresh execution
observed `0644` in all six cases.  Its second control
(`:81-121`) restored a canonical report's bytes and `0644` mode while retaining
the location-dependent generated copy at its observed `0600` mode.  Its unsafe
replacement mutation (`:124-142`) reproduced `0644 -> 0600` and was correctly
marked rejected.

The official runner now invokes this control before every phase
(`run_active_verifiers.py:547-549`, `:680-699`), inventories bytes, modes,
object types, and symlink targets (`:49-98`), and rejects any non-runtime
workspace drift or virtual-environment drift (`:593-625`).

The package folder's excluded, unsealed exact-once run record corroborates the
fresh unit control:

- verify: 4/4 commands PASS, empty workspace drift, empty venv drift;
- regenerate: 55/55 commands PASS, empty workspace drift, empty venv drift;
- both phases bind the mode-control stdout SHA-256
  `309da296289aa8552c06354a333e6f55547c1f0fa5abfb4419a708b96e04d5a0`;
- external before/after inventory payloads were exactly equal for 7,775
  package entries and 7,072 venv entries.

Thus the former top-level failure caused by 11 (or 10 on the verify route)
`0644 -> 0600` changes is closed.

### Minor residual: fourth integrated-report writer

`proof_package/reproducibility/verify_k3p_same_classification.py:2189-2198`
contains the same `NamedTemporaryFile`/`os.replace` pattern but no `chmod`.
The new “public atomic JSON mode preservation” control enumerates only three
targets (`test_output_mode_preservation.py:48-58`) and omits this writer.

I imported only that writer in a temporary directory and called it on both an
existing `0644` report and a new path.  Both results were `0600`:

```json
{"existing":"0600","new":"0600"}
```

This does not recreate the former official-runner failure:

- the artifact-only route uses `--no-write-report`
  (`ACTIVE_VERIFIER_PLAN.json:14-23`);
- the fresh runner route writes explicitly under the declared
  `release/work/` runtime area (`ACTIVE_VERIFIER_PLAN.json:25-34`);
- the release full suite also uses `--no-write-report`
  (`proof_package/reproducibility/run_release_suite.py:93-110`);
- where the runner temporarily produces a location-bearing primary report, it
  preserves the generated evidence and restores canonical bytes and mode
  (`run_active_verifiers.py:436-472`, `:580-590`).

Nevertheless, invoking the integrated verifier directly with its default
report path (`verify_k3p_same_classification.py:2236-2240`, `:2275-2276`) changes
the sealed canonical report's mode and makes the package seal fail.  Recommended
repair: add `os.chmod(temporary, 0o644)` before line 2198 and add this fourth
writer's existing/new cases to `test_output_mode_preservation.py`.

Severity: **minor release-interface defect; no theorem effect and no failure of
the declared runner routes**.

## 4. Prior F3: manifest and mutation metadata

The substantive prior inconsistencies are fixed:

- `ACTIVE_MANIFEST.json:319-321` now says
  `passed_16_of_16_with_two_clean_modes`;
- `ACTIVE_MANIFEST.json:395-397` binds the same 16-rejection report, whose
  SHA-256 is
  `b02af9e01230047db346e324b654efd42c1febbfd2dc94c06a9f17b17adf30bc`;
- `verify_primary.py:317-322` requires exactly 16 rejected attacks and two
  passing clean modes;
- the stored report contains 16 mutations, 16 rejected, zero survived, and two
  clean PASS replays;
- the coherent legacy-provenance mutation now accurately says it reseals only
  the local attack cone and does **not** reseal unrelated downstream stored
  reports (`test_cut_transfer_gate_mutations.py:121-127`, `:163-172`);
- the manifest version is now
  `1.0.0-third-referee-certificate-fidelity-repaired`
  (`ACTIVE_MANIFEST.json:382`), correctly describing the repair that produced
  this fourth handoff.

The current release-engineering mutation metadata is also internally exact:

- stored report: 37 mutations, 37 rejected, zero survived, 12 deterministic
  controls;
- stored logical payload SHA-256:
  `e8d8fa6769c57d27fb636a1e8fef6038b1c01a6167b935e9f6ebfdd1452cca35`;
- stored file SHA-256:
  `da1d451839de33515f4b11bbacac8e3f6b8f3a4d098c5486b88f430fce3e3daf`;
- `verify_release_inputs.py:129-173` requires the count 37, verifies the report
  payload, and binds all 15 named implementation/policy inputs by hash;
- a fresh portable `verify_release_inputs.py --allow-uncommitted-sources` run
  returned `K3P_RELEASE_INPUT_GATE_PASS`, 108 active path bindings, and the
  correct 37-case mutation summary.

### Minor documentary residue

`proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md:3`, `:22`, and `:42`
still present a “current targeted second-referee repair” and a 32-mutation
count.  In contrast, `proof_package/README.md:75-79` correctly distinguishes
the then-current 32-case historical run from the present 37-attack/12-control
third-referee repair.  `START_HERE.md:12-14` also explicitly calls the final
release report a historical execution ledger.

This does not enter the active proof core—the release policy excludes that
ledger from the canonical archive—and it does not contradict the current
machine-checked report.  It is, however, sealed into the outer referee package
and its top/current wording is needlessly confusing.  Recommended repair: add
a short current third-referee/fourth-handoff addendum at the top, or relabel the
existing heading and status as historical.

Severity: **editorial release metadata only**.

## 5. Fresh exact-commit release-engineering replay

I created a sparse, detached, clean worktree at exactly
`10bd695cc7b7e0fd98a187026059b043589244f0` and ran

```text
python3 reproducibility/test_release_engineering_mutations.py --no-write-report
```

once.  A preliminary setup command had stopped before invoking the script
because it named a nonexistent package-local interpreter; no mutation case ran
in that setup attempt.  The actual suite invocation was single, bounded, and
completed in under ten seconds.

Fresh result:

- initial scoped Git status: clean;
- final scoped Git status: clean;
- 37/37 mutations rejected;
- zero survivors;
- 12/12 controls passed (`PASS` or deterministic
  `PASS_IDENTICAL` as appropriate);
- sentinel `K3P_RELEASE_ENGINEERING_MUTATIONS_PASS` observed;
- logical payload SHA-256 exactly matched the stored report:
  `e8d8fa6769c57d27fb636a1e8fef6038b1c01a6167b935e9f6ebfdd1452cca35`;
- complete stdout SHA-256:
  `f53948ccedfcfc029b9e4ce8aca8aa1ffc5634b9732dc2a9d09d7143683ed456`.

The tested attack set is explicit at
`test_release_engineering_mutations.py:1079-1169`; report counts and all live
code/tool-policy hashes are constructed at `:1180-1218`.  Coverage includes
stale checksums/member hashes, self-reference, path traversal, noncanonical ZIP
time/TAR mode, optimized-Python bypass, forbidden evidence, tool/cache/source
contract tampering, malformed filesets, unready/mislabeled/malicious
submissions, direct and descendant timeouts, forged command plans/envelopes,
generated README and sidecar tampering, dirty final verification, forged build
counts, and certified-manifest input drift.

## 6. Runner fail-closed controls

Static inspection found the following controls correctly implemented and
accurately disclosed:

- fixed ten-variable child environment:
  `run_active_verifiers.py:146-186`;
- dependency/interpreter/module hash recording: `:189-237`;
- process-group creation, timeout termination, descendant detection and reaping:
  `:240-356`;
- complete pre/post workspace and venv inventories: `:523-625`;
- atomic no-replace lock plus inode identity check: `:702-744`;
- external-sandbox attestation and explicit non-enforcement disclosure:
  `:751-811` and `START_HERE.md:61-73`;
- separate confirmation before any `regenerate` or `all` route:
  `run_active_verifiers.py:809-811`.

I exercised five short hostile controls directly against the runner helper in
temporary directories.  All were rejected with the intended failure class:

- duplicate active lock;
- child exit status 7;
- successful child missing its required sentinel;
- command timeout;
- parent exit leaving a descendant in the process group.

The package makes no false claim that process groups are an OS sandbox or that
they can contain a deliberately escaped process group; `START_HERE.md:64-73`
places that responsibility at the external boundary.

The stored acceptance record is internally consistent.  Its listed SHA-256
values recompute exactly:

- runner summary:
  `8aca186fe28786e61d7c25798fecf255b43dcaf9cfd0dc0035802757bc5f0db8`;
- verify report/transcript:
  `801e180a248c4c6f0e2fdcbf98bed6e0da4ed999fc59a383e5d88a128c43f1e5` /
  `c0f781dfb48bcea8772d97f151fdd3b502f8af69a743e262fa2f385c78ad5ce2`;
- regenerate report/transcript:
  `fc0cecd346d3fe1c7ffb9ad09928b67de485fadce8792f0689c7cf453a2d73f3` /
  `ff494b620088b4a8ba3ff0a079f5d3ffe4ea70f0fec1bf5311515fe7bf70593d`;
- external supervisor JSON/log:
  `afafe7d2504a0937028ec021030ad01dea059fcc932d5f6aa8db7941366c18be` /
  `b8a09c4dc2c029db09827a7abe4fe685f64e810abd7870f9ee74a5855ff5e5b4`.

That record reports one `all` launch, 4/4 verify commands, 55/55 regeneration
commands, and one probe producer execution taking 2,886.752 seconds with stdout
SHA-256
`401ba869ca84580d69863fa01737b3fd6cbf697f06283f6358f63083d082bd62`.
Because `review_runs/` is intentionally outside the seal, these hashes establish
self-consistency and preservation of the supplied runtime evidence; they do
not turn it into a Git-committed or package-sealed execution record.

## Final disposition for the parent referee

- Prior F1 blocking official-runner failure: **FIXED**.
- Residual fourth atomic writer: **MINOR OPEN RELEASE-INTERFACE DEFECT**.
- Prior F3 12/16 count mismatch and overbroad reseal wording: **FIXED**.
- Historical ledger header/count: **MINOR EDITORIAL OPEN ITEM**.
- Outer package byte/mode/symlink seal: **PASS**.
- Canonical proof-core and commit binding: **PASS**.
- Exact detached Git release mutation replay: **PASS, 37/37 rejected and 12
  controls passed**.
- Runner lock/timeout/sentinel/descendant fail-closed controls: **PASS**.
- Theorem impact of findings in this report: **none identified**.
