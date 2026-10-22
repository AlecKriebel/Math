# 11000020: credited nilpotent nonuniqueness

Start with RESULT.md. It gives a source-based negative answer to the explicit nilpotent uniqueness example in Farb Problem 2.19: at least four distinct genus-9 curves have nilpotent **full** automorphism groups of maximal order 128. The examples were already in MSSV's 2002 classification. The proof includes a reconstruction of the classical nilpotent bound.

This is a prior-result correction, not a new discovery. The broader canonical-basepoint programme is not declared exhausted or newly solved. One substantive author-verification turn was used; independent review is pending.

- SOURCE_GATE.md: exact source, prior work, duplicate audit, and limitations
- RESULT.md: complete credited implication, classical bound check, precise scope
- TURN_1.md and TURN_STATE.json: budget and outcome
- source_manifest.json: versions, hashes, and inspected locations; raw sources stay outside the publication packet
- verify.py and verifier_output.json: reproducible arithmetic/signature controls
- manifest.json: frozen packet bindings

Run `python3 verify.py`. Its finite tests do not independently reproduce MSSV's classification or verify that the listed groups occur as full automorphism groups. Those are explicit published dependencies.
