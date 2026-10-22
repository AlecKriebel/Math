# Independent literature and target audit

Date: 2026-10-04. Target: rank 621 / 30001721 / OWR-4800-012.

## Verdict

**PASS for target identification and conservative `unsolved` classification.** The reviewed sources do not establish the universal assertion. No all-roots resolution was found in the bounded independent search through the audit date. This is not a claim of exhaustive bibliographic coverage. The author's distinction between real roots and real Schur roots is necessary and correct; removing it would introduce a substantive error.

The author files were read without alteration. The primary OWR report and Weist 2011 version were independently retrieved online. OWR printed p. 594 was also checked visually from the available PDF. Later central papers were checked using their supplied primary texts, with current online metadata and independent follow-up searches. No source fulltext is reproduced here.

## Exact primary target

Thorsten Weist's contribution, “Localization in quiver moduli spaces and tree modules,” begins on printed p. 594 of *Oberwolfach Reports* 8 (2011), report 10, pp. 523–608. It fixes the field as C and excludes oriented cycles. Its exact existence question is:

> Does there exist an indecomposable tree module for every root d ∈ N^{Q₀}?

Here the coefficient quiver has basis vectors as vertices and a separately arrow-labelled edge for each nonzero matrix coefficient. The adjacent conjecture requesting multiple isomorphism classes for imaginary roots is stronger and separate. The author's nonzero positive-root, finite-dimensional reading and multigraph convention match the intended problem. Theorem 2, p. 596, handles generalized Kronecker quivers; Theorem 3, p. 597, handles imaginary Schur roots. Neither is the universal target. [Publisher](https://ems.press/journals/owr/articles/4800); [primary PDF](https://ems.press/content/serial-article-files/46329?nt=1).

## The crucial real/Schur distinction

[Ringel, *Exceptional modules are tree modules* (1998)](https://doi.org/10.1016/S0024-3795(97)10046-5) proves the result for indecomposables without self-extensions. “Real root” cannot simply replace this hypothesis. For a real root, the Euler identity permits dim End = 1 + dim Ext¹, so uniqueness of the indecomposable does not imply rigidity or scalar endomorphisms. The report's four-subspace example is consistent with this distinction.

[Weist, *Tree modules*, arXiv:1011.1203v3](https://arxiv.org/abs/1011.1203v3), dated 18 October 2011, has the following exact scope:

- Theorem 3.17, printed p. 14: every isotropic root, including divisible ones, has multiple indecomposable tree-module isomorphism classes.
- Theorem 3.18, printed p. 14: every Schur root has an indecomposable tree representative, with multiplicity for imaginary Schur roots.
- Introduction, pp. 1–2, expressly limits the methods on non-Schur roots.
- Example 4.1, pp. 15–16, gives an eight-subspace real non-Schur root for which the indicated reflection construction fails. This is an obstruction to that construction, not a counterexample to tree existence.

Consequently, the abstract's broader “recipe” language does not justify an all-roots theorem. The author's exact version and theorem numbers are correct; publication numbering can differ.

## Later central sources

1. [Weist, *On the recursive construction of indecomposable quiver representations*](https://arxiv.org/abs/1310.2757), published 2015: Theorem 2.7 preserves indecomposability under covering pushdown, and Proposition 2.8 gives compatible roots on the universal cover. Question 4.1, p. 17 of the checked text, remains an explicit recursive-decomposition question. The proof of Proposition 2.8 contains an overbroad assertion that every fundamental-domain root is Schur: divisible isotropic roots require separate treatment. The author's caution and use of the independently available covering formula avoid silently relying on that assertion.

2. [Franzen–Weist, *The value of the Kac polynomial at one*](https://arxiv.org/abs/1608.03419), published 2018: Corollary 1.2 gives a universal-cover formula. Corollary 8.2's equality between the tree count and the polynomial's value at one assumes exceptional compatible roots. Question 8.8 explicitly asks the general tree-count lower bound. The report correctly declines to convert the covering identity alone into tree-module existence.

3. [Kinser–Weist, *Tree normal forms for quiver representations*](https://arxiv.org/abs/1810.04977), published 2019: Conjecture 4.11 is a stronger cellular-normal-form conjecture. Theorem 6.10 assumes an isotropic Schur root with sl(δ)=1; Remark 6.11 describes what is still missing for higher Schur level. These are restricted results. The author supplies no inappropriate universal inference.

4. [Franzen–Weist, *Non-Schurian indecomposables via intersection theory*](https://arxiv.org/abs/1508.04643): the abstract concerns three-vertex acyclic quivers and an intersection-theoretic construction preserving indecomposability. Its scope does not supply the missing arbitrary-quiver tree-existence theorem.

## Recent search checks

The following primary abstracts were independently screened as possible later resolutions; none asserts the target:

- [Kleinau, *Scalar extensions of quiver representations over F₁*](https://arxiv.org/abs/2403.04597): scalar extensions and combinatorial morphism/indecomposability questions.
- [Sengupta–Kuber, *Generalised tree modules: Hom-sets and indecomposability*](https://arxiv.org/abs/2504.18996): zero-relation algebras and sufficient criteria, as the author already notes.
- [Mishra–Kuber, *Rooted tree modules*](https://arxiv.org/abs/2508.07435): a rooted class, an indecomposability criterion in characteristic other than two, and recursive constructions.
- [Sengupta, *Tree Bricks and Finite Tree Automata*](https://arxiv.org/abs/2609.22406), submitted 18 September 2026: automata and brick recognition for Crawley-Boevey tree modules over zero-relation algebras. It is a particularly recent related result, but its abstract neither asserts existence in every root dimension nor resolves the non-Schur cases.

These recent checks are abstract-level scope checks, not full audits of their proofs. Searches included exact tree-module/all-root/conjecture phrases, real non-Schur roots, and dated 2024–2026 follow-ups. Search-result crawl dates were not mistaken for publication dates.

## Recommendation

Retain `unsolved` and the existing caveat that remaining coverage cannot be described as only imaginary non-Schur roots. There is no source-scope blocker to the report. Optionally add the September 2026 paper to the bounded-search note to document the latest independently screened related work; it does not change the outcome. No assertion of mathematical novelty or global literature completeness is warranted by this audit.
