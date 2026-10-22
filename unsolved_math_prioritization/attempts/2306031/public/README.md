# Function Theory 6.31: partial rate estimates

- Problem: 2306031 / AMR-022-6031, queue rank 582.
- Recommended status: **unsolved**, **5/5** substantive approach turns.
- Main target: improve Duren's O(1/log n) coefficient remainder for normalized univalent functions under a power-rate radial asymptotic.
- Strongest restricted result: polynomial rates for Re((1-z)^2 f′)>0, with the original class restriction and endpoint logarithm stated precisely.
- Sharp boundary example: a function in S has radial error of order (1-r)^2 but coefficient error exactly 1/(2n). A general o(1/n) conclusion is therefore impossible.

`FULL_PROOF.md` proves the partial statements and states the remaining gap. `APPROACH_LOG.md` records all five families. `SOURCE_GATE.md` and `SOURCE_MANIFEST.json` document provenance and retrieval limits. No full resolution or novelty is claimed.

Run with Python 3.10+ and only its standard library:

    python3 verify.py
    python3 verify_manifest.py

The controls are finite and bounded. They do not verify the infinite theorems, literature completeness, or the original open problem. Third-party PDFs and imported datasets are not included.
