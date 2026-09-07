# Independent v1.0.10 release and reproducibility audit

Target: commit `953c836a12b9d9d474521feb4a96e218c1155203`, tagged `maximally-collective-stable-turing-v1.0.10`.

## Result

Every requested current-release replay and integrity check passed freshly. One bounded presentation/build-gate defect remains in the **journal exports**: five overfull-box warnings occur in clean builds of the shipped sources, and journal packaging accepts them because the new log check covers only the four canonical document builds. The canonical preprint manuscript and supplement do not have these warnings. This is not a mathematical defect, a failed scientific reproduction, or evidence that any current content is clipped off the physical page.

## Fresh qualification evidence

| Check | Fresh result |
|---|---|
| Preserved source versus fresh git archive | All 1,651 files agree exactly |
| Tracked release manifest | All 1,650 listed files match; exact archive coverage, excluding the manifest itself |
| Portable initial manifest | All 214 listed files match |
| Current seven ZIP files | Hashes, ZIP integrity, and safe relative member paths pass |
| Deterministic package refresh | All seven regenerated ZIP files match the released bytes |
| Pinned toolchain | CPython 3.9.6, the tested package versions, pdfTeX 1.40.24 / TeX Live 2022, Biber 2.17 pass |
| Regression and mutation tests | 39 passed, no skips |
| Direct verifier entrypoints | All 39 exit successfully |
| Optimized-Python negative controls | All 39 reject explicitly because assertions are disabled |
| Minimal verifier replay | Pass |
| Full portable replay | Pass, including current-profile numerical regeneration and numerical provenance |
| Complete symbolic aggregate | Pass, both directly and in replay |
| Three clean detached source builds | bioRxiv, arXiv, and journal builds pass |
| Detached source/PDF agreement | All six main/supplement rendered-text streams equal their intended shipped PDFs |
| Regenerated replay manifest | 216 entries pass independently; initial 214-entry baseline remains byte-identical |
| Remote tag | Annotated tag dereferences to the target commit |
| Actual remote release assets | All nine downloaded assets match both their declared digest and the target source's corresponding bytes |

The remote release is [v1.0.10](https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.10). Its annotated tag object is `855ea82dde247c519b0470f2dd8a504db2f8d246`; dereferencing gives the target commit. Publication time reported by GitHub is `2026-09-06T23:56:13Z`.

`audit_driver.py` records commands, time, exit status, working directory, and duration in `COMMAND_RESULTS.jsonl`; individual output is under `logs/`. `RELEASE_ASSET_INTEGRITY.json`, `REMOTE_TAG.txt`, `PINNED_PYTHON_ENVIRONMENT.json`, and `REPLAY_BASELINE_CHECK.json` preserve independent compact evidence. This audit reused the already installed toolchain and packages; no installation was needed.

## Finding: journal layout and warning gate

The following warnings occur in the **unmodified** v1.0.10 source bundles. They are preserved in `logs/clean_journal_main.log` and `logs/clean_journal_supplement.log`.

| Shipped document | Page | Source | TeX excess width |
|---|---:|---|---:|
| Journal manuscript | 17 | `manuscript/main.tex:1008`, verifier command | 33.31522 pt |
| Journal manuscript | 19 | `data/contrast_table.tex:1`, included by `manuscript/main.tex:1101` | 22.83739 pt |
| Journal supplement | 14 | `manuscript/supplement.tex:888`, verifier command | 59.06581 pt |
| Journal supplement | 20 | `data/sign_certificate_tables.tex:65`, polynomial and rational identity in one display | 48.98580 pt |
| Journal supplement | 23 | `manuscript/supplement.tex:1008`, three operator/space definitions in one display | 1.66727 pt |

