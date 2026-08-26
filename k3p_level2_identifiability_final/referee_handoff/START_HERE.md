# Independent referee package: start here

This folder is designed for an independent post-submission review of the
article and its computer-assisted proof package.  It does not ask for, assume,
or encode a favorable verdict.  Stored reports, status fields, checksums, and
prior audits are evidence to inspect, not conclusions to adopt.

## Contents

- `paper/` contains convenient copies of the article and reader supplement.
- `proof_package/` is an inspectable copy of the canonical full
  reproducibility payload, supplemented by the 18 work logs needed by fresh
  dependency checks.
- `REFEREE_PROMPT.md` is a neutral review brief.
- `PACKAGE_MANIFEST.json` and `SHA256SUMS` bind every shipped file.
- `referee_tools/` contains a Git-independent integrity checker and isolated
  verifier runner.
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

No active mathematical verifier makes a network request.  Dependency
installation may require package-index access unless the reviewer supplies an
offline wheel cache.

## Recommended execution order

First read the article, supplement, neutral prompt, active manifest, and
relevant source code.  Inspect code before executing it.

Confirm that the portable runner reconstructs the expected 43-command
mathematical regeneration plan without starting it:

```sh
./RUN_REVIEW.sh plan
```

Then run the fresh mathematical verification:

```sh
./RUN_REVIEW.sh verify
```

On the reference M1 MacBook Pro this takes about 3--4 minutes and has used
roughly 0.6 GB peak memory.

After code inspection, run the complete active producer/verifier graph once:

```sh
K3P_REFEREE_CONFIRM_REGENERATION=YES ./RUN_REVIEW.sh regenerate
```

Allow 90--120 minutes.  The observed reference runtime was about 72 minutes,
including a single probe producer taking about 49 minutes.  The runner blocks
on each command.  Do not poll by launching a second copy, and do not restart a
healthy long-running producer.

For a combined run in two independent working copies:

```sh
K3P_REFEREE_CONFIRM_REGENERATION=YES ./RUN_REVIEW.sh all
```

Complete transcripts, timings, output hashes, and before/after file-drift
records are written under `review_runs/`.  Never report a command as executed
unless its transcript is present.

## Important boundary

The original release wrappers require a live clean Git checkout and therefore
are not the portable entrypoints for this extracted package.  The supplied
runner invokes the mathematical verifiers and the established producer graph
directly, omitting only the Git-bound release-input check and the
nonmathematical release-engineering mutation suite.  Package integrity is
checked independently before every run.

The exact Tectonic 0.16.9 arm64 binary is not bundled.  It is needed only to
reproduce the PDFs byte-for-byte, not to run the mathematical proof checks.
The source archives record its expected executable SHA-256 and deterministic
build environment.

Passing scripts cannot replace scrutiny of the handwritten topology,
analytic, semialgebraic, genericity, reconstruction, and gluing arguments.
The referee must assess those transitions independently and may reach any
supported verdict.
