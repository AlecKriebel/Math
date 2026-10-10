# Problem 7000022: independent audit

Verdict: **PASS for the frozen partial-results investigation. The full target is unresolved.**

Read `INDEPENDENT_AUDIT.md` for the claim-by-claim review and limits. No substantive correction is required. The five-approach disposition remains exhausted.

Replay the independent checks with Python 3.10 or newer:

`python3 independent_verify.py`

Optionally compare against the author's saved certificates:

`python3 independent_verify.py --author /path/to/geometry_7000022`

Both forms reproduce the supplied `INDEPENDENT_CHECK_RESULTS.json` byte for byte. The second additionally prints the author-certificate cross-check results. Neither command imports the author verifier or reads external source corpora.

`FROZEN_INPUT_MANIFEST.json` identifies the exact nine-file input. `AUTHOR_REPLAY.json` records the isolated author replay. `SOURCE_AUDIT.json` records source verification and bounded inspection. `MUTATION_RESULTS.json` records six rejected implementation mutations. `AUDIT_MANIFEST.json` hashes every other file in this package. No source contents are included.
