# Multiplicity formulas for Galois-invariant induction

Read REPORT.md for the hypothesis reconciliation, credited resolution, direct multiplicity identification, repeated-factor example, and counterexample to the widened catalogue wording.

The precise p-adic irreducible-generic target is a consequence of Beuzart-Plessis's published theorem. No new proof of that analytic theorem is claimed. The broad catalogue statement is not endorsed. Research turns: 0/5.

## Files

- REPORT.md: authored mathematics and explicit dependencies
- SOURCE_METADATA.json: public bibliographic metadata, PDF fingerprints and inspection history
- CORPUS_FINGERPRINTS.json: full public corpus fingerprints, counts and exact-target match metadata; no dataset contents
- LEDGER.json: chronological accounting
- controls.py and CONTROL_RECEIPT.json: exact finite diagnostics
- verify.py: isolated strict-inventory verifier
- MANIFEST.json: hashes and byte counts of every other packet file

The public directory is the entire author packet. It contains no retrieved PDFs, source extracts, source screenshots, raw datasets, private sources or coordination material.

## Replay contract

Use a trusted Python 3 interpreter and standard library. Obtain the manifest SHA-256 and the verify.py SHA-256 independently from the freeze receipt, verify the latter before executing it, and run:

    python -I -S -B verify.py EXPECTED_MANIFEST_SHA256
    python -I -S -B -O verify.py EXPECTED_MANIFEST_SHA256

A trusted, externally pinned copy of verify.py may instead receive the packet directory as its second argument. The verifier checks a flat closed inventory and all byte hashes before executing a captured, verified controls.py byte snapshot. It compares the computed receipt with the frozen one. It rejects symlinks and extra entries. This is an integrity check under a trusted interpreter and OS, not a hostile-code sandbox or a theorem prover.

The controls alone can be run with:

    python -I -S -B controls.py

They cover 494 synthetic multisets and 3,044 explicit checks across six families. The independent sign enumeration is a combinatorial diagnostic, not a replacement for the period-multiplicity theorem.

## Audit status

This is the author freeze prepared for separate review. No independent review, human review, merge, release or publication is claimed.
