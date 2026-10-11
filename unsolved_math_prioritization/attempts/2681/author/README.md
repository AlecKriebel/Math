# Double cover partial research package

This source-free package concerns K3 Problem 1.22, database identifier 2681.
The general conjecture remains unresolved. Start with `REPORT.md`.

## Files

- `REPORT.md`: five mathematical proof attempts, complete elementary derivations,
  precise remaining gaps, source corrections, and public references.
- `APPROACH_LEDGER.json`: scope and outcome of each attempt; source checks and
  computational tests are assigned no mathematical-attempt credit.
- `SOURCE_MANIFEST.json`: public scholarly identifiers, inspection locations,
  and hashes and sizes of the inspected source copies. Source documents are
  deliberately absent from this package.
- `verify.py`: Python 3 standard-library-only exact checks of algebraic support.
- `verification.json`: deterministic saved output from the checker.
- `REPLAY.json`: results of local normal and optimization-mode replays.
- `MANIFEST.json`: sizes and SHA-256 values of the other package files.

## Reproduce the checks

From this directory:

```sh
python3 verify.py > verification.rerun.json
cmp verification.json verification.rerun.json
python3 -O verify.py > verification.optimized.json
cmp verification.json verification.optimized.json
python3 -OO verify.py > verification.double-optimized.json
cmp verification.json verification.double-optimized.json
```

The checker needs no source corpus, PDF, dataset, network connection, external
Python package, or knot-theory software. It does not use `assert` statements, so
its validation does not disappear under Python optimization.

Passing the checks does not prove the knot conjecture, verify the imported
topological theorems, independently recompute the published knot signatures, or
realize the abstract linear-algebra models by knots or manifolds. The report
states these distinctions explicitly.

## Status

Five genuinely different mathematical routes were attempted. There is no claimed
full proof or counterexample. The algebraic reductions are conditional on their
stated hypotheses. No third-party source text, source PDF, dataset contents, or
private coordination material is included.
