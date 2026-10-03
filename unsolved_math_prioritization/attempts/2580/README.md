# Euler characteristics over two fields

Research notes for **Kourovka Notebook Problem 21.71**, UnsolvedMath ID **2580**, proposed by **D. Kielak**.

**Status: UNSOLVED in this investigation; five substantive attempts completed.** No proof of universal equality and no example satisfying both FL hypotheses with distinct Euler characteristics was obtained. No novelty or first-resolution claim is made.

The question asks whether a group whose trivial group-algebra module has a finite, finitely generated free resolution over each of two fields can have different ordinary homological Euler characteristics over those fields. The original question is in the October 2026 Notebook, printed page 187. It is different from the adjacent Poincare-duality problem 21.70.

## Contents

- `turn_01.md`: same-characteristic and common-resolution reductions; avoids falsely descending FL from an extension field.
- `turn_02.md`: exact universal-coefficient defect identity; the real near-counterexample Z[1/p] and its failure of finite generation.
- `turn_03.md`: the BS(1,p) repair and general cancellation for finite-homology-by-Z extensions.
- `turn_04.md`: the established Bestvina-Brady chain formula excludes ordinary Bestvina-Brady groups; exact finite examples.
- `turn_05.md`: constructive product-ring free-resolution synchronization criterion and the precise remaining obstruction.
- `verify_partial_results.py`, `verification.json`: reproducible exact small checks.
- `SOURCES.md`: primary references, attribution and dated retrieval limits.
- `RESEARCH_LOG.md`: scope of the five actual attempts.

## Main useful conclusion

A positive example must use fields of different characteristics and non-finitely-generated integral homology in degree at least 2. Common finite-rank models, ordinary Bestvina-Brady kernels, and finite-homology-by-cyclic repairs do not supply such an example. The defect formula and product-ring synchronization criterion isolate the missing construction or comparison theorem without claiming it exists.

## Verification

Run `python3 verify_partial_results.py`. The script needs only Python's standard library. It recomputes exact rational/modular simplicial homology for six small examples, 35 Baumslag-Solitar Betti calculations, and 8,092 equal-Euler rank-vector synchronization cases. These checks are finite algebraic sanity checks, not an exhaustive search or a proof of the open question.

The written arguments provide the scoped mathematical deductions. Independent review is required before publishing this research package as an audited deliverable. Source PDFs, source screenshots and private context are excluded from the package.
