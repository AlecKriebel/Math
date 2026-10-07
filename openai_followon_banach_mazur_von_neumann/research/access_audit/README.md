# Local primary-PDF header detector preservation

Preservation checkpoint: 2026-10-06 23:10:32 PDT (2026-10-07 06:10:32 UTC).

These source files make the bounded local discovery algorithm checkable. They are **faithfully regenerated, parameterized implementations**, not byte-for-byte copies of original on-disk scripts: the original implementations ran as one-off Python commands on 2026-10-07 and were not saved as files. Regeneration uses the execution source preserved in the agents' tool-call history. The original scans and derived inventories have not been rerun during preservation.

Preservation scope: 100% complete once both root-specific detector files and their provenance are present. Complete Roydor journal article/manuscript retrieval and reading remain 0% complete. This preservation task adds reproducibility evidence for an access search, not new source access or mathematical verification.

## Source files and provenance

- `inventory_pdf_paths.py` preserves the final inventory command flags, explicit excluded directory globs, case-insensitive PDF filename suffix, inventory order, per-root counts, and command statuses. Its required root/output arguments replace the two embedded authorized roots and fixed local paths. It normalizes supplied roots with `Path.resolve()`. It prints aggregate counts instead of each root's full status record; that information is still saved locally. Argument parsing and a `main()` entry point are new packaging.
- `documents_pdf_header_detector.py` preserves the actual Documents detector's lexical-root selection, physical-root check, five-byte `%PDF-` signature test, whole-file SHA-256 deduplication, byte-unique first-page extraction, exact regexes, text normalization, candidate-only page count check, queue bound, timeout handling, and aggregate/per-path accounting. Required arguments replace embedded paths, original numeric caps become CLI defaults, and finite-positive argument checks are added. Progress/full-record terminal output is reduced to aggregates; raw first-page text still never enters saved records. Refactoring into functions does not claim a new completed scan.
- `classify_pdf_signature_errors.py` preserves the separate follow-up examination of the first 1,024 bytes of pre-extraction-error files, with signature/LFS-pointer/empty-file classifications and counts. Required arguments replace embedded paths. An explicit physical-root recheck is added because a reusable caller could supply a different scan file; the original error list arose solely inside the already scoped detector. The original follow-up found no PDF signature in all 98 such entries. The follow-up does not extract text or automatically reopen discovery.
- `desktop_pdf_header_detector.py` and `desktop_detector_provenance.md` preserve the independently executed Desktop detector and document its regeneration separately.

The required arguments have no defaults naming any private research folder. The source contains no unrelated local path inventory or extracted page text. Only the exact target's title/author/DOI matching expressions and generic exclusion rules are embedded.

## Bounds and accounting interpretation

The Documents defaults match the executed scan: 180-second scheduling cap, eight-second per-subprocess timeout, six extraction workers, and at most 60 pending byte-unique jobs. The elapsed timer begins after the root-specific inventory is loaded. At the top of each input iteration the cap can stop new scheduling. Hashing a file in progress and already submitted extraction jobs may finish afterward. Consequently the cap is a scheduling bound, not a strict end-to-end wall-clock deadline; the actual scan took 18.61 seconds. No task was left unattempted because of that cap.

Deduplication is by whole-file SHA-256 within each separately executed root, not by filename, size alone, header hash, or a count of matching text. Counts of unique readable headers, empty first pages, failures, and duplicate paths remain distinct. To account for duplicates, map each duplicate's hash to its canonical header record's status. No page-count restriction decides whether a target candidate is eligible. A first-page match is a discovery candidate, not proof of a complete manuscript. An empty or failed extraction remains unresolved rather than counted as an absence result.

The inventory includes `.pdf` filenames that may not contain actual PDF bytes. The original Documents detector required the signature at byte zero, then the separate follow-up checked for a signature within the first 1,024 bytes of the rejected files. Neither step presumes that every PDF-suffixed filename is a valid PDF.

## Dependencies and controlled use

The scripts use Python's standard library plus installed `rg`, Poppler `pdftotext`, and `pdfinfo`. `pdftotext` uses its local default UTF-8 output encoding in the Documents implementation; the Desktop implementation explicitly requests UTF-8. No network, credential, login, download, purchase, external messaging, Git, OCR, or full unrelated PDF-text extraction is part of these scripts.

An operator may inspect the source or request `--help` without scanning. Any new scan needs explicit authorized roots and explicit local output locations. Keep resulting inventories/status records in an ignored local verification directory; do not bundle unrelated per-path metadata in a published supplement. For example, with operator-supplied placeholder paths:

```text
python3 inventory_pdf_paths.py --root AUTHORIZED_ROOT --inventory-out LOCAL_IGNORED_INVENTORY.json --metadata-out LOCAL_IGNORED_INVENTORY_STATUS.json
python3 documents_pdf_header_detector.py --root AUTHORIZED_ROOT --inventory LOCAL_IGNORED_INVENTORY.json --output LOCAL_IGNORED_SCAN_STATUS.json
python3 classify_pdf_signature_errors.py --root AUTHORIZED_ROOT --scan LOCAL_IGNORED_SCAN_STATUS.json --output LOCAL_IGNORED_SIGNATURE_STATUS.json
```

These commands describe use and were not executed as part of preservation. Roots must be authorized by the human and restricted to the intended research scope.

## Original evidence retained separately

Original derived records stay in ignored `sources/archival/`: `local_pdf_header_inventory_20261007.json`, `local_pdf_header_paths_20261007.json`, `documents_pdf_header_scan_20261007.json`, `documents_pdf_header_signature_classification_20261007.json`, and `desktop_pdf_header_scan_20261007.json`. They contain the actual timestamps, private research paths, hashes, classifications, and counts. They are not copied into this source directory or a publication payload.

The factual scan report is `research/local_primary_pdf_header_discovery.md`. This directory preserves its computation rather than replacing the report, inventing a successful retrieval, or altering a manuscript/frozen review. Preservation verification consists only of Python syntax parsing and SHA-256 hashing of these new implementation files; no original PDF scan is repeated.
