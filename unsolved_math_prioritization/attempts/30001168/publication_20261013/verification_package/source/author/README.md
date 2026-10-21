# Weighted Yamabe heat-trace comparison: dimension-three counterexample

Problem: OWR-3389-021 / 30001168, rank 821.

Result: an authored full counterexample to the statement quantified over
n≥3, using a smooth positive normalized weight on the round S³.
The constructed scaled trace exceeds 0.65 at a specified time; an exact
certificate bounds the round scaled trace below 0.645 at every time.

Status: author-complete mathematical candidate, awaiting fresh independent
adversarial review. This is not a claim of established literature priority.

Files:

- `PROOF.md`: full smooth construction, min–max comparison, normalization,
  round all-time bound, and explicit scope.
- `certificate.py`: standard-library, exact-rational arithmetic certificate.
- `RESULTS.json`: reproducible output of the certificate.
- `SOURCE_METADATA.json`: public bibliographic and verification metadata only.
- `APPROACH_LOG.md`: one substantive approach and its stopping reason.
- `verify_bundle.py`: strict inventory, byte-count, hash, and output verifier.
- `MANIFEST.json`: frozen inventory of the authored files.

Run from any directory:

    python -I -B /path/to/verify_bundle.py
    python -I -B -O /path/to/verify_bundle.py

No external packages or network access are required for replay. Neither
PDFs, source extracts, dataset contents, nor private coordination records
are included. The adjacent n≥4 monotonicity problem is not resolved or
counted by this submission.
