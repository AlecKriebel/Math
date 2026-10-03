# Reproduce the independent controls

Use Python3 with SymPy1.14.0 available. From this folder run:

    python independent_controls.py
    python negative_controls.py

Both import no frozen candidate module. The first has18432 assertions and the second466. Each emits the JSON preserved in its .stdout file. The candidate early scripts were run from a private byte-identical copy; their actual full outputs are retained separately.

The .receipt.json files bind command paths, times, returncodes, script SHA and full stdout/stderr SHA. The private directory contains downloaded primary PDFs, a candidate copy and the isolated runtime; it is ignored by the local .gitignore. Source receipts distinguish historical and fresh hashes, including the Cambridge download stamp variation.

Read PRE_CANDIDATE_RECONSTRUCTION.md and INDEPENDENT_RECONSTRUCTION.md for all-scale arguments. Finite checks alone do not solve the original tiling question.
