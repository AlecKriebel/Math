# Reproduce the finite checks

Requires Python 3 with only its standard library.

Run `python verify_examples.py` from this directory. Its standard output must match `EXACT_CHECKS.json` byte for byte. `python -O verify_examples.py` produces the same output. Passing any argument is an error with a nonzero exit status. The checker uses explicit exceptions rather than removable assert statements.

The three deliberately invalid fixtures test a non-unit edge, a crossing, and adjacent backtracking. Successful finite checks do not certify global configuration-space connectivity. Read `PROOF_AND_GAPS.md` for the continuum arguments and exact unresolved gap.

`SOURCE_AUDIT.json` records only permitted verification metadata, public citations, and inspection history. It does not contain copied source documents or dataset contents. The full source documents and corpus are not required to run this finite checker.

`MANIFEST.json` binds the other eight author files. The external archive manifest additionally binds this manifest and the exact ZIP. This is the author freeze before independent review; acceptance or publication must not be inferred from a successful checker run.
