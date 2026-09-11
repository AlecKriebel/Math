# Offline Lean environment handoff

**No compiler bundle has been built in this chat.** The supplied workflow and
scripts are a way to obtain the missing pinned toolchain/cache. Their local
transport and syntax tests passed; GitHub execution, real toolchain acquisition,
and real Lean smoke tests have **not** been run here.

The available chat runtime can execute local code but cannot download dependencies.
It has no Lean/Lake installation. The connected GitHub integration rejects writes
with HTTP 403 and rejects artifact downloads above 536,870,912 bytes. This is why
restarting the chat did not fix the compiler problem.

## One-file GitHub setup

Add `bell-lean-offline.yml` to this path in `AlecKriebel/Math`:

    .github/workflows/bell-lean-offline.yml

The file is self-contained: it embeds the exporter, restorer, exact Lake
configuration, and full dependency manifest. It does not require that the Lean
project has already been pushed to the repository. It requests only repository
read permission, uses no repository secrets, does not change repository content,
and does not merge anything. Adding the file triggers the path-filtered push
workflow; it can also be run manually from Actions.

The workflow is configured for GitHub-hosted Ubuntu 22.04/Linux x86_64, regardless
of the user's Mac architecture. GitHub Actions usage is subject to the repository's
own quotas and billing. It has a job timeout and no recurring/scheduled trigger.

## Exact environment and checks performed by the workflow

- Lean `leanprover/lean4:v4.19.0`, official Git commit
  `6caaee842e9495688c1567e78c0e68dbb96942aa`.
- Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`, with every dependency at the
  exact revision from this project's `lake-manifest.json`, not a floating update.
- A positive `import Mathlib` polynomial theorem checked by Lean and an invalid
  `1 = 0` proof required to fail with an unsolved-goal error.
- Those tests before AND after moving the environment to a different directory;
  an additional Lake-based import/proof check after relocation.
- Transfer checksums for the complete compressed bundle and every numbered part.

The official release metadata supplied no SHA-256 digest. The exporter therefore
records the digest it computes, checks the inspected release size, and checks the
executable's full Git revision. This is not a claim of an upstream signed hash.
The artifact producer remains a trust assumption, as with any downloaded compiler.
Licenses remain in the bundle; standalone font files are excluded.

**These are compiler/cache smoke tests, not verification of any Bell theorem.**
The workflow intentionally does not label the mathematical project as proved.

## Getting the output back into the chat runtime

Keep the successful workflow run URL. Its output is a manifest artifact plus
numbered part artifacts. Each part contains at most 400 MiB of payload and is
uploaded as a SEPARATE artifact, below the connected downloader's per-artifact
limit. The workflow has twelve part slots and fails rather than claiming success
when they are insufficient. Missing unused slots only produce upload warnings.

The connected GitHub reader can fetch those artifacts from the run. Alternatively,
the downloaded artifact ZIPs can be uploaded here. Put the manifest ZIP and one
copy of every numbered part ZIP in the same local directory.

Restore and attach the dependencies with the supplied helper:

    python3 environment/restore_environment.py \
      --parts /mnt/data/lean_parts \
      --output /mnt/data/lean419_environment \
      --project /mnt/data/bell_lean \
      --build-project

The helper accepts raw part files or the GitHub artifact ZIPs. It verifies every
part and the complete archive, rejects path traversal and external archive links,
preserves executable modes, checks dependency revisions, and reruns the positive
and negative Lean smoke tests. It refuses an existing output directory or a
conflicting project dependency installation. It needs only Python's standard
library plus the ordinary `git` and `bash` executables.

`--build-project` invokes the existing project build and axiom audit after a
successful restore. It returns the actual build exit status and keeps the log
at `reports/offline-build.log`. Compilation errors should be expected in a
previously uncompiled draft; they must be fixed, not suppressed. Even a clean
subset build does not validate the end-to-end source draft. See `../OFFLINE_RUN.md`
for the fresh-project runner, statement contracts, and per-run reports.

`--extract-only` tests/restores bytes without running a compiler and is explicitly
labelled unverified. It cannot be combined with project attachment or building.

## Tests actually executed in this chat

    python3 -m pip install -r requirements-preflight.txt  # preparation while online
    python3 environment/test_handoff.py

21 tests passed: raw and artifact-ZIP roundtrips, file modes, internal links,
corrupt/missing/duplicate/reordered/oversized parts, wrong pins and hashes,
conflicting manifests, malicious archive paths, external symlinks, special files,
extracted-size mismatch, non-overwriting behavior, explicit unverified restore
status, Python syntax, shell syntax, and exact self-contained workflow embedding.

PyYAML is used only by this local test suite to inspect YAML; it is not required
by the exporter or restorer. No test pretends that a fake executable is Lean.

`make_workflow.py` regenerates the standalone YAML from the inspected source
scripts and `pins.json`. The upload action is pinned to the inspected v4 commit
`ea165f8d65b6e75b540449e92b4886f43607fa02`.
