# Exact reproducibility artifacts

This directory contains only the exact computational artifacts used by the
minimum-setting classification. Numerical searches and conjecture-generation
scripts are deliberately excluded from the proof runner.

## `three_by_two_separation`

This suite checks the explicit rational \(3\times2\) Bell functional, the
simple and strengthened algebraic qubit-POVM strategies, and the finite
algebraic identities used in the global fixed-qubit PVM upper bound.

The verifier reads its coefficient and strategy files relative to its own
location, so it does not depend on the caller's working directory.

## `two_by_two_closure`

This suite checks the exact algebraic identities used by the residual
\((2,3)\)-by-\((2,3)\) closure proof. It also includes a rational constructive
simulator for the rank-zero stratum and a machine-readable summary of the
central formulas.

The symbolic verifier is a certificate/regression layer for the algebraic
identities. The universal convexity, duality, architecture-reduction, and
rank-stratification arguments remain human-readable proofs in the manuscript.

## Running

From the publication directory:

```sh
./run_all.sh
```

The runner uses the repository's adjacent `.venv` when present, otherwise
`python3`. Set `PYTHON=/path/to/python` to override that selection.

The runner:

1. checks Python and the pinned SymPy version;
2. verifies every exact source artifact against `SHA256SUMS.txt`;
3. runs the exact \(3\times2\) separation verifier;
4. runs the exact \(2\times2\) closure verifier;
5. runs the rank-zero rational simulator.

It performs no dependency installation and makes no network requests.
