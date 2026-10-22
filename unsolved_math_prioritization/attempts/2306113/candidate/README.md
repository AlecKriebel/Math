# Sigma-neighborhood counterexample candidate

Start with PROOF.md. It gives an explicit degree-10 perturbation and an elementary univalent slit-map composition. The main exact certificate establishes a counterexample for the displayed symmetric Sigma definition. The source contains malformed delimiters; identifying the intended original formula is a separate acceptance dependency.

This is AI-assisted authored mathematical work, pending independent review. It is not human peer review, formal theorem-prover verification, or a novelty certificate.

## Files

- PROOF.md: full analytic argument, exact witness, arithmetic and all-circle covering proof
- COUNTEREXAMPLE.json: exact rational witness
- verify_counterexample.py: standard-library exact arithmetic checker; no assert-based acceptance
- CERTIFICATE_RESULT.json: expected exact successful output
- replay_controls.py: externally pinned, read-only, genuine-nonroot normal/-O/-OO replay and malformed-input controls
- APPROACHES.md: five mathematical approaches and precise limitations
- SOURCE_METADATA.json: public bibliographic/retrieval metadata; no source documents or copied source passages
- search_loewner.py: optional floating-point discovery code; never used by the proof checker
- MANIFEST.json: closed inventory and SHA-256 values; obtain its pin independently

- ALTERNATIVE_REPAIR.md: the same witness under the specifically stated inner-absolute-value repair, with an exact whole-disk covering proof
- verify_alternative.py and ALTERNATIVE_RESULT.json: its exact companion checker and expected output

The companion theorem does not alter the meaning of the main symmetric theorem or certify the source author’s intended syntax.

## Basic replay

From this directory, run:

    python3 -I -B verify_counterexample.py COUNTEREXAMPLE.json

The verifier requires only Python's standard library. Its PASS validates the exact coefficient calculation and arithmetic certificate; read PROOF.md for why these imply the global mathematical statements.

For the full control replay, make a fresh packet copy with directories mode 0555 and files mode 0444, and execute as a genuine nonroot user. Independently verify the driver SHA-256 before executing it. Supply the independently obtained MANIFEST.json SHA-256:

    python3 -I -B replay_controls.py /absolute/path/to/readonly_packet --manifest-sha256 EXTERNAL_PIN

The driver checks the closed inventory, actually attempts writes and requires PermissionError, runs normal/-O/-OO under a hostile working directory/Python environment, tests rejected inputs, and rehashes all files afterward. The permission test is process-level read-only behavior; it does not claim protection from a malicious owner who changes modes, root, concurrent file substitution, or resource-exhaustion attacks.

The optional search needs NumPy and SciPy; versions are recorded in SOURCE_METADATA.json. Its unsuccessful or successful optimizer flags do not affect the exact proof.
