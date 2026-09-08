# Independent v1.0.11 release audit

Target: commit `137ffa9f1a340f621651395ad0236cf1bdadb51c`, tag `maximally-collective-stable-turing-v1.0.11`.

## Conclusion

**The previous J1 journal-layout and warning-gate finding is closed. No new substantive release, build, or reproducibility defect was found.** The five prior warnings are absent from fresh builds, and the actual packaging path now rejects the exact old journal-only overflow witness before copying the bad PDF or changing any sealed bundle.

This conclusion covers the release lane. It does not claim that passing these tests proves every mathematical statement or rejects every possible malformed certificate; those are separate referee lanes.

## Current-release validation

| Check | Fresh result |
|---|---|
| Preserved source versus fresh git archive | All 1,868 files agree exactly |
| Tracked release manifest | All 1,867 entries match; complete archive coverage except the manifest itself |
| Initial portable manifest | All 216 entries match |
| Seven current bundles | Hashes, ZIP integrity, and relative member paths pass |
| Regenerated bundles | All seven ZIPs reproduce the released bytes |
| Tested toolchain | CPython 3.9.6 and pinned Python packages; pdfTeX 1.40.24 / TeX Live 2022; Biber 2.17 |
| Regression/mutation suite | 39 tests passed, no skips |
| Direct verifiers | All 39 pass |
| Optimized-Python controls | All 39 reject explicitly with assertions disabled |
| Complete symbolic aggregate | Pass |
| Minimal replay | Pass |
| Full portable replay | Pass, including all current numerical runs, provenance, figures, and canonical documents |
| Detached submission sources | Three clean builds pass: bioRxiv, arXiv, journal |
| Detached PDF agreement | All six main/supplement text streams equal the intended shipped PDFs |
| Final detached log checks | All six document logs and the fresh cover-letter log pass the shared checker |
| Replay baseline preservation | Initial 216-entry manifest unchanged; regenerated 218-entry self-manifest independently verifies |
| Remote tag | Annotated tag dereferences to the reviewed commit |
| Actual remote assets | All nine downloaded assets match their declared SHA-256 and the target source bytes |

The full portable replay ran with `FINAL_RELEASE_QUICK` unset. Its fresh numerical output contains the 15 published base/refinement cases at dimensions 3, 5, and 8. The provenance audit reports `NUMERICAL_PROVENANCE_PASS` and maximum refinement relative difference `1.4095038570570294e-08`. These are reproductions of the existing illustrations, not new scientific data or an all-dimensional proof.

The public [v1.0.11 release](https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.11) was reported published at `2026-09-07T05:08:21Z`. Its annotated tag object is `6c7864b6a7c2f5fef95dd603e3fcfeb78d570114`; dereferencing gives the target commit above. The nine assets comprise the two canonical PDFs, three submission-source ZIPs, one data ZIP, and three current audit-packet ZIPs.

Compact evidence is in `INTEGRITY_SUMMARY.json`, `RELEASE_ASSET_INTEGRITY.json`, `REMOTE_TAG.txt`, `PINNED_PYTHON_ENVIRONMENT.json`, and `PREFLIGHT_CONTROLS.json`. `COMMAND_RESULTS.jsonl` and `logs/` preserve fresh commands, timestamps, exit codes, and outputs. No new dependency installation was required.

## J1: actual layout repairs

The previous final logs recorded two manuscript and three supplement overfull boxes. All six current detached main/supplement logs now contain **zero** occurrences of the shared policy's undefined-reference/citation or overfull horizontal/vertical-box warnings. Fresh clean logs are retained under `logs/clean_*.log`; `DETACHED_FINAL_LOG_WARNINGS.json` summarizes them. The fresh journal cover-letter log is also clean.

Direct Poppler coordinates independently confirm that the four material old overflow witnesses now fit within the horizontal journal text interval `[90,522]` PDF points:

| Repaired content | Current page | Previous rightmost extent | Current matched rightmost extent |
|---|---:|---:|---:|
| Main verifier command | 17 | 557.31 | 397.20 |
| Supplement verifier command | 14 | 581.11 | 387.07 |
| Contrast table's last-column values | 19 | 538.77 | 516.19 |
| Reference-coefficient rational display | 20 | 570.80 | 382.34 |

