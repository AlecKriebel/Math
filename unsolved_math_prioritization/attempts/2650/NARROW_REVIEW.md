# Narrow independent re-review: 2650 / KOU-21.141

Date: 3 October 2026, UTC.

## Verdict: PASS

The required R1 correction and the nonblocking R2–R3 corrections are properly integrated. The initial HOLD is resolved for the corrected release identified below. The original problem remains **unresolved, exhausted at five of five substantive attempts**. This PASS approves the corrected package as scoped partial progress; it is not a proof, refutation, novelty certification, or machine verification of the original problem.

### Exact review binding

- Corrected release manifest SHA-256: `23a762eb50f83e3e4cec46708b4231e7d1de23a76ef2555098ae30f376533d4f`.
- Original author manifest SHA-256: `93334356491d6719b98b628ebb4b011fcb6438428b46e454935d544702fd1ff7`.
- Preserved initial audit report SHA-256: `5df150120443ae3ae0901407bff19dd2fa402cf10760ea692f655e2faa62b4e4`.
- Corrected payload count: 20 files, plus the manifest.

## Mathematical integration

**R1: PASS.** Attempt 1 now applies Chatzidakis–Zalesskii Theorem 5.1 directly only to a faithful action. The nonfaithful case explicitly factors out its kernel N. A fixed vertex is treated separately. Otherwise N lies in a polycyclic edge stabilizer, making N polycyclic and finitely presented. Quotient vertex stabilizers are coherent by the already proved Lemma Q, maximal stabilizers and their conjugacy classes correspond under quotienting, and quotient edge stabilizers remain polycyclic and finitely generated. Theorem 5.1 and the finite-decomposition criterion give finite presentation of K/N; Lemma E then gives finite presentation of K. The repaired text does not claim an unproved lifted finite graph decomposition. Its dependencies are acyclic and use only results already in the five-attempt package.

**R2–R3: PASS.** Attempts 4 and 5 now use the correct flat-package script filenames. Their scripts and result files remain unchanged. No other mathematical changes occur in those two attempts.

The changes to README, research log, status, verification metadata, and repair notes describe this correction without turning it into a sixth attempt or a full solution. Pre-review “pending” fields record the state at the release freeze; this separate report supplies the subsequent review outcome. The full initial HOLD report and its original status remain historical records, unchanged.

## Integrity and portability

The following were checked independently of the release's own assertions:

1. The corrected manifest matches the supplied pin, and all 20 payload sizes and SHA-256 hashes match its entries. The file inventory is exact.
2. The original author manifest still matches its original pin, and all 15 original payload sizes and SHA-256 hashes match. The original freeze is intact.
3. `AUTHOR_MANIFEST.json` is byte-identical to the original manifest. `INDEPENDENT_AUDIT.md` and `initial_audit_status.json` are byte-identical to the original audit artifacts, including the initial HOLD verdict.
4. The actual changed-file set is exactly the eight entries listed in `CHANGE_MAP.json`; each before/after hash matches the corresponding original and corrected file. Its five added-file entries exactly match the new payload files. All seven designated unchanged author files remain identical.
5. The full corrected release was copied to an independent temporary directory and its portable verifier ran successfully there. It reproduced 128 chain parameter checks, 15 finite lattice systems, 65,536 exponent subsets, and 64 exponent-cover parameters. The resulting files were byte-identical, and neither freeze was modified.
6. The unresolved status, exhausted 5/5 budget, absence of a full candidate, absence of an established novelty claim, and finite-only machine-check scope are retained.

## Scope and disposition

This was a narrow re-review of the specified corrections, provenance, and integration, following the full initial mathematical audit. There was no new literature search, no remote write, no new proof-search attempt, and no alteration of either frozen package.

**Disposition: the initial R1 hold is discharged; corrected scoped package PASS.** The general core-free, higher-rank polycyclic-edge coherence question remains unsolved here. This verdict binds the exact corrected release manifest above; the historical initial audit must continue to be preserved rather than relabeled.
