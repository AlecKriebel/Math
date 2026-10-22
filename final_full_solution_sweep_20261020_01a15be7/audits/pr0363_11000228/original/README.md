# Problem 11000228: qualified source-verification hold

**Queue remains queued, 0/5.** The entire QUEUE file is unchanged by this draft. Independent review passed only for the accuracy of this qualified source report and its arithmetic; it did **not** certify the full classification proof.

The original Exceptional Strata problem asks for a geometric component invariant for four quadratic-differential strata. Chen–Möller (2014) report an algebro-geometric h⁰ invariant. This packet recovers the exact original scope, including the nonsquare convention and exclusion of poles from the divided zero divisor. It preserves the separate, still-open flat-geometric description. [Published theorem](https://doi.org/10.24033/asens.2216).

The proof audit records an unresolved local dimension calculation in Appendix B.5 and traces its use through Lemma 7.7 to Theorem 7.1. It does not claim that the main theorem is false, supply an unproved repair, or convert a later restatement into independent proof verification.

- [Source status](SOURCE_STATUS.md)
- [Original versus modern scope](SCOPE_COMPARISON.md)
- [Exact dependency issue and limitations](PRIOR_PROOF_AUDIT.md)
- [Independent qualified review](final_review/REVIEW.md)

All ten frozen report files and all frozen review files are preserved. Their historical pending-review wording is retained; this wrapper records the completed qualified review. No mathematical author turn was used.

## Replay

Standard-library Python only:

    python verify_source_alignment.py > /tmp/alignment.json
    cmp SOURCE_CHECKS.json /tmp/alignment.json
    python final_review/run_portable.py --math-only

The report has 363 arithmetic/scope controls. Portable source-free review has 33 checks, explicitly omitting four source hashes. For the historical 37-check receipt, supply the four primary PDFs using the filenames and hashes in SOURCE_MANIFEST.json:

    python final_review/run_portable.py --sources /path/to/source-pdfs > /tmp/review.json
    cmp final_review/INDEPENDENT_CHECKS.json /tmp/review.json

These controls are not a connected-component classification proof. Raw PDFs, imported reports and private material are excluded. No authors were contacted.
