# Independent referee package: start here

This folder is designed for an independent review of the
article and its computer-assisted proof package.  It does not ask for, assume,
or encode a favorable verdict.  Stored reports, status fields, checksums, and
prior audits are evidence to inspect, not conclusions to adopt.

## Contents

- `paper/` contains convenient copies of the article and reader supplement.
- `proof_package/` is an inspectable copy of the canonical full
  reproducibility payload, supplemented by the work logs needed by fresh
  dependency checks and by `release/FINAL_RELEASE_ENGINEERING_REPORT.md`, the
  historical execution ledger cited from the project README; the package
  manifest gives the exact rebuilt count.
- `REFEREE_PROMPT.md` is a neutral review brief.
- `PACKAGE_MANIFEST.json` and `SHA256SUMS` provide a sealed-payload check by
  binding the bytes and mode of every delivered payload file and the manifest
  bytes.  `SHA256SUMS` cannot hash itself; reviewer-created
  top-level `.venv/` and `review_runs/` runtime areas are deliberately outside
  the seal.  The checker validates declared members of the expanded canonical
  proof core; it does not validate a compressed archive container.
- `referee_tools/` contains a Git-independent integrity checker and copied,
  Git-free workspace runner.
- `review_runs/` is created locally when a reviewer runs the checks; it is not
  part of the sealed package.

Some machine filenames and sentinels retain a legacy internal outcome code for
backward-compatible hash and schema bindings.  That code is not mathematical
terminology.  The theorem itself is the complete K3P containment and
structural-identifiability classification stated in the article.

## Runtime setup

Use Python 3.14 when possible.  The supplied requirements pin the versions of
`mpmath`, `networkx`, `numpy`, and `sympy`, but do not hash-lock distribution
wheels.  Record the actual interpreter, operating system, architecture, and
installed-package hashes in the review report.

From this package root:

```sh
python3 referee_tools/verify_package_integrity.py
python3 -m venv .venv
.venv/bin/python -m pip install -r proof_package/reproducibility/requirements.txt
```

Perform the first integrity check before creating or activating the virtual
environment.  `RUN_REVIEW.sh` repeats that check with `/usr/bin/python3` when
available; set `K3P_REFEREE_TRUSTED_PYTHON` to another trusted standard-library
interpreter if needed.  A clean delivered package contains neither `.venv/`
nor `review_runs/`.

No active mathematical verifier makes a network request.  Dependency
installation may require package-index access unless the reviewer supplies an
offline wheel cache.

`RUN_REVIEW.sh` creates Git-free copied workspaces, gives child processes a
fixed ten-variable non-secret environment, holds an atomic no-replace lock,
and terminates and reaps a command's process group after interruption, timeout,
or an unexpected surviving descendant.  These controls do not constitute an
operating-system security sandbox and cannot prevent a process from reading
other host files or opening a network connection.  Supply the offline,
credential-free VM, container, account, or operating-system sandbox boundary
externally before executing untrusted code.  The runner requires
`K3P_REFEREE_EXTERNAL_SANDBOX=YES` as an explicit acknowledgement, but cannot
verify or enforce that claim.
For hostile code, the external boundary should also supervise the full process
tree, including descendants that deliberately escape their inherited process
group.

Only one runner may use a package at a time.  Its atomic lock is
`review_runs/.active_runner.lock`.  A normal exit or handled interruption
removes it.  After an uncatchable termination, remove a stale lock only after
independently confirming that no runner or descendant remains.

## Recommended execution order

First read the article, supplement, neutral prompt, active manifest, and
relevant source code.  Inspect code before executing it.

Confirm that the portable runner reconstructs the expected 55-command active
mathematical producer/verifier plan without starting it:

```sh
K3P_REFEREE_EXTERNAL_SANDBOX=YES ./RUN_REVIEW.sh plan
```

Then run the fresh mathematical verification:

```sh
K3P_REFEREE_EXTERNAL_SANDBOX=YES ./RUN_REVIEW.sh verify
```

On the reference M1 MacBook Pro, allow roughly 35--50 minutes; the exact
runtime and peak memory are recorded in the run report.  The full semantic
probe replay and the independent 405,216-case four-port replay dominate this
phase.

After code inspection, run the complete active producer/verifier graph once:

```sh
K3P_REFEREE_EXTERNAL_SANDBOX=YES \
K3P_REFEREE_CONFIRM_REGENERATION=YES ./RUN_REVIEW.sh regenerate
```

Allow roughly 150--210 minutes on the reference M1 machine.  The earlier
44-command package took about 72 minutes, including a single probe producer
taking about 49 minutes; the strengthened plan additionally regenerates and
independently verifies the full four-port universe and semantically replays
all probes.  The runner blocks
on each command.  Do not poll by launching a second copy, and do not restart a
healthy long-running producer.

For a combined run in two independent working copies:

```sh
K3P_REFEREE_EXTERNAL_SANDBOX=YES \
K3P_REFEREE_CONFIRM_REGENERATION=YES ./RUN_REVIEW.sh all
```

Because the seal deliberately excludes those runtime areas, a post-run seal
PASS is not by itself a full filesystem-drift check.  The runner therefore
records full before/after inventories of the copied workspace and virtual
environment, including bytes, modes, object types, and symlink targets.  It
fails on virtual-environment drift and on copied-workspace drift outside the
declared `release/work/` runtime area; all runtime-area differences remain
printed in the report rather than being hidden.

Complete top-level command transcripts, timings, output hashes, interpreter
and platform metadata, dependency versions and module-file hashes, and
before/after file-drift records are written under `review_runs/`.  Verify mode
also preserves and hashes the integrated gate's detailed report for its twenty
nested fresh replays.  Never report a command as executed unless its evidence
is present.

## Important boundary

The original release wrappers require a live clean Git checkout and therefore
are not the portable entrypoints for this extracted package.  The supplied
runner invokes the active mathematical verifiers and the established producer
graph directly, including the portable release-input semantic-binding check.
It omits only the nonmathematical release-engineering mutation suite, which
tests Git-index and packaging behavior and requires the exact live checkout;
its source remains available for inspection.  Package integrity is checked
independently before every run.

The runner treats any byte, mode, type, or symlink-target drift outside
declared runtime evidence as a failure.  The primary gate's otherwise
identical location-bearing report is
preserved separately for audit and the canonical byte copy is restored before
downstream binding checks.

The exact Tectonic 0.16.9 arm64 binary is not bundled.  It is needed only to
reproduce the PDFs byte-for-byte, not to run the mathematical proof checks.
The source archives record its expected executable SHA-256 and deterministic
build environment.

Passing scripts cannot replace scrutiny of the handwritten topology,
analytic, semialgebraic, genericity, reconstruction, and gluing arguments.
The referee must assess those transitions independently and may reach any
supported verdict.
