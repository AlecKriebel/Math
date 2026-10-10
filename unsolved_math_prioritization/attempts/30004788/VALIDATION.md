# Exact-check scope

The checker uses rational/integer arithmetic and explicit exceptions, not Python
assert statements. Baselines were executed successfully under Python's normal,
-O, and -OO modes as UID1000. Each returns the same six orbit dimensions and
114 polynomial-support test cases.

Four deliberate corruptions were rejected in each mode:

- Replacing the repeated-root Jordan action by a split scalar action
- Merging two different orbit representatives
- Identifying unequal Fitting ideals
- Dropping a required polynomial factor

All twelve runs failed with the intended explicit RuntimeError and exit1.
These tests exercise error detection even when Python optimization removes
assertions. They are limited exact checks, not a representation-theoretic proof.

The published negative independence example is an application of Prasad's
1993 Theorem1. The full source theorem and its hypotheses were read, and the
original page169 was visually inspected. The two principal series are
irreducible because equal inducing-character ratios are1, not |.|^(+/-1).
The nontrivial unramified unitary character may be chosen with value-1 on a
uniformizer. No numerical experiment is needed for that argument.

No general restriction model, new theorem of p-adic branching, or novelty
certificate is supplied. The conditional lattice lemma and elementary ideal
example in the analysis are self-contained; their application to a complete
Hecke-module reconstruction remains unfinished.

Only authored analysis/check code and public bibliographic verification metadata
belong in this packet. Source PDFs and text are not included.

## Audited derivative

This derivative adds the explicit Bernstein projection and quotient argument,
clarifies the trivial target's normalized cuspidal support and central characters,
and records both Wang papers' characteristic-zero hypotheses. It also corrects
the pinned Chan v3 PDF page count to 78 and makes the support-test comment
strictly algebraic. The mathematical outcome remains partial and unresolved.
Independent rerun results are supplied in the accompanying audit.
