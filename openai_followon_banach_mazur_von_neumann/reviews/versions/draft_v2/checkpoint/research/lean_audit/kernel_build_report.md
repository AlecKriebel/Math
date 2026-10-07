# Independent pinned Lean kernel build attempt

Checkpoint: 2026-10-07T05:16:42.518814+00:00 (2026-10-06, America/Los_Angeles).
Best-guess completion toward independent kernel reproduction: **10%**. The exact source setup is complete; dependency setup, compilation, and axiom interrogation remain unverified.

## Strongest verified result

- The upstream checkout HEAD was `adc7f1241b42e322a6451854ab7e4b4c146bf78a` and its status was clean when read. The upstream path `/Users/alec/Desktop/math` was not modified.
- All **372 OAI modules** in `import_closure.json` were copied into `build/OAI` with their module paths preserved. Each copied file matched the supplied SHA256 digest, and a second post-failure pass again found **zero mismatches**. Detailed digests are in `build/source_verification.json`.
- `build/lean-toolchain` selects `leanprover/lean4:v4.34.1`. The actual local binary reported Lean 4.34.1, arm64-apple-darwin24.6.0, commit `5045d0056413266e57c625dcd7c365b10e377c52`, Release.
- The minimal `build/lakefile.lean` declares only the pinned mathlib dependency `d13f23b723b8a846827a245b89c10fc7d3f11612` and a library rooted at `OAI.Analysis.BoundedHochschild.MainResult`. It retains upstream `autoImplicit := false` and the fixed toolchain setting.
- The available read-only mathlib source checkout at `/Users/alec/Documents/Math/openai_followon_bosonic_capacity/notes/formal_scope/pinned_build/.lake/packages/mathlib` had exactly that HEAD and a clean status. It was not modified.
- The prepared `build/AxiomProbe.lean` imports the actual MainResult and asks for the axioms of `OAI.BoundedHochschild.KadisonRingrose.main_result`, `bounded_primitive`, `vanishing`, and `normal_tracial_primitive`. The latter three names occur in namespace `OAI.BoundedHochschild.KadisonRingrose` in the copied `Main.lean`.

## Exact failed step

From the isolated build directory, the command was:

```text
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update > dependency_update.log 2>&1
```

It exited with code **1**. The preserved log reads:

```text
info: family295_kernel_audit: no previous manifest, creating one from scratch
info: stderr:
fatal: write error: No space left on device
fatal: fetch-pack: invalid index-pack output
error: external command 'git' exited with code 128
```

Before the attempt, the shared APFS volume had about 755 MiB available. It fell to about 116 MiB during dependency resolution, and even a small shell here-document failed because the filesystem could not create its temporary file. No compiled mathlib cache was attempted. Root coordination instructed this build to stop and recover its disposable storage.

Only this build's failed partial Git pack (about 169 MiB) and disposable copied mathlib dependency tree (about 146 MiB before the failed fetch) were removed. The pinned read-only originals were preserved. Afterwards the shared volume reported about **436 MiB available**. All OAI source copies, the probe, setup files, source-verification record, and the original failure log remain. No downloader remains running.

## Scope and remaining gap

**MainResult was not compiled or imported successfully. None of the four `#print axioms` commands was executed. This attempt does not establish kernel reproduction and supplies no observed axiom list.**

The exact source closure contains **123 modules with a direct `import Mathlib`**, so faithful compilation requires the complete pinned Mathlib environment; a slim replacement of `Mathlib.lean` would change the checked input and is not an upstream reproduction.

The precise next requirement is sufficient storage for the exact pinned dependency sources and compiled cache, followed by successful dependency resolution, `lake build OAI.Analysis.BoundedHochschild.MainResult`, and `lake env lean AxiomProbe.lean`, retaining their exit codes and logs. The cache/artifact footprint was not downloaded or measured, and no numerical storage requirement is asserted here. The current build directory intentionally has no copied mathlib package or completed `lake-manifest.json` after cleanup.

No theorem source was edited, no Git commit/push/release was performed, and no other individual was contacted.
