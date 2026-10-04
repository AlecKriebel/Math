# Problem 2303002: credited harmonic-path resolution

**Reviewed disposition: already_solved, 0/5. Independent full source/proof review: PASS.**

Every nonconstant real-valued harmonic function on all of R^n, n >= 3, has a proper locally polygonal path to infinity along which its value tends to positive infinity. The original Hayman–Lingham Update 3.2 already records this affirmative result, crediting Fuglede and Carleson's polygonal strengthening. [Original source and update](https://arxiv.org/abs/1809.07200).

The imported open triage missed that update. This is prior mathematics, with no novelty claim.

- [Source status](SOURCE_STATUS.md)
- [Complete continuous-case proof verification](SOURCE_PROOF.md)
- [Exact scope and path meaning](SOURCE_NORMALIZATION.md)
- [Independent full review](final_review/REVIEW.md)

The proof uses the ball Poisson formula and maximum principle, an explicit bounded-piece lemma, nested components where the function remains unbounded, and an entire-tail compactness argument. It establishes a proper path, not merely an escaping sequence. No prescribed ray or quantitative growth rate is asserted. The discontinuous-subharmonic extension is not needed or independently recertified.

All ten frozen source/proof files and the review are unchanged. Historical pending-review wording is retained; this wrapper records the completed PASS.

## Replay

Standard-library Python:

    python verify_source_alignment.py > /tmp/alignment.json
    cmp SOURCE_CHECKS.json /tmp/alignment.json
    python final_review/run_portable.py --math-only

There are 3,675 author arithmetic controls. Source-free independent replay runs 1,665 checks, explicitly omitting two PDF hashes. To reproduce the historical 1,667-check receipt, obtain the two PDFs using the filenames and hashes in SOURCE_MANIFEST.json:

    python final_review/run_portable.py --sources /path/to/source-pdfs > /tmp/review.json
    cmp final_review/INDEPENDENT_CHECKS.json /tmp/review.json

Finite controls support the formulas but do not replace the analytic proof. The original review script is preserved byte-for-byte. No raw PDFs, imported records or private material are redistributed.
