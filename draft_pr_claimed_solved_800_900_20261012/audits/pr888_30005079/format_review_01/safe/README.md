# PR888 tool review evidence

These are the explicitly allowlisted review artifacts. Read REPORT.md for the scoped disposition, 42 actual wrapper invocations, separate original-root CLI and in-process observation, and resource-limited failed expectation. No whole-package or mathematical clearance is given.

The control sources are reproducibility designs requiring a fresh review directory, authenticated portable_reviewed.py of the report hash, the 21 pinned original files and external manifest, the explicit metadata/TeX format fixture, the three pinned native corpora, and the exact two wheel files in the original relative layout. Those private inputs and generated fixtures are deliberately absent here. The main script builds from an already independently provisioned private fixture; supplementary scripts extend its receipts. Supplementary setup failed with ENOSPC, so finish_controls.py records the smaller remaining cases. These are not a claim of a self-contained public test package.

Local path prefixes were redacted in safe receipts. CODE_SANITIZATION.json records exact executed-code and safe reproduction-code hashes; the only code replacement is a supplied local workspace path. No original or native bodies, PDFs, wheels, or temporary fixtures are included. SAFE_MANIFEST.json in the review root explicitly lists safe members and excludes itself from its member rows.