The former fifth 1.66727-point warning is removed by splitting the operator and constrained-space definitions in the journal mode. Root visual proofreading independently examines that split and the rest of the pages. The quantitative matched-word evidence above is recorded by `measure_journal_repairs.py` in `JOURNAL_REPAIR_COORDINATES.json`; it is not a claim that all glyph geometry can be characterized by a single rightmost coordinate.

The seven main deliverable PDFs retain a total of 96 pages: 19 canonical manuscript, 19 canonical supplement, 3 theorem summary, 6 proof skeleton, 24 journal manuscript, 24 journal supplement, and 1 cover letter. `PDF_PAGE_COUNTS.json` records these fresh counts. The canonical preprint files also compile without the selected warnings.

## J1: shared gate and actual negative controls

`release/audit_tex_logs.py` now rejects missing and empty logs, undefined-reference/citation warnings, and both overfull hboxes and vboxes. The package scripts call it at the relevant acceptance points:

- `release/refresh_packages.sh:37` checks canonical manuscript, supplement, theorem summary, and proof skeleton before PDF auditing/staging.
- The generated portable replay uses the same checker (`refresh_packages.sh:329`) after its four canonical document builds.
- `refresh_packages.sh:463` checks the detached journal main/supplement logs before PDF copying at lines 467–468.
- `refresh_packages.sh:479` checks the cover-letter log before PDF copying at line 481.
- `release/one_command_replay.sh:180` checks its canonical builds; its detached three-source-package loop calls the checker at line 255 before semantic acceptance. The full historical-route loop was inspected in source, not represented as dynamically executed in the absence of its required archives.

Independent tests went beyond the shipped synthetic CLI control:

| Control | Fresh outcome |
|---|---|
| Feed the two old clean-build logs containing all five actual v1.0.10 warnings to the new checker | Rejected |
| Clean log; hbox; vbox; reference/citation warning; aggregate undefined-reference/citation messages; missing and empty log | Clean accepted; all eight bad cases rejected |
| Exact prior journal-only zero-height overflow witness through real `refresh_packages.sh` | Rejected before journal PDF copy; all seven bundle hashes and accepted journal PDF unchanged |
| Journal-only actual overfull vbox through real refresh | Rejected before journal PDF copy; all seven bundles and accepted journal PDF unchanged |
| Cover-letter actual hbox overflow through real refresh | Rejected before cover PDF copy; all seven bundles and accepted cover PDF unchanged |
| Canonical actual hbox overflow through real refresh | Rejected before acceptance/staging; all seven bundles and accepted journal PDF unchanged |

`check_log_controls.py` contains the exact mutations and assertions. Each action writes a separate `*_RESULT.json`; original v1.0.10 warning logs are retained in `prior_warning_logs/`. The package script's own `--journal-negative-control` also passes, but the real refresh invocations above are the stronger evidence that its wiring now protects the copy boundary. A failed refresh can leave disposable build/staging files; the controls intentionally claim unchanged accepted target PDFs and sealed bundles, not whole-tree transactional rollback.

## Preflight and explicit limitations

The wrong-toolchain control rejects before any scratch-tree file changes. Altering an exact portable data file, with or without a forged **self-consistency** manifest, is rejected against the unchanged shipped baseline before any tree mutation. This does not claim authentication of an attacker-replaced baseline manifest.

The optional full historical-lineage replay could not be completed because all five required archival inputs are still unavailable. I verified its nonmutating preflight freshly: it names all five missing files, exits 2, leaves every scratch-tree file unchanged, and preserves a deliberately installed archived-success log sentinel. The complete **current portable** replay succeeded without those inputs. `check_preflight_controls.py` and `PREFLIGHT_CONTROLS.json` preserve the distinction.

Google Drive contents, a submission portal, and a preprint server's own TeX toolchain were not inspected. The current PDFs and sources were validated in the release's pinned local environment. An initial output-redirection typo in launching the independent preflight driver prevented that command from starting; it was corrected immediately, and the recorded run completed successfully.

All audit artifacts and disposable builds remain in this independent audit folder. No live source, preserved snapshot, manuscript, tag, release, or Git state was changed.
