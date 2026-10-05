# Independent audit package: problem 30005114

Verdict: PASS for the explicitly scoped partial results. General problem: UNSOLVED, five-turn attempt exhausted at 5/5. No novelty or full-solution claim.

Read `AUDIT.md` and `CORRECTIONS_AND_CLARIFICATIONS.md`. `author_frozen/` preserves all seven original author files. Public provenance is in `SOURCE_AUDIT.json`.

With Python 3.10 or newer, run:

    python code/verify_manifest.py
    python code/independent_verify.py
    python author_frozen/code/verify_triangle_removal.py

The recorded outputs are in `results/`. The independent verifier uses only the standard library and does not import the author verifier. To recheck private source inputs, provide your own local copies to `code/verify_sources.py`; its help lists the arguments. Source materials are deliberately absent from this public-safe package.

Finite tests do not replace the analytic proof or the imported concentration theorem. The audit includes no remote writes.
