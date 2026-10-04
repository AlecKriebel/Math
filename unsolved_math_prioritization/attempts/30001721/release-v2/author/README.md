# Tree modules: rank 621, problem 30001721

Status: **unsolved**. Five approaches tested; no full proof or counterexample claimed.

- [REPORT.md](REPORT.md): exact target, five approaches, elementary proofs, counter-controls, and remaining gap.
- [SOURCES.md](SOURCES.md): primary-source locations and limitations.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated investigation record and completion estimates.
- [RESULT.json](RESULT.json): machine-readable outcome.
- [verify_tree_controls.py](verify_tree_controls.py): exact rational endomorphism-algebra tests and support enumeration.
- [control_results.json](control_results.json): reproducible results.

Reproduce with Python 3.12 and SymPy 1.14.0:

    python verify_tree_controls.py --extended-control --output reproduced_results.json
    diff -u control_results.json reproduced_results.json

The extended control completes in roughly half a minute in the development environment; runtime is machine dependent. Omitting --extended-control runs only the three small enumerations. No network, source corpus, downloaded paper, or private coordination file is needed. The script makes no repository or service changes.

Counts are labelled coefficient supports, not isomorphism classes. Indecomposability is tested over C using exact rational arithmetic and the regular trace form; it is not inferred from connectivity or End dimension alone. All examples are controls, with no novelty claim.
