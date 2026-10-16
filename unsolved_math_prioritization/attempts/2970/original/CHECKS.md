# Reproduction and validation

All checks below passed on 2026-10-08. These are verification work, not additional mathematical approaches.

## Exact computation

`verify.py` uses Python's standard library, integers, and `Fraction`. All logical checks use the always-active `require` function and raise `RuntimeError` on failure. No check relies on a Python `assert` statement.

- Normal execution: passed
- `python -O verify.py`: passed; byte-identical JSON output
- `python -OO verify.py`: passed; byte-identical JSON output
- Repeated output comparison with `verification_results.json`: identical
- Complete finite Hurwitz-orbit closure: 216 and 144 elements, disjoint
- Canonical lift product checked on every element of both orbits: I and −I respectively
- Parameter identities at r=2 through 31 and pencil arithmetic at k=1,2,4,8: passed

The report gives symbolic proofs for its all-parameter claims. The finite range is an error check, not induction or a replacement for those proofs.

## Fail-closed check

A disposable copy was changed by replacing matrix A with the identity matrix. Normal, `-O`, and `-OO` execution all failed with the intended `RuntimeError`, exit code 1. The published script was not mutated.

## Read-only execution

A disposable directory was given mode 0555 and its script mode 0444. Running as non-root effective UID 1000 from that directory succeeded under normal, `-O`, and `-OO` execution. Outputs were redirected to external temporary files and matched the saved output exactly. The script itself writes only to standard output and creates no local state.

## Scope check

The finite-group example certifies a counterexample to a general cancellation implication. It is not an encoding of the Horikawa monodromies. The lattice computations do not prove that a marking is intrinsically preserved. The sphere calculation is smooth, with no unsupported claim about canonical-symplectic representability. The common-degeneration counterexample uses even r and is expressly outside the homotopy-equivalent target.

The public files contain authored mathematical analysis, authored executable checks and outputs, and public scholarly verification metadata. They contain no copied PDFs, source extracts, external datasets, or coordination records.
