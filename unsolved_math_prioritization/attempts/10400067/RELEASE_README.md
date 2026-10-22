# Release guide

Start with [REVIEWED_RESULT.md](REVIEWED_RESULT.md). The original problem
remains unresolved after five substantive attempts. The independent audit
passes the scoped partial results only.

The original `README.md`, `RESULT.md`, all five turn files, the author
checkers and all author manifests are frozen historical files. Their bytes
are unchanged. [RELEASE_ADDENDUM.md](RELEASE_ADDENDUM.md) supplies the two
review-requested clarifications without rewriting that history:

1. Polynomial residue invisibility does not imply invisibility after
   dividing the same numerator by an Alexander product. The correct
   fixed-denominator numerator perturbation is Q_Delta H^[J].
2. Zero-framed, strut-free wheeling corrections first affect connected
   graphs with first Betti number at least three, preserving the theta
   sector and its support bound.

`independent_review/` contains the unchanged full audit, manifest, checker
and receipt. The raw remote snapshot is omitted because it duplicates the
18 public author files and is not needed to reproduce the audit.

## Portable replay

From this directory, with Python 3 and no third-party packages:

```sh
python verify_core.py
python verify_reconstruction.py
python replay_independent.py
```

The first two commands reproduce the author receipts. The third recreates
the directory layout expected by the unchanged independent checker in a
temporary directory, verifies its byte-identical output, and prints that
output. It does not change any proof, original checker or manifest.

`RELEASE_CHANGE_MAP.json` records the additive projection, including the
unchanged author and audit files. `RELEASE_MANIFEST.json` hashes the full
projection. These additions are packaging and review clarification, not
additional substantive proof turns.
