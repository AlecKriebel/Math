# Independent polygonalization-counting audit

Decision: accept the frozen partial results and bounded checker; the unrestricted problem remains unresolved.

- `AUDIT.md`: mathematical, source and implementation audit with precise acceptance limits.
- `audit_counting.py`: independent rational geometry, exhaustive finite controls and semantic mutations.
- `EXPECTED_AUDIT_RESULTS.json`: complete deterministic output.
- `run_validation.py`: actual-UID/read-only normal, `-O` and `-OO` reproduction runner.
- `receipts/`: complete stdout/stderr captures and execution receipt for all six final runs.
- `FROZEN_INPUT_MANIFEST.json`: all eight frozen authored inputs, including their manifest.
- `SOURCE_AUDIT.json`: public-source metadata, inspection scope and independent retained-byte checks.
- `MANIFEST.json`: exact self-excluding manifest of this authored audit package.

The original eight-file package is required separately. No source PDF or third-party dataset is needed by either checker.

Example, with the frozen author package at `AUTHOR_PUBLIC`:

    PYTHONDONTWRITEBYTECODE=1 python audit_counting.py AUTHOR_PUBLIC

For the full recorded-mode reproduction, first set the audit and author input directories to mode 0555 and all their ordinary input files to 0444. Then, as UID 1000:

    PYTHONDONTWRITEBYTECODE=1 python run_validation.py AUTHOR_PUBLIC EXTERNAL_OUTPUT_DIRECTORY

Use an output directory outside both input directories. The runner does not change input permissions. Python 3.10+ and its standard library suffice. The run is factorial/exponential and intentionally bounded; it is not a complexity result.
