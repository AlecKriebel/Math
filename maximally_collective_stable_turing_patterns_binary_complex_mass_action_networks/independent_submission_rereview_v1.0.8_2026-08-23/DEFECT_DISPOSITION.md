# Disposition of the v1.0.7 findings in v1.0.8

| Prior item | Rereview disposition | Evidence and residual effect |
|---|---|---|
| D1: advertised PDF replay failed; TeX/Python route insufficiently pinned | **Substantially repaired, with one residual minor reproducibility defect** | The exact CPython/scientific stack, TinyTeX/pdfTeX/Biber route, package interfaces, producer, pages, and extractor-robust probes pass current replay and clean builds. However `check_toolchain.sh:78-85` skips the lockfile's `FORMAT` and `LATEX` rows; impossible mutations of either still pass. This changes no mathematics. |
| D2: some direct verifiers could print false `PASS` under optimized Python | **Closed** | All 39 direct entrypoints now have an explicit assertion-mode guard. Every normal run passes; every `-O` run fails closed. |
| D3: verifier roles overstated; cubic full contraction finite only | **Closed at the claimed software-evidence level** | `independent_verifier/README.md:24-53` distinguishes exact, finite, duplicate, floating, and aggregate layers. The new 309-line standalone generic checker verifies the recurrence-to-`R_m+C_m hfrak` bridge symbolically. It still copies printed local formulas and is not a proof of the PDE theorem by itself; the documentation says so. |
| D4: replay rewrote the shipped manifest and could self-certify changed artifacts | **Portable replay closed; new top-level manifest defect found** | The portable replay preserves the downloaded baseline, compares selected exact regenerated artifacts against it, and writes a separate self-consistency manifest. It passes. But `release/sha256_manifest.txt` was generated from a dirty worktree and lists 570 ignored audit/scratch files absent from the immutable tag, so the top-level baseline gate fails. |
| D5: fixed-mass Fredholm/sectorial stability interface too compressed | **Closed** | Main lines 744-808 and Supplement lines 947-1015 give the Fourier blocks, zero-mode restriction, kernel/range/cokernel, `k^-2` inverse, Fredholm index, spectral tail, sectoriality, `H^1` phase space, and branch-gap continuation. The independent PDE audit found the required standard-theorem hypotheses. |
| D6: `m=200` output/provenance/schema/DOI qualifications | **Closed, with naturally stale post-mint metadata** | The `m=200` row is present, stored outputs have evidence/version provenance, and the JSON schema is labeled descriptive. The exact v1.0.7 DOI is recorded correctly. Since the tag, Zenodo minted v1.0.8 DOI `10.5281/zenodo.22074358`; the source still says pending and must be refreshed for submission. |
| Optional: state that the `b=2a` edge is in neither long cycle | **Closed** | The deleted `X_1 -> X_m` edge is correctly identified as belonging to neither complete long cycle in main, supplement, and proof aid. |
| Optional: print the three-by-three core determinant remainder | **Closed** | The displayed Schur complement is exact and has determinant `2a^2b`; the empty-interior `m=3` case is handled directly. |

## New rereview findings

1. **Minor reproducibility — contaminated release-root manifest.** Exact repair:
   generate the baseline from a sorted NUL-safe tracked-file list rather than
   unrestricted `find .`; exclude the manifest itself; test `--check` against a
   fresh `git archive`; then publish a new immutable release rather than moving
   the v1.0.8 tag.
2. **Minor reproducibility — two unenforced TeX lock rows.** Exact repair:
   validate `FORMAT` and `LATEX` against the probe logs and add negative tests
   for mutations of all special lock fields.
3. **Minor reproducibility — detached supplement validation uses two passes.**
   Exact repair: add a third supplement pass or loop until auxiliary files
   stabilize. Two clean passes leave stale TOC page numbers; three reproduce
   the canonical supplement.
4. **Cosmetic notation — `Delta` versus `Delta_m`.** Replace `\Delta` by
   `\Delta_m` at `manuscript/supplement.tex:981`; no mathematical effect.
5. **Submission-compliance blockers, not theorem defects.** The generic
   0.82-inch-margin manuscript has an approximately 6.86-by-9.36-inch text
   area, no review line numbering, no visible keywords or MSC codes, no
   Supplementary Materials index, no PDF cover letter, and unapproved
   funding/competing-interest/AI declarations. These are explicitly admitted
   by `submission/journal/README.md:1-62` and must be completed before upload.
6. **Minor metadata staleness.** Insert exact v1.0.8 DOI
   `10.5281/zenodo.22074358` wherever the package currently says pending, or
   update all submission-facing metadata to the new corrected release DOI.

Items 1-4 require no changed theorem hypothesis, conclusion, endpoint, or
headline. Item 5 changes presentation and submission metadata only. Because
the immutable v1.0.8 package itself cannot be repaired without changing
bytes, the clean solution is a new versioned release after the local fixes.
