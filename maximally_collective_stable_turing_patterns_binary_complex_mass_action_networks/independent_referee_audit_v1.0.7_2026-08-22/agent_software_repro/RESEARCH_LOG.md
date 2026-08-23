# Independent software and reproducibility audit log

## 2026-08-22 (initial checkpoint)

- Scope assigned: independent semantic inspection of the complete audit wrapper, all advertised verifier entrypoints, replay scripts, dependencies, mutation behavior, and generated artifacts.
- Preservation rule: notes are confined to this directory; execution is confined to the supplied `working_packet`; `source_snapshot` will not be modified.
- The parent auditor reports that the outer and inner manifests were verified before execution (263 and 198 files respectively). I will retain that as reported provenance and perform independent spot/full verification where feasible.
- Initial inventory obtained with a file listing. The packet contains the paper PDFs, full repository (source manuscript, proof aids, exact data, simulations, figures, 38 verifier entrypoints, tests, audit/generator scripts, stored outputs), a duplicated minimal verifier, review maps, two manifests, environment/provenance documentation, and the complete-audit wrapper.
- Completion estimate: **3%**.

## 2026-08-22 (pre-execution source and environment checkpoint)

- Read in full before author-code execution: `RUN_COMPLETE_AUDIT.sh`, `RUN_ALL_VERIFIERS.py`, `repository/replay.sh`, `minimal_verifier/replay.sh`, all 38 verifier entrypoints, the shared `core.py`/`common.py`/`stable_core.py`/`pareto_core.py` modules, all replay-invoked generators and audits, the test suite, simulations, and figure generators.
- Independently reran both manifests before author-code execution. Outer manifest: **263/263 OK** in 0.04 s. Inner manifest: **198/198 OK** in under 0.01 s. The two reading PDFs match their repository counterparts by the wrapper's declared `cmp` check (to be rerun by the wrapper if prerequisites permit).
- `minimal_verifier/` is source-identical to `repository/independent_verifier/` except for its README and added replay script. It is a portability/convenience duplicate, not an independent implementation.
- Actual host: macOS 26.5.2 build 25F84, Darwin 25.5.0 arm64. `python` resolves through `/usr/local/bin/python` to Apple Python 3.9.6. Available package versions: matplotlib 3.7.1, numpy 1.24.3, pandas 2.3.3, pytest 8.4.2, scipy 1.10.1, sympy 1.14.0. **`pypdf` is missing.** `python3` is Homebrew Python 3.14.6 but has none of the required Python packages.
- External tools: Bash 3.2.57; Biber 2.22; Poppler `pdffonts` 26.08.0; Darwin `sha256sum` 1.0; Apple `awk`, `grep`, `sort`, `find`, and `xargs`; Git 2.38.2. **`pdflatex` is not on PATH and no standard installation was found in the tested locations.**
- Dependencies are lower-bounded only (`>=`) rather than pinned. The replay does not create or enforce a clean virtual environment and does not check exact versions, so dependency resolution is not byte-reproducible. The recorded tested environment is informative but not enforced. Biber on this host is 2.22 rather than the recorded 2.17.
- No executable source accesses the network. The only URLs are citation/provenance links and JSON-schema metadata. No private `/Users`, `/home`, or active `/mnt/data` input path was found; the replay contains a portability scan for `/mnt/data/` references. No missing repository-relative data input was identified from static source inspection.
- Completion estimate: **30%**.

## 2026-08-22 (execution and adversarial checkpoint)

