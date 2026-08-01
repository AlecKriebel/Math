# Four-Dimensional Borsuk Program

This directory contains a first-principles research program to decide whether
every bounded subset of \(\mathbb R^4\) can be partitioned into five sets of
strictly smaller diameter.

The discovery phase deliberately avoids searches for prior Borsuk
constructions, low-dimensional covering results, polytope catalogues,
spherical-code catalogues, and earlier computational searches. A narrow
literature and priority audit begins only after an exact proof or exact finite
counterexample has survived independent verification.

## Acceptance criteria

A negative result must include exact coordinates, exact distance comparisons,
the complete diameter graph, a verified non-5-colorability proof certificate,
and independent verification code. A positive result must give a universal
partition, prove strict diameter reduction in every degeneracy and limiting
case, and verify every finite computation exactly.

## Layout

- `RESEARCH_LOG.md`: timestamped checkpoints and completion estimates.
- `WORKING_PLAN.md`: live route tree, decision gates, and falsification tests.
- `notes/`: mathematical derivations and route reports.
- `search/`: bounded discovery programs.
- `verification/`: independent exact checkers.
- `certificates/`: proof objects only when a candidate reaches certification.
- `paper/`: exposition only after a result survives hostile verification.

The Python environment used initially is
`/Users/alec/Documents/Math/.venv/bin/python` (NumPy, SciPy, and SymPy are
available). Discovery jobs are capped conservatively for a 16 GB Apple M1 Pro
and approximately 23 GB of free disk at program start.
