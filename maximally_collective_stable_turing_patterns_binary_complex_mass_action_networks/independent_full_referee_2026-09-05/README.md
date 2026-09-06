# Fresh independent referee audit

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md) and [AUTHOR_ACTIONS.md](AUTHOR_ACTIONS.md). The recommendation is minor revision, with submission held pending concrete corrections and unfinished build checks. This audit concerns immutable commit `6f68ad3e795c239e452206c84ce4ce331386a094`; it does not silently certify later revisions.

The dedicated algebra, PDE, software and document folders preserve review narratives, independent scripts, exact outputs and mutation witnesses. Source snapshots, rendering caches and disposable execution copies are ignored to avoid republishing redundant artifacts. The current manuscript was not edited. All external-source citations are in the narrative reports; nobody was contacted.

## Reproduce the new evidence

From this audit directory in a clone retaining the recorded Git commit:

```sh
python3 restore_snapshot.py
```

This reconstructs an absent `source_snapshot/` and checks all 1,109 recorded file hashes. If it already exists, the script only checks it and fails on a mismatch. It does not repair an existing directory. Git-archive container bytes can be implementation-sensitive; the recorded per-file inventory is also preserved for independent inspection.

The independent exact scripts require SymPy 1.14.0. PDE numerical probes also use NumPy (2.0.2 in the independent PDE run). Run with ordinary, unoptimized Python. The exact checks rely on rational arithmetic; NumPy spectra are supplementary floating estimates. Execute each from its own folder:

```sh
python independent_algebra_check.py
python boundary_stress_check.py
python crosscheck_near_threshold.py
```

The PDE folder analogues are `independent_checks.py`, `generic_gauge_independent.py`, and `near_threshold_independent.py`. Their retained JSON/text outputs state scope. The latter near-threshold script was independently cross-checked by the separately implemented algebra script; neither imports project verification helpers.

To reproduce R1 directly without the software audit's host-specific orchestration, run from this audit directory using a Python interpreter with the project's symbolic dependencies:

```sh
python check_certificate_reader.py
```

It copies only the minimal verifier into a temporary directory, adds the two negative monomials, and records false acceptance by both the direct checker and minimal aggregate. Exit zero in this default witness mode means **the defect was reproduced**, not that the manuscript passed validation. After repair, use `--source /absolute/path/to/repaired/project --expect-rejection`. [ROOT_CERTIFICATE_READER_WITNESS.json](ROOT_CERTIFICATE_READER_WITNESS.json) records the root reviewer's separate reproduction.

`documents/check_table_spacing.py` requires Poppler's `pdftotext` and reproduces the recorded table-collision witness. Its success likewise identifies a known defect. Visual judgment is documented separately and was confirmed by two reviewers; semantic text equality is not a layout test.

The larger `software/audit_driver.py` records the actual host paths, environment, command ledger and disposable setup used in this review. Its scratch toolchain and temporary dependencies were removed after storage exhaustion. It is an inspectable record/reproducer requiring environment setup, not a one-command portable installer. Consult [SOFTWARE_REPORT.md](software/SOFTWARE_REPORT.md) for all failures, skips and actual completed stages. In particular, no full actual-TeX portable replay, detached build completion or historical lineage replay is claimed.
