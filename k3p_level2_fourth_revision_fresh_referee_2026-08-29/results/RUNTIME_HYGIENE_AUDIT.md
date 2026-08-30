# Runtime-hygiene and unsealed-evidence audit

Date: 2026-08-29 (America/Los_Angeles)

Package audited read-only:

`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

No active runner or long producer was invoked.  The only package program run was
the bounded integrity checker.

## Disposition

**Qualified PASS for the 635-file sealed payload; open release-evidence and
runtime-path findings.**  The sealed mathematical/proof payload passes its
declared byte-and-mode check and is not changed or invalidated by the material
under `review_runs/`.  The delivered folder as a whole, however, is not the
“clean delivered package” described by `START_HERE.md`, and its prior-run
acceptance evidence is not authenticated by the package seal.  In addition, a
future hostile object under the excluded runtime root can affect the runner's
control `HOME`/`TMPDIR` setup before the integrity preflight.

This is therefore **not merely documentation hygiene**.  It comprises:

- a **moderate release-evidence/provenance defect** if the supplied acceptance
  run is relied on as authenticated evidence;
- a **low-severity security-hardening defect** in handling excluded runtime
  descendants; and
- **minor editorial defects** in the clean-delivery and historical-ledger
  wording.

I found no present malicious object, no sealed-payload failure, and no theorem
impact.

## Exact observed state

`review_runs/` is a real directory of mode `0755`.  It contains 27 regular
files totaling 14,899,839 bytes and four descendant directories (five
directories including the root).  Object/mode census:

| Object | Count | Modes |
|---|---:|---|
| directories | 5 | all `0755` |
| regular files | 27 | 18 `0644`, 8 `0600`, 1 `0755` |
| symlinks | 0 | — |
| sockets/FIFOs/devices/other special objects | 0 | — |

All regular files have link count one.  The sole executable is
`review_runs/external_supervisor/isolated_supervisor.py`; none of the sealed
entrypoints invokes it.  The eight `0600` objects are the two integrated fresh
reports and six external-supervisor reports/inventories.  Neither
`review_runs/runner_control` nor `review_runs/.active_runner.lock` is present.

For a reproducible identity of the observed unsealed tree, I sorted its 31
descendants by relative POSIX path and encoded for each the path, object type,
four-digit mode, and, for files, byte count and SHA-256, as canonical compact
JSON (`sort_keys=True`, separators `(',', ':')`).  That 5,495-byte inventory has
SHA-256
`424511d53711f38a41417dc5024bde4c48430dd86c0d7b062f0119a4b6af5f72`.
This audit digest records what was inspected; it does not retroactively extend
the package seal.

## Finding RH-1 — the delivered folder is not clean, and the prior-run record is unsealed

Severity: **moderate release-evidence/provenance; no sealed-core or theorem
effect**.

The seal boundary itself is stated accurately at `START_HERE.md:20-25`:
top-level `.venv/` and `review_runs/` are excluded.  But the same sealed guide
says that `review_runs/` “is created locally when a reviewer runs the checks”
at `START_HERE.md:28-29` and that a clean delivered package contains neither
runtime root at `START_HERE.md:51-55`.  Those two statements are false of this
delivered fourth-revision folder.

The implementation confirms the exclusion is total:

- `referee_tools/verify_package_integrity.py:4-8` excludes contents, modes, and
  symlink targets in both runtime roots;
- `:73-78` classifies every path whose first component is `review_runs` as a
  runtime path;
- `:87-92` requires only the root itself to be a real directory and then
  continues; consequently the sealed-payload symlink/nonregular/mode checks at
  `:93-103` never run on any descendant; and
- `:681-688` reports the exclusion in the successful result.

`PACKAGE_MANIFEST.json:3817-3820` declares 635 payload files and 161,122,700
bytes at commit `10bd695cc7b7e0fd98a187026059b043589244f0`; it has no
`review_runs/` row.  A fresh bounded run returned
`K3P_REFEREE_PACKAGE_INTEGRITY_PASS`, exactly as this policy predicts.  That
PASS authenticates the declared payload, not all 664 regular files presently
delivered in the folder.

The unsealed `review_runs/POSTRUN_ACCEPTANCE.md:3-8` correctly calls its tree
post-seal runtime evidence.  Its seven named hashes at `:18-27` and `:37-50`
all recompute exactly for the current files.  This establishes present internal
self-consistency only: the acceptance Markdown, hashes, reports, transcript,
supervisor program, and sandbox profile all reside under the same freely
mutable exclusion.  They can be changed together without making the package
checker fail.  They therefore must be described as **supplied corroborating
evidence**, not package-sealed or independently authenticated evidence.

Recommended repair: ship the referee package with `review_runs/` absent.  If
the prior acceptance run is intended as release evidence, move it to a
read-only `prior_run_evidence/` payload whose complete bytes, modes, types, and
paths are bound by the outer manifest (or distribute it as a separately
authenticated evidence bundle).  Reserve `review_runs/` for the recipient's
new run.  Normalize or explicitly document the eight `0600` modes if the
evidence is meant to be portable across users.

## Finding RH-2 — excluded descendants are consumed before/after preflight

Severity: **low security hardening; no exploit observed in the delivered
tree**.

The present tree has no symlink or special object, so this is not a finding of
current compromise.  Prior timestamped output is also not imported into a new
mathematical workspace: the runner acquires an exclusive lock at
`referee_tools/run_active_verifiers.py:702-724` and creates a new timestamped
session with `exist_ok=False` at `:812-819`.

There is nevertheless a real boundary gap.  `RUN_REVIEW.sh:18-21` performs
`mkdir -p` on `review_runs/runner_control/home` and `tmp` **before** invoking
the integrity checker at `:31-37`.  The Python runner repeats creation and
resolves those paths into control `HOME` and `TMPDIR` at
`referee_tools/run_active_verifiers.py:169-185`.  Because the checker skips all
runtime descendants, an added `runner_control`, `home`, or `tmp` symlink can
remain seal-invisible while redirecting control paths or writes; hostile
precreation can also force denial of service.  The required external sandbox
reduces impact but does not make a seal PASS attest to these paths.

Recommended repair: run integrity before creating runtime descendants; reject
pre-existing non-directory components with `lstat`; create a private `0700`
real control directory with no-follow/open-relative semantics; and verify its
identity before use.  At minimum, fail closed on any symlink in
`review_runs/runner_control` and its `home`/`tmp` components.

## Finding RH-3 — the sealed “final” ledger's current wording is stale

Severity: **minor editorial release metadata**.

`START_HERE.md:10-14` accurately calls
`proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md` a historical
execution ledger.  The ledger itself nevertheless opens with a current-status
claim at `FINAL_RELEASE_ENGINEERING_REPORT.md:3`, labels its top section
“Current targeted second-referee repair” at `:22`, reports the then-current 32
release mutations at `:35-43`, and identifies a dated third-revision handoff
with 624 sealed files at `:45-54`.  The actual fourth-revision manifest instead
binds commit `10bd695...` and 635 files (`PACKAGE_MANIFEST.json:3` and
`:3817-3819`), while `proof_package/README.md:75-79` records the present
37-attack/12-control suite.

The warning at `FINAL_RELEASE_ENGINEERING_REPORT.md:66-70` correctly makes the
manifests authoritative and says older records should not identify the current
handoff, and the section beginning at `:72` is explicitly historical.  It does
not cure the unlabeled top-level status and “Current” heading, which remain
misleading when the ledger is sealed into a later handoff.  Add a short
fourth-revision addendum or relabel the overall status/top section as a dated
historical record.  This wording does not alter any machine-checked evidence.

## Bottom line

The 635-file sealed payload remains intact.  The 27-file pre-existing
`review_runs/` tree is structurally ordinary and internally hash-consistent but
is outside that result.  Treating it as authenticated acceptance evidence would
be an integrity error; executing its lone historical supervisor script as
trusted code would likewise be unjustified.  Clean delivery plus a separately
sealed prior-run evidence bundle, together with no-follow runtime setup, closes
the substantive gap.
