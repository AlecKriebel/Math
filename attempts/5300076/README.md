# 5300076: audited power-law lift partials

**Unsolved, 5/5 substantive approaches.** The separate adversarial audit passed the exact frozen author's partial results with no blocking mathematical correction.

- For every real alpha>1, the lift sequence converges when the critical point has exact period two. The proof uses a global logarithmic contraction.
- There are explicit nontrivial two-cycles of the conjugated-map sequence with a fixed critical point, while the lift sequence stays constant.
- The full lift-convergence question for periodic/preperiodic kneading remains unresolved by this work.

Read [the proofs](author/RESULT.md), [the independent audit](independent_review/AUDIT.md), and [the scope addendum](SCOPE_ADDENDUM.md). The addendum adopts all four audit clarifications. Original files retain their historical pre-audit status and timestamps for byte-preserving reproducibility; this README records the completed review. No novelty or human peer-review claim is made.

The final layout preserves all twelve author files and thirteen audit files unchanged. The independent suite does not import author functions. With Python 3.10+ and the standard library:

    python3 replay.py > /tmp/5300076-replayed.json
    cmp /tmp/5300076-replayed.json PUBLICATION_CHECK_RESULTS.json

Place generated output outside this directory when subsequently running the strict inventory check:

    python3 verify_publication_manifest.py

The replay runs 48,709 author assertions and 4,812 independent assertions. `NEGATIVE_CONTROL_RESULTS.json` records that file corruption and unlisted additions are rejected. Floating-point diagnostics are not universal proofs; the analytic arguments establish the claimed conclusions. Downloaded scholarly PDFs/full text, source screenshots, imported corpus contents, and private coordination files are excluded.
