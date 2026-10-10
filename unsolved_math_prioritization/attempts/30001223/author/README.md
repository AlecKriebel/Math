# Simple tops: independent-audit bundle

Read proof.md for the proposed all-odd-characteristic counterexample family and its exact scope. The smallest example is characteristic 3, degree 5, partition (4,1). Only authored material and public verification metadata are included. No source PDFs, extracted source text, dataset records, or coordination material are included.

Run the inventory verifier and supporting calculations with Python 3.10 or later:

    python -B audit.py
    python -B -O audit.py

The verifier checks the strict, flat manifest before launching verify.py. Unexpected files (including caches), directories, symlinks, and other nonregular entries are rejected. No external dependencies, network access, or absolute input paths are used. File-integrity checks are not a mathematical proof; proof.md distinguishes theorem inputs, authored arguments, and finite supporting computations.

This package has not itself undergone independent mathematical review. A fresh reviewer should check the field and parameter scope of the primary report, injective reciprocity, the two-row calculation, and especially the all-rank truncation step. A successful code run is not a substitute for that review.
