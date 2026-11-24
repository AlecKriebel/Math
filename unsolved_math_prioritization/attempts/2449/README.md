# Erdős Problem 1038: bounded upper-bound reproduction and audit

Database problem ID: 2449. Review date: 2026-10-11 (UTC).

## Accepted result

For nonconstant monic real polynomials whose roots all lie in [-1,1], the infimum of the measure of the strict sublevel set |f|<1 is strictly below 1.834430475762662. The report independently reconstructs a fixed rational one-cut candidate, credits the construction to Shouqiao Wang's proposal and Terence Tao, and proves recovery by admissible finite polynomials. It claims no novelty.

The full proposed exact resolution remains unaccepted here. The matching lower bound, unique global minimizing parameter, and global nonattainment assertion still require independent acceptance of Certificates 6.1 and 7.1. No counterexample to the proposal was found. The known supremum 2sqrt(2) is retained with explicit dependence on Tao's external Theorem 2.1; its entire proof was not re-proved in this audit.

## Contents

- INDEPENDENT_UPPER_BOUND.md: complete authored upper-bound proof, exact rational parameter and root brackets, rigorous logarithm remainders, zero count, positive-platform perturbation, and empirical-polynomial recovery
- AUDIT.md: complete mathematical/source audit, both unresolved certificate gates, interval-software boundaries, and the one-sided hardcoded-upper-comparator bridge
- ACCEPTANCE.md: accepted and unaccepted statements, source and computational boundaries, and next acceptance requirements
- SOURCE_PINS.json: public bibliographic metadata, source hashes and byte counts, retrieval and inspection history, and manuscript status
- CHECK_SUMMARY.json: aggregate integrity and independent exact-arithmetic verification records
- MANIFEST.json: closed content inventory, excluding its own hash to avoid circularity

## Reading the verification record

The mathematical proof and rational formulas are the evidence for the upper bound. Hashes identify the exact reviewed artifacts; they are not proofs. The report includes enough exact rational witnesses and remainder formulas for independent arithmetic rederivation, but excludes executable checker code and does not claim to be a complete public computational replay package. The source author's verifier and linked Lean project were not executed.

Only the authored proof, mathematical audit, acceptance report, necessary proof witnesses, public source metadata, and aggregate verification are included. Copied source documents, extracted source text, source images, executable code, datasets, and nonpublic coordination material are excluded.
