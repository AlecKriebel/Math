# Severity-ranked findings and repair verification

Date: 2026-08-29

## Executive assessment

I found no new theorem-level defect and no failure in the repaired active
certificate routes.  The four findings from the third-revision review are
substantively closed.  Three release/provenance issues remain: two are
low-severity, while the unsealed prior-run tree is moderate only if treated as
authenticated acceptance evidence.  None changes a theorem hypothesis,
certificate conclusion, or generated mathematical byte string.

Recommended disposition: **valid subject to the localized corrections F5--F7
below**.

## Prior findings

### F1 — Active runner mode drift: closed

The three public writers that caused the former official-runner failure now
set their temporary file to mode `0644` before replacement:

- `proof_package/reproducibility/verify_primary.py:79-89`;
- `proof_package/reproducibility/strong_cut_transfer_gate.py:395-404`; and
- `proof_package/cut_recovery/strong_crossbridge/topology_regeneration/
  verify_cut_topology_regeneration.py:185-195`.

`referee_tools/test_output_mode_preservation.py:48-142` now tests existing and
new outputs, restoration of the location-dependent primary report, and a
negative unsafe-writer control.  A fresh bounded run observed six `0644`
outputs and rejected the `0644 -> 0600` mutant.  The exact-once official replay
is reported separately in `COMPUTATIONAL_REPLAY.md`.

### F2 — Untyped cut implication claims: closed

The cut evidence now carries a typed nine-row declaration.  The producer,
direct verifier, and separately implemented adversarial verifier each carry
the full object, and both verifiers require literal equality:

- `cut_recovery/strong_crossbridge/global_transfer/
  build_k3p_cut_inclusion_evidence.py:26-111,246-307`;
- `.../verify_global_transfer.py:43-126,309-326`; and
- `.../adversarial/verify_global_transfer_adversarial.py:83-167,424-441`.

The active release gate freshly invokes both semantic verifiers in ordinary
and optimized mode (`.../verify_release.py:304-369` and
`reproducibility/strong_cut_transfer_gate.py:152-182,364-365`).  Referee-owned
tests rebuilt the evidence byte-identically, rejected 72/72 ordinary and 18/18
optimized coherently resealed claim mutations, rejected four custom-path
binding attacks, and passed the release wrapper once in each mode.  The
manuscript now accurately reserves the analytic implications to the
handwritten proof while describing the machine's typed binding.

### F3 — Mutation count and resealing metadata: closed

`proof_package/ACTIVE_MANIFEST.json:319-321,395-397` now binds
the actual 16/16 cut-gate result.  The coherent-attack metadata correctly says
that the local attack cone is resealed and unrelated downstream stored reports
are not (`test_cut_transfer_gate_mutations.py:121-127,163-172`).  A fresh
exact-commit release-engineering run rejected 37/37 attacks and passed 12/12
controls with a clean scoped Git state.

### F4 — Source/PDF resource contract: closed

The source verifier now binds the Tectonic binary and version, bundle URL and
digest, exact 725-file/57,507,581-byte cache inventory, cached-only command,
and exact 12-key child environment.  The outer seal includes both final-commit
reports and all four transcripts.  An independent implementation matched all
23 article and one supplement Git source blobs and reconstructed both source
ZIPs byte-identically.  Fresh network-denied builds produced each PDF twice,
and all four outputs matched the delivered PDFs byte-for-byte.  See
`SOURCE_LITERATURE_REAUDIT.md` for the hashes and disclosed external-toolchain
boundary.

## Fresh-execution limitation (not a package defect)

The single combined runner launch passed its entire 4-command verification
phase and the first 38 regeneration commands.  Regeneration command 39,
`probe_hour_scale_producer`, then failed solely with `Errno 28: No space left
on device` while flushing three gzip ledgers after reaching two-port parent
600/2,107.  Commands 40--55 were not invoked, and the process was not rerun in
accordance with the user's instruction.

The current verification report has empty workspace and virtual-environment
drift.  The postfailure package seal passes and the 6,635-entry environment is
unchanged.  The probe, restoration, anchor, four-port, and sharpness trees are
byte-identical to the third revision, whose independent exact-once run passed
all 55 command bodies; current referee-owned checks and the current integrated
20-child replay also pass.  This is enough for the theorem assessment but is
not a fresh current 55/55 regeneration.  Exact accounting is in
`COMPUTATIONAL_REPLAY.md`.

