# Research log

## 2026-08-27 21:49 PDT — source identification checkpoint

- Goal: assemble the latest local TeX source for exactly four main papers,
  excluding all supplement, technical-summary, clarification-note, historical,
  referee, and frozen-copy TeX sources.
- Inspected the current `main` working tree, per-project Git history, project
  documentation, manuscript entry points, and TeX dependency directives.
- Identified the four canonical main-paper entry points documented in
  `SOURCE_SELECTION.md`.
- Confirmed that all selected source paths are clean relative to Git at
  repository commit `f6f9a1598d760e55efd7b55d137d4d00e8b3545f`.
- Best-guess completion: 55%.

## 2026-08-27 21:50 PDT — assembly checkpoint

- Copied only each entry point and the local TeX/BibTeX dependencies needed by
  that main paper.
- Deliberately excluded every supplement source and all alternative manuscript
  products.
- Remaining work: exact source/copy comparison, dependency-closure checks,
  compilation, and manifest generation.
- Best-guess completion: 75%.

## 2026-08-27 21:52 PDT — validation checkpoint

- Exact comparisons passed for all 36 copied source files.
- Confirmed exactly four document-class entry points and zero
  supplement-named TeX source files.
- Papers 1--3 compiled directly with Tectonic 0.16.9, producing 33-, 20-, and
  26-page PDFs in an isolated temporary directory.
- The exact current K3P source stopped at
  `sections/17_reproducibility.tex:40`; Git history shows the malformed
  `(5\\)-minor` text was introduced in commit `f845f188`. The collection keeps
  that current source byte-for-byte. A temporary validation copy corrected it
  to `\\(5\\)-minor` and then compiled successfully to 38 pages, with no other
  missing source or compilation error.
- The source selection and dependency closure are complete. Remaining work is
  to record checksums and publish the checkpoint.
- Best-guess completion: 95%.

## 2026-08-27 21:53 PDT — completed collection

- Recorded and independently rechecked SHA-256 hashes for all 36 manuscript
  source files in `SHA256SUMS`.
- Repeated the byte-for-byte comparisons after documentation and validation;
  every copied source still matches its selected local original.
- Final inventory: 9 STC/JC files, 2 theta-collision files, 2 K2P files, and
  23 K3P files; exactly four document-class entry points; no supplement source.
- Best-guess completion: 100%.
