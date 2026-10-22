# Read-only reproduction

This packet's own programs use Python3 standard-library exact Fractions. Run from this folder:

    python3 diagnostics.py
    python3 -O diagnostics.py
    python3 -OO diagnostics.py
    python3 fixed_candidate_fraction_check.py
    python3 -O fixed_candidate_fraction_check.py
    python3 -OO fixed_candidate_fraction_check.py
    python3 seal_and_verify.py --verify-only

The diagnostics must report15766checks in each mode. The fixed-candidate program must report the four strict signs, admissibility and positive exact comparison against T. Only the optimization field differs between modes. EXECUTION_RECHECK.json records a second full six-run reproduction matching the saved results.

These commands make no provider requests or mutations. They do not replay global6.1/7.1 certificates and cannot establish the matching global lower bound. Read ANALYTIC_DERIVATION.md for the necessary analytic inference and precise external/numerical inputs; REPORT.md states the conditional verdict.

The read_ledger scripts are separate provider-read programs, not required for offline reproduction. Their two actual runs are captured privately. Do not publish raw spreadsheet captures. No append/action helper is included.

The original1958PDF is stored losslessly as sources/ehp1958.pdf.gz. SOURCE_COMPRESSION.json binds both its compressed and original hashes. Its original byte count is4304732. All21pinned PR blobs are available under pinned_pr with repository-relative paths. Both nested PR MANIFEST.json files are included as ordinary sealed input files; only this packet's own root MANIFEST.json excludes itself.

The source-fetch scripts are historical bounded read procedures and do not need rerunning for offline validation. Exact downloaded payloads, receipts and observed failures are preserved. An alternate primary circle edition was used; its payload is not claimed identical to the old PR pin.