## Remaining findings

### F5 — A fourth direct-report writer still creates mode `0600`

**Severity:** minor release-interface/portability defect; no theorem effect and
no effect on the declared portable runner routes.

`proof_package/reproducibility/verify_k3p_same_classification.py:2189-2198`
uses `NamedTemporaryFile` followed by `os.replace` without setting the intended
public mode.  A fresh temporary-directory control found mode `0600` for both an
existing `0644` destination and a new destination.  The new test named
`public_atomic_json_mode_preservation` enumerates only the other three writers
(`referee_tools/test_output_mode_preservation.py:48-58`).

This omission does not revive F1.  The artifact-only and release-suite paths
use `--no-write-report`; the fresh integrated path writes under the declared
`release/work/` runtime area; and the official runner restores the canonical
location-dependent report.  Directly invoking the integrated verifier with
its default sealed report path can nevertheless change that file's mode and
make the package seal fail.

**Repair:** add `os.chmod(temporary, 0o644)` before replacement and add this
fourth writer's existing/new cases to the focused mode control.

### F6 — The historical release ledger presents stale material as current

**Severity:** minor editorial/release-metadata defect; no evidentiary or
theorem effect.

`proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md:3,22-54` opens with
“current targeted second-referee repair,” the earlier 32-mutation count, the
third-revision PDF hashes, and its 624-file handoff.  The same file later says
that these are historical and that manifests control (`:66-70`), while
`START_HERE.md:13-18` explicitly calls it a historical execution ledger.  The
current manifest, PDFs, source reports, transcripts, and active README carry
the correct fourth-handoff data.

**Repair:** add a current fourth-handoff addendum or relabel the opening status
and section as historical; do not leave the word “current” attached to the
older snapshot.

### F7 — The delivered runtime tree is unsealed and insufficiently hardened

**Severity:** minor delivery hygiene plus low-severity runtime-path hardening
in this review, because the supplied prior run was not relied upon; it would
become a moderate provenance defect only if represented as authenticated
acceptance evidence.  No present malicious object, theorem effect, or
fresh-execution effect was observed.

`START_HERE.md:28-29,54-55` says `review_runs/` is reviewer-created and absent
from a clean delivery.  The supplied folder already contains 27 files totaling
14,899,839 bytes under author-generated `review_runs/`.  The seal deliberately
excludes that tree (`referee_tools/verify_package_integrity.py:73-92`), so the
material is untrusted and was not used as theorem evidence.  Its internally
consistent hashes do not authenticate it, because the reports, hashes, and
acceptance note can all be changed together without changing the seal.  The
fresh audit excluded it when constructing the execution copy.  The delivered
runtime tree contains only regular files and directories; no symlink or
special object was found.

There is also a low-severity prospective path issue.  `RUN_REVIEW.sh:18-21`
creates `review_runs/runner_control/home` and `tmp` before integrity preflight,
while the checker ignores all runtime descendants.  A hostile pre-existing
symlink at those excluded paths could redirect the runner's control `HOME` or
`TMPDIR`; the required external sandbox limits impact but does not make the
seal attest to those paths.  No such object exists in the supplied folder.

**Repair:** omit `review_runs/` from the distributed folder.  If the historical
run is retained, seal it under a separate non-runtime evidence path and tell
reviewers to begin from a clean sealed-only extraction.  Run integrity before
creating runtime descendants, reject pre-existing non-directory/symlink path
components with `lstat`, and create the private control directory with
no-follow semantics.

## Theorem dependency

F5--F7 do not enter the cut recovery, four-port classification, probe census,
bridge gluing, global analytic argument, strict-CT specialization, or
weak-class sharpness proof.  They therefore require no theorem-statement or
mathematical repair.  F5 is worth fixing because a public default invocation
should not damage an otherwise byte-and-mode-sealed package; F6--F7 are worth
fixing because a referee package should make its current/historical and
sealed/unsealed evidence boundaries immediately unambiguous.
