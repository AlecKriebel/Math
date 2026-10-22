# Inequivalent trisections: 2991 / KP-4.115

- `PART_A_PROOF.md`: complete proof of a diffeomorphic/non-isotopic pair on the spin of L(8,3), including sector permutations and minimal genus.
- `PART_A_INDEPENDENT_AUDIT.md`: independent mathematical acceptance of that proof's literal part-(a) scope.
- `REPORT.md`: exact target normalization and all five substantive approaches; part (b) remains unresolved.
- `RESULT.json`: machine-readable claim and scope boundaries.
- `SOURCE_METADATA.json`: primary-source titles, public URLs, inspection records, byte counts and SHA-256 fingerprints. No source text or PDFs are included.
- `CORPUS_BINDINGS.json`: independently rehashed corpus metadata and exact target-join results. No dataset content is included.
- `verify_exact.py`: standard-library-only finite algebraic checks with always-active errors, useful negative controls and no default writes.
- `FROZEN_MANIFEST.json`: immutable-candidate file bindings, excluding this self-referential manifest.

Run `python verify_exact.py`, `python -O verify_exact.py`, and `python -OO verify_exact.py`. The commands print JSON to stdout. `--output /existing/external/directory/result.json` is optional, rejects paths inside this candidate, and refuses to overwrite an existing file. `--inject-fault multiplier`, `surjectivity`, `matrix`, and `expected-count` must each fail even under optimization.

The code verifies arithmetic and matrix consistency only; it does not certify smooth topology. No novelty claim is made. No part-(b) solution, simply connected part-(a) example, or distinction after arbitrary stabilization is claimed. The complete proof of (a) and partial report of (b) must be kept separate when describing the result.