- Literal `bash RUN_COMPLETE_AUDIT.sh` exited 2 at prerequisite preflight (`pdflatex` missing) before a wrapper work root was created. The same was true for the literal full portable replay in a manual disposable copy. These stages are not checked.
- Minimal replay passed in 43.28 s. All 38 advertised verifier entrypoints passed individually in 88.979 s. All 22 tests passed in 7.30 s.
- Source/manuscript and stale-claim audits passed. Numerical provenance passed on supplied and regenerated data. The public PDF audit failed under the default Python because `pypdf` was absent; it passed conditionally after installing pypdf 6.10.0 only into `/tmp`.
- Full non-quick simulation regeneration (15 configurations, three processes) passed in 8.15 s. Exact JSON/tables/exporters were byte-identical. Numerical outputs differed at small solver-scale levels but passed the documented tolerance; 37/49 simulation files differed bytewise.
- All three Matplotlib figure generators passed. Extracted text was identical; the tradeoff raster was pixel-identical, while the two simulation-based figures changed slightly with numerical data/tight bounding boxes.
- Tectonic was used only as explicitly separate fallback evidence. Network figure and supplement rebuilt with identical text/raster but different PDF bytes. Main fallback failed because Biber 2.22 rejected control-file version 3.8. No Tectonic result is counted as the advertised pdfLaTeX/Biber pass.
- Independent mutations of reaction topology and a cubic-source coefficient were rejected. A forced child failure propagated through the 38-runner. A manifest mutation demonstrated that the replay's final self-regenerated manifest checks the current tree rather than a fixed supplied baseline.
- Direct optimized-Python tests reproduced false `PASS` output from assertion-only entrypoints; the orchestrated wrappers correctly reject optimized mode.
- Completion estimate: **92%**.

## 2026-08-22 (final software-referee checkpoint)

- Completed a 38-row semantic inventory separating exact symbolic checks, finite exact regressions, floating regressions, aggregates, and provenance checks.
- Classified duplicate/aggregate inflation, hard-coded/common-source bridges, denominator/domain proof dependencies, exact-vs-float distinctions, stale output differences, document-engine mismatch, and unpinned dependencies.
- Final report: `SOFTWARE_REPRO_FINDINGS.md`; machine-readable results: `COMMAND_RESULTS.jsonl`; literal wrapper output: `FULL_WRAPPER_OUTPUT.txt`.
- No source snapshot was modified, no external communication occurred, and no commit was made.
- Completion estimate: **100%** for the assigned software/reproducibility audit, with the advertised TeX/full-wrapper route explicitly unresolved rather than passed.

## 2026-08-22 (TeX-route follow-up checkpoint)

- Reopened the software conclusion after the root audit supplied disposable TinyTeX environments. The base-host `pdflatex` preflight failure remains an accurately recorded first run, but it no longer limits route coverage.
- TinyTeX 2026.08 initially stopped at the figure stage for missing `standalone`; after the necessary TeX packages were installed, the wrapper reached the PDF audit and failed three version-sensitive assertions (19-page supplement, main positive-`D` extraction, Latin-`u` extraction).
- Full TinyTeX 2022.08/pdfTeX 1.40.24/Biber 2.18 and exact-generation TinyTeX 2022.04/pdfTeX 1.40.24/Biber 2.17 each ran the minimal replay and repository stages 1–8, including all figures and both documents. Both stopped only at the final Latin-`u` semantic check. Exact-environment runtime was approximately 135 s; retained work root is `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/exact-diffusion-referee.bfXanG`.
- Independently confirmed with `pypdf` 6.10.0 that extracted supplement text contains `withu the Latin letter`, not the literal `with u the Latin letter`, and that `with\s*u\s+the\s+Latin\s+letter` matches. A disposable one-condition audit repair passed. The packet source and `source_snapshot` remain unchanged.
- Reclassified the remaining TeX-route failure from an essential/unexecuted reproducibility gap to a **minor false-negative PDF-audit defect**. The exact repair changes no mathematical claim. Modern TeX page/extraction drift and absent lockfiles remain a minor-to-moderate portability limitation.
- Updated `SOFTWARE_REPRO_FINDINGS.md` and expanded the valid machine-readable `COMMAND_RESULTS.jsonl` to 47 rows. Confirmed `source_snapshot` and `working_packet` copies of `audit_pdfs.py` remain byte-identical (SHA-256 `7a7926ae...`).
- Completion estimate: **100%** for the revised software/reproducibility audit.
