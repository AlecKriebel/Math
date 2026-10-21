# Affine vertices: scoped partial results

Problem 6000013 / AMR-059-0013. Status: UNSOLVED, substantive partial progress after five approaches. Date: 2026-10-21.

A vertex here is a noninflectional sextactic point: osculating-conic contact of order at least six. The historical question does not explicitly specify that convention or the intended compatibility/completeness hypotheses.

Three accepted authored partials are included:
- A compact complex-compatible affine flat torus admits an embedded essential spiral with V=I=0.
- Periodic graphs on a translation torus satisfy V>=I for isolated inflections, even infinitely flat ones; sine examples are sharp.
- Contractible strictly convex ovals with I=0 and exactly V=2n exist for each integer n>=3, on a fixed torus.

These do not classify all possible relations between V and I. No novelty or priority claim is made. Sasaki's 1995 full text is uninspected. The incomplete non-equiaffine spiral is not a contradiction to classical complete or equiaffine results. The proof texts, not finite numerical or symbolic experiments, justify the general propositions.

## Reproduction

Requires Python 3 and SymPy. From this directory run:

    python verify.py
    python -O verify.py
    python test_checks.py
    python -O test_checks.py
    python inventory.py

verify.py uses explicit exceptions, not assert statements. It is an AST-equivalent transformation of the research check script, replacing each assert condition with an explicit if-not condition and RuntimeError. Test checks mutate actual mathematical constants and expressions and require failures in ordinary and optimized Python. All successful verifier output must exactly equal VERIFY_OUTPUT.txt. inventory.py checks the entire recursive tree, including nested MANIFEST.json files; only the root MANIFEST.json is excluded from self-inventory. No copied source document or dataset extract is included.
