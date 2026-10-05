# 5300076: power-law Thurston lifts

**Status: unsolved, 5/5 substantive approaches. Independent audit pending.**

The packet proves global convergence of the lift sequence for a critical orbit of exact period two, for every real exponent greater than one, using a logarithmic contraction. It also constructs nontrivial two-cycles of the conjugated-map sequence with a fixed critical point, while the lifts remain constant. Those are different outputs of the algorithm, so the latter counterexample is not called a solution of the imported lift-convergence question.

Read `RESULT.md` for the complete definitions, proofs, quantifiers, and remaining gap. `APPROACHES.md` records the five distinct routes. `SOURCE_GATE.md` and `SOURCE_MANIFEST.json` record provenance, source scope, and access limitations. The May 2026 entropy-monotonicity preprint is treated as related work, not as a verified global-convergence theorem.

Reproduce author controls with Python 3.10+ and its standard library:

    python3 verify.py > regenerated.json
    cmp regenerated.json CONTROL_RESULTS.json
    python3 verify_manifest.py

The controls are finite floating-point checks with explicit tolerances and deterministic exact integer/Fraction checks. They do not certify the analytic theorems; the proofs do. Only authored files and verification metadata belong in this public packet. No imported raw records, downloaded scholarly full text, or source images are included.
