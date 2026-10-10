# Kourovka 21.39 investigation

**Unresolved after five substantive approaches.** No non-residually-finite example satisfying all hypotheses, and no general impossibility theorem, was obtained. These are scoped, independently checkable reductions and boundary examples. No novelty or priority is claimed.

The October 2026 edition, printed page 182, asks:

> Are there any locally finite, characteristically simple groups with finitely many orbits under automorphisms that are not residually finite?

The authors are A. Dantas and E. de Melo. The inspected edition has no solved or unverified-AI marker on 21.39. This is not a proof that no later or unindexed solution exists.

## Retained results

- A countable-reflection theorem preserves all target hypotheses and does not increase the automorphism-orbit count.
- Any requested example is perfect and centerless, has finite exponent, has no nontrivial finite quotient, and has finite commutator width.
- Boolean A5 functions on pointed Cantor space give a complete eight-orbit, residually finite positive control.
- A dense triangular McLain group has the characteristic-simplicity and finite-quotient properties, but unbounded element orders force infinitely many automorphism orbits.
- An infinite extraspecial odd-p group has exactly three orbits and finite residual equal to its center. That nontrivial proper characteristic center prevents it from answering the problem.
- A finite class-two amalgam gives an exact obstruction to a naive bounded-class homogeneous construction. A separate proof excludes pseudofinite perfect p-group candidates with finite orbit count.

Start with [RESULT.md](RESULT.md), then [PROOFS.md](PROOFS.md). [RESEARCH_LOG.md](RESEARCH_LOG.md) records the five approaches and their precise stopping points. [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) distinguishes inspected primary material from bibliographic leads.

## Reproduction

Python 3.10 or later, standard library only:

    python verify_math.py
    python verify_manifest.py

The mathematical controls pass 116,329 exact assertions, including negative controls. They test explicit finite models; they do not prove the original infinite-group existence statement or replace independent proof review.

Only authored proofs, authored code, verification results, and public source/dataset metadata belong to this package. Scholarly PDFs, extracted source text, dataset records, and private correspondence are excluded.
