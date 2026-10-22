# Reproducing this audit

This directory contains completed evidence. Preserve it as a checkpoint. Reexecution appends receipts, so use a fresh dedicated audit directory with the same parent inputs rather than running over these receipts.

Required existing inputs beside the fresh audit directory are source/ (the exact original 18 files), SOURCE_MANIFEST.json, and private_native/canonical_pair.json. Their external hashes are built into audit_runner.py. The native input is intentionally excluded from the public-safe payload. ROOT_NATIVE_RECEIPT.json is provenance read during initial audit inspection, not a runtime dependency of the harness.

Use an already available Python 3 standard-library interpreter. The observed interpreter here was CPython 3.14.6. No third-party packages, network, installed runtime, Git operation, or scholarly PDF is required. Run audit_runner.py with -I -S -B, then accepted_case_inspection.py with -I -S -B in that fresh directory. The second script loads only function definitions from the reviewed first script and relies on its original positive stdout and controlled startup-hook fixture.

The first harness authenticates inputs, inventories the ZIP, privately copies source, runs original normal and optimized code, records actual raw processes before outcome checks, attributes the 2,896 require calls, and performs the original mutation suite. The second pins and explicitly inspects each accepted false case, reruns it, and isolates five further inner-layer rejection checks. Both reset only their private copied packet; original inputs are read-only.

Review REPORT.md and DECISION.json for the exact assurance limits. PROCESS_RECEIPTS.jsonl records all 61 test processes; raw streams are local under private_tmp and excluded from safe export. ORIGINAL_STDOUT contains actual pristine positive output, and ORIGINAL_CODE contains byte-exact original Python code. The driver receipts cover the harness processes separately. Runtime-discovery probes and their storage limitations are separately documented, including the unavailable exact end time on the delayed-persistence discovery probe.

SAFE_MANIFEST.json includes only safe payload files and excludes itself and private_tmp. It is an inventory, not an external authentication signature; authenticate its identity from the trusted handoff or Git commit. No further finite test can replace the independent global mathematical proof review described in REPORT.md.
