# Degree Bounds for Degenerate Herman Rings

Problem 30001391 / OWR-4137-007. Recommended disposition: **unsolved** for the intended unrestricted periodic target.

The investigation completed five materially distinct approaches. The strongest author candidate is a restricted pole-count theorem: at most d-1 individually invariant Julia-set Jordan curves with irrational-rotation dynamics that are not rotation-domain boundaries. The proof is in PARTIAL_PROOF.md and requires independent audit. Applying it to f^L gives d^L-1, so it does not provide a bound depending only on d for curves of unrestricted period.

Other scoped results: at most one periodic spherical circle with irrational rotation dynamics; a 2d-2 bound for curves containing critical points; and precise obstructions to analytic-linearization and deformation-dimension arguments. None is claimed novel.

A separate source-scope note explains why a literal reading of an omitted exclusion in the 2009 definition admits uncountably many Siegel-disk level curves already in degree two. The surrounding source context already discusses those examples, so the note is not presented as a solution of the intended problem.

## Read first

- SOURCE_GATE.md: exact source and counting conventions
- PARTIAL_PROOF.md: restricted proof candidates and failed-route deductions
- LITERAL_SCOPE_COUNTEREXAMPLE.md: definition warning, not an intended-target solution
- APPROACH_LOG.md: five attempts and exact remaining gaps
- VALIDATION_LIMITS.md: what computations and source searches do not prove

## Replay

Use Python 3.10 or later with the standard library:

    python verify.py
    python verify_manifest.py

CONTROL_RESULTS.json is the expected finite-control output. No downloaded article, full-text extraction, dataset corpus, or private coordination inventory is included in this packet. Source URLs and hashes are in SOURCE_MANIFEST.json.
