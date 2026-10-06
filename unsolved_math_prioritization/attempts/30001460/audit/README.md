# Independent audit for problem 30001460

**Outcome: accepted scoped partial, with one minor wording clarification.**

The quotient construction covers all gl_n/sl_n K-sheets over an algebraically closed characteristic-zero field, with connected K and possibly nonseparated scheme targets. The arbitrary-type nonregular case remains outside the result.

Start with AUDIT.md. PROOF_SUPPLEMENT.md gives explicit scheme-level descent, overlap, and group-choice arguments. CLARIFICATION.patch adds “K-invariant” to one summary sentence in the original RESULT.md; it was not applied to the author freeze.

The author archive is a separate required input, not included here:

- Filename: K_SHEETS_30001460_AUTHOR_SAFE_FREEZE.zip
- Bytes: 16235
- SHA-256: 41b212dc7842cdedf598efebf41976351489115363f30ab2cb599cfa93050e34

## Reproduction

Run the sealed audit inventory check with Python 3.10 or later:

    python -B verify_audit.py
    python -O -B verify_audit.py

A separately supplied trusted receipt should anchor the audit ZIP and verifier hashes. A self-contained manifest is an integrity inventory, not a cryptographic authority for its own code.

Replay the byte-pinned author archive (Python standard library only):

    python -B independent_replay.py --author-archive /path/to/K_SHEETS_30001460_AUTHOR_SAFE_FREEZE.zip
    python -O -B independent_replay.py --author-archive /path/to/K_SHEETS_30001460_AUTHOR_SAFE_FREEZE.zip

Run the independently authored symbolic controls using an existing SymPy installation (reviewed with 1.14.0):

    python -B mathematical_controls.py
    python -O -B mathematical_controls.py

Recheck the complete external corpora, if available:

    python -B identity_recheck.py --catalog /path/to/catalog.json --problems /path/to/problems.json --research-results /path/to/research_results.json

The three programs print only authored test results or public verification metadata. The stored outputs are REPLAY_RESULTS.json, MATH_RESULTS.json, and IDENTITY_RECHECK.json. SOURCE_REVIEW.json records public source metadata and inspection boundaries. No datasets, source PDFs, source extracts, or private coordination material are distributed.

Every checker uses explicit exceptions rather than optimization-sensitive assert statements. Finite checks validate formulas and file identity; they do not prove geometric descent or establish a full solution.
