# Depth relative to K-trivial oracles

The original classification remains **unsolved, 2/5**. [PARTIAL.md](PARTIAL.md) proves an elementary truth-table transfer lemma and derives a reduction to c.e. K-trivial oracles from Nies's published covering theorem. It also proves why a uniform output-preserving compiler cannot remove a noncomputable oracle; that obstruction does not decide the required nonuniform depth comparison. No novelty claim is made.

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) preserves the ordinary computable time-bound convention and exact known directions. [RESEARCH_LOG.md](RESEARCH_LOG.md) records the two stopped approaches. Independent review is pending.

Run `python verify.py` for bounded standard-library controls. They do not compute Kolmogorov complexity or decide any infinite depth question.
