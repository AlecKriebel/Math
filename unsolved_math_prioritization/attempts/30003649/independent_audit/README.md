# Independent verification package

Verdict: PASS. Read AUDIT.md for the exact scope, source-status qualifications, and universal proof audit.

The public witness is intentionally not included. Download the five files at the immutable URLs in input_pins.json into DATA. The checker enforces every SHA-256 and byte count before reading the witness.

Run with Python 3.10 or later:

    python3 PACKAGE/independent_verifier.py DATA
    python3 PACKAGE/adversarial_controls.py DATA
    python3 PACKAGE/integer2_independent.py

PACKAGE can be absolute; all commands work from any current directory. Python optimization does not remove the checks. Independent verifier run times may differ; elapsed_seconds is not a mathematical result.

Methods differ from the freeze: common-denominator field arithmetic; independently bisected root bounds; Laplace-cofactor exhaustive facets; quotient-step integral descent. Programs import only Python's standard library and local independent_verifier.py. No source-package code is executed.

Result files are actual run metadata, never proof inputs. Source byte pins identify the public witness; all mathematical predicates are recomputed. The finite predicates establish the unrestricted-width rational obstruction only in conjunction with the complete mathematical argument audited in AUDIT.md.

No source PDFs, source text, source data, private comparison script, or private coordination material is included. Manifest hashes cover only the safe audit files. Original mathematical attribution remains Sidney Holden for the rational counterexample and Thomas Laffey / Helena Šmigoc for the integral order-two theorem. The separate George Stepaniants Lean formalization was not relied on or rerun.
