# Desktop PDF header detector provenance

Preservation checkpoint: 2026-10-07 06:09:55 UTC.

`desktop_pdf_header_detector.py` was faithfully regenerated from the inline Python
tool-call source that performed the Desktop first-page scan. That contemporaneous
source was available in the agent transcript; it had not been saved as a standalone
script. The preserved file is therefore a parameterized reconstruction, not a
byte-identical original executable or evidence of a second scan.

Preserved detector SHA-256:
`c40545a4fcae31cc3c2df1ebccbfbe8d661e5aa33083bac23bbc55b1375e902d`.

The original run started at 2026-10-07 06:04:23.133657 UTC and finished at
06:04:25.990925 UTC (2.857 seconds). Its ignored metadata artifact is
`sources/archival/desktop_pdf_header_scan_20261007.json`. It reports 733 inventory
paths, 733 unique byte hashes, 733 successful first-page extractions, zero
duplicates, failures, empty first pages, unscanned or excluded entries, and zero
matching candidates. These are the original recorded results, not results from
the preserved script.

## Changes made for preservation

- Required `--inventory`, `--output`, and repeatable `--root` arguments replace
  private paths. Roots are expanded and made absolute. Selection still uses the
  inventory path's lexical containment before validating its realpath. With
  multiple supplied roots, the first lexical match determines the corresponding
  real root; each inventory entry is selected once.
- `--pdftotext` and `--pdfinfo`, defaulting to executable discovery on `PATH`,
  replace machine-specific executable paths. The original constants are now
  configurable arguments with unchanged defaults: 115-second cooperative scan
  budget, six workers, four-second first-page extraction timeout, and 1.5-second
  candidate-metadata timeout.
- The scan is encapsulated in a function with local state and an argument parser.
  The parser validates positive workers, finite positive time limits, and both executables
  to be available. The inline source did not perform these upfront checks.
- Metadata records a `roots` list in place of a single `root`, and the scope
  description refers to explicitly supplied roots. No private research root is
  embedded in the published script's defaults.

The target-title normalization, author and DOI detectors, exact excluded directory
component set, realpath restriction, SHA-256 byte deduplication, first-page-only
text extraction, candidate metadata, exclusive output creation, and aggregate
accounting preserve the inline implementation. Hashing reads file bytes; it does
not extract full PDF text. Only candidate metadata and scan status/counts are
retained, never unrelated extracted page text.

## Verification and limits

The preserved source passed static Python AST parsing. An independent read-only
static review checked the implementation against supplied original matching,
exclusion, containment, deduplication, timeout, and accounting formulas. It found
that newly configurable time limits initially accepted NaN/infinity; preservation
corrected this by requiring finite positive values. The reviewer did not receive
the full original source and did not independently verify full source equality.
No issue affected the original fixed-default scan. Preservation did not run
the detector, reread PDFs, download content, or modify the original scan metadata.
The original budget checks were cooperative: a blocking filesystem read could
exceed the nominal budget, and candidate metadata retains the original minimum
0.05-second timeout. This is not a hard wall-clock cancellation mechanism.

An empty first page counts separately from extraction failure; duplicates inherit
their canonical file's coverage status. No OCR is performed. Matching the title,
author, or DOI anywhere on page 1 is only a candidate signal and can identify a
citation, slide deck, or older paper. Zero matches excludes no target hidden
outside searchable first-page text.

Detector preservation: 100%. Bounded original Desktop scan: 100%. Mandatory
complete-article retrieval/read: 0%; the source-access gate remains unsatisfied.
