# Independent audit for 4400001

Verdict: pass. Recommend `already_solved`, negative answer, with the author's research-turn count retained at 1/5. The complete report is `AUDIT.md`. It verifies the exact two-sided target and the application of Salo's published extension theorem, including inspection of the applicable proof. No substantive correction is required. The theorem is imported as established mathematics; no new theorem or formal certification is claimed.

## Contents

- `AUDIT.md`: mathematical audit, proof inspection, verdict and limits
- `BINDING.json`: exact frozen author archive and all nine input file fingerprints
- `PROVENANCE.json`: fresh versus retained source inspection and access limits
- `RESULT.json`: machine-readable result, author replay and independent counters
- `independent_checks.py` and `independent_results.json`: separately implemented finite controls
- `verify_audit.py` and `MANIFEST.json`: offline replay and byte integrity

## Replay

Run `python3 -B verify_audit.py` from this directory for self-contained audit replay.

For complete binding verification, supply both original inputs:

`python3 -B verify_audit.py --author-dir /path/to/original/public --author-archive /path/to/hochman_4400001_PUBLIC_SAFE.zip`

Python's standard library suffices. The scripts make no network calls and modify no input files. Finite checks do not prove the infinite-space extension theorem.

The public audit excludes source PDFs, extracts, images, raw dataset records, and private material. Its sources are identified by public URLs and fingerprints only. The exact catalog detail page and selected AI corpora remain uninspected. The fresh journal-PDF download failed with 403; the retained published copy was independently hashed and inspected, alongside successful independent publisher-full-text and author-PDF reads. No remote action was performed.
