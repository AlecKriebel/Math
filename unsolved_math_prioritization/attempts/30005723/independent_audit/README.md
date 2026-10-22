# Independent audit package

Verdict: **PASS_PARTIAL**. The five-attempt research note is mathematically
consistent within its stated limits. Neither original continuum question is
solved.

- `AUDIT_REPORT.md`: source, domain, localization, exact-identity and finite-model audit
- `audit_controls.py`: independent controls and isolated replay of the author's verifier
- `control_results.json`: exact/numerical/negative-control results and integrity checks
- `verdict.json`: concise machine-readable disposition

From the research package root, run:

    python independent_audit/audit_controls.py

Python 3, SymPy and mpmath are required. The program verifies the pinned manifest
and all 12 frozen files before and after its checks. It executes the author's
verifier only from a temporary copy, so frozen results are not overwritten.
It writes `independent_audit/control_results.json` only.

The 23 exact assertions, five high-precision numerical checks and eleven
negative controls are supplementary to the analytical audit. Numerical checks
are not interval arithmetic, continuum convergence, or continuum witnesses.
No source PDFs or source corpus files belong in this folder.
