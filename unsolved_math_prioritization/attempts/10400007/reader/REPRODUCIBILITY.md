# Reproducibility and provenance

## Verify integrity first

Use Python 3.12 with SymPy 1.14.0 and mpmath 1.3.0 for the recorded computational environment. The mathematical source reports are readable without those dependencies. Dependencies are not vendored, and the checkers make no network requests.

    python -I -B verify_package.py
    python -I -B verify_package.py --manifest-sha256 HASH_FROM_ARCHIVE_RECEIPT
    python -I -B run_checks.py
    python -I -B check_tamper_controls.py

The first command verifies canonical JSON, the exact file and directory set, regular-file restrictions, every byte count and every SHA-256 value. The second also checks an external manifest pin. Without a separately trusted pin, a malicious replacement of both payload and manifest is not excluded; the manifest is not a signature.

The separate archive receipt pins the exact root manifest and deterministic archive. The root manifest excludes only itself; nested historical manifests are ordinary hashed payload files. Original/public identities explain adapted copies. Historical audit manifests retain their original reviewed-input hashes rather than claiming those originals are byte-identical to every public edition. [Audit bindings](AUDIT_BINDINGS.json) records which historical inputs have included public counterparts and which supporting original is represented only by its verification identity.

## Self-contained finite replay

The replay wrapper copies the complete package into a temporary directory for each execution, removes inherited Python optimization/path settings, and executes every selected checker with `-I -B` in normal, `-O`, and `-OO` modes. It checks exact retained outputs, cross-mode equality and that the source payload was not modified. The isolated Floer wrapper explicitly loads its bundled sibling implementation rather than using an ambient Python import path.

The selected checks cover:

1. PASS1 independent skein/Euler/gauge algebra.
2. PASS1 neutral graph complexes.
3. PASS1 Floer specialization algebra.
4. PASS1 independent finite Jones examples.
5. PASS2 independent Blanchfield, relative-factor, normalization and spectral-support algebra.
6. PASS2 enriched-pairing and four-particle incidence matrices.
7. PASS2 local relative computation and high-precision SU(2) diagnostics.
8. PASS2 exact planar Floer generators, gradings and forced-arrow algebra.
9. PASS2 independent Floer fibers, using the included derived grading baseline.
10. PASS2 exact cyclotomic SU(2) calibration at levels 1–12.

There are ten selected checker entry points and thirty executions per full replay. The local descent checker contains numerical diagnostics, explicitly labeled as such; the separate cyclotomic calibration uses exact quotient-field arithmetic. Only the published mathematical arguments establish all-knot, all-genus and naturality statements.

`CHECK_REPLAY.json` is the recorded result. It records dependency versions, stdout identities, artifact/baseline matches, optimization-mode agreement and the external-input limits. The package adaptation replacing assertions in the local descent checker keeps its checks active under optimized Python; the equations and retained result are unchanged.

## Two tests require external source inputs

The public package is not a self-contained offline replay of these two tests:

- `pass2_validation/check_pd_k11n42.py INPUT_JSON` needs the separately sourced K11n42 fixture with keys `PD`, `TREFOIL`, and `table_jones`. The reviewed fixture was 874 bytes, SHA-256 `8902d73feb07f44aa1bc13a39e29e2ac0a9a2957254ab78132b99799c8e8a266`. Its public source is [Knot Atlas K11n42](https://katlas.org/wiki/K11n42). The retained [derived result](pass2_validation/K11N42_REPLAY.txt) contains computed invariants and input verification metadata, without the copied fixture.
- `pass2_configuration/check_higher_rank_kt.py --input INPUT_JSON` needs a separately sourced Wada representation/presentation fixture. The reviewed fixture was 1,046 bytes, SHA-256 `d441e8606b116f7994fd9b5e6f166ff656fe9c2bfe2b0d56c7ae2c40148acd24`. Its public source is [Wada's paper, §6](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/wada.pdf). The retained [derived result](pass2_configuration/HIGHER_RANK_KT_CHECKS.json) and [source ledger](pass2_configuration/SOURCE_LEDGER.json) record the computation and identity.

Both public checkers require explicit input arguments and have no fallback path to an excluded fixture. The self-contained wrapper checks that they fail closed when called without those inputs; it does not claim to rerun their mathematics. Reconstructing a source transcription may change its byte hash even when the mathematical input agrees; exact receipt reproduction requires the hash-identified transcription. No network fetch or hidden local source access is performed.

## Tamper controls

Fifteen disposable-copy mutations are tested under all three Python optimization modes: changed bytes, same-size changed bytes, deleted file, added file, added directory, symlink, FIFO, unsafe path, duplicate path, manifest self-entry, wrong byte count, wrong hash, noncanonical JSON, duplicate JSON key and wrong external pin. All must fail verification. These are integrity controls, not proof-correctness tests.

## Deterministic archive

The public tar.gz contains regular files under `public/` only, in sorted order. Ownership, mode 0444, timestamps and gzip timestamp are fixed. The sealing script rebuilds the archive twice and compares the bytes, restores it in a fresh directory, checks every byte against the source payload, and reruns integrity, the finite replay and tamper controls there.

No copied PDF, extracted source text, source dataset fixture, cache, draft or coordination file is part of the public payload. This build makes no repository change or external publication.