The configured journal text area runs horizontally from 90 to 522 PDF points. Independent Poppler word boxes confirm substantial margin incursions in the first four cases: the verifier commands reach about 557.31 and 581.11 points, the contrast table about 538.77, and the rational display about 570.80. `JOURNAL_MARGIN_WITNESS.json` records exact affected word coordinates. The final 1.67-point warning is visually much smaller and should not be overstated; normal microtype punctuation protrusion elsewhere also extends slightly beyond the nominal text edge.

The new explicit failure loop in `release/refresh_packages.sh:34` checks only canonical `main`, `supplement`, `theorem_summary`, and `proof_skeleton` logs. The detached journal build at lines 421–447 and cover-letter build at lines 449–460 have no equivalent warning check before copying their PDFs. The analogous final-document loop in `release/one_command_replay.sh` likewise does not cover those detached logs. `audit_pdfs.py --profile journal` checks required text, page counts, fonts, and the four modulus-certificate tables; it does not enforce the full six-inch horizontal text area or generally inspect build warnings. Consequently both the supplied journal PDFs and the current refresh script pass despite these five warnings.

Bounded repair: allow the long verifier commands to break, fit the contrast table inside the journal text width, split the polynomial/rational display and long operator display as needed, and apply one shared final-log check to the canonical, detached journal, and cover-letter builds before their PDFs are copied or packaged. The journal-specific presentation change can remain conditional on review mode. Rebuild the affected documents, inspect these pages, confirm the selected warning pattern is absent from all checked final logs, and regenerate the affected source bundles and PDF evidence. No theorem, certificate, endpoint, or numerical change is indicated by this finding.

For adversarial confirmation, `check_release_controls.py journal_warning` inserts a journal-only zero-height overflowing box and shows that package refresh still exits 0 and seals the altered journal PDF. The output has an additional 550.90533-point warning; `JOURNAL_WARNING_WITNESS.json` and `logs/journal_warning_main.log` preserve the result. This synthetic test supports the coverage diagnosis; the five real shipped warnings above are the primary finding. An initial, taller injected box was rejected by the page-count check because it produced 25 pages, so the page-count gate itself works.

## Other new release hardening: verified

- A mismatching engine lock causes `refresh_packages.sh` to fail before any file in the scratch release tree changes.
- A canonical overfull-box mutation causes refresh to fail before bundle hashes or packages are rewritten. The new canonical warning check is effective.
- Seven intentionally invalid canonical/journal PDF files and poisoned PDF evidence reports are replaced by refresh. Both semantic reports are regenerated; all seven resulting ZIP files are byte-identical to the original release. The changed ordering therefore fixes the stale-evidence problem it was intended to fix.
- Altering an exact data file causes portable replay to reject against the shipped baseline before mutation. Adding a forged self-consistency manifest for that altered data does not bypass the shipped baseline; replay rejects and leaves the entire scratch tree unchanged.

These tests are reproduced by the `preflight`, `canonical_warning`, and `fresh_evidence` actions of `check_release_controls.py`. Their compact results are in the corresponding `*_controls.json` files. The test scripts and witnesses never modify the preserved snapshot or live manuscript.

## Explicit limits

The optional historical-lineage `release/one_command_replay.sh` was **not completed**: its five external archival inputs remain unavailable. With the pinned toolchain present, I verified that its first failure names all five missing archives, exits 2, and leaves every scratch-tree file unchanged, including a deliberately installed archived-success replay-log sentinel. This is a failure-sensitive preflight test, not a substitute for having replayed that historical route. The current full portable route completed successfully and does not consume those archives.

The old `external_audit/full_referee_validation_packet_v1.0.7` tree is historical source provenance. It is not one of the seven current ZIPs or nine current remote assets, so old reader behavior there is not a v1.0.10 packaging defect.

This audit verifies the shipped code, packages, pinned local build, and public GitHub release. It does not claim to have reproduced a preprint service's server-side TeX environment, Google Drive contents, or an actual submission. It does not independently prove that all software tests exhaust all possible malformed certificate inputs; the separate certificate audit addresses additional semantic attacks.
