# Problem 3341: balanced-picture MSO alternation

**Unsolved; five substantive approaches exhausted. No new full-resolution claim.**

The proof artifact reconstructs the known Σ1⊊Σ2 separation directly on binary squares, proves obstructions to tower restriction and naive padding transfers, bounds Boolean-only constructions, and gives a conditional connection to polynomial-hierarchy strictness. Higher balanced alternation levels remain unresolved.

Files:

- PARTIAL_RESULTS.md: exact conventions, proofs, five approaches, and remaining gaps.
- SOURCE_STATUS.md: primary-source and repository checks, access limitations, provenance.
- APPROACH_LOG.md: budget accounting and research checkpoints.
- controls/check.py: self-contained deterministic finite controls.
- CONTROL_RESULTS.json: recorded control output.
- RESULT.json: machine-readable conservative classification.
- SHA256SUMS: frozen package manifest (does not include itself).

Reproduce with Python 3.10 or newer, standard library only, from this directory:

    python3 controls/check.py
    sha256sum -c SHA256SUMS

The control script regenerates CONTROL_RESULTS.json deterministically. It does not prove the infinite hierarchy, enumerate all formulas, compile a general Turing-machine verifier, or establish PH strictness. The mathematical arguments, including the tableau construction, require proof review.

No source PDF, raw corpus, private coordination, or remote credentials is included. No remote mutation has been performed. Publication and any queue edit remain subject to independent audit and the parent gate. The proposal changes only this target's visible Status to unsolved and Turns to 5/5; it does not authorize a Findings change or counter reset.
