# Independent audit packet: 30002753

**Verdict: retained exact claims pass; exploratory precision is qualified; problem remains unsolved at 5/5.**

The controlling numerical qualification is in `AUDIT.md` and `EXPLORATORY_RECHECK.json`: the saved n=3 optimizer value differs by approximately 7.27e-9 from an independent evaluation of the saved pair. This does not affect the separately verified exact κ_3<9/10 witness.

## Contents

- `AUDIT.md`: full mathematical and source-scope audit
- `BINDING.json`: original frozen file/archive binding
- `RESULTS.json`: concise machine-readable verdict and limitations
- `AUTHOR_REPLAY.json`: unchanged author-checker replay
- `INDEPENDENT_RESULTS.json`: 187 exact assertions, including nine negative controls
- `SYMBOLIC_RESULTS.json`: 19 supplemental symbolic checks
- `NEGATIVE_CONTROLS.json`: mathematical, byte-integrity, and scope negative controls
- `SOURCE_CHECKS.json`: public-source hashes and independent inspection scope
- `EXPLORATORY_RECHECK.json`: numerical-only high-precision re-evaluation
- `independent_controls.py`, `symbolic_controls.py`, `verify_binding.py`, `check_exploration.py`: reproducible audit code
- `MANIFEST.json`: SHA-256 safe-audit inventory, excluding itself

## Replay

Run `python3 independent_controls.py` from any working directory. It requires only the standard library and imports no author code. Run `python3 symbolic_controls.py` for the supplemental checks; these require SymPy (audited at version 1.14.0).

To rebind against an available original packet, run `python3 verify_binding.py DIRECTORY_CONTAINING_ORIGINAL_SAFE_RELEASE`. To recheck the numerical candidates, run `python3 check_exploration.py PATH_TO_ORIGINAL_EXPLORATORY_RESULTS.json`. The latter is not a rigorous interval or optimality certificate.

All original inputs are preserved. No remote writes were performed. This audit packet contains no public-source PDFs, source extracts, images, raw problem records, raw datasets, or private coordination files.
