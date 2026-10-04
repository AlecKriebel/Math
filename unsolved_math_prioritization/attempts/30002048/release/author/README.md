# Exceptional-unit bounds by algebraic degree

Source problem 30002048 / OWR-11784-007. Full target status: **unsolved**.

The author packet gives height-unrestricted, exact computer-assisted proofs of the scoped equalities e(7)=5, e(8)=7, e(9)=6; an elementary proof for all roots of unity; and precise gaps for the all-degree conjecture. Historical novelty is not asserted. Fresh independent review is required before promoting the scoped results.

- `PROOF.md`: hypotheses, completeness argument, proofs, and scope.
- `ROUTES.md`: all five substantive mechanisms and their gaps.
- `SOURCES.md`: source correction, provenance, literature limits.
- `verify.py`: standard-library-only exact certificate generator.
- `results.json`: all residue, quartic-root, resultant, and witness certificates.
- `crosscheck_sympy.py`: a second mathematical implementation using SymPy.
- `CROSSCHECK.txt`: passed cross-check summary.
- `RESEARCH_LOG.md`: timestamped checkpoints and honest completion estimates.
- `STATUS.json`: machine-readable disposition.

Run `python3 verify.py > reproduced.json`, then `cmp reproduced.json results.json`.
For the second implementation, run `python3 crosscheck_sympy.py` with SymPy 1.14.0 (or a compatible version). The first verifier needs no third-party packages and takes under a second in the author environment. No search bounds, floating-point arithmetic, external data, network access, or source PDFs are needed.

The result does not justify a solved status for the source question, which asks for every degree d≥7. The remaining gap is non-root-of-unity algebraic integers in degrees d≥10.
