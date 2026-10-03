# Projective characters from centralizer p-element counts

Research package for Kourovka Notebook Problem 21.113 / UnsolvedMath 2622.

**Unresolved after five substantive mathematical attempts. No proof or counterexample to the full conjecture is claimed. Independent audit pending.**

## What is established here

1. Exact averaging through quotients and a centerless, directly indecomposable, O_p-free reduction for a least-order projective counterexample.
2. A Fourier/Mobius fiber formula for induced linear characters, including two positive inducing cases and exact small-group checks.
3. A pure-p/mixed-order decomposition, with an explicit negative mixed correction in C6 and an index obstruction to a universal permutation realization.
4. An ordinary but nonprojective p-vanishing character in A5, contrasted with an explicit projective tensor-square realization of the actual Psi.
5. An exact proper-centralizer subtraction formula whose unproved componentwise domination is the final obstruction.

These are partial research notes and proof-route diagnostics. Much of the structural baseline and all known group-family resolutions are prior literature, credited in SOURCE_GATE.md and in the attempt notes. No novelty or historical-priority claim is made. The A5 example in Attempt 4 concerns a different character and does not refute the problem.

## Verification

Run `python verify_examples.py` and `python verify_a5_characters.py` with Python 3.8 or later. Both use only the standard library. The first performs bounded exact permutation calculations; the second uses exact arithmetic in Q(sqrt(5)). Their output JSON files record the scope of the checks. Neither is a general computational proof.

## Reading order

SOURCE_GATE.md records source versions and limitations. The five numbered notes record distinct mathematical attempts. RESEARCH_LOG.md records progress. Source PDFs, screenshots and catalogue datasets are not distributed in this package.
