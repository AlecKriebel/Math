# Fixed-camera complex integral-curve reconstruction

Scoped disposition: **scoped_resolved1/5** (2026-10-16). Catalogue ID 20000188; authoritative queue row 1792.

This is an established-tools synthesis for two fixed full-rank pinhole cameras over C with distinct centers and reduced integral closed image/world curves. It supplies complete existence and degree classifications and necessary-and-sufficient embedded-smoothness criteria within the explicit [contract](CONTRACT.md). It makes no novelty claim and does not settle every interpretation of AIM Reconstruction Problem 1.4.

Read [the scope and result guide](RESULTS_AND_SCOPE.md), the complete authored proofs below, and the [independent mathematical audit](audit/INDEPENDENT_AUDIT.md). The proofs have been preserved in full. Administrative wording, completed-audit cross-references, and one reproduction command are adapted for a portable public edition; [acceptance bindings](audit/ACCEPTANCE.json) distinguish exact copies from presentation-only edits.

## Reproduce

Use Python 3.12 and SymPy 1.14.0 (listed in requirements.txt). From this directory:

    python verify_package.py

The verifier checks the complete manifest, then copies the disclosed tests and expected outputs into a fresh temporary directory. It reruns all 13 fixture groups and all 430 monomial checks, compares outputs byte for byte, and leaves this package unchanged. It does not use network access or third-party source files. For integrity only, use `python verify_package.py --integrity-only`.

A successful replay certifies the finite fixtures, not the universal theorem. The general decision criterion is proved using standard terminating subroutines under effective exact-coefficient assumptions. No general reconstruction solver, arbitrary-input absolute-decomposition engine, or arbitrary-input smoothness application is implemented here.

## Complete proof and audit files

- [Global classification and degree formulas](global/GLOBAL_CLASSIFICATION.md)
- [Embedded smoothness](local/EMBEDDED_SMOOTHNESS_CRITERION.md)
- [All-degree sharpness families](local/SHARPNESS_FAMILIES.md)
- [Exceptional epipolar-plane classification](exceptions/EXCEPTIONAL_CLASSIFICATION.md)
- [Finite algebraic criterion](algorithm/authored/FINITE_ALGEBRAIC_CRITERION.md)
- [Prior art and clean-case monodromy audit](algorithm/authored/PRIOR_ART_AND_MONODROMY_AUDIT.md)
- [Exact fixture explanations](exact/EXACT_EXAMPLES_AUDIT.md)
- [Independent mathematical acceptance](audit/INDEPENDENT_AUDIT.md)
- [Source provenance and limits](SOURCES.md)
- [Build replay evidence](REPLAY_REPORT.json)

Only authored mathematics, exact tests, acceptance reports, and public verification metadata are included. Source PDFs, extracted source text, dataset records/contents, and personal information are not included.
