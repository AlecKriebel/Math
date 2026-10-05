# A Dirichlet Series with Exactly One Zero

**30002507 / OWR-12866-017, queue rank 722. Original target unresolved after five substantive approaches.**

This is an AI-assisted, unrefereed research checkpoint. It does not claim a new theorem of priority, a complete solution, independent external human review, or an exhaustive certification of the current literature. A fresh independent audit is still required before any promotion or publication.

## Useful result

The packet proves a frequency-rounding and exact-zero-correction lemma. Applied to the credited Broucke–Vindas generalized-series example, it gives ordinary Dirichlet series converging on Re(s)>1/2 with a simple zero at 1 and rigorously controlled nonvanishing on any fixed prescribed compact zero-free region. The parameter depends on that region. Exclusion of further zeros at all heights remains unproved.

The remaining files prove restricted recurrence and representation obstructions, a sparse-prime perturbation theorem, and an explicitly conditional Möbius construction. These are retained as classical or elementary deductions and credited synthesis, without novelty claims.

## Read in order

1. `SCOPE.md`: exact ordinary-series question and boundaries.
2. `SOURCE_REVIEW.md`: primary-source status, especially the withdrawn claimed solution and the valid general-series result.
3. `TURN_1_RECURRENCE.md` through `TURN_5_GENERALIZED_ROUNDING.md`: complete retained arguments and exact gaps.
4. `STATUS.json`, `RESEARCH_LOG.md`, `REPOSITORY_CHECK.json`: disposition, approach accounting, and bounded earlier-attempt search.

## Reproduce

Run `python3 -B verify_manifest.py --replay` from this directory. The checker resolves its default root from its own location, so it also works from another working directory.

Run `python3 -B negative_controls.py` to reproduce the 12 damaged-package controls. Its output should match `NEGATIVE_CONTROL_RESULTS.json` exactly.

The mathematical controls use only Python integers and rational arithmetic: 67,207 finite predicates. They check algebra, finite Dirichlet convolutions, rounding inequalities, and negative examples. They are not numerical zero searches, not a proof of all-height exclusion, and not formal verification of the analytical arguments.

## Source and package boundary

Primary PDFs were read privately; their public URLs, byte counts, SHA-256 digests, inspection locations, and publicly stated version status are retained in `SOURCE_VERIFICATION.json`. No downloaded PDF, full extraction, page image, raw imported record, private source, or private coordination file belongs in this safe payload. The exact problem website was inaccessible, and the lost raw imported statement/prior AI report were not inspected. The 2014 primary question was independently checked.
