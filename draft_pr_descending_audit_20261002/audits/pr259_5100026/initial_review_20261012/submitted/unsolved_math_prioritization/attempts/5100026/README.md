# 5100026: k407 outer focal-antipedal vertex centroid

Full first-turn author candidate; independent review pending. Read PROOF.md for the exact theorem, all real constructions, complete complex singularity classification, four-period exception and original-focus convention. This is a vertex centroid, so signed-area zeros do not cause a quotient problem.

- SOURCE_GATE.md and SOURCES.md preserve the exact source and prior-attempt gate
- TURN_1_CHECKPOINT.md preserves the initial mechanism; PROOF.md is the complete current argument
- verify_exact.py / exact_checks.json give reproducible symbolic and integer controls
- verify_numeric.py / numeric_checks.json give separately labeled high-precision diagnostics
- FROZEN_MANIFEST.json pins the packet used by a separate reviewer

Run `python verify_exact.py` and `python verify_numeric.py`; dependencies are SymPy and mpmath. Neither script reads source PDFs, private files or an absolute workspace path. Source reading copies are intentionally excluded. No historical novelty certification is asserted, and no claimed-result PR is authorized by the author freeze alone.
