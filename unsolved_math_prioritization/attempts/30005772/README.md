# Negative fixed-point colors: verified candidate partial results

Problem **30005772 / OWR-14298158-017**, rank 494.

**Overall status: unresolved after five substantive approaches.** The packet contains a complete algorithmic cancellation construction for the even-size subquestion, local models at `k=-1`, and eventual unsigned models at each negative integer. It does not claim a structural all-size interpretation, historical novelty, or human peer review. A fresh independent audit is required before accepting these candidate results.

## Main deliverable

Read [PROOF.md](PROOF.md), particularly its opening scope statement.

- Theorem 1 gives `A(2n,k)` as the cardinality of a specified finite set for every integer `k`, with an explicit sign-reversing involution transported back to colored permutations. It uses **global ordered-prefix cancellation**; the resulting interpretation is generic and potentially expensive, and no stronger naturalness claim is made.
- Theorem 2 gives a local colored-walk model for `A(2n,-1)`. A fixed nonnegative terminal vector extends it to every odd size at least five; sizes one and three retain their negative signs.
- Proposition 3 proves that squaring the classical Jacobi matrix and merely changing vertex signs cannot produce an entrywise nonnegative matrix for any integer `k<=-2`.
- Theorem 6 and equation (19) give an unsigned finite-band walk model for every negative integer `k` at all sizes `N>=4(1-k)`.
- The remaining odd-size difficulty and the limitations of the generic models are explicit. The known signed fixed-point formula, recurrence, exponential generating function, Laguerre history framework, and even-moment positivity are credited as prior mathematics.

## Reproduction

Run `python3 check_exact.py`. It uses only the Python standard library, performs no network operations and writes a deterministic JSON report to standard output. Compare the output with `exact_results.json`.

The author run passes **124,917 assertions**, including exhaustive permutation/history round trips through size six with zero to three colors, actual transported cancellation involutions, integer sum-of-squares identities, Laguerre linearization coefficients, local and eventual graph counts, and negative-cycle obstruction certificates. These finite checks do not replace the general proofs.

## Files and status

- [SOURCE_GATE.md](SOURCE_GATE.md): exact source, bounded history/literature checks, and scope.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): five substantive mathematical approaches and their outcomes.
- [check_exact.py](check_exact.py) and [exact_results.json](exact_results.json): reproducibility.
- `FROZEN_AUTHOR_MANIFEST.json`: SHA-256 seals of the author files at audit handoff, excluding the manifest itself.

This packet contains original exposition and small verification code. It excludes downloaded source PDFs, page images, full extracted source texts, raw catalogue records, and private history. No repository mutation or remote publication was performed while preparing it.
