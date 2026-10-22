# Fixed-camera compatibility: epipole overlap corrections

Numeric target: **20000185**, AIM-ALGEBRAIC_GEOMETRY-0185, AIM Algebraic Vision Problem 1.25.

**Status: unsolved; five substantive approaches recorded.** The source asks broadly about compatibility of two curve views. This packet gives a scoped characteristic-zero algebraic classification for integral reduced images, with exact degree and baseline-multiplicity formulas in the epipole-incidence regime. It does not claim to settle every real, visible, scheme-theoretic or degree-constrained interpretation of the source question.

The clean epipolar fiber-product construction, cover-isomorphism criterion, gcd bound and classical Hurwitz count are credited background. No novelty or first-priority claim is made. This is AI-assisted, unrefereed work, subject to independent mathematical and source review.

## Main calculation

For an irreducible normalized correspondence component, let N be its moving epipolar-pencil degree and let A,B be the two pulled-back epipole base divisors. Then

    world degree = N + degree(max(A,B)).

The two camera-center multiplicities are degree((B-A)_+) and degree((A-B)_+). Across all components, the baseline cycle multiplicity is

    alpha beta + sum degree(min(A,B)),

where alpha,beta are the two image epipole multiplicities. The maximum and minimum are coefficientwise divisors on the same normalized component, not maxima or minima of total degrees.

Examples with two conic images give a degree-two residual plus a double baseline, or a degree-three residual plus a simple baseline. A line and conic can also have a birational common realization. These verify why the clean degree formula cannot simply be reused at epipoles.

## Files

- `PROOF.md`: exact scope, proofs, known-source attribution, examples, and remaining gaps
- `RESEARCH_LOG.md` and `turns.jsonl`: five distinct substantive approaches and outcomes
- `SOURCE_GATE.md` and `SOURCE_MANIFEST.json`: source identity, prior work, retrieval limits, metadata-only provenance
- `verify.py` and `CONTROL_RESULTS.json`: reproducible exact finite controls
- `STATUS.json`: machine-readable disposition
- `SHA256SUMS.json` and `verify_manifest.py`: frozen-file integrity

Run with Python 3 and SymPy 1.14:

    python verify.py
    python verify_manifest.py

The author run passes 8,625 assertions, covering 1,225 rational image pairs, five generic-baseline local-length calculations over QQ(z), three saturated ideal examples, 40 classical monodromy classes, and real/inseparable boundary controls. Tests are finite algebraic controls, not a formal proof or a novelty certificate.

No source PDFs, source-page copies, dataset contents, or private coordination files are included.
